// Abre dist/nike-atletas-top.html con jsdom, verifica que no haya errores de consola,
// imprime los conteos x/N por celda y corre los chequeos automáticos del checklist de QA.
// Uso: node scripts/check.js
const fs = require("fs");
const path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");

const file = path.join(__dirname, "..", "dist", "nike-atletas-top.html");
const html = fs.readFileSync(file, "utf8");
const errors = [];
const vc = new VirtualConsole();
vc.on("error", (e) => errors.push(String(e)));
vc.on("jsdomError", (e) => errors.push(String(e.message || e)));

const dom = new JSDOM(html, { runScripts: "dangerously", virtualConsole: vc, pretendToBeVisual: true });
const doc = dom.window.document;
const D = dom.window.eval("DATA");
const fail = [];

// Conteos x/N por celda de la matriz.
console.log("Conteos x/N (matriz):");
const cells = [...doc.querySelectorAll("#matrix button.cell")];
for (const sp of D.sports) {
  const line = D.years.map((y) => {
    const b = cells.find((c) => c.dataset.k === sp.key && +c.dataset.y === y);
    return `${y}: ${b ? b.textContent.trim().padEnd(5) : "  —  "}`;
  });
  console.log(`  ${sp.label.padEnd(10)} ${line.join("  ")}`);
}
console.log("Mujeres 2026:");
doc.querySelectorAll("#women .panel h3").forEach((h) => console.log("  " + h.textContent.replace("Nike", " Nike")));

// QA: la matriz no muestra n.d.
if (/n\.d\.|n\/a/.test(doc.getElementById("matrix").textContent)) fail.push("La matriz muestra n.d.");
// QA: todo v tiene "?" con URL http.
const allRows = [...D.sports.flatMap((s) => Object.values(s.cuts).flatMap((c) => c.rows)), ...D.women.flatMap((w) => w.rows)];
allRows.filter((r) => r.c === "v" && !(r.s && /^https?:\/\//.test(r.s[1]))).forEach((r) => fail.push(`v sin URL: ${r.n}`));
// QA: cada celda se puede abrir sin errores.
for (const c of cells) c.click();
// QA: promesas cumplen edad <= 23 y años 2023-2026.
D.promesas.filter((p) => p.age > 23 || p.yr < 2023 || p.yr > 2026).forEach((p) => fail.push(`Promesa fuera de regla: ${p.n}`));
// QA: MH no suman (el panel de hombres cuenta solo filas numeradas).
doc.querySelectorAll("#men .panel").forEach((p) => {
  const [nk, n] = p.querySelector("h3 span").textContent.match(/\d+/g).map(Number);
  const numbered = p.querySelectorAll("li:not(.mh)").length;
  if (n !== numbered) fail.push(`MH cuentan en el total: ${p.querySelector("h3").textContent}`);
});
// QA: el mercado de pases muestra solo los movimientos clave.
doc.querySelector('.filters button[data-f="all"]').click();
const keyRows = doc.querySelectorAll("#ledger tbody tr").length;
const keyData = D.moves.filter((m) => m.clave).length;
if (keyRows !== keyData) fail.push(`Mercado de pases muestra ${keyRows} filas y hay ${keyData} movimientos clave`);
// QA: cifras financieras con auditUrl de FiscalAI.
D.fin.demand_creation.filter((f) => !/^https:\/\/fiscal\.ai\//.test(f.auditUrl)).forEach((f) => fail.push(`FY${f.fy} sin auditUrl`));
// QA: contradicción Mbappé con ambas versiones.
const mb = D.moves.find((m) => m.atleta === "Kylian Mbappé");
if (!(mb && /CNBC/.test(mb.causa) && /Irish Times/.test(mb.causa))) fail.push("Mbappé no muestra ambas versiones");
// QA: cifras de conclusiones coinciden con la matriz (build.py las genera de los mismos conteos).
const concl = doc.getElementById("r-title").parentElement.textContent;
if (/\{\{/.test(concl)) fail.push("Quedan cifras sin sustituir en conclusiones");
for (const sp of D.sports) for (const [y, c] of Object.entries(sp.cuts)) {
  const nk = c.rows.filter((r) => ["Nike", "Jordan", "Converse"].includes(r.b)).length;
  const b = cells.find((x) => x.dataset.k === sp.key && x.dataset.y === y);
  if (b.textContent.trim() !== `${nk}/${c.rows.length}`) fail.push(`Celda ${sp.key} ${y} no coincide`);
}

console.log(`\nMovimientos: ${D.moves.length} (clave: ${keyData}) | Promesas: ${D.promesas.length}`);
if (errors.length) { console.log("Errores de consola:"); errors.forEach((e) => console.log("  " + e)); }
if (fail.length) { console.log("Fallas de QA:"); fail.forEach((f) => console.log("  " + f)); }
if (errors.length || fail.length) process.exit(1);
console.log("Sin errores de consola. QA automático OK.");
