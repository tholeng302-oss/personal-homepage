import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CleanEnergySiteBoundaryTest(unittest.TestCase):
    def test_clean_energy_data_contains_only_clean_energy_and_carbon_topics(self):
        """A wrongly retained finance, AI, or scenery feed must not publish here."""
        data = json.loads((ROOT / "data/weekly-intelligence.json").read_text())

        self.assertEqual(
            {topic["id"] for topic in data["topics"]},
            {"methanol", "saf", "ammonia", "hydrogen", "biogas", "carbon"},
        )

    def test_clean_energy_home_does_not_link_to_moved_life_sections(self):
        """Visitors must not be sent from the clean-energy site to old memory pages."""
        home = (ROOT / "index.html").read_text()

        self.assertIn("清洁的能源、化工信息网", home)
        self.assertNotIn('href="memories.html"', home)
        self.assertNotIn('href="family.html"', home)

    def test_clean_energy_site_does_not_ship_migrated_memory_pages(self):
        """A direct URL must not continue to expose the migrated time-box pages."""
        self.assertFalse((ROOT / "memories.html").exists())
        self.assertFalse((ROOT / "family.html").exists())

    def test_clean_energy_site_does_not_ship_migrated_memory_photos(self):
        """Public time-box images belong only to the separate life website."""
        for filename in (
            "assets/fengxian-tea-chant.jpg",
            "assets/xinjiang-2026-04-01.jpg",
            "assets/xinjiang-2026-04-02.jpg",
            "assets/xinjiang-2026-04-03.jpg",
            "assets/cape-breton-highlands-hero.png",
        ):
            self.assertFalse((ROOT / filename).exists(), filename)

    def test_clean_energy_intelligence_does_not_offer_equities_or_commodities_filters(self):
        """The public desk must retain carbon, but not the migrated market categories."""
        script = (ROOT / "script.js").read_text()

        self.assertIn('topicIds: ["carbon"]', script)
        self.assertNotIn('topicIds: ["stocks", "carbon", "commodities"]', script)


if __name__ == "__main__":
    unittest.main()
