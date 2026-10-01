"""Genera dist/nike-atletas-top.html desde los CSV de data/.

Uso: python3 scripts/build.py [--fecha "1 de octubre de 2026"]

Pasos: corre validate.py, arma el JSON de datos, calcula conteos y promesas,
sustituye las cifras {{...}} en data/conclusiones.html y escribe el HTML.
Las cifras de las conclusiones salen de los mismos conteos que muestra la matriz.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "dist"
NIKE_INC = {"Nike", "Jordan", "Converse"}
YEARS = [2015, 2018, 2021, 2024, 2026]

# Nombre legible para URLs de movimientos (que solo guardan la URL).
SITE_NAMES = {
    "cnbc.com": "CNBC", "irishtimes.com": "The Irish Times", "onefootball.com": "OneFootball",
    "sponsorunited.com": "SponsorUnited", "tennisavid.com": "TennisAvid", "racquetsocial.com": "Racquet Social",
    "sports.yahoo.com": "Yahoo Sports", "si.com": "Sports Illustrated", "footyheadlines.com": "Footy Headlines",
    "sportbible.com": "SPORTbible", "golfmonthly.com": "Golf Monthly", "kicksologists.com": "Kicksologists",
    "bleacherreport.com": "Bleacher Report", "cbssports.com": "CBS Sports", "hypebeast.com": "Hypebeast",
    "wikipedia.org": "Wikipedia", "puntodebreak.com": "Punto de Break", "cricexec.com": "CricExec",
    "sportico.com": "Sportico", "fashionnetwork.com": "FashionNetwork", "thetennisinsider.com": "The Tennis Insider",
    "x.com": "X (Twitter)", "tennisnow.com": "Tennis Now", "forbes.com": "Forbes", "espn.com": "ESPN",
    "thehill.com": "The Hill", "money.cnn.com": "CNN Money", "sportbusiness.com": "SportBusiness",
    "tennisnet.com": "tennisnet", "fashionunited.com": "FashionUnited", "about.puma.com": "Puma Newsroom",
    "elgoldigital.com": "El Gol Digital", "womenstennisblog.com": "Women's Tennis Blog", "10sballs.com": "10sBalls",
}


def site_name(url):
    host = urlparse(url).netloc.lower().removeprefix("www.").removeprefix("ww.")
    for k, v in SITE_NAMES.items():
        if host == k or host.endswith("." + k):
            return v
    return host


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def row(r):
    out = {"n": r["atleta"], "b": r["marca"], "c": r["confianza"]}
    if r.get("fuente_url"):
        out["s"] = [r.get("fuente_nombre") or site_name(r["fuente_url"]), r["fuente_url"]]
    if r.get("nota"):
        out["note"] = r["nota"]
    if r.get("rank") and r["rank"].isdigit():
        out["rank"] = int(r["rank"])
    return out


def build_data():
    atletas = load("atletas.csv")
    deportes = sorted(load("deportes.csv"), key=lambda r: int(r["orden"]))
    rankings = {(r["deporte"], r["genero"], r["corte"]): r for r in load("rankings.csv")}
    brands = {r["marca"]: {"g": r["grupo"], "c": r["color"]} for r in load("marcas.csv")}
    born = {r["atleta"]: {"y": int(r["anio_nacimiento"]), "v": r["verificado"] == "1", "u": r["fuente_url"]}
            for r in load("nacimientos.csv")}

    def rk_src(dep, gen, corte):
        k = rankings.get((dep, gen, str(corte)))
        return [k["fuente_nombre"], k["fuente_url"]] if k else None

    sports = []
    for d in deportes:
        cuts = {}
        for y in YEARS:
            rows = [r for r in atletas if r["deporte"] == d["clave"] and r["genero"] == "M" and r["corte"] == str(y)]
            if rows:
                rows.sort(key=lambda r: int(r["rank"]))
                cuts[y] = {"rows": [row(r) for r in rows], "src": rk_src(d["clave"], "M", y)}
        sports.append({"key": d["clave"], "label": d["etiqueta"], "sub": d["ranking"], "cuts": cuts})

    women = []
    for dep in dict.fromkeys(r["deporte"] for r in atletas if r["genero"] == "F"):
        rows = sorted((r for r in atletas if r["genero"] == "F" and r["deporte"] == dep), key=lambda r: int(r["rank"]))
        w = {"label": dep, "rows": [row(r) for r in rows], "src": rk_src(dep, "F", 2026)}
        if dep == "Tenis (WTA)":
            w["note"] = "Iga Swiatek (nº 9) está con On."
        women.append(w)

    mh = {}
    for r in load("mh.csv"):
        mh.setdefault(r["deporte"], []).append(row(r))

    moves = []
    for m in load("movimientos.csv"):
        urls = [u.strip() for u in m["fuentes_url"].split("|") if u.strip()]
        moves.append({"anio": m["anio"], "atleta": m["atleta"], "deporte": m["deporte"], "de": m["de"], "a": m["a"],
                      "tipo": m["tipo"], "causa": m["causa"], "conf": m["confianza"],
                      "srcs": [[site_name(u), u] for u in urls], "clave": int(m["clave"] or 0)})

    # Promesas: edad <= 23 en cortes y movimientos 2023-2026; marca del registro más reciente.
    prom = {}

    def reg(name, brand, yr):
        b = born.get(name)
        if not b or not (2023 <= yr <= 2026) or yr - b["y"] > 23:
            return
        if name not in prom or yr > prom[name]["yr"]:
            prom[name] = {"n": name, "b": brand, "yr": yr, "age": yr - b["y"], "verified": b["v"],
                          "s": ["Año de nacimiento", b["u"]] if b["u"] else None}

    for sp in sports:
        for y, c in sp["cuts"].items():
            for r in c["rows"]:
                reg(r["n"], r["b"], y)
    for w in women:
        for r in w["rows"]:
            reg(r["n"], r["b"], 2026)
    for m in moves:
        reg(m["atleta"], m["a"], int(m["anio"][:4]))
    promesas = sorted(prom.values(), key=lambda p: (p["age"], p["n"]))

    fin = json.loads((DATA / "finanzas.json").read_text(encoding="utf-8"))
    return {"years": YEARS, "sports": sports, "women": women, "mh": mh, "moves": moves,
            "born": {k: {"y": v["y"]} for k, v in born.items()}, "promesas": promesas,
            "brands": brands, "fin": {"demand_creation": fin["demand_creation"], "endorsement": fin["endorsement"]}}


def counts(data):
    """Conteos por celda: {'futbol.2024': (nk, N, nk_verificados)}; mujeres con su etiqueta."""
    out = {}
    for sp in data["sports"]:
        for y, c in sp["cuts"].items():
            rs = c["rows"]
            out[f"{sp['key']}.{y}"] = (sum(r["b"] in NIKE_INC for r in rs), len(rs),
                                       sum(r["b"] in NIKE_INC and r["c"] == "v" for r in rs))
    for w in data["women"]:
        rs = w["rows"]
        out[f"{w['label']}.2026"] = (sum(r["b"] in NIKE_INC for r in rs), len(rs),
                                     sum(r["b"] in NIKE_INC and r["c"] == "v" for r in rs))
    return out


def prom_groups(data):
    g = {}
    for p in data["promesas"]:
        grp = data["brands"].get(p["b"], {"g": "otro"})["g"]
        key = "nike" if grp == "nike" else p["b"].lower() if grp == "principal" else grp
        g.setdefault(key, []).append(p["n"])
    return g


def fill(text, data):
    cnt = counts(data)
    pg = prom_groups(data)

    def rep(m):
        tok = m.group(1)
        if tok.startswith("v:"):
            return str(cnt[tok[2:]][2])
        if tok.startswith("nk:"):
            return str(cnt[tok[3:]][0])
        if tok == "prom:total":
            return str(len(data["promesas"]))
        if tok.startswith("prom:"):
            return str(len(pg.get(tok[5:], [])))
        if tok.startswith("promlist:"):
            names = pg.get(tok[9:], [])
            return ", ".join(names[:-1]) + (" y " if len(names) > 1 else "") + (names[-1] if names else "")
        nk, n, _ = cnt[tok]
        return f"{nk}/{n}"

    try:
        return re.sub(r"\{\{([^}]+)\}\}", rep, text)
    except KeyError as e:
        sys.exit(f"Cifra desconocida en conclusiones: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default="1 de octubre de 2026")
    args = ap.parse_args()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")], check=True)
    data = build_data()
    concl = fill((DATA / "conclusiones.html").read_text(encoding="utf-8"), data)
    html = (ROOT / "scripts" / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (html.replace("/*__DATA__*/", payload)
                .replace("<!--__CONCLUSIONES__-->", concl)
                .replace("__FECHA__", args.fecha))
    DIST.mkdir(exist_ok=True)
    out = DIST / "nike-atletas-top.html"
    out.write_text(html, encoding="utf-8")
    (DIST / "conteos.json").write_text(json.dumps(
        {k: {"nike": v[0], "total": v[1], "nike_verificados": v[2]} for k, v in counts(data).items()},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Escrito {out.relative_to(ROOT)} ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
