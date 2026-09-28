---
title: Authority Directory
scope: Qatar · Saudi Arabia · United Arab Emirates · Lebanon · Jordan
purpose: Routing index — WHO regulates WHAT, and WHERE their official portal is
compiled: 2026-08-10
method: Web verification of official portals. Authority names, portal URLs and
  document TITLES only.
contains_numeric_requirements: false
tags:
  - normia
  - authorities
  - reference
  - qatar
  - saudi-arabia
  - uae
  - lebanon
  - jordan
---

# AUTHORITY DIRECTORY

> [!info] Part of [[NORMIA]] · See also [[Regulation Record]] · [[Project Intake]]

## HOW TO USE THIS FILE

This is a **routing index, not a source of requirements.** It tells NORMIA which
authority governs which discipline in which jurisdiction, and where that
authority's official portal is. It deliberately contains **no setbacks, no
heights, no FAR, no coverage, no parking ratios, no clause values of any kind.**

Every requirement must still be obtained from the authority's own document and
recorded via [[Regulation Record]] with a full verification trail.

Jurisdiction notes: [[Qatar]] · [[Saudi Arabia]] · [[UAE]] · [[Lebanon]]

**Confidence keys used below**

- **VERIFIED** — the official page was fetched and confirmed to belong to that
  authority.
- **VERIFIED (indirect)** — the domain hosts that authority's own official
  documents, or is listed on another government portal, but the page itself
  could not be machine-read (bot blocking, JS-only shell, robots.txt).
- **UNVERIFIED** — could not be confirmed. Treat as a lead to check, not a fact.

**Standing caveat.** Authorities restructure, merge and rename. Verify the
authority name and portal at the start of every project before relying on this
index. Known recent changes are listed under §5.

---

# 1. QATAR

## 1.1 Core regulators

| Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|
| Planning & urban development | Ministry of Municipality (MoM) — وزارة البلدية, Urban Planning Dept | `https://www.mme.gov.qa/QatarMasterPlan/English/About-QNMP.aspx` (QNMP portal); `https://www.mm.gov.qa/` | Qatar National Master Plan (QNMP); Qatar National Development Framework (QNDF); Municipality Spatial Development Plans (MSDP); Centre Plans; Zoning Regulations | VERIFIED |
| Building permits | Ministry of Municipality — Technical Affairs Dept, Development & Building Permits Section (municipality level) | `https://hukoomi.gov.qa/en` (national e-gov catalogue) | Building / Demolition / Maintenance Permit service rules; Qatar Construction Specifications (QCS 2014) | VERIFIED (Hukoomi) |
| Fire & life safety / civil defence | General Directorate of Civil Defence (QCDD) — الإدارة العامة للدفاع المدني, Ministry of Interior | `https://portal.moi.gov.qa/wps/portal/MOIInternet/departmentcommittees/gacivildefence` | Civil Defence Technical Requirements; General Requirements of the Civil Defence; Maintenance and Periodic Inspection Schedule; Compatibility List of Dangerous Materials; Exhibitions and Events — Designing Guidelines; Exhibitions and Events — Inspection Guidelines; List of Accredited Laboratories for Safety Systems | VERIFIED |
| Roads & highways | Public Works Authority "Ashghal" — هيئة الأشغال العامة | `https://www.ashghal.gov.qa/en/Pages/default.aspx` | Qatar Highway Design Manual (QHDM); Qatar Traffic Manual (QTM); Qatar Roads Maintenance Manual (QRMM); Qatar Construction Specifications (QCS 2014); PWA Interim Advice Notes (IANs) | VERIFIED |
| Drainage & sewerage | Ashghal — Drainage Affairs / Roads & Drainage Network Design Dept | `https://www.ashghal.gov.qa/en/AboutUS/OrganisationChart/PWA/InfrastructureAffairs/Pages/DM-Roads-Draiange.aspx` | Qatar Sewerage & Drainage Design Manual (QSDDM); PWA IAN — Design Criteria for Drainage Structures | VERIFIED |
| Electricity & water | KAHRAMAA — Qatar General Electricity & Water Corporation | `https://www.km.qa/Pages/lawsRegulations.aspx` | Regulations for the Installation of Electrical Wiring, Electrical Equipment and Air Conditioning Equipment; Energy & Water Conservation Code; Law No. 10 of 2000; Law No. 4 of 2018; Law No. 26 of 2008 | VERIFIED |
| Telecom (in-building) | Communications Regulatory Authority (CRA) — هيئة تنظيم الاتصالات | `https://www.cra.gov.qa/en` | In-Building Telecommunications Infrastructure Standards (updated edition announced Sept 2025 — exact formal title not confirmed); Telecommunications Law No. 34 of 2006; Telecommunications By-Law | VERIFIED (title of the in-building standard: UNVERIFIED) |
| Telecom policy | Ministry of Communications and Information Technology (MCIT) | `https://www.mcit.gov.qa/en` | National ICT strategy documents (no building-level code issued directly) | VERIFIED |
| Environment | Ministry of Environment and Climate Change (MECC) | `https://www.mecc.gov.qa`; `https://envsustainability.mecc.gov.qa/en` | Environment Protection Law and Executive By-Law; EIA/environmental permitting regime; Qatar National Environment and Climate Change Strategy | VERIFIED (site); exact EIA guideline titles UNVERIFIED |
| National construction specification | Qatar Construction Specifications (QCS 2014) — issued by ministerial decision; applied by Ashghal, MoM, QCDD | Referenced in Ashghal IANs at `https://www.ashghal.gov.qa/ServicesLibrary/English/` | Qatar Construction Specifications 2014; PWA IAN — Amendments/Additions to QCS 2014 | VERIFIED (indirect) — the legacy MoM QCS landing page now returns 404 |

### Qetaifan Island North — approval chain (from primary documents)

Established from the QIN Planning & Design Guidelines Rev 2 (§1.6.3, §1.6.4) rather than
from web sources. This is a **master-developer-led** process — the municipal permit sits
inside it, not before it.

```text
QP (Concept) → QP + CAC (DC-1) → Services Review → CAC (DC-2)
                                → Al Daayen Municipality issues the Building Permit
```

