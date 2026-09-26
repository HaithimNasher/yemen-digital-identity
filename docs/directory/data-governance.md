# National Directory Data Governance

## Purpose

YDII separates three concepts:

1. **Entity directory**
2. **Namespace policy**
3. **Live Internet observations**

They must never be merged into one unqualified status.

## Entity verification states

- `verified-source`
- `user-provided`
- `screenshot-reference`
- `pending-verification`

## Domain states

- `CURRENT`
- `VERIFIED`
- `PROPOSED`
- `UNKNOWN`

`PROPOSED` must never be displayed as registered or official.

## Provenance

Future curated records should include:

- source URL
- source note
- verification date
- entity category
- current or proposed domain status

## High-sensitivity sectors

Government, finance, telecom and healthcare records require stronger verification before being marked `verified-source`.

## No synthetic records

Empty datasets are intentional. A category being present in the architecture does not justify inventing organizations to populate it.
