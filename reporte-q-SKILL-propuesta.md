---
name: reporte-q
description: >
  Genera el Reporte Q de una empresa pública como artifact HTML chart-first (estilo Omaha Inversiones):
  "the print" en tiles, valuación bear/base/bull en cards, fundamentals anuales, momentum trimestral,
  segmentos y una sección del sector, con un gráfico por card (gráfico → tabla de datos → análisis).
  Datos: modelo del usuario / plataforma Omaha → FiscalAI → filings → web (solo macro). Contenido en inglés.
  Usar cuando el usuario diga "reporte Q", "reporte-q", "/reporte-q TICKER", "reporte trimestral",
  "análisis de resultados del trimestre". Bases aprobadas: LEN, CTT, DGE, Auna. Si el usuario pide
  explícitamente un DOCX con forense y guidance, usar el formato anterior (tres partes) y decirlo.
---

# reporte-q — Reporte Q chart-first

Responde una pregunta: qué de lo reportado este trimestre importa para la tesis de largo plazo.
No es un volcado del trimestre.

## Fase 0 — Preguntas (reverse prompting)
1. Trimestre a cubrir (por defecto el último reportado; semestral si la empresa reporta por semestres).
2. KPIs del sector y comparable (proponer una tabla: KPI → fuente; el usuario aprueba).
3. Valuación: tomar bear/base/bull de la plataforma (`valuations`, primaria marcada). Confirmar si hay
   un modelo propio (Excel / art-val) que deba mandar.
Después: preguntar si quiere más preguntas o el resultado.

## Fase 1 — Datos (jerarquía y reglas duras)
1. Modelo del usuario / plataforma Omaha (`valuations`, `valuation_lines`, `own_thesis`, `catalysts`,
   `risks`, `metric_catalog` + `catalog_values` con su fuente).
2. FiscalAI (`company_financials_standardized`, `company_ratios`, `company_segments_and_kpis` con
   `periodType:"quarterly"`, `company_filings` / `filing_pdf` para releases).
3. Filings / IR. 4. Web solo para macro, con fuente.
Cada número graficado debe poder rastrearse; si no, no se grafica ("not available" en el caption).
Gotchas de FiscalAI a revisar siempre: EBITDA = EBIT (margen idéntico), net debt solo de un segmento,
gross margin inflado, FCF rellenado con ceros, semestrales partidos en dos trimestres iguales (usar
semestres), cotizaciones en GBX (peniques). Corrección → anotarla en naranja en el gráfico.
Reglas de casa: net debt histórico como niveles y promedio 3 años, nunca CAGR; caja sin restringida.

## Fase 2 — Construcción
Copiar un reporte base (LEN es el motor más completo) y reemplazar título, cuerpo, datos e `init()`.
No reescribir el `<style>` ni las funciones `render*`. Estructura:
1. Header `Reporte Q — <Empresa> (<TICKER>)`.
2. The print: 7–8 tiles + párrafo "read of the quarter". Beat/miss solo con fuente citada (FiscalAI no
   trae consensos).
3. Valuation bear/base/bull en cards: target, upside, CAGR al año objetivo, ~5 supuestos.
4. Fundamentals anuales (historia larga), 5. Quarterly momentum (8–11 trimestres, KPI líder con YoY),
6. Cash flow / segmentos, 7. Sección del sector, 8. Footer `Omaha Inversiones · Fuente: …`.
10–16 gráficos. Cada card: título → caption → gráfico → tabla → `<details class="analysis" open>`.
Formato: 1 decimal en % y múltiplos; YoY de márgenes en bps; un label por punto; colores por tipo de
métrica (teal revenue, gold EPS, green FCF, blue retornos/deuda, red múltiplos/alerta, slate referencia).

## Fase 3 — Validación (bloqueante)
`node audit.js reporte.html shots/` (Playwright headless) debe dar: `JS errors: none`,
`undefined/NaN/Infinity in text: 0`, `empty tables: 0` y cada gráfico `OK` (marks == labels,
collisions = 0). Mirar 3–4 screenshots de los gráficos más cargados. No se publica si falla.

## Fase 4 — Publicar y registrar
Artifact (mismo URL en cada actualización). Registrar en `skill_outputs` (skill_name `reporte_q`,
quarter_tag, artifact_link, result_text con la lectura del trimestre). Entregar al usuario: link,
período cubierto, número de gráficos, resultado del audit, datos que no se pudieron obtener y dudas
ordenadas de más a menos crítica.
