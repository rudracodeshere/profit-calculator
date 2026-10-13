PAGE = dict(
    slug="markup-calculator",
    cat="Pricing & margins",
    nav_name="Markup calculator",
    title="Markup Calculator: Price From Cost, Plus a Markup to Margin Table",
    desc="Free markup calculator. Enter your cost and markup % to get the selling price and the real profit margin, with a markup to margin conversion table.",
    h1="Markup calculator",
    lead="Enter what a product costs you and the markup you want. You get the selling price, the profit per unit and the margin that markup actually gives you, plus a conversion table for common markups.",
    form="""      <label for="cost">Cost per unit <small>(product, materials, packaging)</small></label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="mk">Markup on cost</label>
      <div class="in"><input id="mk" type="number" inputmode="decimal" min="0" step="1" value="150"><span>%</span></div>
      <label for="tm">Margin you want <small>(to find the markup you need)</small></label>
      <div class="in"><input id="tm" type="number" inputmode="decimal" min="0" max="99" step="1" value="30"><span>%</span></div>""",
    out="""<div class="big"><span>Selling price</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Markup to margin</h3>
      <table class="wide"><thead><tr><th>Markup</th><th>Margin</th><th>Price</th></tr></thead><tbody id="conv"></tbody></table>""",
    js="""function calc(){
  var c=n('cost'),k=n('mk')/100,t=n('tm')/100,p=c*(1+k);
  var h='';[25,50,100,150,200,300].forEach(function(x){var r=x/100;h+='<tr><td>'+x+'%</td><td>'+pc(r/(1+r))+'</td><td>'+(c?m(c*(1+r)):'-')+'</td></tr>'});
  $('conv').innerHTML=h;
  var need=t<1?pc(t/(1-t)):'not possible';
  if(!c){$('big').textContent='-';setRows([['Markup needed for a '+pc(t)+' margin',need]]);verdict(false,'Enter your cost per unit to get a price.');return}
  var mg=k/(1+k);
  $('big').textContent=m(p);
  setRows([['Cost per unit',m(c)],['Markup ('+pc(k)+')',m(c*k)],['Selling price',m(p),'total'],['Profit margin',pc(mg)],['Price is this many times cost',(1+k).toFixed(2)+'x'],['Markup needed for a '+pc(t)+' margin',need]]);
  if(mg<0.3)verdict(false,'A '+pc(k)+' markup keeps only '+pc(mg)+' of the price. Marketplace fees of 10-15% would take a third or more of that.');
  else verdict(true,'A '+pc(k)+' markup gives a '+pc(mg)+' margin: '+m(c*k)+' of every '+m(p)+' sale is gross profit before fees and shipping.');
}""",
    note="Markup = profit / cost. Margin = profit / price. Gross figures only: marketplace fees, shipping labels and ads come out of the profit shown. Fee figures in the text are US rates as of October 2026.",
    body="""<h2>How markup works</h2>
<p>Markup is the amount you add on top of your cost, written as a percentage of that cost. A $8 product with a 150% markup gets $12 added, so it sells for <strong>$20.00</strong>. The $12 is gross profit, and it is <strong>60.0%</strong> of the price. That 60% is the margin.</p>
<p class="formula">Price = cost x (1 + markup) &nbsp;|&nbsp; Margin = markup / (1 + markup) &nbsp;|&nbsp; Markup = margin / (1 - margin)</p>
<p>Markup is easy to apply when you know your cost. Margin tells you how much of each sale you keep. Use markup to set the price and margin to judge it.</p>
<h2>Why a "2x markup" is not a 100% margin</h2>
<p>When people say they price at "2x" or "double cost", they mean the price is twice the cost. On a $8 item that is $16. The markup is 100%, because you added 100% of the cost. The margin is only <strong>50.0%</strong>, because the $8 profit is half of the $16 price.</p>
<p>The confusion runs the other way too. A 100% margin is impossible, since it would mean the product was free. And "3x cost" is a 200% markup, not 300%: a $8 item sells for $24.00 and the margin is 66.7%.</p>
<h2>Common markups for makers and resellers</h2>
<p>Doubling cost (100% markup, 50% margin) is often called keystone pricing in retail. Handmade sellers who also sell wholesale often double cost to get a wholesale price, then double again for retail. That is a 300% markup on cost, a $32.00 retail price on an $8 cost and a 75.0% margin, which leaves the shop selling it wholesale with its own 50%.</p>
<p>Whatever markup you choose, check it against your selling costs. Etsy's US fees take roughly 10-11% of a typical order and Amazon's referral fee is 15% in most categories. A 25% markup gives only a 20.0% margin, so fees alone would take half of it.</p>""",
    faqs=[
        ("What markup do I need for a 30% margin?", "42.9%. Divide the margin by 1 minus the margin: 0.30 / 0.70 = 0.429. On a $8 cost that is a price of about $11.43."),
        ("Is 100% markup the same as 2x?", "Yes. A 100% markup doubles the cost, so a $8 item sells for $16.00. The margin on that sale is 50.0%."),
        ("How do I convert markup to margin?", "Divide the markup by 1 plus the markup. A 150% markup is 1.5 / 2.5 = 60.0% margin. A 50% markup is 0.5 / 1.5 = 33.3%."),
        ("Should I use markup or margin to price?", "Either works if you are consistent. Markup is quicker when you start from cost. Margin is better for comparing products and for checking that fees and ads are covered, because they are charged as a share of the price."),
    ],
    related=["profit-margin-calculator", "wholesale-price-calculator", "handmade-pricing-calculator", "break-even-calculator", "etsy-pricing-calculator"],
    og_image="pins/pin-06.png",
    tests=[
        {"expect": {"big": "$20.00", "rows": ["$12.00", "60.0%", "2.50x", "42.9%"], "conv": ["20.0%", "33.3%", "50.0%", "60.0%", "66.7%", "75.0%", "$16.00", "$24.00", "$32.00"]}},
        {"set": {"mk": "100"}, "expect": {"big": "$16.00", "rows": ["50.0%", "2.00x"]}},
        {"set": {"mk": "50"}, "expect": {"rows": ["33.3%"], "verdict": "33.3%"}},
        {"set": {"mk": "25"}, "expect": {"rows": ["20.0%"], "verdict": "only 20.0%"}},
        {"set": {"cost": "8", "mk": "42.857"}, "expect": {"big": "$11.43"}},
        {"set": {"cost": "0"}, "expect": {"big": "-", "verdict": "Enter your cost", "conv": "75.0%"}},
        {"set": {"tm": "100"}, "expect": {"rows": "not possible"}},
    ],
)
