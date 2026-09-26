import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/"scripts/observatory_probe.py"

spec=importlib.util.spec_from_file_location("observatory_probe",ENGINE)
obs=importlib.util.module_from_spec(spec)
spec.loader.exec_module(obs)

class TestObservatoryV2(unittest.TestCase):
    def test_targets_exist(self):
        d=json.loads(
            (ROOT/"data/observatory/targets.json").read_text(encoding="utf-8")
        )
        domains={x["domain"] for x in d["targets"]}
        self.assertIn("ye",domains)
        self.assertIn("gov.ye",domains)
        self.assertIn("edu.ye",domains)

    def test_proposed_university_domains_not_in_targets(self):
        t=json.loads(
            (ROOT/"data/observatory/targets.json").read_text(encoding="utf-8")
        )
        u=json.loads(
            (ROOT/"data/entities/universities.json").read_text(encoding="utf-8")
        )
        targets={x["domain"] for x in t["targets"]}
        proposed={x["suggested_ye_domain"] for x in u["entities"]}
        self.assertTrue(targets.isdisjoint(proposed))

    def test_rdap_404_not_called_available(self):
        class Fake404(Exception):
            pass

        # Contract check: the literal output vocabulary must not use AVAILABLE
        src=ENGINE.read_text(encoding="utf-8")
        self.assertIn("NOT_FOUND_IN_RDAP",src)
        self.assertNotIn('"AVAILABLE"',src)

    def test_summary(self):
        sample=[
            {
                "dns":{"a":["1.2.3.4"],"aaaa":[],"dnssec_evidence":"DS_PRESENT"},
                "tls":{"certificate_valid":True},
                "http":{"status":200},
                "rdap":{"status":"FOUND"}
            },
            {
                "dns":{"a":[],"aaaa":["2001:db8::1"],"dnssec_evidence":"NO_SIGNING_EVIDENCE_OBSERVED"},
                "tls":{"certificate_valid":False},
                "http":{"status":None},
                "rdap":{"status":"NOT_FOUND_IN_RDAP"}
            }
        ]
        s=obs.build_summary(sample)
        self.assertEqual(s["targets_checked"],2)
        self.assertEqual(s["dns_ipv4_present"],1)
        self.assertEqual(s["dns_ipv6_present"],1)
        self.assertEqual(s["rdap_found"],1)

    def test_page_exists(self):
        html=(ROOT/"site/observatory.html").read_text(encoding="utf-8")
        self.assertIn("Live DNS / RDAP / TLS Observatory",html)

if __name__=="__main__":
    unittest.main()
