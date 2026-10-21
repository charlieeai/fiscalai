---
name: q-report-charts
description: >
  Builds the Q-Report Charts of a public company as a chart-first HTML artifact (Omaha Inversiones
  style): "the print" in tiles, bear/base/bull valuation cards, annual fundamentals, quarterly momentum,
  segments and a sector section, one chart per card (chart → data table → AI Analysis). It is the data
  annex the narrative Q-Report (skill q-report) is written on. Data: Omaha Value platform → FiscalAI →
  filings → web (macro only). Content in English. Use when the user says "Q-Report Charts",
  "/q-report-charts TICKER", "chart-first", "reporte Q chart-first", "anexo de datos del trimestre".
  Approved bases: LEN, CTT, DGE, Auna.
---

# q-report-charts — chart-first data annex

Answers one question: what in this quarter's print matters for the long-term thesis. Not a dump of
the quarter.

## Phase 0 — Questions (reverse prompting), in Spanish
1. Quarter to cover (default the last reported; half-year if the company reports by halves).
2. Sector KPIs and comparable (propose a table: KPI → source; the analyst approves).
3. Valuation: take bear/base/bull from the platform (`valuations`, primary marked, plus any second
   valuation such as a sum of parts). Confirm whether an own model (Excel / art-val) should rule.
4. Files: as in the q-report skill (Google Drive folder → Dropbox → `fiscalai/inputs/` → one PDF).
Then ask whether the analyst wants more questions or the result.

## Phase 1 — Data (hierarchy and hard rules)
1. Omaha Value platform (Lovable connector, `query_database`, project_id
   `1cfc33e1-fa07-40f3-a8ee-609966fcebc5`): `valuations` + `valuation_lines`, `own_thesis`,
   `catalysts`, `risks`, `position_decisions` in force.
2. FiscalAI (`company_financials_standardized`, `company_ratios`, `company_segments_and_kpis` with
   `periodType:"quarterly"`, `company_filings` / `filing_pdf` for releases).
3. Filings / IR. 4. Web only for macro, with source.
Every charted number must be traceable; if not, it is not charted ("not available" in the caption).
FiscalAI gotchas to check every time: EBITDA = EBIT (identical margin), net debt from one segment
only, inflated gross margin, FCF filled with zeros, half-years split into two equal quarters (use
halves), quotes in GBX (pence). A correction is noted in orange on the chart.
House rules: historical net debt as levels and a 3-year average, never a CAGR; cash excludes
restricted cash.

## Phase 2 — Build
Copy an approved base (LEN is the most complete engine) and replace title, body, data and `init()`.
Do not rewrite the `<style>` or the `render*` functions. Structure:
1. Header `<Company> Q-Report Charts — <quarter>` and a line with the date, the price used and a link
   to the narrative Q-Report when it exists.
2. The print: 7–8 tiles + a "read of the quarter" paragraph. Beat/miss only with a cited source
   (FiscalAI has no consensus).
3. Valuation bear/base/bull in cards: per-share value, upside vs the price, ~5 assumptions. The base
   is the platform's primary valuation, with the same numbers; a sum of parts shows its parts, the
   claims, equity and shares.
4. Annual fundamentals (long history), 5. Quarterly momentum (8–11 quarters, lead KPI with YoY),
6. Cash flow / segments, 7. Sector section, 8. Footer `Omaha Inversiones · Source: …`.
10–16 charts. Each card: title → caption → chart → table → `<details class="analysis" open>` with the
summary **"AI Analysis"**. Everything in English, no Spanish left in the analysis.
Format: 1 decimal in % and multiples; margin YoY in bps; one label per point; colours by metric type
(teal revenue, gold EPS, green FCF, blue returns/debt, red multiples/alerts, slate reference).

## Phase 3 — Validation (blocking)
`node audit.js report.html shots/` (Playwright headless) must give: `JS errors: none`,
`undefined/NaN/Infinity in text: 0`, `empty tables: 0` and every chart `OK` (marks == labels,
collisions = 0). Look at 3–4 screenshots of the busiest charts. Check that the price, IVO, deals and
catalysts match the Q-Report and the platform. Nothing is published if it fails.

## Phase 4 — Publish and register
Artifact (same URL on every update). Register in `skill_outputs`: skill_name `reporte_q` (shown as
"Q-Report Charts" in the header), document_name `<TICKER> Q-Report Charts <quarter>`, quarter_tag,
artifact_link, result_text with the read of the quarter. Deliver to the analyst (in Spanish): link,
period covered, number of charts, audit result, data that could not be obtained and questions ordered
from most to least critical.
