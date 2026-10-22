# qwen-research-workflow

A [Qwen Code](https://github.com/QwenLM/qwen-code) workflow for academic LaTeX and Beamer work. It bundles 14 skills, 6 read-only reviewer subagents, 8 path-gated rules and 4 hooks, so Qwen can compile your decks, proofread them, audit their layout, check your bibliography and verify factual claims in a fresh context.

It is a Qwen Code port of [richardcsuwandi/research-workflow](https://github.com/richardcsuwandi/research-workflow), which is itself a fork of Pedro Sant'Anna's [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow). The port keeps the LaTeX, Beamer, TikZ and citation-checking core and drops the R, Stata, Quarto and econometrics pieces.

## Get started

```sh
git clone https://github.com/richardcsuwandi/qwen-research-workflow.git my-project
cd my-project
qwen
```

Qwen Code reads `QWEN.md`, discovers `.qwen/skills`, `.qwen/agents` and `.qwen/rules`, and loads the hooks from `.qwen/settings.json` once you trust the workspace. Then try the sample deck.

```text
/compile-latex HelloWorld
/proofread Slides/HelloWorld.tex
/visual-audit HelloWorld
```

To add the workflow to an existing project, copy `.qwen/`, `QWEN.md`, `Preambles/` and `templates/` into it and edit `QWEN.md` to describe your project.

## What is in the box

### Skills

Type `/<name>` to run one directly. Skills marked slash-only never run unless you call them.

| Skill | What it does |
|-------|--------------|
| `/compile-latex` | Builds a deck with XeLaTeX and BibTeX, then reports overfull boxes and undefined citations |
| `/proofread` | Read-only grammar, typo, overflow and consistency pass that writes a report |
| `/visual-audit` | Layout audit of a Beamer deck, delegated to the `slide-auditor` agent |
| `/validate-bib` | Cross-checks citation keys against the `.bib` file and, in `--semantic` mode, looks for duplicates and drift |
| `/verify-claims` | Chain-of-Verification on a draft, run by a fresh-context `claim-verifier` |
| `/lit-review` | Searches and synthesizes literature, then verifies the citations it produced |
| `/devils-advocate` | Challenges the ordering, prerequisites and cognitive load of a deck |
| `/respond-to-referees` | Drafts a point-by-point response letter from a referee report and the revised manuscript |
| `/interview-me` | Turns a fuzzy idea into a structured research spec through a multi-turn interview |
| `/extract-tikz` | Extracts TikZ blocks from a deck into standalone PDFs and SVGs |
| `/humanize` (slash-only) | Flags machine-written prose patterns without rewriting anything |
| `/new-diagram` (slash-only) | Starts a TikZ figure from a verified snippet in `templates/tikz-snippets/` |
| `/checkpoint` (slash-only) | Saves a structured state snapshot before you stop |
| `/commit` (slash-only) | Runs the quality gate, then commits, pushes and opens a PR |

### Subagents

`proofreader`, `claim-verifier`, `slide-auditor`, `tikz-reviewer`, `verifier` and `humanize-auditor`. Reviewers only report findings. They never edit your files.

### Rules

Rules in `.qwen/rules/` carry `paths:` globs, so Qwen injects them only when it touches a matching file. That keeps the always-on context small. They cover TikZ collision prevention and measurement, proofreading protocol, quality gates, plan-first workflow, post-flight verification and PDF reading.

### Hooks

| Hook | Event | Effect |
|------|-------|--------|
| `git-guardrails` | `PreToolUse` | Denies `git reset --hard`, `git clean -f`, force pushes and blanket `git add`, and warns on hardcoded machine paths |
| `pre-compact` | `PreCompact` | Saves plan and session state before context compaction |
| `post-compact-restore` | `SessionStart` | Restores that state after a compaction or resume |
| `notify` | `Notification` | Sends a desktop notification when Qwen needs attention |

## How it differs from the Claude Code original

| Claude Code | Qwen Code |
|-------------|-----------|
| `CLAUDE.md` | `QWEN.md` |
| `.claude/` | `.qwen/` |
| `Task` tool with `context: fork` | `agent` tool with a named `subagent_type`, which starts fresh by design |
| Tool names `Read`, `Grep`, `Bash` | `read_file`, `grep_search`, `run_shell_command` |
| `tools: Read, Grep` in agent frontmatter | A YAML list of Qwen tool names |
| `CLAUDE_PROJECT_DIR` | `QWEN_PROJECT_DIR` |
| `Bash\|Write\|Edit\|MultiEdit` hook matcher | `run_shell_command\|write_file\|edit` |

Dropped on purpose are the R, Stata and Quarto skills, the multi-referee peer-review pipeline and the surface-sync scripts. They depend on tooling that is not part of a LaTeX and Beamer workflow.

## Develop

```sh
python3 scripts/validate.py          # checks skills, agents, rules, hooks, links and leftovers
python3 -m unittest discover -s tests # tests the git-guardrails hook
```

`validate.py` runs in CI. It confirms that every skill name matches its directory, every agent lists only real Qwen tools, every hook script in `settings.json` exists and no Claude Code or Quarto leftovers remain.

## Credits and license

[MIT](LICENSE). Based on [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) by Pedro H. C. Sant'Anna. The TikZ rules adapt Scott Cunningham's [MixtapeTools](https://github.com/scunning1975/MixtapeTools), and the checkpoint pattern follows Hugo Sant'Anna's [clo-author](https://github.com/hugosantanna/clo-author). The Chain-of-Verification approach follows [Dhuliawala et al. (2023)](https://arxiv.org/abs/2309.11495).
