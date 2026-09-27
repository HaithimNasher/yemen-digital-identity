# Domain Lifecycle Policy — Draft

Status: `DRAFT`

The lifecycle engine must support clearly defined states and transitions.

```text
AVAILABLE
   |
   v
PENDING_CREATE
   |
   v
ACTIVE
   |
   +----> SUSPENDED ----> ACTIVE
   |
   v
EXPIRED_GRACE
   |
   +----> ACTIVE (renew)
   |
   v
REDEMPTION
   |
   +----> ACTIVE (restore)
   |
   v
PENDING_DELETE
   |
   v
DELETED
   |
   v
AVAILABLE
```

The actual grace, redemption, and pending-delete durations are intentionally unset until adopted by policy.

All state transitions must produce an audit event.
