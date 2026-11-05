"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const crypto = require("crypto");
const { pathToFileURL } = require("url");
const { chromium } = require("C:/Users/11515/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const ROOT = "D:/CODEX/魔术之心";
const OUT = path.join(ROOT, "deliverables/handoff_20261105/web_qa");
const PREFIX = "magic-maid.pv-manual-review.v1:";
const sha = p => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const FILES = ["manual_review/index.html", "manual_review/app.js", "manual_review/styles.css", "manual_review/data.js", "manual_review/data.json"];
const report = {
  TEST_ONLY: true, started_at: new Date().toISOString(),
  scope: "Isolated headless Edge local file smoke; synthetic manual records only; no actual human approval.",
  external_requests_allowed: false, production_assets_modified: false,
  input_sha256: Object.fromEntries(FILES.map(p => [p, sha(path.join(ROOT, p))])),
  checks: [], console_errors: [], page_errors: [], external_requests_blocked: []
};
let browser, context, page;
function check(name, detail) { report.checks.push({ name, passed: true, detail }); }
async function imagesReady() {
  for (const host of ["#source-image-host", "#drawing-image-host"]) {
    await page.locator(host + " img").waitFor({ state: "visible" });
    await page.waitForFunction(selector => {
      const im = document.querySelector(selector + " img");
      return im && im.complete && im.naturalWidth > 0 && im.naturalHeight > 0;
    }, host);
  }
}
async function select(id) {
  await page.locator("#clear-filters").click();
  await page.locator("#search-input").fill(id);
  await page.locator('.item-row[data-item-id="' + id + '"]').click();
  await page.waitForFunction(id => document.querySelector("#detail-title").textContent === id, id);
  await imagesReady();
}
async function count(id, expected) { assert.strictEqual((await page.locator("#" + id).textContent()).trim(), String(expected), id); }
async function clean() {
  await page.evaluate(prefix => {
    Object.keys(localStorage).filter(k => k.startsWith(prefix)).forEach(k => localStorage.removeItem(k));
  }, PREFIX);
  await page.reload({ waitUntil: "load" });
  await count("pending-count", 307);
  await count("approved-count", 0);
  await count("rework-count", 0);
  assert.strictEqual(await page.evaluate(prefix => Object.keys(localStorage).filter(k => k.startsWith(prefix)).length, PREFIX), 0);
}
async function noOverflow(label) {
  const d = await page.evaluate(() => ({
    inner: innerWidth, body: document.body.scrollWidth, document: document.documentElement.scrollWidth,
    detail: document.querySelector("#detail-panel").getBoundingClientRect().toJSON()
  }));
  assert(d.body <= d.inner + 1 && d.document <= d.inner + 1, label + " horizontal overflow " + JSON.stringify(d));
  check(label + "_no_horizontal_overflow", d);
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  browser = await chromium.launch({
    channel: "msedge", headless: true,
    args: ["--disable-background-networking", "--disable-component-update", "--disable-sync",
      "--no-first-run", "--disable-default-apps", "--disable-extensions", "--disable-domain-reliability",
      "--metrics-recording-only", "--disable-breakpad"]
  });
  report.browser_version = browser.version();
  context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true });
  await context.route(/^https?:\/\//i, route => {
    report.external_requests_blocked.push(route.request().url());
    return route.abort("blockedbyclient");
  });
  page = await context.newPage();
  page.on("console", msg => { if (msg.type() === "error") report.console_errors.push(msg.text()); });
  page.on("pageerror", err => report.page_errors.push(err.message));
  const entry = pathToFileURL(path.join(ROOT, "manual_review/index.html")).href;
  await page.goto(entry, { waitUntil: "load" });
  await count("total-count", 307); await count("pending-count", 307); await count("approved-count", 0);
  assert.strictEqual(await page.locator(".item-row").count(), 307);
  check("file_protocol_307_pending_zero_manual_approval", { url: page.url(), rows: 307 });
  await imagesReady();
  await noOverflow("desktop_1440_initial");
  await page.screenshot({ path: path.join(OUT, "desktop_1440_clean.png"), fullPage: true });

  await select("ART-G33-16");
  report.G33_16_loaded_images = await page.locator("#source-image-host img, #drawing-image-host img").evaluateAll(images => images.map(im => ({
    src: im.src, width: im.naturalWidth, height: im.naturalHeight
  })));
  assert(report.G33_16_loaded_images.every(im => im.width > 0));
  check("G33_16_original_and_current_image_loaded", report.G33_16_loaded_images);
  for (const bg of ["black", "transparent", "white"]) {
    await page.locator('[data-background="' + bg + '"]').click();
    await imagesReady();
  }
  check("white_black_transparent_views_loaded", true);
  const note = "TEST_ONLY 临时浏览器验证：G33-16 返修记录，不代表真实人工评审。";
  await page.locator('[data-status="rework"]').click();
  await page.locator("#review-note").fill(note);
  await page.reload({ waitUntil: "load" });
  await select("ART-G33-16");
  assert.strictEqual(await page.locator("#review-note").inputValue(), note);
  assert.strictEqual(await page.locator('[data-status="rework"]').getAttribute("aria-pressed"), "true");
  await count("pending-count", 306); await count("rework-count", 1); await count("approved-count", 0);
  check("G33_16_rework_note_persists_after_reload", true);
  await page.screenshot({ path: path.join(OUT, "TEST_ONLY_G33_16_rework_desktop.png"), fullPage: true });

  const historicalItem = await page.evaluate(() => window.PV_REVIEW_DATA.items.find(item =>
    (item.versions || []).some(v => v.image_sha256 && v.image_sha256 !== item.image_sha256)).id);
  await select(historicalItem);
  assert((await page.locator("#version-select option").count()) > 1);
  await page.locator("#version-select").selectOption("1");
  await imagesReady();
  await page.locator('[data-status="hold"]').click();
  const oldNote = "TEST_ONLY 历史版本隔离验证，不代表真实评审。";
  await page.locator("#review-note").fill(oldNote);
  const oldHash = await page.locator("#full-hash").textContent();
  await page.locator("#version-select").selectOption("0");
  assert.strictEqual(await page.locator("#review-note").inputValue(), "");
  assert.strictEqual(await page.locator('[data-status="pending"]').getAttribute("aria-pressed"), "true");
  const newHash = await page.locator("#full-hash").textContent();
  assert.notStrictEqual(oldHash, newHash);
  await page.locator("#version-select").selectOption("1");
  assert.strictEqual(await page.locator("#review-note").inputValue(), oldNote);
  await count("pending-count", 306);
  check("historical_version_ID_SHA_record_isolation", { id: historicalItem, historical_sha256: oldHash, current_sha256: newHash });
  await page.locator("#version-select").selectOption("0");

  await select("ART-G33-16");
  await page.locator("#group-filter").selectOption("G33");
  await page.locator("#status-filter").selectOption("rework");
  assert.strictEqual(await page.locator(".item-row").count(), 1);
  const downloadEvent = page.waitForEvent("download");
  await page.locator("#export-button").click();
  const download = await downloadEvent;
  const exportedFile = path.join(OUT, "TEST_ONLY_browser_export_all307.json");
  await download.saveAs(exportedFile);
  const exported = JSON.parse(fs.readFileSync(exportedFile, "utf8"));
  assert.strictEqual(exported.items.length, 307); assert.strictEqual(exported.total, 307);
  assert.strictEqual(exported.counts.pending, 306); assert.strictEqual(exported.counts.rework, 1);
  assert.strictEqual(exported.counts.approved, 0);
  assert.strictEqual(exported.items.find(item => item.id === "ART-G33-16").manual_note, note);
  assert(exported.items.find(item => item.id === historicalItem).version_reviews.some(v => v.note === oldNote && v.status === "hold"));
  report.synthetic_download = {
    TEST_ONLY: true, path: exportedFile, sha256: sha(exportedFile),
    suggested_filename: download.suggestedFilename(), filtered_visible_rows: 1,
    exported_total: exported.total, exported_pending: exported.counts.pending,
    exported_rework: exported.counts.rework
  };
  check("Blob_download_under_filter_includes_all307_and_pending306", report.synthetic_download);

  await clean();
  check("test_localStorage_removed_307_pending_restored", true);
  await page.locator("#clear-filters").click();
  await select("ART-G33-16");
  await imagesReady();
  await noOverflow("desktop_1440_final");
  await page.screenshot({ path: path.join(OUT, "desktop_1440_G33_16_clean_final.png"), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(250);
  await noOverflow("mobile_390");
  await page.screenshot({ path: path.join(OUT, "mobile_390_clean.png"), fullPage: true });
  await clean();
  assert.strictEqual(report.page_errors.length, 0, "browser page errors");
  assert.strictEqual(report.external_requests_blocked.length, 0, "unexpected external resources were requested");
  report.finished_at = new Date().toISOString();
  report.test_storage_cleaned = true;
  report.actual_user_manual_reviews_created = 0;
  report.status = "passed";
  report.output_input_sha256 = Object.fromEntries(FILES.map(p => [p, sha(path.join(ROOT, p))]));
  assert.deepStrictEqual(report.output_input_sha256, report.input_sha256, "smoke must not modify frontend/data files");
})().catch(error => {
  report.status = "failed"; report.error = { message: error.message, stack: error.stack };
  console.error(error.stack); process.exitCode = 1;
}).finally(async () => {
  if (page && !page.isClosed()) {
    try {
      await page.evaluate(prefix => Object.keys(localStorage).filter(k => k.startsWith(prefix)).forEach(k => localStorage.removeItem(k)), PREFIX);
      report.final_isolated_storage_keys = await page.evaluate(prefix => Object.keys(localStorage).filter(k => k.startsWith(prefix)).length, PREFIX);
    } catch (error) { report.cleanup_error = error.message; }
  }
  if (browser) await browser.close();
  fs.writeFileSync(path.join(OUT, "SMOKE.json"), JSON.stringify(report, null, 2) + "\n", "utf8");
  console.log(JSON.stringify({ status: report.status, checks: report.checks.length, output: OUT, test_storage_keys: report.final_isolated_storage_keys }));
});
