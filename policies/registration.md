# Registration Policy — Draft

Status: `DRAFT`

This document is a design policy for YDII Professional v2. It is not an official `.ye` registration policy.

## Registration pipeline

1. normalize requested domain name
2. determine namespace / zone
3. check namespace status
4. check reserved-name rules
5. evaluate eligibility
6. collect required evidence
7. check domain availability
8. apply registrar authentication and authorization
9. create registry transaction
10. publish audit event
11. update DNS/zone data only after successful registry commit

## Core principles

- no registration without explicit namespace policy
- proposed zones cannot be treated as operational zones
- every create/update/delete operation must be attributable to an actor
- registry state is authoritative; screenshots and directory data are not
- sensitive namespaces require stronger review
- registry and registrar roles remain separated

## Minimum request fields

- domain name
- zone
- registrar ID
- registrant handle
- nameservers
- contact references
- eligibility evidence references
- request timestamp
- correlation / audit ID

## Rejection reasons

Examples:
- reserved name
- invalid syntax
- unsupported zone
- proposed/research-only zone
- failed eligibility
- missing evidence
- registrar not authorized
- conflicting registry state
