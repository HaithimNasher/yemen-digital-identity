import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestYemenNamespaceModel(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"data/yemen/namespace-model.json").read_text(encoding="utf-8"))
        self.zones=self.data["zones"]

    def test_required_current_zones(self):
        m={x["zone"]:x["status"] for x in self.zones}
        self.assertEqual(m[".ye"],"CURRENT")
        self.assertEqual(m["gov.ye"],"RESTRICTED")
        self.assertEqual(m["edu.ye"],"RESTRICTED")
        self.assertEqual(m["com.ye"],"CURRENT")
        self.assertEqual(m["org.ye"],"CURRENT")
        self.assertEqual(m["net.ye"],"CURRENT")

    def test_proposals_not_current(self):
        m={x["zone"]:x["status"] for x in self.zones}
        for z in ["sch.ye","med.ye","name.ye","pro.ye","museum.ye"]:
            self.assertEqual(m[z],"PROPOSED")

    def test_idn_is_research(self):
        m={x["zone"]:x["status"] for x in self.zones}
        self.assertEqual(m[".اليمن"],"RESEARCH")

    def test_reserved_classes(self):
        self.assertGreaterEqual(len(self.data["reserved_name_classes"]),3)

    def test_page_exists(self):
        html=(ROOT/"site/namespace-model.html").read_text(encoding="utf-8")
        self.assertIn("YE Namespace Model",html)

if __name__=="__main__":
    unittest.main()
