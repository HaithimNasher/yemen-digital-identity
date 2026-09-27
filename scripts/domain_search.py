#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
CONFIG_PATH=ROOT/"data/search/config.json"
NAMESPACE_PATH=ROOT/"data/yemen/namespace-model.json"
OBS_PATH=ROOT/"scripts/observatory_probe.py"

LABEL_RE=re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_observatory():
    spec=importlib.util.spec_from_file_location("ydii_observatory",OBS_PATH)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def normalize_label(value: str) -> str:
    label=value.strip().lower()
    if "." in label:
        # Search accepts a label, not a complete domain.
        label=label.split(".",1)[0]
    if not LABEL_RE.fullmatch(label):
        raise ValueError(
            "Invalid label. Use 1-63 ASCII letters, digits or hyphens; "
            "label cannot start/end with a hyphen."
        )
    return label

def fqdn(label: str, zone: str) -> str:
    if zone == ".ye":
        return f"{label}.ye"
    return f"{label}.{zone}"

def reserved_labels():
    d=load_json(NAMESPACE_PATH)
    result={}
    for group in d.get("reserved_name_classes",[]):
        for name in group.get("examples",[]):
            result[name.lower()]=group["class"]
    return result

def evaluate_candidate(label: str, zone_cfg: dict[str,Any], live=True, timeout=4.0):
    domain=fqdn(label,zone_cfg["zone"])
    base={
        "label":label,
        "zone":zone_cfg["zone"],
        "domain":domain,
        "namespace_status":zone_cfg["namespace_status"],
        "mode":zone_cfg["mode"],
        "search_state":"UNKNOWN",
        "registration_availability":"NOT_DETERMINED",
        "reason_ar":"",
        "rdap":None
    }

    reserved=reserved_labels()
    if label in reserved:
        base["search_state"]="RESERVED"
        base["reason_ar"]=f"الاسم ضمن فئة محجوزة في نموذج YDII: {reserved[label]}"
        return base

    if zone_cfg["namespace_status"] == "PROPOSED":
        base["search_state"]="PROPOSED_ZONE"
        base["reason_ar"]="المنطقة مقترحة بحثيًا وليست منطقة تسجيل تشغيلية."
        return base

    if zone_cfg["namespace_status"] == "RESTRICTED":
        base["search_state"]="RESTRICTED"
        base["reason_ar"]="هذه منطقة مقيدة وتتطلب تحقق الأهلية قبل أي عملية تسجيل."
        # We still may show RDAP observation if live is requested, but it does not
        # change the restricted nature of the zone.
        if not live:
            return base

    if not live:
        if base["search_state"] == "UNKNOWN":
            base["reason_ar"]="الفحص الحي معطل؛ لم يتم استنتاج حالة التسجيل."
        return base

    obs=load_observatory()
    rdap=obs.rdap_probe(domain,timeout)
    base["rdap"]=rdap

    if rdap["status"] == "FOUND":
        if base["search_state"] != "RESTRICTED":
            base["search_state"]="REGISTERED"
        base["registration_availability"]="NOT_AVAILABLE_AS_NEW_REGISTRATION"
        base["reason_ar"] = (
            base["reason_ar"] + " "
            if base["reason_ar"] else ""
        ) + "RDAP أعاد سجل نطاق."
        return base

    if rdap["status"] == "NOT_FOUND_IN_RDAP":
        if base["search_state"] != "RESTRICTED":
            base["search_state"]="NOT_FOUND_IN_RDAP"
        base["registration_availability"]="NOT_DETERMINED"
        base["reason_ar"] = (
            base["reason_ar"] + " "
            if base["reason_ar"] else ""
        ) + "لم يعثر RDAP على سجل؛ هذا لا يعني أن الاسم متاح للتسجيل."
        return base

    if rdap["status"] in {"QUERY_ERROR","HTTP_ERROR","NO_RDAP_SERVICE_DISCOVERED"}:
        if base["search_state"] != "RESTRICTED":
            base["search_state"]="QUERY_ERROR"
        base["reason_ar"] = (
            base["reason_ar"] + " "
            if base["reason_ar"] else ""
        ) + "تعذر الحصول على نتيجة RDAP حاسمة."
        return base

    return base

def search(label: str, live=True, timeout=4.0):
    label=normalize_label(label)
    cfg=load_json(CONFIG_PATH)
    rows=[evaluate_candidate(label,z,live=live,timeout=timeout)
          for z in cfg["candidate_zones"]]
    return {
        "query":label,
        "mode":"LIVE_RDAP" if live else "OFFLINE_POLICY_ONLY",
        "notice_ar":"NOT_FOUND_IN_RDAP لا يعني AVAILABLE. التوفر الحقيقي يحتاج خدمة Registry/Registrar تشغيلية.",
        "results":rows
    }

def main():
    parser=argparse.ArgumentParser(description="YDII domain search engine")
    parser.add_argument("label",help="Domain label, e.g. yemenai")
    parser.add_argument("--offline",action="store_true",help="Policy-only search")
    parser.add_argument("--timeout",type=float,default=4.0)
    parser.add_argument("--output")
    args=parser.parse_args()

    result=search(args.label,live=not args.offline,timeout=args.timeout)
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:
        p=Path(args.output)
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text+"\n",encoding="utf-8")
        print("Wrote:",p)
    else:
        print(text)

if __name__=="__main__":
    main()
