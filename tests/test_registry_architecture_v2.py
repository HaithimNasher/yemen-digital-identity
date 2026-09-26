import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestRegistryArchitectureV2(unittest.TestCase):
    def setUp(self):
        self.model=json.loads(
            (ROOT/"data/registry/registry-model.json").read_text(encoding="utf-8")
        )
        self.life=json.loads(
            (ROOT/"data/registry/domain-lifecycle.json").read_text(encoding="utf-8")
        )
        self.acc=json.loads(
            (ROOT/"data/registry/registrar-accreditation.json").read_text(encoding="utf-8")
        )

    def test_model_is_explicitly_draft(self):
        self.assertEqual(self.model["status"],"DRAFT_ARCHITECTURE")

    def test_core_actors(self):
        actors={x["id"] for x in self.model["actors"]}
        self.assertTrue(
            {"registry","registrar","registrant","policy-authority"}.issubset(actors)
        )

    def test_security_controls(self):
        controls=set(self.model["security_controls"])
        self.assertIn("MFA for privileged users",controls)
        self.assertIn("least-privilege RBAC",controls)
        self.assertIn("tamper-evident audit logs",controls)

    def test_lifecycle_states(self):
        states={x["id"] for x in self.life["states"]}
        expected={
            "AVAILABLE","PENDING_CREATE","ACTIVE","SUSPENDED",
            "EXPIRED_GRACE","REDEMPTION","PENDING_DELETE",
            "DELETED","RESERVED"
        }
        self.assertEqual(states,expected)

    def test_lifecycle_timers_are_unset(self):
        self.assertIsNone(self.life["timers"]["grace_days"])
        self.assertIsNone(self.life["timers"]["redemption_days"])
        self.assertIsNone(self.life["timers"]["pending_delete_days"])

    def test_accreditation_flow(self):
        stages=self.acc["accreditation_stages"]
        self.assertEqual(stages[0],"application")
        self.assertEqual(stages[-1],"continuous_compliance")

    def test_page_exists(self):
        html=(ROOT/"site/registry-model.html").read_text(encoding="utf-8")
        self.assertIn("Registry / Registrar Architecture",html)

if __name__=="__main__":
    unittest.main()
