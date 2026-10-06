const cleanEnergyDesks = [
  {
    id: "green-fuels",
    label: "绿色燃料周报",
    cadence: "每周",
    scope: "绿色甲醇、SAF、绿色氨与绿色化工燃料的项目、政策和交易动态",
    topicIds: ["methanol", "saf", "ammonia"]
  },
  {
    id: "hydrogen-biogas",
    label: "氢能与沼气",
    cadence: "每月",
    scope: "氢能基础设施、沼气/生物甲烷项目、设备与政策信号",
    topicIds: ["hydrogen", "biogas"]
  },
  {
    id: "carbon-market",
    label: "碳交易观察",
    cadence: "每日/每周",
    scope: "国际主要碳交易市场的价格、规则、政策事件与价值线索",
    topicIds: ["carbon"]
  }
];

const state = { data: null, filter: "all" };

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

function hasSafeHttpUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" || url.protocol === "http:";
  } catch {
    return false;
  }
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "等待可靠来源更新";
  return new Intl.DateTimeFormat("zh-CN", { year: "numeric", month: "short", day: "numeric" }).format(date);
}

function renderNewsItem(item, heading = "h4") {
  const source = escapeHtml(item.source || "来源待确认");
  const publishedAt = escapeHtml(item.publishedAt || "日期待确认");
  const sourceLink = hasSafeHttpUrl(item.url)
    ? `<a class="focus-source-link" href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">查看原文 <span aria-hidden="true">↗</span></a>`
    : `<span class="focus-source-link is-muted">等待可靠来源更新</span>`;

  return `
    <article class="focus-item">
      <span class="tag">${escapeHtml(item.kind || "新闻")}</span>
      <${heading}>${escapeHtml(item.title)}</${heading}>
      <p>${escapeHtml(item.summary)}</p>
      <div class="focus-item-footer"><span class="focus-item-meta">${source} · ${publishedAt}</span>${sourceLink}</div>
    </article>
  `;
}

function topicsFor(desk) {
  if (!state.data?.topics) return [];
  const accepted = new Set(desk.topicIds);
  return state.data.topics.filter((topic) => accepted.has(topic.id));
}

function latestItems(topicIds, maximum = 3) {
  if (!state.data?.topics) return [];
  const accepted = new Set(topicIds);
  return state.data.topics
    .filter((topic) => accepted.has(topic.id))
    .flatMap((topic) => topic.items.map((item) => ({ item, topic })))
    .filter(({ item }) => hasSafeHttpUrl(item.url))
    .sort((left, right) => new Date(right.item.publishedAt) - new Date(left.item.publishedAt))
    .slice(0, maximum);
}

function renderFilters() {
  const container = document.getElementById("intel-filter-bar");
  if (!container) return;
  const filters = [{ id: "all", label: "全部信息" }, ...cleanEnergyDesks.map((desk) => ({ id: desk.id, label: desk.label }))];
  container.innerHTML = filters.map((filter) => `<button class="intel-filter" type="button" data-intel-filter="${filter.id}" aria-pressed="${state.filter === filter.id}">${filter.label}</button>`).join("");
}

function renderSignals() {
  const container = document.getElementById("intel-weekly-signals");
  if (!container) return;
  const items = latestItems(cleanEnergyDesks.flatMap((desk) => desk.topicIds));
  container.innerHTML = `
    <div class="intel-signals-heading"><p class="section-kicker">WEEKLY SIGNALS</p><h3>本周三条信号</h3></div>
    <div class="intel-signal-grid">${items.map(({ item, topic }) => `<article class="intel-signal-card"><p class="focus-topic-label">${escapeHtml(topic.name)}</p>${renderNewsItem(item)}</article>`).join("") || "<p>正在汇总可靠来源。</p>"}</div>
  `;
}

