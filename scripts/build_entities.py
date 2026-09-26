from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "entities"
OUT = ROOT / "site" / "data" / "entities.json"

ORDER = [
    "ministries",
    "companies",
    "organizations",
    "universities",
    "schools",
]

categories = []

for name in ORDER:
    p = SRC / f"{name}.json"
    if not p.exists():
        continue

    data = json.loads(p.read_text(encoding="utf-8"))

    entities = data.get("entities", [])
    if not isinstance(entities, list):
        raise SystemExit(f"Invalid entities list in {p}")

    categories.append(data)

OUT.parent.mkdir(parents=True, exist_ok=True)

payload = {
    "project": "YDII",
    "version": "1.0",
    "categories": categories,
}

OUT.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(f"Built: {OUT}")
print(f"Categories: {len(categories)}")
for c in categories:
    print(f"- {c.get('category')}: {len(c.get('entities', []))} entities")
