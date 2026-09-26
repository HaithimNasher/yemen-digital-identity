#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import socket
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
TARGETS_PATH=ROOT/"data/observatory/targets.json"
SOURCES_PATH=ROOT/"data/observatory/sources.json"

DEFAULT_TIMEOUT=4.0

def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def uniq(items):
    out=[]
    seen=set()
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def resolve_addresses(domain: str):
    a=[]
    aaaa=[]
    error=None
    try:
        infos=socket.getaddrinfo(domain, None, type=socket.SOCK_STREAM)
        for family, _, _, _, sockaddr in infos:
            if family == socket.AF_INET:
                a.append(sockaddr[0])
            elif family == socket.AF_INET6:
                aaaa.append(sockaddr[0])
    except Exception as exc:
        error=f"{type(exc).__name__}: {exc}"
    return {
        "a": uniq(a),
        "aaaa": uniq(aaaa),
        "resolver_error": error
    }

def run_dig(domain: str, rrtype: str, dnssec=False):
    if not shutil.which("dig"):
        return {
            "available": False,
            "records": [],
            "raw_status": "DIG_NOT_INSTALLED"
        }

    cmd=["dig","+time=3","+tries=1","+short"]
    if dnssec:
        cmd.append("+dnssec")
    cmd += [domain, rrtype]

    try:
        p=subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            timeout=6,
            check=False
        )
        rows=[x.strip() for x in p.stdout.splitlines() if x.strip()]
        return {
            "available": True,
            "records": rows,
            "returncode": p.returncode,
            "stderr": p.stderr.strip()[:300] or None
        }
    except Exception as exc:
        return {
            "available": True,
            "records": [],
            "raw_status": f"{type(exc).__name__}: {exc}"
        }

def dns_details(domain: str):
    result=resolve_addresses(domain)

    for rrtype, key in [
        ("NS","ns"),
        ("MX","mx"),
        ("CAA","caa"),
        ("DS","ds")
    ]:
        q=run_dig(domain,rrtype)
        result[key]=q["records"]
        result[f"{key}_query_status"] = (
            "OK" if q.get("available") else "DIG_NOT_INSTALLED"
        )

    # Evidence only. This is NOT cryptographic validation.
    rrsig=run_dig(domain,"RRSIG",dnssec=True)
    result["rrsig"]=rrsig["records"]
    result["dnssec_evidence"] = (
        "DS_PRESENT" if result["ds"] else
        "RRSIG_PRESENT" if result["rrsig"] else
        "NO_SIGNING_EVIDENCE_OBSERVED"
    )
    result["dnssec_validated"]=False
    result["dnssec_note"]="DS/RRSIG evidence only; full chain validation is not claimed."

    return result

def tls_probe(domain: str, timeout=DEFAULT_TIMEOUT):
    out={
        "reachable": False,
        "certificate_valid": False,
        "protocol": None,
        "cipher": None,
        "not_after": None,
        "days_remaining": None,
        "error": None
    }
    try:
        ctx=ssl.create_default_context()
        started=time.monotonic()
        with socket.create_connection((domain,443),timeout=timeout) as raw:
            with ctx.wrap_socket(raw,server_hostname=domain) as s:
                cert=s.getpeercert()
                out["reachable"]=True
                out["certificate_valid"]=True
                out["protocol"]=s.version()
                cipher=s.cipher()
                out["cipher"]=cipher[0] if cipher else None
                out["latency_ms"]=round((time.monotonic()-started)*1000,1)

                not_after=cert.get("notAfter")
                if not_after:
                    out["not_after"]=not_after
                    exp=dt.datetime.strptime(
                        not_after,"%b %d %H:%M:%S %Y %Z"
                    ).replace(tzinfo=dt.timezone.utc)
                    out["days_remaining"]=(exp-dt.datetime.now(dt.timezone.utc)).days
    except Exception as exc:
        out["error"]=f"{type(exc).__name__}: {exc}"
    return out

def http_probe(domain: str, timeout=DEFAULT_TIMEOUT):
    url=f"https://{domain}/"
    req=urllib.request.Request(
        url,
        headers={"User-Agent":"YDII-Observatory/2.0"},
        method="GET"
    )
    started=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            return {
                "url": url,
                "status": r.status,
                "final_url": r.geturl(),
                "latency_ms": round((time.monotonic()-started)*1000,1),
                "error": None
            }
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "final_url": exc.geturl(),
            "latency_ms": round((time.monotonic()-started)*1000,1),
            "error": None
        }
    except Exception as exc:
        return {
            "url": url,
            "status": None,
            "final_url": None,
            "latency_ms": round((time.monotonic()-started)*1000,1),
            "error": f"{type(exc).__name__}: {exc}"
        }

