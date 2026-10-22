---
paths:
  - "Slides/**/*.tex"
---

# Quality Review & Scoring Rubric

> Thresholds are advisory. The `/commit` skill checks them and halts on failure until the user fixes the issues or explicitly overrides, and records the override reason in the commit body.

## Thresholds

- **80/100 = Commit.** Good enough to save.
- **90/100 = PR.** Ready to share.
- **95/100 = Excellence.** Aspirational.

## Beamer Slides (.tex)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | XeLaTeX compilation failure | -100 |
| Critical | Equation overflow | -20 |
| Critical | Undefined citation | -15 |
| Critical | Overfull hbox > 10pt | -10 |
| Critical | Typo in equation | -10 |
| Major | Text overflow | -5 |
| Major | TikZ label overlap | -5 |
| Major | Notation inconsistency | -3 |
| Minor | Font size reduction | -1 per frame |
| Minor | Long source lines (>100 chars), except documented math | -1 |

Score starts at 100. Subtract each deduction once per distinct finding. The `verifier` agent supplies the compile-time findings, and `/proofread` and `/visual-audit` supply the rest.

## Enforcement

- **Score < 80.** Halt within `/commit`. List the blocking issues. The user may override with an explicit signal such as "commit anyway" and a reason.
- **Score < 90.** Allow the commit and list recommendations.

## Quality reports

Save reports under `quality_reports/` using `templates/quality-report.md`.
