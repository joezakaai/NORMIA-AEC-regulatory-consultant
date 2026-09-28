---
title: Qatar GIS — Query Recipes
type: procedure
jurisdiction: "[[Qatar]]"
discipline: "[[GIS]]"
service_root: https://services.gisqatar.org.qa/server/rest/services
spatial_reference: EPSG 2932 — QND95 / Qatar National Grid
authentication: None required
verified: 2026-08-10
status: VERIFIED
confidence: HIGH
tags:
  - normia
  - gis
  - qatar
  - procedure
  - phase-03
---

# Qatar GIS — Query Recipes

> [!info] [[NORMIA]] · [[Qatar National GIS — QMap Source Assessment]] · [[Qatar Zoning Code Register]] · [[Qatar]]

Runnable recipes for **Phase 02 (Plot Sheet Analysis)** and **Phase 03 (GIS Analysis)** on a
Qatari site. All verified live on 2026-08-10. No token, no login.

> [!warning] These services are NOT in the REST directory listing
> `/services/Vector?f=pjson` lists only geocoders and print tools. `Zoning`, `CadastrePlots`,
> `QP_Cadastral` and `Protected_Areas` are reachable **only by direct URL**. That is why this
> note exists — it is the index the server does not give you.

---

## 0. Constants

```text
ROOT   = https://services.gisqatar.org.qa/server/rest/services
SR     = 2932            # QND95 / Qatar National Grid, metres
FORMAT = f=pjson         # or f=json
```

**Coordinates must be in Qatar National Grid (EPSG 2932), not lat/long.** Plot Building
Regulation Sheets in Qatar typically print Easting/Northing on this grid already — use them
directly. To go from WGS84 lat/long instead, pass `inSR=4326` and give `geometry=lon,lat`.

---

## 1. What is the zoning at this point?

**The first question of Phase 03.**

```
{ROOT}/Vector/Zoning/MapServer/0/query
  ?geometry={easting}%2C{northing}
  &geometryType=esriGeometryPoint
  &inSR=2932
  &spatialRel=esriSpatialRelIntersects
  &outFields=*
  &returnGeometry=false
  &f=pjson
```

Returns `ZONING`, `CODE`, `RULEID`, `STARTDATE` and the polygon's area.

**Interpreting the result:** look the code up in [[Qatar Zoning Code Register]].

- A specific class (`R1`, `R2`, `MU2 G+11`, `COM` …) → the State is the controlling planning
  authority. Record it as **VERIFIED classification**, then obtain the Ministry of
  Municipality zoning regulation for the numeric controls.
- **`SD`** → **stop.** The land is Special Development. The national layer holds no
  development control for it. Identify the master developer and obtain the Plot Building
  Regulation Sheet. Do not report "no restrictions found".
- **`EC`, `GB`** → environmental constraint; run recipe 4.
- A very large `SHAPE.AREA` (hundreds of hectares) is itself a signal that you have hit a
  blanket district polygon rather than a parcel-level classification.

---

## 2. Cross-check the plot area against the national cadastre

**Phase 02.** Plot Building Regulation Sheets carry "areas are approximate" disclaimers. The
cadastre gives an independent figure.

### By PIN (plot identification number, printed on the plot sheet)

```
{ROOT}/Vector/CadastrePlots/MapServer/0/query
  ?where=PIN%3D{pin}
  &outFields=PIN,PDAREA,PD_NO,REF_NUMBER,GFCODE,STARTDATE,COMMENTS
  &returnGeometry=false
  &f=pjson
```

### By point

```
{ROOT}/Vector/CadastrePlots/MapServer/0/query
  ?geometry={easting}%2C{northing}
  &geometryType=esriGeometryPoint&inSR=2932
  &spatialRel=esriSpatialRelIntersects
  &outFields=PIN,PDAREA,PD_NO,REF_NUMBER
  &returnGeometry=false&f=pjson
```

**Fields:** `PIN` (plot ID) · `PDAREA` (plot area) · `PD_NO` · `REF_NUMBER` · `GFCODE` ·
`CDST_KEY` · `STARTDATE` / `ENDDATE` · `SHAPE.AREA` / `SHAPE.LEN` · `COMMENTS`.

> [!warning] Report a mismatch, do not resolve it
> If `PDAREA` disagrees with the plot sheet, that is a **🔵 INFORMATION REQUIRED** finding for
> the authority — not a licence to substitute one figure for the other. Where a plot sheet
> states a maximum GFA numerically, keep using the stated GFA (see
> [[QIN Villa Type B — FAR and Plot Coverage]]).

**Privacy:** these fields carry no owner name or contact, and NORMIA must not attempt to
assemble ownership or personal data from this or any adjacent source.

`Vector/QP_Cadastral` is a parallel cadastral service — query it the same way if
`CadastrePlots` returns nothing at a location.

