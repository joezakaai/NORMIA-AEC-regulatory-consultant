---
title: Qatar
type: jurisdiction
tags:
  - normia
  - jurisdiction
  - qatar
---

# Qatar

> [!info] Part of [[NORMIA]] · [[Authority Directory]] · Template: [[Regulation Record]]

State of Qatar. See [[Authority Directory]] §1 for verified authorities and official portals.

> [!important] There is no single "Qatar Building Code"
> The stack is: **statute** ([[Qatar Building Permit Law and Process]]) → **planning/development
> control** ([[QNMP Zoning Regulation Framework]]) → **construction technology**
> ([[Qatar Construction Specifications (QCS)]]) → **fire & life safety**
> ([[QCDD Civil Defence Technical Requirements Guide]]) → **envelope/energy**
> ([[KAHRAMAA Energy and Water Conservation Code]]) → utilities and roads.
> Each is a separate approval with its own authority. None substitutes for another.

---

## 1. Development control — what can be built

**[[QNMP Zoning Regulation Framework]]** is the instrument that attaches FAR, coverage, setbacks,
height and parking to the zoning codes returned by the national GIS. **Public and free.**

### Residential zones — extracted with verified values

| Zone | FAR | Coverage | Height | Front / Side / Rear | Min plot |
| --- | --- | --- | --- | --- | --- |
| **[[Qatar R1 — Low Density Residential Zone]]** | 1.65 | 60% | 13 m (G+1+P) | 5 / 3 / 3 m | 600 m² |
| **[[Qatar R2 — Low-Medium Density Residential Zone]]** | 1.65 | 60% | 13 m (G+1+P) | 5 / **3 (1.5 blank façade)** / 3 m | 400 m² |
| **[[Qatar R3 — Medium Density Residential Zone]]** | 1.3–1.8 | 50% | G+2 to G+3 | 3 / 3 / 3 m | banded |
| **[[Qatar R5 — High Density Residential Zone]]** | 1.3–3.6 | 50% | G+2 to G+7 (G+9 large lots inside D-Ring) | 3 / 1.5–5 / 2–6 m | banded |
| **[[Qatar R6 — Residential Tower Zone]]** | 1.3–5.5 | 50% | up to G+10 (G+12 ≥4,000 m²) | 3 / 1.5–6 m | ≥20 m boundary |

> [!warning] R3, R5 and R6 are **lot-size-banded matrices**, not scalar values
> The figures above are band endpoints. **Read the row for the actual plot area from the source
> PDF.** Establish plot area from the cadastre first — [[Qatar GIS — Query Recipes]] recipe 2.

Also extracted: **[[Qatar Car Parking Regulations]]** · **[[Qatar Two Villas on One Plot]]**

> [!danger] Unresolved FAR conflict
> R1/R2 give **FAR 1.65** (2020); [[Qatar Two Villas on One Plot]] gives **FAR 1.4** (2014) at the
> same 60% coverage. Which governs a two-villa application is not resolved in the published set.

**Not yet extracted:** R4 · all industrial, commercial and open-space zones · **all 7 overlays**
(Heritage, Obstacle Limitation Surfaces, Coastal Protection, Commercial Corridors, Authorized
Commercial Nodes, Workers Accommodation, Railway Safeguarded Area) · 13 of 15 guidelines ·
Centre Plans Volume 4 in full.

---

## 2. Building permit and technical standards

- **[[Qatar Building Permit Law and Process]]** — Law No. 4 of 1985 as amended by Law No. 8 of 2014.
  Permits issued by the Ministry of Municipality's Development and Building Permits Section.
  **Individuals cannot self-file** — submission is through a registered consultant.
- **[[Qatar Construction Specifications (QCS)]]** — the national technical specification, 29
  sections. ⚠️ **QCS 2014 (mandatory) and QCS 2024 (optional) are both live.**
- **[[KAHRAMAA Energy and Water Conservation Code]]** — ⭐ the most architecturally binding national
  performance requirement. Roof U ≤ 0.437, wall U ≤ 0.568 W/m²·°C; glazing and SHGC banded at
  **40% Window Wall Ratio**. Enforced by refusing the electricity connection.

---

## 3. Fire and life safety

- **[[QCDD Civil Defence Technical Requirements Guide]]** — the 2022 guide, free from the MOI
  portal. Based on **NFPA (NFPA 5000), not the IBC**.
- **[[QCDD Drawing Submission and Approval Process]]** — life-safety drawings are approved at
  **DC-1**, not at permit stage.

> [!danger] The villa gap
> The 2022 guide supersedes the 2015 guidelines but **contains no chapter on villas or one/two-family
> dwellings.** What now governs villa fire safety could not be determined. Confirm with GDCD.

---

## 4. Accessibility

**[[Qatar Accessibility — Legal Position]]** — 🔴 **Qatar has no confirmed national built-environment
accessibility code.** Law No. 22 of 2025 creates a mandatory duty effective 19 Nov 2025 with a
~one-year modification deadline, but the **executive regulations carrying any technical criteria
were not confirmed as issued.** Agree the standard with the authority in writing.

---

## 5. Sustainability

**[[GSAS — Global Sustainability Assessment System]]** — GORD, 4th Edition. **No national mandate
found.** Mandatory where imposed: Lusail requires 2-star.

