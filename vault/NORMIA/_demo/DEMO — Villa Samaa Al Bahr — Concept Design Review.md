---
title: DEMO — Villa Samaa Al Bahr — Concept Design Review
type: demo-review
project: Villa Samaa Al Bahr
location: Qetaifan Island North — East Villa Precinct, Al Daayen, Qatar
plot: QN-V2-B-15 (land area matches)
client: Mohammad Jaber
architect: NAZA Architecture Studio / grown studio, Mexico City
consultant: Nemanja Biondic
stage: S.D — Schematic Design
drawings_dated: 2026-05-18 / 2026-06-13
reviewed: 2026-08-10
output_mode: CONCEPT DESIGN REVIEW
status: DEMONSTRATION
tags:
  - normia
  - demo
  - review
  - qatar
  - qetaifan
---

# NORMIA PROJECT COMPLIANCE — DEMO

**Project:** Villa Samaa Al Bahr
**Location:** Qetaifan Island North — East Villa Precinct, Al Daayen, Qatar
**Stage:** S.D — Schematic Design
**Jurisdiction:** State of Qatar → Al Daayen Municipality → Lusail (LREDC/CAC) → Qetaifan Island North (QP)

| | |
| --- | --- |
| **Overall Compliance** | **Not meaningful** — 2 critical issues and no site plan. A percentage would misrepresent the position. |
| 🔴 **Critical** | **2** |
| 🟠 **High** | **3** |
| 🟡 **Medium** | **4** |
| 🔵 **Information Required** | **6** |
| 🟢 Verified compliant | **4** |
| Regulations applied | 19 vault records |

> [!info] Demo scope
> This is a demonstration run of the full NORMIA protocol — [[DEMO — Concept Design Review Protocol]].
> It consumes the regulation library; it does not modify it.

---

## 1. Documents reviewed

12 sheets, AutoCAD 2022, A1 format, stated scale 1:50.

| # | Sheet | Title | Date |
| --- | --- | --- | --- |
| 1 | **A-100** | Basement floor | 2026_06_13 |
| 2 | **A-101** | Ground floor | 2026_05_18 |
| 3 | **A-102** | First floor | 2026_05_18 |
| 4 | **A-103** | **Second floor** | 2026_05_18 |
| 5 | **A-104** | Roof | 2026_05_18 |
| 6 | **A-200** | Longitudinal Section 7 | 2026_05_18 |
| 7 | **A-201** | Longitudinal Section 8 | 2026_05_18 |
| 8 | **A-202** | Transversal Sections 3 & 4 | 2026_05_18 |
| 9–12 | **A-300 / 301 / 302 / 303** | Front / East / West / South elevations | 2026_05_18 |

Plus three source DWGs (plans, sections, elevations).

**Title block data, repeated on every sheet:**

| Field | Value |
| --- | --- |
| LAND AREA | **786.15 SQM** |
| BUILT AREA | **819.65 SQM** |
| FREE AREA | **458 SQM** |
| Project phase | **S.D** (Schematic Design) |

> [!tip] Jurisdiction confirmed from the drawings themselves
> Land area **786.15 m²** matches the Qetaifan Island North plot record exactly, and the location
> field reads "QETAFAIN ISLAND". The governing controls are therefore the **master developer's**
> — [[Lusail — Regulatory Hierarchy and Mandatory Status]] — not the national R-zone regulations.
> The national GIS returns only `SD` here ([[Qatar Zoning Code Register]]).

---

## 2. Level structure, as drawn

From sections A-200/201/202 and the plans:

| Level | FFL | Storey height below |
| --- | --- | --- |
| Roof | **+14.525** (elements to **+15.00**) | 3.85 m |
| **"Penthouse" / "Second floor"** | **+10.675** (also +10.15, +11.22) | 3.85 m |
| First floor | **+6.825** | **5.95 m** |
| Ground floor | **+0.875** | — |
| Access sidewalk | **±0.00** | — |
| Underground parking | **−2.10** (FFL −2.275) | — |

