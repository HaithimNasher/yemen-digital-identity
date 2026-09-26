import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestGCCParityAuditV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable,str(ROOT/"scripts/gcc_parity_audit.py")],
            check=True
        )
        cls.data=json.loads(
            (ROOT/"site/data/gcc-parity-audit.json").read_text(encoding="utf-8")
        )

    def test_six_reference_countries(self):
        self.assertEqual(len(self.data["gcc_reference_countries"]),6)

    def test_not_a_ranking(self):
        self.assertIn("not a country ranking",self.data["methodology"].lower())

    def test_core_areas_covered(self):
        rows={x["id"]:x for x in self.data["requirements"]}
        for rid in [
            "national-cctld-model",
            "registry-registrar-separation",
            "registrar-accreditation",
            "namespace-eligibility",
            "reserved-names",
            "domain-lifecycle",
            "privacy-rdap",
            "dnssec",
            "domain-search",
            "policy-center",
            "bilingual-portal"
        ]:
            self.assertEqual(rows[rid]["state"],"COVERED",rid)

    def test_security_ci_is_partial_before_step13(self):
        rows={x["id"]:x for x in self.data["requirements"]}
        self.assertEqual(rows["security-ci-gates"]["state"],"PARTIAL")

    def test_page_exists(self):
        html=(ROOT/"site/gcc-parity-audit.html").read_text(encoding="utf-8")
        self.assertIn("GCC Parity Audit",html)

if __name__=="__main__":
    unittest.main()
