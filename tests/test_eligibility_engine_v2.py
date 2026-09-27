import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ENGINE_PATH=ROOT/"scripts/eligibility_engine.py"

spec=importlib.util.spec_from_file_location("eligibility_engine", ENGINE_PATH)
engine=importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

class TestEligibilityEngineV2(unittest.TestCase):
    def test_government_with_evidence(self):
        r=engine.evaluate(
            "gov.ye",
            "government",
            ["institution_authorization","authorized_contact"]
        )
        self.assertEqual(r["decision"],"ELIGIBLE")

    def test_government_wrong_type(self):
        r=engine.evaluate("gov.ye","company",[])
        self.assertEqual(r["decision"],"NOT_ELIGIBLE")

    def test_government_missing_evidence(self):
        r=engine.evaluate("gov.ye","government",[])
        self.assertEqual(r["decision"],"REVIEW_REQUIRED")
        self.assertIn("institution_authorization",r["missing_evidence"])

    def test_education(self):
        r=engine.evaluate(
            "edu.ye",
            "university",
            ["education_license_or_authorization","authorized_contact"]
        )
        self.assertEqual(r["decision"],"ELIGIBLE")

    def test_commercial_needs_review(self):
        r=engine.evaluate(
            "com.ye",
            "company",
            ["commercial_identity","authorized_contact"]
        )
        self.assertEqual(r["decision"],"REVIEW_REQUIRED")

    def test_direct_ye_needs_review(self):
        r=engine.evaluate(".ye","company",[])
        self.assertEqual(r["decision"],"REVIEW_REQUIRED")

    def test_proposed_zone_cannot_be_approved(self):
        r=engine.evaluate(
            "med.ye",
            "healthcare_provider",
            ["healthcare_license","authorized_contact"]
        )
        self.assertEqual(r["decision"],"PROPOSED_ZONE")

    def test_idn_research_cannot_be_approved(self):
        r=engine.evaluate(".اليمن","individual",[])
        self.assertEqual(r["decision"],"PROPOSED_ZONE")

    def test_unknown_zone(self):
        r=engine.evaluate("unknown.ye","company",[])
        self.assertEqual(r["decision"],"UNKNOWN_ZONE")

    def test_rules_are_draft(self):
        d=json.loads(
            (ROOT/"data/eligibility/rules.json").read_text(encoding="utf-8")
        )
        self.assertEqual(d["status"],"DRAFT_POLICY_ENGINE")

if __name__=="__main__":
    unittest.main()
