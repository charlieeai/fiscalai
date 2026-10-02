# Metodología: cómo se construye el estudio y el artifact

## 1. Principios

1. **Datos financieros:** siempre se consultan primero en FiscalAI (MCP o API). Otras fuentes solo complementan.
2. **Toda marca necesita fuente.** Si no hay fuente, el dato es una hipótesis (`h`), no un hecho. Con evidencia insuficiente se pone `n.d.`; nunca se adivina.
3. **Contradicciones entre fuentes:** se registran ambas versiones. No se elige una por inferencia.
4. **Sin prosa decorativa:** textos en español, frases directas y voz activa.

## 2. Modelo de datos

Son dos CSV, que funcionan como fuente única de verdad. El HTML se genera desde ellos; nunca se editan datos dentro del HTML.

### `atletas.csv` (una fila por atleta, deporte y corte)

| Campo | Descripción |
|---|---|
| `deporte` | futbol, basquet, tenis, golf, nfl, beisbol, atletismo (en mujeres, el nombre del panel) |
| `genero` | M / F |
| `corte` | Año del corte (2015, 2018, 2021, 2022, 2023, 2024, 2025, 2026) |
| `rank` | Posición en el ranking del corte; "MH" para mención honorífica |
| `atleta` | Nombre canónico (siempre igual entre cortes) |
| `marca` | Marca real del contrato principal (calzado o indumentaria), "Sin contrato" o "n.d." |
| `nike_inc` | 1 si la marca es Nike, Jordan o Converse |
| `confianza` | `v` = verificado con fuente; `h` = hipótesis o dato con más de 2 años; `n` = no determinado |
| `fuente_nombre`, `fuente_url` | Fuente principal. Solo URLs que existan de verdad. |
| `nota` | Contexto breve, por ejemplo "Dejó Nike en 2024" o "Dato de 2022" |
| `tipo_ranking` | Qué ranking define el top (ver sección 3) |
| `anio_nacimiento` | Vive en `data/nacimientos.csv` (con fuente y `verificado`), porque también lo usan los movimientos. |
| `busquedas` | Número de búsquedas hechas cuando el resultado es `n.d.`. Mínimo 2 antes de aceptar n.d. |

### `movimientos.csv` (una fila por cambio de marca)

| Campo | Descripción |
|---|---|
| `anio` | Año del cambio; se admite un rango ("2025–26") si la fecha no es exacta |
| `atleta`, `deporte` | — |
| `de`, `a` | Marca de origen y de destino |
| `tipo` | `out` = sale de Nike Inc.; `in` = llega o renueva con Nike Inc.; `rival` = entre otras marcas |
| `causa` | Solo la que reporta una fuente (ver taxonomía en la sección 6) |
| `confianza` | `v` / `h` / `n` |
| `fuentes_url` | Una o más URLs, separadas por " \| " |
| `clave` | 1 si el movimiento es de alto impacto |

## 3. Definición del top por deporte

| Deporte | Ranking | Tamaño | Regla de corte |
|---|---|---|---|
| Fútbol | Balón de Oro (France Football) | 10 | Corte Y = clasificación de la edición Y. Para 2026, hasta la gala del 26-oct-2026, se usa el power ranking de GOAL (8-sep-2026); después se reemplaza por la clasificación oficial. |
| Básquet | All-NBA primer y segundo equipo | 10 | Corte Y = temporada que termina en Y |
| Tenis (ATP) | Ranking ATP de fin de año | 10 | Corte 2026 = ranking del 14-sep-2026 (actualizar a fin de año) |
| Golf | OWGR de fin de año | 10 | Corte 2026 = OWGR del 20-sep-2026 |
| NFL | Top 5 de la votación al MVP de la AP | 5 | Corte Y = MVP anunciado en Y (temporada Y-1). Si no hay votos completos publicados, usar los finalistas y documentarlo. Corte 2026 = votación de feb-2026 (Yahoo Sports). |
| Béisbol | Top 5 combinado de la votación al MVP de AL y NL (BBWAA), ordenado por puntos | 5 | Corte Y = temporada Y. Aprobado por el usuario (1-oct-2026). El corte 2026 usa criterio propio hasta la votación de nov-2026. |
| Atletismo | Finalistas a Atleta Masculino del Año de World Athletics | 5 | Corte Y = edición Y. Aprobado por el usuario (1-oct-2026). El corte 2026 usa criterio propio hasta que se publiquen los finalistas. |
| Mujeres | Tenis WTA top 5. Fútbol: Balón de Oro Femenino top 5 (hoy criterio propio). WNBA, atletismo y gimnasia: criterio propio documentado. | 5 | Hoy solo corte 2026 |

**Orden de los deportes en la matriz** (audiencia global, criterio cualitativo): fútbol, básquet, tenis, golf, NFL, béisbol, atletismo.

