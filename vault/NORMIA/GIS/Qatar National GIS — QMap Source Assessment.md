---
title: Qatar National GIS — QMap Source Assessment
type: source-assessment
jurisdiction: "[[Qatar]]"
discipline: "[[GIS]]"
custodian: Centre for GIS (CGIS), Ministry of Municipality — مركز نظم المعلومات الجغرافية
application: QMap — بوابة نظم المعلومات الجغرافية
application_url: https://geoportal.gisqatar.org.qa/qmap/index.html
service_root: https://services.gisqatar.org.qa/server/rest/services
platform: ArcGIS Server 11.3
spatial_reference: EPSG 2932 — QND95 / Qatar National Grid
authentication: None — public, no token required
assessed: 2026-08-10
assessed_by: NORMIA (live inspection in browser)
status: VERIFIED
confidence: HIGH
tags:
  - normia
  - gis
  - qatar
  - source-assessment
  - verified
---

# Qatar National GIS — QMap Source Assessment

> [!info] [[NORMIA]] · [[Authority Directory]] · [[Qatar]] · [[GIS]]
> Companions: [[Qatar Zoning Code Register]] · [[Qatar GIS — Query Recipes]]

**Verdict: usable as a NORMIA Phase 03 source, with one decisive limitation.**
The national zoning and cadastre layers are public, queryable and authoritative for
ordinary municipal land. **In master-planned districts they return a single blanket
"Special Development" polygon and no plot-level control** — so they cannot substitute for
the master developer's Plot Building Regulation Sheet there.

---

## 1. Custodian and authority status

| Item | Finding |
| --- | --- |
| Application | **QMap** — بوابة نظم المعلومات الجغرافية |
| Custodian | **Centre for GIS (CGIS)**, **Ministry of Municipality** — confirmed from the co-branded splash screen (CGIS Qatar + وزارة البلدية / Ministry of Municipality, State of Qatar) |
| Service host | `services.gisqatar.org.qa/server/rest/services` |
| Platform | Esri **ArcGIS Server 11.3** |
| Coordinate system | **EPSG 2932 — QND95 / Qatar National Grid** (metres) |
| Authentication | **None.** Public REST, no token, no login |
| Interface language | Bilingual Arabic / English; layer labels are **Arabic-only** in the zoning renderer |

CGIS sits under the Ministry of Municipality — the national planning authority recorded in
[[Authority Directory]] §1.1. That makes this the **custodial national GIS**, not a
third-party aggregation.

---

## 2. How it was verified

WebFetch returns only a browser-compatibility stub for this application — it is a
JavaScript SPA and cannot be assessed by fetching HTML. It was opened in a live browser and
its own network traffic read to recover the service endpoints, which are **not discoverable
from the REST directory** (see §5). Layer schemas and zoning codes were then read directly
from the REST API.

---

## 3. What is published

### 3.1 Vector — planning and cadastre

| Service | Content | NORMIA use |
| --- | --- | --- |
| `Vector/Zoning` | **National zoning** — 62 distinct codes, polygon | **Phase 03 / Phase 05 land use and zoning** |
| `Vector/CadastrePlots` | **Cadastral plots** — PIN, plot area | **Phase 02 plot sheet cross-check** |
| `Vector/QP_Cadastral` | Cadastral (secondary/parallel service) | Phase 02 |
| `Vector/ZonesA` | Zone (municipal numbering) boundaries | Jurisdiction identification |
| `Vector/MunicipalityA` | **Municipality boundaries** | **Phase 01 jurisdiction** |
| `Vector/DistrictsAr` | District boundaries | Phase 01 |
| `Vector/Protected_Areas` | **Environmental protected areas** | **Phase 03 constraints** |
| `Vector/ROADFlowlnA` | Road network / flow direction | Phase 03 access |
| `Vector/GeonamesA` · `Landmarks` · `POIs_AR` · `POIs_COMM` | Place names, landmarks, points of interest | Context |
| `Vector/QARS` | Qatar Address Registration System | Address resolution |

**Geocoders** (address → coordinate): `QARS_Custom_Locator`, `QARS_CompoundLocator`,
`Custom_LandmarksLocator`.

### 3.2 Imagery — a 30-year archive

`Imagery/` carries a dated historical series, which is genuinely valuable for site history,
prior structures, coastline and reclamation change:

> **QatarOrtho_1995** · QatarSatelitte_2003 · **QatarOrtho_2004** · QatarSatelitte_2010 ·
> QatarSatelitte_2012 · QatarSatelitte_2017 · QatarSatelitte_2019 · QatarSatelitte_2021 ·
> **QatarSatelitte2024** · QatarSatelitte (current) · QatarOrtho (current)

For a reclaimed or recently developed site this archive can establish when land was formed
and what previously stood on it — evidence no single current basemap provides.

### 3.3 Other folders

`Collector` · `MobileMapping` · `Routing` · `Tafteesh` (تفتيش — inspection) · `Utilities`.
Contents not enumerated; `Tafteesh` and `MobileMapping` are likely internal municipal
workflows rather than public planning data.

