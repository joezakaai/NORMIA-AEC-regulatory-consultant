---
title: Projects
type: index
tags:
  - normia
  - index
---

# Projects

> [!info] Part of [[NORMIA]] · [[Authority Directory]] · Template: [[Regulation Record]]

One folder per project, built from [[Project Intake]].

## Records

Empty by design — add notes only from source documents in hand. One note per
clause.

```dataview
TABLE authority, document_title, edition, clause, status, confidence
FROM "NORMIA/Projects"
WHERE document_title
SORT jurisdiction ASC
```

## Source documents

Drop regulation PDFs in this folder, then ask NORMIA to extract clause records.

---

**Related:** [[NORMIA]] · [[Authority Directory]] · [[Regulation Record]] · [[Project Intake]]
