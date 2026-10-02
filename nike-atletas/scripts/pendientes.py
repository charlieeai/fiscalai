"""Genera hipotesis-pendientes.md: filas con confianza h y n.d., agrupadas por deporte.

Uso: python3 scripts/pendientes.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "data" / "atletas.csv", encoding="utf-8")))
NIKE = {"Nike", "Jordan", "Converse"}
h = [r for r in rows if r["confianza"] == "h"]
nd = [r for r in rows if r["marca"] == "n.d."]

out = ["# Hipótesis y n.d. pendientes", "",
       f"{len(h)} filas en hipótesis (h) y {len(nd)} sin marca (n.d.), de {len(rows)}. "
       "Las filas Nike van primero porque mueven el conteo. Para confirmar una, basta indicar atleta, corte y marca.", ""]
for title, sel in (("Hipótesis (h)", h), ("Sin marca (n.d.)", nd)):
    out += [f"## {title}", ""]
    deps = list(dict.fromkeys(r["deporte"] + (" (F)" if r["genero"] == "F" else "") for r in sel))
    for d in deps:
        rs = [r for r in sel if r["deporte"] + (" (F)" if r["genero"] == "F" else "") == d]
        rs.sort(key=lambda r: (r["marca"] not in NIKE, r["atleta"], r["corte"]))
        out += [f"### {d} ({len(rs)})", "", "| Atleta | Corte | Marca | Motivo |", "|---|---|---|---|"]
        out += [f"| {r['atleta']} | {r['corte']} | {r['marca']} | {r['nota'].replace('|', '/')} |" for r in rs]
        out.append("")
(ROOT / "hipotesis-pendientes.md").write_text("\n".join(out), encoding="utf-8")
print(f"h={len(h)} nd={len(nd)}")
