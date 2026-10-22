# QWEN.md

**Project:** Academic LaTeX and Beamer workflow (template, not tied to one paper)
**Stack:** XeLaTeX, BibTeX, TikZ. Python scripts for analysis.
**Branch:** main

Replace the bracketed placeholders and the example rows below with your own project details. Keep this file short, because Qwen Code loads it on every request.

---

## Core principles

- **Plan first.** Enter plan mode before any non-trivial task and save the plan to `quality_reports/plans/`.
- **Verify after.** Compile and read the log at the end of every task.
- **One source of truth.** The Beamer `.tex` file is authoritative and every derived artifact comes from it.
- **Quality gate.** Nothing is committed below 80/100 (see `.qwen/rules/quality-gates.md`).
- **Read-only reviewers.** Reviewer agents report findings and never edit files. Only you or the main agent applies fixes.
- **Learn from corrections.** When corrected, save `[LEARN:category] wrong -> right` to `MEMORY.md`.

---

## Folder structure

```
[YOUR-PROJECT]/
├── QWEN.md                      # This file
├── .qwen/                       # Skills, agents, rules, hooks, settings
├── Bibliography_base.bib        # Central bibliography
├── Figures/                     # Figures and extracted TikZ
├── Preambles/header.tex         # Shared LaTeX preamble and palette
├── Slides/                      # Beamer .tex files
├── quality_reports/             # Plans, session logs, review reports
├── explorations/                # Research sandbox
├── templates/                   # Report templates and the TikZ snippet gallery
└── master_supporting_docs/      # Papers and reference material
```

---

## Commands

```bash
# LaTeX, 3 passes with XeLaTeX
cd Slides && TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
BIBINPUTS=..:$BIBINPUTS bibtex file
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
```

The `/compile-latex` skill runs this sequence and reports overfull boxes and undefined citations.

---

## Skills quick reference

| Skill | Use it to |
|-------|-----------|
| `/compile-latex` | Build a deck and check the log |
| `/proofread` | Read-only grammar, typo, overflow and consistency pass |
| `/visual-audit` | Layout audit of a Beamer deck |
| `/validate-bib` | Cross-check citation keys against the `.bib` file |
| `/verify-claims` | Check factual claims against sources in a fresh context |
| `/lit-review` | Search and synthesize literature with verified citations |
| `/humanize` | Flag machine-written prose patterns, read-only |
| `/devils-advocate` | Challenge the ordering and pedagogy of a deck |
| `/respond-to-referees` | Draft a point-by-point response to reviewers |
| `/interview-me` | Turn a fuzzy idea into a structured research spec |
| `/new-diagram` | Start a TikZ figure from a verified snippet |
| `/extract-tikz` | Extract TikZ blocks from a deck into standalone PDFs and SVGs |
| `/checkpoint` | Save a state snapshot before stopping |
| `/commit` | Run the quality gate, commit, push and open a PR |

Agents live in `.qwen/agents/` and are `proofreader`, `claim-verifier`, `slide-auditor`, `tikz-reviewer`, `verifier` and `humanize-auditor`.

---

## Beamer custom environments

| Environment | Effect | Use case |
|-------------|--------|----------|
| `[your-env]` | [Description] | [When to use] |
| `keybox` | Gold background box | Key points (example, delete) |
| `definitionbox[Title]` | Blue-bordered titled box | Formal definitions (example, delete) |

---

## Current project state

| Deck | File | Key content |
|------|------|-------------|
| HelloWorld (sample, delete when ready) | `Slides/HelloWorld.tex` | Minimal deck to verify the setup |
| 1: [Topic] | `Slides/[File].tex` | [Brief description] |

---

## Skill and agent conventions

- Skills are model-invoked by description and can be called directly as `/<skill-name>`.
- Whatever you type after a slash command reaches the skill as `$ARGUMENTS`.
- Path-gated rules in `.qwen/rules/` load only when a matching file is touched, which keeps this file's context cost low.
- Hooks are configured in `.qwen/settings.json`. The `git-guardrails` hook blocks destructive git commands before they run.
