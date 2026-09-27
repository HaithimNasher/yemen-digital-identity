# Registry / Registrar Architecture

## Scope

YDII Professional v2 uses a **Registry–Registrar architecture model** as a design target.

This is an architectural prototype, not a claim that YDII is the official `.ye` registry.

## Logical architecture

```text
Registrant
    |
    v
Accredited Registrar
    |
    | authenticated provisioning API
    v
Registry Core
    |
    +--> Registry Database
    +--> Lifecycle Engine
    +--> Eligibility Engine
    +--> Reserved Names Engine
    +--> Audit Log
    +--> RDAP
    +--> DNS / Zone Publication
    +--> DNSSEC
```

## Separation of concerns

### Registry
Authoritative registry state, policy enforcement, lifecycle, zone publication, RDAP, DNSSEC, audit.

### Registrar
Customer onboarding, evidence collection, registration requests, renewal, transfer, contacts and support.

### Registrant
Accurate data, eligibility, nameserver management, policy compliance and renewal.

## Next implementation layers

1. Eligibility Engine
2. Policy Center
3. RDAP/DNS/DNSSEC Observatory
4. Domain Search
5. API contracts
6. Security and CI gates
