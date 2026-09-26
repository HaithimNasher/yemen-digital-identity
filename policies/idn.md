# Arabic IDN Policy — Research Draft

Status: `RESEARCH_DRAFT`

YDII keeps `.اليمن` as a research track only until official and technical status is independently confirmed.

## Research areas

- Unicode normalization
- Arabic character repertoire
- variant handling
- homoglyph / spoofing risks
- right-to-left rendering
- Punycode representation
- reserved variants
- label validation
- registration bundling, if ever adopted
- DNSSEC compatibility
- browser behavior

## Safety principle

An Arabic label must not be displayed as operational solely because it can be encoded as IDNA/Punycode.

Operational status requires independent authoritative confirmation.
