#!/usr/bin/env node
// Read-only smoke test of the published site.
// Loads every page in the live sitemap, fails on JS console errors or page
// errors, checks every Gumroad buy link returns HTTP 200, and checks that
// links carrying the FIRST10 discount keep ?code=FIRST10 and point only at
// the Seller Profit Sheet, the Get Paid Kit, and the 2027 Budget Planner.
//
//   npm install --no-save playwright
//   npx playwright install chromium
//   node tools/smoke_live.js [baseURL]
//
// GET requests only. Does not write to the repo or the site.
'use strict';

const fs = require('fs');
const { chromium, request } = require(process.env.PW || 'playwright');

const DEFAULT_BASE = 'https://rudracodeshere.github.io/profit-calculator/';
// Product URLs from tools/build_pages.py (GUMROAD, KIT, EXTRAS.budget).
const FIRST10_HOST = 'quietprofitsheets.gumroad.com';
const FIRST10_SLUGS = new Set([
  'seller-profit-sheet',
  'get-paid-kit',
  '2027-budget-spreadsheet',
]);

function baseUrl() {
  const raw = process.argv[2] || process.env.SMOKE_BASE || DEFAULT_BASE;
  const url = new URL(raw);
  if (!url.pathname.endsWith('/')) url.pathname += '/';
  url.search = '';
  url.hash = '';
  return url.toString();
}

function decodeXml(text) {
  return text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'");
}

function productOf(href) {
  let url;
  try {
    url = new URL(href);
  } catch (err) {
    return null;
  }
  if (!/(^|\.)gumroad\.com$/i.test(url.hostname)) return null;
  const parts = url.pathname.split('/').filter(Boolean);
  if (parts[0] !== 'l' || !parts[1]) return null;
  return {
    href: href.split('#')[0],
    host: url.hostname.toLowerCase(),
    slug: parts[1],
  };
}

function first10Problems(href) {
  let url;
  try {
    url = new URL(href);
  } catch (err) {
    return href.includes('FIRST10') ? ['invalid URL'] : null;
  }
  const carries = href.includes('FIRST10') || url.searchParams.get('code') === 'FIRST10';
  if (!carries) return null;
  const problems = [];
  if (url.searchParams.get('code') !== 'FIRST10') problems.push('missing ?code=FIRST10');
  const parts = url.pathname.split('/').filter(Boolean);
  const slug = parts[0] === 'l' ? parts[1] : '';
  if (url.hostname.toLowerCase() !== FIRST10_HOST || !FIRST10_SLUGS.has(slug)) {
    problems.push(`points at ${url.hostname}${url.pathname}, not the seller sheet, get paid kit, or 2027 budget`);
  }
  return problems;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getStatus(api, url) {
  let lastError = null;
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const res = await api.get(url, { timeout: 30000, maxRedirects: 10 });
      const status = res.status();
      // Gumroad rate-limits bursts of the same product. Back off and retry.
      if ((status === 429 || status >= 500) && attempt < 4) {
        await sleep(5000 * attempt);
        continue;
      }
      return { status, error: '', finalUrl: res.url() };
    } catch (err) {
      lastError = err;
      if (attempt < 4) await sleep(5000 * attempt);
    }
  }
  return { status: 0, error: String(lastError && lastError.message || lastError), finalUrl: url };
}

// One fetch per product path and discount code. utm_* values only track which
// page the link came from; they are not a different buy link.
function buyKey(link) {
  const url = new URL(link.href);
  const code = url.searchParams.get('code') || '';
  return `${url.origin}${url.pathname}${code ? '?code=' + code : ''}`;
}

async function listPages(api, base) {
  const sitemapUrl = new URL('sitemap.xml', base).toString();
  const res = await api.get(sitemapUrl, { timeout: 30000 });
  if (res.status() !== 200) throw new Error(`sitemap ${sitemapUrl} returned HTTP ${res.status()}`);
  const xml = await res.text();
  const locs = [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/gi)].map(match => decodeXml(match[1].trim()));
  if (!locs.length) throw new Error(`sitemap ${sitemapUrl} has no <loc> entries`);
  const root = new URL(base);
  const pages = [];
  const seen = new Set();
  for (const loc of locs) {
    const url = new URL(loc);
    if (url.origin !== root.origin || !url.pathname.startsWith(root.pathname)) continue;
    url.search = '';
    url.hash = '';
    const key = url.toString();
    if (seen.has(key)) continue;
    seen.add(key);
    pages.push(key);
  }
  if (!pages.length) throw new Error(`sitemap ${sitemapUrl} has no pages under ${base}`);
  pages.sort();
  return pages;
}

