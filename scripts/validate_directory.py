#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/directory/manifest.json"

ALLOWED_VERIFY = {
    "verified-source",
    "user-provided",
    "screenshot-reference",
    "pending-verification",
}
ALLOWED_DOMAIN = {"CURRENT", "VERIFIED", "PROPOSED", "UNKNOWN", None}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    manifest = load(MANIFEST)
    seen_ids = set()
    total = 0

    for sector in manifest["sectors"]:
        path = ROOT / sector["dataset"]
        if not path.exists():
            raise SystemExit(f"Missing dataset: {path}")

        data = load(path)
        if data.get("category") != sector["id"]:
            raise SystemExit(
                f"Category mismatch: {path}: "
                f"{data.get('category')} != {sector['id']}"
            )

        rows = data.get("entities")
        if not isinstance(rows, list):
            raise SystemExit(f"entities must be a list: {path}")

        for row in rows:
            total += 1
            entity_id = row.get("id")
            if not entity_id or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", entity_id):
                raise SystemExit(f"Invalid id in {path}: {entity_id!r}")
            scoped = f"{sector['id']}:{entity_id}"
            if scoped in seen_ids:
                raise SystemExit(f"Duplicate entity id: {scoped}")
            seen_ids.add(scoped)

            if not row.get("name_ar") or not row.get("name_en"):
                raise SystemExit(f"Missing bilingual name: {scoped}")

            vs = row.get("verification_status")
            if vs not in ALLOWED_VERIFY:
                raise SystemExit(f"Invalid verification_status for {scoped}: {vs}")

            ds = row.get("domain_status")
            if ds not in ALLOWED_DOMAIN:
                raise SystemExit(f"Invalid domain_status for {scoped}: {ds}")

            if ds == "PROPOSED" and row.get("current_domain"):
                raise SystemExit(
                    f"PROPOSED entity must not use current_domain: {scoped}"
                )

    print("National Directory validation passed.")
    print("Sectors:", len(manifest["sectors"]))
    print("Entities:", total)

if __name__ == "__main__":
    main()
