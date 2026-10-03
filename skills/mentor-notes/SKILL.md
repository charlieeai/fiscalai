---
name: mentor-notes
description: >
  Writes 1–3 one-line "mentor" reminders for a portfolio company in the Omaha Value platform:
  short critiques in the voice of Buffett, Munger, Graham, Pabrai, Marks, Fisher (and other
  mentors in the principles library), each tied to an approved principle and to a concrete
  number from the company's own data. Advisory only, never an input to scores or valuations.
  Trigger on "/mentor-notes TICKER", "mentor notes de X", "qué diría Buffett de X",
  "recordatorios de principios para X", "aplica los principios a X", or at the end of an
  analysis skill run (qpulse, reporte-q, buffett-brief, idea-screener, one-pager) when the user
  wants the mentors' read. Batch: "/mentor-notes all" runs every position and basket member.
---

# mentor-notes — principles applied, one line each

The platform keeps a library of investing principles (`principles`, status `approved`): each is
a one-line reflection with its source. This skill reads a company's data, picks the
principles the data actually speaks to, and writes at most three one-line reminders to
`mentor_notes`. They show up in a collapsed "Mentors" section of the position page. They are
reminders to keep in mind, not verdicts: nothing reads them, and they never change a score.

Output language: English (the platform's language). Conversation with the user follows the
user's language.

## Hard rules

1. **Only approved principles.** Every note points to one `principles.id` with
   `status = 'approved'`. If no approved principle fits, write no note. Never use a principle
   that is `proposed` or `archived`.
2. **Never put words in a mentor's mouth.** A note is Omaha's application of the principle,
   written in the mentor's spirit. Do not write it as a quotation, do not add quotation marks,
   and do not claim the mentor said or thinks anything about this company. The principle and
   its source show on hover.
3. **One concrete fact per note**, taken from the platform (scorecard reasons, valuation
   lines, thesis, latest Q-pulse, financial fields) or FiscalAI. If you cannot point to the
   number, do not write the note.
4. **Short.** One line, ideally under 140 characters, hard limit 220 (the column rejects more).
   No preamble, no hedging, no "it is worth noting".
5. **Few.** 1–3 notes per company per run, the ones that matter most for this company now.
   Silence is a valid output: a company with nothing that a principle flags gets no note.
6. **Advice, not alarm.** Name the issue and the number; do not tell the user to buy or sell.

## Style

The `mentor` column carries the name; the note is the critique. Examples of the register
(numbers are illustrative):

- Buffett — "Net debt is 8.9x EBITDA. Leverage turns a bad year into a permanent loss."
- Munger — "Invert it: the bear case is a price war in payments, 62% of recurring gross profit."
- Graham — "Price is 62% of the base value: the margin of safety is there, but the bear case sits 12% below."
- Pabrai — "Heads we win, tails we lose little? Bear case −54% vs base +77%: the bet is not asymmetric."
- Marks — "Consensus already expects the recovery; what do we see that the price does not?"
- Fisher — "Organic growth slowed to 1% for two quarters. What does management do for the next leg?"

## Data (Lovable connector, project `1cfc33e1-fa07-40f3-a8ee-609966fcebc5`)

Read (one query per company is enough; resolve basket members by `member_ticker`, the basket
row has it null):

- `principles` where `status='approved'`: id, mentor, principle, topics.
- `scorecard_ratings` (12 criteria: rating 0–4 and reason; read `dante` and `christian`).
- Primary valuation (`valuations.is_primary`) and its `valuation_lines` (target price, net
  income, P/E, net debt, market cap) plus Bear/Bull target prices.
- `positions` / `basket_members`: price, net_debt_ebitda, margins, last_q_reported.
- `own_thesis` claims and breaks; latest `skill_outputs` row with `skill_name='qpulse'`.
- Existing active `mentor_notes` for the company (`dismissed_at is null`).

Match principle topics to what the data shows, for example: leverage ↔ net debt/EBITDA,
covenants, refinancing; moat ↔ moat_strength/durability reasons; valuation and
margin_of_safety ↔ price vs IVO and Bear case; management and capital_allocation ↔
leadership/culture reasons, buybacks, M&A; growth ↔ organic growth; behavior ↔ crowded
narratives, recent drawdowns; cyclicality ↔ commodity or housing exposure; accounting ↔
adjusted vs GAAP gaps.

## Write-back

Replace, do not stack. In one approved query per company:

```sql
update mentor_notes set dismissed_at = now()
 where position_id = 'POSITION_ID' and member_ticker is not distinct from MEMBER_OR_NULL
   and dismissed_at is null;
insert into mentor_notes (position_id, member_ticker, principle_id, mentor, note, topic, quarter_tag)
values ('POSITION_ID', MEMBER_OR_NULL, 'PRINCIPLE_ID', 'Buffett', $$NOTE$$, 'leverage', 'YYYYQn');
```

`quarter_tag` is the latest reported quarter in `YYYYQn` form. Confirm the rows landed. Never
write to any other table.

## Reply to the user

Per company: the notes written (mentor — note), or "no notes" with the reason in one line.
Then, separately, any principle you wanted to use but could not because it is not approved yet.
