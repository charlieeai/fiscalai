---
name: qpulse
description: >
  Fast post-earnings pulse check. Produces a one-screen, numbers-first read (~200 words per
  company) scoring a quarterly print against a pre-registered thesis — not a valuation, not
  transcript analysis. Trigger on "/qpulse TICKER", "q-pulse de X", "reportó X — dame el
  pulso", "qué reportó X", "quick read on X's print", "resumen post-earnings de X", "X just
  reported, anything change?", "did the quarter break the thesis", or any request for a
  compressed post-print summary. Also on batch requests in reporting season: "/qpulse ONON
  NKE LULU". Use it even when the user pastes an earnings summary, press release, or headline
  numbers without naming the skill — if a company just reported and the user wants to know
  what changed for their position, this is the skill. Thesis, scorecard, and VIO come from
  the Omaha Value platform via the Lovable connector; each run is logged back. Does not
  replace earnings-call-analyst or one-pager; it precedes the decision to run either.
---

# Q-pulse — Post-Print Pulse Check

## Overview

Q-pulse is the T+0 read. It answers one question — *did anything in my thesis change* — in
the time it takes to read one screen. It is deliberately disposable: no archival PDF, no
valuation view, no narrative. The output is a scoreboard, not an essay.

It sits below `earnings-call-analyst` in the stack. That skill reads transcripts for
narrative drift and produces a PDF. Q-pulse reads numbers and produces a screen. Q-pulse
runs on every print in the portfolio and watchlist; `earnings-call-analyst` runs on the
few prints where the numbers raised a question worth chasing.

The design principle throughout: **the print is scored against what was pre-registered,
never against a narrative constructed after the fact.** Every rule below exists to
enforce that.

---

## HARD CONSTRAINTS

**~200 words per company. One screen. No exceptions.**

If a print seems to require more, that is the signal to escalate to
`earnings-call-analyst` — not to write a longer Q-pulse. State the escalation in chat and
keep the Q-pulse at length.

**Six lines, always in order, never renamed, never merged.** A line with no data prints
its label followed by "n/a" — it does not disappear. A missing line is itself information:
it tells the user the field could not be sourced, which is different from the field not
mattering.

**No valuation opinion.** Line 5 reports the multiple reset as an arithmetic fact
(multiple going in → multiple on revised numbers). It does not say whether the stock is
cheap. That judgment belongs to `one-pager` or `ai-writeup`.

---

## OUTPUT FORMAT

| Companies in the request | Format |
|---|---|
| 1–2 | Inline in chat. Plain markdown, no artifact. |
| 3+ | Single HTML artifact: read-through block on top, then one compact card per company. |

Never a PDF. The build cycle defeats the purpose of the skill.

For the HTML artifact, follow the `one-pager` visual conventions: standalone HTML, CSS
variables, teal accent palette, no external libraries, no CDN dependencies. Cards stack
vertically; each card carries the six lines with the verdict tag as a colored chip in the
card header. Keep it readable at phone width — this gets read during a reporting week, on
a phone, between prints.

---

## LANGUAGE

**Mirror the language of the request.** Spanish prompt → Spanish output. English prompt →
English output. Do not flag or comment on the switch.

This departs from the PDF skills (`ai-writeup`, `initial-take`, `company-compare`), which
are English-only because they are archival deliverables. Q-pulse is read once and
discarded, so it follows the reader rather than the archive.

Metric names stay in standard English form regardless of output language: EPS, FCF, SSS,
ROIC, SBC, capex, y/y, q/q, guidance. Do not translate these.

---

## THE SIX-LINE SKELETON

### Line 1 — Verdict

One tag from a closed set, then one clause of characterization. No hedging, no "on
balance," no "mixed but."

| Tag | Assign when |
|---|---|
| **Beat & raise** | Beat on the quarter AND forward guidance raised above prior consensus |
| **Beat & hold** | Beat on the quarter, guidance reiterated or unchanged |
| **In line** | Within noise on both lines, no guidance change |
| **Miss** | Below consensus on EPS or revenue, or guidance cut — but operating drivers intact |
| **Deterioration** | The underlying economics changed, not just the quarter |

