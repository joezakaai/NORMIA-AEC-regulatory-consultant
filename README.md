# NORMIA — AEC Regulatory Intelligence & Compliance Consultant

NORMIA is an AI consultant for architecture, engineering and construction
(AEC) regulatory work across the Middle East. It reads the official
regulations, turns them into a linked knowledge base, and checks projects
against them.

It works to one rule: **never invent a regulation or a compliance result.**
Anything it could not verify from an official source is marked
**UNVERIFIED — OFFICIAL SOURCE REQUIRED**. Numbers are read visually from
the official page images, never from OCR text.

## What is in this repository

| Folder | Contents |
|---|---|
| [`agent/`](agent/) | The NORMIA agent definition (`normia.md`) — role, method, output rules |
| [`vault/`](vault/) | The Obsidian regulation library. Open this folder as a vault in Obsidian |
| [`deliverables/jordan/`](deliverables/jordan/) | Finished reports for the Jordan work |
| [`tools/`](tools/) | The Python scripts that draw the diagrams and build the PDFs |

### The regulation library (`vault/NORMIA/`)

| Country | Coverage |
|---|---|
| **Jordan** | Building and Town & Village Planning Regulation No. (1) of 2022, as amended by No. (12) of 2025 — development control table, height and datum, subdivision, setbacks, parking, fees. Arabic Gazette sources in `Countries/Jordan/sources/` |
| **Lebanon** | Building Law Implementing Decree 15874/2005 — envelope, projections, view distance, coverage and FAR, parking, clear heights, permits. 119 figures from the decree in `_attachments/lebanon/` |
| **Qatar** | QNMP zoning (R1, R2, R3, R5, R6), parking, two villas on one plot, building permit process, QCS, KAHRAMAA, QCDD civil defence, GSAS, accessibility, Lusail and Qetaifan Island North developer guidelines, QMap GIS |
| Saudi Arabia, UAE | Placeholders — not yet populated |

Notes are grouped by discipline (Planning, Building Codes, Fire & Life
Safety, Roads, Utilities, Sustainability…) and linked through country hubs
and the `Authorities/Authority Directory.md`.

### Deliverables (`deliverables/jordan/`)

- **Jordan_Building_Regulation_2022_Illustrated.pdf** — 40-page illustrated
  reference of the Jordanian regulation, article by article, with all fee
  schedules in JOD and 32 diagrams drawn by NORMIA (the Gazette has none).
- **NORMIA_Plot3+4_Capacity_Study.pdf** — 19-page architect's capacity and
  feasibility study for Plots 3+4, Parcel 96, Makawir (near the Dead Sea).
- **Jordan Plot 3+4 Combined … Regulatory Brief.md** — the underlying
  regulatory brief.

## Rebuilding the PDFs

```bash
pip install -r requirements.txt
# Arabic text needs the Noto Naskh Arabic font
#   Debian/Ubuntu: sudo apt install fonts-noto-core

cd tools/jordan-illustrated-regulation
python draw.py      # 32 diagrams -> figs/
python build.py     # -> Jordan_Building_Regulation_2022_Illustrated.pdf

cd ../plot-capacity-study
python calc.py && python figs.py && python build_pdf.py
```

The scripts expect the fonts at `/usr/share/fonts/truetype/noto/`. On
Windows or macOS, change the `ARP` / `ARB` font paths at the top of
`draw.py` and `build.py`.

## Important

This is a reference and research tool, not legal advice. The official
published text of each regulation governs. The diagrams are NORMIA's own
interpretation and carry no legal force. Zone-specific and scheme-specific
provisions override the general tables — always confirm the governing
scheme for a real plot with the competent authority.
