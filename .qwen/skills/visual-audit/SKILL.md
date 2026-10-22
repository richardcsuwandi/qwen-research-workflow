---
name: visual-audit
description: Adversarial visual-layout audit of a Beamer `.tex` deck. Flags overflow, font inconsistency, box fatigue, spacing, and alignment issues. Use when user says "visual audit", "check the layout", "does this overflow?", "look for visual issues", "audit the slides", or after reworking a deck's appearance. Does NOT check writing, pair with `/proofread` for that.
argument-hint: "[TEX filename]"
---

> Arguments. Whatever the user typed after the slash command is `$ARGUMENTS` below.

# Visual Audit of a Beamer Deck

Perform a thorough visual layout audit of a Beamer slide deck.

## Steps

1. **Read the slide file** at `Slides/$ARGUMENTS` (add `.tex` if missing).

2. **Compile** with `/compile-latex` and collect `Overfull \hbox` and `Overfull \vbox` warnings with their line numbers.

3. **Audit every frame for:**

   **OVERFLOW:** Content exceeding frame boundaries
   **FONT CONSISTENCY:** `\tiny` or `\footnotesize` overrides, inconsistent sizes
   **BOX FATIGUE:** 2+ colored boxes on one frame, wrong box types
   **SPACING:** `\vspace{-Xem}` hacks, blank lines in itemize, unaligned figures
   **LAYOUT:** Missing transition frames, missing framing sentences before definitions, semantic colors on binary contrasts

4. **Delegate** the detailed pass to the `slide-auditor` agent and merge its report with the compiler warnings.

5. **Produce a report** organized by frame with severity and recommendations.

6. **Follow the spacing-first principle:**
   1. Reduce vertical spacing structurally (split the frame instead of stacking `\vspace{-Xem}`)
   2. Consolidate lists
   3. Move displayed equations inline
   4. Reduce figure width (100% to 80% or 70%)
   5. Last resort: font size reduction (never below `\footnotesize`)

Save the report to `quality_reports/[FILENAME]_visual_audit.md`. Do not edit the deck.
