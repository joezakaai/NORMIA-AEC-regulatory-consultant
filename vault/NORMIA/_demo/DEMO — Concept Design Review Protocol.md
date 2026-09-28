---
title: DEMO — Concept Design Review Protocol
type: demo-harness
status: AWAITING DRAWINGS
created: 2026-08-10
scope: Demonstration only — kept separate from the regulation library
tags:
  - normia
  - demo
  - review-protocol
---

# DEMO — Concept Design Review Protocol

> [!info] [[NORMIA]] · [[Qatar]] · [[Authority Directory]]
> **This folder is the demo sandbox.** Nothing here is a regulation record. The library in
> `NORMIA/Planning`, `Building Codes`, `Fire & Life Safety` etc. stays untouched — this only
> *consumes* it.

**Status: awaiting concept drawings.**

---

## What NORMIA will check, and against what

Each row names the phase, what gets tested, and the **specific vault record** the test is drawn
from. Where a record does not exist, the finding will be reported as 🔵 INFORMATION REQUIRED or
UNVERIFIED rather than guessed.

### Phase 01 — Jurisdiction

| Test | Source |
| --- | --- |
| Country, municipality, district, zone | [[Qatar GIS — Query Recipes]] recipe 3 |
| Which permit authority applies | [[Qatar Building Permit Law and Process]] · [[Authority Directory]] |
| Ordinary municipal land **or** master-planned district | [[Qatar Zoning Code Register]] — the `SD` test |
| Approval chain and gating stages | [[Lusail — Review and Approval Process]] (if SD) |

### Phase 02 — Plot sheet

| Test | Source |
| --- | --- |
| Plot number, PIN, area, boundary, access points | Plot Building Regulation Sheet |
| **Independent area cross-check** against the national cadastre | [[Qatar GIS — Query Recipes]] recipe 2 (`PDAREA` by `PIN`) |
| Stated vs computed GFA consistency | Zone regulation or plot sheet |

### Phase 03 — GIS

| Test | Source |
| --- | --- |
| Zoning classification at the site | [[Qatar GIS — Query Recipes]] recipe 1 |
| Decode the code | [[Qatar Zoning Code Register]] |
| Protected areas, +1 km proximity | Recipe 4 |
| Site history / reclamation date | Recipe 5 — 1995–2024 imagery |
| **What was NOT tested** — flood, aviation, rail, heritage | Reported as UNVERIFIED, not omitted |

### Phase 04 — Topography

Levels, slope, road levels, height datum. **Critical where height is measured from the lowest side
of the plot** — [[QIN Villa Type B — Height, Floors and Level Controls]].

### Phase 05–06 — Development control and buildable envelope

| Test | Ordinary municipal land | Master-planned (Qetaifan) |
| --- | --- | --- |
| Land use | [[QNMP Zoning Regulation Framework]] | Plot sheet |
| FAR / GFA | [[Qatar R1 — Low Density Residential Zone]] etc. | [[QIN Villa Type B — FAR and Plot Coverage]] |
| Plot coverage | ↑ | ↑ |
| Setbacks | ↑ | [[QIN Villa Type B — Setbacks]] |
| Height and floors | ↑ | [[QIN Villa Type B — Height, Floors and Level Controls]] |
| Basement | ↑ | [[QIN Villa Type B — Basement and GFA Exclusion]] |
| Penthouse | ↑ | [[QIN Villa Type B — Penthouse Controls]] |
| Ancillary buildings | ↑ | [[QIN Villa Type B — Ancillary Buildings]] |
| Parking | [[Qatar Car Parking Regulations]] | Plot sheet + [[Lusail — Vehicle Access, Parking Geometry and Site Levels]] |
| Landscape | Zone regulation | [[QIN Villa Type B — Landscape and Soft Landscape Minimum]] |
| Boundary wall | Zone regulation | [[QIN Front Boundary Wall — Heights]] 🟠 |

### Phase 08–09 — Concept and architectural review

Building position · setbacks measured off the drawing · footprint and coverage · GFA take-off ·
height and levels · floor count · parking count and geometry · access · vertical circulation ·
openings and privacy ([[QIN Villa Type B — Openings and Privacy]]) · roof terraces
([[QIN Villa Type B — Roof Terraces]]) · external works.

### Phase 10 — Fire and life safety ⚠️ highest priority

| Test | Source |
| --- | --- |
| Occupancy classification | [[QCDD Civil Defence Technical Requirements Guide]] |
| Egress, travel distance, exits | ↑ — **note the villa gap** |
| Ancillary fire-hazard separation | [[QIN — Ancillary Fire Hazard Uses and Civil Defence]] |
| Approval stage and submission requirements | [[QCDD Drawing Submission and Approval Process]] |

### Phase 11 — Accessibility

[[Qatar Accessibility — Legal Position]] — **no national code**; the applicable standard must be
agreed. [[Lusail — Universal Access and Accessible Parking]] where the district applies.

### Envelope, sustainability, utilities

| Test | Source |
| --- | --- |
| **Window Wall Ratio band and glazing spec** | [[KAHRAMAA Energy and Water Conservation Code]] |
| Roof and wall U-values | ↑ |
| GSAS rating pathway | [[GSAS — Global Sustainability Assessment System]] |
| Stormwater retained on plot, utility routing | [[Lusail — Services Review and Utility Authority Approvals]] |
| Vehicle access, driveway, visibility | [[Ashghal Design Manuals — QHDM and QSDDM]] |

---

## Output format

1. **Dashboard** — project, jurisdiction, stage, issue counts by severity, verified vs unverified.
2. **Compliance register** — one row per test:

   | ID | Discipline | Requirement | Design Condition | Status | Severity | Source | Recommended Action |

   Statuses: 🟢 COMPLIANT · 🟡 REVIEW REQUIRED · 🟠 NON-COMPLIANT · 🔴 CRITICAL · ⚪ N/A · 🔵 INFO REQUIRED
   Severity: CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL
3. **Conflicts** raised, if any.
4. **Information required** before a final determination.
5. **Architect action list** — before continuing design / before submission / authority confirmation.

---

## Rules this demo will hold to

> [!danger] What NORMIA will not do
> - **Not measure what the drawing does not state.** If a setback is not dimensioned and there is
>   no stated scale, the finding is 🔵 INFORMATION REQUIRED — not a scaled guess.
> - **Not report COMPLIANT where the governing control is unverified.** A design cannot be
>   compliant with a requirement nobody has established.
> - **Not invent a regulation to test against.** Every row cites a vault record or is marked
>   UNVERIFIED.
> - **Not treat a master-developer approval as a substitute for authority approval**, or vice versa.

## What will limit this demo

| Limitation | Effect |
| --- | --- |
| **PDF drawings without a reliable scale** | Dimensional checks depend on printed dimensions and stated areas. Scaled measurement off a PDF is indicative only and will be labelled as such |
| **No QCS clause content in the vault** | Construction-technology checks (waterproofing, insulation build-up, finishes) cannot be tested against clauses |
| **QCDD villa gap** | If the concept is a villa, fire compliance cannot be fully determined |
| **No national accessibility code** | Accessibility findings will be against an unagreed standard |
| **Plot-specific road levels not held** | Height-from-lowest-side cannot be closed on a Qetaifan plot |

These are stated up front so the demo is judged on what it can honestly establish.

---

## Drawings received

*(populated on attachment)*

| # | Drawing no. | Title | Discipline | Rev | Scale | Date |
| --- | --- | --- | --- | --- | --- | --- |