Elevations A-300–A-303 confirm the building tops at **+15.00**.

---

## 3. Compliance Register

| ID | Discipline | Requirement | Design Condition | Status | Sev. | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **C-01** | Planning | **Max GFA 472 m²** (plot sheet); ancillary buildings included | **BUILT AREA 819.65 m²** stated on every sheet. No area schedule; composition not stated | 🔴 | **CRITICAL** | [[QIN Villa Type B — FAR and Plot Coverage]] |
| **C-02** | Planning | **G + 1 + P**; penthouse ≤ **40% of first-floor footprint**, min 3 m back from first-floor front and rear façades | A-103 is titled **"Second floor"** — a full storey of bedrooms, living, kitchen and terraces across the plan. Sections label the same level "penthouse" | 🔴 | **CRITICAL** | [[QIN Villa Type B — Penthouse Controls]] |
| **H-01** | Planning | DG level bands: ground ≤ **+5.5 m**, first ≤ **+9.0 m** | First floor **+6.825** (+1.325 over); penthouse **+10.675** (+1.675 over) | 🟠 | HIGH | [[QIN Villa Type B — Height, Floors and Level Controls]] |
| **H-02** | Planning | Max **15.00 m** measured **from the lowest side of the plot**, incl. all parapets and roof structures | Tops at **+15.00** measured from **"access sidewalk" ±0.00**. Datum is not the regulated one; **zero headroom remains** | 🟠 | HIGH | ↑ |
| **H-03** | Drawings | Setbacks 5 m front (max 10 m) / 3 m sides / 6 m rear must be demonstrable | **No site plan in the set.** No sheet dimensions the building to the plot boundary | 🟠 | HIGH | [[QIN Villa Type B — Setbacks]] |
| **M-01** | Planning | Projections: only architectural elements may project **1.5 m** into neighbour side setback, **no openings** | First floor shows **2.00 m** projections beyond grids 1 and 5 (overall 30.00 m vs 26.00 m grid) | 🟡 | MEDIUM | ↑ |
| **M-02** | Planning | Basement excluded from GFA **only if naturally ventilated AND non-habitable**; habitable ≤ 50% of footprint | One level shown ✅, but **no ventilation strategy and no habitable/non-habitable split** | 🟡 | MEDIUM | [[QIN Villa Type B — Basement and GFA Exclusion]] |
| **M-03** | Developer | Boundary wall — **2.50 m vs 3.00 m unresolved** | No boundary wall height annotated on any elevation | 🟡 | MEDIUM | [[Regulatory Conflict — Boundary Wall Height, Qetaifan Villa Precincts]] |
| **M-04** | Roads | **2 spaces** min; typical bay **2.65 × 5.80 m**, aisle **6.70 m** | Underground parking shown; **no space count, no bay dimensions** | 🟡 | MEDIUM | [[Lusail — Vehicle Access, Parking Geometry and Site Levels]] |
| **I-01** | Planning | Min **5%** soft irrigated landscape; **≥2 mature trees** in front garden | ~9 trees drawn along the front ✅ likely; **no landscape area schedule** to evidence 5% | 🔵 | INFO | [[QIN Villa Type B — Landscape and Soft Landscape Minimum]] |
| **I-02** | Planning | Swimming pool **min 2.00 m** from external plot boundary | Pool drawn along the east side; **not dimensioned to the boundary** | 🔵 | INFO | [[QIN Villa Type B — Setbacks]] |
| **I-03** | Envelope | Glazing U-value and **SHGC band at 40% Window Wall Ratio** | Extensive glazing on all elevations; **no WWR calculation, no glazing spec** | 🔵 | INFO | [[KAHRAMAA Energy and Water Conservation Code]] |
| **I-04** | Fire | QCDD approval required at **DC-1**; fire strategy, egress, ancillary separation | **No fire strategy drawing in the set** | 🔵 | INFO | [[QCDD Drawing Submission and Approval Process]] |
| **I-05** | Sustainability | **GSAS 2-star minimum**, demonstrated at all review stages | Not evidenced | 🔵 | INFO | [[Lusail — GSAS Two-Star Minimum Rating]] |
| **I-06** | Drawings | Title block must carry PIN, plot/street numbers, applicable codes with editions, revision history | Title block carries no PIN, no revision number; **dates inconsistent** (A-100 06_13, rest 05_18) | 🔵 | INFO | [[QCDD Drawing Submission and Approval Process]] |
| **P-01** | Planning | Plot coverage ≤ **50%** | Land 786.15 − Free 458 = **328.15 m² footprint = 41.7%** | 🟢 | — | [[QIN Villa Type B — FAR and Plot Coverage]] |
| **P-02** | Planning | Ground floor ≤ **+1.00 m** above plot access level | **+0.875 m** | 🟢 | — | [[QIN Villa Type B — Height, Floors and Level Controls]] |
| **P-03** | Planning | **One** basement level permitted | One level, −2.10 | 🟢 | — | [[QIN Villa Type B — Basement and GFA Exclusion]] |
| **P-04** | Planning | Land use — Residential Low Density Villa | Single villa ✅ | 🟢 | — | Plot Building Regulation Sheet |

