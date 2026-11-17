import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { industries } from "../content/industries.mjs";
import { cases, newCountryCases } from "../content/networks.mjs";
import { minimumSites, registeredDomain } from "../content/network-schema.mjs";

const root = fileURLToPath(new URL("../dist", import.meta.url));
const content = path => readFileSync(resolve(root, path), "utf8");
const htmlFiles = readdirSync(root, { recursive: true }).filter(path => path.endsWith(".html"));
const knownLinks = new Map();
const internalLabels = /历次研究|历史研究|访问备注|证据范围|网站资料核对|>资料核对<|class="site-note"/u;
assert.equal(htmlFiles.length, industries.length + cases.length + 5);
assert(!existsSync(resolve(root, "research")));
assert(!existsSync(resolve(root, "cases/pdtrus")));
for (const file of htmlFiles) {
  const html = content(file);
  assert.match(html, /<html lang="zh-CN">/u, file);
  assert.equal([...html.matchAll(/<h1(?:\s[^>]*)?>/g)].length, 1, file);
  assert.match(html, /<meta name="description" content="[^"]+"/);
  assert.doesNotMatch(html, internalLabels, file);
  const path = file === "index.html" ? "/" : "/" + file.replace(/index\.html$/, "");
  for (const [, value] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    if (value.startsWith("https://")) continue;
    assert(value.startsWith("/") || value.startsWith("#"), `Unexpected link in ${file}: ${value}`);
    const url = new URL(value, "https://example.test" + path);
    let target = resolve(root, "." + url.pathname);
    if (existsSync(target) && statSync(target).isDirectory()) target = resolve(target, "index.html");
    assert(existsSync(target), `${file}: missing ${value}`);
    if (url.hash) {
      if (!knownLinks.has(target)) {
        const text = readFileSync(target, "utf8");
        knownLinks.set(target, new Set([...text.matchAll(/ id="([^"]+)"/g)].map(match => match[1])));
      }
      assert(knownLinks.get(target).has(url.hash.slice(1)), `${file}: missing fragment ${value}`);
    }
  }
}

const caseIndex = content("cases/index.html");
const sitesCSV = content("data/b2b-site-links.csv");
const localeCSV = content("data/localized-country-sites.csv");
assert.doesNotMatch(sitesCSV, internalLabels);
assert.doesNotMatch(localeCSV, internalLabels);
let localeCount = 0;
for (const item of cases) {
  const html = content(`cases/${item.id}/index.html`);
  const industry = content(`industries/${item.industry}/index.html`);
  const renderedDomains = [...html.matchAll(/<li class="site-item" data-domain="([^"]+)"/g)].map(match => match[1]);
  const domains = item.sites.map(site => registeredDomain(site.url));
  assert(domains.length >= minimumSites, item.id);
  assert.equal(new Set(domains).size, domains.length, item.id);
  assert.deepEqual(renderedDomains, domains, item.id);
  assert(html.indexOf('id="site-links"') < html.indexOf("网站如何分工"), item.id);
  assert.match(html, /<details class="case-sources" id="sources">/, item.id);
  for (const site of item.sites) {
    const destination = `href="${site.url.replaceAll("&", "&amp;")}"`;
    for (const page of [html, industry, caseIndex]) {
      assert(page.includes(destination), `${item.id} missing site link ${site.domain}`);
    }
    assert(html.includes(`href="${site.evidenceUrl.replaceAll("&", "&amp;")}"`), `${item.id} missing site evidence ${site.domain}`);
    assert(sitesCSV.includes(`"${site.domain}","${site.url}"`), `${item.id} missing CSV row ${site.domain}`);
    if (site.countrySuffix) {
      assert(html.includes(`data-country-suffix="${site.countrySuffix}"`), `${item.id} missing country-domain metadata`);
      assert(localeCSV.includes(`"${site.domain}","${site.countrySuffix}","${site.url}"`), `${item.id} missing local-site CSV row ${site.domain}`);
      localeCount++;
    }
  }
  for (const entry of item.sources) {
    assert(html.includes(`href="${entry.url.replaceAll("&", "&amp;")}"`), `${item.id} missing source ${entry.label}`);
  }
}
assert(newCountryCases.every(item => item.sites.some(site => site.countrySuffix)), "New subject cases require a local-language country domain");
assert.equal(localeCSV.trim().split(/\r?\n/).length, localeCount + 1);
for (const item of industries) {
  const hasCases = cases.some(network => network.industry === item.id);
  assert.equal(content(`industries/${item.id}/index.html`).includes("data-coverage-gap"), !hasCases, item.id);
}
assert.equal(sitesCSV.trim().split(/\r?\n/).length, 1 + cases.reduce((sum, item) => sum + item.sites.length, 0));
assert.equal(content("data/export-metrics.csv").trim().split(/\r?\n/).length, 1 + industries.reduce((sum, item) => sum + item.metrics.length, 0));
assert.match(content("404.html"), /name="robots" content="noindex"/);
console.log(`Checked ${htmlFiles.length} HTML pages, four-domain admission, per-site evidence, and 3 CSV downloads.`);
