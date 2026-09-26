from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def validate():
    required = [
        ROOT / "data" / "gcc_domains.json",
        ROOT / "data" / "sources.json",
        ROOT / "site" / "index.html",
    ]
    for p in required:
        if not p.exists():
            raise SystemExit(f"Missing required file: {p}")

    gcc = json.loads((ROOT / "data" / "gcc_domains.json").read_text(encoding="utf-8"))
    countries = gcc.get("countries", [])
    if len(countries) < 7:
        raise SystemExit("Expected GCC countries plus Yemen")

    cc = {c.get("ccTLD") for c in countries}
    expected = {".sa", ".ae", ".qa", ".kw", ".om", ".bh", ".ye"}
    missing = expected - cc
    if missing:
        raise SystemExit(f"Missing ccTLDs: {sorted(missing)}")

    sources = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    if not sources.get("sources"):
        raise SystemExit("No sources found")

    print("Validation passed.")

if __name__ == "__main__":
    validate()
