# Q-Pulse — patch for scorecard v2 (proposal)

The `qpulse` skill still reads the legacy traffic-light scorecard. Since 1 Oct 2026 the app
uses `scorecard_ratings` (5 pillars, 12 criteria, 0–4 by Dante and Christian, reasons by
Christian). The legacy color/rationale columns on `scorecard` are marked DEPRECATED
(migration `20261002120000_scorecard_legacy_deprecated.sql`) and are no longer shown or
edited in the app. They are kept only until this skill is updated; after that they can be
dropped.

## Problems in the current skill

1. Line 4 ("Scorecard read") names the six old pillars (circulo / moat / management /
   cashflow / debt / mos). Circle of competence no longer exists.
2. The read query pulls `s.circulo_*`, `s.moat_*`, `s.management_*`, `s.cashflow_*`,
   `s.debt_color/rationale`, `s.mos_color/rationale`. These are frozen: nobody updates them.
3. The query joins `own_thesis` and `scorecard` on `position_id` only. Both tables now carry
   one row per basket member (`member_ticker`), so for a member (e.g. ADBE in SAAS) the join
   returns several rows (the basket row plus each member's). The text "thesis and pillars
   are basket-wide" is out of date.
4. The valuation join returns Bear, Base and Bull (three rows) for a basket member, because
   it filters members by `member_ticker` only. `is_primary` is now set per member (the Base
   scenario), so the join should require it for members too.
5. The query reads `bullet_1..3` but not the registered claims and breaks
   (`claim_1..3`, `breaks_1..3`), which are what a print should be scored against.

## Proposed replacement — Line 4

4. **Scorecard read**: name any of the 12 criteria whose rating this print calls into
   question, grouped by pillar — Strength (financial_resilience, gross_margin,
   returns_on_capital, free_cash_flow, capital_allocation), Moat (moat_strength,
   moat_durability), Potential (optionality, organic_growth), Culture (leadership, culture),
   Margin of safety (margin_of_safety) — with the current Christian rating (0–4) and the
   direction of the suggested change, or `sin cambios`. Opinion for the analyst; Q-pulse does
   not write to `scorecard_ratings`.

## Proposed replacement — read query

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
           and r.member_ticker is not distinct from tgt.member_ticker) as ratings,
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

Also replace the paragraph "The thesis (`own_thesis`, 3 bullets) and the qualitative pillars
(`scorecard`: circulo, moat, …) are basket-wide" with: "Thesis, claims/breaks and scorecard
ratings are per member in a basket (`member_ticker`); the basket row has `member_ticker` null."

Tested read-only on 2 Oct 2026 for ADBE (one row, 12 ratings, VIO 386.78 Base). Not yet run inside a Q-Pulse run: the query was written against the current schema
(`own_thesis.member_ticker`, `scorecard.member_ticker`, `scorecard_ratings`), not executed
inside a Q-Pulse run.
