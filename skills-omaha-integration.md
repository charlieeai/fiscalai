# Omaha Value como fuente única — texto para los SKILL.md

Para: art-val, one-pager, reporte-q, q-pulse, earnings-forensics (y forensic-accounting).

**Por qué:** cada skill guardaba su propia copia de los números y de las decisiones. El net debt de LEN a 3Q26 salió distinto en tres lugares: $4,818M en Valuation, $4,218M en el Reporte Q y $4,200M en el one-pager. Con este bloque, cada skill lee de la plataforma antes de FiscalAI. Una decisión se registra una sola vez.

**Cifras (desde el 21-oct-2026):** el catálogo de métricas (`metric_catalog`, `catalog_values`) se retiró de la plataforma; las tablas quedan archivadas (ver `backup/metric-catalog/README.md`). Las cifras salen de la valuación de la plataforma (`valuations`, `valuation_lines`) y, después, de FiscalAI. `data_points` (el Data book viejo) queda solo como archivo histórico.

**Canal:** el conector de Lovable, herramienta `query_database`, con `project_id = 1cfc33e1-fa07-40f3-a8ee-609966fcebc5`.

---

## Bloque común (pegar en cada SKILL.md, antes del primer paso que use FiscalAI)

```markdown
## Paso 0 — Omaha Value primero (conector Lovable, query_database, project_id 1cfc33e1-fa07-40f3-a8ee-609966fcebc5)

1. Posición:
   SELECT id, ticker, company_name, bucket, is_basket FROM positions WHERE upper(ticker) = '<TICKER>';
   Si la empresa es miembro de una canasta, búscala en basket_members y usa el position_id de la canasta
   con member_ticker = '<TICKER>' en todas las consultas siguientes (si no, member_ticker IS NULL).

2. Decisiones en vigor (se aplican SIEMPRE; si chocan con el método por defecto de esta skill, gana la
   decisión y lo dices en el output):
   SELECT topic, decision, rationale, decided_at FROM position_decisions
   WHERE (position_id = '<POSITION_ID>' OR position_id IS NULL) AND superseded_at IS NULL
   ORDER BY decided_at DESC;
   position_id NULL = regla de la casa (ej. historia de net debt = promedio 3 años, nunca CAGR).

3. Valuación de la plataforma (antes que FiscalAI para las cifras que ya están ahí):
   SELECT v.id, v.label, v.method, v.is_primary, v.target_price, v.currency, l.label, l.metric_key,
          l.target_value, l.current_value, l.multiple, l.rationale
   FROM valuations v LEFT JOIN valuation_lines l ON l.valuation_id = v.id
   WHERE v.position_id = '<POSITION_ID>' AND v.member_ticker IS NOT DISTINCT FROM <MEMBER|NULL>
   ORDER BY v.is_primary DESC, l.sort_order;
   - Lo que no esté ahí: FiscalAI, marcado "FiscalAI" en el output.

## Paso final — registrar el output

4. INSERT INTO skill_outputs (position_id, member_ticker, skill_name, quarter_tag, artifact_link, result_text)
   VALUES ('<POSITION_ID>', <'<MEMBER>'|NULL>, '<qpulse|art_val|one_pager|reporte_q|q_report|earnings_forensics|forensic_accounting>',
           '<2026Q3>', '<https://claude.ai/...>', '<resumen de 1-3 líneas o el texto completo de q-pulse>');
   - quarter_tag = año fiscal + trimestre del último período reportado.
   - reporte_q = Q-Report Charts (chart-first); q_report = Q-Report narrativo. Cada uno tiene su botón en el header.
   - En canastas, el output de un miembro va con su member_ticker; un one-pager o Q-Report de toda la canasta
     va con member_ticker NULL.

5. Cifras nuevas extraídas de filings: NO se escriben en la base. Van en el output con documento y página.
```

---

## Notas por skill (agregar debajo del bloque común)

### art-val
- El ancla LTM parte de los mismos números que la valuación de la plataforma cuando existen.
- Los presets bear/base/bull respetan las decisiones. Ejemplo: net debt consolidado en el EV si `net_debt` lo dice.

### one-pager
- Net debt, EBITDA y EV/EBITDA siguen las decisiones de la posición.

### reporte-q
- Formato: HTML chart-first (guía `GUIA-reporte-q-chart-first.md`; bases aprobadas LEN, CTT, DGE, Auna). No el DOCX.
- Se registra como `reporte_q` (botón "Q-Report Charts"). El análisis de cada gráfico se titula "AI Analysis".

### q-report
- Ensayo narrativo sobre el Q-Report Charts del mismo trimestre (skill `q-report`). Se registra como `q_report` (botón "Q-Report").

### q-pulse
- Usa la tesis (`own_thesis`: claims y breakers), el scorecard y la valuación primaria de la plataforma como vara.
- El scorecard vive en `scorecard_ratings`: 12 criterios (`criterion`), nota 0–4 de `dante` y de `christian`, y `reason` (solo Christian). Pesos por pilar: Strength 15, Moat 25, Potential 15, Culture 25, Margin of safety 20, repartidos en partes iguales entre sus criterios; puntos = peso × nota / 4; score sobre 100. Los colores de `scorecard` (`*_color`) ya no se usan; esa tabla solo guarda las cifras de deuda y el mínimo de 52 semanas.
- La cifra del trimestre que choque con un breaker se cita con su fuente.

### earnings-forensics / forensic-accounting
- Usa las decisiones de la posición (deuda consolidada, EBITDA con D&A real).
