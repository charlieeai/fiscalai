import re
SRC = {
 "cacesa": 'ECO, "CTT chegam a acordo para comprar espanhola Cacesa por 104 milhões," 18 Dec 2024. <a href="https://eco.sapo.pt/2024/12/18/ctt-chegam-a-acordo-para-comprar-espanhola-cacesa-por-104-milhoes/">eco.sapo.pt</a>',
 "pr": 'CTT, 1H26 results release, 28 Jul 2026 (via FiscalAI, filing 0000000650-26-10306546).',
 "eco0728": 'ECO, "CTT aumentam recompra de ações mas lucro semestral cai," 28 Jul 2026. <a href="https://eco.sapo.pt/2026/07/28/ctt-aumentam-recompra-de-acoes-mas-lucro-semestral-cai-34/">eco.sapo.pt</a>',
 "omaha": 'Omaha Value platform, CTT: valuations "Omaha" (IVO €9.53) and "Greenwood" (sum of the parts, €13.43), catalysts and thesis, as of 5 Oct 2026.',
 "g4": 'ACE Cargadores, "Aduanas amplía al 15 de junio la prórroga para aplicar el G4," 27 May 2026. <a href="https://www.ace-cargadores.com/2026/05/27/aduanas-amplia-al-15-de-junio-la-prorroga-para-aplicar-el-g4-y-la-inspeccion-fisica-en-1a-linea/">ace-cargadores.com</a>',
 "duty": 'Crowe UK, "EU agrees fixed customs duty on small parcels," Dec 2025 <a href="https://www.crowe.com/uk/news/eu-agrees-fixed-customs-duty-on-small-parcels">crowe.com</a>; AEAT, Aduanas novedades 2026 (Regulation 2026/382) <a href="https://sede.agenciatributaria.gob.es/Sede/aduanas/novedades/2026.html">agenciatributaria.gob.es</a>.',
 "call": 'CTT 2Q26 earnings call, 29 Jul 2026, transcript via FiscalAI; also <a href="https://www.investing.com/news/transcripts/earnings-call-transcript-ctt-posts-solid-h1-2026-growth-as-customs-pressure-lingers-93CH-4819022">Investing.com</a>.',
 "postnl": 'PostNL H1 2026 results call, 3 Aug 2026 (transcript via FiscalAI).',
 "bpost": 'bpost group 2Q26 results call, 7 Aug 2026 (transcript via FiscalAI).',
 "austrian": 'news.at, Austrian Post H1 2026 results, Aug 2026. <a href="https://www.news.at/wirtschaft/post-ebit-sinkt-im-halbjahr-um-22-prozent-auf-733-mio-euro">news.at</a>',
 "inpost": 'InPost 2Q26 results call, 31 Aug 2026 (transcript via FiscalAI).',
 "poczta": 'Rzeczpospolita, "Poczta Polska potwierdza mocny spadek paczek z Chin," 28 Jul 2026. <a href="https://www.rp.pl/handel/art44902161-poczta-polska-potwierdza-mocny-spadek-paczek-z-chin">rp.pl</a>',
 "liege": 'Air Cargo News, "New EU e-commerce rules have instant impact at Liège," 14 Aug 2026. <a href="https://www.aircargonews.net/cargo-airport/2026/08/new-eu-e-commerce-rules-have-instant-impact-at-liege/">aircargonews.net</a>',
 "capacity": 'Air Cargo News, "Air cargo e-commerce growth flatlines in July," 10 Sep 2026 <a href="https://www.aircargonews.net/e-commerce-logistics/2026/09/air-cargo-e-commerce-growth-flatlines-in-july/">aircargonews.net</a>; StatTimes, 1 Sep 2026 <a href="https://www.stattimes.com/ecommerce/china-europe-e-commerce-cargo-after-eu-de-minimis-reform-1360498">stattimes.com</a> (Rotate data, 1–21 Jun vs 1–21 Aug 2026).',
 "temu": 'ECO, "CTT reforçam parceria logística com chinesa Temu na Península Ibérica," 4 Dec 2025 <a href="https://eco.sapo.pt/2025/12/04/ctt-reforcam-parceria-logistica-com-chinesa-temu-na-peninsula-iberica/">eco.sapo.pt</a>; Ecommerce News Europe, "Temu: 80% of European sales via local warehouses," 20 Jan 2025 <a href="https://ecommercenews.eu/temu-80-of-european-sales-via-local-warehouses/">ecommercenews.eu</a>.',
 "guid": 'Jornal Económico, CTT 2026 guidance, 18 Mar 2026; ECO, 28 Jul 2026 (guidance revised).',
 "slides": 'Investing.com, "CTT H1 2026 slides: CEP growth strong but customs pressure weighs." <a href="https://www.investing.com/news/company-news/ctt-h1-2026-slides-cep-growth-strong-but-customs-pressure-weighs-93CH-4819070">investing.com</a>',
 "cnmc": 'CNMC, annual postal market report, 5 Aug 2026 (revenue per parcel computed: €7,325m / 1,335m). <a href="https://www.cnmc.es/prensa/informe-anual-postal-20260805">cnmc.es</a>',
 "postnlh1": 'Post&amp;Parcel, PostNL H1 2026 results, 5 Aug 2026. <a href="https://postandparcel.info/?p=162509">postandparcel.info</a>',
 "dhl": 'ECO, "CTT encaixam 64 milhões com parceria ibérica com a DHL," 12 May 2026. <a href="https://eco.sapo.pt/2026/05/12/ctt-encaixam-64-milhoes-com-parceria-iberica-com-a-dhl-para-a-distribuicao-de-encomendas-online/">eco.sapo.pt</a>',
 "ipo": 'Euronext, CTT listing release, Dec 2013 <a href="https://www.euronext.com/en/about/media/euronext-press-releases/acoes-dos-ctt-comecam-negociar-na-euronext-apos-sucesso-da">euronext.com</a>; CTT 2013 results <a href="https://www.ctt.pt/contentAsset/raw-data/6b71b92f-5300-4d36-a058-da9d9ded00b1/ficheiro/export/CTT%202013%20Results%20Press%20Release_EN.pdf">press release</a>.',
 "mult": 'Multiples computed by Omaha from CTT results (2013 <a href="https://www.ctt.pt/contentAsset/raw-data/6b71b92f-5300-4d36-a058-da9d9ded00b1/ficheiro/export/CTT%202013%20Results%20Press%20Release_EN.pdf">release</a>, FY15 <a href="https://www.ctt.pt/contentAsset/raw-data/65b75db2-e459-46e4-b522-5b300e8ce1df/ficheiro/export/CTT_FY15%20Results.pdf">presentation</a>, FY20 <a href="https://www.ctt.pt/contentAsset/raw-data/4c775e33-a480-4bbe-b968-c5e8cabaf7cb/ficheiro/export/Press%20Release_2020_16%20Mar.pdf">release</a> with 2019 comparatives, FY25 release) and FiscalAI prices. EV includes employee-benefit liabilities net of tax; today excludes IFRS 16 leases for comparability with 2013.',
 "je2017": 'Jornal Económico, CTT shares fall 21.58%, 1 Nov 2017. <a href="https://jornaleconomico.sapo.pt/noticias/ctt-sofre-queda-de-2158-e-fecha-abaixo-dos-4-euros-acionistas-perdem-milhoes-227881">jornaleconomico.sapo.pt</a>',
 "eco2019": 'ECO, "CTT atingem novo mínimo histórico. Ações já valem menos de dois euros," 30 Jul 2019. <a href="https://eco.sapo.pt/2019/07/30/ctt-atingem-novo-minimo-historico-acoes-ja-valem-menos-de-dois-euros/">eco.sapo.pt</a>',
 "jn2019": 'Jornal de Negócios, CEO of CTT invested in shares after taking office, 3 Jun 2019. <a href="https://www.jornaldenegocios.pt/mercados/detalhe/ceo-dos-ctt-investiu-mais-de-11-mil-euros-em-acoes-apos-a-tomada-de-posse">jornaldenegocios.pt</a>',
 "jn2026": 'Jornal de Negócios, "João Bento despede-se dos CTT com lucros a crescer 11%," 18 Mar 2026. <a href="https://www.jornaldenegocios.pt/empresas/telecomunicacoes/detalhe/joao-bento-despede-se-dos-ctt-com-lucros-a-crescer-11-para-50-7-milhoes-de-euros">jornaldenegocios.pt</a>',
 "fiscal": 'FiscalAI, XLIS_CTT: stock prices (adjusted), shares outstanding, adjusted EBITDA FY2025.',
 "cep": 'CEP-Research, "2025 Spain CEP market outlook," 25 Sep 2025. <a href="https://www.cep-research.com/2025/09/25/2025-spain-cep-market-outlook/">cep-research.com</a>',
 "cajamar": 'ECO, "Espanhóis do Cajamar interessados no Banco CTT," 21 Jul 2026 <a href="https://eco.sapo.pt/2026/07/21/espanhois-do-cajamar-interessados-no-banco-ctt/">eco.sapo.pt</a>; Investing.com Brasil, 22 Jul 2026 <a href="https://br.investing.com/news/stock-market-news/acoes-da-ctt-disparam-com-interesse-nao-solicitado-no-banco-ctt-93CH-2009260">br.investing.com</a>; ECO, "Espanhóis do Cajamar desistem da compra do Banco CTT," 4 Sep 2026 <a href="https://eco.sapo.pt/2026/09/04/espanhois-do-cajamar-desistem-da-compra-do-banco-ctt/">eco.sapo.pt</a>.',
 "generali": 'ECO, "Dois anos depois, Generali entra no capital do Banco CTT," 29 Nov 2024. <a href="https://eco.sapo.pt/2024/11/29/dois-anos-depois-generali-entra-no-capital-do-banco-ctt-com-injecao-de-25-milhoes/">eco.sapo.pt</a>',
 "gw": 'GreenWood Investors, first half 2026 letter, 13 Aug 2026 <a href="https://www.gwinvestors.com/first-half-2026-letter-to-investors/">gwinvestors.com</a>; CTT shareholder structure, 30 Sep 2026 <a href="https://www.ctt.pt/grupo-ctt/investidores/estrutura-acionista?language_id=1">ctt.pt</a>.',
 "bv": 'Reuters Breakingviews on BPCE\'s purchase of Novo Banco, 13 Jun 2025. <a href="https://www.itiger.com/news/2543093504">itiger.com</a>',
 "annex": 'Omaha, CTT Q-report 2Q26 data annex (Banco CTT returns, Iberian bank comps and deals, sale multiple estimate). <a href="https://claude.ai/artifact/UaGUNasNFebt4xoxFC3w6b">claude.ai</a>',
 "ptdeals": 'Portuguese bank transactions, announcement to closing: Generali–Banco CTT 8.7% (Nov 2022–Nov 2024), BPCE–Novo Banco (Jun 2025–Apr 2026), Abanca–EuroBic (Nov 2023–Jul 2024), Abanca–Banco Caixa Geral (Nov 2018–Oct 2019), Bankinter–Barclays Portugal (Sep 2015–Apr 2016), Lone Star–Novo Banco (Mar–Oct 2017), CaixaBank–BPI (Apr 2016–Feb 2017), Fosun–BCP (Jul–Nov 2016); from company releases, ECO and Observador. Median 8.8 months excluding the Banif resolution.',
 "analysts": 'CTT investor relations, analyst consensus page. <a href="https://www.ctt.pt/grupo-ctt/investidores/acao-ctt/analistas-consenso">ctt.pt</a>',
 "buyback": 'CTT current reports via FiscalAI: buyback increase, 28 Jul 2026 (0000000650-26-48884911); purchases to 30 Sep 2026 (0000000650-26-12531166).',
 "insiders": 'JornalPT50, "Chairman e administradores executivos dos CTT gastam 85 mil euros na compra de ações," 23 Mar 2026. <a href="https://jornalpt50.pt/noticia/chairman-e-administradores-executivos-dos-ctt-gastam-85-mil-euros-na-compra-de-acoes/">jornalpt50.pt</a>',
 "ar25": 'CTT, Integrated Report 2025 (network, lockers, Iberian B2C share, Cacesa Polonia), ctt.pt.',
 "austriancall": 'Austrian Post H1 2026 results call, 7 Aug 2026 (Investing.com transcript).',
 "anacom": 'ANACOM, postal statistics, 3Q 2025. <a href="https://anacom.pt/render.jsp?contentId=1823702">anacom.pt</a>',
}

