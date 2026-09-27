# Domain Transfer Policy — Draft

Status: `DRAFT`

## Supported transfer concept

A transfer changes the sponsoring registrar while preserving the domain registration.

## Controls

- authenticated request
- registrant authorization
- domain state check
- no transfer while prohibited by active registry lock/policy state
- explicit audit event
- old and new registrar identifiers
- transaction correlation ID
- rollback handling for failed transfers

The precise waiting periods and authorization method are intentionally left for future policy adoption.
