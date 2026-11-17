import { cpSync, mkdirSync, mkdtempSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { cases } from "../content/networks.mjs";
import { minimumSites, registeredDomain } from "../content/network-schema.mjs";
import { groups, industries, tradeTotal } from "../content/industries.mjs";
import { leadTypes, structures } from "../content/schema.mjs";

const root = fileURLToPath(new URL("../", import.meta.url));
const byIndustry = new Map(industries.map(item => [item.id, item]));
const activeStructures = Object.entries(structures).filter(([id]) => cases.some(item => item.structure === id));
const siteName = "中国外贸 B2B 站群案例库";
const number = new Intl.NumberFormat("zh-CN", { maximumFractionDigits: 2 });
const counts = {
  industries: industries.length,
  cases: cases.length,
  sites: new Set(cases.flatMap(item => item.sites.map(site => site.domain))).size,
  coveredIndustries: new Set(cases.map(item => item.industry)).size,
  localizedSites: cases.flatMap(item => item.sites).filter(site => site.countrySuffix).length,
};
const featured = ["hsg", "hengtong", "opple"].map(id => cases.find(item => item.id === id));
const nationalMetrics = industries.flatMap(industry => industry.metrics
  .filter(metric => metric.national).map(metric => ({ ...metric, industry }))
).sort((a, b) => b.amount - a.amount);
const sectorMetrics = industries.flatMap(industry => industry.metrics
  .filter(metric => !metric.national).map(metric => ({ ...metric, industry }))
);

function escape(value) {
  const characters = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  return String(value).replace(/[&<>"']/g, char => characters[char]);
}

function link(href, label, className = "") {
  return `<a href="${escape(href)}"${className ? ` class="${escape(className)}"` : ""}${href.endsWith(".csv") ? " download" : ""}>${escape(label)}</a>`;
}

function external(href, label, className = "") {
  return `<a href="${escape(href)}" class="external ${escape(className)}" target="_blank" rel="noopener noreferrer">${escape(label)} <span aria-hidden="true">↗</span><span class="sr-only">（在新标签页打开）</span></a>`;
}

function iconArrow() {
  return `<span class="arrow" aria-hidden="true">→</span>`;
}

function button(href, label, secondary = false) {
  return `<a class="button${secondary ? " button-secondary" : ""}" href="${escape(href)}">${escape(label)}${iconArrow()}</a>`;
}

function industryPath(item) { return `/industries/${item.id}/`; }
function casePath(item) { return `/cases/${item.id}/`; }
function signed(growth) { return `${growth > 0 ? "+" : growth < 0 ? "−" : ""}${number.format(Math.abs(growth))}%`; }
function ownCases(industry) { return cases.filter(item => item.industry === industry.id); }

function frame({ title, description, current, content, script = false, robots = "" }) {
  const navigation = [{ id: "industries", url: "/industries/", label: "品类研究" }, { id: "cases", url: "/cases/", label: "站群案例" }];
  const nav = navigation.map(item => `<a href="${item.url}"${current === item.id ? ' aria-current="page"' : ""}>${item.label}</a>`).join("");
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escape(title)}</title>
  <meta name="description" content="${escape(description)}">
  <meta name="theme-color" content="#101e38">
  ${robots ? `<meta name="robots" content="${robots}">` : ""}
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css">
  ${script ? '<script src="/assets/filters.js" defer></script>' : ""}
</head>
<body>
  <a class="skip" href="#main">跳到正文</a>
  <header class="site-header">
    <div class="shell header-inner">
      <a class="brand" href="/" aria-label="出口站群研究首页"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>出口站群<span class="brand-tag">研究</span></span></a>
      <nav class="nav" aria-label="网站导航">${nav}</nav>
      ${link("/data/b2b-site-links.csv", "下载数据", "nav-download")}
    </div>
  </header>
  <main id="main">${content}</main>
  <footer class="site-footer">
    <div class="shell foot-layout">
      <div><a class="brand foot-brand" href="/"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>出口站群<span class="brand-tag">研究</span></span></a>
      <p>按中国出口品类研究工厂与外贸公司的独立站。</p></div>
      <div class="foot-links">${link("/industries/", "品类研究")}${link("/cases/", "站群案例")}${link("/methodology/", "收录标准")}${link("/data/b2b-site-links.csv", "案例网址 CSV")}</div>
    </div>
  </footer>
</body>
</html>
`;
}

function crumb(items) {
  const values = [{ url: "/", label: "首页" }, ...items];
  return `<nav class="crumb" aria-label="当前位置"><ol>${values.map(item => `<li>${item.url ? link(item.url, item.label) : `<span aria-current="page">${escape(item.label)}</span>`}</li>`).join("")}</ol></nav>`;
}

function intro(kicker, title, description, crumbs = "") {
  return `<div class="page-intro"><div class="shell">${crumbs}${kicker ? `<p class="eyebrow">${escape(kicker)}</p>` : ""}<h1>${escape(title)}</h1><p class="page-deck">${escape(description)}</p></div></div>`;
}

function countLine() {
  const fields = [
    [number.format(tradeTotal / 10000), "万亿元", "2025 年中国货物出口"],
    [counts.industries, "个", "研究行业与品类"],
    [counts.cases, "组", "企业站群 · 每组至少 4 站"],
    [counts.sites, "个", "独立网站"],
  ];
  return `<dl class="stats shell">${fields.map(([value, unit, label]) => `<div><dt>${escape(label)}</dt><dd>${value}<span>${unit}</span></dd></div>`).join("")}</dl>`;
}

function tradeChart(metrics, className = "") {
  return `<ol class="trade-bars ${className}">${metrics.map(item => `<li>
    <a href="${industryPath(item.industry)}"><span>${escape(item.item)}</span><b>${number.format(item.amount)}</b></a>
    <meter min="0" max="${nationalMetrics[0].amount}" value="${item.amount}" aria-label="${escape(item.item + "出口额，亿元")}">${number.format(item.amount)}</meter>
  </li>`).join("")}</ol>`;
}

function domainList(item) {
  return `<ul class="domain-list" aria-label="${escape(item.name)}的独立网站">${item.sites.map(site => `<li>${external(site.url, site.domain, site.countrySuffix ? "local-domain" : "")}</li>`).join("")}</ul>`;
}

function card(item) {
  const industry = byIndustry.get(item.industry);
  const localSites = item.sites.filter(site => site.countrySuffix).length;
  const searchable = [item.name, item.english, item.title, item.summary, industry.name, ...item.sites.map(site => [site.market, site.language, site.operator, site.role, site.domain].join(" "))].join(" ");
  return `<article class="case-card" data-card data-case="${item.id}" data-industry="${escape(item.industry)}" data-structure="${escape(item.structure)}" data-lead="${escape(item.lead)}" data-local="${localSites ? "1" : "0"}" data-index="${escape(searchable)}">
    <div class="case-card-copy">
      <div class="card-meta"><span class="tag">${item.sites.length} 个独立网站</span>${localSites ? `<span class="tag locale-tag">${localSites} 个本地语言国家域</span>` : ""}<span>${escape(industry.name)}</span></div>
      <h3>${link(casePath(item) + "#site-links", item.name)}</h3>
      <p class="case-card-title">${escape(item.title)}</p>
      <p>${escape(item.summary)}</p>
      ${link(casePath(item) + "#site-links", "查看完整案例 →", "strong-link")}
    </div>
    ${domainList(item)}
  </article>`;
}

function industryCard(item) {
  const metric = item.metrics[0];
  return `<article class="industry-card" data-card data-group="${escape(item.group)}">
    <div class="card-meta">${escape(groups[item.group])}</div>
    <h3><a href="${industryPath(item)}">${escape(item.name)}${iconArrow()}</a></h3>
    <p>${escape(metric?.item ?? item.scope)}</p>
    <div class="industry-card-bottom">${metric ? `<span class="fig-small">${number.format(metric.amount)} <span>${escape(metric.unit)}</span></span>` : ""}<span>${ownCases(item).length ? `${ownCases(item).length} 组站群` : "暂无案例"}</span></div>
  </article>`;
}

function home() {
  return frame({
    title: siteName,
    description: "按中国出口品类查看工厂和外贸公司的站群。每家企业或集团至少四个独立网站，逐站列出网址、市场、运营主体和证据。",
    content: `<section class="hero shell">
      <div class="hero-copy">
        <p class="eyebrow"><span class="signal"></span> 中国出口品类研究 <span class="hero-year">2025</span></p>
        <h1>中国外贸 B2B<br><span>站群案例库</span></h1>
        <p class="hero-deck">每家企业或集团至少有 4 个独立网站。按出口品类查企业，打开站点清单看每个网站服务的市场、业务和运营方。</p>
        <div class="actions">${button("/cases/", "查看企业站群")}${button("/cases/?local=1", "找本地语言国家域名", true)}</div>
      </div>
      <figure class="hero-media">
        <img src="/images/container-port.webp" alt="蓝调晨光下的集装箱港口示意图" width="1400" height="933" fetchpriority="high">
        <figcaption><span>港口示意</span><span>贸易规模与企业样本</span></figcaption>
      </figure>
    </section>
    <div class="stats-wrap">${countLine()}</div>
    <section class="shell section home-explore">
      <div class="chart-panel">
        <div class="section-heading"><div><p class="eyebrow">出口数据 / 2025</p><h2>重点商品出口额</h2></div><span class="subtle">人民币亿元</span></div>
        ${tradeChart(nationalMetrics.slice(0, 6))}
        <div class="panel-footer"><p>选自国家统计局公报表 11。<br>条形按同一金额刻度绘制。</p>${link("/industries/#trade", "查看完整数据 →", "strong-link")}</div>
      </div>
      <div>
        <div class="section-heading"><h2>企业站群示例</h2></div>
        <div class="featured-list">${featured.map(item => `<article class="feature"><div class="feature-heading"><h3>${link(casePath(item) + "#site-links", item.name)}</h3><span class="tag">${item.sites.length} 个站</span></div>${domainList(item)}</article>`).join("")}</div>
        ${link("/cases/", "浏览全部站群 →", "strong-link featured-end")}
      </div>
    </section>
    <section class="section industry-strip">
      <div class="shell">
        <div class="section-heading"><div><p class="eyebrow">产业入口</p><h2>按产品找对标</h2></div>${link("/industries/", "查看全部品类 →", "strong-link")}</div>
        <div class="industry-map">${Object.entries(groups).map(([group, label]) => `<section><h3>${escape(label)}</h3><ul>${industries.filter(item => item.group === group).map(item => `<li>${link(industryPath(item), item.name)}${iconArrow()}</li>`).join("")}</ul></section>`).join("")}</div>
      </div>
    </section>`,
  });
}

function industriesIndex() {
  const introContent = intro("出口数据与企业站群", "按行业和品类查看研究", `查看重点商品的出口额，以及各行业的采购需求和网站分工。${counts.coveredIndustries} 个行业与品类已有符合四站门槛的企业清单。`, crumb([{ label: "品类研究" }]));
  const columns = `<thead><tr><th scope="col">商品统计项</th><th scope="col">2025 年出口额</th><th scope="col">金额同比</th><th scope="col">数据来源</th></tr></thead>`;
  const metricsTable = (metrics, label) => `<div class="table-scroll" tabindex="0" role="region" aria-label="${escape(label)}"><table>${columns}<tbody>${metrics.map(metric => `<tr><td>${link(industryPath(metric.industry), metric.item, "strong-link")}</td><td class="table-number">${number.format(metric.amount)} ${escape(metric.unit)}</td><td><span class="change">${signed(metric.growth)}</span></td><td>${external(metric.source, metric.publisher)}</td></tr>`).join("")}</tbody></table></div>`;
  return frame({
    title: `行业与品类研究 | ${siteName}`, description: `${counts.industries} 个行业与品类的采购逻辑、中国工厂与外贸独立站案例及重点商品出口数据。`,
    current: "industries", script: true,
    content: introContent + `<section class="section shell" id="categories">
      <div class="section-heading"><h2>选择产业与品类</h2><span class="subtle">${counts.industries} 个研究入口</span></div>
      <div class="group-filter" data-group-filter aria-label="按产业筛选" hidden>
        <button type="button" data-group-choice="" aria-pressed="true">全部</button>
        ${Object.entries(groups).map(([id, label]) => `<button type="button" data-group-choice="${escape(id)}" aria-pressed="false">${escape(label)}</button>`).join("")}
      </div>
      <div class="industry-grid" data-group-grid>${industries.map(industryCard).join("")}</div>
    </section>
    <section class="section section-border shell" id="trade">
      <div class="section-heading"><div><p class="eyebrow">2025 年 / 全年</p><h2>重点商品出口数据</h2></div>${link("/data/export-metrics.csv", "下载统计表 ↓", "strong-link")}</div>
      <p class="prose intro-note">国家统计局公报列示的商品项按出口金额排序。行业报告列在下一张表，各自保留原币种和统计范围。</p>
      <h3 class="table-heading">国家统计局重点商品</h3>
      ${metricsTable(nationalMetrics, "国家统计局重点商品出口")}
      <h3 class="table-heading">补充行业口径</h3>
      ${metricsTable(sectorMetrics, "补充行业出口统计")}
    </section>`,
  });
}

function industryPage(industry) {
  const items = ownCases(industry);
  const siteCount = items.reduce((sum, item) => sum + item.sites.length, 0);
  return frame({
    title: `${industry.name}外贸站群研究 | ${siteName}`, description: industry.scope,
    current: "industries",
    content: intro(groups[industry.group], industry.name, industry.scope, crumb([{ url: "/industries/", label: "品类研究" }, { label: industry.name }]))
      + `<section class="section shell" id="networks">
        <div class="section-heading"><h2>企业站群</h2>${items.length ? `<span class="subtle">${items.length} 组 · ${siteCount} 个网站</span>` : ""}</div>
        ${items.length
          ? `<div class="network-list">${items.map(card).join("")}</div>`
          : `<div class="empty" data-coverage-gap><p>暂无收录案例。</p>${link("/cases/", "浏览案例 →", "strong-link")}</div>`}
      </section>
      <div class="shell detail-grid section section-border">
        <div>
          ${industry.metrics.length ? `<section aria-labelledby="trade-heading">
            <div class="section-heading"><h2 id="trade-heading">年度出口规模</h2><span class="subtle">2025 年</span></div>
            <div class="metric-grid">${industry.metrics.map(metric => `<div class="metric-card"><p>${escape(metric.item)}</p><div class="fig">${number.format(metric.amount)} <span>${escape(metric.unit)}</span></div><p class="subtle">金额同比 <span class="change">${signed(metric.growth)}</span></p><div class="metric-source">${external(metric.source, metric.publisher)}</div></div>`).join("")}</div>
          </section>` : ""}
          <section class="detail-block"><h2>买家根据什么作决定</h2><p>${escape(industry.buyer)}</p></section>
          ${industry.compare ? `<section class="detail-block"><h2>${items.length ? "本站案例如何分工" : "判断网站分工时看什么"}</h2><p>${escape(industry.compare)}</p></section>` : ""}
        </div>
        <aside class="guide-panel"><h2>工厂与外贸公司可以怎么借鉴</h2><p>${escape(industry.apply)}</p>${items.length ? link(`/cases/?industry=${industry.id}`, "筛选此品类 →", "strong-link") : ""}</aside>
      </div>`,
  });
}

function options(values) {
  return values.map(([id, label]) => `<option value="${escape(id)}">${escape(label)}</option>`).join("");
}

function casesIndex() {
  const preferred = ["chint", "hsg", "hengtong", "ztt", "opple", "leo", "sany", "yuto", "je-furniture"];
  const order = new Map(preferred.map((id, index) => [id, index]));
  const arranged = [...cases].sort((a, b) => (order.get(a.id) ?? preferred.length) - (order.get(b.id) ?? preferred.length));
  return frame({
    title: `B2B 站群与网站清单 | ${siteName}`, description: "筛选中国制造商和外贸公司的 B2B 站群。每组网站均可打开，案例详列市场和归属。",
    current: "cases", script: true,
    content: intro("制造商与外贸公司", "B2B 站群与网站清单", `每组至少 ${minimumSites} 个独立网站。点域名可直达原站，点企业名称可查各站用途和归属。`, crumb([{ label: "站群案例" }]))
    + `<section class="section shell" aria-label="案例筛选与结果">
      <form class="filters" data-case-filter role="search" hidden>
        <div><label for="q">搜索企业、国家或域名</label><input type="search" id="q" name="q" placeholder="例如 裕同、德国、sany.in"></div>
        <div><label for="industry">行业与品类</label><select id="industry" name="industry"><option value="">全部品类</option>${options(industries.map(item => [item.id, item.name]))}</select></div>
        <div><label for="structure">网站结构</label><select id="structure" name="structure"><option value="">全部结构</option>${options(activeStructures.map(([id, item]) => [id, item.name]))}</select></div>
        <div><label for="lead">采购入口</label><select id="lead" name="lead"><option value="">全部入口</option>${options(Object.entries(leadTypes))}</select></div>
        <div><label for="local">当地语言＋国家域名</label><select id="local" name="local"><option value="">全部案例</option><option value="1">含本地语言国家域</option></select></div>
        <button class="clear" type="reset">清除</button>
      </form>
      <div class="list-meta">
        <p aria-live="polite" data-result-count>显示 ${cases.length} 组站群</p>
        <div class="list-downloads">${link("/data/localized-country-sites.csv", "本地语言国家域名 CSV ↓", "strong-link")}${link("/data/b2b-site-links.csv", "全部网址 CSV ↓", "strong-link")}</div>
      </div>
      <p class="empty" data-empty hidden>没有符合当前条件的案例。可删掉部分关键词或清除筛选。</p>
      <div class="network-list" data-case-grid>${arranged.map(card).join("")}</div>
    </section>`,
  });
}

function casePage(item) {
  const industry = byIndustry.get(item.industry);
  const related = ownCases(industry).filter(other => other !== item);
  return frame({
    title: `${item.name}站群 · ${item.sites.length} 个独立网站 | ${siteName}`, description: item.summary,
    current: "cases",
    content: intro(industry.name + " / " + structures[item.structure].name, item.name, item.title, crumb([{url:"/cases/",label:"站群案例"},{url:industryPath(industry),label:industry.name},{label:item.name}]))
    + `<article class="shell section">
        <section id="site-links" aria-labelledby="site-list-heading">
          <div class="section-heading"><h2 id="site-list-heading">站群网站清单</h2><span class="tag list-total">${item.sites.length} 个独立网站</span></div>
          <ol class="site-list" role="list">${item.sites.map(site => `<li class="site-item" data-domain="${escape(site.domain)}">
             <div class="site-url">
               <h3>${external(site.url, site.domain, "site-domain")}</h3>
               <p class="site-address">${escape(site.url)}</p>
               <p class="site-market">${escape(site.market)} · ${escape(site.language)}${site.countrySuffix ? ` <span class="tag locale-tag" data-country-suffix="${site.countrySuffix}">${site.countrySuffix} 国家域</span>` : ""}</p>
             </div>
             <div class="site-role">
               <strong>${escape(site.role)}</strong>
               <p>${escape(site.observation)}</p>
             </div>
             <div class="site-owner">
               <span>${escape(site.operator)}</span>
               ${external(site.evidenceUrl, "归属依据", "strong-link")}
             </div>
          </li>`).join("")}</ol>
        </section>
        <div class="case-analysis" id="analysis">
          ${[["网站如何分工", item.pattern], ["采购路径", item.path], ["可借鉴的做法", item.insight]].map(([title, content]) => `<section class="detail-block"><h2>${escape(title)}</h2><p>${escape(content)}</p></section>`).join("")}
        </div>
        <details class="case-sources" id="sources">
          <summary>企业资料</summary>
          <ul class="source-list">${item.sources.map(source => `<li>${external(source.url, source.label, "strong-link")}</li>`).join("")}</ul>
        </details>
    </article>
    ${related.length ? `<section class="section shell section-border"><div class="section-heading"><h2>同品类站群</h2></div><div class="network-list">${related.map(card).join("")}</div></section>` : ""}`,
  });
}

function method() {
  return frame({
    title: `收录标准 | ${siteName}`, description: "中国外贸 B2B 站群案例的企业、网址与本地语言筛选标准。",
    current: "method",
    content: intro("", "收录标准", "面向海外采购的中国工厂、制造集团和外贸公司。", crumb([{ label: "收录标准" }]))
      + `<div class="shell section">
        <dl class="definition-list prose">
          <div><dt>企业站群</dt><dd>同一家企业或集团至少运营 ${minimumSites} 个有独立注册域的 B2B 网站。同一注册域下的语言版、目录与子域合计为一个网站。</dd></div>
          <div><dt>网站归属</dt><dd>通过企业官网、当地公司的法律声明或公开财务资料核对运营方。企业案例页列出逐站来源。</dd></div>
          <div><dt>小语种国家站</dt><dd>网站使用目标市场的国家域名，并提供当地非英语的业务内容。</dd></div>
        </dl>
        <div class="inline-links">${link("/cases/", "浏览站群案例 →", "strong-link")}${link("/cases/?local=1", "查看小语种国家站 →", "strong-link")}</div>
      </div>`,
  });
}

function write(rootPath, name, contents) {
  const target = join(rootPath, name);
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, contents);
}

function csv(rows) {
  return "\uFEFF" + rows.map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(",")).join("\r\n") + "\r\n";
}

function assertData() {
  const seen = new Set();
  for (const item of [...industries, ...cases]) {
    if (seen.has(item.id) || !/^[a-z0-9-]+$/.test(item.id)) throw Error(`Invalid or duplicate id: ${item.id}`);
    seen.add(item.id);
  }
  for (const item of industries) {
    if (!groups[item.group] || !item.scope || (!item.metrics.length && !ownCases(item).length)) throw Error(`Incomplete industry ${item.id}`);
    for (const metric of item.metrics) {
      if (!Number.isFinite(metric.amount) || !Number.isFinite(metric.growth)) throw Error(`Invalid metric ${metric.item}`);
    }
  }
  for (const item of cases) {
    if (!byIndustry.has(item.industry) || !structures[item.structure] || !leadTypes[item.lead]) throw Error(`Invalid case: ${item.id}`);
    if (item.sites.length < minimumSites || !item.sources.length || !item.insight) throw Error(`Incomplete case: ${item.id}`);
    const domains = new Set();
    for (const site of item.sites) {
      if (!site.operator || !site.role || !site.evidenceUrl || site.domain !== registeredDomain(site.url) || domains.has(site.domain)) {
        throw Error(`Missing evidence or duplicate domain in ${item.id}: ${site.domain}`);
      }
      domains.add(site.domain);
      if (site.countrySuffix && (!/^\.(?:[a-z]+\.)?[a-z]{2}$/u.test(site.countrySuffix) || site.countrySuffix === ".eu" || !site.domain.endsWith(site.countrySuffix))) {
        throw Error(`Invalid country suffix for ${site.domain}`);
      }
    }
    for (const href of [...item.sites.flatMap(site => [site.url, site.evidenceUrl]), ...item.sources.map(source => source.url)]) {
      const url = new URL(href);
      if (url.protocol !== "https:" || url.username || url.password || /token=|X-Amz-.*=|api-key=/i.test(url.search)) throw Error(`Unsafe or invalid URL in ${item.id}`);
    }
  }
}

assertData();
const tmp = mkdtempSync(join(root, ".stage-"));
try {
  cpSync(join(root, "public"), tmp, { recursive: true });
  write(tmp, "index.html", home());
  write(tmp, "industries/index.html", industriesIndex());
  for (const item of industries) write(tmp, `industries/${item.id}/index.html`, industryPage(item));
  write(tmp, "cases/index.html", casesIndex());
  for (const item of cases) write(tmp, `cases/${item.id}/index.html`, casePage(item));
  write(tmp, "methodology/index.html", method());
  write(tmp, "404.html", frame({
    title: `页面未找到 | ${siteName}`, description: "可从品类或案例索引查看有效入口。", robots: "noindex",
    content: `<section class="shell not-found"><h1>页面未找到</h1><p>从品类或案例索引继续查找。</p><div class="actions">${button("/industries/", "品类研究")}${button("/cases/", "浏览案例", true)}</div></section>`,
  }));
  write(tmp, "data/b2b-site-links.csv", csv([
    ["案例ID", "品类", "企业或集团", "该组独立网站数", "网站结构", "采购重点", "独立注册域", "网址", "市场", "语言", "运营方", "网站用途", "业务说明", "归属依据", "本地语言对应的国家域名后缀"],
    ...cases.flatMap(item => item.sites.map(site => [
      item.id, byIndustry.get(item.industry).name, item.name, item.sites.length, structures[item.structure].name, leadTypes[item.lead],
      site.domain, site.url, site.market, site.language, site.operator, site.role, site.observation, site.evidenceUrl, site.countrySuffix || "",
    ])),
  ]));
  write(tmp, "data/localized-country-sites.csv", csv([
    ["案例ID", "行业或品类", "企业或集团", "独立注册域", "国家域名后缀", "网址", "市场", "语言", "运营方", "用途", "归属依据"],
    ...cases.flatMap(item => item.sites.filter(site => site.countrySuffix).map(site => [
      item.id, byIndustry.get(item.industry).name, item.name, site.domain, site.countrySuffix, site.url,
      site.market, site.language, site.operator, site.role, site.evidenceUrl,
    ])),
  ]));
  write(tmp, "data/export-metrics.csv", csv([
    ["年度", "品类", "商品或行业口径", "金额", "单位", "金额同比%", "来源机构", "来源网址"],
    ...[...nationalMetrics, ...sectorMetrics].map(metric => ["2025", metric.industry.name, metric.item, metric.amount, metric.unit, metric.growth, metric.publisher, metric.source]),
  ]));
  rmSync(join(root, "dist"), { recursive: true, force: true });
  renameSync(tmp, join(root, "dist"));
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
console.log(JSON.stringify({ ...counts, exportIndicators: nationalMetrics.length + sectorMetrics.length, pages: industries.length + cases.length + 5 }));
