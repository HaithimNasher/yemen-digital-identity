#!/usr/bin/env python3
from __future__ import annotations

import json
import datetime as dt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REQ=ROOT/"data/audit/gcc-parity-requirements.json"
GCC=ROOT/"data/gcc/benchmark.json"
OUT=ROOT/"site/data/gcc-parity-audit.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

def evaluate(req):
    evidence=[]
    missing=[]
    for item in req.get("evidence",[]):
        p=ROOT/item
        if p.exists():
            evidence.append(item)
        else:
            missing.append(item)

    forced=req.get("force_state")
    if forced:
        state=forced
    elif evidence and not missing:
        state="COVERED"
    elif evidence:
        state="PARTIAL"
    else:
        state="PLANNED"

    return {
        "id":req["id"],
        "name_ar":req["name_ar"],
        "name_en":req["name_en"],
        "category":req["category"],
        "state":state,
        "evidence_found":evidence,
        "evidence_missing":missing,
        "note_ar":req.get("note_ar")
    }

def main():
    reqs=load(REQ)
    gcc=load(GCC)

    rows=[evaluate(x) for x in reqs["requirements"]]
    counts={s:sum(x["state"]==s for x in rows)
            for s in reqs["states"]}

    categories={}
    for row in rows:
        categories.setdefault(row["category"],{
            "requirements":0,
            "covered":0,
            "partial":0,
            "planned":0
        })
        c=categories[row["category"]]
        c["requirements"]+=1
        if row["state"]=="COVERED":
            c["covered"]+=1
        elif row["state"]=="PARTIAL":
            c["partial"]+=1
        elif row["state"]=="PLANNED":
            c["planned"]+=1

    out={
        "project":"YDII Professional v2",
        "generated_at":utc_now(),
        "status":"TECHNICAL_COVERAGE_AUDIT",
        "methodology":reqs["methodology"],
        "gcc_reference_countries":[
            {"code":x["code"],"cctld":x["cctld"]}
            for x in gcc.get("countries",[])
        ],
        "summary":{
            "requirements":len(rows),
            "covered":counts.get("COVERED",0),
            "partial":counts.get("PARTIAL",0),
            "planned":counts.get("PLANNED",0),
            "not_applicable":counts.get("NOT_APPLICABLE",0)
        },
        "categories":categories,
        "requirements":rows,
        "interpretation_ar":"هذه مصفوفة تغطية فنية لمكونات المشروع، وليست ترتيبًا أو تقييمًا للدول الخليجية، ولا تثبت الجاهزية التشغيلية لسجل وطني.",
        "next_priority":[
            x["id"] for x in rows
            if x["state"] in {"PARTIAL","PLANNED"}
        ]
    }

    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(
        json.dumps(out,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8"
    )

    print("GCC parity audit built.")
    print("Requirements:",out["summary"]["requirements"])
    print("Covered:",out["summary"]["covered"])
    print("Partial:",out["summary"]["partial"])
    print("Planned:",out["summary"]["planned"])
    if out["next_priority"]:
        print("Next priority:",", ".join(out["next_priority"]))

if __name__=="__main__":
    main()
