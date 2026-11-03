---
name: q-report
description: >
  The full quarterly report flow for a position in two deliverables. First the Q-Report Charts: a
  chart-first HTML annex (print tiles, bear/base/bull, fundamentals, segments, sector) with an AI
  Analysis per chart. Then the Q-Report: a ~1,500-word narrative essay in the analyst's first person
  that says whether the thesis holds and whether the business's fundamental value is above what the
  market pays, with a "Download PDF" button. Data from the Omaha Value platform (Lovable connector),
  then FiscalAI, then filings and cited press. Both are published as artifacts and registered in the
  platform (reporte_q and q_report). Use when the user says "Q-Report", "/q-report TICKER",
  "reporte Q", "reporte-q", "Q-Report Charts", "chart-first", "reporte trimestral", "narrar el
  trimestre", or asks for the quarter's report of a position. Report content in English;
  conversation with the analyst in Spanish.
---

# q-report — quarterly report flow

Two deliverables, in this order. Each can be run alone if the user asks only for one.

| Step | Deliverable | Detail | Registered as |
|---|---|---|---|
| 1 | Q-Report Charts (data annex) | `references/charts.md` | `reporte_q` |
| 2 | Q-Report (narrative) | `references/narrative.md` | `q_report` |

Platform queries and registration SQL: `references/platform.md`.

## Requirements in the session
- Connectors: **FiscalAI** (all financial figures first), **Lovable** (`query_database` on the Omaha
  Value project), web search. Optional: Google Drive or Dropbox for the analyst's files.
- Artifact publishing (the Artifact tool or the claude-artifacts connector).
- To run the validation scripts: Node + Playwright (present in Claude Code cloud sessions). Where
  they cannot run (e.g. a claude.ai chat), say so and do the checks by reading the page and data.
If a connector is missing, say which one and stop before writing numbers you cannot source.

## Step 0 — Questions (reverse prompting, in Spanish)
1. Ticker and quarter (default: last reported; halves if the company reports by halves).
2. Which deliverable: both (default), only Charts, or only the Q-Report on an existing Charts.
3. The central question of the quarter and the analyst's read (propose one from the latest Q-pulse
   and the platform's catalysts).
4. Sources the analyst wants included, and how the files arrive, in this order of preference:
   a Google Drive folder per position and quarter (e.g. `Omaha/Q-Reports/CTT/3Q26/`); a Dropbox
   folder; files committed to a repo under `inputs/<TICKER>/<quarter>/`; one merged PDF in the chat.
5. Length of the Q-Report (default 1,500 words).
Then ask whether they want more questions or the result.

## Step 1 — Q-Report Charts
Follow `references/charts.md`. Start from `assets/charts-base-ctt.html` (CTT 2Q26, the approved
engine: styles and `render*` functions stay as they are; replace header, tiles, data arrays, card
text and `init()`). Validate with `scripts/audit-charts.cjs`. Publish, register as `reporte_q`.

## Step 2 — Q-Report
Follow `references/narrative.md`. Start from `assets/q-report-base-ctt.html` (page shell, styles,
value-bridge figure and the in-page jsPDF "Download PDF"; publish it with the `downloads`
capability). `assets/q-report-build-ctt.py` shows how the CTT essay was assembled: sources keyed by
id, `[[key]]` cite markers numbered by first appearance, word count printed. Validate with
`scripts/check-q-report.mjs`. Publish, register as `q_report`, link it from the Charts footer and
link the Charts from its end.

## Rules that apply to both
- Every number traceable to the platform, FiscalAI or a cited source; otherwise it is out, or it is
  a hypothesis marked as one. "I don't know" is a valid answer.
- Check each premise of the analyst against evidence; when it does not hold, the text says so and
  the analyst is told.
- No recommendation language (buy / sell / hold / "I suggest" / "we recommend"). The documents are
  informational: they conclude whether fundamental value is above or below the market price.
- When citing an activist or a holder with board seats, state their interest.
- Both documents must say the same thing: price, IVO, deals, catalysts. If step 2 changes a fact,
  update the Charts.
- Same artifact URL on every update. Back up the final HTML and any build script where the user keeps
  them (by default `reportes-q/` in the working repo) and commit them.
- No model identifiers in reports, the database or commits.
- Deliver in Spanish: links, word count, sources, hypotheses, data not obtained, open questions, and a
  reminder that a private artifact must be shared before the PM can open it.