The **Miss / Deterioration** distinction carries the whole skill. A miss is a bad quarter.
Deterioration is a different business: margin compression that is not cyclical, a KPI
inflection, FCF breaking from earnings, a leverage step-up, an off-balance-sheet
commitment growing faster than the balance sheet. A company can beat consensus and still
be tagged Deterioration — META in the sample beat on nothing that mattered while R&D went
from $13B to $22B and FCF collapsed to $784M. Reserve the tag for structural change and it
stays meaningful.

**Assign the verdict before writing anything else, and never revise it to match the stock
reaction.** Line 5 reports what the market did; line 1 reports what the company did. When
they disagree, that disagreement is the most useful output of the run — do not resolve it
by moving line 1.

### Line 2 — The print

EPS and revenue, each with three values: absolute, y/y %, vs. consensus. Then the single
KPI that governs this business.

Consensus is a required field, not an optional one. A +30% EPS print reads as good news
until you learn it was the bar. If consensus cannot be sourced, print "vs. cons: n/a" —
never infer it from the price reaction.

**KPI selection is pre-registered, not chosen after the fact.** The Omaha platform does not
register a per-ticker governing KPI, so select it by business type from the table below and
use that same line every quarter for a given name, even when it is the quarter's worst
number. Metric-shopping — quietly switching to whichever line looked best this quarter — is
the exact failure this skill exists to prevent. Keep the mapping stable across runs:

| Business type | Governing KPI |
|---|---|
| Cloud / infrastructure | Segment revenue growth, and whether it accelerated or decelerated vs. prior quarter |
| Consumer / retail / restaurants | Same-store sales or comparable growth; DTC mix if the thesis turns on channel |
| Soft goods / footwear / apparel | Constant-currency revenue growth by region, plus inventory (see line 3) |
| Homebuilders | Orders and backlog, not revenue — revenue is a lagging print |
| Vertical software / serial acquirers | Organic growth ex-acquisition; capital deployed on acquisitions |
| Airports / concessions | Passenger traffic and revenue per passenger |
| Financial platforms | Revenue by activity line, so a single line's collapse is visible |
| Pharma / animal health | Volume vs. price decomposition on the core franchise |

State the KPI with its prior-period comparison, not standalone. "Azure +43%" is a number.
"Azure +43%, accelerating from +40%" is a read.

### Line 3 — Quality check

The cash-and-accrual audit. Include only the fields that apply; print the ones that apply
even when they are clean, because a clean line is a finding.

- **FCF vs. EPS** — always. The divergence is the highest-value line in the whole format.
  EPS +30% against FCF −23% is the entire MSFT story.
- **GAAP bridge** — when the reported number contains marks, one-offs, or an accounting
  change. State what is in the number that shouldn't be, with the amount. Revaluation gains
  on private holdings, useful-life reclassifications, IRGA liability marks, acquisition
  amortization, FX/IFRS translation noise. If reported and adjusted diverge materially, use
  adjusted in line 2 and say so here.
- **Diluted share count y/y, and SBC as % of revenue** — always. This is where EPS growth
  quietly comes from.
- **Constant-currency vs. reported growth** — whenever the reporting currency is not USD,
  or a majority of revenue is earned outside the reporting currency. For CHF, EUR, GBP, and
  TRY reporters this is mandatory: reported growth alone is not a signal.
- **Inventory growth vs. revenue growth** — for any consumer or soft-goods name. Inventory
  outgrowing revenue is the earliest available warning, well ahead of gross margin.
- **Off-balance-sheet commitments** — when disclosed: future lease obligations, SPV
  structures, purchase commitments, supplier financing. Report the level and the rate of
  change. META's $279B of future leases growing 53% in three months is a leverage event
  that never touches the debt line.

### Line 4 — Guidance & capital

Next quarter vs. consensus. Full-year revision direction. Capex guidance and how it moved.
Buyback as % of shares outstanding, in the quarter and year-to-date.

**Flag whether a raise flows the beat through or absorbs it.** A company that beats by
$0.10 and raises the full year by $0.10 has changed nothing about the back half. One that
beats by $0.10 and raises by $0.25 has. One that beats by $0.10 and leaves the year
unchanged has just told you the back half is worse than it was.

