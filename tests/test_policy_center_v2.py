import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestPolicyCenterV2(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(
            (ROOT/"data/policies/catalog.json").read_text(encoding="utf-8")
        )
        self.rows=self.data["policies"]

    def test_catalog_is_draft(self):
        self.assertEqual(self.data["status"],"DRAFT_POLICY_LIBRARY")

    def test_policy_count(self):
        self.assertGreaterEqual(len(self.rows),13)

    def test_required_policies(self):
        ids={x["id"] for x in self.rows}
        expected={
            "registration","eligibility","registrar-accreditation",
            "reserved-names","domain-lifecycle","privacy-rdap",
            "whois-transition","abuse","disputes","transfer",
            "renewal-expiry","dnssec","idn"
        }
        self.assertTrue(expected.issubset(ids))

    def test_files_exist(self):
        for row in self.rows:
            self.assertTrue((ROOT/row["file"]).exists(),row["file"])

    def test_idn_is_research_draft(self):
        row=next(x for x in self.rows if x["id"]=="idn")
        self.assertEqual(row["status"],"RESEARCH_DRAFT")

    def test_policy_center_page(self):
        html=(ROOT/"site/policy-center.html").read_text(encoding="utf-8")
        self.assertIn("Policy Center",html)

if __name__=="__main__":
    unittest.main()
