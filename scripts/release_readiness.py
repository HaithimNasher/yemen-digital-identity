#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

REQUIRED=[
    "data/gcc/benchmark.json",
    "data/yemen/namespace-model.json",
    "data/directory/manifest.json",
    "data/registry/registry-model.json",
    "data/eligibility/rules.json",
    "data/policies/catalog.json",
    "data/audit/gcc-parity-requirements.json",
    "scripts/observatory_probe.py",
    "scripts/domain_search.py",
    "scripts/security_gate.py",
    "site/index.html",
    "site/national-dashboard.html",
    "site/gcc-parity-audit.html",
    ".github/workflows/ydii-v2-security-ci.yml"
]

def main():
    failures=[]

    for rel in REQUIRED:
        if not (ROOT/rel).exists():
            failures.append(f"missing: {rel}")

    audit_path=ROOT/"site/data/gcc-parity-audit.json"
    if audit_path.exists():
        audit=json.loads(audit_path.read_text(encoding="utf-8"))
        pending=[
            x["id"] for x in audit.get("requirements",[])
            if x.get("state") in {"PARTIAL","PLANNED"}
        ]
        if pending:
            failures.append("parity audit still incomplete: "+", ".join(pending))
    else:
        failures.append("missing parity audit output")

    p=subprocess.run(
        [sys.executable,"scripts/security_gate.py"],
        cwd=ROOT
    )
    if p.returncode:
        failures.append("security_gate.py failed")

    print("\nRelease Readiness")
    print("-----------------")
    if failures:
        for x in failures:
            print(" -",x)
        print("NOT READY")
        return 1

    print("PASS: all Step 13 release-readiness checks passed.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