Authorities the developer must additionally satisfy, as listed at DG §1.6.3, p.31 —
"Nothing in these Design Guidelines and Controls shall relieve the Developer of the
responsibility for … securing relevant approval(s), NOC(s) or permit(s) from, any
government agency":

> MMUP *(obsolete — now the Ministry of Municipality, see §5)* · Al Daayen Municipality ·
> Karahmaa *(KAHRAMAA)* · Ashgal *(Ashghal)* · Ooreedoo *(Ooredoo)* ·
> Marafeq (SNG, District Cooling, Vacuum Waste) · The Department of Civil Defense *(QCDD)* ·
> Ministry of the Environment *(now MECC)* · Civil Aviation · Ministry of the Interior (MoI) ·
> GORD

Written evidence of all such approvals must be submitted to CAC **in advance of
construction**. QCDD fire safety approval and KAHRAMAA electrical/water approval are
required as early as **DC-1**.

Extracted controls: see [[Qatar]] → Qetaifan Island North.

## 1.2 Accessibility — Qatar

> ⚠️ **No single named mandatory national built-environment accessibility code
> was confirmed.** In practice requirements are distributed across MoM planning
> guidelines, QCDD egress requirements and QCS. Confirm per project.

| Body | Nature | Portal | Confidence |
|---|---|---|---|
| Mada — Assistive Technology Center Qatar | Advisory / consultancy, **not a regulator** | `https://yusr.msdf.gov.qa/en/service-category/accessibility-2/ministry-of-municipality/` | VERIFIED |
| Accessible Qatar (Sasol + Ministry of Social Development and Family) | **Voluntary** rating/awareness initiative | `https://www.accessibleqatar.com/about-us/` | VERIFIED |

## 1.3 Sustainability & master developers — Qatar

| Body | Nature | Portal | Key document titles | Confidence |
|---|---|---|---|---|
| GORD — Gulf Organisation for Research & Development | Non-governmental research org; **contractually** mandated on many projects (e.g. Lusail) | `https://gsas.gord.qa/` | Global Sustainability Assessment System (GSAS) — Design & Build, Construction Management, Operations | VERIFIED |
| Lusail — LREDC / Lusail City Management ("LCAC") | Master developer; single point of contact for permit approvals in Lusail, coordinating Al Daayen Municipality, Civil Defence and KAHRAMAA | `https://www.lusail.com/services/lcac/core-business/` | Lusail General Guidelines for Developers; Lusail Building Permit Related Forms; Marafeq Guidelines; Storm Water Guidelines for Lusail Developers; Synopsis of the District Cooling and Gas Supply Systems | VERIFIED (LCAC acronym expansion not stated on source pages) |
| **Lusail City Administration Complex (CAC)** — a department within LREDC | **The development control authority for Lusail City districts.** Issues Concept Design, DC-1, Services Review and DC-2 approvals; administers the building permit application and fees; has the power to interpret the Design Guidelines, and its decision "shall be final and binding" | — (no standalone portal confirmed) | Lusail Planning & Design Guidelines, Sections 1 & 2; Plot Building Regulation Sheets | **VERIFIED from primary document** — QIN Planning & Design Guidelines Rev 2, §1.6.3, p.31 |
| **Qetaifan Projects (QP)** | **Master Developer of Qetaifan Island North District**, and development control authority for that district in coordination with CAC. Runs the Architectural Review Committee and Concept Design review | — (no portal verified; web checking paused at user request) | Qetaifan Island North District — Planning & Design Guidelines, Residential & Mixed-Use Plots (REV 2, May 2023); Front Boundary Wall — VL-01 + VL-02 Unification of Boundary Wall Design (REV 00, Nov 2025); Plot Building Regulation Sheets | **VERIFIED from primary document** — DG Rev 2 §1.6.3, p.31 |
| **Al Daayen Municipality** | **Issues the building permit** for developments that have received CAC approval; permit administered and received via CAC | — (see Ministry of Municipality, §1.1) | Building permit | **VERIFIED from primary document** — DG Rev 2 §1.6.3–§1.6.4 |
| Marafeq | Lusail utility provider — **SNG (gas), District Cooling, Vacuum Waste** collection | — | Marafeq Guidelines | VERIFIED from primary document (DG Rev 2 §1.6.3) |
| Qatar Free Zones Authority (QFZ/QFZA) | Grants building permits inside free zones | `https://qfz.gov.qa/` | Building Permits and Planning Regulations; Licensing Regulations | VERIFIED |
| Manateq — Economic Zones Company | Developer of special economic zones | `https://manateq.qa/about-us/` | No public building-permit regulation titles confirmed | VERIFIED (site); documents UNVERIFIED |
| QatarEnergy — Industrial Cities Directorate (Ras Laffan, Mesaieed, Dukhan) | Industrial city permitting | `https://www.qatarenergy.qa/en/Whatwedo/IndustrialCities/Pages/default.aspx` | Land/facility/service permit and gate-pass procedures; Engineering & Construction Procedures (VI-ECP series) | VERIFIED (portal); document titles UNVERIFIED |
| Msheireb Properties | Master developer (Qatar Foundation subsidiary) | `https://www.msheirebproperties.com/` (JS shell) | No public development-control document titles confirmed | UNVERIFIED |
| Qatar Rail | Rail corridor protection / adjacent-development NOC | — | — | **UNVERIFIED** — no official URL or document title confirmed, though the NOC requirement is widely referenced in practice |
| Energy City Qatar | — | domain did not resolve | — | **Treat as dormant/defunct — not a regulator.** Plots in that area now fall under Lusail/LREDC governance |

---

# 2. SAUDI ARABIA

| Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|
| Planning & urban development; municipality/amanah system | **Ministry of Municipalities and Housing (MOMAH)** — وزارة البلديات والإسكان (**renamed from MOMRAH**) | `https://momah.gov.sa/en` | Urban planning & sustainable urban development standards; municipal licensing regulations | VERIFIED (portal + renaming); document titles UNVERIFIED |
| Building permits (e-permitting) | **Balady Platform** — منصة بلدي (operated by MOMAH) | `https://balady.gov.sa/en` | Building Permit; Fencing Permit; Renovation Permit; Expansion Permit; Building Demolition Permit; Occupancy Certificate | VERIFIED |
| Building code | **Saudi Building Code National Committee (SBCNC)** | `https://sbc.gov.sa` | Saudi Building Code (SBC) series incl. SBC 201 General Building Code & Commentary; The Implementing Regulations of the Saudi Building Code; Regulations for Classification of Saudi Building Code Violations; General Requirements Regulations for Appointing Inspectors for SBC Works | VERIFIED |
| Fire & life safety / civil defence | **General Directorate of Civil Defense** — المديرية العامة للدفاع المدني (Ministry of Interior) | `https://998.gov.sa` | Civil Defense Law; Private Fire and Rescue Teams Regulation; Requirements for Protection from Fire (safety instruction series, by occupancy) | VERIFIED |
| Roads | **Roads General Authority (RGA)** — الهيئة العامة للطرق | `https://rga.gov.sa` (code library `https://shc.rga.gov.sa`) | Saudi Highway Code (SHC) — volume series (planning, geometric design, bridges & tunnels, construction, maintenance & asset management, traffic engineering & road safety, environmental aspects, autonomous vehicle requirements) | VERIFIED (main portal); code subdomain UNVERIFIED |
| Electricity | **Saudi Electricity Regulatory Authority (SERA)** — **renamed from WERA** | `https://www.sera.gov.sa/en/` | The Saudi Arabian Grid Code; Electricity Service Guide; Regulatory Framework for Renewable Energy Generation | VERIFIED (indirect — robots.txt blocks direct fetch) |
| Water & drainage/sewerage (regulator) | **Saudi Water Authority (SWA)** — الهيئة السعودية للمياه (MEWA) | `https://www.swa.gov.sa/en/` | Water Law and implementing instruments; Rules for Connecting Water Networks to New Developments | UNVERIFIED (403 on fetch) |
| Water & sewerage (service provider) | **National Water Company (NWC)** | `https://www.nwc.com.sa/EN/` | Service connection guidelines / customer service manuals | UNVERIFIED |
| Environment (compliance) | **National Center for Environmental Compliance (NCEC)** | `https://ncec.gov.sa` (e-permits: `ecompliance.ncec.gov.sa`) | Environmental Permit (facilities) regulations; environmental compliance requirements | UNVERIFIED |
| Environment (parent ministry) | **Ministry of Environment, Water and Agriculture (MEWA)** | `https://www.mewa.gov.sa/en/` | Environmental Law and implementing regulations | UNVERIFIED |
| Telecom (in-building) | **Communications, Space & Technology Commission (CST)** | `https://www.cst.gov.sa/en` | Regulations for Establishing and Providing Telecommunications Services in Real Estate (issued 8 July 2025); Telecom Service Requirements for Buildings (CST-GUIDE-101.3-24) | VERIFIED |
| Engineering practice licensing | **Saudi Council of Engineers (SCE)** — الهيئة السعودية للمهندسين | `https://www.saudieng.sa/English/pages/default.aspx` | The Practice of Engineering Professions Regulating Law; Implementing Regulations; Professional Accreditation Guide for Engineering Categories | VERIFIED (indirect) |
| Special zones (framework) | **Economic Cities and Special Zones Authority (ECZA)** | `https://ecza.gov.sa/en` | Special Economic Zones regulatory framework documents | UNVERIFIED |

## 2.1 Accessibility — Saudi Arabia (fragmented)

> ⚠️ **No single national universal-accessibility regulator.** Which instrument
> binds depends on jurisdiction — confirm per project.

| Body | Role | Portal | Key document titles | Confidence |
|---|---|---|---|---|
| SBCNC | Accessibility provisions within the Saudi Building Code | `https://sbc.gov.sa` | SBC series | VERIFIED |
| **Royal Commission for Riyadh City (RCRC)** | Riyadh only — binding city code | `https://www.rcrc.gov.sa/en/` | Accessibility Code for Riyadh City; Design and Architectural Guidelines (Applied Reference Guide); Urban Code for Wadi Hanifah | VERIFIED (indirect) |
| King Salman Center for Disability Research (KSCDR) | Technical guidance, **non-statutory** (`.org.sa`, not a regulator) | `https://kscdr.org.sa/en/universal-accessibility-guidelines` | Universal Accessibility Guidelines; Universal Accessibility: Built Environment Guidelines; Inclusive Parks Guide; Web Accessibility Guide | UNVERIFIED |
| Authority for the Care of Persons with Disabilities (APD) | Policy / rights | `https://apd.gov.sa/en` | Local Legislations library | UNVERIFIED |
| MHRSD — Mowaamah | **Workplace certification, not a building code** | `https://www.hrsd.gov.sa/en` | Mowaamah certificate issuance criteria | UNVERIFIED |

## 2.2 Giga-projects & master developers — Saudi Arabia

> ⚠️ **Most giga-project design controls are not public.** Obtain them from the
> developer directly under NDA. Do not rely on third-party copies circulating
> online — edition control cannot be established.

| Developer | Portal | Key document titles | Confidence |
|---|---|---|---|
| **Diriyah Gate Development Authority (DGDA)** — government authority holding planning/design-compliance powers (distinct from Diriyah Company, the PIF development company) | `https://www.dgda.gov.sa/en` | Wadi Hanifah Form-Based Code; FBC Submission Guidelines; Wadi Hanifah Form-Based Code Design Compliance Declaration; Contractor & Consultant Appointment Form; User Manual | VERIFIED — publicly operates a design-compliance certification process |
| NEOM | `https://www.neom.com` | NEOM Engineering Norms (NEN) series — List of Technical Codes and Standards; Technical Guidance Documents (TGD); Coastal Development Technical Guideline | Portal VERIFIED; **document series UNVERIFIED** — titles seen only on third-party hosts, not on neom.com |
| Red Sea Global (RSG) | `https://www.redseaglobal.com/en/` | Internal design/sustainability standards (not published) | Portal VERIFIED; design code UNVERIFIED |
| Red Sea Authority (coastal regulator) | `https://redsea.gov.sa/en` | Requirements and Conditions for Red Sea Beach Operators (reported) | UNVERIFIED |
| Qiddiya Investment Company | `https://qiddiya.com` | Not public | Portal VERIFIED; design controls UNVERIFIED |
| ROSHN Group | `https://www.roshn.sa` | Not public ("Human by Design" is a brand framework, not a code) | Portal VERIFIED; design controls UNVERIFIED |
| King Abdullah Financial District (KAFD) | `https://www.kafd.sa/` | KAFD Design Manual / design guidelines (historic; current status not confirmed) | UNVERIFIED |

