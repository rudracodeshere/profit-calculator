PAGE = dict(
    slug="etsy-sale-calculator",
    cat="Etsy tools",
    nav_name="Etsy sale & coupon calculator",
    title="Etsy Sale Calculator: Profit After a Discount or Coupon",
    desc="See what an Etsy sale or coupon really costs: profit at full and sale price after fees, extra sales needed, and the biggest discount you can afford.",
    h1="Etsy sale calculator: can you afford that discount?",
    lead="A 25% sale doesn't cut your profit by 25%. It cuts it by much more, because your costs stay the same. Enter a listing and a discount to see profit at full price and on sale, how many extra orders the sale needs to pay for itself, and the deepest discount before every sale loses money.",
    form="""      <label for="price">Item price before the discount</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <label for="disc">Discount (sale or coupon)</label>
      <div class="in"><input id="disc" type="number" inputmode="decimal" min="0" max="100" step="1" value="25"><span>% off</span></div>
      <label for="ship">Shipping you charge <small>(not discounted)</small></label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="mat">Materials + packaging</label>
      <div class="in"><span>$</span><input id="mat" type="number" inputmode="decimal" min="0" step="0.01" value="12"></div>
      <label for="label">Shipping label you pay</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <label for="units">Sales you'd make at full price in the same period</label>
      <div class="in"><input id="units" type="number" inputmode="decimal" min="0" step="1" value="20"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="lfee">Listing fee per item sold</label>
      <div class="in"><span>$</span><input id="lfee" type="number" min="0" step="0.01" value="0.20"></div>
      </details>""",
    out="""<div class="big"><span>Sales needed to earn the same profit</span><b id="need"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var p=n('price'),s=n('ship'),d=Math.min(n('disc'),100)/100,c=n('mat')+n('label'),N=n('units');
  var rate=(n('tx')+n('pp'))/100,fix=n('pf')+n('lfee');
  function keep(x){return x+s-(x+s)*rate-fix-c}
  if(!p){$('need').textContent='-';setRows([]);verdict(false,'Enter the item price to see what a discount costs.');return}
  var ps=p*(1-d),kf=keep(p),ks=keep(ps),pmin=(c+fix)/(1-rate)-s,dmax=1-pmin/p;
  var r=[['Full price: you keep',m(kf)],['Sale price ('+pc(d,0)+' off)',m(ps)],['On sale: you keep',m(ks)],['Profit lost per sale',m(ks-kf)+(kf>0?' ('+pc((kf-ks)/kf,0)+')':'')]];
  if(N)r.push([Math.round(N)+' full-price sales earn',m(N*kf)]);
  r.push(['Deepest discount before a loss',pmin<=0?'any':(dmax<=0?'none':pc(dmax)+' ('+m(pmin)+')'),'total']);
  setRows(r);
  if(kf<=0){$('need').textContent='-';verdict(false,'This listing already loses '+m(-kf)+' per sale at full price. Fix the price before running a sale.');return}
  if(ks<=0){$('need').textContent='never';verdict(false,'At '+pc(d,0)+' off, every sale loses '+m(-ks)+'. No number of extra orders makes that up. Keep the discount under '+pc(Math.max(dmax,0),0)+'.');return}
  var ratio=kf/ks;
  if(N){var need=Math.ceil(N*ratio-1e-9);$('need').textContent=need+' sales';
    verdict(ratio<1.5,'You need '+need+' sales on sale to match '+Math.round(N)+' at full price, '+(need-Math.round(N))+' more ('+pc(ratio-1,0)+' more orders). '+(ratio<1.5?'A realistic bump for a well-timed sale.':'That is a big lift to ask of one sale. Try a smaller discount or a coupon for past buyers only.'));}
  else{$('need').textContent=pc(ratio-1,0)+' more';verdict(ratio<1.5,'The sale needs '+pc(ratio-1,0)+' more orders than usual just to earn the same profit.');}
}""",
    note="US Etsy rates as of October 2026: 6.5% transaction fee and 3% + $0.25 processing on what the buyer actually pays (discounted item + shipping), $0.20 listing fee per item sold. Etsy sales and coupons in Shop Manager discount the item price; this calculator leaves shipping at full price. Offsite Ads and sales tax are left out.",
    body="""<h2>Why a discount costs more than it looks</h2>
<p>Your materials, label and Etsy's flat fees don't go on sale. The whole discount comes out of your profit, and your profit is only a slice of the price. Etsy does charge its percentage fees on the discounted price, so you save a little there, but only 9.5 cents of every dollar you give away.</p>
<p class="formula">Profit on sale = (sale price + shipping) &times; (1 &minus; 9.5%) &minus; $0.45 &minus; materials &minus; label</p>
<p class="formula">Sales needed = full-price sales &times; full-price profit &divide; sale profit</p>
<h2>Worked example</h2>
<p>A $40 item with free shipping, $12 in materials and a $5 label. At full price you keep <strong>$18.75</strong>. At 25% off the buyer pays $30.00 and you keep <strong>$9.70</strong>, which is 48% less profit from a 25% discount.</p>
<p>If you'd normally sell 20 in a month ($375.00 profit), the sale has to sell <strong>39</strong> to earn the same. A 10% discount leaves $15.13 per sale and needs 25 sales. The deepest discount this item can take before each sale loses money is <strong>51.8%</strong>, a price of $19.28. At 60% off, every sale loses $2.97.</p>
<h2>When a sale is still worth it</h2>
<p><strong>Clearing old stock.</strong> If the materials are already paid for and the item isn't selling, profit at a lower price beats none. Treat the materials as spent and judge the sale on fees and the label alone.</p>
<p><strong>Targeted coupons.</strong> Etsy lets you send coupons to buyers who favorited an item or abandoned a cart. Those go to people already close to buying, so you give away the discount on fewer orders than a shop-wide sale.</p>
<p><strong>Big sale events.</strong> When Etsy runs a site-wide event, the extra traffic may supply the extra orders. Use the "sales needed" number as the target and compare it to last year's event if you have one.</p>
<p>A sale is easy to judge on one listing. Across a whole shop with mixed prices it's harder, which is where a per-product breakdown of your sales export helps.</p>""",
    faqs=[
        ("Does Etsy charge fees on the original price or the sale price?", "On the sale price. The 6.5% transaction fee and 3% processing are charged on what the buyer actually pays. On a $40 item at 25% off, the fees are on $30.00."),
        ("How many more sales do I need to make up for a discount?", "Divide your full-price profit by your sale profit. For the $40 example at 25% off that is $18.75 &divide; $9.70, so 20 normal sales become 39 needed on sale."),
        ("What's the biggest discount I can offer on Etsy without losing money?", "Your break-even price is (materials + label + $0.45) &divide; 0.905, minus any shipping you charge. For $17 of costs that is $19.28, so a $40 item can go to 51.8% off before it loses money, and that leaves you nothing at all."),
        ("Is a coupon better than a sale on Etsy?", "The math per order is the same. The difference is who gets the discount: a sale goes to every buyer, including people who would have paid full price, while a targeted coupon only reaches the shoppers you choose."),
    ],
    related=["etsy-fee-calculator", "etsy-profit-calculator", "etsy-free-shipping-calculator", "break-even-calculator", "price-increase-calculator", "profit-margin-calculator"],
    og_image="pins/pin-04.png",
    tests=[
        {"expect": {"need": ["39 sales"], "rows": ["$18.75", "$30.00", "$9.70", "-$9.05", "48%", "$375.00", "51.8%", "$19.28"], "verdict": ["19 more"]}},
        {"set": {"disc": "10"}, "expect": {"need": ["25 sales"], "rows": ["$15.13"]}},
        {"set": {"disc": "60"}, "expect": {"need": ["never"], "verdict": ["loses $2.97"]}},
        {"set": {"price": "20", "ship": "4", "mat": "5", "label": "4", "disc": "20", "units": "30"}, "expect": {"need": ["43 sales"], "rows": ["$12.27", "$8.65", "67.8%"]}},
        {"set": {"price": ""}, "expect": {"verdict": ["Enter the item price"]}},
    ],
)