---

## 4. The two critical issues, explained

### 🔴 C-01 — Built area is 174% of the permitted GFA

The plot's maximum GFA is **472 m²**. Every sheet in this set states **BUILT AREA: 819.65 SQM** —
an apparent excess of **347.65 m²**.

The set contains **no area schedule**, so it cannot be established what the 819.65 m² comprises.
Testing the most favourable reading:

- Implied footprint = 786.15 − 458 (free area) = **328.15 m²**
- If the basement is a full-footprint level and were **entirely** excluded from GFA, the
  above-ground total would be ≈ **491.5 m²** — **still above 472 m²**.

So even on the assumption most generous to the design, the scheme appears over. And that
assumption is not yet earned: basement exclusion requires the area to be **both naturally
ventilated and non-habitable** (M-02), and **ancillary buildings count toward GFA**.

**This is the finding that governs the scheme.** It is not a detailing issue — it is a massing
issue, and it should be resolved before any further design development.

### 🔴 C-02 — The top floor is a second storey, not a penthouse

The plot permits **G + 1 + P**. A penthouse is capped at **40% of the first-floor footprint** and
must sit **at least 3 m back from the first-floor front and rear façades**.

- **A-103 is titled "Second floor"** — not "Penthouse".
- It contains bedrooms, bathrooms, a living area, a kitchen and terraces distributed across both
  ends of the plan.
- Sections A-200/201/202 label the same level **"penthouse"**.

The drawings are therefore internally inconsistent about what this level is, and as drawn it reads
as a **full third storey**. A 40% cap on the first-floor footprint would produce a much smaller,
centrally-inset volume than what is shown.

> [!warning] The naming matters at review
> QP's Architectural Review Committee will read a sheet titled "Second floor" as exactly that.
> If the intent is a compliant penthouse, the plan must be redrawn to the 40% footprint and the
> 3 m stepbacks, and titled accordingly. If the intent is a genuine second storey, it is not
> permitted on this plot.

---

## 5. Why the height is tighter than the drawings suggest

The building tops at **+15.00** against a 15 m limit — apparently exact compliance. Two reasons it
is not that simple:

**The datum is wrong.** The design measures from **"access sidewalk" ±0.00**. The Design
Guidelines measure from **the lowest side of the plot**, including all parapets and roof
structures. On a plot with any fall, the lowest side sits **below** the access sidewalk — and the
design has **zero headroom** to absorb that. Every centimetre of fall is a centimetre of
non-compliance.

**The intermediate bands are already exceeded.** The DG sets maxima at **+5.5 m** and **+9.0 m**.
The design places the first floor at **+6.825** and the penthouse at **+10.675** — over by 1.325 m
and 1.675 m. The scheme achieves 15 m overall by using generous 5.95 m and 3.85 m storey heights,
which is precisely what those intermediate bands exist to prevent.

