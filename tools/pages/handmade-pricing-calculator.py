PAGE = dict(
    slug="handmade-pricing-calculator",
    cat="Maker pricing",
    nav_name="Handmade pricing calculator",
    title="Handmade Pricing Calculator: Cost, Wholesale and Retail Price",
    desc="Price handmade items from materials, your time and overhead. Get base cost, wholesale and retail prices, then see what you keep after Etsy or Shopify fees.",
    h1="Handmade pricing calculator",
    lead="Enter what one item costs you in materials, how long it takes and what your time is worth. You get a base cost, a wholesale price and a retail price, then a check of what you actually keep at that retail price after platform fees.",
    form="""      <label for="mat">Materials per item <small>(supplies, packaging)</small></label>
      <div class="in"><span>$</span><input id="mat" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="mins">Time to make one</label>
      <div class="in"><input id="mins" type="number" inputmode="decimal" min="0" step="1" value="30"><span>minutes</span></div>
      <label for="rate">Your hourly rate</label>
      <div class="in"><span>$</span><input id="rate" type="number" inputmode="decimal" min="0" step="0.5" value="20"><span>/ hour</span></div>
      <label for="ovh">Overhead per item <small>(monthly tools, software, rent / items made)</small></label>
      <div class="in"><span>$</span><input id="ovh" type="number" inputmode="decimal" min="0" step="0.01" value="1.50"></div>
      <label for="wm">Wholesale multiplier <small>(x base cost)</small></label>
      <div class="in"><input id="wm" type="number" inputmode="decimal" min="0" step="0.1" value="2"><span>x</span></div>
      <label for="rm">Retail multiplier <small>(x wholesale)</small></label>
      <div class="in"><input id="rm" type="number" inputmode="decimal" min="0" step="0.1" value="2"><span>x</span></div>
      <label for="plat">Where you sell at retail</label>
      <select id="plat" class="full">
        <option value="etsy">Etsy (6.5% + 3% + $0.25 + $0.20)</option>
        <option value="shop">Shopify Basic (2.9% + $0.30)</option>
        <option value="own">Your own site or in person</option>
      </select>
      <details><summary class="note">Edit fee rates</summary>
      <label for="etx">Etsy transaction fee</label>
      <div class="in"><input id="etx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="epp">Etsy payment processing</label>
      <div class="in"><input id="epp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="epf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="elf">Etsy listing fee per item sold</label>
      <div class="in"><span>$</span><input id="elf" type="number" min="0" step="0.01" value="0.20"></div>
      <label for="spp">Shopify Payments card rate</label>
      <div class="in"><input id="spp" type="number" min="0" step="0.1" value="2.9"><span>% +</span><span>$</span><input id="spf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="opp">Own site or in-person card fee <small>(0 for cash)</small></label>
      <div class="in"><input id="opp" type="number" min="0" step="0.1" value="0"><span>% +</span><span>$</span><input id="opf" type="number" min="0" step="0.01" value="0"></div>
      </details>""",
    out="""<div class="big"><span>Retail price</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var lab=n('mins')/60*n('rate'),cost=n('mat')+lab+n('ovh');
  var ws=cost*n('wm'),rt=ws*n('rm'),pl=$('plat').value,fees,name;
  if(pl==='etsy'){fees=rt*(n('etx')+n('epp'))/100+n('epf')+n('elf');name='Etsy fees';}
  else if(pl==='shop'){fees=rt*n('spp')/100+n('spf');name='Shopify Payments fee';}
  else{fees=rt*n('opp')/100+n('opf');name='Card fees';}
  var keep=rt-fees,prof=keep-cost;
  $('big').textContent=m(rt);
  setRows([['Materials',m(n('mat'))],['Your time ('+n('mins')+' min at '+m(n('rate'))+'/hr)',m(lab)],['Overhead',m(n('ovh'))],['Base cost',m(cost),'total'],
    ['Wholesale price ('+n('wm')+'x cost)',m(ws)],['Wholesale profit',m(ws-cost)],['Retail price ('+n('rm')+'x wholesale)',m(rt)],
    [name+' at retail',m(-fees)],['You keep after fees',m(keep)],['Profit beyond your wage and costs',m(prof),'total']]);
  if(!cost){verdict(false,'Enter your materials, time and hourly rate to get a price.');return}
  if(prof<0)verdict(false,'At '+m(rt)+' the '+name.toLowerCase()+' ('+m(fees)+') eat into your own wage: you are paid '+m(lab+prof)+' instead of '+m(lab)+'. Raise the retail multiplier.');
  else verdict(true,'At '+m(rt)+' you keep '+m(keep)+' after '+m(fees)+' in fees. That pays your '+m(lab)+' wage and costs, with '+m(prof)+' left as profit.');
}""",
    note="Fee defaults are US rates as of October 2026: Etsy 6.5% transaction + 3% + $0.25 processing + $0.20 listing per item sold; Shopify Basic 2.9% + $0.30 with Shopify Payments (plus the $39 monthly plan, not included here). Fees are on the item price only; shipping and sales tax are left out. Edit any rate above.",
    body="""<h2>How the formula works</h2>
<p>Handmade pricing starts from your <strong>base cost</strong>: everything one item uses up, including your time. Materials are the obvious part. Labor is minutes times an hourly rate you would actually accept. Overhead is the monthly stuff that isn't in any one item (tools, software, studio rent, the craft fair table) divided by how many items you make in a month.</p>
<p class="formula">Base cost = materials + (minutes / 60 x hourly rate) + overhead per item<br>Wholesale = base cost x 2 &nbsp;|&nbsp; Retail = wholesale x 2</p>
<p>The first doubling is your profit as a business, separate from your wage. The second doubling is the shop's margin when a store buys from you wholesale. If you sell direct, that second half pays for the selling: platform fees, photos, customer messages and the items that don't sell.</p>
<h2>A worked example</h2>
<p>A set of handmade soap dishes uses $6 of clay and glaze and takes 30 minutes. At $20 an hour, your time is $10.00. Add $1.50 of overhead and the base cost is <strong>$17.50</strong>. Double it for a wholesale price of <strong>$35.00</strong> ($17.50 profit per piece to a shop). Double again for retail: <strong>$70.00</strong>.</p>
<p>Sold on Etsy at $70.00, the fees are $7.10, so you keep <strong>$62.90</strong>. After your $17.50 base cost, $45.40 is profit on top of your wage. On Shopify Basic the per-sale fee is $2.33 and the profit is $50.17, but the monthly plan fee comes out of that, so it only wins once you have enough sales.</p>
<h2>When the numbers look too high</h2>
<p>If the retail price feels steep, don't cut your hourly rate first. Look at the time instead: batching steps, making in larger runs and simplifying the design all lower the base cost without paying yourself less. If you will never sell wholesale, you can price retail lower than 4x cost, but keep the gap. The fees, the free shipping you build into the price and the occasional sale all come out of it.</p>
<p>For the time you actually earn per hour across all your orders, use the <a href="../etsy-hourly-wage-calculator/">Etsy hourly wage calculator</a>.</p>""",
    faqs=[
        ("How do you calculate the price of a handmade item?", "Add materials, your time at an hourly rate and a share of overhead to get the base cost. Double it for wholesale and double again for retail. With $6 materials, 30 minutes at $20 an hour and $1.50 overhead, that is $17.50, then $35.00 wholesale and $70.00 retail."),
        ("Should I include my labor in the cost?", "Yes. If your time is not in the base cost, the profit you see is really your wage, and you can't tell whether a product is worth making. Pay yourself in the cost, then the multiplier is profit on top."),
        ("How do I work out overhead per item?", "Add up the monthly costs that aren't in any one product (tools, software, rent, booth fees) and divide by how many items you make in a month. $60 a month over 40 items is $1.50 per item."),
        ("Do I need a wholesale price if I only sell on Etsy?", "It helps. Pricing retail at twice wholesale means a shop can stock you later without you underpricing yourself, and it leaves room for Etsy's fees, which take $7.10 of a $70.00 sale."),
    ],
    related=["wholesale-price-calculator", "etsy-pricing-calculator", "etsy-hourly-wage-calculator", "candle-pricing-calculator", "jewelry-pricing-calculator", "markup-calculator"],
    og_image="pins/pin-08.png",
    tests=[
        {"expect": {"big": "$70.00", "rows": ["$6.00", "$10.00", "$1.50", "$17.50", "$35.00", "$70.00", "-$7.10", "$62.90", "$45.40"], "verdict": "$45.40"}},
        {"set": {"plat": "shop"}, "expect": {"rows": ["-$2.33", "$67.67", "$50.17"]}},
        {"set": {"plat": "own"}, "expect": {"rows": ["$70.00", "$52.50"]}},
        {"set": {"wm": "1", "rm": "1"}, "expect": {"big": "$17.50", "verdict": "Raise the retail multiplier"}},
        {"set": {"mat": "0", "mins": "0", "ovh": "0"}, "expect": {"big": "$0.00", "verdict": "Enter your materials"}},
    ],
)
