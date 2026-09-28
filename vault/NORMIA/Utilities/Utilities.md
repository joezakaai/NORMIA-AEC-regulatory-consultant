---
title: Utilities
type: discipline
tags:
  - normia
  - discipline
---

# Utilities

> [!info] Part of [[NORMIA]] · [[Authority Directory]] · Template: [[Regulation Record]]

Connection requirements and NOCs — electricity, water, drainage, telecom, district cooling, gas.

## Records

Empty by design — add notes only from source documents in hand. One note per
clause.

```dataview
TABLE authority, document_title, edition, clause, status, confidence
FROM "NORMIA/Utilities"
WHERE document_title
SORT jurisdiction ASC
```

## Source documents

Drop regulation PDFs in this folder, then ask NORMIA to extract clause records.

---

**Related:** [[NORMIA]] · [[Authority Directory]] · [[Regulation Record]] · [[Project Intake]]