ARTICLE = r'''
<p>In December 2024 CTT paid €104 million for Cacesa, a Spanish customs broker, at a price the press described as "equivalent to a 5.5x EBIT multiple."[[cacesa]] That implied roughly €19 million of profit a year. In the second quarter of 2026 Cacesa earned €0.6 million of recurring EBIT, down 88.8% on a pro forma basis.[[pr]] So, was the acquisition overpaid? On the profit it was bought for, no; on this quarter's run rate, €2.4 million a year, it cost over 40x EBIT. It depends on whether Cacesa can replace parcel-by-parcel clearance with B2B clearance and fulfilment, which is where management is taking it while it cuts staff at Cacesa's sites.[[eco0728]][[omaha]]</p>

<p>Nothing went wrong inside Cacesa. Two regulatory events hit it, so the cause is external. Spain's G4 pre-declaration now requires customs brokers to list "each one of the individual packages that a consolidated shipment contains," and after two extensions it became mandatory on 15 June.[[g4]] Two weeks later, on 1 July, the EU ended the €150 de minimis exemption and put a fixed €3 duty on small parcels.[[duty]] Guy Pacheco, CTT's CEO since April, named both on the call:</p>
<blockquote>"driven by two regulatory change, one affecting only the Spanish business, that is in the introduction of the G4 regulation, and the anticipation of what has been implemented on the 1st of July"[[call]]</blockquote>

<p>The Chinese marketplaces did not stop shipping. As the CEO also explained, they rerouted: "We are seeing volumes moving from Madrid to Eastern Europe and Central Europe, namely Benelux."[[call]] The operators there are not gaining. PostNL's international volumes fell 15%, "mainly coming from our Asian webshops," and when an analyst asked about CTT's comment, its CEO answered: "On the Asian side... I don't see more volume coming to Amsterdam or Liège."[[postnl]] bpost saw "a serious decline in the volumes coming in" after the €3 duty,[[bpost]] and Austrian Post, InPost and Poczta Polska all reported falling Chinese volumes.[[austrian]][[inpost]][[poczta]] Freighter capacity fell at every hub between June and August, most at Madrid (−78%) against Liège (−35%).[[capacity]] The shift is relative: Madrid lost more of a shrinking flow, which is a smaller market more than a share loss to competitors. Part of what moved east still passes through CTT: "In Eastern Europe, we have strong market share in Poland," Pacheco said, where Cacesa clears cargo at Łódź airport.[[call]][[ar25]]</p>

<p>The same rules push the platforms toward the other half of what CTT sells. Temu has said it wants 80% of its European orders shipped from local warehouses, and in December 2025 CTT signed a memorandum with Temu covering road and sea transport, warehousing and delivery in Iberia.[[temu]] Pacheco said the GMV (gross merchandise value, the total value of goods sold on a platform) of the three big platforms is "declining between 30% and 40%."[[call]] If those parcels move from air freight cleared in Madrid to containers unloaded in a warehouse near Lisbon, CTT loses a customs fee and keeps the delivery. It is better for CTT to keep at least that part of the logistics chain.</p>

<h2>Everything else grew</h2>
<p>Group revenue rose 11.7% to €345.0 million. Express and parcel volumes rose 20.7% pro forma to 44.1 million items, and parcel recurring EBIT rose 6.6% to €10.2 million. The core held through the shock: first-half volumes grew 19.4% to 83.8 million items, management still guides at least high single digit growth for the year, and July, the worst month, was only 2–3% down overall.[[pr]][[call]] Mail, which is supposed to be dying, grew recurring EBIT 37.3% to €9.6 million on a 5.93% price increase.[[pr]]</p>

[[FIGURE_EBIT]]

<p>The bill came at the bottom of the income statement. Recurring EBIT fell 3.8% to €25.7 million, net profit halved to €8.4 million, below the €10.0 million consensus, and management cut the 2026 recurring EBIT target to €115–125 million from the "at least €125 million" it set in March.[[pr]][[guid]] The guidance now separates the two worlds: €105–110 million without customs. Pacheco on why the range is wide: "the implementation of a new levy in the end of the year brings limited visibility to Cacesa." He also warned that "in November is to be expected an additional fee of €2 per parcel," and July started weak: "In July, we are expecting to have a decline between 2% and 3% overall."[[call]] The €3 duty runs until at least July 2028,[[duty]] so the next quarters will carry this effect. What matters is how management deals with what looks like a structural break in Cacesa's old model.</p>

<p>One number bothers me more than Cacesa. Parcel volumes grew 21%, but the parcel EBIT margin fell from 7.7% to 6.7%.[[slides]] Spain's market grew 10% to 1,335 million parcels in 2025 with revenue per parcel flat at about €5.49, according to the CNMC; there is no quarterly data for 2026 yet.[[cnmc]] So far volume is winning on revenue and losing on margin. The DHL joint venture is CTT's answer: €17.5 million of the €35 million synergy target is already identified, and Pacheco said 40% of it comes from revenue.[[call]][[dhl]] Two variables to monitor: whether volume keeps accelerating, and whether margins improve once the synergy costs are behind us.</p>

<h2>Everyone was hit. CTT has the most complete answer</h2>
<p>Because every operator lost Chinese volume, this is an industry problem, and the question is who adapts best. Each peer is answering with one lever. PostNL is pricing: its average price per parcel rose 5.0% while e-commerce volumes fell 6.4%, its Asian webshop contracts now raise prices if volumes fall, and it added a €75 million cost programme.[[postnlh1]][[postnl]] bpost is fighting for share of what still lands in Liège "by commercial action."[[bpost]] Austrian Post bought an SME fulfilment business and raised prices.[[austriancall]] InPost is replacing Chinese parcels with local e-commerce through lockers, and says its Iberian network is now "the largest local network in its market."[[inpost]]</p>

<p>CTT's answer differs in one way: it is the only one of these operators that owns the three links the new flow needs in Iberia. When platforms move from parcels cleared one by one to containers cleared in bulk and stored in local warehouses, the customer needs clearance, storage and delivery together. CTT has the clearance (Cacesa), the last mile (CTT Express, now with DHL eCommerce Spain) and the density: 2,415 post offices and agencies, about 20,000 pickup points across Iberia and 1,320 lockers in Portugal. It already carries Temu's and Shein's local sellers, and by its own estimate its Iberian B2C parcel share doubled to about 12% between 2021 and 2024.[[ar25]] Pacheco called the target "this integration between the clearance, the fulfillment, and also last mile."[[call]] That is the moat: density plus integration.</p>

<p>The weak link is fulfilment. Pacheco admitted CTT's fulfilment operations "are not large" and that acquisitions are "on the table";[[call]] PostNL, bpost and Austrian Post are further ahead there. And InPost's lockers compete directly for out-of-home delivery, which is 16% of CTT's parcel deliveries today and which CTT expects to reach 20–30% of the market within three years.[[call]]</p>

<h2>Back at the IPO price, and at the IPO multiple</h2>
<p>CTT listed in December 2013 at €5.52.[[ipo]] Today it trades at €5.86. A price comparison only means something if the multiples are comparable, so I rebuilt them on the same basis. At the IPO, enterprise value including the employee-benefit liabilities was 6.6x 2013 recurring EBITDA, the P/E was 13.6x and the dividend yield 7.2%. Today, stripping out lease accounting that did not exist in 2013, CTT trades at 6.5x EBITDA and 15.1x 2025 earnings.[[mult]] Same multiple. In between, the multiple went from 10.2x at the November 2015 peak to 3.2x in August 2019,[[mult]] after a 57% profit drop and a dividend cut in 2017 sent the stock below €2.[[je2017]][[eco2019]]</p>

<p>So CTT is not cheap against its IPO. It is cheap against the company it has become: in 2025 recurring EBIT reached €115.2 million, up 35%, and net profit €50.7 million.[[jn2026]] Buybacks cut the share count from 142.4 million at the end of 2022 to 130.3 million in July,[[fiscal]] and CTT Express grew more than twice as fast as the Spanish market in 2024.[[cep]] The market pays for this company what it paid for the 2013 mail operator.</p>

<h2>The bank bid lasted six weeks</h2>
<p>On 21 July CTT disclosed "an unsolicited and non-binding expression of interest" in Banco CTT. Bloomberg named Grupo Cajamar, and the stock rose 5.4% the next day. On 4 September ECO reported that the talks had ended without agreement. No price was ever published.[[cajamar]]</p>

<p>The bank is the part of the thesis I hold with the least evidence. The only recent mark is Generali's purchase of 8.7%, which valued the whole bank at €290 million, about 1.1x book.[[generali]][[annex]] Our own estimate for a sale is 1.3–1.5x book: the bank earned a 13.8% return on tangible equity in 2025, and recent European bank deals cleared at 1.2x book or more.[[annex]] GreenWood, a 6.4% holder, calculates 11–44% EPS accretion from selling the bank at 1.25–2.0x tangible book, and Iberian deals support the top of that range: BPCE paid 1.7x tangible book for Novo Banco.[[gw]][[bv]] The value is real. The path to it is slow and political.</p>

<h2>What are we paying</h2>
<p>Our IVO is €9.53 per share. It values CTT at 8x €199 million of EBITDA, then subtracts net debt with the bank under the equity method and the healthcare liability, net of tax.[[omaha]]</p>
[[FIGURE_BRIDGE]]
<p>The €199 million of EBITDA is almost exactly what CTT earned in 2025: €198.4 million.[[fiscal]] Our valuation does not need growth. It needs last year back, and a market that pays 8x for it instead of today's 6.5x. The DHL deal valued CTT's parcel business at 12.5x EBIT, so 8x EBITDA for the group is not a stretch.[[dhl]] GreenWood's sum of the parts, which we keep as a second valuation, gives €13.43.[[omaha]] The company's own cash says more than any target: it raised the buyback from €30 million to €40 million and by 30 September had bought 4.1 million shares for €25.1 million, about €6.12 each.[[buyback]] In March the chairman bought 10,000 shares at about €6.[[insiders]]</p>

<h2>Where I could be wrong</h2>
<p>First, Cacesa may not be a dip. If the €2 fee in November keeps Chinese flows away from Madrid for many quarters, maybe years, the €104 million is a future write-down. Second, parcel margins: if the joint venture synergies arrive late, CTT will be growing volume for its customers, not its shareholders. Third, the bank may not be sellable on good terms for a long time. Portuguese bank deals since 2015 took a median of about nine months from announcement to closing, but Banco CTT's own precedent, Generali's 8.7%, took 25 months,[[ptdeals]] and there is no buyer today. I should stop counting on a re-rating from it. Fourth, the CEO is new. Pacheco was CFO before he took the job, and he cut guidance in his first quarter in it. Not a good beginning.</p>

<h2>What I will watch on 3 November</h2>
<p>The four catalysts we track:[[omaha]] whether customs EBIT keeps decelerating or tracks the guidance (about €12.5 million for the year at the midpoints); whether Cacesa wins B2B clearance and fulfilment clients and deploys money in acquisitions; whether the Temu fulfilment test, in negotiation since late August, becomes a five-year contract, which would confirm the bull case; and any new process for the bank, now less likely near term. Beyond them: second-half parcel volumes against guidance, after a July management called "the bottom";[[call]] the parcel margin; and the buyback.</p>

<p>Regulation cost CTT this quarter and may cost it the next ones. It did not change what the company is: 41.5% of Portugal's parcels, a network in Spain growing faster than its market, a mail business that still makes money, and a bank someone wanted to buy. At the IPO multiple, with the IVO 63% above the price, I suggest holding while management adapts.</p>
'''

