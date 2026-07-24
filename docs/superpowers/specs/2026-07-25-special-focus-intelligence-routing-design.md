# Special Focus and Intelligence Routing Design

## Goal

Reorganize the homepage so that `特别关注` is a compact public brief for artificial intelligence and scenery/cultural landscapes, while the green-energy and investment topics are presented through the existing `绿色能源与投资情报台`.

## Information Architecture

### 特别关注

- Rename the navigation label and section title from `关注方向` to `特别关注`.
- Retain only the `人工智能` and `风景与文化景观` weekly brief cards.
- Do not duplicate source links in this section. It remains a concise current-information view with at most three items per retained topic.

### 绿色能源与投资情报台

- `绿色燃料周报` receives `绿色甲醇`, `可持续航空燃料`, and `绿氨` content. Its existing weekly cadence applies.
- `股市与碳交易观察` receives `全球主要股市` and `碳排放交易` content. Its existing daily/weekly cadence applies.
- `氢能与沼气月度观察` receives `绿色氢能` and `沼气与生物甲烷` content. Its existing monthly cadence applies.
- Rename `全球信息源调度台` to `全球信息资源调度台`, retaining its planned cadence.

### Global Source Directory

- Move every authority-source link from the former focus data set into the `全球信息资源调度台` area.
- Display sources grouped by all nine subject areas: AI, hydrogen, ammonia, methanol, SAF, biogas, global equities, carbon markets, and scenery/cultural landscapes.
- Source links open in a new tab and are maintained only once in the page data.

## Data and Rendering

- Keep a single `weekly-intelligence.json` data source and the existing GitHub Actions update job.
- Add a topic-to-desk mapping in the client renderer.
- Filter the weekly data shown in `特别关注` to AI and scenery.
- Render the remaining topics into their designated intelligence cards and render all source directories in the global information-resource desk.
- Preserve the current maximum of three published items per topic.

## Verification

- Automated tests assert the special-focus filter, the three desk mappings, the source-directory placement, and the renamed labels.
- Existing editorial and weekly-intelligence tests continue to pass.
- Review the deployed homepage at desktop and mobile widths after publishing.
