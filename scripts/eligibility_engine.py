#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "data/eligibility/rules.json"

def load_rules():
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))

def evaluate(zone, applicant_type, evidence=None):
    evidence = set(evidence or [])
    data = load_rules()
    rules = {x["zone"]: x for x in data["zones"]}

    if zone not in rules:
        return {
            "zone": zone,
            "applicant_type": applicant_type,
            "decision": "UNKNOWN_ZONE",
            "missing_evidence": [],
            "reason_ar": "المنطقة غير معرفة في محرك أهلية YDII."
        }

    rule = rules[zone]

    if rule["namespace_status"] in {"PROPOSED", "RESEARCH"}:
        return {
            "zone": zone,
            "applicant_type": applicant_type,
            "decision": "PROPOSED_ZONE",
            "missing_evidence": [],
            "reason_ar": rule["reason_ar"]
        }

    if rule["rule_type"] == "manual-review":
        return {
            "zone": zone,
            "applicant_type": applicant_type,
            "decision": "REVIEW_REQUIRED",
            "missing_evidence": [],
            "reason_ar": rule["reason_ar"]
        }

    if applicant_type not in rule["allowed_applicant_types"]:
        return {
            "zone": zone,
            "applicant_type": applicant_type,
            "decision": rule["decision_if_not_matched"],
            "missing_evidence": [],
            "reason_ar": rule["reason_ar"]
        }

    required = set(rule["required_evidence"])
    missing = sorted(required - evidence)

    if missing:
        return {
            "zone": zone,
            "applicant_type": applicant_type,
            "decision": "REVIEW_REQUIRED",
            "missing_evidence": missing,
            "reason_ar": "نوع الجهة مناسب مبدئيًا، لكن مستندات الأهلية المطلوبة غير مكتملة."
        }

    return {
        "zone": zone,
        "applicant_type": applicant_type,
        "decision": rule["decision_if_matched"],
        "missing_evidence": [],
        "reason_ar": rule["reason_ar"]
    }

def main():
    parser = argparse.ArgumentParser(
        description="YDII draft eligibility evaluator"
    )
    parser.add_argument("--zone", required=True)
    parser.add_argument("--type", dest="applicant_type", required=True)
    parser.add_argument(
        "--evidence",
        default="",
        help="Comma-separated evidence identifiers"
    )
    args = parser.parse_args()

    evidence = [x.strip() for x in args.evidence.split(",") if x.strip()]
    print(json.dumps(
        evaluate(args.zone, args.applicant_type, evidence),
        ensure_ascii=False,
        indent=2
    ))

if __name__ == "__main__":
    main()
