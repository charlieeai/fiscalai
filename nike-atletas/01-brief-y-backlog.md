# Estudio Nike: atletas top y "mercado de pases" (2015–2026)

Brief y backlog para continuar en Claude Code. Leer junto con `02-metodologia.md`.

## Objetivo

Medir qué proporción de los mejores atletas de cada deporte tiene contrato con Nike Inc. (Nike + Jordan + Converse), cómo cambió por año y qué movimientos de marca lo explican.

**Detonante:** Kylian Mbappé dejó Nike y firmó con On (18-sep-2026).

**Uso final:** tesis de inversión de NKE en Omaha. El entregable es un artifact HTML interactivo, autocontenido, en español.

## Archivos de partida

| Archivo | Contenido |
|---|---|
| `nike-atletas-top.html` | Artifact actual (v3). Los datos viven en constantes JS: `R` (rankings por deporte y corte), `WOMEN`, `MOVES`, `FIN`, `S` (fuentes), `BORN` (años de nacimiento). |
| `atletas.csv` | Export de `R` y `WOMEN`: 210 filas. |
| `movimientos.csv` | Export de `MOVES`: 37 filas. |

**Primer paso en Claude Code:** convertir los CSV en la fuente única de verdad y generar el HTML desde ellos (ver pipeline en `02-metodologia.md`). Los datos no se vuelven a escribir a mano dentro del HTML.

## Estado actual (v3, 1-oct-2026)

| Deporte | Cortes con datos | Tamaño del top |
|---|---|---|
| Fútbol | 2015, 2018, 2021, 2024, 2026 | 10 |
| Básquet | 2015, 2018, 2021, 2024, 2026 | 10 |
| Tenis | 2015, 2018, 2021, 2024, 2026 | 10 |
| Golf | 2015 (top 5), 2024 (top 5), 2026 (top 10) | — |
| NFL | solo 2026 | 5 |
| Béisbol | solo 2026 | 5 |
| Atletismo | solo 2026 | 5 |
| Mujeres | solo 2026: tenis, fútbol, básquet, atletismo, gimnasia | 5 |

**Resultado principal hasta ahora (proporción Nike):**

| Deporte | 2015 | 2018 | 2021 | 2024 | 2026 |
|---|---|---|---|---|---|
| Fútbol | 5/10 | 6/10 | 4/10 | 6/10 | 3/10 |
| Básquet | 4/10 | 6/10 | 5/10 | 6/10 | 6/10 |
| Tenis | 2/10 | 2/10 | 2/10 | 3/10 | 2/10 |
| Golf (2026) | | | | | 3/10 |

En golf, Nike tiene a los números 1 y 2 del mundo.

**Datos no determinados:** quedan 36 atletas con marca n.d. (lista abajo).

## Decisiones ya tomadas por el usuario (no reabrir)

1. Se excluyen cricket y F1.
2. La ponderación entre deportes es cualitativa: orden por audiencia global según criterio, sin pesos numéricos.
3. El criterio de "atleta top" es el ranking deportivo. Las redes sociales no se usan.
4. Solo se cuentan contratos individuales de atletas. Los uniformes de club o equipo no cuentan.
5. Marcas principales: Nike, Jordan, Converse, Adidas, Puma, Under Armour, On, New Balance, ASICS, Anta y Li-Ning. Cualquier otra se muestra como "Otro" con el nombre al lado.
6. "n.d." solo se usa cuando no hay información tras buscar. Nunca se adivina.
7. Las mujeres van en un panel aparte (hoy solo el corte 2026).
8. Movimientos clave a resaltar: Mbappé, Fritz, Yamal, Bonmatí, Kvaratskhelia, Neymar, Federer. Se agregaron Tiger Woods, Jokić y Curry.
9. Menciones honoríficas (MH) en los paneles 2026 de hombres, sin contar en el total:
   - Fútbol: Cristiano Ronaldo.
   - Básquet: Michael Jordan y Stephen Curry.
   - Tenis: Djokovic.
10. La sección "Método y límites" se eliminó del artifact; la metodología vive en este repo.

## Backlog (en orden de prioridad)

### P1. Agregar cortes 2022, 2023 y 2025

- **Qué:** las columnas de la matriz pasan a ser 2015, 2018, 2021, 2022, 2023, 2024, 2025 y 2026, en los 7 deportes.
- **Ranking:** el de cada deporte, definido en `02-metodologia.md`.
- **Aceptación:** cada celda tiene su lista completa y cada atleta tiene marca o n.d. con al menos 2 búsquedas registradas.

### P2. Completar los cortes históricos faltantes

