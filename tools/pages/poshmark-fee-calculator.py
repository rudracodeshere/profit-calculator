PAGE = dict(
    slug="poshmark-fee-calculator",
    cat="Platform fees",
    nav_name="Poshmark fee calculator",
    title="Poshmark Fee Calculator 2026: Earnings, Profit and the $15 Trap",
    desc="Free Poshmark fee calculator. See your earnings after the $2.95 or 20% fee, your profit after cost, and the listing price you need to earn a set amount.",
    h1="Poshmark fee calculator",
    lead="Enter a sale price to see Poshmark's fee, what you earn and your profit after what you paid for the item. Or enter what you want to earn and get the lowest listing price that gets you there, with the $15 fee threshold handled correctly.",
    form="""      <label for="price">Sale price</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="30"></div>
      <label for="cost">What you paid for the item</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="want">Amount you want to earn</label>
      <div class="in"><span>$</span><input id="want" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="flat">Flat fee on sales under the threshold</label>
      <div class="in"><span>$</span><input id="flat" type="number" min="0" step="0.01" value="2.95"></div>
      <label for="thr">Threshold</label>
      <div class="in"><span>$</span><input id="thr" type="number" min="0" step="0.01" value="15"></div>
      <label for="pct">Commission at or above the threshold</label>
      <div class="in"><input id="pct" type="number" min="0" step="1" value="20"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>You earn</span><b id="earn"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <h3>Price needed to earn a set amount</h3>
      <table><tbody id="rows2"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var Tc=Math.round(n('thr')*100),fl=Math.round(n('flat')*100),r=n('pct')/100,Pc=Math.round(n('price')*100);
  function fee(c){return c<Tc?fl:Math.round(c*r)}
  function earn(c){return c-fee(c)}
  function first(from,ok){var c=Math.max(Tc,from);for(var k=0;k<100000;k++,c++)if(ok(earn(c)))return c;return -1}
  var lowMax=Tc>=1?Tc-1-fl:-1,Wc=Math.round(n('want')*100);
  if(Wc){
    var c=[];if(Wc+fl<Tc)c.push(Wc+fl);
    if(r<1){var h=first(Math.floor(Wc/(1-r))-2,function(e){return e>=Wc});if(h>=0)c.push(h)}
    if(c.length){var best=Math.min.apply(null,c);
      setRows([['To earn '+m(Wc/100)+', list at',m(best/100),'total'],['Poshmark fee',m(-fee(best)/100)],['You earn',m(earn(best)/100)]],'rows2');}
    else setRows([['No price earns that with these rates.','']],'rows2');
  }else setRows([['Enter the amount you want to earn.','']],'rows2');
  if(!Pc){$('earn').textContent='-';setRows([['Enter a sale price.','']]);verdict(false,'No sale price entered yet.');return}
  var f=fee(Pc)/100,P=Pc/100,e=P-f,pr=e-n('cost');
  setRows([['Sale price',m(P)],[Pc<Tc?'Poshmark flat fee':'Poshmark fee ('+n('pct')+'%)',m(-f)+' ('+pc(f/P)+')'],['You earn',m(e)],['What you paid',m(-n('cost'))],['Profit',m(pr),'total']]);
  $('earn').textContent=m(e);
  if(Pc>=Tc&&r<1&&lowMax>0&&earn(Pc)<lowMax){
    var beat=first(Math.floor(lowMax/(1-r))-2,function(x){return x>lowMax});
    verdict(false,'Price trap: listing at '+m((Tc-1)/100)+' earns '+m(lowMax/100)+', more than '+m(e)+' at this price. You need '+m(beat/100)+' or more to beat it.');
  }else if(e<=0)verdict(false,'The '+m(fl/100)+' flat fee takes the whole sale. Bundle this with other items.');
  else if(pr<0)verdict(false,'This sale loses '+m(-pr)+' after what you paid for the item.');
  else verdict(true,'You keep '+m(e)+' and make '+m(pr)+' profit. Poshmark takes '+pc(f/P)+'.');
}""",
    note="US Poshmark fees as of October 2026: $2.95 flat on sales under $15, 20% on sales of $15 or more. The buyer pays shipping through the prepaid label, so it isn't part of your earnings. Rates differ in Canada and other markets and can change, so they are editable. The 20% fee is rounded to the nearest cent here; Poshmark's own rounding may differ by a cent.",
    body="""<h2>Poshmark's two-tier fee</h2>
<p>Poshmark keeps one fee per sale. Under $15, it is a flat $2.95. At $15 or more, it is 20% of the sale price. The buyer pays for shipping with Poshmark's prepaid label, so shipping doesn't come out of your earnings and isn't charged a fee.</p>
<p class="formula">Earnings = price - $2.95 (under $15) &nbsp;|&nbsp; Earnings = price x 0.80 ($15 and up)</p>
<p>Example: a top you paid $8 for sells for $30. Poshmark takes $6.00 and you earn $24.00, so your profit is $16.00.</p>
<h2>The $15 trap</h2>
<p>Because the fee switches from flat to percentage, earnings drop when you cross the threshold. A $14.99 sale earns $12.04. A $15.00 sale earns $12.00. Every price from $15.00 to $15.04 earns less than $14.99 does, and you need to list at $15.06 to earn more ($12.05). If your item is priced in that band, take it down to $14.99.</p>
<p>The flat fee also makes cheap items costly to sell. On a $5 item, the $2.95 fee is 59.0% of the sale and you earn $2.05. Bundles help, since the fee is charged once per order.</p>
<h2>Pricing backward from what you want to earn</h2>
<p>Divide by 0.8 when the result lands at $15 or above, otherwise add $2.95. To earn $25 you list at $31.25. To earn $10 you list at $12.95. The calculator picks whichever rule gives the lower price, so it never sends you into the gap just above $15. Remember offers: buyers expect to negotiate, so list a little above the price you actually need.</p>""",
    faqs=[
        ("How much does Poshmark take from a $30 sale?", "20%, or $6.00, so you earn $24.00. Shipping is paid by the buyer and isn't counted."),
        ("Is it better to price at $14.99 or $15 on Poshmark?", "$14.99. It earns $12.04 after the $2.95 flat fee, while $15.00 earns $12.00 after the 20% fee. You need $15.06 to earn more than you would at $14.99."),
        ("What should I list at to earn $25 on Poshmark?", "$31.25. Poshmark takes 20%, $6.25, and you keep $25.00."),
        ("Does Poshmark charge fees on shipping?", "No. The buyer pays for the prepaid shipping label and the fee is based on the sale price only."),
    ],
    related=["ebay-fee-calculator", "etsy-vs-ebay", "profit-margin-calculator", "markup-calculator", "price-increase-calculator"],
    og_image="pins/pin-08.png",
    tests=[
        {"expect": {"rows": ["$30.00", "-$6.00", "$24.00", "-$8.00", "$16.00"], "earn": "$24.00", "rows2": "$31.25"}},
        {"set": {"price": "14.99", "cost": "0", "want": "12.04"}, "expect": {"rows": "-$2.95", "earn": "$12.04", "rows2": ["$14.99", "$12.04"]}},
        {"set": {"price": "15", "cost": "0"}, "expect": {"rows": "-$3.00", "earn": "$12.00", "verdict": ["$14.99", "$12.04", "$15.06"]}},
        {"set": {"price": "15.04"}, "expect": {"verdict": "Price trap"}},
        {"set": {"price": "15.06", "cost": "0", "want": "12.05"}, "expect": {"earn": "$12.05", "rows2": "$15.06", "verdict": "You keep"}},
        {"set": {"want": "10", "price": "5", "cost": "0"}, "expect": {"rows2": "$12.95", "earn": "$2.05", "rows": "59.0%"}},
        {"set": {"want": "25"}, "expect": {"rows2": ["-$6.25", "$25.00"]}},
        {"set": {"price": "2", "want": ""}, "expect": {"verdict": "takes the whole sale", "rows2": "Enter the amount"}},
    ],
)
