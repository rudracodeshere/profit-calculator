PAGE = dict(
    slug="etsy-free-shipping-calculator",
    cat="Etsy tools", starter_line=True,
    nav_name="Etsy free shipping calculator",
    title="Etsy Free Shipping Calculator: New Price for the Same Profit",
    desc="Switching an Etsy listing to free shipping? See the price that keeps your profit the same, what you lose by absorbing part of the label, and the $35 rule.",
    h1="Etsy free shipping calculator: what should the new price be?",
    lead="You charge an item price plus shipping today and want to offer free shipping. Enter both. The calculator shows the new price that leaves your profit exactly where it is, and what you give up if you only add part of the shipping to the price. Both versions sit side by side.",
    form="""      <label for="price">Item price now</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="22"></div>
      <label for="ship">Shipping you charge now</label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="mat">Materials + packaging</label>
      <div class="in"><span>$</span><input id="mat" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="label">Shipping label you pay</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="5.50"></div>
      <label for="roll">Part of the shipping to add to the item price</label>
      <div class="in"><input id="roll" type="number" inputmode="decimal" min="0" max="100" step="5" value="100"><span>%</span></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="lfee">Listing fee per item sold</label>
      <div class="in"><span>$</span><input id="lfee" type="number" min="0" step="0.01" value="0.20"></div>
      </details>""",
    out="""<div class="big"><span>Free-shipping price for the same profit</span><b id="same"></b></div>
      <table class="wide" aria-live="polite"><thead><tr><th></th><th>Charge shipping</th><th>Free shipping</th></tr></thead><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function fees(t){return t*(n('tx')+n('pp'))/100+n('pf')+n('lfee')}
function calc(){
  var x=n('price'),y=n('ship'),c=n('mat')+n('label'),r=Math.min(n('roll'),100)/100;
  var t=x+y,p=x+y*r,f1=fees(t),f2=fees(p),k1=t-f1-c,k2=p-f2-c,d=k2-k1;
  $('same').textContent=m(t);
  var rows=[['Item price',m(x),m(p)],['Shipping charged',m(y),m(0)],['Buyer pays',m(t),m(p)],['Etsy fees',m(-f1),m(-f2)],['Materials + label',m(-c),m(-c)],['You keep',m(k1),m(k2)]];
  var h='';rows.forEach(function(a,i){h+='<tr'+(i==5?' class="total"':'')+'><td>'+a[0]+'</td><td>'+a[1]+'</td><td>'+a[2]+'</td></tr>'});
  $('rows').innerHTML=h;
  if(!t){verdict(false,'Enter your current item price and shipping to compare.');return}
  var q=Math.ceil(35/Math.max(p,0.01)),tip=p>=35?' At '+m(p)+' one item reaches $35, so every US order of it qualifies for the free shipping guarantee.':' At '+m(p)+' a US buyer needs '+q+' of these to reach $35.';
  if(d<-0.005)verdict(false,'Adding only '+pc(r,0)+' of the shipping costs you '+m(-d)+' per sale. Price it at '+m(t)+' to keep '+m(k1)+'.'+tip);
  else if(k2<0)verdict(false,'This listing loses '+m(-k2)+' per sale either way. Raise the price before changing shipping.');
  else verdict(true,'Same profit: list it at '+m(p)+' with free shipping. Etsy fees do not change because the buyer pays the same total.'+tip);
}""",
    note="US Etsy rates as of October 2026: 6.5% transaction fee and 3% + $0.25 processing on the order total (item + shipping), $0.20 listing fee per item sold. One item per order; Offsite Ads and sales tax left out. Etsy's US free shipping guarantee threshold is $35; check Shop Manager for the current terms in your country.",
    body="""<h2>Why the free-shipping price is just price plus shipping</h2>
<p>Etsy's transaction and processing fees are charged on the order total, and shipping is part of that total. Moving $6 from the shipping line into the item price leaves the order total, and every percentage fee on it, exactly where it was. So the free-shipping price that keeps your profit the same is simply what the buyer paid before.</p>
<p class="formula">Free-shipping price for the same profit = current item price + current shipping charge</p>
<p>That is why the result above usually matches your current total to the cent. It only changes if your fees aren't proportional to the order, which on Etsy they are, apart from the flat $0.25 and $0.20 that stay the same either way.</p>
<h2>Worked example</h2>
<p>A $22 print with $6 shipping, $8 in materials and a $5.50 label. The buyer pays $28.00, Etsy takes $3.11, and you keep <strong>$11.39</strong>. List it at <strong>$28.00</strong> with free shipping and you keep the same $11.39.</p>
<p>Many sellers worry $28 looks expensive and only add part of the shipping. For a $30 item with $8 shipping, $10 materials and a $7 label, adding half the shipping makes it $34.00. You keep $13.32 instead of $16.94, so each sale costs you <strong>$3.62</strong>. Try it in the calculator with 50% before deciding: the lost profit is the real price of the lower sticker.</p>
<h2>The $35 free shipping guarantee</h2>
<p>US shops can opt into Etsy's free shipping guarantee, which promises free shipping on US orders of $35 or more. Etsy gives listings from those shops priority in US search. Orders under $35 can still carry your normal shipping charge.</p>
<p>That creates two cases:</p>
<p><strong>Items priced $35 or more.</strong> Every order qualifies, so the label has to be inside the price. Use the full price-plus-shipping figure from the calculator.</p>
<p><strong>Items under $35.</strong> Single-item orders keep paying shipping. You only absorb the label when a buyer adds enough to cross $35. In the first example that is 2 items at $22. Because a combined label for two items usually costs less than two labels, the hit is often small, but check your heaviest items.</p>
<h2>Does free shipping sell more?</h2>
<p>In the US it helps search placement through the guarantee, and a single all-in price is easier to compare than price plus shipping. Whether it lifts your sales enough is something only your own numbers show. Change a handful of listings first and compare their views and orders over a month before converting the whole shop.</p>""",
    faqs=[
        ("How much should I raise my price for free shipping on Etsy?", "By the full shipping charge you're dropping. Etsy's fees are on the whole order, so a $22 item with $6 shipping becomes a $28.00 item with free shipping, and your profit stays at $11.39 in the example above."),
        ("Do I pay Etsy fees on free shipping?", "You pay them on the item price, which now includes the shipping cost. The fee total is the same as charging shipping separately: $3.11 on a $28.00 order either way."),
        ("What if I only add part of the shipping to my price?", "You absorb the rest, and it comes straight out of profit. In the $30 + $8 example, adding half the shipping costs $3.62 a sale."),
        ("Do I have to offer free shipping on Etsy?", "No. It is optional. US shops that guarantee free shipping on orders of $35 or more get a search boost, and orders under $35 can still be charged shipping."),
    ],
    related=["etsy-fee-calculator", "etsy-pricing-calculator", "etsy-profit-calculator", "etsy-sale-calculator", "price-increase-calculator"],
    og_image="pins/pin-03.png",
    tests=[
        {"expect": {"same": ["$28.00"], "rows": ["$22.00", "$28.00", "-$3.11", "-$13.50", "$11.39"], "verdict": ["Same profit", "needs 2 of these"]}},
        {"set": {"price": "30", "ship": "8", "mat": "10", "label": "7", "roll": "50"}, "expect": {"same": ["$38.00"], "rows": ["$34.00", "$16.94", "$13.32"], "verdict": ["costs you $3.62", "needs 2 of these"]}},
        {"set": {"price": "30", "ship": "8", "mat": "10", "label": "7"}, "expect": {"verdict": ["one item reaches $35"]}},
        {"set": {"price": "0", "ship": "0"}, "expect": {"verdict": ["Enter your current item price"]}},
    ],
)
