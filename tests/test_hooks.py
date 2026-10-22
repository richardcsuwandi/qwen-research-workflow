import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / ".qwen" / "hooks" / "git-guardrails.py"


def run(tool, tool_input, env=None):
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
        capture_output=True, text=True, env=env,
    )
    return proc, (json.loads(proc.stdout) if proc.stdout.strip() else None)


class GuardrailTests(unittest.TestCase):
    def assertDenied(self, command):
        proc, out = run("run_shell_command", {"command": command})
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny", command)

    def assertAllowed(self, command):
        proc, out = run("run_shell_command", {"command": command})
        self.assertEqual(proc.returncode, 0)
        self.assertIsNone(out, command)

    def test_blocks_destructive_git(self):
        for cmd in ("git reset --hard HEAD", "git clean -fd", "git push --force origin main",
                    "git add -A", "git -C /repo reset --hard"):
            self.assertDenied(cmd)

    def test_allows_normal_git(self):
        for cmd in ("git status", "git add Slides/talk.tex", "git push --force-with-lease origin x",
                    "git commit -m 'update'"):
            self.assertAllowed(cmd)

    def test_ignores_other_tools(self):
        proc, out = run("read_file", {"file_path": "x.tex"})
        self.assertEqual(proc.returncode, 0)
        self.assertIsNone(out)

    def test_hardcoded_path_warns_but_allows(self):
        proc, out = run("write_file", {"file_path": "a.py", "content": "p = '/Users/bob/data'"})
        self.assertEqual(proc.returncode, 0)
        self.assertIsNone(out)
        self.assertIn("Hardcoded machine path", proc.stderr)

    def test_strict_paths_denies(self):
        import os
        env = dict(os.environ, QWEN_STRICT_PATHS="1")
        proc, out = run("write_file", {"file_path": "a.py", "content": "p = '/home/bob/data'"}, env=env)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_malformed_input_fails_open(self):
        proc = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
