---
title: NORMIA
type: MOC
created: 2026-08-10
tags:
  - normia
  - moc
cssclasses:
  - normia
---

# NORMIA

**AEC Regulatory Intelligence & Compliance Consultant**
*Norms + Intelligence + Architecture*

> [!abstract] What this vault is
> The regulatory memory for the NORMIA agent. Everything here is evidence:
> verified requirements, traced to a clause, a page and an official source.
> The agent itself lives outside the vault at `.claude/agents/normia.md` —
> a readable copy is at [[NORMIA — Agent Definition]].

---

## Start here

- [[Authority Directory]] — **who** regulates **what**, and **where** their
  official portal is. Qatar · Saudi Arabia · UAE · Lebanon · Jordan. Routing
  index only, no numeric values.
- [[Regulation Record]] — the template. One note per clause.
- [[Project Intake]] — the template for a new project file.
- [[NORMIA — Agent Definition]] — the full agent brief, readable in Obsidian.

---

## Jurisdictions

| | |
|---|---|
| [[Qatar]] | [[Saudi Arabia]] |
| [[UAE]] | [[Lebanon]] |
| **[[Jordan]]** | [[Other]] |

---

## Disciplines

| | | |
|---|---|---|
| [[Planning]] | [[Building Codes]] | [[Fire & Life Safety]] |
| [[Accessibility]] | [[Structural]] | [[Mechanical]] |
| [[Electrical]] | [[Plumbing]] | [[Sustainability]] |
| [[Environment]] | [[Roads]] | [[Utilities]] |
| [[GIS]] | [[Developer Guidelines]] | |

---

## Projects

See [[Projects]] — one folder per project, built from [[Project Intake]].

```dataview
TABLE country, city_municipality, project_type, project_stage
FROM "NORMIA/Projects"
WHERE project_name
SORT date_opened DESC
```

*(The table above renders if the Dataview community plugin is installed. Without
it, browse the `Projects` folder directly.)*

---

## The lifecycle NORMIA covers

> Land / Plot → GIS → Topography → Regulations → Feasibility → Concept Design →
> Design Development → Authority Submission → Detailed Design → BIM →
> Shop Drawings → Construction → As-Built Compliance

---

## Working rules

> [!warning] The golden rule — never invent compliance
> - Sufficient evidence → **VERIFIED COMPLIANT**
> - Violation demonstrated → **NON-COMPLIANT — ACTION REQUIRED**
> - Information incomplete → **INSUFFICIENT INFORMATION**
> - Requirement unverifiable → **UNVERIFIED — AUTHORITY / OFFICIAL SOURCE
>   CONFIRMATION REQUIRED**
>
> A plausible number is more dangerous than no number, because the team will
> build to it.

1. **One note per clause.** Use [[Regulation Record]]. Never a summary blob
   covering several clauses.
2. **Never write a record without the source document in hand.** An empty vault
   is correct. A vault populated from recollection is actively dangerous.
3. **[[Authority Directory]] holds no requirements.** Routing index only.
4. **Record the edition and effective date, always.** The newest document is not
   automatically the applicable one — a project already in the approval pipeline
   may be governed by a superseded edition.
5. **Mark third-party sources as third-party.** Edition control cannot be
   established for a code PDF found on a document-sharing site.
6. **Set `superseded_by`, don't delete.** Projects approved under old records
   still exist.

---

## Classification vocabulary

| Tag | Meaning |
|---|---|
`#mandatory` | Required by applicable law, authority, regulation or code |
`#project-requirement` | Required by client, developer, operator, tender or brief |
`#international-standard` | From a recognised international standard |
`#best-practice` | Recommended, not necessarily mandatory |
`#assumption` | Temporary, because project information is unavailable |
`#unverified` | Not yet confirmed through an authoritative source |

Compliance statuses: 🟢 COMPLIANT · 🟡 REVIEW REQUIRED · 🟠 NON-COMPLIANT ·
🔴 CRITICAL · ⚪ NOT APPLICABLE · 🔵 INFORMATION REQUIRED

Severity: CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL

Confidence: HIGH · MEDIUM · LOW · UNVERIFIED

---

## Adding regulation PDFs

Drop source PDFs into the relevant discipline folder, or into a `sources`
subfolder per jurisdiction. Then ask NORMIA to extract clause records from them
— it produces one note per clause with a verification trail, and flags anything
it cannot attribute to a specific clause and page.

---

## Status

Vault created 2026-08-10. Knowledge base **empty by design** — awaiting source
documents. [[Authority Directory]] is populated and verified.