---

# 3. UNITED ARAB EMIRATES

> The UAE regulates **emirate by emirate.** Always establish the emirate first,
> then the free zone or master development, before applying any requirement.

## 3.1 Federal

| Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|
| Fire & life safety | Ministry of Interior — General Directorate of Civil Defence | `https://moi.gov.ae/` | UAE Fire and Life Safety Code of Practice; UAE Ministerial Resolution No. (505) of 2012 | VERIFIED (indirect) |
| Telecom infrastructure | Telecommunications and Digital Government Regulatory Authority (TDRA) | `https://tdra.gov.ae/en/initiatives/telecommunications-infrastructure-guidelines` | Telecommunications Networks Specifications Manual for Buildings | VERIFIED |
| Green building / energy | Ministry of Energy and Infrastructure (MoEI) | `https://www.moei.gov.ae/` | National Green Building Regulation; National Green Certificates Program; National Demand-side Management Program | VERIFIED |
| Authority directory | Official Portal of the UAE Government | `https://u.ae/en/information-and-services/justice-safety-and-the-law/building-safety` | Directory of emirate municipalities & codes | VERIFIED |
| Electricity & water regulation | Federal Regulatory Bureau for Electricity and Water (under MoEI) | no standalone URL confirmed | — | UNVERIFIED |

## 3.2 Dubai

| Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|
| Planning, building permits, building code | Dubai Municipality | `https://www.dm.gov.ae/` | **Dubai Building Code (2021 Edition)**; Planning Standards' Guide | VERIFIED |
| Accessibility / universal design | Dubai Municipality — Building Permits Dept | `https://www.dm.gov.ae/municipality-business/dubai-universal-design-code/` | Dubai Building Code Guide – Accessibility; Accessibility Guideline for Villas; Dubai Universal Design Code | VERIFIED |
| Green building | Dubai Municipality | `https://www.dm.gov.ae/municipality-business/al-safat-dubai-green-building-system/` | Al Sa'fat – Dubai Green Building System (2nd edition, January 2023); Dubai Green Building Regulations and Specifications (superseded) | VERIFIED |
| Drainage / sewerage / stormwater | Dubai Municipality | `https://www.dm.gov.ae/`; `https://drainage.dm.gov.ae/` | DM Sewerage Guidelines; DM Stormwater Guidelines; Local Order No. (8) of 2002 | VERIFIED (main); subdomain UNVERIFIED |
| Legislation reference | Dubai Legislation Portal (Legal Affairs Dept) | `https://dlp.dubai.gov.ae/` | Decree No. (45) of 2021 Concerning the Dubai Building Code; **Decree No. (19) of 2025 Concerning Safety in Construction Work**; **Law No. (7) of 2025 (contracting sector)** | UNVERIFIED (documents indexed on the domain) |
| Fire & life safety | General Command of Dubai Civil Defence (DCD) | `https://www.dcd.gov.ae/` | UAE Fire and Life Safety Code of Practice | VERIFIED |
| Roads & transport | Roads and Transport Authority (RTA) | `https://www.rta.ae/` | Right-of-way permits; rail right-of-way NOCs; road closure permits | VERIFIED |
| Electricity & water | Dubai Electricity and Water Authority (DEWA) | `https://www.dewa.gov.ae/` | DEWA Electrical Installation Regulations; DEWA circulars and regulations; DEWA Green Building guidance | VERIFIED |
| Real estate development regulation | Dubai Land Department incl. RERA | `https://dubailand.gov.ae/en/` | Project registration, escrow and developer licensing regulations | VERIFIED |
| Free-zone planning & building (TECOM / media & internet zones) | Dubai Development Authority (DDA) | `https://www.dda.gov.ae/` | DDA Codes and Guidelines; DDA Laws and Regulations; DDA Circulars and Announcements; Fit-out NOC Matrix; Circular no. 400 | VERIFIED |
| Free-zone / master-development permits (Palm Jumeirah, Jafza, Dubai Waterfront, DWC) | Ports, Customs and Free Zone Corporation (PCFC) — Dept of Planning & Development ("**Trakhees**"), Civil Engineering Dept & EHS | `https://pcfc.ae/en/Pages/aboutus-trakhees.aspx`; `https://trakhees.ae/` | Trakhees Rules and Regulations (CED / EHS) | PCFC VERIFIED; trakhees.ae bot-blocked |
| Free zone (logistics) | Jebel Ali Free Zone (Jafza) | `https://www.jafza.ae/` | — (approvals commonly routed via Trakhees/PCFC) | Domain VERIFIED; routing UNVERIFIED |
| Financial free zone | Dubai International Financial Centre (DIFC) | `https://difc.ae/` | DIFC laws/regulations; third-party building NOC process | Domain VERIFIED; building-code titles UNVERIFIED |
| Free zone (JLT) | Dubai Multi Commodities Centre (DMCC) | `https://www.dmcc.ae/` | — | Domain VERIFIED; fit-out approval function UNVERIFIED |
| Master developer | Emaar Properties PJSC | `https://www.emaar.com/en` | Developer NOC / community design guidelines (not published) | Domain VERIFIED; titles UNVERIFIED |
| Master developer | Nakheel (**merged with Meydan under Dubai Holding**) | no live official URL confirmed | Developer NOC / community regulations | UNVERIFIED |