---

## 3. Which municipality, zone and district?

**Phase 01 jurisdiction identification.** Run all three at the site point:

```
{ROOT}/Vector/MunicipalityA/MapServer/0/query?geometry=...   # municipality
{ROOT}/Vector/ZonesA/MapServer/0/query?geometry=...          # zone number
{ROOT}/Vector/DistrictsAr/MapServer/0/query?geometry=...     # district
```

Same parameter pattern as recipe 1. The municipality determines which building-permit
authority applies — see [[Authority Directory]] §1.1.

---

## 4. Environmental and protected-area constraints

```
{ROOT}/Vector/Protected_Areas/MapServer/0/query
  ?geometry={easting}%2C{northing}
  &geometryType=esriGeometryPoint&inSR=2932
  &spatialRel=esriSpatialRelIntersects
  &outFields=*&returnGeometry=false&f=pjson
```

To test **proximity** rather than intersection — usually the more useful question — buffer the
point by passing `distance` and `units`:

```
  &distance=1000&units=esriSRUnit_Meter
```

An empty result means "no protected area found in this layer", **not** "no environmental
constraint". Flood, coastal, aviation and high-voltage corridor layers were **not located** in
this service. Treat those as **UNVERIFIED — separate source required**.

---

## 5. Site history from the imagery archive

Phase 03 / Phase 04. Compare a site across three decades to establish reclamation date, prior
structures, or coastline change:

```
{ROOT}/Imagery/QatarOrtho_1995/MapServer
{ROOT}/Imagery/QatarSatelitte_2003/MapServer
{ROOT}/Imagery/QatarOrtho_2004/MapServer
{ROOT}/Imagery/QatarSatelitte_2010/MapServer
{ROOT}/Imagery/QatarSatelitte_2012/MapServer
{ROOT}/Imagery/QatarSatelitte_2017/MapServer
{ROOT}/Imagery/QatarSatelitte_2019/MapServer
{ROOT}/Imagery/QatarSatelitte_2021/MapServer
{ROOT}/Imagery/QatarSatelitte2024/MapServer
{ROOT}/Imagery/QatarSatelitte/MapServer      # current
{ROOT}/Imagery/QatarOrtho/MapServer          # current
```

Export a clip with `/export?bbox={xmin},{ymin},{xmax},{ymax}&bboxSR=2932&size=1200,1200&format=png&f=image`,
or read tiles at `/tile/{z}/{y}/{x}`.

Particularly relevant on reclaimed land: if a site does not exist in the 2010 image but does in
2017, that tells you something real about fill depth and settlement history that no current
basemap will.

---

## 6. Address and landmark geocoding

```
{ROOT}/Vector/QARS_Custom_Locator/GeocodeServer/findAddressCandidates?SingleLine={text}&f=pjson
{ROOT}/Vector/QARS_CompoundLocator/GeocodeServer/findAddressCandidates?SingleLine={text}&f=pjson
{ROOT}/Vector/Custom_LandmarksLocator/GeocodeServer/findAddressCandidates?SingleLine={text}&f=pjson
```

QARS is the Qatar Address Registration System. Use to resolve a street address or building
number to coordinates before running recipes 1–4.

---

## 7. Standard Phase 03 sweep for a Qatari site

Run in this order and record each result with its source URL and query date:

1. **Municipality / zone / district** → recipe 3 → establishes the permit authority
2. **Zoning** → recipe 1 → land-use classification
3. **If `SD`** → stop the GIS line of enquiry; pivot to the master developer's Plot Building
   Regulation Sheet and district Design Guidelines
4. **Cadastre** → recipe 2 → PIN and area cross-check
5. **Protected areas** → recipe 4, including a 1 km proximity test
6. **Imagery history** → recipe 5 → site formation and prior structures
7. **Record what was NOT tested** — flood, aviation, high-voltage, metro/rail corridors,
   heritage. These are not in this service and remain **UNVERIFIED**.

Every finding is filed as **VERIFIED evidence of a classification**, never as a development
control. Numeric controls require the Ministry of Municipality zoning regulation, which this
vault does not yet hold.

---

## 8. Reliability notes

- **Query the REST API, not the QMap application.** The application froze under automation;
  the API was stable throughout.
- The application at `geoportal.gisqatar.org.qa/qmap/index.html` cannot be read by
  server-side fetching — it is a JavaScript SPA that returns only a browser-compatibility
  stub. A real browser is required to use the map interface.
- No published terms of use were located. Confirm licensing with CGIS before republishing
  extracts in a commercial submission.

---

**Related:** [[Qatar National GIS — QMap Source Assessment]] · [[Qatar Zoning Code Register]] ·
[[Qatar]] · [[GIS]] · [[Authority Directory]] · [[NORMIA]]
