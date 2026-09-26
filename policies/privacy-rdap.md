# Privacy & RDAP Policy — Draft

Status: `DRAFT`

## Objective

Provide public registration-data access while minimizing unnecessary disclosure of personal data.

## RDAP-first design

YDII uses RDAP as the preferred modern registration-data interface in the architecture.

Public output should distinguish:
- domain status
- registrar
- nameservers
- DNSSEC status
- important lifecycle events
- public entity contacts where appropriate

Personal contact data should be minimized or redacted according to adopted privacy rules.

## Access tiers

### Public
Minimal public registration data.

### Authenticated operational access
Additional data for authorized registry / registrar functions.

### Compliance / incident access
Controlled access for authorized investigations subject to audit.

## Required controls

- access logging
- rate limiting
- data minimization
- purpose limitation
- audit trail
- retention schedule
- abuse prevention
- documented disclosure rules
