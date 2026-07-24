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
            "scenery",
        }
        topic_ids = {topic["id"] for topic in data["topics"]}
        self.assertEqual(len(data["topics"]), 9)
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
        html = Path("index.html").read_text()
        script = Path("script.js").read_text()

        self.assertIn('id="weekly-intelligence"', html)
        self.assertIn('fetch("data/weekly-intelligence.json")', script)

    def test_special_focus_and_intelligence_mounts_exist(self):
        html = Path("index.html").read_text()
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
  { id: "markets-carbon", topicIds: ["stocks", "carbon"] }
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

    def test_authority_source_links_are_rendered_only_in_global_directory(self):
        script = Path("script.js").read_text()
        global_directory_start = script.index('if (resourceDirectory && resourceDesk)')
        global_directory = script[global_directory_start:]
        item_rendering = script[:global_directory_start]

        self.assertEqual(script.count('topic.sources.map'), 1)
        self.assertIn('topic.sources.map', global_directory)
        self.assertNotIn('topic.sources.map', item_rendering)
        self.assertNotIn('<a class="focus-item"', item_rendering)
        self.assertNotIn('href="${escapeHtml(item.url)}"', item_rendering)
        self.assertIn('<article class="focus-item">', item_rendering)

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
