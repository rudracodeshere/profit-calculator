PAGE = dict(
    gig="seo",
    slug="etsy-title-tag-checker",
    cat="Etsy tools",
    cta_extra=["sizekit"],
    nav_name="Etsy title and tag checker",
    title="Etsy Title and Tag Checker: Character Counter for 13 Tags and 140-Character Titles",
    desc="Free Etsy title and tag checker. Paste a listing title and tags to count characters, catch tags over 20 characters, duplicates, banned symbols and wasted tag slots.",
    h1="Etsy title and tag checker",
    lead="Paste a listing's title and tags. The checker counts characters, flags anything Etsy will reject, and points out wasted tag slots: duplicates, plural repeats, single words and words already in your title.",
    form="""      <label for="title">Listing title <small>(max 140 characters)</small></label>
      <textarea id="title" rows="3" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;resize:vertical">Boho Macrame Wall Hanging, Large Macrame Wall Hanging, Boho Wall Decor, Gift for Her, HANDMADE Wall Art & Bedroom Decor & Nursery Decor</textarea>
      <label for="tags">Tags <small>(one per line or comma separated, up to 13)</small></label>
      <textarea id="tags" rows="7" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;resize:vertical">macrame wall hanging, boho decor, wall hanging, macrame, boho wall decors, boho wall decor, large macrame wall hanging art, gift for her, nursery decor, bedroom wall art</textarea>""",
    out="""<div class="big"><span>Problems found</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Your tags</h3>
      <table class="wide"><thead><tr><th>Tag</th><th>Chars</th><th>Check</th></tr></thead><tbody id="tagtab"></tbody></table>""",
    js="""var esc=function(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var STOP={'a':1,'an':1,'and':1,'the':1,'for':1,'of':1,'with':1,'in':1,'on':1,'to':1,'or':1,'by':1,'her':1,'him':1};
var words=function(s){return s.toLowerCase().split(/[^\\p{L}\\p{N}']+/u).filter(Boolean)};
var sing=function(w){return w.length>3&&/s$/.test(w)&&!/ss$/.test(w)?w.slice(0,-1):w};
function calc(){
  var t=$('title').value.replace(/\\s+/g,' ').trim(), rows=[], bad=0, warn=0;
  var add=function(label,val,level){rows.push([label,val]);if(level==2)bad++;else if(level==1)warn++};
  // Title
  var tl=t.length, tw=words(t);
  add('Title length',tl+' / 140'+(tl>140?' (over by '+(tl-140)+')':''),tl>140?2:0);
  if(!tl)add('Title','empty',2);
  if(tw.length>15)add('Title words',tw.length+': Etsy suggests keeping titles short and readable',1);
  var caps=(t.match(/\\b[A-Z]{2,}\\b/g)||[]).length;
  if(caps>3)add('ALL CAPS words in title',caps+' (Etsy allows 3)',2);
  ['%',':','&'].forEach(function(c){var k=t.split(c).length-1;if(k>1)add('"'+c+'" in title',k+' times (Etsy allows once)',2)});
  var ban=t.match(/[$^`]/g);if(ban)add('Not allowed in titles',ban.join(' '),2);
  if(tl&&/^[^\\p{L}\\p{N}]/u.test(t))add('Title start','must start with a letter or number',2);
  var seen={},rep=[];tw.forEach(function(w){w=sing(w);if(STOP[w])return;seen[w]=(seen[w]||0)+1;if(seen[w]==2)rep.push(w)});
  if(rep.length)add('Words repeated in title',rep.join(', '),1);
  // Tags
  var tags=$('tags').value.split(/[,\\n]+/).map(function(s){return s.replace(/\\s+/g,' ').trim()}).filter(Boolean);
  var titleSet={};tw.forEach(function(w){titleSet[sing(w)]=1});
  var keyN={},keyS={},h='';
  tags.forEach(function(g){var k=g.toLowerCase();keyN[k]=(keyN[k]||0)+1;var s=words(g).map(sing).join(' ');keyS[s]=(keyS[s]||0)+1});
  var nLong=0,nChar=0,nDup=0,nNear=0,nOne=0,nInTitle=0,doneN={},doneS={};
  tags.forEach(function(g,i){
    var k=g.toLowerCase(),s=words(g).map(sing).join(' '),w=words(g),msg=[],lvl=0;
    if(i>=13){msg.push('over 13');lvl=2}
    if(g.length>20){msg.push('over 20');lvl=2;nLong++}
    if(/[^\\p{L}\\p{N} '\\-]/u.test(g)){msg.push('bad character');lvl=2;nChar++}
    if(keyN[k]>1&&doneN[k]){msg.push('duplicate');lvl=2;nDup++}
    else if(keyS[s]>1&&doneS[s]){msg.push('plural repeat');lvl=Math.max(lvl,1);nNear++}
    doneN[k]=1;doneS[s]=1;
    if(w.length==1){msg.push('single word');lvl=Math.max(lvl,1);nOne++}
    else if(w.length&&w.every(function(x){return titleSet[sing(x)]})){msg.push('all words in title');nInTitle++}
    h+='<tr><td>'+esc(g)+'</td><td>'+g.length+'</td><td style="color:'+(lvl==2?'var(--red)':lvl==1?'#a15c00':'var(--green)')+'">'+(msg.length?msg.join(', '):'ok')+'</td></tr>';
  });
  $('tagtab').innerHTML=h||'<tr><td colspan="3">No tags entered</td></tr>';
  add('Tags used',Math.min(tags.length,13)+' / 13'+(tags.length>13?' ('+(tags.length-13)+' extra)':''),tags.length>13?2:tags.length<13?1:0);
  if(nLong)add('Tags over 20 characters',nLong,2);
  if(nChar)add('Tags with characters Etsy rejects',nChar,2);
  if(nDup)add('Duplicate tags',nDup,2);
  if(nNear)add('Singular/plural repeats',nNear+' (Etsy matches both forms)',1);
  if(nOne)add('Single-word tags',nOne+' (multi-word phrases match more searches)',1);
  if(nInTitle)add('Tags whose words are all in the title',nInTitle+' (could target a new phrase)',0);
  setRows(rows);
  $('big').textContent=bad+' errors, '+warn+' warnings';
  if(bad)verdict(false,'Fix the '+bad+' error'+(bad>1?'s':'')+' first: Etsy will reject or cut these.'+(tags.length<13?' Then fill the '+(13-Math.min(tags.length,13))+' empty tag slots.':''));
  else if(tags.length<13)verdict(false,'No hard errors, but '+(13-tags.length)+' of your 13 tag slots are empty. Each empty slot is a search phrase you are not showing up for.');
  else if(warn)verdict(true,'Etsy will accept this. The warnings are tag slots you could spend on new search phrases.');
  else verdict(true,'Clean: 13 tags, no repeats, nothing Etsy will reject.');
}
['title','tags'].forEach(function(id){$(id).addEventListener('input',calc)});""",
    note="Rules checked as of October 2026: titles up to 140 characters, no more than 3 ALL CAPS words, % : and &amp; once each, no $ ^ or `; 13 tags of up to 20 characters using letters, numbers, spaces, apostrophes and hyphens. Nothing you type leaves your browser.",
    body="""<h2>What the checker looks for</h2>
<p>Etsy has hard limits it enforces when you save a listing, and softer habits that decide whether your 13 tags actually bring in different searches. The checker splits them into <strong>errors</strong> (Etsy will reject or cut it) and <strong>warnings</strong> (it saves, but you are wasting reach).</p>
<h3>Errors</h3>
<ul>
<li><strong>Title over 140 characters.</strong> The listing editor stops at 140, so anything past that is lost.</li>
<li><strong>More than 3 ALL CAPS words, or %, : or &amp; used more than once.</strong> Etsy blocks these to keep titles readable. $, ^ and ` are not allowed at all.</li>
<li><strong>Tags over 20 characters.</strong> "large macrame wall hanging art" is 30 characters and will not save. Cut it to the phrase buyers type, like "large macrame art".</li>
<li><strong>More than 13 tags, duplicate tags, or symbols in tags.</strong> Tags can only use letters, numbers, spaces, apostrophes and hyphens.</li>
</ul>
<h3>Warnings</h3>
<ul>
<li><strong>Empty tag slots.</strong> Every listing gets 13. Leaving 3 empty means 3 fewer phrases you can be found for.</li>
<li><strong>Singular and plural repeats.</strong> Etsy search treats "boho wall decor" and "boho wall decors" as the same phrase, so the second tag is a wasted slot.</li>
<li><strong>Single-word tags.</strong> One word like "macrame" competes with every macrame listing on the site. Two- and three-word phrases match what buyers type and face less competition.</li>
<li><strong>Repeated words in the title.</strong> Saying "macrame wall hanging" twice does not count twice. Etsy recommends short, readable titles that describe the item.</li>
</ul>
<h2>Do my tags need to repeat my title?</h2>
<p>No. Etsy has said it matches searches across your title, tags, categories and attributes together, and that there is no need to repeat the same words. The checker marks tags whose words all already appear in the title so you can decide whether that slot would earn more as a new phrase (a style, an occasion, a recipient or a material).</p>
<h2>Why sales can drop after rewriting titles</h2>
<p>Editing a title or tags makes Etsy re-evaluate the listing, and listings that were already selling can lose their place for a while. Fix errors and empty slots on listings that get few views first, and change your best sellers one at a time.</p>""",
    faqs=[
        ("How many characters can an Etsy tag have?", "20, including spaces. Each listing can have 13 tags."),
        ("How long can an Etsy title be?", "140 characters including spaces. Etsy recommends keeping titles short and descriptive rather than filling all 140."),
        ("Does Etsy count plural tags separately?", "No. Etsy search matches singular and plural forms, so \"wall hanging\" and \"wall hangings\" use two slots for one phrase."),
        ("Is my listing text saved anywhere?", "No. The checker runs entirely in your browser and nothing is sent to a server."),
    ],
    related=["etsy-fee-calculator", "etsy-profit-calculator", "etsy-pricing-calculator", "etsy-ads-calculator", "etsy-sale-calculator"],
    cta_head="Your listings bring the views. Do the sales make money?",
    tests=[
        {"expect": {"big": "errors", "rows": ["135 / 140", "\"&", "10 / 13", "Single-word tags"],
                    "tagtab": ["over 20", "plural repeat", "single word"], "verdict": "Fix the"}},
        {"set": {"title": "Handmade Ceramic Mug, Speckled Stoneware Coffee Cup", "tags": "ceramic mug,coffee cup,stoneware mug,pottery mug,handmade mug,speckled mug,gift for him,gift for her,tea cup,latte mug,camping mug,rustic mug,birthday gift"},
         "expect": {"big": "0 errors", "rows": "13 / 13", "verdict": "Clean"}},
        {"set": {"tags": "ceramic mug,Ceramic Mug,coffee cup$"}, "expect": {"rows": ["Duplicate tags", "characters Etsy rejects"], "tagtab": ["duplicate", "bad character"]}},
        {"set": {"title": "BIG RED SALE NOW mug"}, "expect": {"rows": "ALL CAPS words in title"}},
        {"set": {"title": "x" * 150}, "expect": {"rows": "over by 10"}},
        {"set": {"title": "", "tags": ""}, "expect": {"rows": "empty", "tagtab": "No tags entered"}},
        {"set": {"title": "<b>Mug</b>", "tags": "<i>tag</i>"}, "expect": {"tagtab": "<i>tag</i>"}},
    ],
)
