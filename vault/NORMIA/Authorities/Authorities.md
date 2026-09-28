---
title: Authorities
type: index
tags:
  - normia
  - index
---

# Authorities

> [!info] Part of [[NORMIA]] · [[Authority Directory]] · Template: [[Regulation Record]]

Home of [[Authority Directory]] — the routing index of who regulates what, and where.

## Records

Empty by design — add notes only from source documents in hand. One note per
clause.

```dataview
TABLE authority, document_title, edition, clause, status, confidence
FROM "NORMIA/Authorities"
WHERE document_title
SORT jurisdiction ASC
```

## Source documents

Drop regulation PDFs in this folder, then ask NORMIA to extract clause records.

---

**Related:** [[NORMIA]] · [[Authority Directory]] · [[Regulation Record]] · [[Project Intake]]
