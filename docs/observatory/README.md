# YDII Live Observatory

The Observatory separates **live technical observations** from:
- static directory data,
- policy data,
- screenshots,
- proposed namespaces.

## Signals

The probe can collect:

- IPv4 (`A`)
- IPv6 (`AAAA`)
- NS
- MX
- CAA
- DS
- RRSIG evidence
- HTTPS response
- TLS certificate validity
- TLS protocol/cipher
- RDAP result

## DNSSEC limitation

The current implementation records DS/RRSIG **evidence** only.

It does **not** claim full cryptographic DNSSEC chain validation.

A later production implementation may use a validating resolver or dedicated DNSSEC validator.

## RDAP limitation

`NOT_FOUND_IN_RDAP` does **not** mean the domain is available to register.

Availability is a separate Registry/Registrar function.

## Optional `dig`

A/AAAA resolution, HTTPS, TLS and RDAP use Python standard-library functions.

NS/MX/CAA/DS/RRSIG checks use `dig` when installed. If `dig` is unavailable, the observer records that condition rather than inventing results.

## Examples

Probe one domain:

```bash
python scripts/observatory_probe.py --domain gov.ye
```

Probe first five project targets:

```bash
python scripts/observatory_probe.py --limit 5
```

Probe all current targets:

```bash
python scripts/observatory_probe.py
```