## 4. Normalización de marcas

| Grupo | Marcas | Cómo se muestra |
|---|---|---|
| Nike Inc. | Nike, Jordan, Converse | Chip azul de Nike |
| Principales | Adidas, Puma, Under Armour, On, New Balance, ASICS, Anta, Li-Ning | Chip con su color |
| Otras | Lacoste, Uniqlo, Yonex, Boss, Lululemon, 361, Wilson, Descente, Peter Millar, Reebok, Athleta, 741, etc. | Chip "Otro" con el nombre real al lado, en gris |
| Sin marca | "Sin contrato" (por ejemplo Olise o Fleetwood) | Chip gris. Es un dato, no un n.d. |
| No determinado | "n.d." | Chip gris |

**Qué se cuenta:** el contrato principal de calzado o indumentaria del atleta. Si están separados (por ejemplo Schauffele: ropa Descente, calzado Adidas), se usa la ropa y el calzado va en la nota.

## 5. Protocolo de búsqueda por atleta

1. Buscar "<atleta> <boot/shoe/apparel> sponsor <año>". En fútbol, priorizar Footy Headlines y SoccerBible; en tenis, Tennis.com, SI Serve y Racquet Social; en golf, Golf Monthly, MyGolfSpy y GolfWRX.
2. Si no aparece, hacer una segunda búsqueda con otra formulación ("<atleta> signs with", "<atleta> leaves").
3. Calificar la confianza:
   - **`v`:** fuente fechada dentro del año del corte o el anterior, que nombre explícitamente el contrato.
   - **`h`:** fuente de más de 2 años de antigüedad, inferencia de una fuente especializada (por ejemplo "usa botas X"), o conocimiento previo sin fuente.
   - **`n`:** nada tras 2 búsquedas. Registrar el número de búsquedas en `busquedas`.
4. **Usar las botas como evidencia con cuidado.** Que un atleta use una marca no prueba que tenga contrato. Caso Olise: usa Nike sin cobrar. Caso Judge: jugó con New Balance sin contrato.
5. **Si dos cortes muestran marcas distintas**, crear la fila en `movimientos.csv`.

## 6. Taxonomía de causas en movimientos

Usar solo una de estas causas, y únicamente si una fuente la reporta:

1. **Nike no renovó**
2. **El atleta eligió otra marca:** Nike quería retenerlo.
3. **Nike terminó el contrato:** ruptura anticipada.
4. **Contrato expiró, causa no pública**
5. **Movimiento interno de Nike Inc.:** por ejemplo Converse a Nike.
6. **Versiones encontradas:** se citan ambas fuentes.
7. **Causa no pública**

## 7. Reglas especiales

- **Promesa:** atleta con edad ≤ 23, calculada como año del corte menos año de nacimiento.
  - Se aplica solo a cortes y movimientos de 2023 a 2026.
  - Se marca con independencia de la marca.
  - La sección "Promesas 2023–2026 y su marca" lista a cada promesa una sola vez, con su marca del corte más reciente.
  - Los años de nacimiento deben verificarse (hoy salen de conocimiento previo).
- **Mención honorífica (MH):** atletas de influencia comercial que no están en el top del corte. No cuentan en el "x/N".
  - Hoy: Cristiano Ronaldo (fútbol); Michael Jordan y Stephen Curry (básquet); Djokovic (tenis).
- **Movimiento clave:** fila resaltada en el mercado de pases.
  - Hoy: Mbappé, Fritz, Yamal, Bonmatí, Kvaratskhelia, Neymar, Federer, Tiger Woods, Jokić, Curry, Harry Kane y Josh Allen.

## 8. Ancla financiera (FiscalAI primero)

- **Demand creation de NKE:** `company_financials_as_reported` con `statementType: "income-statement"`, `companyKey: "NYSE_NKE"` y `periodType: "annual"`.
  - Métricas: `Demand creation expense` y `Revenues`.
  - Guardar el `auditUrl` de cada valor como fuente.
- **Compromisos por endorsement:** no están en los datos estructurados.
  - Usar `company_filings` para encontrar el 10-K FY2026.
  - El dato está en MD&A ("Endorsement Contracts", dentro de material cash requirements), no en la Nota 16.
  - El PDF de FiscalAI tiene texto con fuentes CID; se lee con `filing_pdf` decodificando los ToUnicode (ver `finanzas.json`).
  - FiscalAI no da `auditUrl` para este texto: se enlaza el `sourceUrl` (SEC) de `company_filings`.
- **Nunca construir URLs de fiscal.ai a mano.** Usar solo `auditUrl` o el `terminalUrl` de `company_profile`.
- **Gráfico:** barras = demand creation en US$ mm (eje izquierdo); línea = % de ventas (eje derecho).

## 9. Pipeline de construcción

