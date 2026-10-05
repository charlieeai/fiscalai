with p as (select id, ticker from public.positions where ticker in ('TICKER1','TICKER2')),
wc as (select 1)
select json_agg(x) from (
  select 'scorecard_ratings' as table, r.id::text id, 'reason' col, r.reason old, 25 lim, p.ticker, r.member_ticker
  from public.scorecard_ratings r join p on p.id = r.position_id
  where array_length(regexp_split_to_array(trim(r.reason), '\s+'), 1) > 25
  union all
  select 'risks', r.id::text, 'description', r.description, 35, p.ticker, r.member_ticker
  from public.risks r join p on p.id = r.position_id
  where array_length(regexp_split_to_array(trim(r.description), '\s+'), 1) > 35
  union all
  select 'catalysts', c.id::text, 'detail', c.detail, 35, p.ticker, c.member_ticker
  from public.catalysts c join p on p.id = c.position_id
  where array_length(regexp_split_to_array(trim(c.detail), '\s+'), 1) > 35
  union all
  select 'own_thesis', o.id::text, v.col, v.txt, v.lim, p.ticker, o.member_ticker
  from public.own_thesis o join p on p.id = o.position_id
  cross join lateral (values ('bullet_1', o.bullet_1, 45), ('bullet_2', o.bullet_2, 45), ('bullet_3', o.bullet_3, 45),
                             ('breaks_1', o.breaks_1, 25), ('breaks_2', o.breaks_2, 25), ('breaks_3', o.breaks_3, 25)) v(col, txt, lim)
  where array_length(regexp_split_to_array(trim(v.txt), '\s+'), 1) > v.lim
  union all
  select 'valuation_lines', l.id::text, 'rationale', l.rationale, 25, p.ticker, va.member_ticker
  from public.valuation_lines l join public.valuations va on va.id = l.valuation_id join p on p.id = va.position_id
  where array_length(regexp_split_to_array(trim(l.rationale), '\s+'), 1) > 25
) x;
