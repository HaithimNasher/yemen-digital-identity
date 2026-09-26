#!/usr/bin/env python3
from __future__ import annotations

import json
import datetime as dt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(path: str, default=None):
    p=ROOT/path
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))

def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

def main():
    ns=load("data/yemen/namespace-model.json",{})
    directory=load("data/directory/manifest.json",{})
    policies=load("data/policies/catalog.json",{})
    gcc=load("data/gcc/benchmark.json",{})
    registry=load("data/registry/registry-model.json",{})
    observatory=load("site/data/observatory-live.json",{})
    search=load("site/data/domain-search-sample.json",{})
    entities=load("site/data/entities.json",{})

    ns_rows=ns.get("zones",[])
    ns_counts={}
    for row in ns_rows:
        ns_counts[row.get("status","UNKNOWN")]=ns_counts.get(row.get("status","UNKNOWN"),0)+1

    sectors=directory.get("sectors",[])
    sector_counts={}
    total_entities=0

    category_map={
        x.get("category"):x.get("entities",[])
        for x in entities.get("categories",[])
    }

    for sector in sectors:
        sid=sector["id"]
        count=len(category_map.get(sid,[]))
        sector_counts[sid]=count
        total_entities += count

    milestones=[
        ("baseline","Baseline / Backup","v1.0-baseline"),
        ("gcc","GCC Benchmark","data/gcc/benchmark.json"),
        ("namespace","YE Namespace Model","data/yemen/namespace-model.json"),
        ("directory","National Directory","data/directory/manifest.json"),
        ("registry","Registry / Registrar","data/registry/registry-model.json"),
        ("eligibility","Eligibility Engine","data/eligibility/rules.json"),
        ("policies","Policy Center","data/policies/catalog.json"),
        ("observatory","Live Observatory","scripts/observatory_probe.py"),
        ("search","Domain Search","scripts/domain_search.py"),
        ("dashboard","National Dashboard","scripts/build_national_dashboard.py"),
    ]

    milestone_rows=[]
    for mid,name,ref in milestones:
        if ref=="v1.0-baseline":
            done=True
        else:
            done=(ROOT/ref).exists()
        milestone_rows.append({
            "id":mid,
            "name":name,
            "status":"COMPLETE" if done else "PENDING"
        })

    obs_summary=observatory.get("summary",{})
    dashboard={
        "project":"YDII Professional v2",
        "generated_at":utc_now(),
        "status":"DEVELOPMENT_DASHBOARD",
        "notice_ar":"لوحة تجميع فنية للمشروع. لا تمثل سجل .ye الرسمي ولا جهة حكومية، ونتائج الرصد الحي تعكس لحظة الفحص فقط.",
        "registry":{
            "architecture_status":registry.get("status","UNKNOWN"),
            "actors":len(registry.get("actors",[])),
            "security_controls":len(registry.get("security_controls",[]))
        },
        "namespace":{
            "zones_total":len(ns_rows),
            "by_status":ns_counts
        },
        "directory":{
            "sectors_total":len(sectors),
            "entities_total":total_entities,
            "by_sector":sector_counts
        },
        "policies":{
            "count":len(policies.get("policies",[])),
            "status":policies.get("status","UNKNOWN")
        },
        "gcc":{
            "countries":len(gcc.get("countries",[]))
        },
        "observatory":{
            "generated_at":observatory.get("generated_at"),
            "mode":observatory.get("mode","UNKNOWN"),
            "summary":obs_summary
        },
        "domain_search":{
            "sample_query":search.get("query"),
            "sample_mode":search.get("mode","UNKNOWN"),
            "sample_results":len(search.get("results",[]))
        },
        "milestones":milestone_rows,
        "warnings":[
            "Live observations are not proof of ownership or registration eligibility.",
            "NOT_FOUND_IN_RDAP does not mean AVAILABLE.",
            "DNSSEC evidence in Step 8 is not full cryptographic validation.",
            "Proposed namespace labels remain non-operational research proposals."
        ]
    }

    out=ROOT/"site/data/national-dashboard.json"
    out.write_text(
        json.dumps(dashboard,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8"
    )

    print("Built:",out)
    print("Directory entities:",dashboard["directory"]["entities_total"])
    print("Policy count:",dashboard["policies"]["count"])
    print("GCC countries:",dashboard["gcc"]["countries"])
    print("Namespace zones:",dashboard["namespace"]["zones_total"])
    print("Milestones complete:",
          sum(x["status"]=="COMPLETE" for x in milestone_rows),
          "/",
          len(milestone_rows))

if __name__=="__main__":
    main()
