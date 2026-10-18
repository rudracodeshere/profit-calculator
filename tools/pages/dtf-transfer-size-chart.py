PAGE = dict(
    gig="pod",
    cta_head=None,
    store_url="https://quietprofitsheets.gumroad.com/l/seller-profit-sheet?utm_source=calculator&amp;utm_content=dtf-transfer-size-chart",  # no product box on this page, so the footer link goes to a product
    slug="dtf-transfer-size-chart",
    cat="Print & design sizes",
    nav_name="DTF transfer size chart and t-shirt design size calculator",
    title="DTF Transfer Size Chart and T-Shirt Design Size Calculator (Adult, Youth, Hoodie)",
    desc="Free DTF and t-shirt design size calculator. Pick the garment, shirt size and placement to get the print width and height in inches, the pixels your file needs at 300 DPI, and a printable size chart for shirts, hoodies, youth and toddler tees.",
    h1="DTF transfer size chart and t-shirt design size calculator",
    lead="Pick the garment, the shirt size and where the print goes. You get the width and height to print, the pixels your artwork needs at 300 DPI, and whether your file is big enough. The full chart for every garment is below, and there's a free printable PDF.",
    form="""      <label for="g">Garment</label>
      <select id="g" class="full"></select>
      <div id="szwrap"><label for="sz">Shirt size</label>
      <select id="sz" class="full"></select></div>
      <label for="pl">Placement</label>
      <select id="pl" class="full"></select>
      <label for="aw">Your artwork <small>(optional, pixels)</small></label>
      <div class="in"><input id="aw" style="width:0" type="number" inputmode="numeric" min="0" step="1" placeholder="width"><span>&times;</span><input id="ah" style="width:0" type="number" inputmode="numeric" min="0" step="1" placeholder="height"><span>px</span></div>""",
    out="""<div class="big"><span>Print it at</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""var AD={XS:[8.5,9.5],S:[9.5,10.5],M:[10.5,11],L:[11,11],XL:[11,11.5],'2XL':[11.5,12],'3XL':[12,12.5],'4XL':[12.5,13],'5XL':[13,13.5],'6XL':[13.5,14]};
var YO={'XS (4-5)':[8,9],'S (6-8)':[9,9.5],'M (10-12)':[9.5,10.5],'L (14-16)':[10.5,11],'XL (18-20)':[11,11.5]};
var G={
 'Adult t-shirt or polo':{sz:AD,pl:{'Full front':[10,11.5,11,13,1],'Full back':[11,12.5,14,16,1],'Left chest':[3.5,4,3.5,4],'Back collar (tag)':[2.5,3,2.5,3],'Short sleeve':[3,4,2,3.5],'Long sleeve, down the arm':[2,2,14,18]}},
 'Oversized t-shirt':{pl:{'Full front':[12.5,14,14,16],'Full back':[13,15,15,18]}},
 'Pullover hoodie':{pl:{'Full front (above the pocket)':[10,11.5,11,13],'Front chest strip (above the pocket)':[9,10,4,5],'Full back':[13,15,16,18],'Left chest':[3.5,4,3.5,4]}},
 'Zip-up hoodie':{pl:{'Full back':[11,13.5,14,16],'Left or right chest (each side)':[3.5,4,3.5,4]}},
 'Crewneck sweatshirt':{pl:{'Front or back center':[11,12.5,11,13]}},
 'Tank top':{pl:{'Full front':[9,10,12,14]}},
 'Youth t-shirt':{sz:YO,pl:{'Full front':[8,9,9,11,1],'Full back':[10,11,11,13,1],'Left chest':[2.5,3,2.5,3],'Sleeve':[2,3,2,3]}},
 'Toddler t-shirt (2T-4T)':{pl:{'Full front':[6,7,6,8]}},
 'Infant onesie or tee (0-24M)':{pl:{'Upper chest':[4,5,4,5]}},
 'Tote bag':{pl:{'Front':[9,9,9,9]}},
 'Cap':{pl:{'Front panel':[3,4,2,2.5],'Back, above the strap':[3.5,3.5,1,1]}}
};
var opts=function(el,list,keep){var v=el.value,h='';list.forEach(function(k){h+='<option>'+k+'</option>'});el.innerHTML=h;if(keep&&list.indexOf(v)>=0)el.value=v};
var r1=function(x){return (Math.round(x*10)/10).toString()};
var rng=function(a,b){return a==b?r1(a)+'"':r1(a)+'" to '+r1(b)+'"'};
var built='';
opts($('g'),Object.keys(G));
function calc(){
  var gk=$('g').value,g=G[gk];
  if(built!=gk){opts($('pl'),Object.keys(g.pl),true);if(g.sz){opts($('sz'),Object.keys(g.sz),true);if(gk.indexOf('Adult')==0&&!$('sz').dataset.set){$('sz').value='L';$('sz').dataset.set=1}}built=gk}
  $('szwrap').style.display=g.sz?'':'none';
  var p=g.pl[$('pl').value],w0=p[0],w1=p[1],h0=p[2],h1=p[3];
  if(g.sz&&p[4]){var s=g.sz[$('sz').value];w0=s[0];w1=s[1]}
  var pw=(w0+w1)/2,ph=h1,aw=n('aw'),ah=n('ah'),fit=null;
  if(aw&&ah){var hh=pw*ah/aw;if(hh>h1){hh=h1;pw=h1*aw/ah}ph=hh;fit=aw/pw}
  $('big').textContent=r1(pw)+'" \\u00d7 '+r1(ph)+'"'+(aw&&ah?'':' max');
  var r=[['Width range',rng(w0,w1)],['Height range',rng(h0,h1)]];
  r.push(['Artwork for '+r1(pw)+'" wide at 300 DPI',Math.round(pw*300).toLocaleString('en-US')+' px wide']);
  if(aw&&ah){r.push(['Print size for your artwork',r1(pw)+'" \\u00d7 '+r1(ph)+'"']);r.push(['Your artwork prints at',Math.floor(fit)+' DPI'])}
  else r.push(['Largest artwork you need at 300 DPI',Math.round(w1*300).toLocaleString('en-US')+' \\u00d7 '+Math.round(h1*300).toLocaleString('en-US')+' px']);
  setRows(r);
  if(!(aw&&ah))verdict(true,'Print '+r1(pw)+'" wide and no taller than '+r1(h1)+'". Enter your artwork\\'s pixel size to check it is big enough.');
  else if(fit>=300)verdict(true,'Your file is big enough: it prints at '+Math.floor(fit)+' DPI at '+r1(pw)+'" \\u00d7 '+r1(ph)+'".');
  else if(fit>=200)verdict(true,'Usable: '+Math.floor(fit)+' DPI looks fine on fabric for most designs. For 300 DPI the artwork needs '+Math.round(pw*300).toLocaleString('en-US')+' px wide.');
  else verdict(false,'Too small: '+Math.floor(fit)+' DPI will look soft. Upscale the artwork to '+Math.round(pw*300).toLocaleString('en-US')+' px wide, or print it smaller.');
}""",
    note="Starting sizes compiled from published DTF sizing guides (Kingdom DTF for shirt and youth widths by size, xTool for placements and heights; checked October 2026). Garments vary by brand and cut, so lay the transfer on your actual blank before pressing. Nothing you type leaves your browser.",
    body="""<p><a class="btn" href="dtf-size-chart.pdf" download>Download the printable size chart (PDF)</a></p>
<h2>T-shirt design width by shirt size</h2>
<p>For full front and full back prints on adult tees, the width changes with the shirt size. If you print one design for every size, <strong>11 inches wide</strong> is the usual pick: it sits well on S to XL and still works on 2XL and 3XL.</p>
<table class="wide"><thead><tr><th>Adult size</th><th>Design width</th><th>Youth size</th><th>Design width</th></tr></thead><tbody>
<tr><td>XS</td><td>8.5" to 9.5"</td><td>XS (4-5)</td><td>8" to 9"</td></tr>
<tr><td>S</td><td>9.5" to 10.5"</td><td>S (6-8)</td><td>9" to 9.5"</td></tr>
<tr><td>M</td><td>10.5" to 11"</td><td>M (10-12)</td><td>9.5" to 10.5"</td></tr>
<tr><td>L</td><td>11"</td><td>L (14-16)</td><td>10.5" to 11"</td></tr>
<tr><td>XL</td><td>11" to 11.5"</td><td>XL (18-20)</td><td>11" to 11.5"</td></tr>
<tr><td>2XL</td><td>11.5" to 12"</td><td>Toddler 2T-4T</td><td>6" to 7"</td></tr>
<tr><td>3XL</td><td>12" to 12.5"</td><td>Infant 0-24M</td><td>4" to 5"</td></tr>
<tr><td>4XL</td><td>12.5" to 13"</td><td></td><td></td></tr>
<tr><td>5XL</td><td>13" to 13.5"</td><td></td><td></td></tr>
</tbody></table>
<h2>DTF size chart by placement</h2>
<table class="wide"><thead><tr><th>Garment and placement</th><th>Width</th><th>Height</th></tr></thead><tbody>
<tr><td>T-shirt full front</td><td>10" to 11.5"</td><td>11" to 13"</td></tr>
<tr><td>T-shirt full back</td><td>11" to 12.5"</td><td>14" to 16"</td></tr>
<tr><td>Left chest (adult)</td><td>3.5" to 4"</td><td>3.5" to 4"</td></tr>
<tr><td>Back collar (tag)</td><td>2.5" to 3"</td><td>2.5" to 3"</td></tr>
<tr><td>Short sleeve</td><td>3" to 4"</td><td>2" to 3.5"</td></tr>
<tr><td>Long sleeve, down the arm</td><td>2"</td><td>14" to 18"</td></tr>
<tr><td>Oversized tee front</td><td>12.5" to 14"</td><td>14" to 16"</td></tr>
<tr><td>Oversized tee back</td><td>13" to 15"</td><td>15" to 18"</td></tr>
<tr><td>Hoodie front, above the pocket</td><td>10" to 11.5"</td><td>11" to 13"</td></tr>
<tr><td>Hoodie back</td><td>13" to 15"</td><td>16" to 18"</td></tr>
<tr><td>Tank top front</td><td>9" to 10"</td><td>12" to 14"</td></tr>
<tr><td>Youth front</td><td>8" to 9"</td><td>9" to 11"</td></tr>
<tr><td>Youth left chest</td><td>2.5" to 3"</td><td>2.5" to 3"</td></tr>
<tr><td>Tote bag</td><td>9"</td><td>9"</td></tr>
<tr><td>Cap front</td><td>3" to 4"</td><td>2" to 2.5"</td></tr>
</tbody></table>
<h2>How big should the artwork file be?</h2>
<p class="formula">Pixels needed = print width (inches) &times; 300</p>
<p>An 11" wide front print needs a file <strong>3,300 pixels wide</strong> for 300 DPI. A typical 1024 &times; 1024 AI image printed at 11" comes out at 93 DPI and looks soft on a shirt, so upscale it first. 200 DPI is usually fine on fabric, since the weave hides fine detail, but 300 is the safe target for transfers and for print-on-demand uploads.</p>
<h2>Placement tips</h2>
<p>Width matters more than height: shirts stretch vertically, so a design that looks narrow on screen often looks right once pressed. On hoodies, measure above the pocket seam so the transfer doesn't fold into it. On onesies, keep the print short so it stays above the snaps. Print a paper test at full size and lay it on the blank when you're unsure.</p>
<p>Selling these on Etsy through print on demand? Printify, Printful and Gelato each give a print area per product. Make the file at least as many pixels as that area needs, and check the size with the <a href="../printable-wall-art-size-calculator/">print size and DPI calculator</a>.</p>""",
    faqs=[
        ("What size should a DTF transfer be for an adult t-shirt?", "10 to 11.5 inches wide for a full front, and 11 to 12.5 inches for a full back. If you make one size for every shirt, 11 inches wide is the common choice."),
        ("What size is a left chest DTF transfer?", "3.5 to 4 inches wide on adult shirts and hoodies, and 2.5 to 3 inches on youth shirts."),
        ("What size DTF for a toddler or infant shirt?", "Toddler (2T to 4T) fronts run 6 to 7 inches wide. Infant onesies and tees take 4 to 5 inches."),
        ("How many pixels does a t-shirt design need?", "Width in inches times 300. An 11 inch wide print needs 3,300 pixels wide, and a 12 &times; 16 inch back print needs 3,600 &times; 4,800."),
        ("What size is a DTF hoodie front?", "About 10 to 11.5 inches wide, kept above the pocket. A small strip above the pocket is 9 to 10 inches wide and 4 to 5 inches tall."),
    ],
    related=["printable-wall-art-size-calculator", "print-on-demand-profit-calculator", "etsy-title-tag-checker", "etsy-fee-calculator"],
    og_image="pins/pin-06.png",
    tests=[
        {"expect": {"big": ['11" × 13" max'], "rows": ["3,300 px wide", "3,300 × 3,900 px"]}},
        {"set": {"sz": "XS"}, "expect": {"big": ['9" × 13" max'], "rows": ['8.5" to 9.5"']}},
        {"set": {"pl": "Full back", "sz": "2XL"}, "expect": {"rows": ['11.5" to 12"', '14" to 16"']}},
        {"set": {"aw": "1024", "ah": "1024"}, "expect": {"big": ['11" × 11"'], "rows": ["93 DPI"], "verdict": ["Too small"]}},
        {"set": {"aw": "3300", "ah": "6600"}, "expect": {"big": ['6.5" × 13"'], "verdict": ["big enough"]}},
        {"set": {"g": "Toddler t-shirt (2T-4T)"}, "expect": {"big": ['6.5" × 8" max'], "rows": ['6" to 7"']}},
        {"set": {"g": "Youth t-shirt", "sz": "M (10-12)", "pl": "Full front"}, "expect": {"rows": ['9.5" to 10.5"', '9" to 11"']}},
        {"set": {"g": "Cap", "pl": "Back, above the strap"}, "expect": {"big": ['3.5" × 1" max']}},
    ],
)
