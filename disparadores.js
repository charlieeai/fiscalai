// Lógica de disparadores. Pura: recibe datos y configuración, devuelve evaluación.
const MULTS = [
  { id: "ratio_ev_to_sales", label: "EV/Sales", fmt: "x", cheapLow: true, max: 60 },
  { id: "ratio_ev_to_ebitda", label: "EV/EBITDA", fmt: "x", cheapLow: true, max: 100 },
  { id: "ratio_price_to_earnings", label: "P/E", fmt: "x", cheapLow: true, max: 200 },
  { id: "ratio_price_to_book", label: "P/B", fmt: "x", cheapLow: true, max: 100 },
  { id: "ratio_fcf_yield", label: "FCF yield", fmt: "%", cheapLow: false }
];
const MARGINS = [
  { id: "ratio_gross_profit_margin", label: "Margen bruto" },
  { id: "ratio_operating_margin", label: "Margen EBIT" },
  { id: "ratio_ebitda_margin", label: "Margen EBITDA" },
  { id: "ratio_net_profit_margin", label: "Margen neto" },
  { id: "ratio_fcf_margin", label: "FCF margin" }
];
const DEFAULT_CFG = {
  dropMtd: -10, drop6m: -20, dropYtd: -25,   // % de caída que activa
  cheapPct: 20,                              // percentil 5 años que cuenta como barato
  marginTol: 1.0,                            // pp por debajo de la mediana tolerados
  leverTol: 0.5,                             // veces de deuda neta/EBITDA sobre la mediana toleradas
  peerWeight: 30,                            // % del puntaje de valuación que viene de pares
  wVal: 45, wQual: 35, wDrop: 20,            // pesos del puntaje total
  cheapScore: 65, qualOk: 70, qualBad: 50
};

function validMult(m, v) {
  if (v == null || !isFinite(v)) return false;
  if (m.cheapLow) return v > 0 && v < m.max;
  return true;
}
function median(a) {
  const s = a.filter(v => v != null && isFinite(v)).sort((x, y) => x - y);
  if (!s.length) return null;
  const k = Math.floor(s.length / 2);
  return s.length % 2 ? s[k] : (s[k - 1] + s[k]) / 2;
}
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

