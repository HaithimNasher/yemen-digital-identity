import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestSecurityCIV2(unittest.TestCase):
    def test_security_workflow_exists(self):
        p=ROOT/".github/workflows/ydii-v2-security-ci.yml"
        self.assertTrue(p.exists())
        text=p.read_text(encoding="utf-8")
        self.assertIn("feat/ydii-professional-v2",text)
        self.assertIn("pull_request:",text)

    def test_security_gate_exists(self):
        text=(ROOT/"scripts/security_gate.py").read_text(encoding="utf-8")
        self.assertIn("PRIVATE_KEY_MARKERS",text)
        self.assertIn("NOT_FOUND_IN_RDAP",text)

    def test_release_gate_exists(self):
        text=(ROOT/"scripts/release_readiness.py").read_text(encoding="utf-8")
        self.assertIn("Release Readiness",text)

    def test_parity_security_is_covered(self):
        d=json.loads(
            (ROOT/"site/data/gcc-parity-audit.json").read_text(encoding="utf-8")
        )
        rows={x["id"]:x for x in d["requirements"]}
        self.assertEqual(rows["security-ci-gates"]["state"],"COVERED")

if __name__=="__main__":
    unittest.main()
