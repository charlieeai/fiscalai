"""Consolida JSON de investigación de promesas en data/promesas.csv.

Uso: python3 scripts/promesas_json_a_csv.py archivo1.json [archivo2.json ...]
Si un atleta aparece en varios archivos, gana el último. Deja fuera a los nacidos antes de 2003.
"""
import csv
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "promesas.csv"
COLS = ["deporte", "genero", "criterio", "criterio_url", "atleta", "anio_nacimiento", "nacimiento_url",
        "marca", "confianza", "fuente_nombre", "fuente_url", "nota", "busquedas"]

rows = {}
for p in sys.argv[1:]:
    for a in json.loads(Path(p).read_text(encoding="utf-8")):
        if int(a["anio_nacimiento"]) < 2003:
            continue
        rows[a["atleta"]] = {c: "" if a.get(c) is None else str(a.get(c)) for c in COLS}
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL, lineterminator="\n")
    w.writeheader()
    w.writerows(sorted(rows.values(), key=lambda r: (r["deporte"], r["atleta"])))
print(f"{len(rows)} promesas en {OUT.name}")