> ⚠️ **Dubai Municipality permit platform naming is UNVERIFIED.** Third-party
> sources widely cite a "Building Permit System (BPS)" and "Rasid", but neither
> name appears on dm.gov.ae's own planning-and-construction pages. Confirm the
> current platform name with DM directly before citing it.

## 3.3 Abu Dhabi

| Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|
| Planning, urban development, building permits | Department of Municipalities and Transport (DMT) | `https://www.dmt.gov.ae/en/` | **Abu Dhabi Capital Development Code**; Abu Dhabi Architectural Façade Design Manual; Abu Dhabi Storefront Design Manual; Abu Dhabi Public Toilets Planning and Design Manual; Concept Master Plan / Detailed Master Plan submission templates | VERIFIED |
| Municipal permit delivery | Abu Dhabi City Municipality (ADM); Al Ain City Municipality; Al Dhafra Region Municipality — **all under DMT, not independent** | `https://www.dmt.gov.ae/en/ADM/`; `/en/aam`; `/en/drm` | Specific Requirements for Technical Approval (ADM e-library) | VERIFIED (indirect) |
| Government service portal | TAMM | `https://www.tamm.abudhabi/` | — (delivery channel for DMT permit services) | Domain resolves; content UNVERIFIED |
| Green building | DMT — Estidama programme | `https://www.dmt.gov.ae/` (DMT E-Library) | The Pearl Rating System for Estidama (Building, Villa, Community); Public Realm Rating System; Sahel Public Realm Rating System Handbook | VERIFIED |
| Building code (legacy series) | Abu Dhabi International Building Codes (ADIBC) — issued by the former Department of Municipal Affairs | legacy: `https://dmat.abudhabi.ae/en/About/Pages/buildingcode.aspx` | Abu Dhabi International Building Codes (Building, Fire, Mechanical, Plumbing, Electrical, Energy Conservation, Green, Property Maintenance series) | **UNVERIFIED — whether ADIBC remains operative or has been superseded by the Abu Dhabi Capital Development Code could not be confirmed. Confirm with DMT before relying on either.** |
| Fire & life safety | Abu Dhabi Civil Defence Authority (ADCDA) | `https://www.adcda.gov.ae/en` | UAE Fire and Life Safety Code of Practice; Certificate of Compliance with Preventive Safety Requirements; Distributor Licence in the Field of Preventive Fire Safety; Licence for a Fire Prevention Safety Equipment Factory | VERIFIED |
| Roads & transport | Integrated Transport Centre (ITC), operating as **Abu Dhabi Mobility** | `https://admobility.gov.ae/` | Policies and Procedures | VERIFIED |
| Electricity, water, wastewater, district cooling (regulator) | Abu Dhabi Department of Energy (DoE) | `https://www.doe.gov.ae/` | Licensing and compliance regulations for electricity, water, wastewater, district cooling, petroleum products | VERIFIED |
| Electricity & water (distributor) | **TAQA Distribution** (merged ADDC + AADC) | `https://taqadistribution.com/`; `https://www.addc.ae/` | Connection / load application requirements | UNVERIFIED (listed on u.ae) |
| Sewerage / wastewater | Abu Dhabi Sustainable Water Solutions Company (SWS) | no standalone URL confirmed | — | UNVERIFIED |
| Environment | Environment Agency – Abu Dhabi (EAD) | `https://www.ead.gov.ae/en` | Environmental laws and policies; No Objection Certificate services | VERIFIED |
| Construction products conformity | Abu Dhabi Quality and Conformity Council (ADQCC / QCC) | `https://www.qcc.gov.ae/`; `https://qcc.abudhabi.ae/` | Trustmark conformity scheme; product and personnel conformity certificates; Specific Requirements for Technical Approval | VERIFIED |
| Financial free zone | Abu Dhabi Global Market (ADGM) | `https://www.adgm.com/` | — | Domain VERIFIED; building-approval function UNVERIFIED |
| Free zone / sustainable district | Masdar City Free Zone | `https://masdarcity.ae/` | References Estidama; no proprietary code confirmed | Domain VERIFIED; own-code issuance UNVERIFIED |
| Master developer | Aldar Properties PJSC | `https://www.aldar.com/` | Not published | Domain VERIFIED; titles UNVERIFIED |

## 3.4 Northern Emirates

| Emirate | Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|---|
| Sharjah | Building permits, municipal & environmental permits | Sharjah Municipality | `https://portal.shjmun.gov.ae/en` | Building permit and environmental permit services | VERIFIED |
| Sharjah | Town planning & survey | Sharjah Dept of Town Planning and Survey (SDTPS) | `https://www.sdtps.gov.ae/` | Planning statements, plot plans, planning approvals | VERIFIED |
| Sharjah | Fire & life safety | Sharjah Civil Defence Authority | `http://feelsafewithshjcd.ae/` | UAE Fire and Life Safety Code of Practice | **UNVERIFIED — non-.gov.ae domain, could not be loaded. Route Sharjah fire-safety queries via Sharjah Municipality.** |
| Sharjah | Electricity, water & gas | SEWA | `https://www.sewa.gov.ae/` | Connection/NOC requirements | VERIFIED (indirect) |
| Sharjah | Environment | Environment and Protected Areas Authority – Sharjah (EPAA) | `https://epaashj.ae/` | Environmental legislations and decisions | UNVERIFIED |
| Ajman | Planning, permits, roads works, environment | Ajman Municipality and Planning Department | `https://www.am.gov.ae/en/` | Building permit / addition permit / roads works / environmental compliance regulations | VERIFIED (indirect) |
| Ajman | Service delivery | Department of Digital Ajman | `https://www.ajman.ae/en/servicecatalog/service_categories/municipality-planning-department` | Building Permit Request; Permit to Construct an Addition to an Existing Building; roads works and underground pipe permits | VERIFIED |
| Ras Al Khaimah | Planning, permits, transport, public health | RAK Municipality Department | `https://mun.rak.ae/` | Building Conditions and Specifications Regulation (Architectural Requirements); **Barjeel Green Building Regulations**; Buildings Administration regulations; Real Estate Regulatory Administration guidelines; Transportation and Traffic Dept regulations; Energy Efficiency and Renewables Administration regulations; Public Health Administration regulations | VERIFIED |
| Fujairah | Planning & building permits | Fujairah Municipality | `https://www.fujmun.gov.ae/` | Building permit regulations | VERIFIED (indirect) |
| Umm Al Quwain | Planning & building permits | Umm Al Quwain Municipality | `https://www.uaq.ae/en/adfservicecatalog.html` | Building permit regulations | VERIFIED (indirect) |
| Ajman / RAK / Fujairah / UAQ | Electricity & water | **Etihad Water and Electricity (EtihadWE, formerly FEWA)** | `https://etihadwe.ae/` | Connection requirements | VERIFIED (indirect) |

