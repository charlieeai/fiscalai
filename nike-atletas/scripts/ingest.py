"""Incorpora un JSON de investigación a los CSV de data/.

Uso: python3 scripts/ingest.py archivo.json [archivo2.json ...]

Formato del JSON (ver REGLAS en el README): objeto con claves opcionales
"rankings", "atletas", "movimientos" y "nacimientos".
- atletas: upsert por (deporte, genero, corte, atleta). Si cambia el rank de otra fila, se reporta.
- rankings: upsert por (deporte, genero, corte).
- movimientos: se agrega si no existe la misma (atleta, de, a).
- nacimientos: se agrega si el atleta no está.
Después correr validate.py y build.py.
"""
import csv
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
NIKE_INC = {"Nike", "Jordan", "Converse"}


def read(name):
    with open(DATA / name, encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        return rd.fieldnames, list(rd)


def write(name, cols, rows):
    with open(DATA / name, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def s(v):
    return "" if v is None else str(v)


def main(paths):
    acols, atletas = read("atletas.csv")
    if "metodo" not in acols:
        acols.append("metodo")
    rcols, rankings = read("rankings.csv")
    mcols, movs = read("movimientos.csv")
    ncols, nac = read("nacimientos.csv")
    stats = {"atletas_nuevos": 0, "atletas_actualizados": 0, "rankings": 0, "movimientos": 0, "nacimientos": 0}

    for p in paths:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        for r in d.get("rankings", []):
            key = (r["deporte"], r["genero"], s(r["corte"]))
            row = {"deporte": key[0], "genero": key[1], "corte": key[2], "ranking": r.get("ranking", ""),
                   "fuente_nombre": r.get("fuente_nombre", ""), "fuente_url": r.get("fuente_url", "")}
            rankings = [x for x in rankings if (x["deporte"], x["genero"], x["corte"]) != key] + [row]
            stats["rankings"] += 1
        for a in d.get("atletas", []):
            marca = a["marca"]
            row = {"deporte": a["deporte"], "genero": a.get("genero", "M"), "corte": s(a["corte"]), "rank": s(a.get("rank")),
                   "atleta": a["atleta"], "marca": marca, "nike_inc": "1" if marca in NIKE_INC else "0",
                   "confianza": a["confianza"], "fuente_nombre": a.get("fuente_nombre") or "",
                   "fuente_url": a.get("fuente_url") or "", "nota": a.get("nota") or "",
                   "tipo_ranking": a.get("tipo_ranking", ""), "busquedas": s(a.get("busquedas")),
                   "metodo": a.get("metodo", "")}
            key = (row["deporte"], row["genero"], row["corte"], row["atleta"])
            old = next((x for x in atletas if (x["deporte"], x["genero"], x["corte"], x["atleta"]) == key), None)
            if old:
                row["tipo_ranking"] = row["tipo_ranking"] or old.get("tipo_ranking", "")
                old.update(row)
                stats["atletas_actualizados"] += 1
            else:
                if not row["tipo_ranking"]:
                    peer = next((x for x in atletas if x["deporte"] == row["deporte"] and x["genero"] == row["genero"]), None)
                    row["tipo_ranking"] = peer["tipo_ranking"] if peer else ""
                atletas.append(row)
                stats["atletas_nuevos"] += 1
        for m in d.get("movimientos", []):
            if any(x["atleta"] == m["atleta"] and x["de"] == m["de"] and x["a"] == m["a"] for x in movs):
                continue
            movs.append({c: s(m.get(c, "")) for c in mcols} | {"clave": s(m.get("clave", "0")) or "0"})
            stats["movimientos"] += 1
        for n in d.get("nacimientos", []):
            if any(x["atleta"] == n["atleta"] for x in nac):
                continue
            nac.append({"atleta": n["atleta"], "anio_nacimiento": s(n["anio_nacimiento"]),
                        "verificado": "1" if n.get("fuente_url") else "0", "fuente_url": n.get("fuente_url") or ""})
            stats["nacimientos"] += 1

    # Orden estable: deporte (orden de aparición), género, corte, rank.
    order = {k: i for i, k in enumerate(dict.fromkeys(x["deporte"] for x in atletas))}
    atletas.sort(key=lambda x: (x["genero"] != "M", order[x["deporte"]], int(x["corte"]),
                                int(x["rank"]) if x["rank"].isdigit() else 99))
    # Avisar si un corte quedó con ranks duplicados.
    seen = {}
    for x in atletas:
        k = (x["deporte"], x["genero"], x["corte"], x["rank"])
        if k in seen:
            print(f"AVISO: rank duplicado {k}: {seen[k]} y {x['atleta']}")
        seen[k] = x["atleta"]
    write("atletas.csv", acols, atletas)
    write("rankings.csv", rcols, rankings)
    write("movimientos.csv", mcols, movs)
    write("nacimientos.csv", ncols, nac)
    print(stats)


if __name__ == "__main__":
    main(sys.argv[1:])
