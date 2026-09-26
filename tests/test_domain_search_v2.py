import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/"scripts/domain_search.py"

spec=importlib.util.spec_from_file_location("domain_search",ENGINE)
searchmod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(searchmod)

class FakeObs:
    @staticmethod
    def rdap_probe(domain,timeout):
        if domain=="taken.ye":
            return {"status":"FOUND","http_status":200}
        return {"status":"NOT_FOUND_IN_RDAP","http_status":404}

class TestDomainSearchV2(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(searchmod.normalize_label(" YemenAI "),"yemenai")

    def test_invalid_label(self):
        with self.assertRaises(ValueError):
            searchmod.normalize_label("-bad-")

    def test_reserved(self):
        cfg={"zone":".ye","mode":"LIVE_CHECK","namespace_status":"CURRENT"}
        r=searchmod.evaluate_candidate("login",cfg,live=False)
        self.assertEqual(r["search_state"],"RESERVED")

    def test_proposed(self):
        cfg={"zone":"med.ye","mode":"PROPOSED_ONLY","namespace_status":"PROPOSED"}
        r=searchmod.evaluate_candidate("clinic",cfg,live=False)
        self.assertEqual(r["search_state"],"PROPOSED_ZONE")

    def test_restricted(self):
        cfg={"zone":"gov.ye","mode":"RESTRICTED","namespace_status":"RESTRICTED"}
        r=searchmod.evaluate_candidate("agency",cfg,live=False)
        self.assertEqual(r["search_state"],"RESTRICTED")

    def test_rdap_found_registered(self):
        cfg={"zone":".ye","mode":"LIVE_CHECK","namespace_status":"CURRENT"}
        with patch.object(searchmod,"load_observatory",return_value=FakeObs):
            r=searchmod.evaluate_candidate("taken",cfg,live=True)
        self.assertEqual(r["search_state"],"REGISTERED")
        self.assertEqual(r["registration_availability"],"NOT_AVAILABLE_AS_NEW_REGISTRATION")

    def test_rdap_not_found_is_not_available(self):
        cfg={"zone":".ye","mode":"LIVE_CHECK","namespace_status":"CURRENT"}
        with patch.object(searchmod,"load_observatory",return_value=FakeObs):
            r=searchmod.evaluate_candidate("unknownname",cfg,live=True)
        self.assertEqual(r["search_state"],"NOT_FOUND_IN_RDAP")
        self.assertEqual(r["registration_availability"],"NOT_DETERMINED")

    def test_page_exists(self):
        html=(ROOT/"site/domain-search.html").read_text(encoding="utf-8")
        self.assertIn("Domain Search",html)

if __name__=="__main__":
    unittest.main()
