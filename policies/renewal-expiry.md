# Renewal & Expiry Policy — Draft

Status: `DRAFT`

## Lifecycle

```text
ACTIVE
  |
  v
EXPIRED_GRACE
  |
  +--> ACTIVE      (renewal)
  |
  v
REDEMPTION
  |
  +--> ACTIVE      (restore)
  |
  v
PENDING_DELETE
  |
  v
DELETED
```

## Policy variables not yet fixed

- registration term
- renewal term
- grace duration
- redemption duration
- pending-delete duration
- restore fees, if any
- notice schedule

These values must not be invented by the software before formal policy adoption.
