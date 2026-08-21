import json
from pathlib import Path
import unittest


class WeeklyIntelligenceTest(unittest.TestCase):
    def test_each_topic_has_at_most_three_entries_and_sources(self):
        data = json.loads(Path("data/weekly-intelligence.json").read_text())

        expected_topic_ids = {
            "ai",
            "hydrogen",
            "ammonia",
            "methanol",
            "saf",
            "biogas",
            "stocks",
            "carbon",
            "commodities",
            "scenery",
        }
        topic_ids = {topic["id"] for topic in data["topics"]}
        self.assertEqual(len(data["topics"]), 10)
        self.assertEqual(len(topic_ids), len(data["topics"]))
        self.assertEqual(topic_ids, expected_topic_ids)
        for topic in data["topics"]:
            self.assertTrue(
                {"name", "nameEn", "sources", "feeds", "items"}.issubset(topic),
                topic["id"],
            )
            self.assertTrue(topic["name"])
            self.assertTrue(topic["nameEn"])
            self.assertLessEqual(len(topic["items"]), 3)
            self.assertGreaterEqual(len(topic["sources"]), 2)
            self.assertTrue(
                all(item["url"] and item["publishedAt"] for item in topic["items"])
            )

    def test_page_has_focus_area_mount_and_data_loader(self):
        html = Path("intelligence.html").read_text()
        script = Path("script.js").read_text()

        self.assertIn('id="intel-live-briefs"', html)
        self.assertIn('fetch("data/weekly-intelligence.json")', script)

    def test_special_focus_and_intelligence_mounts_exist(self):
        html = Path("intelligence.html").read_text()
        script = Path("script.js").read_text()

        self.assertIn('id="intel-live-briefs"', html)
        self.assertIn('id="global-resource-directory"', html)
        self.assertIn('"特别关注"', script)
        self.assertIn('"全球信息资源调度台"', script)

    def test_english_resource_desk_uses_the_approved_visible_title(self):
        script = Path("script.js").read_text()

        self.assertIn('title: "Global Information Resource Dispatch Desk"', script)
        self.assertNotIn('title: "Global Intelligence Resource Desk"', script)

    def test_stylesheet_does_not_keep_the_unmounted_intel_grid_selector(self):
        stylesheet = Path("style.css").read_text()

        self.assertNotIn(".intel-grid", stylesheet)

    def test_topic_routing_contract(self):
        script = Path("script.js").read_text()

        self.assertIn('specialFocusTopicIds = new Set(["ai", "scenery"])', script)
        self.assertIn(
            '''const intelligenceDeskGroups = [
  { id: "green-fuels", topicIds: ["methanol", "saf", "ammonia"] },
  { id: "hydrogen-biogas", topicIds: ["hydrogen", "biogas"] },
  { id: "markets-carbon", topicIds: ["stocks", "carbon", "commodities"] }
];''',
            script,
        )
        self.assertIn('global-resource-directory', script)

    def test_intelligence_desk_cadences_are_explicit(self):
        script = Path("script.js").read_text()

        expected_cadences = {
            "green-fuels": ("每周", "Weekly"),
            "hydrogen-biogas": ("每月", "Monthly"),
            "markets-carbon": ("每日/每周", "Daily / Weekly"),
        }

        for desk_id, (chinese_cadence, english_cadence) in expected_cadences.items():
            for cadence in (chinese_cadence, english_cadence):
                self.assertRegex(
                    script,
                    rf'id: "{desk_id}",\s*title: "[^"]+",\s*cadence: "{cadence}"',
                )

    def test_every_news_item_has_a_direct_source_link(self):
        script = Path("script.js").read_text()

        self.assertIn("function renderNewsItem", script)
        self.assertIn('href="${escapeHtml(item.url)}"', script)
        self.assertIn('target="_blank" rel="noreferrer"', script)
        self.assertIn('查看原文', script)
        self.assertIn('Read source', script)

    def test_framework_page_mounts_all_four_public_overview_sections(self):
        html = Path("framework.html").read_text()
        script = Path("script.js").read_text()

        self.assertIn('id="framework-overview"', html)
        self.assertIn('href="#framework-energy"', html)
        self.assertIn('href="#framework-capital"', html)
        self.assertIn('href="#framework-scenery"', html)
        self.assertIn('href="#framework-memory"', html)
        self.assertIn('function renderFrameworkOverview', script)
        self.assertIn('id="framework-energy"', script)
        self.assertIn('id="framework-capital"', script)
        self.assertIn('id="framework-scenery"', script)
        self.assertIn('id="framework-memory"', script)
        self.assertIn('href="intelligence.html"', script)
        self.assertIn('href="memories.html"', script)
        self.assertIn('href="family.html"', script)

    def test_capital_overview_has_separate_equities_carbon_and_commodities_blocks(self):
        script = Path("script.js").read_text()

        self.assertIn('id: "framework-capital-equities"', script)
        self.assertIn('id: "framework-capital-carbon"', script)
        self.assertIn('id: "framework-capital-commodities"', script)
        self.assertIn('getOverviewTopicItems(data, ["stocks"])', script)
        self.assertIn('getOverviewTopicItems(data, ["carbon"])', script)
        self.assertIn('getOverviewTopicItems(data, ["commodities"])', script)

    def test_capital_market_renders_one_heading_and_one_kind_label_per_column(self):
        script = Path("script.js").read_text()

        self.assertIn("function renderCapitalItems", script)
        self.assertIn("renderCapitalItems(market.items, locale, emptyMessage)", script)
        self.assertNotIn("renderItems(market.items)", script)

    def test_special_focus_signal_copy_only_names_ai_and_cultural_landscapes(self):
        script = Path("script.js").read_text()

        self.assertIn(
            '{ label: "特别关注", value: "AI、风景/文化景观" }',
            script,
        )
        self.assertIn(
            '{ label: "Special focus", value: "AI, scenery/cultural landscapes" }',
            script,
        )

if __name__ == "__main__":
    unittest.main()
