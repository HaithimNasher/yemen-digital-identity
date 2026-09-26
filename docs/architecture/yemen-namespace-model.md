# Yemen Namespace Model — YDII Professional v2

## Design rule

YDII must never present a proposed namespace as if it were already approved or operational.

Every namespace belongs to one of five states:

- `CURRENT`
- `RESTRICTED`
- `PROPOSED`
- `RESEARCH`
- `RESERVED`

## Current / restricted model

```text
.ye
├── gov.ye   [RESTRICTED]
├── edu.ye   [RESTRICTED]
├── com.ye   [CURRENT]
├── org.ye   [CURRENT]
└── net.ye   [CURRENT]
```

Direct registrations under `.ye` are represented separately as part of the national namespace.

## Policy proposals

```text
sch.ye
med.ye
name.ye
pro.ye
museum.ye
```

These are research proposals derived from GCC benchmarking. They are not represented as existing registration zones.

## Arabic IDN track

`.اليمن` is maintained as a `RESEARCH` track until its operational/official status is independently confirmed.

## Reserved names

YDII proposes policy classes for:
- state institutions
- registry infrastructure
- security-sensitive digital-government labels

This is a policy model, not a registration action.
