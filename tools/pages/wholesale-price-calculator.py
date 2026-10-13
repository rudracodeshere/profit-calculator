PAGE = dict(
    slug="wholesale-price-calculator",
    cat="Maker pricing",
    nav_name="Wholesale price calculator",
    title="Wholesale Price Calculator: Keystone, Margin and Consignment",
    desc="Turn a retail price into a wholesale price (keystone 50% or your own %), see your margin and minimum order value, and compare it with a consignment split.",
    h1="Wholesale price calculator",
    lead="Start from the retail price a shop will put on your product. You get the wholesale price, your profit and margin per unit, what a minimum order is worth, and how that compares with consignment and with selling it yourself.",
    form="""      <label for="rp">Retail price <small>(what the shop's customer pays)</small></label>
      <div class="in"><span>$</span><input id="rp" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <label for="wp">Wholesale as a share of retail <small>(50 = keystone)</small></label>
      <div class="in"><input id="wp" type="number" inputmode="decimal" min="0" max="100" step="1" value="50"><span>%</span></div>
      <label for="cost">Your cost per unit <small>(materials, labor, packaging)</small></label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="12"></div>
      <label for="moq">Minimum order quantity <small>(units per order)</small></label>
      <div class="in"><input id="moq" type="number" inputmode="decimal" min="0" step="1" value="24"><span>units</span></div>
      <label for="cs">Your share on consignment</label>
      <div class="in"><input id="cs" type="number" inputmode="decimal" min="0" max="100" step="1" value="60"><span>%</span></div>
      <details><summary class="note">Selling through a wholesale marketplace?</summary>
      <label for="cm">Marketplace commission on wholesale orders <small>(enter your platform's rate)</small></label>
      <div class="in"><input id="cm" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="0"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>Wholesale price per unit</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Same unit, three ways to sell it</h3>
      <table class="wide"><thead><tr><th>Channel</th><th>You get</th><th>Profit</th></tr></thead><tbody id="cmp"></tbody></table>""",
    js="""function calc(){
  var rp=n('rp'),wf=Math.min(n('wp'),100)/100,c=n('cost'),cf=Math.min(n('cm'),100)/100,q=Math.round(n('moq')),sh=Math.min(n('cs'),100)/100;
  var ws=rp*wf,com=ws*cf,rec=ws-com,pr=rec-c,mg=rec?pr/rec:0,cons=rp*sh;
  $('big').textContent=m(ws);
  var r=[['Wholesale price ('+pc(wf,0)+' of retail)',m(ws)]];
  if(cf)r.push(['Marketplace commission ('+pc(cf)+')',m(-com)],['You receive per unit',m(rec)]);
  r.push(['Your cost per unit',m(-c)],['Wholesale profit per unit',m(pr),'total'],['Wholesale margin',pc(mg)],
    ['Minimum order ('+q+' units)',m(rec*q)],['Profit on a minimum order',m(pr*q)]);
  setRows(r);
  $('cmp').innerHTML='<tr><td>Wholesale (paid on invoice)</td><td>'+m(rec)+'</td><td>'+m(pr)+'</td></tr>'+
    '<tr><td>Consignment '+pc(sh,0)+'/'+pc(1-sh,0)+' (paid when sold)</td><td>'+m(cons)+'</td><td>'+m(cons-c)+'</td></tr>'+
    '<tr><td>Selling it yourself (before fees)</td><td>'+m(rp)+'</td><td>'+m(rp-c)+'</td></tr>';
  if(!rp||!wf){verdict(false,'Enter the retail price and the wholesale share to see your wholesale price.');return}
  var need=(1-cf)>0?c/0.5/wf/(1-cf):0;
  if(mg<0.3)verdict(false,'Wholesale leaves you '+m(pr)+' a unit ('+pc(mg)+' margin). For a 50% margin on what you receive, the retail price needs to be '+m(need)+'.');
  else if(cons>rec)verdict(true,'Wholesale earns '+m(pr)+' a unit, paid up front. Consignment pays '+m(cons-rec)+' more per unit, but only once it sells, and unsold stock comes back to you.');
  else verdict(true,'Wholesale earns '+m(pr)+' a unit, paid up front, and pays at least as much as this consignment split. Prefer wholesale here.');
}""",
    note="Wholesale share, consignment split and marketplace commission are all inputs because they vary by shop and platform. Keystone (wholesale at 50% of retail) is a convention, not a rule. Payment card fees on wholesale invoices are not included. As of October 2026.",
    body="""<h2>From retail price to wholesale price</h2>
<p>Shops usually expect to buy at about half the retail price. That is <strong>keystone</strong> pricing: the shop doubles what it paid you, and the half it keeps covers rent, staff, the items that don't sell and its own profit. Some shops ask for a deeper discount, and makers with strong demand sometimes hold out for more than half. Change the share above to see your side of any offer.</p>
<p class="formula">Wholesale = retail x wholesale share &nbsp;|&nbsp; Wholesale margin = (wholesale - your cost) / wholesale</p>
<h2>A worked example</h2>
<p>A candle that retails for $40 wholesales at keystone for <strong>$20.00</strong>. If it costs you $12 to make, you earn $8.00 a unit, a <strong>40.0%</strong> margin. With a 24-unit minimum, each opening order is worth $480.00 and $192.00 of profit.</p>
<p>The same candle on a 60/40 consignment split pays you $24.00 when it sells, $12.00 of profit. That is $4.00 more per unit, but the shop pays only for what sells and returns the rest, often months later. Selling it yourself at $40 leaves $28.00 before platform fees and shipping.</p>
<h2>Minimum orders</h2>
<p>A minimum order protects you from small orders that cost more in packing and invoicing than they earn. You can set it as a unit count (24 units, or 6 of each design) or as a dollar opening minimum. Pick a number that still lets a small shop try you; a minimum worth a few hundred dollars is easier to say yes to than one worth a few thousand.</p>
<h2>Wholesale marketplaces</h2>
<p>Online wholesale marketplaces connect makers with independent shops and handle invoicing and payment terms. They charge the maker a commission on each order, and the rate can depend on whether the shop found you through the marketplace or through your own link. Enter the commission you are quoted in the box above: it comes out of your wholesale price, not the shop's, so it lowers your margin directly. With a 20% commission the $20.00 wholesale price pays you $16.00, and your margin drops to 25.0%.</p>""",
    faqs=[
        ("What is keystone pricing?", "Keystone pricing means the retail price is double the wholesale price, so wholesale is 50% of retail. A product that retails for $40 wholesales for $20.00."),
        ("How do I calculate wholesale price from my cost?", "Work out your full cost per unit, including your time, and double it for a 50% wholesale margin. Then check the retail price is twice that. If your cost is $12, a 50% margin needs a $24 wholesale price and a $48 retail price. If the market won't pay that retail price, your cost is the problem, not the markup."),
        ("Is consignment better than wholesale?", "It pays more per unit (60% of a $40 retail price is $24.00, against $20.00 wholesale) but you carry all the risk: you are paid only when items sell, your stock sits in someone else's shop, and damaged or unsold pieces come back. Use it to get into a new shop, then move to wholesale once your products have a sales record there."),
        ("What margin should I make on wholesale?", "Aim for around 50% of the wholesale price as profit after your full cost, labor included. Below about 30% (the calculator flags it), a single return or reorder discount can wipe out the profit on an order."),
    ],
    related=["handmade-pricing-calculator", "markup-calculator", "profit-margin-calculator", "candle-pricing-calculator", "jewelry-pricing-calculator", "break-even-calculator"],
    og_image="pins/pin-09.png",
    tests=[
        {"expect": {"big": "$20.00", "rows": ["$20.00", "-$12.00", "$8.00", "40.0%", "$480.00", "$192.00"], "cmp": ["$24.00", "$12.00", "$40.00", "$28.00", "60%/40%"], "verdict": "$4.00 more"}},
        {"set": {"cm": "20"}, "expect": {"rows": ["-$4.00", "$16.00", "25.0%"], "verdict": "$60.00"}},
        {"set": {"cost": "25"}, "expect": {"rows": ["-$5.00"], "verdict": "$100.00"}},
        {"set": {"wp": "60"}, "expect": {"big": "$24.00", "rows": ["50.0%"], "verdict": "Prefer wholesale"}},
        {"set": {"cost": "12", "rp": "48", "wp": "50"}, "expect": {"big": "$24.00", "rows": ["50.0%"]}},
        {"set": {"rp": "0"}, "expect": {"big": "$0.00", "verdict": "Enter the retail price"}},
    ],
)
