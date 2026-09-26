# YDII Eligibility Engine

The engine evaluates a **draft policy model**.

It does not:
- query a live registry,
- confirm domain availability,
- verify government/legal status,
- approve registrations,
- prove domain ownership.

## CLI example

```bash
python scripts/eligibility_engine.py \
  --zone gov.ye \
  --type government \
  --evidence institution_authorization,authorized_contact
```

Example result:

```json
{
  "decision": "ELIGIBLE"
}
```

A missing evidence item results in `REVIEW_REQUIRED`.

A proposed zone such as `med.ye` always returns `PROPOSED_ZONE`.
