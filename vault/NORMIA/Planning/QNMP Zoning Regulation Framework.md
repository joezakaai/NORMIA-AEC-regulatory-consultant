---
jurisdiction: "[[Qatar]]"
authority: Ministry of Municipality — Urban Planning Department
discipline: "[[Planning]]"
document_title: Qatar National Master Plan — MSDP Zoning Regulations
document_reference: QNMP / MSDP Volumes 1–4
edition: Mixed — Residential zones 12/04/2020; most other zones Aug–Nov 2017; Centre Plans V5 23/03/2023
current_status: CURRENT
source: https://www.mme.gov.qa/QatarMasterPlan/English/msdp-zoning.aspx
source_type: OFFICIAL PORTAL — mme.gov.qa
classification: MANDATORY
status: VERIFIED
confidence: HIGH
date_recorded: 2026-08-10
recorded_by: NORMIA
tags:
  - normia
  - regulation
  - qatar
  - planning
  - zoning
  - index
---

# QNMP Zoning Regulation Framework

> [!info] [[NORMIA]] · [[Qatar]] · [[Planning]] · [[Qatar Zoning Code Register]] · [[Authority Directory]]
> **This is the instrument that attaches FAR, coverage, setbacks, height and parking to the
> zoning codes returned by the national GIS.** It is public and free.

**Portal:** https://www.mme.gov.qa/QatarMasterPlan/English/msdp-zoning.aspx

## The two-tier structure

Quoted from the official QNMP page:

> The **QNDF** "sets the strategic direction and policies to guide the future spatial growth of
> the country", with "Detailed plans for the Municipalities and local areas within Municipalities
> … prepared under the umbrella of the QNDF."

| Tier | Instrument | Carries development control? |
| --- | --- | --- |
| National strategy | **QNDF** — Qatar National Development Framework. Approved by **Council of Ministers decree No. 77, April 2014**; Emiri approval **December 2014** | ❌ Policy and strategy only |
| Municipal | **MSDPs** — Municipal Spatial Development Plans, for **6 municipalities**, horizon 2032 | ✅ In Volume 2 and Volume 4 |

**MSDP volume structure:**

| Volume | Content |
| --- | --- |
| Volume 1 | Strategic vision and development strategy |
| **Volume 2** | **Zoning and land use regulations** — the 21 zones and 7 overlays |
| Volume 3 | Zoning and public facilities maps |
| **Volume 4** | **Centre Plans** — centre-specific land use zones and regulations |

## What is published

**Group (1) — Planning Zones (21):** R1 · R2 · R3 · R4 · R5 · R6 · LInd · MInd · HInd · LDW ·
LFR · EC · GB · OSR · S · CF · TU · RD · SU · SDA · T

**Group (2) — Overlay Zones (7):** Heritage · Obstacle Limitation Surfaces · Coastal Protection ·
Commercial Corridors · Authorized Commercial Nodes · Workers Accommodation · Railway Safeguarded
Area

> [!tip] The overlays are easy to miss and can be decisive
> **Obstacle Limitation Surfaces** (aviation height restriction), **Coastal Protection** and
> **Railway Safeguarded Area** are exactly the constraints NORMIA's Phase 03 asks about — and they
> are published here as overlay regulations even though they are not in the CGIS zoning layer.
> Check them on every project.

**Group (3) — Planning & Design Guidelines (15):** Car Parking Regulations · Advertising & Signs ·
Two Villas on One Plot · Community Facilities Standards · Open Space Guidelines · Master Plan
Application Submission Guidelines · Planning Assessment Guidelines · Malls · Commercial Streets ·
Hypermarkets · Private Education · Private Health · Typical Areas (Location Plan) · Utilities ·
Interim Coastal Development

## Centre Plans — Volume 4

**Centre Plans and Zoning Regulations, Volume 4, Version V, 23/03/2023**, Ministry of Municipality.
Source: `https://www.mme.gov.qa/QatarMasterPlan/Downloads-qnmp/Regulation/English/Centre_Zoning/Centres%20Report.pdf`

This volume holds **MU1, MU2, MU3, SCZ, FCLO** and the centre hierarchy **CCC, MC, DC, TC** — the
codes that do *not* appear in the Group (1) zone set.

**It confirms what the `G+N` suffix means.** Verbatim examples:

> MU1, G+2, Commercial Strip: "Lot size 600 and more: Building Height G+2, Building Coverage 70%,
> FAR 1.9, Front setback 0, Side setback 0, Rear setback 6"
>
> MU1, G+8, Podium & Tower: "FAR Maximum 4.00, Podium coverage 75%, Tower coverage 50%,
> Front setback 0m, Side setback 6m (tower)"

So **`MU1 G+2` is not a separate zone** — it is the built-form/height typology *row* within the
Volume 4 control table for MU1. That resolves the structure seen in the GIS
([[Qatar Zoning Code Register]] §3).

## Editions — a real risk

| Document set | Edition |
| --- | --- |
| Residential zones R1–R6 | **12/04/2020** |
| Tourism (T) | April 2020 |
| Most non-residential zones | **August / November 2017** |
| SDA | 10/12/2017 |
| Large Format Retail | 23/04/2018 |
| Car Parking Regulations | August 2017 |
| Two Villas on One Plot | **01/10/2014** |
| Centre Plans Volume 4 | **V5, 23/03/2023** |

**Edition drift across the set is severe — six years between the oldest guideline and the newest
volume.** Re-check the portal for a newer edition before relying on any 2017-dated zone.

## Records held in this vault

- [[Qatar R1 — Low Density Residential Zone]] ✅
- [[Qatar R2 — Low-Medium Density Residential Zone]] ✅
- [[Qatar R3 — Medium Density Residential Zone]] ✅
- [[Qatar R5 — High Density Residential Zone]] ✅
- [[Qatar R6 — Residential Tower Zone]] ✅
- [[Qatar Car Parking Regulations]] ✅
- [[Qatar Two Villas on One Plot]] ✅

**Not yet extracted:** R4 · all industrial, commercial and open-space zones · all 7 overlays ·
13 of the 15 guidelines · Centre Plans Volume 4 in full.

## Unresolved

| Item | Issue |
| --- | --- |
| **COM, MUC, MUR, RES, NC** | Appear in the CGIS zoning layer but in **no** published zone document found. Probably centre land-use sub-designations or GIS attributes. Resolve via MSDP Volume 2 Addendum 3 (Definitions of Terms) — referenced by Volume 4 but **not located as a public download**. |
| **R1-TYP** | Undefined in any fetched document. The Group (3) guideline "Typical Areas (Location Plan)" is an **image-only PDF with no extractable text** — most likely where the "-TYP" suffix is defined. Needs OCR or a manual read. |
| **DC (District Centre)** | In the Doha zoning map legend and Volume 4, but not in the CGIS code list. |

## How a consultant obtains a plot's designation

The regulation PDFs are free and public. **The plot's actual zoning code is not derivable from
them** — obtain it from the CGIS geoportal (see [[Qatar GIS — Query Recipes]]) or by requesting a
**planning/zoning certificate from the Ministry of Municipality's Urban Planning Department**.

---

**Related:** [[Qatar]] · [[Qatar Zoning Code Register]] · [[Qatar GIS — Query Recipes]] ·
[[Qatar Building Permit Law and Process]] · [[Authority Directory]] · [[NORMIA]]
