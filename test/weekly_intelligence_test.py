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
        self.assertEqual({topic["id"] for topic in data["topics"]}, expected_topic_ids)
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

    def test_topic_routing_contract(self):
        script = Path("script.js").read_text()

        self.assertIn('specialFocusTopicIds = new Set(["ai", "scenery"])', script)
        self.assertIn('green-fuels', script)
        self.assertIn('hydrogen-biogas', script)
        self.assertIn('markets-carbon', script)
        self.assertIn('global-resource-directory', script)

if __name__ == "__main__":
    unittest.main()
