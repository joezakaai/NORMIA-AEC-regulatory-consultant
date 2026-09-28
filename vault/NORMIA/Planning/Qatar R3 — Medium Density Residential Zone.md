---
jurisdiction: "[[Qatar]]"
region: National — ordinary municipal land
authority: Ministry of Municipality — Urban Planning Department
discipline: "[[Planning]]"
document_title: Qatar National Master Plan — Zone Development Control and Design Regulations — Residential R3 (Medium Density Residential Zone)
document_reference: R3
edition: 12/04/2020
publication_date: 2020-04-12
effective_date: ""
current_status: CURRENT (verify against the MSDP zoning page)
source: https://www.mme.gov.qa/QatarMasterPlan/Downloads-qnmp/Regulation/English/01-Residential%20Zones/03-Residential%203%20-%20Eng%20-%2012042020.pdf
source_type: OFFICIAL PDF — mme.gov.qa
classification: MANDATORY
status: VERIFIED
confidence: HIGH
applies_to_use: "Residential R3 (Medium Density Residential Zone)"
applies_to_stage: Land Evaluation · Feasibility · Concept · Authority Submission
date_recorded: 2026-08-10
recorded_by: NORMIA
tags:
  - normia
  - regulation
  - qatar
  - planning
  - zoning
  - mandatory
---

# Qatar R3 — Medium Density Residential Zone

> [!info] [[NORMIA]] · [[Qatar]] · [[Planning]] · [[Qatar Zoning Code Register]] · [[QNMP Zoning Regulation Framework]]
> Zone code **R3** · Ministry of Municipality · Edition **12/04/2020**
> Source: https://www.mme.gov.qa/QatarMasterPlan/Downloads-qnmp/Regulation/English/01-Residential%20Zones/03-Residential%203%20-%20Eng%20-%2012042020.pdf

> [!warning] Applies to ordinary municipal land only
> Master-planned districts (Lusail, Qetaifan Island North, Msheireb, Education City, Qatar Free
> Zones) are outside this instrument — they are zoned **SD** and carry their own development
> control. See [[Qatar National GIS — QMap Source Assessment]] §4.

## Requirement

The R3 controls are published as a **lot-size-banded table**, not as single values. Endpoints
quoted verbatim from the official PDF:

> FAR: "1.3" to "1.8"
> Building coverage: "50"%
> Front setback: "3"m
> Side setback: "3"m — "1.5m" on 200–300 m² plots
> Rear setback: "3"m — "2m" on 200–300 m² plots
> Height: "G + 3" for most plots; "G + 2" under 400 m²
> Top lot-size band: "≥540" m²

## Value / Criterion

| Control | Range | Unit | Note |
| --- | --- | --- | --- |
| FAR (max) | **1.3 – 1.8** | — | **Banded by lot size** |
| Building coverage (max) | **50** | % | |
| Front setback | **3.00** | m | |
| Side setback | **3.00** | m | **1.50 m** on 200–300 m² plots |
| Rear setback | **3.00** | m | **2.00 m** on 200–300 m² plots |
| Height | **G+2 to G+3** | storeys | G+2 under 400 m²; G+3 for most plots |
| Top lot-size band | **≥ 540** | m² | |

> [!danger] These are **band endpoints, not scalar values**
> R3 controls are a matrix keyed to lot size. **Read the row for the actual plot area from the
> source PDF.** Applying "FAR 1.8" to a small plot would be wrong.

## Design Consequence

R3 is the first zone where **coverage drops to 50%** and the front setback relaxes to 3 m —
the built form shifts from detached villa toward denser townhouse/apartment typologies at G+3.

The banded structure means plot area is not just an input to the GFA calculation; it changes
**which FAR, setback and height row applies**. Establish the exact plot area from the cadastre
before quoting any figure — see [[Qatar GIS — Query Recipes]] recipe 2.

## Interpretation Notes

Only the band endpoints were captured from the source. The intermediate rows — and the exact
lot-size thresholds between them — must be read from the PDF for any specific plot. This record
is **VERIFIED as to the endpoints and structure**, and deliberately does not state a single FAR.

## Verification Trail

- [x] Official PDF fetched from mme.gov.qa
- [x] Values quoted verbatim from the fetched document
- [x] Edition date recorded (12/04/2020)
- [ ] Confirmed no newer edition on the MSDP zoning page
- [ ] Confirmed the plot's zoning designation from the CGIS geoportal or a planning certificate

## Open Questions for the Authority

1. Confirm the full lot-size band table and thresholds for the specific plot area.

---

**Related:** [[QNMP Zoning Regulation Framework]] · [[Qatar Car Parking Regulations]] · [[Qatar Zoning Code Register]] · [[Qatar GIS — Query Recipes]] · [[Qatar]]
