---
title: Qatar Zoning Code Register
type: lookup-register
jurisdiction: "[[Qatar]]"
discipline: "[[GIS]]"
authority: Ministry of Municipality — via Centre for GIS (CGIS)
source: services.gisqatar.org.qa/server/rest/services/Vector/Zoning/MapServer/0
source_type: OFFICIAL PORTAL — live REST query
extracted: 2026-08-10
layer_startdate: 2024-05-26
classification: VERIFIED evidence of classification — NOT a statement of development control
status: VERIFIED
confidence: HIGH
tags:
  - normia
  - gis
  - qatar
  - zoning
  - reference
---

# Qatar Zoning Code Register

> [!info] [[NORMIA]] · [[Qatar National GIS — QMap Source Assessment]] · [[Qatar GIS — Query Recipes]] · [[Qatar]]

The complete `ZONING` code list from the national zoning layer, read live from the Ministry
of Municipality / CGIS service on 2026-08-10. **62 distinct values.**

> [!warning] This register carries classifications, not development controls
> A zoning code tells you the land-use class. It does **not** tell you FAR, plot coverage,
> setbacks or height — except where a code embeds a height suffix (§3). The numeric controls
> live in the Ministry of Municipality zoning regulations, which are **not published through
> this portal and are not yet held in this vault**.
>
> Reporting "zoned R2, therefore FAR is X" is **UNVERIFIED**. Reporting "zoned R2" is VERIFIED.

English column is NORMIA's working translation of the Arabic renderer labels. The Arabic is
the official text.

---

## 1. Residential — المناطق السكنية

| Code | Arabic label | Working English |
| --- | --- | --- |
| **R1**, **R1-TYP** | مناطق سكنية منخفضة الكثافة | Low density residential |
| **R2** | مناطق سكنية منخفضة الى متوسطة الكثافة | Low to medium density residential |
| **R3** | مناطق سكنية متوسطة الكثافة | Medium density residential |
| **R4** | مناطق سكنية متوسطة الى مرتفعة الكثافة | Medium to high density residential |
| **R5** | مناطق سكنية مرتفعة الكثافة | High density residential |
| **R6** | منطقة الابراج السكنية | Residential towers zone |

## 2. Industrial — المناطق الصناعية

| Code | Arabic label | Working English |
| --- | --- | --- |
| **LInd** | مناطق صناعية منخفضة التأثير البيئي — الصناعات الخفيفة | Low environmental impact industrial — light industry |
| **MInd** | مناطق صناعية متوسطة التأثير البيئي — الصناعات المتوسطة | Medium environmental impact industrial — medium industry |
| **HInd** | مناطق صناعية مرتفعة التأثير البيئي — الصناعات الثقيلة | High environmental impact industrial — heavy industry |

## 3. Urban centres and mixed use — المراكز العمرانية

| Code | Arabic label | Working English |
| --- | --- | --- |
| **CCC** | مركز عاصمة | Capital city centre |
| **MC** | مركز حاضرة | Metropolitan centre |
| **TC** | مناطق عبور تجارية | Transit commercial |
| **NC** | خدمة تجارية محلية | Neighbourhood commercial service |
| **COM** | مناطق تجارية | Commercial |
| **MUC** | مناطق استعمالات مختلطة تجارية | Mixed use — commercial |
| **MUR** | مناطق استعمالات مختلطة سكنية | Mixed use — residential |
| **RES** | مناطق سكنية مركزية | Central residential |
| **MU1** | استعمالات مختلطة-1 | Mixed use 1 |
| **MU2** | استعمالات مختلطة-2 | Mixed use 2 |
| **MU3** | استعمالات مختلطة-3 | Mixed use 3 |

### ⭐ Mixed-use codes embed permitted height

This is the one place where the zoning layer carries a **direct regulatory parameter**. MU
codes appear in the data with a `G+N` suffix giving storeys above ground, and some carry an
`-N` / `-S` sub-variant (north / south sub-area):