Read capex range mechanics rather than midpoints: narrowing $125–145B to $130–145B is a
raise of the floor, which is a firmer commitment than a raise of the midpoint.

### Line 5 — Setup & reaction

Reaction is uninterpretable without the setup. Report, in order: YTD performance and
distance from the all-time high going into the print; forward multiple going in → forward
multiple on revised numbers; after-hours move; T+1 close.

**T+1 close is the real number.** After-hours is a thin-book first draft and reverses often
enough to be noise — HOOD in the sample fell after hours and had reversed by the next
morning. Report both, and when the run happens before the T+1 close, print "T+1: pending"
rather than treating the after-hours move as final.

The multiple reset is arithmetic, not opinion: recompute the forward multiple on the
revised forward estimate and report both numbers. A stock that fell 9% while forward
estimates fell 15% got more expensive. That is the kind of thing this line exists to catch.

### Line 6 — Thesis

Open with the position tag from `positions.bucket` (e.g. `Core`, `Starter`, `Watchlist`),
then the VIO from the resolved Omaha valuation: `Core · VIO $[Y] ([target_year])`. For a
basket member this is that member's own VIO (AMR ≠ HCC ≠ CNR), not the basket's headline —
name the member so it's unambiguous. Sizing and distance-to-VIO change what a number means —
a 9% order decline in a starter is information; in a core position trading near VIO it is a
decision. If no position row exists, print `No position`.

Then, in order:

1. **Score**: *confirms · neutral · challenges*, against the three `own_thesis` bullets (the
   registered pillars). Nothing else.
2. **Trigger fired**: yes/no, and which one. The triggers are the three registered breaks
   (`own_thesis.breaks_1..3`, k1–k3); a break fires only on the condition as written.
3. **Next dated trigger**: `positions.next_earnings_date`, or a more specific pre-committed
   date if one is known.
4. **Scorecard read**: name any of the 12 criteria of the quality scorecard
   (`scorecard_ratings`) whose rating or reason this print calls into question, with the
   current rating (0–4) and the direction of the suggested change — or `sin cambios`. The
   criteria, by pillar (weight): Strength 15 (financial_resilience, gross_margin,
   returns_on_capital, free_cash_flow, capital_allocation) · Moat 25 (moat_strength,
   moat_durability) · Potential 15 (optionality, organic_growth) · Culture 25 (leadership,
   culture) · Margin of safety 20 (margin_of_safety). Each is rated 0–4 by two reviewers,
   `christian` and `dante`; name the rating you are reading. This is an opinion for the
   analyst to action in the app; Q-pulse does not write to `scorecard_ratings`. The old
   six-pillar traffic-light scorecard (circulo / moat / management / cashflow / debt / mos
   colors) no longer exists; never read or cite it.

Score only against the pillars registered before the print. If a print is bad in a way none
of the three bullets anticipated, the correct output is "challenges — via an unregistered
channel," followed by a one-line note that the thesis bullet or scorecard criterion should be
updated in the Omaha platform. Do not retrofit the surprise into an existing bullet; that
converts a forecasting miss into an apparent hit and destroys the record.

---

## READ-THROUGH BLOCK

Required whenever 2+ companies are in the run. One short paragraph at the top, before the
individual cards.

This is where the aggregate value sits and it is the part most post-earnings summaries
skip. What do the prints say collectively that no single print says alone? The sample does
this three times: MSFT vs. META on who owns the cloud business funding the AI spend; AMZN's
AWS acceleration read back against Azure; Quanta framed as the electricity derivative of
everyone else's capex.

Look for: the same cost line moving in the same direction across names; one company's capex
appearing as another's revenue; a shared input or customer; divergence between companies
the market treats as a single trade. When the prints genuinely say nothing collectively,
write one sentence saying so — do not manufacture a theme.

---

## DATA DISCIPLINE

**A ticker is a sufficient input.** Q-pulse does not wait for the user to paste a press
release or transcript. Identify the company from the ticker and go get the primary
document yourself — that is the normal path, not a fallback for when the user forgot to
attach something.

**Source hierarchy:**

