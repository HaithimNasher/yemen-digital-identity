#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads(
    (ROOT/"data/policies/catalog.json").read_text(encoding="utf-8")
)

required={
    "registration",
    "eligibility",
    "registrar-accreditation",
    "reserved-names",
    "domain-lifecycle",
    "privacy-rdap",
    "whois-transition",
    "abuse",
    "disputes",
    "transfer",
    "renewal-expiry",
    "dnssec",
    "idn",
}

rows=catalog["policies"]
ids={x["id"] for x in rows}

missing=required-ids
if missing:
    raise SystemExit(f"Missing required policies: {sorted(missing)}")

if len(ids) != len(rows):
    raise SystemExit("Duplicate policy IDs detected.")

for row in rows:
    p=ROOT/row["file"]
    if not p.exists():
        raise SystemExit(f"Policy file missing: {p}")
    text=p.read_text(encoding="utf-8")
    if "Status:" not in text:
        raise SystemExit(f"Policy status missing: {p}")

print("Policy Center validation passed.")
print("Policies:",len(rows))
print("Domains:",len({x['domain'] for x in rows}))