| Family | Observed height variants |
| --- | --- |
| **MU1** | G+2 · G+3 · G+4 · G+5 · G+6 · G+7 · G+8 · G+8-S · G+11-N · G+11-S |
| **MU2** | G+2 · G+3 · G+4 · G+5 · G+6 · G+8 · G+8-N · G+11 · G+11-N · G+11-S |
| **MU3** | G+2 · G+3 · G+4 · G+5 · G+7 · G+8 · G+8-N · G+8-S · G+11-N · G+11-S |

So a query returning `MU2 G+11` is telling you the parcel permits ground plus eleven storeys.
Treat the storey count as **VERIFIED evidence from the custodial GIS**, but confirm against
the Ministry of Municipality regulation before designing to it — a storey count is not a
metre height, and no height-per-storey is given.

## 4. Other classifications — تصنيفات أخرى

| Code | Arabic label | Working English | NORMIA note |
| --- | --- | --- | --- |
| **SD** | مناطق تنمية خاصة | **Special Development Areas** | ⚠️ **Master-planned districts — controls held by the master developer, not the State.** See §4 of [[Qatar National GIS — QMap Source Assessment]] |
| **SCZ** | مناطق خاصة | Special zones | |
| **SU** | مناطق ذات استعمالات خاصة | Special use zones | |
| **CF** | مناطق خدمات مجتمعية | Community facilities | |
| **T** | مناطق سياحية | Tourism zones | |
| **TU** | مناطق نقل ومرافق بنية تحتية | Transport and infrastructure utilities | Corridor constraint — check adjacency |
| **LDW** | مناطق الخدمات اللوجستية — التوزيع — المخازن | Logistics, distribution and warehousing | |
| **LFR** | مناطق بيع البضائع كبيرة الحجم | Large format retail | |
| **OSR** | مناطق مفتوحة وترفيهية | Open space and recreation | |
| **S** | مناطق خدمات ومرافق رياضية | Sports services and facilities | |
| **GB** | منطقة الحزام الاخضر | Green belt | Development constraint |
| **EC** | مناطق حفاظ / محميات بيئية | Environmental conservation / protected areas | ⚠️ Constraint — cross-check `Vector/Protected_Areas` |
| **RD** | مناطق ريفية / صحراوية | Rural / desert areas | |

---

## 5. Codes that should raise a flag immediately

| Code | Why |
| --- | --- |
| **SD** | The national layer is silent on development control. Find the master developer and their Plot Building Regulation Sheet before saying anything about capacity. |
| **EC**, **GB** | Environmental conservation and green belt — expect development restriction. Cross-check `Vector/Protected_Areas` and the Ministry of Environment and Climate Change. |
| **HInd**, **MInd** | Heavy/medium industry — check separation distances and environmental permitting; also check as an *adjacent* condition for a sensitive receptor. |
| **TU** | Transport/infrastructure corridor. If adjacent to the site, expect reservation or easement. |
| **SCZ**, **SU** | Special regimes — the ordinary zoning regulation may not apply. |

---

## 6. Provenance

| Item | Value |
| --- | --- |
| Layer | `Vector/Zoning/MapServer/0`, geometry type polygon |
| Fields | `ZONING`, `CODE`, `RULEID`, `STARTDATE`, `EMP_NUM`, `JOB`, `SHAPE.AREA`, `SHAPE.LEN`, `OBJECTID` |
| Renderer field | `ZONING` |
| Spatial reference | EPSG 2932 — QND95 / Qatar National Grid |
| Layer `STARTDATE` observed | 2024-05-26 |
| Extracted | 2026-08-10, live REST query |

**Re-verify this register annually**, and whenever a project turns on a classification. Codes
and their boundaries change; the observed start date shows the layer was edited in 2024.

---

**Related:** [[Qatar National GIS — QMap Source Assessment]] · [[Qatar GIS — Query Recipes]] ·
[[Qatar]] · [[GIS]] · [[NORMIA]]
