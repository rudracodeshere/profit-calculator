// Load every generated page in Chromium, fail on JS errors, empty results, or failed spec tests.
// Run: python3 tools/build_pages.py --tests > /tmp/t.json && node tools/check_pages.js /tmp/t.json
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const specs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const b = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') ? undefined : undefined });
  let fail = 0;
  for (const s of specs) {
    const pg = await b.newPage({ viewport: { width: 390, height: 900 } });
    const errs = [];
    pg.on('pageerror', e => errs.push(String(e)));
    pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto('file://' + path.join(root, s.slug, 'index.html'));
    const txt = await pg.evaluate(() => document.querySelector('.card').innerText);
    const overflow = await pg.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    const probs = [...errs];
    if (overflow) probs.push('horizontal overflow at 390px');
    const box = await pg.evaluate(() => {
      const bs = document.querySelectorAll('.buybox'), b = bs[0];
      return { n: bs.length, cta: document.querySelectorAll('.cta').length, text: b ? b.innerText : '',
        href: b ? b.querySelector('a.btn').href : '', inCard: b ? !!b.closest('.card') : true };
    });
    if (box.n > 1 || box.cta) probs.push(`expected at most one .buybox and no .cta, got ${box.n} / ${box.cta}`);
    if (!box.inCard) probs.push('.buybox is not under the result');
    const launch = /\/l\/(seller-profit-sheet|get-paid-kit|2027-budget-spreadsheet)\?code=FIRST10/.test(box.href);
    if (/FIRST10/.test(box.text) !== launch) probs.push('FIRST10 text and link disagree: ' + box.href);
    if (/NaN|undefined|Infinity/.test(txt)) probs.push('bad value in output: ' + (txt.match(/.{0,40}(NaN|undefined|Infinity).{0,20}/) || [''])[0]);
    for (const [i, t] of (s.tests || []).entries()) {
      await pg.reload();
      for (const [id, v] of Object.entries(t.set || {})) {
        await pg.evaluate(([id, v]) => {
          const el = document.getElementById(id);
          if (el.type === 'checkbox') el.checked = !!v; else el.value = v;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }, [id, v]);
      }
      for (const id of t.click || []) await pg.click('#' + id);
      for (const [id, want] of Object.entries(t.expect || {})) {
        const got = await pg.evaluate(id => { const e = document.getElementById(id); return e ? e.innerText : '(missing #' + id + ')'; }, id);
        for (const w of [].concat(want)) if (!got.includes(w)) probs.push(`test ${i}: #${id} lacks "${w}" | got: ${got.replace(/\s+/g, ' ').slice(0, 300)}`);
      }
    }
    console.log((probs.length ? 'FAIL ' : 'ok   ') + s.slug + (probs.length ? '\n  ' + probs.join('\n  ') : ''));
    if (probs.length) fail++;
    await pg.close();
  }
  await b.close();
  process.exit(fail ? 1 : 0);
})();
