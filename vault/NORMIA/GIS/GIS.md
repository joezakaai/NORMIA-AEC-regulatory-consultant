---
title: GIS
type: discipline
tags:
  - normia
  - discipline
  - gis
---

# GIS

> [!info] Part of [[NORMIA]] · [[Authority Directory]] · Template: [[Regulation Record]]

Spatial constraints, datasets and the sources NORMIA uses for **Phase 03 — GIS Analysis** and
**Phase 02 — Plot Sheet Analysis**.

> [!warning] GIS is evidence, not regulation
> A zoning polygon is verified evidence of a **classification**. It is not a statement of FAR,
> setback, coverage or height. Those come from the authority's written regulation. Never
> convert a zoning code into a development control without the regulation in hand.

---

## Assessed sources

### Qatar

| Source | Custodian | Status | Notes |
| --- | --- | --- | --- |
| [[Qatar National GIS — QMap Source Assessment]] | Centre for GIS (CGIS), Ministry of Municipality | ✅ **VERIFIED — usable** | Public REST, no token. Zoning, cadastre, protected areas, 1995–2024 imagery archive |
| [[Qatar Zoning Code Register]] | Ministry of Municipality via CGIS | ✅ VERIFIED | All 62 national zoning codes with translations |
| [[Qatar GIS — Query Recipes]] | — | ✅ VERIFIED | Runnable queries for Phases 01–03 |

**Key limitation to carry into every Qatari project:** master-planned districts (Lusail,
Qetaifan Island North and others) are classified **`SD` — Special Development** in the national
layer, with **no plot-level control published**. Development control there sits with the master
developer. See [[Lusail — Regulatory Hierarchy and Mandatory Status]].

### Saudi Arabia · UAE · Lebanon

Not yet assessed. See [[Authority Directory]] for the authorities that would hold them.

---

## Not covered by any assessed source

These remain **UNVERIFIED** for Qatar and need a separate custodian:

- Flood zones and stormwater catchments
- Aviation height restriction surfaces (Civil Aviation)
- High-voltage transmission corridors (KAHRAMAA)
- Metro / rail corridors and safeguarding zones (Qatar Rail)
- Road reservations and future infrastructure (Ashghal)
- Heritage and archaeological constraint areas
- Coastal setback lines

---

## Records

```dataview
TABLE custodian, status, confidence
FROM "NORMIA/GIS"
WHERE type = "source-assessment"
```

---

**Related:** [[NORMIA]] · [[Authority Directory]] · [[Qatar]] · [[Planning]] · [[Environment]] · [[Roads]]