html = open("ctt-reporte-q-2q26.html").read()
fig_ebit = re.search(r'    <figure id="fig-ebit".*?</figure>', html, re.S).group(0)
fig_bridge = re.search(r'    <figure id="fig-bridge".*?</figure>', html, re.S).group(0)
fig_bridge = fig_bridge.replace("Omaha valuation as stored in the platform. At €5.86 the discount is 38%.", "Omaha valuation as stored in the platform. At €5.86 the discount is 38%; the IVO is 63% above the price.")

order = []
def cite(m):
    k = m.group(1)
    assert k in SRC, k
    if k not in order: order.append(k)
    n = order.index(k) + 1
    return f'<sup class="ref"><a href="#s{n}">{n}</a></sup>'
art = ARTICLE.replace("[[FIGURE_EBIT]]", "@@FIGE@@").replace("[[FIGURE_BRIDGE]]", "@@FIGB@@")
art = re.sub(r"\[\[(\w+)\]\]", cite, art)
# figure captions cite the release and platform
fig_ebit = re.sub(r'<sup class="ref"><a href="#s\d+">\d+</a></sup>', '', fig_ebit)
fig_ebit = fig_ebit.replace("change).</figcaption>", "change).[[pr]]</figcaption>")
fig_ebit = re.sub(r"\[\[(\w+)\]\]", cite, fig_ebit)
art = art.replace("@@FIGE@@", fig_ebit).replace("@@FIGB@@", fig_bridge)
art = "\n".join("    " + l if l.strip() else "" for l in art.strip().splitlines())

