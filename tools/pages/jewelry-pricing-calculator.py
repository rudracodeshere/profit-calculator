PAGE = dict(
    slug="jewelry-pricing-calculator",
    cat="Maker pricing",
    nav_name="Jewelry pricing calculator",
    title="Jewelry Pricing Calculator: Metal, Labor, Wholesale and Retail",
    desc="Price handmade jewelry from metal weight, stones, findings, labor and overhead. Get wholesale and retail prices and what you keep after Etsy or Shopify fees.",
    h1="Jewelry pricing calculator",
    lead="Enter the metal by weight at your supplier's price, then stones, findings and your time. You get a full cost per piece, a wholesale and a retail price, how sensitive that price is to metal prices, and what a retail sale leaves you after platform fees.",
    form="""      <label for="gr">Metal weight per piece</label>
      <div class="in"><input id="gr" type="number" inputmode="decimal" min="0" step="0.1" value="5"><span>grams</span></div>
      <label for="pg">Metal price <small>(today's price from your supplier)</small></label>
      <div class="in"><span>$</span><input id="pg" type="number" inputmode="decimal" min="0" step="0.01" value="1.50"><span>per gram</span></div>
      <label for="st">Stones, beads and findings</label>
      <div class="in"><span>$</span><input id="st" type="number" inputmode="decimal" min="0" step="0.01" value="4.50"></div>
      <label for="mn">Bench time per piece</label>
      <div class="in"><input id="mn" type="number" inputmode="decimal" min="0" step="1" value="60"><span>minutes</span></div>
      <label for="hr">Your hourly rate</label>
      <div class="in"><span>$</span><input id="hr" type="number" inputmode="decimal" min="0" step="0.5" value="25"><span>/ hour</span></div>
      <label for="oh">Overhead <small>(tools, polishing supplies, packaging, as % of cost)</small></label>
      <div class="in"><input id="oh" type="number" inputmode="decimal" min="0" step="1" value="10"><span>%</span></div>
      <label for="mk">Markup to wholesale <small>(on full cost)</small></label>
      <div class="in"><input id="mk" type="number" inputmode="decimal" min="0" step="5" value="100"><span>%</span></div>
      <label for="rm">Retail multiplier <small>(x wholesale)</small></label>
      <div class="in"><input id="rm" type="number" inputmode="decimal" min="0" step="0.1" value="2"><span>x</span></div>
      <label for="plat">Fees check: where you sell at retail</label>
      <select id="plat" class="full">
        <option value="etsy">Etsy (6.5% + 3% + $0.25 + $0.20)</option>
        <option value="shop">Shopify Basic (2.9% + $0.30)</option>
        <option value="own">Craft fair, own site or custom rate</option>
      </select>
      <details><summary class="note">Edit fee rates</summary>
      <label for="etx">Etsy fees per sale <small>(6.5% + 3%; $0.25 + $0.20 listing)</small></label>
      <div class="in"><input id="etx" type="number" min="0" step="0.1" value="9.5"><span>% +</span><span>$</span><input id="etf" type="number" min="0" step="0.01" value="0.45"></div>
      <label for="spp">Shopify Payments card rate</label>
      <div class="in"><input id="spp" type="number" min="0" step="0.1" value="2.9"><span>% +</span><span>$</span><input id="spf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="opp">Custom rate <small>(card reader, own site)</small></label>
      <div class="in"><input id="opp" type="number" min="0" step="0.1" value="0"><span>% +</span><span>$</span><input id="opf" type="number" min="0" step="0.01" value="0"></div>
      </details>""",
    out="""<div class="big"><span>Retail price</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var mt=n('gr')*n('pg'),lab=n('mn')/60*n('hr'),sub=mt+n('st')+lab,o=n('oh')/100,cost=sub*(1+o);
  var mul=(1+n('mk')/100)*n('rm'),ws=cost*(1+n('mk')/100),rt=ws*n('rm'),rt10=(cost+mt*0.1*(1+o))*mul;
  var pl=$('plat').value,k=pl==='etsy'?['etx','etf','Etsy fees']:pl==='shop'?['spp','spf','Shopify Payments fee']:['opp','opf','Card fees'];
  var fees=rt?rt*n(k[0])/100+n(k[1]):0,keep=rt-fees,prof=keep-cost;
  $('big').textContent=m(rt);
  setRows([['Metal ('+n('gr')+' g at '+m(n('pg'))+'/g)',m(mt)],['Stones, beads, findings',m(n('st'))],['Labor ('+n('mn')+' min)',m(lab)],['Overhead ('+pc(o,0)+')',m(sub*o)],['Full cost per piece',m(cost),'total'],
    ['Wholesale ('+n('mk')+'% markup)',m(ws)],['Retail ('+n('rm')+'x wholesale)',m(rt)],['Retail if metal goes up 10%',m(rt10)],
    [k[2]+' on a retail sale',m(-fees)],['You keep after fees',m(keep)],['Profit after full cost',m(prof),'total']]);
  if(!cost){verdict(false,'Enter the metal, findings and your time to price a piece.');return}
  if(prof<0)verdict(false,'At '+m(rt)+' the '+k[2].toLowerCase()+' of '+m(fees)+' leave you '+m(-prof)+' short of your full cost. Raise the markup.');
  else verdict(true,'At '+m(rt)+', '+k[2].toLowerCase()+' take '+m(fees)+' and you keep '+m(prof)+' after metal, findings, overhead and your '+m(lab)+' of labor.');
}""",
    note="Metal prices are not live: enter what your supplier charges per gram today (sheet, wire and casting grain are priced differently from spot). Fee defaults are US rates as of October 2026: Etsy 6.5% transaction + 3% + $0.25 processing + $0.20 listing; Shopify Basic 2.9% + $0.30 (plan fee not included). Fees are on the item price only, shipping and tax left out.",
    body="""<h2>How to price a piece of jewelry</h2>
<p>Price from the bench up. Weigh the metal that goes into the finished piece (plus what you lose to filing and sprue, if you track it) and multiply by what you pay per gram. Add stones, beads, chain and findings. Add your bench time at an hourly rate, then a percentage for overhead: saw blades, polishing compound, pickle, packaging and tool wear that no single piece carries on its own.</p>
<p class="formula">Full cost = (metal g x price per g + stones + findings + labor) x (1 + overhead %)<br>Wholesale = full cost x (1 + markup) &nbsp;|&nbsp; Retail = wholesale x 2</p>
<h2>A worked example</h2>
<p>A silver ring uses 5 grams at $1.50 a gram, so <strong>$7.50</strong> of metal. Add $4.50 of stone and findings and an hour at $25 ($25.00). Adding 10% overhead ($3.70) brings the full cost to <strong>$40.70</strong>. A 100% markup gives a wholesale price of <strong>$81.40</strong> and doubling that gives a retail price of <strong>$162.80</strong>.</p>
<p>Sold on Etsy at $162.80, fees take $15.92, and after the full cost you keep $106.18. On Shopify Basic the card fee is $5.02 and you keep $117.08, before the monthly plan fee.</p>
<h2>When metal prices move</h2>
<p>Labor is usually the biggest part of a handmade piece, so a rise in metal prices moves the retail price less than people expect. In the example, a 10% rise in the silver price raises the retail price from $162.80 to $166.10. Pieces that are heavy and quick to make, like cast or chunky chain pieces, feel it much more. Re-run your heaviest pieces whenever your supplier's price changes, and reprice those first.</p>
<p>Gold and platinum pieces are the opposite case: metal can be most of the cost. For those, some jewelers quote metal at the day's price and add labor and markup on top, rather than fixing a price for a whole season.</p>""",
    faqs=[
        ("How do you calculate the price of handmade jewelry?", "Add metal (grams x price per gram), stones and findings, and your labor, then add overhead. Mark the total up to wholesale and double for retail. 5 g of silver at $1.50/g, $4.50 of findings and an hour at $25 with 10% overhead is a $40.70 cost, $81.40 wholesale and $162.80 retail."),
        ("Should I mark up my labor too, or just materials?", "Mark up the full cost, labor included. If you only mark up materials, your profit disappears on the pieces that take longest to make, which are often your best work. The markup is what pays for selling, marketing and slow months; your hourly rate is just your wage."),
        ("How much does Etsy take on a jewelry sale?", "In the US, 6.5% transaction fee, 3% + $0.25 processing and $0.20 listing fee per item. On a $162.80 ring that is $15.92, before any Offsite Ads fee."),
        ("How often should I update prices for metal costs?", "Whenever your supplier's price per gram changes noticeably, starting with your heaviest pieces. On a labor-heavy ring like the example, a 10% rise in metal adds only $3.30 to a $162.80 retail price; on a heavy cast piece it can add much more."),
    ],
    related=["handmade-pricing-calculator", "wholesale-price-calculator", "etsy-fee-calculator", "etsy-pricing-calculator", "markup-calculator"],
    og_image="pins/pin-11.png",
    tests=[
        {"expect": {"big": "$162.80", "rows": ["$7.50", "$4.50", "$25.00", "$3.70", "$40.70", "$81.40", "$166.10", "-$15.92", "$146.88", "$106.18"], "verdict": "$106.18"}},
        {"set": {"plat": "shop"}, "expect": {"rows": ["-$5.02", "$157.78", "$117.08"]}},
        {"set": {"mk": "0", "rm": "1"}, "expect": {"big": "$40.70", "verdict": "Raise the markup"}},
        {"set": {"plat": "own"}, "expect": {"rows": ["$162.80", "$122.10"]}},
        {"set": {"gr": "0", "st": "0", "mn": "0"}, "expect": {"big": "$0.00", "verdict": "Enter the metal"}},
    ],
)
