# WHOIS / RDAP Transition Policy — Draft

Status: `DRAFT`

YDII treats WHOIS as a compatibility / legacy interface where required and RDAP as the preferred structured protocol.

## Design goals

- avoid creating new dependencies on unstructured WHOIS output
- expose machine-readable registration data through RDAP
- use a documented privacy model
- keep public and privileged views separate
- ensure query logging and rate limiting

No operational WHOIS service is implied by this document.
