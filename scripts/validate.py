#!/usr/bin/env python3
"""Validate the Qwen Code configuration in this repository.

Checks skills, agents, rules, hooks and settings against what Qwen Code accepts,
and flags leftovers from the Claude Code original. Exits 1 on any problem.
"""
from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QWEN = ROOT / ".qwen"
NAME_RE = re.compile(r"^[\w:.-]+$", re.UNICODE)
TOOLS = {
    "read_file", "write_file", "edit", "glob", "grep_search", "run_shell_command",
    "web_fetch", "web_search", "agent", "skill", "todo_write", "list_directory",
}
LEFTOVERS = re.compile(r"\bClaude\b|\.claude/|CLAUDE\.md|\bQuarto\b|\.qmd\b")
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(path: Path) -> dict[str, object] | None:
    """Parse the small YAML subset used here, which is scalars and string lists."""
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
    if not m:
        return None
    out: dict[str, object] = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+-\s+", line) and key:
            out.setdefault(key, [])
            assert isinstance(out[key], list)
            out[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip("'\""))
        elif ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            out[key] = val.strip("'\"") if val else []
    return out


def check_skills() -> int:
    n = 0
    for d in sorted((QWEN / "skills").iterdir()):
        skill = d / "SKILL.md"
        if not skill.is_file():
            err(f"{d.name}: missing SKILL.md")
            continue
        n += 1
        fm = frontmatter(skill)
        if fm is None:
            err(f"{d.name}: no frontmatter")
            continue
        if fm.get("name") != d.name or not NAME_RE.match(str(fm.get("name", ""))):
            err(f"{d.name}: name must equal the directory name")
        if not fm.get("description"):
            err(f"{d.name}: empty description")
    return n


def check_agents() -> int:
    n = 0
    for f in sorted((QWEN / "agents").glob("*.md")):
        n += 1
        fm = frontmatter(f)
        if fm is None:
            err(f"agent {f.name}: no frontmatter")
            continue
        if fm.get("name") != f.stem:
            err(f"agent {f.name}: name must equal the file name")
        if not fm.get("description"):
            err(f"agent {f.name}: empty description")
        tools = fm.get("tools", [])
        if not isinstance(tools, list) or not tools:
            err(f"agent {f.name}: tools must be a non-empty list")
        else:
            for t in tools:
                if t not in TOOLS:
                    err(f"agent {f.name}: unknown tool {t!r}")
    return n


def check_rules() -> int:
    n = 0
    for f in sorted((QWEN / "rules").glob("*.md")):
        n += 1
        text = f.read_text()
        if text.startswith("---"):
            fm = frontmatter(f)
            if fm is None:
                err(f"rule {f.name}: malformed frontmatter")
            elif "paths" in fm and not isinstance(fm["paths"], list):
                err(f"rule {f.name}: paths must be a list")
    return n


def check_hooks() -> None:
    for f in sorted((QWEN / "hooks").iterdir()):
        if f.suffix == ".py":
            try:
                py_compile.compile(str(f), doraise=True)
            except py_compile.PyCompileError as e:
                err(f"hook {f.name}: {e}")
    settings = QWEN / "settings.json"
    try:
        cfg = json.loads(settings.read_text())
    except (OSError, json.JSONDecodeError) as e:
        err(f"settings.json: {e}")
        return
    for event, entries in cfg.get("hooks", {}).items():
        for entry in entries:
            for h in entry.get("hooks", []):
                m = re.search(r"\.qwen/hooks/[\w.-]+", h.get("command", ""))
                if not m or not (ROOT / m.group(0)).is_file():
                    err(f"settings.json {event}: hook script not found in {h.get('command')!r}")


def check_links() -> None:
    for f in list(ROOT.rglob("*.md")):
        if ".git" in f.parts:
            continue
        for m in re.finditer(r"(?<!\!)\[[^\]]+\]\(((?!https?:|#|mailto)[^)\s]+)\)", f.read_text()):
            target = m.group(1).split("#")[0]
            if target and not (f.parent / target).resolve().exists():
                err(f"{f.relative_to(ROOT)}: broken link {target}")


def check_leftovers() -> None:
    for f in list(QWEN.rglob("*")) + [ROOT / "QWEN.md"]:
        if f.is_file() and f.suffix in {".md", ".py", ".sh", ".json"}:
            for i, line in enumerate(f.read_text().splitlines(), 1):
                if LEFTOVERS.search(line):
                    err(f"{f.relative_to(ROOT)}:{i}: leftover {LEFTOVERS.search(line).group(0)!r}")


def main() -> int:
    ns = check_skills(), check_agents(), check_rules()
    check_hooks()
    check_links()
    check_leftovers()
    for e in errors:
        print("ERROR", e)
    print(f"{ns[0]} skills, {ns[1]} agents, {ns[2]} rules, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
