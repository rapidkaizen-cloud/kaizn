#!/usr/bin/env node
// verify_pages.js - design-settle Step 8's rendered checks, one run for every promoted page
// (skills/design-settle/references/verify.md). Prints one row per page and width; a reader
// opens only the rows marked FAIL or n/v.
//
//   node verify_pages.js --url <dev server> --widths <w,w> [--storage <state.json>] [--out <dir>] <page>=<target> ...
//   node verify_pages.js --app <built .exe> --widths <w,w> [--out <dir>] <page>=<target> ...
//
// --url  : headless Chrome on its own temporary profile (build-flow Section 5).
// --app  : the app's own build, launched here with its webview's debugging port open and
//          reached with connectOverCDP - WebView2 (Tauri) or Electron's Chromium, on Windows.
// target : a path or hash (/settings, #/settings), opened against the start URL; anything
//          else is a Playwright selector clicked to reach the page (role=tab[name="Settings"]).
// Run from the app repo: Playwright and axe-core are resolved from its node_modules, axe-core
// fetched from jsDelivr where the repo has none - never installed into the app.
// Exit: 0 every row passed · 1 a row failed or could not run a check · 2 usage · 3 no Playwright.
'use strict';
const fs = require('fs');
const path = require('path');
const net = require('net');
const http = require('http');
const { spawn } = require('child_process');
const { createRequire } = require('module');

const AXE_URL = 'https://cdn.jsdelivr.net/npm/axe-core@4.10.3/axe.min.js';
// Each check is a count; above zero fails, null means it could not run.
const CHECKS = ['errors', 'fonts', 'axe', 'contrast', 'motion', 'overflow'];

function parseArgs(argv) {
  const a = { pages: [], widths: [], out: '.design-audit/verify' };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === '--selftest') a.selftest = true;
    else if (['--url', '--app', '--storage', '--out'].includes(k)) a[k.slice(2)] = argv[++i];
    else if (k === '--widths') a.widths = String(argv[++i] || '').split(',').map(Number).filter(n => n > 0);
    else if (k.includes('=')) { const at = k.indexOf('='); a.pages.push({ name: k.slice(0, at), target: k.slice(at + 1) }); }
    else throw new Error(`unknown argument: ${k}`);
  }
  if (a.selftest) return a;
  if (!a.url === !a.app) throw new Error('give exactly one of --url and --app');
  if (!a.widths.length) throw new Error('--widths is required: the desktop breakpoint and the lowest supported width');
  if (!a.pages.length) throw new Error('name at least one <page>=<target>');
  return a;
}

