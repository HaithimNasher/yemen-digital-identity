import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestNationalDashboardV2(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(
            (ROOT/"site/data/national-dashboard.json").read_text(encoding="utf-8")
        )

    def test_status(self):
        self.assertEqual(self.data["status"],"DEVELOPMENT_DASHBOARD")

    def test_gcc_count(self):
        self.assertEqual(self.data["gcc"]["countries"],6)

    def test_directory_counts(self):
        self.assertEqual(self.data["directory"]["by_sector"]["ministries"],26)
        self.assertEqual(self.data["directory"]["by_sector"]["universities"],21)
        self.assertEqual(self.data["directory"]["entities_total"],47)

    def test_policy_count(self):
        self.assertGreaterEqual(self.data["policies"]["count"],13)

    def test_milestones(self):
        ids={x["id"] for x in self.data["milestones"]}
        self.assertTrue(
            {"gcc","namespace","directory","registry","eligibility",
             "policies","observatory","search","dashboard"}.issubset(ids)
        )

    def test_dashboard_page(self):
        html=(ROOT/"site/national-dashboard.html").read_text(encoding="utf-8")
        self.assertIn("National Observatory Dashboard",html)

if __name__=="__main__":
    unittest.main()
