import sys
p=sys.argv[1]; s=open(p).read()
def r(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt,(n,a[:80])
    s=s.replace(a,b)
r('<title>Reporte Q — CTT Correios de Portugal (CTT)</title>','<title>CTT Q-Report Charts 2Q26</title>')
r('''  <h1>Reporte Q — CTT Correios de Portugal (CTT)</h1>
  <div style="margin-bottom:20px;"></div>''','''  <h1>CTT Q-Report Charts — 2Q26</h1>
  <div class="sub">CTT Correios de Portugal (CTT) · data annex to the CTT Q-Report 2Q26 · updated 21 Oct 2026 · price €5.86, as in the Q-Report</div>''')
r('''<div class="exec-tile"><div class="label">Buyback</div><div class="value ">€40M program</div><div class="detail">shares 132.6M → 130.3M · ramped &lt;€6</div></div>''','''<div class="exec-tile"><div class="label">Buyback</div><div class="value ">€40M program</div><div class="detail">raised from €30M · 4.1M shares for €25.1M by 30 Sep (avg €6.12)</div></div>''')
r('''<div class="exec-tile"><div class="label">Banco CTT</div><div class="value good">NBO received</div><div class="detail">unsolicited offer (Cajamar) — sale process moving</div></div>''','''<div class="exec-tile"><div class="label">Banco CTT</div><div class="value bad">Approach ended</div><div class="detail">Cajamar's non-binding approach (21 Jul) ended without agreement on 4 Sep</div></div>''')
r('''the buyback was topped up (+€10M) and ramped below €6, and — the real catalyst — Banco CTT received an unsolicited offer, moving the long-awaited bank sale forward.''','''the buyback was topped up (+€10M) and ramped below €6, and Banco CTT received an unsolicited, non-binding approach (Grupo Cajamar, 21 Jul). <strong>Update:</strong> those talks ended without agreement on 4 Sep (ECO) and no price was published; a sale now needs a new buyer and a new process.''')
# valuation section
r('<h2 class="section">Valuation — EV/EBITDA (bear / base / bull)</h2>','<h2 class="section">Valuation — bear / base / bull</h2>')
i=s.index('    <p class="note" style="margin:0 0 8px;">Valued on a whole-company')
j=s.index('</p>',i)+4
s=s[:i]+'''    <p class="note" style="margin:0 0 8px;"><strong>Base</strong> = the Omaha valuation as stored in the platform (IVO <strong>€9.53</strong>, 2028E): revenue €1,660M × 11.9% EBITDA margin = €199M EBITDA; × <strong>8.0×</strong> EV/EBITDA = €1,592M enterprise value; − net debt €292.8M (bank under the equity method) − healthcare liability €117M (net of DTA) = €1,182M equity ÷ 124.1M shares. <strong>Bear</strong> = e-commerce disappoints and no re-rating (<strong>6.5×</strong>, roughly where CTT trades today — LTM ~6.1×, FY25 6.6× — plus margin compression to 11%). <strong>Bull</strong> = GreenWood's sum of the parts (2-pager, Nov-25), the second valuation in the platform: <strong>€13.43</strong>. All in <strong>EUR</strong>, price €5.86.</p>'''+s[j:]
r('''  price:6.29,''','''  price:5.86,''')
r("Fair value €4.71 — 25% below today.',","Fair value €4.71 — 20% below €5.86.',")
r("ps:4.71, up:-0.25, cagr:'−9%/yr (3Y)', hz:'2028E' },","ps:4.71, up:-0.196, cagr:'2028E', hz:'2028E' },")
i=s.index("    base:{ label:'Base · 8.0× EV/EBITDA (Omaha \\'28)',")
j=s.index("  }\n};",i)
s=s[:i]+'''    base:{ label:'Base · 8.0× EV/EBITDA (Omaha, platform)',
      note:'The Omaha valuation stored in the platform: revenue €1,660M by 2028, below the CMD-2025 ambition given regulation and slower Chinese shipments; EBITDA margin 11.9% (e-commerce 9%, mail & services 15%, Banco CTT 20%; no bank sale assumed); 8.0× EV/EBITDA, close to 2025 levels and below the 12.5× EBIT the DHL deal implied for parcels. Shares fall to 124.1M at the current buyback pace. IVO €9.53 — 63% above €5.86.',
      rev:1660, revcagr:'below CMD-2025 (€1,600–1,700M revenue ambition)', mgn:11.9, ebitda:199, mult:8.0, ev:1592, netdebt:292.8, hc:117, eq:1182.2, sh:124.1, ps:9.53, up:0.626, cagr:'2028E', hz:'2028E' },
    bull:{ label:'Bull · GreenWood sum of the parts',
      note:'GreenWood\\'s 2-pager (Nov-25), kept in the platform as the second valuation: parcels at 12.5× EBIT (the DHL deal multiple), the bank at 1.4× book, mail & financial services at 7.5× EBIT and the real estate fund, less HoldCo debt and the healthcare liability. €13.43 — 129% above €5.86. GreenWood\\'s later flash notes put 2026E fair value at €18.0 (Apr-26) and €14.7 (Aug-26).',
      parts:[['Parcels EBIT €85M × 12.5×',1062.5],['Bank book €348M × 1.4×',487.2],['Mail & FS EBIT €37M × 7.5×',277.5],['Real estate',165]],
      claims:[['HoldCo debt',143],['Healthcare liability',117]],
      sum:1992.2, eq:1732.2, sh:129, ps:13.43, up:1.292, cagr:'GreenWood Nov-25', hz:'2026E' }
'''+s[j:]
r('''      var rows='';
      rows+='<tr><td>Revenue '+s.hz+'</td><td>'+eur(s.rev)+'</td></tr>';''','''      var rows='';
      if(s.parts){
        s.parts.forEach(function(pt,k){ rows+='<tr><td>'+(k?'+ ':'')+pt[0]+'</td><td>'+eur(pt[1])+'</td></tr>'; });
        rows+='<tr class="vc-sep"><td>= Value of parts</td><td>'+eur(s.sum)+'</td></tr>';
        s.claims.forEach(function(c){ rows+='<tr><td>− '+c[0]+'</td><td>('+c[1]+')</td></tr>'; });
        rows+='<tr class="vc-sep"><td>= Equity value</td><td>'+eur(s.eq)+'</td></tr>';
        rows+='<tr><td>÷ Shares</td><td>'+s.sh+'M</td></tr>';
      } else {
      rows+='<tr><td>Revenue '+s.hz+'</td><td>'+eur(s.rev)+'</td></tr>';''')
r('''      rows+='<tr><td>÷ Shares</td><td>'+s.sh+'M</td></tr>';
      var card=''','''      rows+='<tr><td>÷ Shares</td><td>'+s.sh+'M</td></tr>';
      }
      var card=''')
r("rows+='<tr><td>− Net debt</td><td>('+s.netdebt+')</td></tr>';","rows+='<tr><td>− Net debt</td><td>('+(+s.netdebt).toFixed(s.netdebt%1?1:0)+')</td></tr>';")
# AI Analysis
n=s.count('<summary>Analysis</summary>'); assert n>5
s=s.replace('<summary>Analysis</summary>','<summary>AI Analysis</summary>')
# Spanish passage
r('''EBIT bajó y el net income bajó más porque el impuesto se normalizó: 2023 tuvo una tasa efectiva anómala de ~1.8% (impuesto de solo €1.1M); 2024 volvió a ~16.5% (€9.3M). Ese salto explica buena parte de la caída (tax noise, no operación). Los minoritarios empezaron a crecer, consistente con consolidar adquisiciones donde CTT no tiene el 100%.''','''EBIT fell and net income fell more because tax normalised: 2023 had an unusual effective rate of ~1.8% (only €1.1M of tax), and 2024 went back to ~16.5% (€9.3M). That jump explains much of the drop (tax noise, not operations). Minorities started to grow, consistent with consolidating acquisitions CTT does not own 100%.''')
# bank tables
r('<tr><td><strong>Banco CTT</strong></td><td><strong>1.1×</strong></td><td>—</td><td><strong>19%</strong></td></tr>','<tr><td><strong>Banco CTT</strong></td><td><strong>1.1×</strong></td><td>—</td><td><strong>13.8%*</strong></td></tr>')
r('<tr><td>BPCE — NovoBanco</td><td>Jun-25</td><td>1.7×</td><td>1.3×</td><td>Portugal</td></tr>','<tr><td>BPCE — Novo Banco</td><td>Jun-25</td><td>—</td><td>1.7×</td><td>Portugal</td></tr>')
r('<td><strong>Banco CTT (9%) — Generali</strong></td>','<td><strong>Banco CTT (8.7%) — Generali</strong></td>')
r('''The sale of the 9% stake to Generali in 2022 (1.1× book) already sets a precedent, and the aim is to secure a sale multiple around 1.3–1.5× book to crystallize value.</p>''','''The sale of the 8.7% stake to Generali in 2022 (1.1× book) already sets a precedent, and the aim is to secure a sale multiple around 1.3–1.5× book to crystallize value. BPCE paid 1.7× tangible book for Novo Banco. GreenWood (Aug-26) puts the bank's tangible book at €275M and CTT's 91% stake at €350–475M (1.4–1.9×). Grupo Cajamar's approach ended on 4 Sep without a published price, so a sale now needs a new process and then Bank of Portugal/ECB approval.</p>
<p style="font-size:0.78rem;color:var(--muted);">* Banco CTT: return on tangible equity FY25 (CTT results), replacing the 19% ROE shown earlier, which did not match the 13.8% / 12.1% ROTE in the chart above.</p>''')
# GreenWood chart
r('<h3>GreenWood base-case fair value vs stock price (€/share) — Sep-17 → Nov-25</h3>','<h3>GreenWood base-case fair value vs stock price (€/share) — Sep-17 → Aug-26</h3>')
r('''The honest read for today's thesis is the recent, same-target-year cluster: €15–17.3 on a 2026 basis, trimmed to €13.3 in the latest 2-pager.</p>''','''The honest read for today's thesis is the recent, same-target-year cluster on a 2026 basis: €15–17.3 through May-25, €13.3 in the Nov-25 2-pager, then €18.0 in the April 2026 flash note and €14.7 in August 2026, the last one after the Cacesa hit, with the price at €6.15. GreenWood is a 6.4% holder with board seats, so these are an interested party's numbers.</p>''')
r('''var GWX = ["Sep-17","Nov-17","Dec-17","Jan-18","Feb-18","Mar-18","Apr-18","May-18","Aug-18","Nov-18","Feb-19","May-19","Nov-19","Aug-20","Mar-21","Jan-22","Nov-22","Oct-23","Apr-24","Dec-24","May-25","Nov-25"];
var gwSOP   = [20.27,18.58,20.48,13.6,13.6,14.03,15.92,15.48,22.03,28.59,21.02,28.28,17.63,15.44,14.79,21.0,17.0,15.0,17.0,17.0,17.3,13.3];
var gwPrice = [5.06,3.13,3.49,3.49,3.4,3.2,3.0,3.11,3.18,3.38,2.78,2.52,3.15,2.69,3.18,4.2,3.1,3.36,4.5,5.4,7.18,7.0];
var gwTY    = ["2020","2020","2020","2020","2020","2020","2020","2020","2021","2022","2022","2022","2022","2022","2022","2024","2024","2025","2026","2026","2026","2026"];''','''var GWX = ["Sep-17","Nov-17","Dec-17","Jan-18","Feb-18","Mar-18","Apr-18","May-18","Aug-18","Nov-18","Feb-19","May-19","Nov-19","Aug-20","Mar-21","Jan-22","Nov-22","Oct-23","Apr-24","Dec-24","May-25","Nov-25","Apr-26","Aug-26"];
var gwSOP   = [20.27,18.58,20.48,13.6,13.6,14.03,15.92,15.48,22.03,28.59,21.02,28.28,17.63,15.44,14.79,21.0,17.0,15.0,17.0,17.0,17.3,13.3,18.0,14.7];
var gwPrice = [5.06,3.13,3.49,3.49,3.4,3.2,3.0,3.11,3.18,3.38,2.78,2.52,3.15,2.69,3.18,4.2,3.1,3.36,4.5,5.4,7.18,7.0,6.60,6.15];
var gwTY    = ["2020","2020","2020","2020","2020","2020","2020","2020","2021","2022","2022","2022","2022","2022","2022","2024","2024","2025","2026","2026","2026","2026","2026","2026"];''')
r('<div class="foot">Omaha Inversiones · Fuente: FiscalAI + CTT filings + GreenWood Investors · CTT Correios de Portugal (XLIS_CTT)</div>','<div class="foot">Omaha Inversiones · Source: FiscalAI + CTT filings + GreenWood Investors (Nov-25 2-pager; Apr-26 and Aug-26 flash notes) + ECO · CTT Correios de Portugal (XLIS_CTT) · Narrative: <a href="https://claude.ai/artifact/EaAHV1fdv9bVLP7SEN2Yoq" target="_blank" rel="noopener">CTT Q-Report 2Q26</a></div>')
open(p,'w').write(s)
print('ok')