function pageLabel(page, base) {
  const path = page.slice(base.length - (base.endsWith('/') ? 1 : 0));
  return path || '/';
}

function writeSummary(markdown) {
  console.log(markdown);
  if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, markdown + '\n');
}

async function main() {
  const base = baseUrl();
  const api = await request.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  });
  const browser = await chromium.launch();
  const failures = [];
  const pageResults = [];
  const buyOccurrences = [];
  const first10Occurrences = [];
  try {
    const pages = await listPages(api, base);
    console.log(`live smoke: ${pages.length} pages at ${base}`);
    for (const pageUrl of pages) {
      const label = pageLabel(pageUrl, base);
      const context = await browser.newContext();
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', err => errors.push('pageerror: ' + String(err)));
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push('console: ' + msg.text());
      });
      let status = 0;
      try {
        const res = await page.goto(pageUrl, { waitUntil: 'load', timeout: 45000 });
        status = res ? res.status() : 0;
        await page.waitForTimeout(300);
        const hrefs = await page.$$eval('a[href]', anchors => anchors.map(anchor => anchor.href));
        for (const href of hrefs) {
          const product = productOf(href);
          if (product) buyOccurrences.push({ page: pageUrl, label, ...product });
          const discountProblems = first10Problems(href);
          if (discountProblems) first10Occurrences.push({ page: pageUrl, label, href, problems: discountProblems });
        }
      } catch (err) {
        errors.push('load: ' + String(err && err.message || err));
      }
      if (status && status !== 200) errors.push(`HTTP ${status}`);
      const uniqueErrors = [...new Set(errors)];
      pageResults.push({ page: pageUrl, label, status, errors: uniqueErrors });
      if (uniqueErrors.length) {
        failures.push({ kind: 'page', label, detail: uniqueErrors.join('; ') });
        console.log('FAIL ' + label + '\n  ' + uniqueErrors.join('\n  '));
      } else {
        console.log('ok   ' + label);
      }
      await context.close();
    }

    const buyByKey = new Map();
    for (const link of buyOccurrences) {
      const key = buyKey(link);
      if (!buyByKey.has(key)) buyByKey.set(key, { ...link, key, pages: [], hrefs: [] });
      const entry = buyByKey.get(key);
      if (!entry.pages.includes(link.label)) entry.pages.push(link.label);
      if (!entry.hrefs.includes(link.href)) entry.hrefs.push(link.href);
    }
    const buyResults = [];
    for (const link of buyByKey.values()) {
      const got = await getStatus(api, link.href);
      await sleep(400);
      const ok = got.status === 200;
      buyResults.push({ ...link, ...got, ok });
      if (!ok) {
        const detail = got.error ? `${got.error}` : `HTTP ${got.status}`;
        failures.push({ kind: 'buy', label: link.key, detail: `${detail} (${link.hrefs.length} links, on ${link.pages.join(', ')})` });
        console.log(`FAIL buy ${link.key} ${detail}`);
      } else {
        console.log(`ok   buy ${link.slug} ${link.key} (${link.hrefs.length} links)`);
      }
    }

    for (const link of first10Occurrences) {
      if (!link.problems.length) continue;
      failures.push({ kind: 'first10', label: link.href, detail: `${link.problems.join('; ')} (on ${link.label})` });
      console.log(`FAIL FIRST10 ${link.href}\n  ${link.problems.join('\n  ')} on ${link.label}`);
    }
    const first10Ok = first10Occurrences.filter(link => link.problems.length === 0).length;
    if (first10Occurrences.length) {
      console.log(`ok   FIRST10 ${first10Ok}/${first10Occurrences.length} links keep ?code=FIRST10 on the three launch products`);
    } else {
      failures.push({ kind: 'first10', label: '(none)', detail: 'no FIRST10 links found' });
      console.log('FAIL FIRST10: no discount links found');
    }

    const lines = [];
    lines.push('# Live smoke test');
    lines.push('');
    lines.push(`Base: ${base}`);
    lines.push('');
    lines.push(`- Pages checked: ${pageResults.length}`);
    lines.push(`- Page failures: ${pageResults.filter(item => item.errors.length).length}`);
    lines.push(`- Gumroad buy links checked: ${buyOccurrences.length} (${buyResults.length} distinct product URLs fetched)`);
    lines.push('- Each product path is fetched once, and once more with `?code=FIRST10` when a link carries that code. Tracking parameters are not separate pages.');
    lines.push(`- Buy-link failures: ${buyResults.filter(item => !item.ok).length}`);
    lines.push(`- FIRST10 links checked: ${first10Occurrences.length}`);
    lines.push(`- FIRST10 failures: ${first10Occurrences.filter(item => item.problems.length).length}`);
    lines.push('');
    lines.push(failures.length ? '**Result: failed**' : '**Result: passed**');
    lines.push('');
    if (failures.length) {
      lines.push('## Failures');
      lines.push('');
      for (const failure of failures) lines.push(`- ${failure.kind}: ${failure.label} — ${failure.detail}`);
      lines.push('');
    }
    lines.push('## Pages');
    lines.push('');
    for (const item of pageResults) {
      const mark = item.errors.length ? `FAIL HTTP ${item.status || '—'}` : `ok HTTP ${item.status}`;
      lines.push(`- ${mark} \`${item.label}\``);
      for (const error of item.errors) lines.push(`  - ${error}`);
    }
    lines.push('');
    lines.push('## Gumroad buy links');
    lines.push('');
    const bySlug = new Map();
    for (const item of buyResults) {
      if (!bySlug.has(item.slug)) bySlug.set(item.slug, []);
      bySlug.get(item.slug).push(item);
    }
    for (const [slug, items] of [...bySlug.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
      const bad = items.filter(item => !item.ok);
      const covered = items.reduce((sum, item) => sum + item.hrefs.length, 0);
      lines.push(`- \`${slug}\`: ${covered} link${covered === 1 ? '' : 's'}, ${items.length} URL${items.length === 1 ? '' : 's'} fetched, ${bad.length ? bad.length + ' failed' : 'all HTTP 200'}`);
      for (const item of items) {
        const mark = item.ok ? `HTTP ${item.status}` : `HTTP ${item.status || 'error'} ${item.error || 'not 200'}`;
        lines.push(`  - ${mark} \`${item.key}\` (${item.hrefs.length} links, on ${item.pages.join(', ')})`);
      }
    }
    lines.push('');
    lines.push('## FIRST10 links');
    lines.push('');
    if (!first10Occurrences.length) {
      lines.push('No links carrying FIRST10 were found.');
    } else {
      const slugs = [...new Set(first10Occurrences.map(link => {
        try {
          const url = new URL(link.href);
          const parts = url.pathname.split('/').filter(Boolean);
          return parts[0] === 'l' ? parts[1] : url.pathname;
        } catch (err) {
          return link.href;
        }
      }))].sort();
      lines.push(`Allowed products: \`seller-profit-sheet\`, \`get-paid-kit\`, \`2027-budget-spreadsheet\` on \`${FIRST10_HOST}\`.`);
      lines.push('');
      lines.push(`Products linked with FIRST10: ${slugs.map(slug => '`' + slug + '`').join(', ') || '(none)'}.`);
      const bad = first10Occurrences.filter(link => link.problems.length);
      if (bad.length) {
        lines.push('');
        for (const link of bad) lines.push(`- ${link.problems.join('; ')} — ${link.href} (on \`${link.label}\`)`);
      }
    }
    lines.push('');
    writeSummary(lines.join('\n'));
  } finally {
    await browser.close();
    await api.dispose();
  }
  process.exit(failures.length ? 1 : 0);
}

main().catch(err => {
  console.error(err);
  writeSummary('# Live smoke test\n\n**Result: failed**\n\n```\n' + String(err && err.stack || err) + '\n```\n');
  process.exit(1);
});