---

## 4. ⚠️ The decisive limitation — master-planned districts return "SD"

A point query on the national zoning layer over **Qetaifan Island North / Lusail** returns:

```json
{ "ZONING": "SD", "SHAPE.AREA": 1185332.85, "OBJECTID": 87408502,
  "CODE": 56, "RULEID": 13, "STARTDATE": 1716681600000 }
```

That is **one polygon of ~1,185,333 m² (118 hectares)** classified **SD —
مناطق تنمية خاصة, "Special Development Areas"** — with a start date of **26 May 2024**.

**There is no R1, no villa typology, no FAR, no setback, no height in the national layer for
this land.** The State zones the whole district "Special Development" and delegates detailed
development control to the master developer.

> [!danger] What this means for compliance work
> In Lusail, Qetaifan Island North, and any other SD district, **QMap tells you the land is
> special-development and nothing more**. The governing controls remain the master
> developer's **Plot Building Regulation Sheet** and district Design Guidelines — see
> [[Lusail — Regulatory Hierarchy and Mandatory Status]].
>
> Never report a Qetaifan or Lusail plot as "zoned SD, no restrictions found". The
> restrictions exist; they are simply held by a different custodian.

Outside SD districts — ordinary municipal land — the zoning layer **is** the controlling
land-use classification, and its codes carry real regulatory content (the mixed-use codes
embed permitted height, e.g. `MU2 G+11`). See [[Qatar Zoning Code Register]].

---

## 5. Access characteristics and caveats

| Finding | Detail |
| --- | --- |
| **Directory listing is suppressed** | `/services/Vector?f=pjson` lists only 6 services (geocoders, print tools, Landmarks). The planning services — `Zoning`, `CadastrePlots`, `QP_Cadastral`, `Protected_Areas` — are **absent from the listing but fully accessible by direct URL**. `/services/Vectors` returns empty entirely. **You cannot discover this data by browsing the directory; you must know the service name.** That is what §6 of this note is for. |
| **No authentication** | All queries succeeded with no token. |
| **Full query API** | `/query` supports attribute filters, spatial filters, `outFields`, `returnDistinctValues`. Real analysis is possible, not just map viewing. |
| **No owner data in cadastre** | `CadastrePlots` fields are OBJECTID, ENDDATE, GFCODE, CDST_KEY, **PIN**, JOB, **PDAREA**, STARTDATE, EMP_NUM, SHAPE.AREA, SHAPE.LEN, GLOBALID, REF_NUMBER, PD_NO, COMMENTS. **No name, no owner, no contact.** Good — and NORMIA must not attempt to compile personal information from any adjacent source. |
| **Arabic-only classification labels** | The zoning renderer labels are Arabic. Translations are recorded in [[Qatar Zoning Code Register]]; treat them as NORMIA's working translations, not official English text. |
| **No published terms of use located** | Licensing and permitted-reuse terms were not found. Data may be freely readable but that is not the same as licensed for reuse in a commercial submission. **Confirm with CGIS before republishing extracts.** |
| **Renderer instability** | The QMap application froze under automation after the splash screen. The REST API was stable throughout — **query the API, don't drive the app**. |

---

## 6. Standing in the regulatory hierarchy

Per [[NORMIA]] §9, GIS is **evidence**, not a regulation.

- A zoning polygon is **VERIFIED evidence of a classification**. It is not itself a statement
  of FAR, setback or height.
- The numeric controls attached to a classification come from the **Ministry of Municipality
  zoning regulations** — a separate document not published through this portal. Until those
  are held in this vault, any development control inferred from a zoning code is
  **UNVERIFIED**.
- The cadastre gives **PIN and PDAREA**, which is enough to **cross-check a plot sheet's
  stated area** — a genuinely useful independent check, since plot sheets carry
  "areas are approximate" disclaimers.

> [!warning] Do not state a development control on the strength of a zoning code alone
> "The site is zoned R2" is VERIFIED. "The site is zoned R2, therefore FAR is X" is
> **UNVERIFIED** until the Ministry of Municipality zoning regulation is in hand.

---

## 7. What is still missing

1. **Ministry of Municipality zoning regulations** — the document that attaches FAR, coverage,
   setbacks and heights to each zoning code. This is the highest-value acquisition for the
   Qatar library.
2. **Terms of use / data licence** for CGIS data.
3. Flood, drainage, aviation-restriction and high-voltage corridor layers — **not found** in
   the services observed. Absence here is not evidence of absence nationally.
4. Contents of the `Collector`, `MobileMapping`, `Routing`, `Tafteesh` and `Utilities` folders.
5. Metadata currency — only the zoning layer exposed a `STARTDATE` (2024-05-26). Update
   frequency for cadastre and other layers is unknown.

---

**Related:** [[Qatar Zoning Code Register]] · [[Qatar GIS — Query Recipes]] ·
[[Qatar]] · [[Authority Directory]] · [[GIS]] · [[NORMIA]]