---

# 4. LEBANON

> ⚠️ **Lebanon has no unified national building code.** The regulatory stack is
> Building Law No. 646 (2004) + Implementing Decree No. 15874 (2005) + Public
> Safety Decree No. 7964 (2012), supplemented piecemeal by LIBNOR standards.
> Structural/seismic design in practice references international codes — that
> practice is **not itself a statutory instrument** and must not be cited as one.

## 4.1 Authorities

| Discipline | Authority | Official portal | Key document titles | Confidence |
|---|---|---|---|---|
| Planning & urban development | Directorate General of Urban Planning (DGU) — المديرية العامة للتنظيم المدني / Direction Générale de l'Urbanisme, MoPWT | `https://dgu.gov.lb/` | Urban Planning Law (Legislative Decree No. 148, 1983); Building Law No. 646 (2004); Implementing Decree No. 15874 (2005) | VERIFIED — **the most reliable and current Lebanese AEC portal; best single entry point** |
| Strategic planning / appeals | Higher Council for Urban Planning — المجلس الأعلى للتنظيم المدني | `https://www.dgu.gov.lb/HC.html`; `https://www.dgu.gov.lb/high_council.html` | Higher Council decisions/circulars (rolling) | VERIFIED — no standalone domain |
| Parent ministry | Ministry of Public Works and Transport (MoPWT) — contains DG Urban Planning, DG Roads and Buildings, DG Land & Maritime Transport, DG Civil Aviation | `mopw.gov.lb` — **cert hostname mismatch / HTTP 403; content not retrievable** | Legal-texts index | Structure VERIFIED; site UNVERIFIED |
| Building permits — issuing authority | **Municipalities** (البلديات) under the DG of Local Administrations and Councils; DGU issues permits where no municipality exists | `https://moim.gov.lb/en/` (Ministry of Interior and Municipalities) | Municipalities Law; Building Law No. 646 (2004) | VERIFIED — legacy `interior.gov.lb` no longer resolves |
| Building permits — Beirut | Municipality of Beirut — بلدية بيروت | **No official government portal located.** `beirut.gov.lb` did not resolve; only social-media presence found | — | **UNVERIFIED — significant practical gap. Engagement is in person or via the Governor of Beirut / MoIM.** |
| Permit review / technical audit (Beirut, Mount Lebanon, Bekaa, South) | Order of Engineers and Architects in Beirut (OEA Beirut) — نقابة المهندسين في بيروت | `https://www.oea.org.lb` | Lebanese Standards implementation / technical-audit guidance; lift & escalator safety standards series | VERIFIED (domain live; root blocks automated fetch) |
| Permit review / technical audit (North Lebanon) | Order of Engineers and Architects in Tripoli | `https://oea-tripoli.org.lb/` | Technical Office monthly reports and publications | VERIFIED |
| Fire & civil defence | General Directorate of Lebanese Civil Defence (MoIM) | **No official portal confirmed** | Public Safety Decree No. 7964 (2012) — applied through permitting | **UNVERIFIED (portal)** — role exercised through municipal/DGU referral, not an independent published process |
| Roads & buildings | DG of Roads and Buildings (MoPWT) | No separate portal; sits under mopw.gov.lb | — | UNVERIFIED |
| Major infrastructure delivery | Council for Development and Reconstruction (CDR) — مجلس الإنماء والإعمار | `https://www.cdr.gov.lb/` | Strategic Environmental and Social Assessment reports | VERIFIED |
| Electricity | Électricité du Liban (EDL) — كهرباء لبنان | `edl.gov.lb` — **invalid/untrusted TLS certificate; liveness not confirmable** | — | UNVERIFIED |
| Energy/water parent ministry | Ministry of Energy and Water | `https://www.energyandwater.gov.lb/` | Laws, decrees, decisions and circulars index | VERIFIED |
| Water & sewerage — Beirut & Mount Lebanon | Beirut and Mount Lebanon Water Establishment (BMLWE/EBML) | `https://ebml.gov.lb/?lang=en` | Water Sector Organisation Law No. 221 (2000) | VERIFIED |
| Water & sewerage — North | North Lebanon Water Establishment (NLWE) | `https://eeln.gov.lb/en/home/` | Law No. 221 (2000) | VERIFIED |
| Water & sewerage — South | South Lebanon Water Establishment (SLWE) | `https://www.slwe.gov.lb/` | Law No. 221 (2000) | VERIFIED |
| Water & sewerage — Bekaa | Bekaa Water Establishment (BWE) | `bwe.gov.lb` — **TLS handshake failure** | Law No. 221 (2000) | UNVERIFIED |
| Telecom | OGERO — أوجيرو (Ministry of Telecommunications) | `https://www.ogero.gov.lb/` | — | VERIFIED |
| Environment | Ministry of Environment | `https://www.moe.gov.lb/` | Administrative procedures; laws, decrees, decisions and circulars index | VERIFIED — EIA framework not surfaced on homepage |
| Heritage / antiquities | Directorate General of Antiquities (DGA), Ministry of Culture | **No standalone portal found**; parent `culture.gov.lb` redirects HTTPS→HTTP, content not retrievable | Antiquities Law (Resolution No. 166, 1933) | UNVERIFIED |
| Standards / codes of practice | LIBNOR — Lebanese Standards Institution (Ministry of Industry) | `https://libnor.gov.lb/` | Lebanese Standards (NL); codes of practice for professional and structural work; earthquake-prevention standards for new and existing buildings | VERIFIED |
| Legislation source of record | Lebanese Parliament | `https://www.lp.gov.lb/` | Law No. 646 (2004); Decree No. 15874 (2005) records | VERIFIED |