- **NFL:** top 5 de la votación al MVP de la AP en todos los cortes. El corte Y corresponde al MVP anunciado en el año Y.
- **Béisbol y atletismo:** todos los cortes, con el ranking definido en metodología.
- **Golf:** agregar 2018 y 2021, y ampliar 2015 y 2024 de top 5 a top 10 (OWGR de fin de año).

### P3. Cerrar los n.d. actuales

| Grupo | Atletas |
|---|---|
| Fútbol | Alexis Sánchez (2015), Varane (2018), Jorginho (2021), Donnarumma (2021), Cubarsí (2026; una fuente débil dice Adidas) |
| Básquet | Marc Gasol, LaMarcus Aldridge, DeMarcus Cousins, Pau Gasol (2015); Aldridge (2018); Julius Randle (2021); Anthony Davis (2024) |
| Tenis | Berdych, Tsonga (2015); Kevin Anderson, Čilić, Thiem, Isner (2018); Rublev, Berrettini (2021); Rublev, Dimitrov (2024) |
| Golf | Bubba Watson (2015); Morikawa, Åberg (2024); Fitzpatrick, Wyndham Clark, Sam Burns (2026) |
| Mujeres | Andreeva (tenis); Paralluelo, Pajor (fútbol); Julien Alfred (atletismo); Rebeca Andrade, Suni Lee, Jordan Chiles, Kaylia Nemour (gimnasia) |

**Regla para Rublev:** se sabe que desde 2025 es imagen de K-Swiss. Hay que confirmar su marca a fin de 2021 y a fin de 2024.

### P4. Convertir hipótesis en datos verificados

Todas las filas con confianza `h` deben buscarse y pasar a `v`, o quedar en `h` con nota del motivo. Prioridad:

1. Atletas en el top 3 de cada corte.
2. Datos de 2022 o anteriores usados en el corte 2026: Soto, Witt Jr. y Cameron Young.
3. Todo el panel de NFL 2026.

### P5. Movimientos (`movimientos.csv`)

- **Completar el campo "de"** donde dice n.d.: Swiatek, Shelton, Raducanu (destino) y Draper (destino).
- **Agregar movimientos que surjan de P1 a P4.** Siempre que un atleta cambie de marca entre dos cortes, debe existir la fila correspondiente.
- **Mbappé:** mantener las dos versiones de la causa.
  - CNBC, con fuente anónima: Nike no renovó.
  - The Irish Times: Nike ofreció 10 años por más de €20 mm anuales y Mbappé eligió On (efectivo más acciones).
  - Buscar si The Athletic u otra fuente primaria resuelve la contradicción.
- **Fechas de Fritz y Tiafoe:** verificar las fechas exactas. Fritz hoy figura como "2025–26".

### P6. Ancla financiera

- **Ya incluido:** demand creation de NKE FY2015–FY2026, tomado de FiscalAI.
- **Pendiente:** leer en el 10-K FY2026 de NKE la nota de compromisos por contratos de endorsement. No está en los datos estructurados de FiscalAI: usar `company_filings` + `filing_pdf` o `filing_page_image`.
- **Opcional:** el mismo análisis de demand creation para ONON y Adidas, para comparar la intensidad de gasto.

### P7. Revisión visual

Aplicar el checklist de QA de `02-metodologia.md` antes de entregar.

## Cambios de diseño ya aplicados en v3 (mantener)

- Los párrafos ocupan todo el ancho del contenedor.
- La matriz muestra solo "x/N". No muestra n.d.; el n.d. se acepta únicamente en la lista desplegable de cada celda.
- Las fuentes aparecen como un ícono "?" que enlaza a la fuente; el subtítulo de cada sección lo explica.
- Las filas clave del mercado de pases van resaltadas con la etiqueta "Clave".
- La etiqueta "Promesa" marca a atletas de 23 años o menos en cortes y movimientos 2023–2026, sin importar la marca. Hay además una sección "Promesas 2023–2026 y su marca".
- Paneles "Hombres, corte 2026" y "Mujeres, corte 2026" con top 5 por deporte. Las MH van al final del panel de hombres y no cuentan en el total.
- Se eliminó la sección "Método y límites".

## Tensiones abiertas (no resolver por inferencia)

- **Mbappé:** las fuentes se contradicen sobre si Nike quiso o no retenerlo.
- **Reasignación vs. pérdida en subastas:** la lectura de que Nike reasigna dinero hacia básquet y pocos nombres, en lugar de perder subastas, es una hipótesis. Hay que contrastarla con los compromisos de endorsement del 10-K (P6).

## Estado al 1-oct-2026 (sesión Claude Code)

