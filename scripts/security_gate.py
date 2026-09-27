#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

TEXT_SUFFIXES={
    ".py",".js",".css",".html",".json",".md",".yml",".yaml",
    ".txt",".toml",".ini",".cfg",".sh"
}

SKIP_PREFIXES=(
    ".git/",
    "backups/",
)

# Build sensitive markers from fragments so this scanner does not
# falsely detect its own source code as containing private-key material.
PRIVATE_KEY_MARKERS=(
    "-----BEGIN " + "RSA PRIVATE KEY-----",
    "-----BEGIN " + "EC PRIVATE KEY-----",
    "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
    "-----BEGIN " + "PRIVATE KEY-----",
)

SECRET_PATTERNS=[
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
]

OFFICIAL_CLAIM_PATTERNS=[
    re.compile(r"\bYDII\s+is\s+the\s+official\s+\.ye\s+registry\b",re.I),
    re.compile(r"\bwe\s+operate\s+the\s+\.ye\s+registry\b",re.I),
]

def tracked_files():
    p=subprocess.run(
        ["git","ls-files","-z"],
        cwd=ROOT,
        capture_output=True,
        check=True
    )
    return [
        x.decode("utf-8",errors="replace")
        for x in p.stdout.split(b"\0") if x
    ]

def is_text_candidate(rel: str):
    if rel.startswith(SKIP_PREFIXES):
        return False
    p=ROOT/rel
    return p.is_file() and (
        p.suffix.lower() in TEXT_SUFFIXES or p.name in {"LICENSE","SECURITY"}
    )

def check_json():
    failures=[]
    count=0
    for rel in tracked_files():
        if not rel.endswith(".json"):
            continue
        p=ROOT/rel
        try:
            json.loads(p.read_text(encoding="utf-8"))
            count+=1
        except Exception as exc:
            failures.append(f"{rel}: invalid JSON: {exc}")
    return count,failures

def check_secrets():
    failures=[]
    checked=0
    for rel in tracked_files():
        if not is_text_candidate(rel):
            continue
        p=ROOT/rel
        try:
            text=p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        checked+=1

        for marker in PRIVATE_KEY_MARKERS:
            if marker in text:
                failures.append(f"{rel}: private key material marker detected")

        for name,rx in SECRET_PATTERNS:
            if rx.search(text):
                failures.append(f"{rel}: possible {name} detected")
    return checked,failures

def check_integrity():
    failures=[]

    ns_path=ROOT/"data/yemen/namespace-model.json"
    if ns_path.exists():
        ns=json.loads(ns_path.read_text(encoding="utf-8"))
        rows={x.get("zone"):x.get("status") for x in ns.get("zones",[])}

        expected={
            ".ye":"CURRENT",
            "gov.ye":"RESTRICTED",
            "edu.ye":"RESTRICTED",
            "com.ye":"CURRENT",
            "org.ye":"CURRENT",
            "net.ye":"CURRENT",
            "sch.ye":"PROPOSED",
            "med.ye":"PROPOSED",
            "name.ye":"PROPOSED",
            "pro.ye":"PROPOSED",
            "museum.ye":"PROPOSED",
            ".اليمن":"RESEARCH",
        }
        for zone,status in expected.items():
            if rows.get(zone)!=status:
                failures.append(
                    f"namespace integrity: {zone} expected {status}, got {rows.get(zone)}"
                )

    search_path=ROOT/"data/search/config.json"
    if search_path.exists():
        cfg=json.loads(search_path.read_text(encoding="utf-8"))
        states=set(cfg.get("result_states",[]))
        if "AVAILABLE" in states:
            failures.append(
                "domain search integrity: AVAILABLE must not be inferred from RDAP absence"
            )
        if "NOT_FOUND_IN_RDAP" not in states:
            failures.append(
                "domain search integrity: NOT_FOUND_IN_RDAP state missing"
            )

    return failures

def check_disclaimer():
    failures=[]
    must_contain=[
        ROOT/"site/index.html",
        ROOT/"docs/observatory/README.md",
    ]
    for p in must_contain:
        if not p.exists():
            failures.append(f"{p.relative_to(ROOT)}: required file missing")
            continue
        t=p.read_text(encoding="utf-8").lower()
        if ".ye" not in t:
            failures.append(f"{p.relative_to(ROOT)}: .ye disclaimer/context missing")

    for rel in tracked_files():
        if not is_text_candidate(rel):
            continue
        try:
            text=(ROOT/rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for rx in OFFICIAL_CLAIM_PATTERNS:
            if rx.search(text):
                failures.append(f"{rel}: prohibited official-registry claim detected")
    return failures

def check_local_links():
    failures=[]
    pages=list((ROOT/"site").glob("*.html"))
    href_re=re.compile(r'href=["\']([^"\'#?]+)["\']',re.I)
    for page in pages:
        text=page.read_text(encoding="utf-8")
        for href in href_re.findall(text):
            if "://" in href or href.startswith(("mailto:","tel:","javascript:","data:")):
                continue
            target=(page.parent/href).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{page.name}: link escapes repository: {href}")
                continue
            if not target.exists():
                failures.append(f"{page.name}: broken local link: {href}")
    return len(pages),failures

def main():
    failures=[]

    json_count,json_failures=check_json()
    failures.extend(json_failures)

    text_count,secret_failures=check_secrets()
    failures.extend(secret_failures)

    failures.extend(check_integrity())
    failures.extend(check_disclaimer())

    page_count,link_failures=check_local_links()
    failures.extend(link_failures)

    print("Security Gate")
    print("-------------")
    print("JSON files validated:",json_count)
    print("Text files scanned:",text_count)
    print("HTML pages link-checked:",page_count)

    if failures:
        print("\nFAILURES:")
        for x in failures:
            print(" -",x)
        return 1

    print("\nPASS: security and integrity gate passed.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
