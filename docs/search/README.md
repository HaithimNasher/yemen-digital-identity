# YDII Domain Search Engine

The search engine evaluates one label across the Yemen namespace model.

## Result states

- `REGISTERED`
- `NOT_FOUND_IN_RDAP`
- `RESERVED`
- `RESTRICTED`
- `PROPOSED_ZONE`
- `QUERY_ERROR`
- `UNKNOWN`

## Critical rule

`NOT_FOUND_IN_RDAP` is **not** converted to `AVAILABLE`.

A production availability decision requires an operational Registry/Registrar service with authoritative availability semantics.

## Examples

Offline policy-only check:

```bash
python scripts/domain_search.py yemenai --offline
```

Live RDAP-backed observation:

```bash
python scripts/domain_search.py yemenai
```

Reserved-name test:

```bash
python scripts/domain_search.py login --offline
```
