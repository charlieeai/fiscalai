// Usage: NODE_PATH=/opt/node22/lib/node_modules node audit.js file.html [shotsDir]
// Reports per chart: marks (bars/dots/stack segments), value labels, label collisions; JS errors; undefined/NaN in text.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = path.resolve(process.argv[2]);
  const shots = process.argv[3];
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message || e)));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForTimeout(600);
  const res = await page.evaluate(() => {
    function ov(a, b) { return Math.min(a.right, b.right) - Math.max(a.left, b.left) > 0.5 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 0.5; }
    const out = [];
    document.querySelectorAll('svg.chart-svg').forEach((svg, k) => {
      const host = svg.closest('[id]');
      const id = host ? host.id : ('svg' + k);
      const marks = svg.querySelectorAll('rect[class*="bar-"], circle[class*="dot-"], rect.stack, rect[data-stack]').length;
      const labels = Array.from(svg.querySelectorAll('text.value-label'));
      const boxes = labels.map(t => t.getBoundingClientRect());
      const axis = Array.from(svg.querySelectorAll('text.axis-label')).map(t => t.getBoundingClientRect());
      let coll = 0;
      for (let i = 0; i < boxes.length; i++) {
        for (let j = i + 1; j < boxes.length; j++) if (ov(boxes[i], boxes[j])) coll++;
        for (const a of axis) if (ov(boxes[i], a)) coll++;
      }
      out.push({ id, marks, labels: labels.length, collisions: coll, partial: svg.getAttribute('data-partial-labels') === '1' });
    });
    const txt = document.body.innerText;
    const bad = (txt.match(/\bundefined\b|\bNaN\b|Infinity/g) || []).length;
    const tables = document.querySelectorAll('table').length;
    const emptyTables = Array.from(document.querySelectorAll('table')).filter(t => t.querySelectorAll('td').length === 0).length;
    return { charts: out, bad, tables, emptyTables, title: document.title };
  });
  console.log('FILE', file, '|', res.title);
  console.log('JS errors:', errors.length ? errors.join(' || ') : 'none');
  console.log('undefined/NaN/Infinity in text:', res.bad, '| tables:', res.tables, 'empty tables:', res.emptyTables);
  let fails = 0;
  for (const c of res.charts) {
    const okLab = c.partial || c.marks === c.labels;
    const ok = okLab && c.collisions === 0;
    if (!ok) fails++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} ${c.id}: marks=${c.marks} labels=${c.labels}${c.partial ? ' (partial-labels)' : ''} collisions=${c.collisions}`);
  }
  console.log(`charts=${res.charts.length} failing=${fails}`);
  if (shots) {
    const fs = require('fs'); fs.mkdirSync(shots, { recursive: true });
    const cards = await page.$$('.chart-card');
    for (let i = 0; i < cards.length; i++) await cards[i].screenshot({ path: path.join(shots, `card-${String(i).padStart(2, '0')}.png`) });
    await page.screenshot({ path: path.join(shots, 'full.png'), fullPage: true });
    console.log('screenshots ->', shots);
  }
  await browser.close();
})();