## 4.2 Principal legal framework — titles and dates only

| Document | Date | Status |
|---|---|---|
| **Building Law No. 646** (قانون البناء) — principal Construction/Building Law; amended Legislative Decree No. 148 of 1983 | Enacted 11/12/2004 (DGU text carries 16/12/2004) | VERIFIED |
| **Implementing Decree of the Building Law, No. 15874** — includes the "Fifth Façade" provisions | 12/12/2005 | VERIFIED |
| **Urban Planning Law, Legislative Decree No. 148** | 16/09/1983 | VERIFIED |
| **Public Safety Decree No. 7964** — de facto national building-safety framework (fire, structural, seismic, MEP) | 07/04/2012 (Official Gazette No. 17, 19/04/2012) | VERIFIED |
| **Water Sector Organisation Law No. 221** — constitutes the Regional Water Establishments | 2000 (sources give 26/05/2000 and 29/05/2000 — **date variance unresolved**) | VERIFIED (title) |
| **Reconstruction Law No. 22** — post-conflict reconstruction registries at DGU offices | 11/07/2025 (Official Gazette No. 37, 17/07/2025) | VERIFIED |
| Antiquities Law (Resolution No. 166) | 1933 | UNVERIFIED |
| Lebanese Standards (NL) issued by LIBNOR | rolling | VERIFIED (titles only) |

## 4.3 Institutional caveat

Post-2019 financial collapse, the 2020 Beirut port explosion and the 2023–24
conflict have degraded staffing and digital infrastructure across Lebanese
agencies. Several bodies operate through ministry-level channels rather than
their own directorates' portals. Municipal capacity varies sharply, and the
May 2025 municipal elections reconstituted many councils — **contact points and
delegated signatories may have changed.** Confirm current practice locally at
the start of every Lebanese project.

---


# 5. JORDAN

> [!tip] Jordan is different from the Gulf jurisdictions in this directory
> Development control here is **national and codified in one instrument**, not distributed across
> master developers and emirate-level codes. The numeric controls live in
> **[[Jordan Building Regulation 2022]]**, which this vault holds in full — so for Jordan the
> "routing index only" rule is relaxed: the requirements themselves are recorded, with article and
> page citations, in the linked records.

## 5.1 Authorities

| Discipline | Authority | Arabic | Role | Confidence |
|---|---|---|---|---|
| Planning — national | **Higher Planning Council** | مجلس التنظيم الأعلى | "The Council". Reserved matters: coverage relief (Art. 16(g)), residential suburb projects, investment projects outside planning areas | **VERIFIED from primary document** |
| Planning — administration | **Central Department of Town, Village and Building Planning** | دائرة تنظيم المدن والقرى والأبنية المركزية | "The Department", constituted under the Law | VERIFIED from primary document |
| Licensing | **Competent planning committee** | اللجنة المختصة | Local, district (لوائية), joint district or joint local committee. **Day-to-day licensing authority** | VERIFIED from primary document |
| Municipal | Municipalities | البلديات | Licensing, fees, permissions for home-based professions | VERIFIED from primary document |
| Professional | **Jordan Engineers Association** | نقابة المهندسين الأردنيين | Certifies engineering plans — required by the 2025 amendment | VERIFIED from primary document |
| Ministerial | Minister (per the Law) | الوزير | Issues instructions, e.g. flagpole specifications under Art. 41(ج)(9) | VERIFIED from primary document |

*(Portal URLs not yet verified — no web checking was performed for Jordan. Sourced entirely from
the Official Gazette scans supplied by the client.)*

## 5.2 Instruments

| Instrument | Arabic | Date | Status |
|---|---|---|---|
| Town, Village and Building Planning Law | قانون تنظيم المدن والقرى والأبنية | — | Enabling law. **Number and year UNVERIFIED** (OCR garbled; believed Law No. 79 of 1966 as amended) |
| **Regulation No. (1) of 2022** — Buildings and Town & Village Planning Regulation | نظام الأبنية وتنظيم المدن والقرى | 2022 | **CURRENT** — the principal development-control instrument, 49 pages |
| **Regulation No. (12) of 2025** — amending regulation | نظام معدل لنظام الأبنية وتنظيم المدن والقرى | Signed **29/1/2025**, Gazette pp. 835–837 | **IN FORCE** — read as **one regulation** with the 2022 |
| Local zoning decisions | أحكام التنظيم | varies | **Override** the national table where structural or detailed plans impose restrictions or grant facilities |

## 5.3 Road-width thresholds — the Jordanian gating tests

| Width | Effect |
|---|---|
| **< 8 m** | Road not counted in the height-datum average (Art. 15(a)(1)) |
| **≥ 12 m** | Balconies permitted in the front setback (Art. 33) |
| **≥ 12 m** | **Minimum serving street for a project**, renewable energy excepted (**Art. 10(و), added 2025**) |
| **≥ 14 m** | Additional floor of up to 4 m may be licensed (Art. 16(f)) |
| **≥ 20 m** | Required to access the high-building table, height bonuses and the 60 m provisions (Art. 16(e)) |

## 5.4 Records held

[[Jordan]] · [[Jordan Building Regulation 2022]] · [[Jordan Amendment Regulation 12 of 2025]] ·
[[Jordan Subdivision Minimums (Article 11)]] · [[Jordan Development Control Table (Article 16)]] ·
[[Jordan Building Height Measurement (Article 15)]] · [[Jordan Parking Requirements (Article 36)]] ·
[[Jordan Setbacks, Fences and Ancillary Buildings]] · [[Jordan Balconies and Entrance Canopies]]

---

# 6. RECENT RENAMES, MERGERS & SUPERSESSIONS

Treat any document or reference using the **old** name as potentially
superseded, and check its edition.

