# Omaha Value como fuente única — texto para los SKILL.md

Para: art-val, one-pager, reporte-q, earnings-forensics (y forensic-accounting).

**Por qué:** hoy cada skill guarda su propia copia de los números y de las decisiones. El net debt de LEN a 3Q26 salió distinto en tres lugares: $4,818M en Valuation, $4,218M en el Reporte Q y $4,200M en el one-pager. Con este bloque, cada skill lee de la plataforma antes de FiscalAI y escribe de vuelta lo que extrae. Una decisión se registra una sola vez.

**Canal:** el conector de Lovable, herramienta `query_database`, con `project_id = 1cfc33e1-fa07-40f3-a8ee-609966fcebc5`.

- **q-pulse** ya lo usa así.
- **Chat:** hay que tener el conector de Lovable habilitado.
- **Claude Code nube:** confirmado; funciona desde esta sesión.
- **Claude Code local (earnings-forensics):** hay que agregar el MCP de Lovable a la configuración local. Esto está **sin verificar**.

---

## Bloque común (pegar en cada SKILL.md, antes del primer paso que use FiscalAI)

```markdown
## Paso 0 — Omaha Value primero (conector Lovable, query_database, project_id 1cfc33e1-fa07-40f3-a8ee-609966fcebc5)

1. Posición:
   SELECT id, ticker, company_name, bucket FROM positions WHERE upper(ticker) = '<TICKER>';
   Si hay más de una fila (portfolio e ideas), usa la del bucket que indique el usuario; si no indica, pregunta.
   Si la empresa es miembro de una canasta, busca en basket_members y usa el position_id de la canasta con member_ticker = '<TICKER>'.

2. Decisiones en vigor (se aplican SIEMPRE; si chocan con el método por defecto de esta skill, gana la decisión y lo dices en el output):
   SELECT topic, decision, rationale, decided_at
   FROM position_decisions
   WHERE (position_id = '<POSITION_ID>' OR position_id IS NULL) AND superseded_at IS NULL
   ORDER BY decided_at DESC;
   position_id NULL = regla de la casa, aplica a todas las empresas.

3. Libro de datos (usar ANTES que FiscalAI):
   SELECT metric, label, segment, period, period_type, fiscal_year, fiscal_quarter, value, unit,
          source_type, source_ref, source_page, note
   FROM data_points
   WHERE position_id = '<POSITION_ID>' AND status = 'active'
   ORDER BY metric, segment, fiscal_year, fiscal_quarter NULLS LAST;
   - unit: USD_M = millones de USD; USD = dólares; units = unidades; pct = porcentaje en puntos (22.8 = 22.8%); x = múltiplo.
   - Si un dato está en el libro y en FiscalAI y difieren más de 1%: usa el libro y muestra el de FiscalAI como nota.
   - Si falta en el libro: usa FiscalAI y márcalo como "FiscalAI" en el output.

4. Conflictos abiertos (no los resuelvas tú; menciónalos en el output):
   SELECT label, segment, period, value, source_ref FROM data_points
   WHERE position_id = '<POSITION_ID>' AND status = 'conflict';

## Paso final — escribir de vuelta

5. Cada cifra que esta skill tomó de un filing o release y que NO está en el libro se inserta, una fila por cifra.
   Nunca hagas UPDATE de una fila existente. Si ya hay un valor activo distinto, la tuya entra como 'conflict':
   INSERT INTO data_points (position_id, member_ticker, metric, label, segment, period, period_type,
                            fiscal_year, fiscal_quarter, period_end, value, unit,
                            source_type, source_ref, source_page, note, status)
   SELECT '<POSITION_ID>', NULL, '<metric_key>', '<Label>', '<Segment>', '<FY2025|3Q FY2026>', '<annual|quarterly|ltm>',
          <año>, <trimestre o NULL>, '<AAAA-MM-DD>', <valor>, '<USD_M|USD|units|pct|x>',
          'skill', '<nombre-skill> · <documento>', '<página>', '<fórmula o NULL>',
          CASE WHEN EXISTS (SELECT 1 FROM data_points d WHERE d.position_id = '<POSITION_ID>'
                              AND d.metric = '<metric_key>' AND d.segment = '<Segment>'
                              AND d.period = '<período>' AND d.status = 'active')
               THEN 'conflict' ELSE 'active' END
   WHERE NOT EXISTS (SELECT 1 FROM data_points d WHERE d.position_id = '<POSITION_ID>'
                       AND d.metric = '<metric_key>' AND d.segment = '<Segment>'
                       AND d.period = '<período>' AND d.value = <valor>);
   metric_key = la etiqueta en minúsculas, "&" → "and", todo lo que no sea letra o número → "_"
   (ej. "Homebuilding SG&A pct" → homebuilding_sg_and_a_pct). Usa SIEMPRE la misma etiqueta para la misma métrica.
   Cifras de web search o no verificadas: NO se escriben.

6. Registrar el output:
   INSERT INTO skill_outputs (position_id, member_ticker, skill_name, quarter_tag, artifact_link, result_text)
   VALUES ('<POSITION_ID>', NULL, '<art_val|one_pager|reporte_q|earnings_forensics|forensic_accounting>',
           '<3Q FY2026>', '<https://claude.ai/artifact/...>', '<resumen de 1-3 líneas>');
   Usa el link de la forma claude.ai/artifact/<id>, no claude.ai/public/artifacts/..., para que se pueda leer después.
```

---

## Notas por skill (agregar debajo del bloque común)

### art-val
- La tabla histórica y el ancla LTM salen del libro cuando existen. Así el modelo parte de los mismos números que Valuation.
- Los presets bear/base/bull deben respetar las decisiones. Ejemplo: net debt consolidado en el EV si `net_debt` lo dice.
- Escribe de vuelta solo los KPIs que verificó en filings. Los de web search quedan fuera del libro.

### one-pager
- Net debt, EBITDA y EV/EBITDA siguen las decisiones de la posición. El one-pager de LEN mezcló deuda Homebuilding ($4,297M) con la etiqueta "consolidated".
- El comparable (DHI, NVR…) usa el libro de su propia posición si existe; si no, FiscalAI.

### reporte-q
- Es la principal fuente trimestral del libro. Escribe los KPIs del release: orders, deliveries, ASP, backlog, margen, SG&A, deuda y caja por segmento. Todos con documento y página.
- Antes de escribir, compara con lo que ya hay en el libro. Si difiere, entra como conflicto y lo dices en la sección de verificación.

### earnings-forensics / forensic-accounting
- Lee las decisiones y el libro para usar las mismas definiciones que el resto (deuda consolidada, EBITDA con D&A real).
- Escribe de vuelta solo cifras extraídas de los PDFs con página.