Resolving this needs the plot's road levels — still outstanding from the Qetaifan document set,
where the levels drawing supplied is a **site-wide 1:500 sheet covering many plots**.

---

## 6. The missing drawing

**There is no site plan.** The set runs basement → ground → first → second → roof → sections →
elevations, with no sheet showing the building set out against the plot boundary.

For this plot that is the single most consequential omission. The footprint occupies roughly 42%
of a 786 m² plot with a 5 m front, 3 m side and 6 m rear setback regime plus a **maximum 10 m**
front setback — and the first floor projects **2.00 m** beyond the structural grid at both ends.
None of that can be checked without a dimensioned site plan.

**Until it is provided, no setback finding can be issued either way.** NORMIA does not scale
setbacks off an undimensioned PDF.

---

## 7. Information required before a final assessment

1. **Area schedule by floor**, stating what is included in BUILT AREA and what basement area is
   claimed as excluded from GFA.
2. **Site plan** dimensioned to the plot boundary, showing all setbacks, the pool, ancillary
   structures and the boundary wall.
3. **Plot road levels** and the surveyed lowest point of the plot, to fix the height datum.
4. **Basement ventilation strategy** and a habitable / non-habitable split.
5. **Parking layout** with space count and bay dimensions.
6. **Boundary wall elevations** with heights — pending the 2.5 m / 3.0 m ruling.
7. **WWR calculation** and glazing specification against the KAHRAMAA bands.
8. **Fire strategy** for QCDD DC-1, and confirmation of what governs villa fire safety given the
   gap in the 2022 guide.
9. **GSAS pathway** and appointed service provider.
10. **Landscape schedule** evidencing 5% soft irrigated area.

---

## 8. Architect Action List

### BEFORE CONTINUING DESIGN

1. **Resolve the GFA position.** Produce the area schedule and establish whether the scheme is
   over the 472 m² cap. If it is, this is a massing revision, not a detailing one.
2. **Decide what the top floor is** — a compliant penthouse at ≤40% of the first-floor footprint
   with 3 m stepbacks, or a second storey that is not permitted. Retitle and redraw accordingly.
3. **Re-set the height datum** to the lowest side of the plot and re-test the section. Expect to
   lose height, not gain it.
4. **Bring the first floor and penthouse levels down** within the +5.5 m and +9.0 m bands, which
   will likely require reducing the 5.95 m ground-floor storey height.
5. **Produce a dimensioned site plan.**

### BEFORE AUTHORITY SUBMISSION

1. Parking count and geometry to Lusail dimensions.
2. Boundary wall design to **2.50 m** front until the conflict is ruled on.
3. WWR and glazing specification to the KAHRAMAA bands.
4. Fire strategy and QCDD submission prepared for **DC-1**, in parallel with the architectural
   review — not after it.
5. Title blocks completed with PIN, plot and street numbers, code editions and revision history.

### AUTHORITY CONFIRMATION REQUIRED

1. Boundary wall height — [[Regulatory Conflict — Boundary Wall Height, Qetaifan Villa Precincts]]
2. Basement "naturally ventilated" test
3. Villa fire safety basis post-2022 guide
4. Accessibility standard accepted for villa submissions

---

## 9. What this demo could not test

Stated plainly so the result is not over-read:

| Not tested | Why |
| --- | --- |
| **Setback compliance** | No site plan; no boundary dimensions |
| **Exact penthouse ratio** | No area schedule; scaling off a PDF is not evidence |
| **Height against the true datum** | Plot-specific road levels not held |
| **Construction technology** (waterproofing, insulation, finishes) | **No QCS clause content in the vault** — the official portal is unreachable |
| **Fire compliance for a villa** | The 2022 QCDD guide has no dwelling chapter |
| **Accessibility** | Qatar has no national built-environment accessibility code |
| **Structural, MEP** | Not in the submitted set |

---

**Related:** [[DEMO — Concept Design Review Protocol]] · [[NORMIA]] · [[Qatar]] ·
[[Lusail — Regulatory Hierarchy and Mandatory Status]] · [[Authority Directory]]
