import json
from pathlib import Path
import unittest


class WeeklyIntelligenceTest(unittest.TestCase):
    def test_each_topic_has_at_most_three_entries_and_sources(self):
        data = json.loads(Path("data/weekly-intelligence.json").read_text())

        self.assertGreaterEqual(len(data["topics"]), 9)
        for topic in data["topics"]:
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

    def test_topic_routing_contract(self):
        script = Path("script.js").read_text()

        self.assertIn('specialFocusTopicIds = new Set(["ai", "scenery"])', script)
        self.assertIn('green-fuels', script)
        self.assertIn('hydrogen-biogas', script)
        self.assertIn('markets-carbon', script)
        self.assertIn('global-resource-directory', script)

    def test_weekly_workflow_and_failure_preservation_exist(self):
        workflow = Path(".github/workflows/weekly-intelligence.yml").read_text()
        updater = Path("scripts/update-weekly-intelligence.mjs").read_text()

        self.assertIn("cron:", workflow)
        self.assertIn("update-weekly-intelligence.mjs", workflow)
        self.assertIn("previousTopic.items", updater)


if __name__ == "__main__":
    unittest.main()
