# Omaha Value como fuente única — texto para los SKILL.md

Para: art-val, one-pager, reporte-q, q-pulse, earnings-forensics (y forensic-accounting).

**Por qué:** cada skill guardaba su propia copia de los números y de las decisiones. El net debt de LEN a 3Q26 salió distinto en tres lugares: $4,818M en Valuation, $4,218M en el Reporte Q y $4,200M en el one-pager. Con este bloque, cada skill lee de la plataforma antes de FiscalAI. Una decisión se registra una sola vez, y las cifras propias viven en el catálogo de métricas de cada empresa.

**Cómo están guardadas las cifras (desde el 30-sep-2026):**

- `metric_catalog`: las métricas de cada empresa, con su definición.
  - `kind = 'input'`: las llena el analista en su Google Sheet.
  - `kind = 'derived'`: las calcula la plataforma con `formula`.
- `catalog_values`: los valores de los inputs.
  - Vienen de la última importación del Sheet (`source` = lo que escribió el analista) o de la precarga de FiscalAI (`source = 'FiscalAI'`).
  - El Sheet es la fuente de verdad: una importación reemplaza todos los valores de la empresa.
- `data_points` (el Data book viejo) queda solo como archivo histórico. **No se escribe más ahí.**

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

3. Catálogo de la empresa (definiciones y fórmulas):
   SELECT key, label, kind, unit, segment, definition, formula, aggregation, section
   FROM metric_catalog WHERE position_id = '<POSITION_ID>' AND member_ticker IS NOT DISTINCT FROM <MEMBER|NULL>
   ORDER BY sort_order;
   - Usa las definiciones del catálogo para nombrar y calcular (ej. EBITDA, net debt, homes delivered).
   - unit: USD_M = millones de la moneda de reporte (la definición lo dice si no es USD); USD = unidades de
     moneda; units = unidades; M_units = millones de unidades; pct = puntos (22.8 = 22.8%); x = múltiplo.

4. Valores (usar ANTES que FiscalAI):
   SELECT metric_key, period, period_type, fiscal_year, fiscal_quarter, value, source, source_ref, note
   FROM catalog_values WHERE position_id = '<POSITION_ID>' AND member_ticker IS NOT DISTINCT FROM <MEMBER|NULL>
   ORDER BY metric_key, fiscal_year, fiscal_quarter NULLS FIRST;
   - Períodos: 'FY2025', '3Q FY2026', 'LTM 3Q FY2026'.
   - LTM que falte: flujos = suma de 4 trimestres; saldos = último trimestre; aggregation 'avg' = promedio.
   - Derivadas: calcúlalas con la fórmula del catálogo sobre estos valores; si falta un input, no la inventes.
   - source distinto de 'FiscalAI' = cifra del analista: gana siempre. Si FiscalAI difiere >1%, muéstralo como nota.
   - Si falta en el catálogo: usa FiscalAI y márcalo "FiscalAI" en el output.

## Paso final — registrar el output

5. INSERT INTO skill_outputs (position_id, member_ticker, skill_name, quarter_tag, artifact_link, result_text)
   VALUES ('<POSITION_ID>', <'<MEMBER>'|NULL>, '<qpulse|art_val|one_pager|reporte_q|earnings_forensics|forensic_accounting>',
           '<2026Q3>', '<https://claude.ai/...>', '<resumen de 1-3 líneas o el texto completo de q-pulse>');
   - quarter_tag = año fiscal + trimestre del último período reportado.
   - En canastas, el output de un miembro va con su member_ticker; un one-pager o Reporte Q de toda la canasta
     va con member_ticker NULL.

6. Cifras nuevas extraídas de filings: NO se escriben en la base. Van en el output con documento y página;
   el analista las pasa a su Sheet si las acepta.
```

---

## Notas por skill (agregar debajo del bloque común)

### art-val
- La tabla histórica y el ancla LTM salen del catálogo cuando existen. Así el modelo parte de los mismos números que Valuation.
- Los presets bear/base/bull respetan las decisiones. Ejemplo: net debt consolidado en el EV si `net_debt` lo dice.

### one-pager
- Net debt, EBITDA y EV/EBITDA siguen las definiciones del catálogo y las decisiones de la posición.
- El comparable usa el catálogo de su propia posición si existe; si no, FiscalAI.

### reporte-q
- Compara los KPIs del release con `catalog_values`. Cada diferencia >1% va en la sección de verificación, con documento y página.
- Lista al final las cifras del trimestre que el analista debería agregar a su Sheet.

### q-pulse
- Usa la tesis (`own_thesis`: claims y breakers), el scorecard y la valuación primaria de la plataforma como vara.
- La cifra del trimestre que choque con un breaker se cita con su fuente.

### earnings-forensics / forensic-accounting
- Usa las mismas definiciones del catálogo (deuda consolidada, EBITDA con D&A real).
