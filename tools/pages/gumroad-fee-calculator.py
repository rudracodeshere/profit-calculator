PAGE = dict(
    slug="gumroad-fee-calculator",
    cat="Platform fees",
    nav_name="Gumroad fee calculator",
    title="Gumroad Fee Calculator 2026: Direct Sales vs Discover",
    desc="Free Gumroad fee calculator. Compare what you keep from a direct sale (10% + $0.50 plus card processing) and a Discover marketplace sale (30%) at any price.",
    h1="Gumroad fee calculator",
    lead="Enter your product's price. You see what you keep when a buyer comes through your own link or profile, next to what you keep when the sale comes from Gumroad Discover, plus the price below which the fixed fees take a painful share.",
    form="""      <label for="price">Product price</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="10"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="gp">Gumroad fee on direct sales</label>
      <div class="in"><input id="gp" type="number" min="0" step="0.1" value="10"><span>% +</span><span>$</span><input id="gf" type="number" min="0" step="0.01" value="0.50"></div>
      <label for="pp">Card processing on direct sales</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="2.9"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="dp">Discover marketplace fee <small>(includes processing)</small></label>
      <div class="in"><input id="dp" type="number" min="0" step="1" value="30"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>You keep from a direct sale</span><b id="keep"></b></div>
      <table class="wide" aria-live="polite"><thead><tr><th></th><th>Direct</th><th>Discover</th></tr></thead><tbody id="cmp"></tbody></table>
      <p id="cross" class="note"></p>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var P=n('price'),gp=n('gp')/100,gf=n('gf'),pp=n('pp')/100,pf=n('pf'),dp=n('dp')/100,fx=gf+pf,dr=gp+pp;
  var cross=dp>dr?fx/(dp-dr):0;
  $('cross').textContent=(cross?'Below '+m(cross)+', a Discover sale costs you less in fees than a direct one, because the '+m(fx)+' of fixed fees outweighs the higher percentage. ':'With these rates a direct sale is always cheaper. ')+'The fixed fees are more than 10% of the price below '+m(fx/0.1)+'.';
  if(!P){$('keep').textContent='-';$('cmp').innerHTML='<tr><td colspan="3">Enter a price to compare.</td></tr>';verdict(false,'No price entered yet.');return}
  var g=P*gp+gf,pr=P*pp+pf,d=g+pr,ds=P*dp;
  function row(a,b,c,cls){return '<tr'+(cls?' class="'+cls+'"':'')+'><td>'+a+'</td><td>'+b+'</td><td>'+c+'</td></tr>'}
  $('cmp').innerHTML=row('Price',m(P),m(P))+row('Gumroad fee',m(-g),m(-ds))+row('Card processing',m(-pr),'incl.')+
    row('Total fees',m(-d),m(-ds))+row('Fees as % of price',pc(d/P),pc(dp))+row('Fixed part ('+m(fx)+')',pc(fx/P),'-')+row('You keep',m(P-d),m(P-ds),'total');
  $('keep').textContent=m(P-d);
  if(P-d<=0)verdict(false,'At '+m(P)+' the fixed fees take the whole direct sale. Price higher or sell it in a bundle.');
  else if(fx/P>0.1)verdict(false,'The '+m(fx)+' fixed fees alone are '+pc(fx/P)+' of this price. A bundle or a higher price keeps more of each sale.');
  else verdict(true,'A direct sale keeps '+m(P-d)+', '+m((P-d)-(P-ds))+' more than a Discover sale. Send buyers to your own link where you can.');
}""",
    note="Gumroad rates as of October 2026: 10% + $0.50 per direct sale (your own link or profile) and 30% on sales through the Discover marketplace. Several third-party summaries report that card processing (about 2.9% + $0.30) is deducted on top of the 10% for direct sales, while the 30% Discover fee includes it; Gumroad has changed its pricing several times, so check Gumroad's pricing page and adjust the rates here. Sales tax and VAT that Gumroad collects are left out.",
    body="""<h2>Two fee schedules, depending on where the buyer came from</h2>
<p><strong>Direct sales.</strong> When a buyer comes through your own link, your profile, an embed or your email list, Gumroad charges 10% of the price plus $0.50. Third-party summaries of Gumroad's pricing report that card processing, roughly 2.9% + $0.30, is taken on top of that. Check Gumroad's pricing page for the current terms; every rate here is editable.</p>
<p><strong>Discover sales.</strong> When the buyer finds you through Gumroad's own marketplace, Gumroad takes a flat 30%, which already covers processing.</p>
<p class="formula">Direct fees = price x 12.9% + $0.80 &nbsp;|&nbsp; Discover fees = price x 30%</p>
<p>Example: a $10 template. A direct sale costs $1.50 in Gumroad fees and $0.59 in processing, $2.09 in total or 20.9%, so you keep $7.91. A Discover sale costs $3.00 and you keep $7.00.</p>
<h2>Where the fixed $0.50 starts to matter</h2>
<p>The 30% Discover fee sounds expensive, but it has no fixed part. A direct sale carries $0.80 of fixed fees ($0.50 to Gumroad and $0.30 to processing) whatever the price. At $10 that fixed part is 8.0% of the price. Below $8.00 it is more than 10%.</p>
<p>Below $4.68, a Discover sale actually costs you less than a direct sale. On a $3 product, a direct sale keeps $1.81 (fees take 39.6%) while a Discover sale keeps $2.10. On a $1 product a direct sale keeps just $0.07, against $0.70 from Discover.</p>
<p>If you sell low-priced items through your own audience, bundling several into one product, or setting a pay-what-you-want minimum around $5, keeps the fixed fee from swallowing each sale.</p>""",
    faqs=[
        ("How much does Gumroad take from a $10 sale?", "On a direct sale, $1.50 in Gumroad fees (10% + $0.50) plus about $0.59 in card processing, so you keep $7.91. On a Discover sale Gumroad takes 30%, $3.00, and you keep $7.00."),
        ("Does Gumroad charge payment processing on top of its fee?", "Third-party summaries say yes for direct sales: about 2.9% + $0.30 on top of the 10% + $0.50. Discover's 30% is reported to include processing. Check Gumroad's pricing page, and edit the rates here if your payouts show something different."),
        ("Is Gumroad worth it for cheap products?", "The fixed fees hurt. A $1 product sold directly keeps about $0.07 after fees. Below $4.68 you keep more from a Discover sale than a direct one, so for low prices, bundles work better."),
        ("Is it better to get sales from Discover or my own link?", "Above $4.68, your own link keeps more per sale: $0.91 more at $10. Discover is still worth having as extra sales you wouldn't otherwise get."),
    ],
    related=["etsy-digital-download-calculator", "paypal-fee-calculator", "stripe-fee-calculator", "etsy-fee-calculator", "profit-margin-calculator"],
    og_image="pins/pin-07.png",
    tests=[
        {"expect": {"cmp": ["$10.00", "-$1.50", "-$0.59", "-$2.09", "20.9%", "8.0%", "$7.91", "-$3.00", "$7.00"], "keep": "$7.91", "cross": ["$4.68", "$8.00", "$0.80"], "verdict": "$0.91 more"}},
        {"set": {"price": "3"}, "expect": {"cmp": ["$1.81", "39.6%", "$2.10"]}},
        {"set": {"price": "1"}, "expect": {"cmp": ["$0.07", "$0.70"]}},
        {"set": {"price": ""}, "expect": {"keep": "-", "verdict": "No price"}},
        {"set": {"price": "0.5"}, "expect": {"verdict": "take the whole direct sale"}},
    ],
)
