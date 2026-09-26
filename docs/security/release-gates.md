# YDII v2 Security and Release Gates

Step 13 adds local and CI-enforced checks for YDII Professional v2.

## Security gate

`scripts/security_gate.py` checks:

- JSON parse validity
- private-key material markers
- conservative token/secret patterns
- Yemen namespace status integrity
- the `NOT_FOUND_IN_RDAP != AVAILABLE` invariant
- anti-impersonation positioning
- local HTML link integrity

## Release readiness

`scripts/release_readiness.py` verifies:

- required v2 architecture artifacts exist
- GCC parity audit has no remaining `PARTIAL` or `PLANNED` requirement
- the security gate passes
- the dedicated GitHub Actions workflow exists

## CI

`.github/workflows/ydii-v2-security-ci.yml` runs on:

- pushes to `main`
- pushes to `feat/ydii-professional-v2`
- pull requests targeting `main`
- manual dispatch

## Operational limitation

Passing these gates means the repository satisfies the project's defined integrity checks.

It does not make YDII an official `.ye` registry and does not replace external security review, legal adoption, authoritative registry operations, or formal accreditation.
