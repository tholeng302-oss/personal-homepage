import json
from pathlib import Path
import unittest
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


class WeeklyIntelligenceTest(unittest.TestCase):
    def test_every_clean_energy_topic_has_at_most_three_safe_source_entries(self):
        data = json.loads((ROOT / "data/weekly-intelligence.json").read_text())

        for topic in data["topics"]:
            self.assertLessEqual(len(topic["items"]), 3, topic["id"])
            self.assertGreaterEqual(len(topic["sources"]), 2, topic["id"])
            for item in topic["items"]:
                self.assertIn(urlparse(item["url"]).scheme, {"http", "https"})
                self.assertTrue(item["source"])
                self.assertTrue(item["publishedAt"])

    def test_weekly_workflow_only_updates_this_repositorys_data_file(self):
        workflow = (ROOT / ".github/workflows/weekly-intelligence.yml").read_text()

        self.assertIn("scripts/update-weekly-intelligence.mjs", workflow)
        self.assertIn("git add data/weekly-intelligence.json", workflow)
        self.assertNotIn("my-life-finance-ai-scenery", workflow)

    def test_public_intelligence_pages_have_no_life_site_navigation(self):
        for filename in ("index.html", "intelligence.html", "framework.html"):
            page = (ROOT / filename).read_text()
            self.assertNotIn("memories.html", page, filename)
            self.assertNotIn("family.html", page, filename)


if __name__ == "__main__":
    unittest.main()
