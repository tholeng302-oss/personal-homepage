import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const dataPath = resolve("data/weekly-intelligence.json");
const maximumItems = 3;

function decodeXml(value) {
  return value
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/<[^>]*>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function getTag(block, tagName) {
  const match = block.match(new RegExp(`<${tagName}[^>]*>([\\s\\S]*?)</${tagName}>`, "i"));
  return match ? decodeXml(match[1]) : "";
}

function getLink(block) {
  const atomLink = block.match(/<link[^>]+href=["']([^"']+)["'][^>]*>/i);
  if (atomLink) return decodeXml(atomLink[1]);
  return getTag(block, "link");
}

function parseFeed(xml) {
  const blocks = xml.match(/<(?:item|entry)\b[\s\S]*?<\/(?:item|entry)>/gi) || [];
  return blocks.map((block) => ({
    title: getTag(block, "title"),
    url: getLink(block),
    publishedAt: getTag(block, "pubDate") || getTag(block, "published") || getTag(block, "updated"),
    summary: getTag(block, "description") || getTag(block, "summary")
  })).filter((item) => item.title && item.url);
}

function toPublishedDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? new Date().toISOString().slice(0, 10) : date.toISOString().slice(0, 10);
}

function normalizeEntries(entries, topic) {
  return entries.slice(0, maximumItems).map((entry) => ({
    title: entry.title,
    titleEn: entry.title,
    summary: `来自 ${topic.name} 监测网络的本周更新，请访问原文了解详情。`,
    summaryEn: `This week’s update from the ${topic.nameEn} monitoring network. Open the source for full details.`,
    source: "Google News RSS",
    url: entry.url,
    publishedAt: toPublishedDate(entry.publishedAt),
    kind: "新闻"
  }));
}

async function refreshTopic(previousTopic) {
  try {
    const feedUrl = previousTopic.feeds?.[0];
    if (!feedUrl) return previousTopic;

    const response = await fetch(feedUrl, { headers: { "User-Agent": "PeterObservatory/1.0" } });
    if (!response.ok) throw new Error(`Feed request failed: ${response.status}`);

    const entries = parseFeed(await response.text());
    if (!entries.length) throw new Error("Feed contained no valid entries");

    return { ...previousTopic, items: normalizeEntries(entries, previousTopic) };
  } catch (error) {
    return { ...previousTopic, items: previousTopic.items };
  }
}

const previousData = JSON.parse(await readFile(dataPath, "utf8"));
const refreshedTopics = await Promise.all(previousData.topics.map(refreshTopic));
const nextData = { ...previousData, updatedAt: new Date().toISOString(), topics: refreshedTopics };

await writeFile(dataPath, `${JSON.stringify(nextData, null, 2)}\n`);