function evaluate(o, cfg, threshold) {
  const r = { key: o.key, mult: [], marg: [], notes: [] };
  // Precio
  const drops = [
    { k: "MTD", v: o.ret.mtd, t: cfg.dropMtd / 100 },
    { k: "6M", v: o.ret.m6, t: cfg.drop6m / 100 },
    { k: "YTD", v: o.ret.ytd, t: cfg.dropYtd / 100 }
  ];
  r.dropHits = drops.filter(d => d.v != null && d.v <= d.t).map(d => d.k);
  r.dropped = r.dropHits.length > 0;
  r.dropScore = Math.round(100 * Math.max(0, ...drops.map(d => d.v != null && d.v < 0 ? clamp(d.v / d.t, 0, 1) : 0)));
  r.threshold = threshold;
  r.inRange = threshold != null && threshold > 0 && o.price <= threshold;
  r.distToThreshold = threshold ? o.price / threshold - 1 : null;

  // Múltiplos vs historia y pares
  const histScores = [], peerScores = [];
  for (const m of MULTS) {
    const x = o.mult[m.id];
    const row = { ...m, cur: null, med: null, pct: null, peerMed: null, peerDiff: null, ns: false, cheap: false };
    if (!x || x.err) { row.ns = true; r.mult.push(row); continue; }
    row.cur = x.cur; row.med = x.med; row.pct = x.pct; row.min = x.min; row.max5 = x.max; row.s = x.s; row.m6 = x.m6;
    const okNow = validMult(m, x.cur), okMed = validMult(m, x.med);
    if (!okNow || !okMed) { row.ns = true; }
    const peerVals = (o.peers || []).map(p => p.m && p.m[m.id]).filter(v => validMult(m, v));
    row.peerMed = peerVals.length >= 2 ? median(peerVals) : null;
    row.peerN = peerVals.length;
    if (!row.ns) {
      const histCheap = m.cheapLow ? 100 - x.pct : x.pct;
      histScores.push(histCheap);
      row.cheap = m.cheapLow ? x.pct <= cfg.cheapPct : x.pct >= 100 - cfg.cheapPct;
      if (row.peerMed != null) {
        row.peerDiff = x.cur / row.peerMed - 1;
        const d = m.cheapLow ? -row.peerDiff : row.peerDiff;   // positivo = más barata que pares
        peerScores.push(clamp(50 + d * 100, 0, 100));
      }
    }
    r.mult.push(row);
  }
  const hs = histScores.length ? histScores.reduce((a, b) => a + b, 0) / histScores.length : null;
  const ps = peerScores.length ? peerScores.reduce((a, b) => a + b, 0) / peerScores.length : null;
  const pw = cfg.peerWeight / 100;
  r.valScore = hs == null ? null : Math.round(ps == null ? hs : hs * (1 - pw) + ps * pw);
  r.cheapCount = r.mult.filter(m => m.cheap).length;

  // Calidad: márgenes LTM vs mediana 5 años fiscales, y apalancamiento
  let ok = 0, n = 0;
  for (const m of MARGINS) {
    const f = o.fund && o.fund[m.id];
    const row = { ...m, ltm: f ? f.ltm : null, med: f ? f.med : null, h: f ? f.h : [], delta: null, ok: null };
    if (f && f.ltm != null && f.med != null && !(f.ltm === 0 && f.med === 0)) {
      row.delta = (f.ltm - f.med) * 100;
      row.ok = row.delta >= -cfg.marginTol;
      n++; if (row.ok) ok++;
    }
    r.marg.push(row);
  }
  const nd = o.fund && o.fund.ratio_net_debt_to_ebitda;
  const ndAbs = o.fund && o.fund.calculated_net_debt;
  const ebitdaPos = o.fund && o.fund.ratio_ebitda_margin && o.fund.ratio_ebitda_margin.ltm > 0;
  r.lever = { ltm: nd ? nd.ltm : null, med: nd ? nd.med : null, h: nd ? nd.h : [], netDebt: ndAbs ? ndAbs.ltm : null, netDebtMed: ndAbs ? ndAbs.med : null, netDebtH: ndAbs ? ndAbs.h : [], ok: null, ns: false };
  if (!ebitdaPos || (nd && Math.abs(nd.ltm) > 50)) { r.lever.ns = true; }
  else if (nd && nd.ltm != null && nd.med != null) {
    r.lever.ok = nd.ltm <= 1 || nd.ltm <= nd.med + cfg.leverTol;
    n++; if (r.lever.ok) ok++;
  }
  r.qualScore = n ? Math.round(100 * ok / n) : null;
  r.qualN = n; r.qualOkN = ok;

  // Clasificación
  const cheap = r.valScore != null && r.valScore >= cfg.cheapScore;
  const ebitM = o.fund && o.fund.ratio_operating_margin ? o.fund.ratio_operating_margin.ltm : null;
  r.unprofitable = ebitM != null && ebitM <= 0;
  if (r.unprofitable) r.notes.push("Margen EBIT de los últimos doce meses negativo: la calidad no se valida aunque los márgenes mejoren.");
  const qGood = !r.unprofitable && r.qualScore != null && r.qualScore >= cfg.qualOk;
  const qBad = r.qualScore != null && r.qualScore < cfg.qualBad;
  if (r.dropped && cheap && qGood) r.signal = "div";
  else if (r.dropped && qBad) r.signal = "trap";
  else if (r.dropped) r.signal = "watch";
  else if (cheap && qGood) r.signal = "cheap";
  else r.signal = "none";

  const W = cfg.wVal + cfg.wQual + cfg.wDrop || 1;
  r.score = Math.round(((r.valScore ?? 0) * cfg.wVal + (r.unprofitable ? 0 : (r.qualScore ?? 0)) * cfg.wQual + r.dropScore * cfg.wDrop) / W);

  // Descomposición 6M: precio = EPS implícito × P/E
  const pe = o.mult.ratio_price_to_earnings;
  if (pe && pe.cur > 0 && pe.m6 > 0 && pe.cur < 60 && pe.m6 < 60 && o.ret.m6 != null) {
    const mChg = pe.cur / pe.m6 - 1;
    const eChg = (1 + o.ret.m6) / (1 + mChg) - 1;
    r.decomp = { basis: "P/E", ret: o.ret.m6, mult: mChg, fund: eChg, from: pe.m6, to: pe.cur };
  } else {
    const ev = o.mult.ratio_ev_to_sales;
    if (ev && ev.cur > 0 && ev.m6 > 0 && o.ret.m6 != null) {
      const mChg = ev.cur / ev.m6 - 1;
      r.decomp = { basis: "EV/Sales", ret: o.ret.m6, mult: mChg, fund: (1 + o.ret.m6) / (1 + mChg) - 1, from: ev.m6, to: ev.cur, approx: true };
    } else r.decomp = null;
  }
  return r;
}
if (typeof module !== "undefined") module.exports = { evaluate, DEFAULT_CFG, MULTS, MARGINS };
