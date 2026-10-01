"""Valida la calidad de los datos del estudio. Sale con código 1 si hay errores.

Reglas (02-metodologia.md, sección 9):
  1. Un dato `v` sin URL.
  2. Un `n.d.` con menos de 2 búsquedas registradas.
  3. Un atleta con marcas distintas en cortes consecutivos sin fila en movimientos.csv.
  4. Una marca que no está mapeada en marcas.csv.
"""
import csv
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
NIKE_INC = {"Nike", "Jordan", "Converse"}


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    errors, warnings = [], []
    atletas = load("atletas.csv")
    movs = load("movimientos.csv")
    marcas = {r["marca"] for r in load("marcas.csv")}
    mh = load("mh.csv")
    nac = load("nacimientos.csv")

    def where(r):
        return f'{r["deporte"]} {r["corte"]} #{r["rank"]} {r["atleta"]}'

    for r in atletas:
        if r["confianza"] not in ("v", "h", "n"):
            errors.append(f"Confianza inválida: {where(r)} = {r['confianza']!r}")
        if r["confianza"] == "v" and not r["fuente_url"].startswith("http"):
            errors.append(f"Dato v sin URL: {where(r)}")
        if r["marca"] == "n.d.":
            b = int(r["busquedas"] or 0)
            if b < 2:
                errors.append(f"n.d. con {b} búsquedas (mínimo 2): {where(r)}")
        if r["marca"] not in marcas:
            errors.append(f"Marca sin mapear en marcas.csv: {r['marca']!r} ({where(r)})")
        expected = "1" if r["marca"] in NIKE_INC else "0"
        if r["nike_inc"] != expected:
            errors.append(f"nike_inc no coincide con la marca: {where(r)}")

    for m in movs:
        tag = f'{m["anio"]} {m["atleta"]} {m["de"]}→{m["a"]}'
        if m["tipo"] not in ("out", "in", "rival"):
            errors.append(f"Tipo de movimiento inválido: {tag}")
        if m["confianza"] == "v" and "http" not in m["fuentes_url"]:
            errors.append(f"Movimiento v sin URL: {tag}")
        for b in (m["de"], m["a"]):
            if b not in marcas:
                errors.append(f"Marca sin mapear en marcas.csv: {b!r} (movimiento {tag})")

    for r in mh:
        if r["marca"] not in marcas:
            errors.append(f"Marca sin mapear en marcas.csv: {r['marca']!r} (MH {r['atleta']})")
        if r["confianza"] == "v" and not r["fuente_url"].startswith("http"):
            errors.append(f"MH v sin URL: {r['atleta']}")

    # Regla 3: cambios de marca entre cortes consecutivos del mismo atleta.
    by_athlete = {}
    for r in atletas:
        if r["marca"] in ("n.d.",):
            continue
        by_athlete.setdefault((r["genero"], r["atleta"]), []).append(r)
    for (_, name), rs in by_athlete.items():
        rs.sort(key=lambda r: int(r["corte"]))
        for prev, cur in zip(rs, rs[1:]):
            if prev["marca"] == cur["marca"]:
                continue
            ok = any(
                m["atleta"] == name and (m["de"] == prev["marca"] or m["a"] == cur["marca"])
                for m in movs
            )
            if not ok:
                errors.append(
                    f"Cambio sin movimiento: {name} {prev['corte']} {prev['marca']} → {cur['corte']} {cur['marca']}"
                )

    for r in nac:
        if r["verificado"] == "0":
            warnings.append(f"Año de nacimiento sin fuente: {r['atleta']} ({r['anio_nacimiento']})")

    fin = json.loads((DATA / "finanzas.json").read_text(encoding="utf-8"))
    for f in fin["demand_creation"]:
        if "fiscal.ai" not in f.get("auditUrl", ""):
            errors.append(f"Demand creation FY{f['fy']} sin auditUrl de FiscalAI")

    h = sum(r["confianza"] == "h" for r in atletas)
    nd = sum(r["marca"] == "n.d." for r in atletas)
    print(f"atletas.csv: {len(atletas)} filas | h: {h} | n.d.: {nd}")
    print(f"movimientos.csv: {len(movs)} filas")
    for w in warnings:
        print("AVISO:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        print(f"{len(errors)} errores")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
