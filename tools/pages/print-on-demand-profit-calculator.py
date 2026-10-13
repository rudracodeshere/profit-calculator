PAGE = dict(
    slug="print-on-demand-profit-calculator",
    cat="Maker pricing",
    nav_name="Print on demand profit calculator",
    title="Print on Demand Profit Calculator for Etsy and Shopify (2026)",
    desc="Work out profit per print on demand sale after the base cost, the provider's shipping, Etsy or Shopify fees and ad spend, plus the break-even price.",
    h1="Print on demand profit calculator",
    lead="Enter the base cost and shipping your print provider charges you, what you charge the buyer, and where you sell. You get profit per sale after platform fees and ads, and the lowest price that doesn't lose money.",
    form="""      <label for="pr">Your sale price <small>(item)</small></label>
      <div class="in"><span>$</span><input id="pr" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div>
      <label for="sb">Shipping you charge the buyer <small>(0 for free shipping)</small></label>
      <div class="in"><span>$</span><input id="sb" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <label for="bc">Product base cost <small>(from your POD provider's catalog)</small></label>
      <div class="in"><span>$</span><input id="bc" type="number" inputmode="decimal" min="0" step="0.01" value="12.50"></div>
      <label for="ps">Shipping the POD provider charges you</label>
      <div class="in"><span>$</span><input id="ps" type="number" inputmode="decimal" min="0" step="0.01" value="4.75"></div>
      <label for="ad">Ad cost per sale <small>(ad spend / orders, or Offsite Ads fee)</small></label>
      <div class="in"><span>$</span><input id="ad" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="plat">Where you sell</label>
      <select id="plat" class="full">
        <option value="etsy">Etsy (9.5% + $0.45 per order)</option>
        <option value="shop">Shopify Basic (2.9% + $0.30)</option>
        <option value="cus">Other (custom % + fixed fee)</option>
      </select>
      <details><summary class="note">Edit fee rates</summary>
      <label for="etx">Etsy: transaction + processing <small>(6.5% + 3%; $0.25 + $0.20 listing)</small></label>
      <div class="in"><input id="etx" type="number" min="0" step="0.1" value="9.5"><span>% +</span><span>$</span><input id="etf" type="number" min="0" step="0.01" value="0.45"></div>
      <label for="spp">Shopify Payments card rate</label>
      <div class="in"><input id="spp" type="number" min="0" step="0.1" value="2.9"><span>% +</span><span>$</span><input id="spf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="cpp">Custom platform fee</label>
      <div class="in"><input id="cpp" type="number" min="0" step="0.1" value="10"><span>% +</span><span>$</span><input id="cpf" type="number" min="0" step="0.01" value="0"></div>
      </details>""",
    out="""<div class="big"><span>Profit per sale</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var pl=$('plat').value,k=pl==='etsy'?['etx','etf','Etsy fees']:pl==='shop'?['spp','spf','Shopify Payments fee']:['cpp','cpf','Platform fees'];
  var r=n(k[0])/100,f=n(k[1]),p=n('pr'),s=n('sb'),t=p+s,costs=n('bc')+n('ps')+n('ad');
  var fees=t?t*r+f:0,prof=t-fees-costs,be=r<1?Math.max(0,(costs+f)/(1-r)-s):-1;
  $('big').textContent=m(prof);
  var rows=[['Buyer pays (item + shipping)',m(t)],[k[2],m(-fees)],['Product base cost',m(-n('bc'))],['POD shipping',m(-n('ps'))]];
  if(n('ad'))rows.push(['Ad cost per sale',m(-n('ad'))]);
  rows.push(['Profit per sale',m(prof),'total'],['Margin on what the buyer pays',t?pc(prof/t):'0%'],['Break-even item price',be<0?'not possible':m(be)]);
  setRows(rows);
  if(!t){verdict(false,'Enter your sale price to see profit per sale. At these costs the break-even item price is '+(be<0?'not reachable':m(be))+'.');return}
  var gap=n('ps')-s,gs=gap>0?' You charge '+m(gap)+' less for shipping than the provider charges you; that gap comes out of the item price.':'';
  if(prof<0)verdict(false,'Each sale loses '+m(-prof)+'. Raise the item price to at least '+m(be)+' to break even.'+gs);
  else verdict(prof/t>=0.15,'You make '+m(prof)+' per sale. Below '+m(be)+' an item price loses money.'+gs+(prof/t<0.15?' A margin under 15% leaves little room for misprint refunds or a sale.':''));
}""",
    note="Base cost and provider shipping are inputs because they depend on your provider, product, print method and destination; nothing here is a quoted provider price. Fee defaults are US rates as of October 2026: Etsy 6.5% transaction + 3% + $0.25 processing + $0.20 listing; Shopify Basic 2.9% + $0.30 (the monthly plan fee is not included). Sales tax and VAT are left out.",
    body="""<h2>Where the money goes on a POD sale</h2>
<p>On a print on demand sale you pay twice before you see a cent: the provider charges the <strong>base cost</strong> for printing the item and a separate <strong>shipping charge</strong> to send it, and the platform takes its fee on everything the buyer paid, shipping included. Ads, if you run them, come out of what is left.</p>
<p class="formula">Profit = item price + shipping charged - platform fees - base cost - POD shipping - ad cost<br>Break-even price = (base cost + POD shipping + ad cost + fixed fee) / (1 - fee %) - shipping charged</p>
<h2>A worked example</h2>
<p>A t-shirt sells on Etsy for $25 plus $5 shipping. The buyer pays $30.00, so Etsy's fees are $3.30. The provider charges $12.50 for the shirt and $4.75 to ship it. Profit is <strong>$9.45</strong> per sale, 31.5% of what the buyer paid. The break-even item price is <strong>$14.56</strong>: below that, every sale loses money.</p>
<p>Now add ads. If you spend $6.00 in ads for each sale, profit drops to $3.45, and the break-even price jumps to $21.19. Track ad spend per sale, not per day, or you won't see this happen.</p>
<p>The same shirt on Shopify Basic costs $1.17 in card fees, for $11.58 profit and a $13.07 break-even, but you pay the monthly plan and you bring your own traffic.</p>
<h2>The shipping gap</h2>
<p>Many POD sellers charge less shipping than the provider bills them, or offer free shipping, and forget to put the difference into the item price. Moving shipping into the price doesn't change the fee, since Etsy charges on the total either way: $30 with free shipping and $25 + $5 shipping both leave $9.45. What loses money is charging $3 shipping on a $4.75 label without raising the price. The calculator flags that gap.</p>""",
    faqs=[
        ("How much profit do you make on print on demand?", "It depends almost entirely on your price. A $25 shirt with $5 shipping, a $12.50 base cost and $4.75 provider shipping makes $9.45 on Etsy before ads. At $6.00 of ad spend per sale it makes $3.45."),
        ("What is the lowest price I can charge?", "Add base cost, provider shipping, ad cost per sale and the platform's fixed fee, divide by 1 minus the platform's percentage, and subtract the shipping you charge. For the example shirt on Etsy that is $14.56."),
        ("Should I offer free shipping on print on demand products?", "You can, as long as you add the shipping to the item price. Etsy's fees apply to the order total either way, so a $30 shirt with free shipping makes the same $9.45 as a $25 shirt with $5 shipping."),
        ("Is Shopify cheaper than Etsy for print on demand?", "Per sale, yes: $1.17 in card fees against $3.30 on Etsy for a $30 order. But Shopify adds a monthly plan fee and no marketplace traffic, so you usually pay for visitors with ads instead. Put that ad spend per sale in the calculator to compare honestly."),
    ],
    related=["etsy-fee-calculator", "etsy-profit-calculator", "etsy-free-shipping-calculator", "roas-calculator", "break-even-calculator", "shopify-fee-calculator"],
    og_image="pins/pin-12.png",
    tests=[
        {"expect": {"big": "$9.45", "rows": ["$30.00", "-$3.30", "-$12.50", "-$4.75", "$9.45", "31.5%", "$14.56"], "verdict": "$14.56"}},
        {"set": {"ad": "6"}, "expect": {"big": "$3.45", "rows": ["-$6.00", "$21.19"], "verdict": "under 15%"}},
        {"set": {"plat": "shop"}, "expect": {"rows": ["-$1.17", "$11.58", "$13.07"]}},
        {"set": {"pr": "30", "sb": "0"}, "expect": {"big": "$9.45", "rows": "$30.00"}},
        {"set": {"sb": "3"}, "expect": {"rows": ["$28.00", "-$3.11", "$7.64"], "verdict": "$1.75 less"}},
        {"set": {"pr": "11"}, "expect": {"big": "-$3.22", "verdict": ["loses $3.22", "$14.56"]}},
        {"set": {"pr": "0", "sb": "0"}, "expect": {"big": "-$17.25", "verdict": ["Enter your sale price", "$19.56"]}},
    ],
)