sources = "\n".join(f'      <li id="s{i+1}">{SRC[k]}</li>' for i, k in enumerate(order))

html = re.sub(r'(<article id="essay">).*?(</article>)', lambda m: m.group(1) + "\n" + art + "\n  " + m.group(2), html, flags=re.S)
html = re.sub(r'(<section class="sources" id="sources">\s*<h2>Sources</h2>\s*<ol>).*?(</ol>)', lambda m: m.group(1) + "\n" + sources + "\n    " + m.group(2), html, flags=re.S)

reps = [
 ("<title>CTT Reporte Q 2Q26</title>", "<title>CTT Q-Report 2Q26</title>"),
 ('<span class="tag">Reporte Q</span>', '<span class="tag">Q-report</span>'),
 ('<h1 id="title">A Customs Form in Madrid Cost CTT a Quarter. It Did Not Change the Company.</h1>',
  '<h1 id="title">Regulation Took CTT\'s Quarter and May Take the Next Ones. The Thesis Now Rests on How It Adapts.</h1>'),
 ('Parcels grew 21%. Two customs rules wiped out the broker CTT bought eighteen months ago, the bank bid came and went, and the stock is back at its 2013 IPO price. I am holding.',
  'Parcels grew 21%. Two customs rules wiped out the broker CTT bought eighteen months ago, the bank bid came and went, and the stock trades at its 2013 IPO multiple. I suggest holding while management adapts.'),
 ('<div class="byline"><span>By <b>Charlie</b>, Omaha</span><span>5 October 2026</span>', '<div class="byline"><span>5 October 2026</span>'),
 ('Data annex: <a href="https://claude.ai/artifact/UaGUNasNFebt4xoxFC3w6b" target="_blank" rel="noopener">Reporte Q 2Q26, chart-first</a>', 'Data annex: <a href="https://claude.ai/artifact/UaGUNasNFebt4xoxFC3w6b" target="_blank" rel="noopener">Q-report 2Q26, charts and tables</a>'),
 ('text("Data annex: Reporte Q 2Q26 chart-first, https://claude.ai/artifact/UaGUNasNFebt4xoxFC3w6b"', 'text("Data annex: Q-report 2Q26, charts and tables, https://claude.ai/artifact/UaGUNasNFebt4xoxFC3w6b"'),
 ('doc.text("Omaha · CTT Reporte Q 2Q26", M, H - 28);', 'doc.text("Omaha · CTT Q-report 2Q26", M, H - 28);'),
 ('filename: "CTT-Reporte-Q-2Q26.pdf"', 'filename: "CTT-Q-Report-2Q26.pdf"'),
]
for a, b in reps:
    if a not in html and b in html:
        continue
    assert html.count(a) == 1, a[:60]
    html = html.replace(a, b)
open("ctt-reporte-q-2q26.html", "w").write(html)

body = re.sub(r'<figure.*?</figure>', '', art, flags=re.S)
body = re.sub(r'<sup.*?</sup>', '', body, flags=re.S)
print("words", len(re.sub(r'<[^>]+>', ' ', body).split()), "sources", len(order))
