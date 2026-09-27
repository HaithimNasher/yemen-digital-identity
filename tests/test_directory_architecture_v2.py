import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestDirectoryArchitectureV2(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads(
            (ROOT/"data/directory/manifest.json").read_text(encoding="utf-8")
        )

    def test_nine_sectors(self):
        self.assertEqual(len(self.manifest["sectors"]),9)

    def test_expected_sectors(self):
        got={x["id"] for x in self.manifest["sectors"]}
        expected={
            "ministries","universities","authorities","schools",
            "companies","banks","telecom","healthcare","organizations"
        }
        self.assertEqual(got,expected)

    def test_every_dataset_exists(self):
        for sector in self.manifest["sectors"]:
            self.assertTrue((ROOT/sector["dataset"]).exists(), sector["dataset"])

    def test_future_categories_are_empty_not_fake(self):
        for name in [
            "authorities","schools","companies","banks",
            "telecom","healthcare","organizations"
        ]:
            d=json.loads(
                (ROOT/f"data/entities/{name}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(d["entities"],[])

    def test_current_counts_preserved(self):
        m=json.loads(
            (ROOT/"data/entities/ministries.json").read_text(encoding="utf-8")
        )
        u=json.loads(
            (ROOT/"data/entities/universities.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(m["entities"]),26)
        self.assertEqual(len(u["entities"]),21)

    def test_directory_validator_exists(self):
        self.assertTrue((ROOT/"scripts/validate_directory.py").exists())

if __name__=="__main__":
    unittest.main()
