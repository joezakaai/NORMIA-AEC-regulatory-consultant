---
title: Environment
type: discipline
tags:
  - normia
  - discipline
---

# Environment

> [!info] Part of [[NORMIA]] · [[Authority Directory]] · Template: [[Regulation Record]]

EIA, environmental permitting, protected areas, coastal and heritage constraints.

## Records

Empty by design — add notes only from source documents in hand. One note per
clause.

```dataview
TABLE authority, document_title, edition, clause, status, confidence
FROM "NORMIA/Environment"
WHERE document_title
SORT jurisdiction ASC
```

## Source documents

Drop regulation PDFs in this folder, then ask NORMIA to extract clause records.

---

**Related:** [[NORMIA]] · [[Authority Directory]] · [[Regulation Record]] · [[Project Intake]]
