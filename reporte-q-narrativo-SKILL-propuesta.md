---
name: reporte-q
description: >
  Genera el Reporte Q de una posición como ensayo narrativo en primera persona del analista
  (estilo Burry en Substack): una tesis en el título, historia de la empresa, analogías,
  investigación externa citada y solo las cifras que prueban el argumento. ~1,500 palabras,
  artifact HTML con botón "Download PDF", registrado en la plataforma Omaha.
  El Reporte Q chart-first queda como anexo de datos (automatizable).
  Usar cuando el usuario diga "reporte Q", "reporte-q", "/reporte-q TICKER", "reporte trimestral",
  "análisis del trimestre de X". Contenido en inglés.
---

# reporte-q — Reporte Q narrativo

Responde una pregunta: después de este trimestre, ¿la tesis sigue en pie y por qué?
Es un argumento, no un resumen del trimestre. Los números del trimestre ya están en la
plataforma (Financials, Valuation, Q-pulse) y en el anexo chart-first.

## Fase 0 — Preguntas (reverse prompting)
1. La pregunta central del trimestre para la tesis (proponer una a partir del Q-pulse y los
   catalizadores de la plataforma; el analista la corrige).
2. La tesis en una línea y la posición actual (cartera o idea; IVO y margen de seguridad).
3. Largo (por defecto 1,500 palabras) y si hay fuentes que el analista quiere incluir
   (cartas, writeups, Substacks).
Después: preguntar si quiere más preguntas o el resultado.

## Fase 1 — Investigación (tres frentes, cada hecho con fuente)
A. **Plataforma Omaha** (Lovable): `own_thesis`, `valuations` primaria y bear/bull, `catalysts`,
   `risks`, `scorecard_ratings`, último `skill_outputs` (qpulse, reporte_q chart-first).
B. **FiscalAI primero** para toda cifra financiera: el print, segmentos/KPIs, guidance,
   historia larga (crisis pasadas visibles en los números), acciones en circulación, precio.
   Transcript del call: 4–8 citas textuales con nombre y cargo, copiadas exactas.
C. **Investigación externa**, en este orden de prioridad: prensa (Reuters, Bloomberg, FT, prensa
   local de referencia), papers y reportes de reguladores, Substack y cartas de inversores,
   estudios de mercado. **Evitar X y foros con poca interacción.** Buscar:
   - crisis pasadas de la propia empresa y cómo terminaron;
   - un análogo (otra empresa que pasó por lo mismo) y qué hizo su acción;
   - competencia con datos propios;
   - regulación y macro que mueven el trimestre;
   - consenso de analistas, insiders, activistas, cambios de accionistas.
   Cada hecho externo: fuente, fecha, URL y cita corta. Sin fuente → hipótesis marcada o fuera.

## Fase 2 — Esquema antes de escribir
Título = la tesis del ensayo (una frase con opinión). Secciones cortas con títulos que son
afirmaciones. Esqueleto por defecto (adaptar al caso):
1. Gancho: el hecho o la escena que mejor resume el trimestre.
2. Qué pasó (3–5 cifras, no más) y por qué.
3. ¿Ya pasó antes? Historia de la empresa o análogo.
4. Lo que cree el mercado y lo que dice la evidencia.
5. Competencia / regulación / management, según lo que mueva la tesis.
6. Valuación en un párrafo: IVO de la plataforma, cómo se llega (puente de valor), descuento.
7. Dónde puedo estar equivocado (lo débil de la tesis, dicho sin rodeos).
8. Qué miro el próximo trimestre (fechas y umbrales de los catalizadores).
Gráficos: 2–3 como máximo, solo si prueban un punto del texto.

## Fase 3 — Redacción
Primera persona del analista ("I", "my position"). Inglés. ~1,500 palabras (±10%).
Frases cortas y directas. Las citas del call se usan como evidencia y se comentan, no se resumen.
Cada cifra lleva su fuente en una nota numerada al final. Sin adornos ni frases hechas.

## Fase 4 — Validación (bloqueante)
- Cada cifra rastreable a FiscalAI, la plataforma o una fuente externa con link.
- Cada cita textual verificada palabra por palabra contra el transcript o el artículo.
- IVO, precio y descuento iguales a los de la plataforma el día de publicación.
- Conteo de palabras dentro del rango. Lista de hipótesis marcadas como tales.
No se publica si algo falla.

## Fase 5 — Publicar y registrar
Artifact HTML (mismo URL en cada actualización), con botón "Download PDF" (capacidad
`downloads`; el PDF se genera en la página). Registrar en `skill_outputs` (skill_name
`reporte_q`, quarter_tag, artifact_link, result_text = el resumen de 3 líneas). Entregar al
analista: link, conteo de palabras, fuentes usadas, hipótesis y dudas.

## Anexo de datos (chart-first)
El formato chart-first anterior (`reporte-q-SKILL-propuesta.md`) pasa a ser el anexo de datos.
Se puede automatizar: los datos ya están en la plataforma y FiscalAI, y el análisis de cada
gráfico lo puede escribir la IA. El ensayo enlaza al anexo en lugar de repetir sus tablas.