const isUrl = t => /^([/#?]|https?:|file:)/.test(t);

function verdict(row) {
  const failed = CHECKS.filter(k => row[k] !== null && row[k] > 0);
  const unrun = CHECKS.filter(k => row[k] === null);
  return failed.length ? `FAIL ${failed.join(',')}` : unrun.length ? `n/v ${unrun.join(',')}` : 'pass';
}

function table(rows) {
  const cell = v => (v === null ? 'n/v' : String(v));
  const lines = ['page | width | verdict | ' + CHECKS.join(' | ') + ' | capture'];
  for (const r of rows) lines.push([r.page, r.width, verdict(r), ...CHECKS.map(k => cell(r[k])), r.shot || '-'].join(' | '));
  const bad = rows.filter(r => verdict(r) !== 'pass');
  lines.push(`rows ${rows.length} · failed ${bad.filter(r => verdict(r).startsWith('FAIL')).length} · not verified ${bad.filter(r => verdict(r).startsWith('n/v')).length}`);
  return { text: lines.join('\n'), ok: bad.length === 0 };
}

function selftest() {
  const a = parseArgs(['--url', 'http://localhost:5173', '--widths', '1440,375', 'home=/', 'settings=role=tab[name="Settings"]']);
  const pass = { page: 'home', width: 1440, errors: 0, fonts: 0, axe: 0, contrast: 0, motion: 0, overflow: 0, shot: 'x.png' };
  const t = table([pass, { ...pass, width: 375, overflow: 12 }, { ...pass, page: 'settings', axe: null }]);
  const ok = a.widths.join() === '1440,375' && a.pages[1].target === 'role=tab[name="Settings"]'
    && isUrl('/') && isUrl('#/a') && !isUrl('role=tab') && verdict(pass) === 'pass'
    && t.text.includes('| FAIL overflow |') && t.text.includes('| n/v axe |') && t.text.endsWith('rows 3 · failed 1 · not verified 1') && !t.ok
    && table([pass]).ok;
  let refused = 0;
  for (const bad of [[], ['--url', 'x', '--app', 'y', '--widths', '1', 'a=/'], ['--url', 'x', 'a=/'], ['--url', 'x', '--widths', '1']]) {
    try { parseArgs(bad); } catch { refused++; }
  }
  if (!ok || refused !== 4) throw new Error('verify_pages: selftest failed');
  return 'ok';
}

function loadFromRepo() {
  const req = createRequire(path.join(process.cwd(), 'package.json'));
  let pw = null;
  for (const m of ['playwright', '@playwright/test', 'playwright-core']) { try { pw = req(m); break; } catch { /* next */ } }
  let axe = null;
  try { axe = fs.readFileSync(req.resolve('axe-core/axe.min.js'), 'utf8'); } catch { /* fetched later */ }
  return { pw, axe };
}

const freePort = () => new Promise((ok, no) => { const s = net.createServer(); s.on('error', no); s.listen(0, '127.0.0.1', () => { const { port } = s.address(); s.close(() => ok(port)); }); });
const answers = url => new Promise(ok => { http.get(url, r => { r.resume(); ok(r.statusCode === 200); }).on('error', () => ok(false)); });

async function launchApp(exe) {
  const port = await freePort();
  // Electron reads the switch from its command line, WebView2 from this variable; a Tauri app
  // is never handed an argument it did not declare.
  const electron = fs.existsSync(path.join(path.dirname(exe), 'resources', 'app.asar')) || fs.existsSync(path.join(path.dirname(exe), 'resources', 'app'));
  const env = { ...process.env, WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS: `--remote-debugging-port=${port}` };
  const child = spawn(exe, electron ? [`--remote-debugging-port=${port}`] : [], { env, stdio: 'ignore' });
  let exited = false;
  child.on('exit', () => { exited = true; });
  child.on('error', () => { exited = true; });
  for (let t = 0; t < 120; t++) {
    if (await answers(`http://127.0.0.1:${port}/json/version`)) return { child, endpoint: `http://127.0.0.1:${port}` };
    if (exited) break;
    await new Promise(r => setTimeout(r, 250));
  }
  child.kill();
  throw new Error(exited ? 'the app exited before its webview opened - is another copy of it already running?' : 'no webview answered on the debugging port within 30 s');
}

async function measure(page, axeSrc, measureSrc) {
  const row = {};
  row.fonts = await page.evaluate(async () => { await Promise.allSettled([...document.fonts].map(f => f.load())); return [...document.fonts].filter(f => f.status === 'error').length; }).catch(() => null);
  row.overflow = await page.evaluate(() => Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)).catch(() => null);
  row.contrast = await page.evaluate(`(${measureSrc})('pairs')`).then(r => r.text.under + r.nontext.under).catch(() => null);
  row.axe = axeSrc === null ? null : await page.evaluate(async src => {
    if (!window.axe) (0, eval)(src);
    const r = await window.axe.run(document, { resultTypes: ['violations'] });
    return r.violations.filter(v => v.impact === 'serious' || v.impact === 'critical').reduce((n, v) => n + v.nodes.length, 0);
  }, axeSrc).catch(() => null);
  try {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.waitForTimeout(300);
    row.motion = await page.evaluate(() => document.getAnimations().filter(a => a.playState === 'running').length
      + [...document.querySelectorAll('*')].filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length);
  } catch { row.motion = null; }
  await page.emulateMedia({ reducedMotion: null }).catch(() => {});
  return row;
}

async function main() {
  let a;
  try { a = parseArgs(process.argv.slice(2)); } catch (e) { console.error(`verify_pages: ${e.message}`); process.exit(2); }
  if (a.selftest) { console.log(selftest()); return; }
  const { pw, axe } = loadFromRepo();
  if (!pw) { console.error('verify_pages: no Playwright in this repo - every check is not verified'); process.exit(3); }
  let axeSrc = axe;
  if (axeSrc === null) axeSrc = await fetch(AXE_URL).then(r => (r.ok ? r.text() : null)).catch(() => null);
  const measureSrc = fs.readFileSync(path.join(__dirname, 'audit_measure.js'), 'utf8');
  fs.mkdirSync(a.out, { recursive: true });

  let browser, app, page, start;
  try {
    if (a.app) {
      app = await launchApp(path.resolve(a.app));
      browser = await pw.chromium.connectOverCDP(app.endpoint);
      const ctx = browser.contexts()[0];
      page = ctx.pages()[0] || await ctx.waitForEvent('page');
      await page.waitForLoadState('load');
      start = page.url();
    } else {
      browser = await pw.chromium.launch({ channel: 'chrome', headless: true });
      const ctx = await browser.newContext(a.storage ? { storageState: a.storage } : {});
      page = await ctx.newPage();
      start = a.url;
    }
    let errors = 0;
    page.on('console', m => { if (m.type() === 'error') errors++; });
    page.on('pageerror', () => { errors++; });

    const rows = [];
    for (const p of a.pages) {
      errors = 0;
      let reached = true;
      try {
        if (isUrl(p.target)) await page.goto(new URL(p.target, start).href, { waitUntil: 'load' });
        else await page.locator(p.target).first().click({ timeout: 10000 });
        await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      } catch { reached = false; }
      for (const width of a.widths) {
        if (!reached) { rows.push({ page: p.name, width, ...Object.fromEntries(CHECKS.map(k => [k, null])), shot: 'not reached' }); continue; }
        await page.setViewportSize({ width, height: 900 });
        await page.waitForTimeout(300);
        const row = await measure(page, axeSrc, measureSrc);
        const shot = path.join(a.out, `${p.name.replace(/[^\w.-]+/g, '-')}-${width}.png`);
        await page.screenshot({ path: shot, fullPage: true }).catch(() => {});
        rows.push({ page: p.name, width, errors, ...row, shot: fs.existsSync(shot) ? shot : null });
      }
    }
    const t = table(rows);
    console.log(t.text);
    process.exitCode = t.ok ? 0 : 1;
  } finally {
    if (browser) await browser.close().catch(() => {});
    if (app) app.child.kill();
  }
}

if (require.main === module) main().catch(e => { console.error(`verify_pages: ${e.message}`); process.exit(1); });