1. **The primary filing — fetched directly, first.** For US filers, go to SEC EDGAR and
   pull the 8-K (Exhibit 99.1 carries the press release) for the headline print and
   guidance language, and the 10-Q/10-K for the detail the release compresses away: GAAP
   bridge, diluted share count, SBC, off-balance-sheet commitments, segment breakout. This
   is the source, not a news article about the source — go to `sec.gov/cgi-bin/browse-edgar`
   or the company's EDGAR filing index directly rather than routing through a search engine
   when a direct fetch will do. Non-US filers: use the home-market equivalent (RNS for UK
   listings, ad hoc disclosures / Bundesanzeiger for German issuers, SEDAR+ for Canadian).
   Also check the company's investor-relations site for the same press release when EDGAR
   is slow to index same-day filings.
2. **Documents in the request** — if the user pastes a press release, transcript, or
   summary anyway, use it. Reconcile against the fetched filing where both exist, and flag
   any conflict rather than silently picking one.
3. **Web fetch / web search — for what the filing doesn't carry.** Consensus EPS and
   revenue, guidance vs. consensus, same-day and T+1 price action, and the forward
   estimates behind the multiple reset all live outside the filing by definition — go get
   them.

**Search and fetch authorization.** Within a Q-pulse run, going out to the web — to fetch
the primary filing and to fill any of the six lines from it or from consensus/price
sources — is pre-approved. The test is narrow but not itemized: *does this fill a line in
the skeleton from the company's own numbers or the market's read of them?* If yes, go get
it without asking.

**Anything that isn't the company's own numbers or the market's pricing of them still
requires explicit permission** — competitor data, analyst commentary and price targets,
sector context, short interest, or any other color that goes beyond the six lines. Ask
before searching for those, per standing workflow preference.

**Never estimate a field.** Any value that cannot be sourced prints as "n/a". An estimated
consensus number is worse than no consensus number, because it produces a beat-or-miss
verdict on invented data. If EDGAR, the IR site, and a bounded web search all come up empty
on a field, "n/a" is still the answer — fetching more aggressively is not license to fill
the gap with a guess.

---

## THESIS SOURCE — OMAHA VALUE PLATFORM

Q-pulse reads the pre-registered thesis, scorecard, and VIO **live from the Omaha Value
platform** (the `omahavalue` app, Supabase-backed) through the **Lovable connector**, using
`query_database` against project id `1cfc33e1-fa07-40f3-a8ee-609966fcebc5`. There is no local
thesis file. The published site (omahavalue.lovable.app) sits behind a login, so a web fetch
will not return this data — the connector is the only path.

**Baskets are the reason the read is not a simple ticker match.** Some positions are baskets
(`positions.is_basket = true`, e.g. `COAL`) that hold several member tickers (AMR, HCC, CNR).
The reported name the user hands you is usually the **member** (AMR), not the basket label
(COAL). Member tickers live in `basket_members`, and each member has its **own VIO**
(`valuations.member_ticker`) and its **own debt/MoS** (`scorecard_members.member_ticker`) and
its **own** `next_earnings_date`. `is_primary` marks the basket's headline member, **not** the
one you were asked about — filtering on it would return AMR's VIO even when the user asked
about HCC. Resolve the member explicitly.

