---
name: q-report
description: >
  Writes the Q-Report of a position: a narrative essay in the analyst's first person (Burry-on-Substack
  style) that answers whether the thesis still holds after the quarter and whether the business's
  fundamental value is above what the market pays. Thesis in the title, company history, analogies,
  cited outside research and only the numbers that prove the argument. ~1,500 words, HTML artifact with
  a "Download PDF" button, registered in the Omaha Value platform as q_report. It is written on top of
  the Q-Report Charts of the same quarter (skill q-report-charts), built first. Use when the user says
  "Q-Report", "/q-report TICKER", "Q-report de X", "narrar el trimestre", "ensayo del trimestre".
  Content in English, conversation in Spanish.
---

# q-report — narrative Q-Report

Answers one question: after this quarter, does the thesis still stand, and is the business worth more
or less than the market perceives? It is an argument, not a summary. The quarter's numbers already live
in the platform (Financials, Valuation, Q-pulse) and in the Q-Report Charts.

## Prerequisite — Q-Report Charts
The Q-Report is written on top of the Q-Report Charts of the same quarter (skill `q-report-charts`:
charts, tables and an AI Analysis per chart). If it does not exist or is out of date, build or update it
first. It is the data context for narrating the Q-Report with the analyst, and the essay links to it at
the end instead of repeating its tables. When the Q-Report changes a fact (a deal that ended, a new
multiple, a new price), update the Charts so both say the same thing.

## Phase 0 — Questions (reverse prompting), in Spanish
1. The central question of the quarter for the thesis (propose one from the Q-pulse and the platform's
   catalysts; the analyst corrects it).
2. The thesis in one line and the analyst's read of the quarter.
3. Length (default 1,500 words) and the sources the analyst wants included (letters, write-ups,
   Substacks, broker or activist reports).
4. How the files arrive. Chat uploads are limited, so ask for one of these, in this order:
   a Google Drive folder per position and quarter (e.g. `Omaha/Q-Reports/CTT/3Q26/`), read with the
   Google Drive connector; a Dropbox folder, read with the Dropbox connector; files committed to the
   `fiscalai` repo under `inputs/<TICKER>/<quarter>/`; or, as a last resort, one merged PDF in the chat.
Then ask whether the analyst wants more questions or the result.

## Phase 1 — Research (each fact with a source)
A. **Omaha Value platform** (Lovable connector, `query_database`, project_id
   `1cfc33e1-fa07-40f3-a8ee-609966fcebc5`): `own_thesis`, primary `valuations` with `valuation_lines`
   (and the second valuation, e.g. a sum of parts), `catalysts` (with `probability`), `risks`,
   `scorecard_ratings`, `position_decisions` in force, and the latest `skill_outputs` (qpulse, reporte_q).
B. **FiscalAI first** for every financial figure: the print, segments/KPIs, guidance, long history
   (past crises visible in the numbers), shares outstanding, price. Call transcript: 4–8 verbatim quotes
   with name and title, copied exactly.
C. **Outside research**, in this order: press (Reuters, Bloomberg, FT, the reference local press),
   papers and regulator reports, Substack and investor letters, market studies. **Avoid X and forums
   with little engagement.** Look for:
   - the company's own past crises and how they ended;
   - an analogue (another company that went through the same) and what its stock did;
   - competitors with their own data, and their latest calls in the markets the business is moving to,
     to tell lost share from a shrinking market;
   - regulation and macro that move the quarter, with their timelines (e.g. bank-sale approvals);
   - consensus, insiders, activists, changes among shareholders;
   - the company's historical multiples (IPO, peak, trough, today) on a comparable basis (IFRS 16,
     employee-benefit liabilities, bank) before comparing prices.
   If a shock hits the whole industry, compare what each competitor does about it and why the
   company's response would work better: what its advantage (moat) is, with evidence.
   Each outside fact: source, date, URL and a short quote. No source → a marked hypothesis, or out.

## Phase 2 — Outline before writing
Title = the essay's thesis (one sentence with an opinion). Short sections whose titles are claims.
Default skeleton (adapt it):
1. Hook: the fact or scene that best sums up the quarter.
2. What happened (3–5 figures, no more) and why; always one line on the core KPI (e.g. volumes) even
   when it is fine, so the reader sees what holds.
3. Has it happened before? Company history or an analogue.
4. What the market believes and what the evidence says.
5. Competition / regulation / management, whichever moves the thesis.
6. Valuation in one paragraph plus the value bridge: the platform's IVO, how it is reached, the gap.
7. Where I could be wrong (the weak part of the thesis, said plainly).
8. What I will watch next quarter: ALL the dashboard catalysts with their probability, plus the
   quarter's variables (dates and thresholds).
9. Conclusion: whether the business's fundamental value is above or below what the market pays, the
   sources of the gap, and what would close it.
Charts: 2–3 at most, only if they prove a point in the text.

## Phase 3 — Writing
- First person of the analyst for the analysis ("I"); "we/our" for Omaha's valuation and IVO.
- **Informational document: no recommendation language** ("buy", "sell", "hold", "I suggest holding",
  "we recommend"). The conclusion states intrinsic value vs market price.
- No author byline. English. ~1,500 words (±10%).
- Short, direct sentences. Call quotes are evidence and get commented, not summarised.
- Every figure carries its source in a numbered note at the end. No ornaments or stock phrases.
- When citing an activist or a holder with board seats, state their interest.
- Acronyms explained the first time (e.g. GMV).

## Phase 4 — Validation (blocking)
- Every figure traceable to FiscalAI, the platform or an outside source with a link.
- Every verbatim quote checked word by word against the transcript or article.
- IVO, price and gap equal to the platform's on the publication date.
- Every analyst premise checked against evidence; when the evidence contradicts it, the text says so
  and the analyst is told.
- Search the text for buy/sell/hold/suggest/recommend before publishing: zero hits as recommendations.
- Word count within range. List of hypotheses marked as such.
- Render check (Playwright): no JS errors, no horizontal overflow at 390px, the PDF downloads.
Nothing is published if something fails.

## Phase 5 — Publish and register
HTML artifact (same URL on every update), with a "Download PDF" button (capability `downloads`; the
PDF is generated in the page with jsPDF). File name `<TICKER>-Q-Report-<quarter>.pdf`.
Register in `skill_outputs`: skill_name `q_report`, document_name `<TICKER> Q-Report <quarter>`,
quarter_tag (e.g. 2026Q2), artifact_link, result_text = a neutral 3-line summary. It shows on the
"Q-Report" button of the position header; the Charts show on "Q-Report Charts".
Back up the HTML and its build script to `fiscalai/reportes-q/`.
Deliver to the analyst (in Spanish): link, word count, sources used, hypotheses and open questions, and
a reminder that a private artifact must be shared before the PM can open it.