**Hecho:** pipeline (CSV → `validate.py` → `build.py` → `check.js`), P3, P4 (parcial), P5 y P6. P1 y P2 siguen pendientes.

**Proporción Nike tras la actualización:**

| Deporte | 2015 | 2018 | 2021 | 2024 | 2026 |
|---|---|---|---|---|---|
| Fútbol | 6/10 | 7/10 | 5/10 | 5/10 | 2/10 |
| Básquet | 8/10 | 7/10 | 6/10 | 7/10 | 6/10 |
| Tenis | 2/10 | 2/10 | 3/10 | 2/10 | 2/10 |
| Golf | 1/5 | | | 2/5 | 3/10 |
| NFL | | | | | 2/5 |

**Cambios de dato relevantes:**
- Harry Kane: Skechers desde 2023, no Nike. Fútbol 2024 baja de 6 a 5 y 2026 de 3 a 2.
- Taylor Fritz: Boss desde mar-2024; tenis 2024 baja de 3 a 2. TennisAvid (2024) aún lo listaba con Nike: se registran ambas versiones.
- Rublev: K-Swiss desde ago-2024, no desde 2025. Entre 2023 y mediados de 2024 vistió su marca Rublo.
- LaMarcus Aldridge (Jordan) y el cierre de los n.d. de 2015 suben básquet 2015 de 4 a 8, pero varias de esas filas son hipótesis.
- NFL 2026 ahora usa el top 5 de la votación MVP AP (temporada 2025): Stafford, Maye, Allen (New Balance), McCaffrey (While On Earth) y Lawrence.
- P6: obligaciones por endorsement del 10-K: US$7.6 mil mm (FY23), 10.6 (FY24), 16.2 (FY25, incluye marketing asociado), 15.5 (FY26). Porción a 12 meses: 1.3, 1.7, 1.6, 1.7.

**Pendiente o con reservas:**
- Los agentes de búsqueda no pudieron abrir la mayoría de las páginas (el proxy las bloqueó). Muchos `v` se basan en el resultado de búsqueda y no en el texto de la página. Conviene abrir manualmente las fuentes de las filas clave.
- Siguen en `h`: Jokić 2021, Djokovic 2015, Zverev 2021, Duplantis, Warholm y Kipchoge 2026, Stafford, Maye y Lawrence (NFL) y la mayoría de las filas de básquet 2015–2024.
- Siguen en n.d.: Matt Fitzpatrick 2026 (Castore, Skechers o Greyson; fuentes en conflicto) y Ewa Pajor.
- Hay 11 años de nacimiento sin fuente (`verificado = 0` en `nacimientos.csv`).
- Mbappé: The Athletic diría que fue Mbappé quien terminó la relación, pero no hay URL verificable. Sigue sin resolverse.
- Béisbol y atletismo 2026 siguen con criterio propio hasta que se publiquen la votación MVP (nov-2026) y los finalistas de World Athletics.
- Movimientos nuevos que podrían marcarse como clave (decisión del usuario): Harry Kane, Josh Allen.

## Estado al 2-oct-2026 (segunda tanda)

**Hecho:**
- Verificación de 14 datos clave por corroboración en búsquedas.
  - Kane: el contrato con Nike venció en el verano de 2023 sin renovarse; no en ago-2022.
  - Fritz: ropa Boss en mar-2024 y calzado Asics en ago-2024.
  - Bonmatí: ninguna fuente dice que Nike quisiera retenerla; se corrigió la causa.
  - Kvaratskhelia ("Nike no renovó") baja a h: lo dice una sola fuente.
  - Mbappé: The Irish Times cita a The Athletic. Según esa versión, Mbappé eligió On.
- P1 completo en tenis (2022, 2023, 2025) y básquet (2022, 2023, 2025), y fútbol 2022.
- P2: NFL 2018–2025, béisbol 2015, 2018 y 2021, y golf 2015 (top 10) y 2018.
- Movimientos clave nuevos: Harry Kane y Josh Allen.
- `scripts/ingest.py` incorpora los JSON de investigación a los CSV.

**Pendiente (`data/pendiente/`).** Estos cortes no se publican porque tienen n.d. con menos de 2 búsquedas:
- Fútbol 2023 y 2025.
- NFL 2015.
- Béisbol 2022 a 2025.
- Golf 2021 a 2025.
- Atletismo, todos los cortes históricos.
Se agotó el cupo de 200 búsquedas web de la sesión.

**Limitación de red:** WebFetch y curl están bloqueados para los sitios de fuentes; solo funciona WebSearch. Las filas nuevas llevan `metodo = busqueda`. Cuando se habilite la red, conviene reabrir esas fuentes.