function renderDeskCards() {
  const container = document.getElementById("intel-live-briefs");
  if (!container) return;
  const visibleDesks = cleanEnergyDesks.filter((desk) => state.filter === "all" || state.filter === desk.id);
  container.innerHTML = visibleDesks.map((desk) => {
    const topics = topicsFor(desk);
    return `
      <article class="intel-card intel-live-card" id="${desk.id}">
        <div class="intel-topline"><span class="tag">${desk.cadence}</span><span class="tag">自动更新</span></div>
        <h3>${desk.label}</h3><p>${desk.scope}</p>
        <div class="intel-topic-briefs">${topics.map((topic) => `<section class="intel-topic-brief"><p class="focus-topic-label">${escapeHtml(topic.name)}</p><div class="focus-items">${topic.items.slice(0, 3).map((item) => renderNewsItem(item)).join("")}</div></section>`).join("")}</div>
      </article>
    `;
  }).join("");
}

function renderResourceDirectory() {
  const container = document.getElementById("global-resource-directory");
  if (!container || !state.data?.topics) return;
  container.innerHTML = `
    <div class="global-resource-heading"><p class="section-kicker">GLOBAL DIRECTORY</p><h3>全球清洁能源与碳资源台</h3><p>官方机构、项目公告、研究报告和碳市场信息来源</p></div>
    <div class="global-resource-grid">${state.data.topics.map((topic) => `<article class="global-resource-card"><p class="focus-topic-label">${escapeHtml(topic.name)}</p><div class="global-resource-links">${topic.sources.filter((source) => hasSafeHttpUrl(source.url)).map((source) => `<a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.name)} <span aria-hidden="true">↗</span></a>`).join("")}</div></article>`).join("")}</div>
  `;
}

function renderFramework() {
  const container = document.getElementById("framework-overview");
  if (!container) return;
  const sections = [
    { id: "framework-green-fuels", kicker: "01 · GREEN FUELS", title: "绿色燃料", copy: "绿色甲醇、SAF、绿色氨与绿色化工燃料的关键项目和政策。", topicIds: ["methanol", "saf", "ammonia"] },
    { id: "framework-hydrogen", kicker: "02 · HYDROGEN & BIOGAS", title: "氢能与沼气", copy: "氢能基础设施、生物甲烷、设备、项目与产业政策。", topicIds: ["hydrogen", "biogas"] },
    { id: "framework-carbon", kicker: "03 · CARBON MARKETS", title: "碳交易", copy: "国际碳市场的价格、规则、政策与价值判断。", topicIds: ["carbon"] }
  ];
  container.innerHTML = sections.map((section) => {
    const items = latestItems(section.topicIds);
    return `<section class="framework-overview-section" id="${section.id}"><div class="framework-overview-heading"><div><p class="section-kicker">${section.kicker}</p><h2>${section.title}</h2><p>${section.copy}</p></div><a href="intelligence.html">查看全部情报 <span aria-hidden="true">→</span></a></div><div class="framework-overview-news-grid">${items.map(({ item, topic }) => `<div class="framework-overview-news"><p class="focus-topic-label">${escapeHtml(topic.name)}</p>${renderNewsItem(item, "h3")}</div>`).join("") || "<p>正在汇总可靠来源。</p>"}</div></section>`;
  }).join("");
}

function renderAll() {
  const update = document.getElementById("focus-updated");
  if (update) update.textContent = state.data ? `最后成功更新 · ${formatDate(state.data.updatedAt)}` : "暂时无法载入更新，保留上次内容";
  renderFilters();
  renderSignals();
  renderDeskCards();
  renderResourceDirectory();
  renderFramework();
}

async function loadIntelligence() {
  try {
    const response = await fetch("data/weekly-intelligence.json");
    if (!response.ok) throw new Error("Unable to load intelligence");
    state.data = await response.json();
  } catch {
    state.data = null;
  }
  renderAll();
}

document.addEventListener("click", (event) => {
  const filter = event.target.closest("[data-intel-filter]");
  if (!filter) return;
  state.filter = filter.dataset.intelFilter || "all";
  renderAll();
});

loadIntelligence();
