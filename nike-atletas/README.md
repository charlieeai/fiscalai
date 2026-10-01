# Estudio Nike: atletas top y mercado de pases (2015–2026)

Los CSV de `data/` son la fuente única de verdad. El HTML se genera desde ellos y no se edita a mano.

```
npm install            # solo para check.js (jsdom)
python3 scripts/validate.py
python3 scripts/build.py --fecha "1 de octubre de 2026"
node scripts/check.js
```

`build.py` corre `validate.py` primero y se detiene si falla. La salida queda en `dist/nike-atletas-top.html`, y los conteos por celda en `dist/conteos.json`.

## Archivos

| Archivo | Contenido |
|---|---|
| `data/atletas.csv` | Una fila por atleta, deporte y corte. Agrega la columna `busquedas`. |
| `data/movimientos.csv` | Una fila por cambio de marca. |
| `data/nacimientos.csv` | Año de nacimiento, fuente y `verificado` (0 = de memoria). Se usa para la etiqueta Promesa. |
| `data/rankings.csv` | Fuente del ranking de cada corte (reemplaza a `fuentes.csv` del plan). |
| `data/deportes.csv` | Orden y etiqueta de cada deporte en la matriz. |
| `data/mh.csv` | Menciones honoríficas del corte 2026 (no cuentan en el total). |
| `data/marcas.csv` | Mapeo de marcas a grupo (nike, principal, otro, sin, nd). Toda marca nueva debe agregarse aquí. |
| `data/finanzas.json` | Demand creation (FiscalAI, con `auditUrl`) y compromisos por endorsement del 10-K. |
| `data/conclusiones.html` | Texto de "Qué dicen los datos". Las cifras van como `{{futbol.2024}}` y las calcula `build.py`. |
| `scripts/template.html` | Plantilla del artifact (estilos de v3). |
| `v3-original.html` | Artifact v3 de partida, como referencia. |
| `01-brief-y-backlog.md`, `02-metodologia.md` | Brief, backlog y metodología. |

## Cifras disponibles en conclusiones

- `{{deporte.corte}}` → "x/N" (por ejemplo `{{basquet.2026}}`; en mujeres, la etiqueta del panel: `{{Fútbol.2026}}`).
- `{{nk:deporte.corte}}` → atletas Nike; `{{v:deporte.corte}}` → atletas Nike verificados.
- `{{prom:total}}`, `{{prom:nike}}`, `{{prom:adidas}}`, `{{prom:on}}`, `{{promlist:nike}}`.