---

## 6. Roads, drainage and utilities

- **[[Ashghal Design Manuals — QHDM and QSDDM]]** — ⚠️ QHDM **2015 and 2021 both live**; QSDDM Vol 4
  (June 2005) still normatively cited in 2023. Amended continuously by Interim Advice Notes.

---

## 7. GIS

| Note | Use |
| --- | --- |
| [[Qatar National GIS — QMap Source Assessment]] | What is published, custodianship, limitations |
| [[Qatar Zoning Code Register]] | All 62 national zoning codes, translated |
| [[Qatar GIS — Query Recipes]] | Runnable queries — zoning at a point, cadastre by PIN, protected areas, imagery history |

> [!danger] Master-planned districts return `SD` and nothing more
> Lusail and Qetaifan Island North are classified **`SD` — Special Development Areas** as a single
> blanket polygon with no plot-level control. Development control there belongs to the master
> developer. Never report an SD site as having no restrictions.

---

## 8. Master-planned districts — Lusail / Qetaifan Island North

District controls sit **on top of** the national stack, never replacing it.

| Body | Role |
| --- | --- |
| **LREDC** | Master Developer, Lusail City |
| **CAC** | Development control authority; Concept, DC-1, Services Review, DC-2; interpretation final and binding |
| **Qetaifan Projects (QP)** | Master Developer, Qetaifan Island North |
| **Al Daayen Municipality** | Issues the building permit on a CAC approval |
| **Marafeq** | Gas (SNG), district cooling, vacuum waste |

**Cross-cutting:** [[Lusail — Regulatory Hierarchy and Mandatory Status]] ·
[[Lusail — Review and Approval Process]] · [[Lusail — Vehicle Access, Parking Geometry and Site Levels]] ·
[[Lusail — Services Review and Utility Authority Approvals]] ·
[[Lusail — Universal Access and Accessible Parking]] · [[Lusail — GSAS Two-Star Minimum Rating]]

**Villa Type B (Parkside) typology controls:**
[[QIN Villa Type B — FAR and Plot Coverage]] · [[QIN Villa Type B — Setbacks]] ·
[[QIN Villa Type B — Height, Floors and Level Controls]] · [[QIN Villa Type B — Penthouse Controls]] ·
[[QIN Villa Type B — Basement and GFA Exclusion]] · [[QIN Villa Type B — Openings and Privacy]] ·
[[QIN Villa Type B — Roof Terraces]] · [[QIN Villa Type B — Ancillary Buildings]] ·
[[QIN Villa Type B — Landscape and Soft Landscape Minimum]]

**Boundary treatment:** [[QIN Front Boundary Wall — Heights]] 🟠 ·
[[QIN Front Boundary Wall — Gates, Materials and Finishes]]

**Fire:** [[QIN — Ancillary Fire Hazard Uses and Civil Defence]]

---

## 9. Open conflicts

| Severity | Conflict |
| --- | --- |
| 🟠 HIGH | [[Regulatory Conflict — Boundary Wall Height, Qetaifan Villa Precincts]] |
| 🟠 HIGH | **QCS 2014 (mandatory) vs QCS 2024 (optional)** — no repeal found |
| 🟡 MEDIUM | **FAR 1.65 vs 1.4** — R1/R2 zone regulations vs Two Villas guidance |
| 🟡 MEDIUM | **QHDM 2015 vs 2021** — both live per Ashghal's own IAN |
| 🔵 INFO | **QCDD villa gap** — 2015 provisions superseded, nothing published in their place |

---

## 10. Version-control watch list

| Item | Issue |
| --- | --- |
| "**MMUP**" in QIN DG Rev 2 (2023) | **Obsolete** — reorganised 2021 into Ministry of Municipality and MECC |
| "Ministry of the Environment" | Now Ministry of Environment and Climate Change |
| **KAHRAMAA code filename** | URL says "2016"; document is **Issue 1, 29.05.2023**. Re-download, don't reuse cached copies |
| **QCS edition** | Cite by year, not ordinal — Ashghal calls QCS 2014 "the 4th Edition", press has called it the fifth |
| **GSAS versioning** | "4th Edition" spans 2019 (CM, Operations) and 2025 (D&B). Cite the specific manual |
| **Non-residential zones** | Most are 2017 — six years older than the newest volume. Check for reissue |
| **IAN numbering** | Not a date cue — IAN 048/14 is "Rev 0" yet dated August 2023 |

---

## 11. Highest-value acquisitions

1. **QCS clause content** — the official portal `qcs.qs.gov.qa` was unreachable. **No numeric QCS
   requirement is held in this vault.**
2. **Law 22/2025 executive regulations** — would be Qatar's first binding accessibility criteria.
3. **QCDD position on villas** — the gap left by the 2022 supersession.
4. **MSDP Volume 2 Addendum 3 (Definitions of Terms)** — would resolve COM, MUC, MUR, RES, NC and
   likely R1-TYP.
5. **QSDDM Volume 8 (Developers Guide)** — the drainage volume that governs the plot interface.
6. **The 7 overlay zone regulations** — aviation, coastal and railway constraints.

---

**Related:** [[NORMIA]] · [[Authority Directory]] · [[Saudi Arabia]] · [[UAE]] · [[Lebanon]]