Everything is **per member** in a basket: the thesis (`own_thesis`: bullets, claims and
breaks), the quality scorecard (`scorecard_ratings`), the VIO (`valuations`, with
`is_primary` marking each member's Base scenario) and the numeric debt & MoS. Each table
carries `member_ticker`; the basket-level row has it null. Always match on
`member_ticker is not distinct from` the resolved member, or the join returns one row per
member.

**One read query per run.** It needs the user's approval when it runs; say so and proceed.
This form resolves the reported ticker as either a standalone position or a basket member and
pulls everything in one shot:

```sql
with tgt as (
  select p.id as position_id, p.ticker as position_ticker, p.is_basket, null::text as member_ticker
  from positions p where upper(p.ticker) = upper('TICKER')
  union all
  select p.id, p.ticker, p.is_basket, bm.ticker
  from basket_members bm join positions p on p.id = bm.position_id
  where upper(bm.ticker) = upper('TICKER')
)
select tgt.position_id, tgt.position_ticker, tgt.is_basket, tgt.member_ticker,
       p.bucket, p.last_q_reported,
       coalesce(bm.next_earnings_date, p.next_earnings_date) as next_earnings_date,
       t.bullet_1, t.bullet_2, t.bullet_3,
       t.claim_1, t.claim_2, t.claim_3, t.breaks_1, t.breaks_2, t.breaks_3,
       (select json_agg(json_build_object('criterion', r.criterion, 'christian', r.christian,
                                          'dante', r.dante, 'reason', r.reason)
                        order by r.criterion)
          from scorecard_ratings r
         where r.position_id = tgt.position_id
           and r.member_ticker is not distinct from tgt.member_ticker) as scorecard,
       coalesce(sm.net_debt_ebitda, s.net_debt_ebitda) as net_debt_ebitda,
       coalesce(sm.has_convertible, s.has_convertible) as has_convertible,
       coalesce(sm.mos_52w_low, s.mos_52w_low)         as mos_52w_low,
       v.target_price as vio, v.target_year, v.label as valuation_label
from tgt
join positions p on p.id = tgt.position_id
left join basket_members  bm on bm.position_id = tgt.position_id and bm.ticker = tgt.member_ticker
left join own_thesis      t  on t.position_id  = tgt.position_id
                            and t.member_ticker is not distinct from tgt.member_ticker
left join scorecard       s  on s.position_id  = tgt.position_id
                            and s.member_ticker is not distinct from tgt.member_ticker
left join scorecard_members sm on sm.position_id = tgt.position_id and sm.member_ticker = tgt.member_ticker
left join valuations v on v.position_id = tgt.position_id
     and v.member_ticker is not distinct from tgt.member_ticker
     and coalesce(v.is_primary, false) = true;
```

`scorecard` here only supplies the numeric reference figures (net debt/EBITDA, convertible
flag, 52-week low); the quality judgement comes from `scorecard_ratings` alone. Score =
sum of (criterion weight × rating / 4), out of 100; the criterion weight is the pillar
weight split evenly across its criteria (Strength 3 each, Moat 12.5, Potential 7.5,
Culture 12.5, Margin of safety 20).

If the Lovable connector is not available in the session, treat it as "not found" and drop to
the fallback below.

**Detect the quarter before anything else.** The moment you know which print you're scoring,
fix its fiscal quarter as `quarter_tag` in `YYYYQn` form (e.g. `2026Q2`). Derive it from the
print itself, cross-checked against `last_q_reported` — note that `last_q_reported` displays
as `"Q2 FY2026"` but `skill_outputs.quarter_tag` is stored as `2026Q2`, so normalize. This
tag is decided up front because it governs both the score and the write-back (add vs. replace,
below).

**The three `own_thesis` bullets are the registered pillars Line 6 scores against**, with
the claims (`claim_1..3`) as their testable form and the breaks (`breaks_1..3`) as the
triggers. The scorecard (`scorecard_ratings`) is read so Line 6 can flag criteria whose
rating or reason may need to change (it never edits them). The VIO is the resolved
valuation's `target_price` — the `is_primary` (Base) scenario of the member, or of the
standalone name — with `target_year` as its horizon.

**Fallback order:**

1. `own_thesis` bullets exist for the ticker → use them as the three registered pillars, and
   read the scorecard and VIO alongside.
2. No row in the platform, but the user states a thesis in the prompt → use that for Line 6,
   and note the position isn't in the Omaha platform yet.
3. Neither → Line 6 prints `Thesis: no hay tesis por contrastar` and stops there. Lines 1–5
   still run normally.

**Q-pulse never improvises a thesis.** The failure mode is specific and seductive: reason
backward from the print to a thesis the print happens to support, then score the print as
confirming it. That produces a run of apparent confirmations and no information. If nothing
was registered before the print, there is nothing to score, and saying so is the correct
output.

---

## WRITE-BACK TO THE OMAHA PLATFORM

After the read is produced, log the run to the platform so it no longer has to be copied in
by hand — but **the write is keyed on the quarter, so it replaces the existing Q-pulse row for
that quarter instead of stacking a new one.** There is one Q-pulse row per
`(position, quarter, member)`: rerunning AUNA for `2026Q2` overwrites AUNA's `2026Q2` row;
running it for a new quarter adds a row. This is why the quarter is detected up front. For a
basket member, set `member_ticker` so each member keeps its own row (AMR, HCC and CNR are
three separate rows under the same basket, exactly as the other skills store them); for a
standalone name, leave `member_ticker` null.

Use this upsert-by-emulation (one approved query): the `UPDATE` replaces the row if it exists,
and the `INSERT` runs only when it didn't. `is not distinct from` makes the null-member case
match correctly.

```sql
with upd as (
  update skill_outputs
     set result_text = $$RESULT_TEXT$$, artifact_link = ARTIFACT_LINK_OR_NULL, created_at = now()
   where position_id = 'POSITION_ID' and skill_name = 'qpulse'
     and quarter_tag = 'YYYYQn' and member_ticker is not distinct from MEMBER_OR_NULL
  returning id
)
insert into skill_outputs (position_id, skill_name, quarter_tag, member_ticker, result_text, artifact_link)
select 'POSITION_ID', 'qpulse', 'YYYYQn', MEMBER_OR_NULL, $$RESULT_TEXT$$, ARTIFACT_LINK_OR_NULL
where not exists (select 1 from upd);
```

- `POSITION_ID` — the id resolved in the read query (the basket parent's id for a member). If
  there is no position row (fallback tier 2/3), skip the write and say so; never create a
  position.
- `quarter_tag` (`YYYYQn`) — the quarter detected up front, e.g. `2026Q2`. Must match the
  stored convention, not the `"Q2 FY2026"` display form.
- `member_ticker` — the reported member for a basket (`'AMR'`), or `null` for a standalone name.
- `result_text` — the full six-line read for this company (the card, in a batch). Dollar-quoted
  (`$$…$$`) so quotes and line breaks pass through.
- `artifact_link` — set it when 3+ companies were rendered as an HTML artifact and a link
  exists; otherwise null.
- Confirm the write landed; if the connector or approval is unavailable, keep the on-screen
  output and tell the user the run wasn't logged.

This replaces the old manual copy-paste into the position's Q-pulse block.

---

## ANTI-PATTERNS

Things Q-pulse does not do, in order of how tempting they are:

- **Explain the price move with a narrative.** Line 5 reports the move. If the move
  disagrees with line 1, leave the disagreement standing.
- **Retrofit an unregistered surprise into a registered pillar.** Say it came through an
  unregistered channel and note that the thesis bullet or scorecard criterion should be updated
  in the Omaha platform.
- **Swap the governing KPI** to whichever metric looked good this quarter.
- **Extend past one screen** because the print was interesting. Escalate instead.
- **Add a valuation view.** The multiple reset is arithmetic; the judgment is another skill.
- **Soften the verdict tag.** The closed set has five options and none of them is "mixed."
- **Fill a field with an estimate** rather than "n/a".

---

## ESCALATION

End in chat — never in the output itself — with one sentence naming the follow-on skill the
print warrants:

| Condition | Escalate to |
|---|---|
| Numbers raise a question about what management is saying, or a topic disappeared | `earnings-call-analyst` |
| Multiple reset materially, or the operating picture changed enough to revisit the numbers | `one-pager` |
| A registered signal was contradicted and the position needs resizing | `ai-writeup` |
| Nothing material changed | Nothing |

**Most prints should escalate to nothing.** A skill that escalates every quarter is not
filtering, and the filtering is the value. If several consecutive runs all escalate, the
registered signals are too loose — say so.

---

## WHEN TO USE THIS SKILL VS. OTHERS

| Situation | Use |
|---|---|
| A company just reported and the question is "did anything change" | **q-pulse** |
| Reading a transcript for narrative drift, evasive language, vanishing topics | `earnings-call-analyst` |
| The multiple reset and the numbers need a full financial history | `one-pager` |
| Sizing or resizing a position | `ai-writeup` |
| Deciding whether an unfamiliar name deserves research time | `initial-take` |
| Several companies in the same sector reported and the question is sector-level | `market-summary` |

Batch runs are normal during reporting season. `/qpulse ONON NKE LULU` produces one
artifact with a read-through block and three cards, and each card independently decides its
own escalation.