def rdap_base_for_tld(tld: str, timeout=DEFAULT_TIMEOUT):
    # First prefer the IANA-published .ye endpoint already recorded in sources.
    sources=load_json(SOURCES_PATH)
    if tld == "ye":
        base=sources.get("ye_registry_metadata",{}).get("rdap_base_url")
        if base:
            return base.rstrip("/")+"/", "IANA_YE_METADATA"

    # Generic fallback: IANA RDAP bootstrap registry.
    url="https://data.iana.org/rdap/dns.json"
    try:
        req=urllib.request.Request(
            url,
            headers={"User-Agent":"YDII-Observatory/2.0"}
        )
        with urllib.request.urlopen(req,timeout=timeout) as r:
            data=json.load(r)
        for service in data.get("services",[]):
            tlds,urls=service
            if tld.lower() in [x.lower() for x in tlds] and urls:
                return urls[0].rstrip("/")+"/", "IANA_RDAP_BOOTSTRAP"
    except Exception:
        pass
    return None, "NO_RDAP_BOOTSTRAP"

def rdap_probe(domain: str, timeout=DEFAULT_TIMEOUT):
    tld=domain.rstrip(".").split(".")[-1].lower()
    base, discovery=rdap_base_for_tld(tld,timeout)
    if not base:
        return {
            "status":"NO_RDAP_SERVICE_DISCOVERED",
            "http_status":None,
            "endpoint":None,
            "discovery":discovery,
            "error":None
        }

    endpoint=base+"domain/"+domain
    req=urllib.request.Request(
        endpoint,
        headers={
            "Accept":"application/rdap+json, application/json",
            "User-Agent":"YDII-Observatory/2.0"
        }
    )
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            payload=json.load(r)
            return {
                "status":"FOUND",
                "http_status":r.status,
                "endpoint":endpoint,
                "discovery":discovery,
                "ldhName":payload.get("ldhName"),
                "unicodeName":payload.get("unicodeName"),
                "objectClassName":payload.get("objectClassName"),
                "error":None
            }
    except urllib.error.HTTPError as exc:
        # Important: RDAP 404 is NOT called AVAILABLE.
        return {
            "status":"NOT_FOUND_IN_RDAP" if exc.code == 404 else "HTTP_ERROR",
            "http_status":exc.code,
            "endpoint":endpoint,
            "discovery":discovery,
            "error":None
        }
    except Exception as exc:
        return {
            "status":"QUERY_ERROR",
            "http_status":None,
            "endpoint":endpoint,
            "discovery":discovery,
            "error":f"{type(exc).__name__}: {exc}"
        }

def probe(target: dict[str,Any], timeout=DEFAULT_TIMEOUT):
    domain=target["domain"]
    started=time.monotonic()
    result={
        "domain":domain,
        "kind":target.get("kind"),
        "label_ar":target.get("label_ar"),
        "source":target.get("source"),
        "checked_at":utc_now(),
        "dns":dns_details(domain),
        "tls":tls_probe(domain,timeout),
        "http":http_probe(domain,timeout),
        "rdap":rdap_probe(domain,timeout),
    }
    result["probe_duration_ms"]=round((time.monotonic()-started)*1000,1)
    return result

def build_summary(results):
    total=len(results)
    return {
        "targets_checked": total,
        "dns_ipv4_present": sum(bool(x["dns"]["a"]) for x in results),
        "dns_ipv6_present": sum(bool(x["dns"]["aaaa"]) for x in results),
        "tls_valid": sum(bool(x["tls"]["certificate_valid"]) for x in results),
        "https_responded": sum(x["http"]["status"] is not None for x in results),
        "rdap_found": sum(x["rdap"]["status"]=="FOUND" for x in results),
        "dnssec_ds_or_rrsig_evidence": sum(
            x["dns"]["dnssec_evidence"] in {"DS_PRESENT","RRSIG_PRESENT"}
            for x in results
        )
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--domain",help="Probe one explicit domain")
    parser.add_argument("--limit",type=int,default=0,help="Limit project targets")
    parser.add_argument("--timeout",type=float,default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--output",
        default=str(ROOT/"site/data/observatory-live.json")
    )
    args=parser.parse_args()

    if args.domain:
        targets=[{
            "domain":args.domain.lower().strip().rstrip("."),
            "kind":"manual",
            "label_ar":"فحص يدوي",
            "source":"CLI"
        }]
    else:
        payload=load_json(TARGETS_PATH)
        targets=payload["targets"]
        if args.limit > 0:
            targets=targets[:args.limit]

    results=[]
    for i,target in enumerate(targets,1):
        print(f"[{i}/{len(targets)}] {target['domain']}",flush=True)
        results.append(probe(target,args.timeout))

    out={
        "generated_at":utc_now(),
        "mode":"LIVE_OBSERVATION",
        "notice_ar":"هذه نتائج رصد شبكي لحظية وليست إثبات ملكية أو توافر للتسجيل. NOT_FOUND_IN_RDAP لا يعني AVAILABLE. DNSSEC هنا دليل DS/RRSIG فقط ولا يمثل تحققاً تشفيرياً كاملاً.",
        "tooling":{
            "dig_available": bool(shutil.which("dig")),
            "rdap_discovery":"IANA metadata/bootstrap"
        },
        "summary":build_summary(results),
        "results":results
    }

    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(
        json.dumps(out,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8"
    )

    print("Wrote:",output)
    print(json.dumps(out["summary"],ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
