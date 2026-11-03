# Omaha Value platform — queries and registration

Channel: Lovable connector, tool `query_database`, `project_id = 1cfc33e1-fa07-40f3-a8ee-609966fcebc5`.
Run one statement per call when you need its rows (a multi-statement call returns only the last result).

## Read (before FiscalAI)
1. Position:
   SELECT id, ticker, company_name, bucket, is_basket, price, reporting_currency FROM positions
   WHERE upper(ticker) = '<TICKER>';
   A basket member: find it in basket_members and use the basket's position_id with
   member_ticker = '<TICKER>' in every query below (otherwise member_ticker IS NULL).
2. Decisions in force (always applied; if one clashes with this skill's default, the decision wins
   and the output says so):
   SELECT topic, decision, rationale, decided_at FROM position_decisions
   WHERE (position_id = '<POSITION_ID>' OR position_id IS NULL) AND superseded_at IS NULL
   ORDER BY decided_at DESC;
3. Valuations (primary first; a sum of parts has method = 'sotp'):
   SELECT v.id, v.label, v.method, v.is_primary, v.source_name, v.target_year, v.target_price,
          v.currency, v.shares_outstanding, v.notes, l.label AS line, l.metric_key, l.target_value,
          l.current_value, l.multiple, l.no_multiple, l.rationale
   FROM valuations v LEFT JOIN valuation_lines l ON l.valuation_id = v.id
   WHERE v.position_id = '<POSITION_ID>' AND v.member_ticker IS NOT DISTINCT FROM <MEMBER|NULL>
   ORDER BY v.is_primary DESC, l.sort_order;
4. Thesis, catalysts, risks:
   SELECT * FROM own_thesis WHERE position_id = '<POSITION_ID>';
   SELECT title, detail, impact, probability, quarter_tag, status FROM catalysts
   WHERE position_id = '<POSITION_ID>' ORDER BY sort_order, created_at;
   SELECT * FROM risks WHERE position_id = '<POSITION_ID>';
5. Earlier outputs of the quarter:
   SELECT skill_name, document_name, quarter_tag, artifact_link, result_text, created_at
   FROM skill_outputs WHERE position_id = '<POSITION_ID>' ORDER BY created_at DESC LIMIT 20;

## Register (after publishing)
INSERT INTO skill_outputs (position_id, member_ticker, skill_name, document_name, quarter_tag,
                           artifact_link, result_text)
VALUES ('<POSITION_ID>', <'<MEMBER>'|NULL>, '<reporte_q|q_report>', '<TICKER> Q-Report[ Charts] <2Q26>',
        '<2026Q2>', '<https://claude.ai/artifact/...>', '<neutral 1-3 line summary>');
- `reporte_q` = Q-Report Charts (header button "Q-Report Charts"); `q_report` = narrative Q-Report
  (button "Q-Report"). On a later version of the same report, UPDATE the existing row instead of
  inserting a new one.
- quarter_tag = fiscal year + quarter of the last reported period.
- A basket-wide report goes with member_ticker NULL.
- If a fact changed (a catalyst probability, a thesis claim), propose the UPDATE to the analyst first;
  write it only once they agree.

## Never
- Model identifiers in the database, the report or commits.
- New figures from filings written into the platform: they go in the report with document and page.