| Jurisdiction | Change | Effect |
|---|---|---|
| Qatar | Ministry of Municipality and Environment (**MME**) split by Emiri Resolution No. 57 of 2021 into the **Ministry of Municipality** and the **Ministry of Environment and Climate Change** | "MME" is obsolete as an authority name. **But note:** the legacy `mme.gov.qa` domain is still live and still hosts MoM technical content (the QNMP portal), while the current `mm.gov.qa` serves a JS-only shell. Some deep legacy pages (e.g. the QCS 2014 landing page) now return 404 |
| Qatar | Nov 2024 cabinet reshuffle | Changed ministers only, not portfolios |
| Saudi Arabia | **MOMRAH → MOMAH** (Ministry of Municipal and Rural Affairs and Housing → Ministry of Municipalities and Housing), by royal order 1446 AH; housing sector absorbed 1442 AH | Canonical domains are now `momah.gov.sa` and `balady.gov.sa`. Legacy `balady.momra.gov.sa` links still surface |
| Saudi Arabia | **WERA → SERA** (Water and Electricity Regulatory Authority → Saudi Electricity Regulatory Authority); water regulation split out to the **Saudi Water Authority (SWA)** | Any pre-2024 "WERA" reference is superseded |
| UAE — Dubai | **Law No. (7) of 2025** — unified emirate-wide contractor/subcontractor registration and classification regime, **Dubai Municipality** as primary regulator; creates a Contracting Activities Regulation and Development Committee. Reported effective from 2026 with a transitional grace period | **Largest recent structural change to Dubai AEC regulation.** Verify current transitional status |
| UAE — Dubai | **Decree No. (19) of 2025 Concerning Safety in Construction Work** | Title confirmed on the official legislation portal; contents not reviewed |
| UAE — Dubai | Nakheel and Meydan **merged under Dubai Holding** | No live official Nakheel developer-approvals URL confirmed |
| UAE — Abu Dhabi | **ITC now operates as "Abu Dhabi Mobility"** (legal entity name ITC retained) | Portal: `admobility.gov.ae` |
| UAE — Abu Dhabi | **ADDC + AADC merged into TAQA Distribution** | Legacy `addc.ae` still resolves per u.ae |
| UAE — Abu Dhabi | Former Department of Municipal Affairs / DMAT → **Department of Municipalities and Transport (DMT)**; ADM, Al Ain and Al Dhafra municipalities absorbed as DMT sub-departments | **Open question: does ADIBC remain operative, or is it superseded by the Abu Dhabi Capital Development Code? Unresolved — confirm with DMT.** |
| Lebanon | `interior.gov.lb` superseded by `moim.gov.lb` | Use `moim.gov.lb` |
| **Jordan** | **Art. 52(أ) settlement window LAPSED 31/12/2025** | The route to license existing unlicensed buildings erected 1/1/2017–31/12/2024 closed. **No extending instrument verified.** See [[Jordan Amendment Regulation 12 of 2025]] |

---

# 7. KNOWN GAPS — DO NOT FILL THESE FROM MEMORY

These were investigated and could **not** be confirmed. Each is a question for
the authority, not a gap to close by inference.

1. **Qatar — accessibility.** No named mandatory national built-environment
   accessibility code confirmed.
2. **Qatar — Qatar Rail.** Corridor-protection / adjacent-development NOC
   requirements are referenced in practice; no official URL or document title
   confirmed.
3. **Qatar — CRA in-building telecom standard.** The updated standard exists
   (announced Sept 2025) but its exact formal title is unconfirmed.
4. **Qatar — Manateq vs QFZA.** Both list Ras Bufontas and Umm Alhoul. The
   current split of permitting authority between them is unconfirmed —
   **verify per plot.**
5. **Saudi Arabia — accessibility.** Fragmented across SBC, RCRC (Riyadh only),
   KSCDR guidance, Mowaamah and APD. Which instrument binds depends on
   jurisdiction.
6. **Saudi Arabia — giga-project design codes.** NEOM, Qiddiya, ROSHN, RSG and
   KAFD do not publish theirs. Obtain from the developer; do not rely on
   third-party copies.
7. **Saudi Arabia — drainage/sewerage.** No standalone authority: regulation
   with SWA, connection with NWC or the regional utility, in-building design
   with the SBC.
8. **UAE — Abu Dhabi building code.** ADIBC vs Abu Dhabi Capital Development
   Code operative status unresolved.
9. **UAE — Dubai permit platform name.** "BPS" / "Rasid" appear only in
   third-party sources.
10. **UAE — free-zone building approvals.** DMCC, DIFC, ADGM, Masdar City and
    Jafza publish no building/fit-out approval process or code title. Routing via
    community managers or Trakhees/DDA/DM is practice, not confirmed policy.
11. **UAE — master developer NOCs.** Emaar, Nakheel and Aldar publish no named
    design guidelines, though the NOC step is mandatory in practice.
12. **UAE — Sharjah Civil Defence.** No confirmable official site.
13. **Lebanon — Beirut Municipality.** No locatable official portal despite being
    the capital's permitting authority.
14. **Lebanon — Civil Defence.** No confirmed official portal or published
    process.
15. **Lebanon — unreachable sites.** `mopw.gov.lb`, `edl.gov.lb`, `bwe.gov.lb`,
    `dgantiquities.gov.lb`, `beirut.gov.lb`.

---

# 8. MAINTENANCE

- Re-verify this directory at the start of every project, and in full at least
  annually.
- When an entry is confirmed or corrected against a primary source, update the
  row **and** its confidence key, and note the date.
- When a requirement is extracted from any document listed here, create a
  separate note in the relevant discipline folder using [[Regulation Record]],
  and wikilink it back to this directory. Requirements never live in this file.

---

**Related:** [[NORMIA]] · [[Regulation Record]] · [[Project Intake]] ·
[[Planning]] · [[Building Codes]] · [[Fire & Life Safety]] · [[Accessibility]] ·
[[Structural]] · [[Mechanical]] · [[Electrical]] · [[Plumbing]] ·
[[Sustainability]] · [[Environment]] · [[Roads]] · [[Utilities]] · [[GIS]] ·
[[Developer Guidelines]]
