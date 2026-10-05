# Text trim job (2026-10-05)

Goal: shorten long analyst texts in the Omaha Value app (Lovable project
1cfc33e1-fa07-40f3-a8ee-609966fcebc5, Postgres via the Lovable `query_database`
tool) without losing substance. Only texts over their limit are touched.

| table.column | limit (words) |
|---|---|
| scorecard_ratings.reason | 25 |
| risks.description | 35 |
| catalysts.detail | 35 |
| own_thesis.bullet_1/2/3 (thesis pillars) | 45 |
| own_thesis.breaks_1/2/3 ("what breaks it") | 25 |
| valuation_lines.rationale | 25 |

## Rewrite rules
- Keep the key figure(s), the source/date or quarter when present (e.g. "10-Q Note 3", "Q3 FY2026"), and the conclusion. Drop repeated context, long parentheticals, hedging and filler.
- Never add a number, name, date or claim that is not in the original. You may drop numbers.
- Keep the original language of each text (English stays English, Spanish stays Spanish).
- Keep the analyst's direction and judgement (bullish/bearish, verdicts) unchanged.
- Plain sentences; semicolons are fine; no bullet characters, no markdown.
- Count words by whitespace split; stay at or under the limit.

## Steps
1. Load the Lovable query tool: ToolSearch with query "select:mcp__Lovable__query_database".
2. Extract the over-limit texts for your positions with the SQL in EXTRACT.sql (replace the ticker list). Save the raw result as JSON to backups/text_trim_2026-10-05/<group>_original.json (a list of objects with table, id, col, old, lim, ticker, member_ticker). This is the backup; write it before changing anything.
3. Write your rewrites to backups/text_trim_2026-10-05/<group>_rewrite.json as a list of {"table","id","column","old","new","limit"}.
4. Run: python3 /home/user/fiscalai/backups/text_trim_2026-10-05/validate.py <that file>. Fix every failure and rerun until "failed": 0.
5. Apply with query_database, in batches of ~20 statements per call:
   - For scorecard_ratings, risks, catalysts, valuation_lines: `update public.<table> set <column> = $t$<new>$t$ where id = '<id>';`
   - For own_thesis: ONE update per row that sets all its changed columns together (a trigger archives the previous version on each update): `update public.own_thesis set bullet_1 = $t$...$t$, breaks_2 = $t$...$t$ where id = '<id>';`
   - If a text contains "$t$", use another dollar tag.
6. Verify with a query that every id you changed now has the new text and is within the limit.
7. Report back: counts per table.column (found / rewritten / applied), any text you left unchanged and why, and 3 before→after examples.
Do not modify anything outside these columns and these positions. Do not touch claims, titles or other tables.