```
data/atletas.csv ─┐
data/movimientos.csv ─┼─> build.py (valida, calcula conteos, promesas, MH) ─> dist/nike-atletas-top.html
data/rankings.csv, nacimientos.csv, marcas.csv, mh.csv ─┤
data/finanzas.json (FiscalAI) ─┘
```

1. **`validate.py`:** valida la calidad de los datos. Debe fallar si:
   - Un `v` no tiene URL.
   - Un `n.d.` tiene menos de 2 búsquedas.
   - Un atleta aparece con marcas distintas en cortes consecutivos sin fila en `movimientos.csv`.
   - Una marca fuera de la lista principal no está mapeada en `data/marcas.csv`.
2. **`build.py`:** inyecta los datos como JSON en una plantilla HTML (`template.html`, a partir del artifact v3). No usa llamadas de red en runtime.
3. **`check.js`:** abre el HTML con jsdom, verifica que no haya errores de consola e imprime los conteos x/N por celda para revisarlos contra el texto de conclusiones.
4. **Conclusiones:** el texto vive en `data/conclusiones.html` y se reescribe después de cada actualización. Las cifras se escriben como `{{futbol.2024}}` y las calcula `build.py`, así que coinciden con la matriz por construcción.

## 10. Especificación del artifact

### Secciones (en orden)

1. **Encabezado:** titular con la conclusión, bajada y fecha de corte.
2. **Matriz:** deportes × cortes.
   - Cada celda muestra solo "x/N", con intensidad de azul según el % Nike.
   - Al tocar una celda se despliega la lista. En esa lista sí se muestran n.d., la confianza, el "?" de fuente y la etiqueta Promesa.
3. **Mercado de pases:** filtros Salidas / Llegadas y renovaciones / Entre rivales / Todos.
   - Filas clave resaltadas y etiqueta Promesa.
   - Nota sobre por qué hay pocas llegadas.
4. **Hombres, corte 2026:** paneles con el top 5 por deporte y las MH al final.
5. **Promesas 2023–2026 y su marca.**
6. **Mujeres, corte 2026.**
7. **Lo que Nike gasta en marketing:** gráfico y tabla con enlaces al 10-K.
8. **Qué dicen los datos:** conclusiones por deporte y tensiones abiertas.

No hay sección de metodología en el artifact.

### Diseño

- **Tipografía:** Barlow Condensed (titulares y cifras) y Source Sans 3 (texto), desde Google Fonts, con fallbacks.
- **Tokens claros:**

  | Token | Valor |
  |---|---|
  | Fondo | `#EEF2F5` |
  | Papel | `#FFFFFF` |
  | Tinta | `#0F1B2A` |
  | Atenuado | `#5A6878` |
  | Línea | `#D3DAE2` |
  | Nike | `#1D4ED8` |
  | Advertencia / Promesa | `#9A5B00` |

- **Modo oscuro:** tokens redefinidos bajo `prefers-color-scheme: dark` y `[data-theme="dark"]`.
- **Ancho:** los párrafos ocupan todo el ancho del contenedor (máximo 1080 px), sin `max-width` en `p`.
- **Fuentes:** ícono circular "?" enlazado, con `title` y `aria-label` que dicen el nombre de la fuente. Cada subtítulo de sección explica qué significa el "?".
- **Responsive:** las tablas anchas van dentro de un contenedor con `overflow-x: auto`. Las filas de los paneles no deben desbordarse: el chip y el "?" van en una columna que no hace salto de línea.
- **Accesibilidad:** foco visible, `aria-pressed` en celdas y filtros, textos alternativos en el gráfico.
- **Sin almacenamiento ni llamadas externas en runtime:** todo el dato va embebido.

## 11. Checklist de QA antes de entregar

- [ ] Los conteos x/N de la matriz coinciden con las cifras citadas en "Qué dicen los datos".
- [ ] La matriz no muestra n.d.
- [ ] Todo `v` tiene un "?" que abre una URL válida.
- [ ] Ningún panel se desborda a 380 px de ancho (revisar especialmente béisbol y golf, que tienen notas largas).
- [ ] Las promesas cumplen la regla de edad ≤ 23 y solo aparecen en cortes 2023–2026.
- [ ] Las MH no suman al total.
- [ ] Los movimientos clave están resaltados.
- [ ] Las contradicciones entre fuentes aparecen con ambas versiones.
- [ ] Las cifras financieras tienen el `auditUrl` de FiscalAI.

## 12. Mantenimiento

- **Tras la gala del Balón de Oro (26-oct-2026):** reemplazar el power ranking de GOAL por la clasificación oficial.
- **A fin de año:** actualizar los rankings ATP y OWGR de fin de temporada.
- **Cada 10-K de NKE (julio):** actualizar demand creation y los compromisos por endorsement.
- **Cada noticia de cambio de marca:** agregar una fila en `movimientos.csv`, actualizar `atletas.csv` y reconstruir.
