// Usage: node check-q-report.mjs path/to/q-report.html
// Renders the narrative Q-Report at desktop (light) and phone (dark) width, checks JS errors and
// horizontal overflow, clicks "Download PDF" with a stub of the artifact downloads capability and
// reports the PDF file name and size. Needs Playwright.
import { readFileSync, writeFileSync, mkdtempSync } from "fs";
import { tmpdir } from "os";
import { join, resolve } from "path";
let chromium;
try { ({ chromium } = await import("playwright")); }
catch { ({ chromium } = await import("/opt/node22/lib/node_modules/playwright/index.mjs")); }
const src = resolve(process.argv[2] ?? "");
const body = readFileSync(src, "utf8");
const dir = mkdtempSync(join(tmpdir(), "qreport-"));
const wrapped = join(dir, "wrapped.html");
// Artifact pages are published without a document skeleton; wrap it the way the viewer does.
writeFileSync(wrapped, body.trimStart().toLowerCase().startsWith("<!doctype") ? body :
  `<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>${body}</body></html>`);
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
let failed = false;
for (const [w, scheme, name] of [[1200, "light", "desktop-light"], [390, "dark", "phone-dark"]]) {
  const page = await browser.newPage({ ignoreHTTPSErrors: true, viewport: { width: w, height: 900 }, colorScheme: scheme });
  const errs = []; page.on("pageerror", e => errs.push(e.message));
  await page.addInitScript(() => { window.__saved = null; window.claude = { use: async (n) => n === "downloads" ? { save: async (r) => { window.__saved = { name: r.filename, size: r.data.size }; return { status: "saved" }; } } : null }; });
  await page.goto("file://" + wrapped, { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  const visible = await page.isVisible("#pdf-btn");
  if (visible) { await page.click("#pdf-btn"); await page.waitForTimeout(1500); }
  const saved = await page.evaluate(() => window.__saved);
  const words = await page.evaluate(() => (document.querySelector("#essay")?.innerText.match(/\S+/g) || []).length);
  const recs = await page.evaluate(() => (document.querySelector("#essay")?.innerText.match(/\b(we recommend|I recommend|I suggest|suggest holding|buy rating|sell rating)\b/gi) || []));
  if (errs.length || overflow || !visible || !saved || recs.length) failed = true;
  console.log(name, JSON.stringify({ errs, overflow, pdfButton: visible, saved, words, recommendationPhrases: recs }));
}
await browser.close();
console.log(failed ? "RESULT: FAIL" : "RESULT: OK");
process.exit(failed ? 1 : 0);
