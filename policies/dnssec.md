# DNSSEC Policy — Draft

Status: `DRAFT`

## Registry responsibilities

The future registry architecture should support:
- secure zone signing
- key lifecycle management
- controlled KSK/ZSK operations
- DS submission from registrars
- validation of DS syntax
- rollover procedures
- incident recovery
- audit logging
- monitoring of signature validity

## Registrar responsibilities

Registrars should:
- accept validated DS material from registrants
- authenticate update requests
- transmit DS changes securely
- preserve transaction logs

## Security principle

Private signing keys must never be stored in source repositories or public CI logs.

A production deployment should use hardened key-management controls such as HSM-backed or equivalent protected signing infrastructure.
