"""Marca la columna `clave` de movimientos.csv con la regla de 02-metodologia.md.

Uso: python3 scripts/clave.py   (build.py lo ejecuta antes de validar)

Un movimiento es clave si el atleta es relevante (está en algún top o MH del estudio,
o en ICONOS) y además:
- salida (out): cambia de grupo Nike Inc.;
- llegada o renovación (in): siempre;
- entre rivales: el destino es una marca principal o una marca propia del atleta.
EXTRA fija movimientos clave por decisión del usuario.
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ICONOS = {"Tiger Woods", "Kyrie Irving", "Allyson Felix", "Emma Raducanu", "Iga Swiatek", "Rodrygo"}
EXTRA = {("Stephen Curry", "2026")}


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    marcas = {r["marca"]: r["grupo"] for r in load("marcas.csv")}
    rel = {r["atleta"] for r in load("atletas.csv")} | {r["atleta"] for r in load("mh.csv")} | ICONOS
    movs = load("movimientos.csv")
    nike = lambda b: marcas.get(b) == "nike"
    for m in movs:
        if (m["atleta"], m["anio"]) in EXTRA:
            k = True
        elif m["atleta"] not in rel:
            k = False
        elif m["tipo"] == "out":
            k = nike(m["de"]) != nike(m["a"])
        elif m["tipo"] == "in":
            k = True
        else:
            k = marcas.get(m["a"]) == "principal" or "marca propia" in m["a"]
        m["clave"] = "1" if k else "0"
    with open(DATA / "movimientos.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(movs[0].keys()), quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(movs)
    print(f"clave: {sum(m['clave'] == '1' for m in movs)} de {len(movs)}")


if __name__ == "__main__":
    main()
