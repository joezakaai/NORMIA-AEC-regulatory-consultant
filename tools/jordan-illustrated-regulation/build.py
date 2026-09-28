import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
"""Jordan Building Regulation No.1/2022 + Amendment No.12/2025 — illustrated reference PDF."""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, KeepTogether,
                                HRFlowable, NextPageTemplate)
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image as PImage

pdfmetrics.registerFont(TTFont("AR", "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf"))
pdfmetrics.registerFont(TTFont("ARB", "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf"))

def ar(s, bold=True):
    f = "ARB" if bold else "AR"
    return f'<font name="{f}">{get_display(arabic_reshaper.reshape(s))}</font>'

INK  = colors.HexColor("#0b0b0b"); INK2 = colors.HexColor("#3f3e3a")
INK3 = colors.HexColor("#6f6d66"); RULE = colors.HexColor("#d6d4ca")
BLU  = colors.HexColor("#2a6fd6"); ORG = colors.HexColor("#c2470f")
GRN  = colors.HexColor("#0b7a55"); RED = colors.HexColor("#c0332f")
AMB  = colors.HexColor("#9a7b2e"); PAPER = colors.HexColor("#fcfcfb")
BOX  = colors.HexColor("#f4f3ed"); HDR = colors.HexColor("#e9e7dd")
PW, PH = A4; M = 18*mm; W = PW - 2*M
REF = "NORMIA · JO-REG-2022 · Rev A"

def S(n, **kw):
    b = dict(name=n, fontName="Helvetica", fontSize=8.9, leading=12.9,
             textColor=INK2, alignment=TA_LEFT, spaceAfter=0)
    b.update(kw); return ParagraphStyle(**b)

st = {
 "h1":   S("h1", fontName="Helvetica-Bold", fontSize=15.5, leading=18.5, textColor=INK, spaceAfter=6),
 "h2":   S("h2", fontName="Helvetica-Bold", fontSize=11.2, leading=14, textColor=INK, spaceBefore=11, spaceAfter=4),
 "h3":   S("h3", fontName="Helvetica-Bold", fontSize=9.4, leading=12.2, textColor=ORG, spaceBefore=8, spaceAfter=3),
 "body": S("body", spaceAfter=5.2),
 "small":S("small", fontSize=7.7, leading=10.8, textColor=INK3, spaceAfter=3),
 "cap":  S("cap", fontSize=7.4, leading=10.2, textColor=INK3, spaceBefore=3, spaceAfter=8),
 "lead": S("lead", fontSize=10.2, leading=14.8, textColor=INK, spaceAfter=7),
 "kick": S("kick", fontName="Helvetica-Bold", fontSize=7.4, leading=9.6, textColor=ORG, spaceAfter=2),
 "tb":   S("tb", fontSize=7.9, leading=10.4),
 "th":   S("th", fontName="Helvetica-Bold", fontSize=7.5, leading=9.6, textColor=INK),
 "tn":   S("tn", fontName="Helvetica-Bold", fontSize=8.1, leading=10.4, textColor=INK, alignment=TA_RIGHT),
 "ct":   S("ct", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=INK, spaceAfter=5),
 "cs":   S("cs", fontSize=12, leading=16.5, textColor=INK2, spaceAfter=4),
 "q":    S("q", fontSize=8.6, leading=13.2, textColor=INK, alignment=TA_RIGHT, spaceAfter=4),
}
SUP = {"\u00b2": "<super>2</super>", "\u00b3": "<super>3</super>"}
import re as _re
_ARABIC = _re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]'
                      r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF'
                      r'\s\u060C\u061B\u061F\u0640()\u066B\u066C0-9\u0660-\u0669/\u060D.,\u00ab\u00bb\u2039\u203a-]*'
                      r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\u00bb]'
                      r'|[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
_FONTSPLIT = _re.compile(r'(<font name="ARB?">.*?</font>)', _re.S)

def _shape(m):
    txt = m.group(0)
    lead = "" ; trail = ""
    core = txt.strip()
    if not core: return txt
    lead = txt[:len(txt)-len(txt.lstrip())]
    trail = txt[len(txt.rstrip()):]
    core = core.replace("(", "\u2039").replace(")", "\u203a")
    return lead + '<font name="ARB">' + get_display(arabic_reshaper.reshape(core)) + '</font>' + trail

def fx(t):
    t = str(t)
    for k, v in SUP.items(): t = t.replace(k, v)
    parts = _FONTSPLIT.split(t)
    out = []
    for i, p in enumerate(parts):
        if p.startswith('<font name="AR'):
            out.append(p)
        else:
            out.append(_ARABIC.sub(_shape, p))
    return "".join(out)
def P(t, s="body"): return Paragraph(fx(t), st[s])

def rule(c=RULE, w=0.7, sb=4, sa=6):
    return HRFlowable(width="100%", thickness=w, color=c, spaceBefore=sb, spaceAfter=sa)

def callout(title, body, accent=ORG, bg=BOX):
    inner = [Paragraph(fx(title), S("x", fontName="Helvetica-Bold", fontSize=8.6,
                                    leading=11.2, textColor=accent, spaceAfter=3))]
    for b in ([body] if isinstance(body, str) else body):
        inner.append(Paragraph(fx(b), S("y", fontSize=8.5, leading=12.0, spaceAfter=3)))
    t = Table([[inner]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("LINEBEFORE",(0,0),(0,-1),2.4,accent),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"TOP")]))
    return [Spacer(1,4), t, Spacer(1,7)]

def dt(rows, widths, align=None, fs=7.9, pad=4.2, hdr=True):
    data=[]
    for i,r in enumerate(rows):
        row=[]
        for j,c in enumerate(r):
            sty = "th" if (hdr and i==0) else ("tn" if (align and j in align) else "tb")
            row.append(Paragraph(fx(c), st[sty]))
        data.append(row)
    t=Table(data, colWidths=widths, repeatRows=1 if hdr else 0)
    cmds=[("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),4.5),
          ("RIGHTPADDING",(0,0),(-1,-1),4.5),("TOPPADDING",(0,0),(-1,-1),pad),
          ("BOTTOMPADDING",(0,0),(-1,-1),pad),("LINEBELOW",(0,0),(-1,-2),0.4,RULE)]
    if hdr: cmds+=[("BACKGROUND",(0,0),(-1,0),HDR),("LINEBELOW",(0,0),(-1,0),0.9,INK3)]
    t.setStyle(TableStyle(cmds)); return t

FIGS = {f["n"]: f for f in json.load(open(HERE + "/figs_index.json"))}
def fig(n, w=None, extra=None):
    f = FIGS[n]; p = f"{HERE}/figs/{f['file']}"
    iw, ih = PImage.open(p).size
    w = w or W
    out = [Spacer(1,3), Image(p, width=w, height=w*ih/iw)]
    cap = f"<b>JO-Fig-{n:02d}</b> — {f['en']}   ·   {f['art']}"
    if extra: cap += f"   ·   {extra}"
    out.append(P(cap, "cap"))
    return out

def quote(a_text, en):
    return [Paragraph(ar(a_text, False), st["q"]),
            Paragraph(fx(f"<i>{en}</i>"), S("qe", fontSize=8.2, leading=11.6,
                                            textColor=INK2, spaceAfter=6))]

def chrome(c, d):
    c.saveState(); c.setFillColor(PAPER); c.rect(0,0,PW,PH,stroke=0,fill=1)
    if d.page > 1:
        c.setStrokeColor(RULE); c.setLineWidth(0.6)
        c.line(M, PH-13*mm, PW-M, PH-13*mm); c.line(M, 12.5*mm, PW-M, 12.5*mm)
        c.setFont("Helvetica", 6.9); c.setFillColor(INK3)
        c.drawString(M, PH-11.4*mm, "Building and Town & Village Planning Regulation No. (1) of 2022  ·  as amended by No. (12) of 2025")
        c.drawRightString(PW-M, PH-11.4*mm, "Hashemite Kingdom of Jordan")
        c.setFont("Helvetica", 6.6); c.drawString(M, 9.6*mm, REF)
        c.drawCentredString(PW/2, 9.6*mm, "Diagrams drawn by NORMIA — the gazette contains none")
        c.setFont("Helvetica-Bold", 7.4); c.setFillColor(INK2)
        c.drawRightString(PW-M, 9.5*mm, str(d.page))
    c.restoreState()

def cover(c, d):
    c.saveState(); c.setFillColor(PAPER); c.rect(0,0,PW,PH,stroke=0,fill=1)
    c.setFillColor(HDR); c.rect(0, PH-30*mm, PW, 30*mm, stroke=0, fill=1)
    c.setFillColor(ORG); c.rect(0, PH-30*mm, PW, 2.4*mm, stroke=0, fill=1)
    c.setStrokeColor(RULE); c.setLineWidth(0.6); c.line(M, 19*mm, PW-M, 19*mm)
    c.setFont("Helvetica", 7.1); c.setFillColor(INK3)
    c.drawString(M, 15*mm, REF)
    c.drawRightString(PW-M, 15*mm, "Prepared by NORMIA — AEC Regulatory Intelligence")
    c.restoreState()

doc = BaseDocTemplate(HERE + "/Jordan_Building_Regulation_2022_Illustrated.pdf",
        pagesize=A4, leftMargin=M, rightMargin=M, topMargin=19*mm, bottomMargin=17*mm,
        title="Jordan Building Regulation No.1/2022 — Illustrated Reference",
        author="NORMIA", subject="نظام الأبنية وتنظيم المدن والقرى رقم 1 لسنة 2022")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[Frame(M, 23*mm, W, PH-57*mm, id="c")], onPage=cover),
    PageTemplate(id="body",  frames=[Frame(M, 17*mm, W, PH-36*mm, id="b")], onPage=chrome)])

E = []

# ═════════════════════════════════════ COVER
E += [Spacer(1, 12*mm),
 P("ILLUSTRATED REGULATORY REFERENCE", "kick"),
 P("Jordan Building Regulation", "ct"),
 P("نظام الأبنية وتنظيم المدن والقرى رقم (1) لسنة 2022".replace("نظام", ""), "cs") if False else
 Paragraph(ar("نظام الأبنية وتنظيم المدن والقرى رقم ١ لسنة ٢٠٢٢"),
           S("cvar", fontSize=15, leading=24, textColor=INK, alignment=TA_RIGHT, spaceAfter=8)),
 P("Regulation No. (1) of 2022, issued under Article 67 of the Provisional Towns, Villages and "
   "Buildings Planning Law No. (79) of 1966<br/>"
   "<b>as amended by the Amending Regulation No. (12) of 2025</b>", "cs"),
 Spacer(1, 4*mm), rule(INK, 1.2, 0, 8)]

hero = Table([[Paragraph("<b>50</b><br/><font size=7 color='#6f6d66'>ARTICLES COVERED</font>",
                S("h", fontSize=19, leading=22, textColor=BLU, alignment=TA_CENTER)),
               Paragraph("<b>32</b><br/><font size=7 color='#6f6d66'>DIAGRAMS DRAWN</font>",
                S("h", fontSize=19, leading=22, textColor=ORG, alignment=TA_CENTER)),
               Paragraph("<b>6</b><br/><font size=7 color='#6f6d66'>FEE SCHEDULES</font>",
                S("h", fontSize=19, leading=22, textColor=GRN, alignment=TA_CENTER)),
               Paragraph("<b>JOD</b><br/><font size=7 color='#6f6d66'>ALL PRICES IN DINARS</font>",
                S("h", fontSize=19, leading=22, textColor=INK, alignment=TA_CENTER))]],
             colWidths=[W/4]*4)
hero.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BOX),("LINEABOVE",(0,0),(-1,0),1.4,INK),
    ("LINEBELOW",(0,-1),(-1,-1),0.6,RULE),("TOPPADDING",(0,0),(-1,-1),10),
    ("BOTTOMPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
E += [Spacer(1,3), hero, Spacer(1,8)]

E += [P("This document sets out the Jordanian building regulation article by article, with every "
        "control table and every fee schedule reproduced in full — and with the rules drawn.", "lead")]
E += callout("A NOTE ON THE DIAGRAMS — PLEASE READ",
 ["The Official Gazette text of this Regulation contains <b>no diagrams whatsoever</b>. All 49 pages "
  "were checked: it is pure text and tables. This is unlike the Lebanese implementing decree, which "
  "carries 119 official drawings.",
  "<b>The 32 diagrams in this document were therefore drawn by NORMIA</b> to illustrate the rules, in "
  "the manner of the Lebanese decree. They are an interpretation of the regulatory text, "
  "<b>not part of the Regulation and of no legal force</b>. Every one is labelled JO-Fig-NN and "
  "cites the article it illustrates.",
  "Where a diagram and the text of this document appear to differ, <b>the text governs</b>; and where "
  "the text of this document and the Official Gazette differ, <b>the Gazette governs</b>."],
 RED, colors.HexColor("#fbf0ef"))
E += [P("Contents — 1 How this document was made · 2 Identity of the instrument · 3 Definitions · "
        "4 Zones and uses · 5 Subdivision · 6 Height and the datum · 7 Development control · "
        "8 Licensing · <b>9 Fees and prices</b> · 10 Building elements · 11 Parking · "
        "12 Outside the planning areas · 13 Miscellaneous provisions · 14 The 2025 amendment · "
        "15 Figure index · 16 Basis, limitations and sources", "small")]
E += [NextPageTemplate("body"), PageBreak()]

# ═════════════════════════════════════ 1 METHOD
E += [P("1 · How this document was made", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("The Regulation was published as a vector PDF of the Official Gazette. It carries almost no "
        "extractable text layer, so every page was rendered as an image and <b>read visually</b>.", "body")]
E += [dt([["Step", "What was done", "Why"],
  ["Source", "Official Gazette PDF of Regulation No. (1) of 2022 — 49 pages — and the Amending "
             "Regulation No. (12) of 2025 — 3 pages.", "The two instruments must be read together."],
  ["Text", "OCR was run, but used <b>only to locate</b> provisions.",
           "Arabic-Indic numeral OCR is not reliable enough to design against."],
  ["<b>Numbers</b>", "<b>Every numeric value was read visually from the page image</b>, at magnification "
                     "where the print is small.", "A misread fee or setback is worse than no figure at all."],
  ["Diagrams", "Drawn from the verified text by NORMIA. The Gazette has none.",
               "To present the rules the way the Lebanese decree presents its own."],
  ["Unverified", "Anything that could not be read with certainty is marked <b>UNCLEAR IN SOURCE</b>.",
                 "NORMIA never invents a regulation or a number."]],
  [22*mm, 86*mm, W-108*mm])]
E += callout("The Golden Rule",
 "Nothing in this document has been inferred, rounded or filled in. Where the Gazette is internally "
 "inconsistent, both readings are recorded and the conflict is flagged rather than resolved.",
 GRN, colors.HexColor("#eef7f2"))

# ═════════════════════════════════════ 2 IDENTITY
E += [P("2 · Identity of the instrument", "h1"), rule(INK, 1.0, 0, 8)]
E += [dt([["Item", "Value"],
  ["Title", "نظام الأبنية وتنظيم المدن والقرى لسنة ٢٠٢٢ — the Building and Town &amp; Village Planning Regulation of 2022"],
  ["Number", "Regulation No. (1) of 2022"],
  ["Enabling provision", "Article (67) of the Provisional Towns, Villages and Buildings Planning Law No. (79) of 1966"],
  ["Constitutional basis", "Article (31) of the Constitution"],
  ["Council of Ministers decision", "12/12/2021"],
  ["Commencement", "From the date of publication in the Official Gazette (Article 1)"],
  ["Amended by", "<b>نظام معدّل رقم (١٢) لسنة ٢٠٢٥</b> — Amending Regulation No. (12) of 2025, "
                 "Council of Ministers decision 29/1/2025, Gazette pp. 835–837, read as one with the 2022 Regulation"],
  ["Extent", "50 articles · 49 Gazette pages · no diagrams"],
  ["Competent bodies", "مجلس التنظيم الأعلى (the Higher Planning Council) · اللجنة المختصة "
                       "(the Local, District, Joint District or Joint Local Planning Committee) · "
                       "دائرة تنظيم المدن والقرى والأبنية المركزية (the Central Department)"]],
  [40*mm, W-40*mm])]
E += [P("Scope — Article 3", "h3")]
E += quote("تطبق أحكام هذا النظام على الأراضي والأبنية ومشاريع الإعمار ضمن مناطق التنظيم في المملكة … "
           "باستثناء مناطق التنظيم التي تخضع لتشريعات خاصة بها",
           "The provisions apply to lands, buildings and development projects within the planning areas "
           "of the Kingdom, and to any person, ministry, department, local authority, municipality or "
           "public institution — EXCEPT planning areas subject to their own special legislation.")
E.append(PageBreak())

# ═════════════════════════════════════ 3 DEFINITIONS
E += [P("3 · Definitions — Article 2", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("The definitions do the heavy lifting in this Regulation. Four of them — the basement, the "
        "semi-basement, the coverage percentage and the floor area — decide most of what can actually "
        "be built, because they decide what <b>counts</b>.", "body")]
E += [dt([["Term", "Definition", "The operative number"],
  ["<b>ارتفاع البناء</b><br/>Building height", "The vertical distance between the <b>average level of the road</b> "
     "and the highest point of the structural roof slab.", "—"],
  ["<b>طابق القبو</b><br/>Basement", "The floor(s) below natural ground level <b>on all sides</b>, provided the "
     "concrete slab does not exceed 45 cm above natural ground or the average level of the abutting road, "
     "<b>whichever is lower</b>. May be built over the entire plot boundary <b>except the front setback</b>.",
     "<b>45 cm</b>"],
  ["<b>طابق التسوية</b><br/>Semi-basement", "The floor(s) below the ground floor whose concrete slab does not "
     "exceed one and a half metres above the average road level.", "<b>1.50 m</b>"],
  ["<b>الطابق الأرضي</b><br/>Ground floor", "A floor, or part of one, directly above natural ground level, or "
     "directly above the semi-basement or the basement.", "—"],
  ["<b>المساحة الطابقية</b><br/>Floor area", "The sum of the <b>roofed</b> horizontal projections of all floors, "
     "<b>excluding</b> semi-basements, basements, commercial mezzanines, mechanical service floors, commercial "
     "and architectural projections, car parking, open passages and stairs, light wells, mechanical ventilation "
     "voids, the lift-room roof and the last-stair roof.", "—"],
  ["<b>النسبة الطابقية</b><br/>Floor area ratio", "The floor area divided by the plot area.", "—"],
  ["<b>النسبة المئوية للبناء</b><br/>Coverage", "The area of the <b>largest horizontal projection</b> divided by the "
     "plot area, <b>excluding</b> commercial and architectural projections, car parking, <b>basements</b>, open "
     "passages and stairs, wells and collection pits, fuel and water tanks, electrical rooms and generators, "
     "light wells and ventilation voids.", "—"],
  ["<b>حجم البناء</b><br/>Building volume", "The permitted building area under the coverage percentage, "
     "<b>multiplied by the prescribed height</b>.", "—"],
  ["<b>الارتداد</b><br/>Setback", "The space separating the building from the plot boundary, or from the line of "
     "the road abutting the plot.", "—"],
  ["<b>المنور</b><br/>Light well", "An internal void within the building providing light and ventilation to the "
     "parts overlooking it, <b>not to be roofed except at the last floor</b>.", "—"],
  ["<b>السدة التجارية</b><br/>Commercial mezzanine", "A secondary floor forming part of a shop, accessible "
     "<b>only</b> through that shop.", "—"],
  ["<b>الروف</b><br/>Roof floor", "The floor whose erection is permitted under this Regulation.", "—"],
  ["<b>البناء الفرعي</b><br/>Ancillary building", "The building subordinate to a main building and <b>detached</b> "
     "from it, serving it.", "—"],
  ["<b>البناء العالي</b><br/>High-rise", "A building whose height exceeds the limit prescribed for the plot — "
     "<b>except in areas regulated by special provisions</b>.", "—"],
  ["<b>الحفرة التجميعية المصمتة</b><br/>Sealed pit", "The pit for wastewater, closed on all sides with reinforced "
     "concrete and <b>not permitting seepage</b>.", "—"],
  ["<b>الأرض الخلاء المقيدة</b><br/>Restricted open land", "Land on which building is <b>permanently prohibited</b> "
     "and classified as such on an approved scheme.", "—"]],
  [36*mm, W-36*mm-24*mm, 24*mm])]
E += fig(1)
E += fig(12)
E += fig(13)
E += callout("Why the basement is the most valuable definition in the Regulation",
 ["A <b>قبو</b> is excluded from the coverage percentage AND from the floor area, and may occupy the "
  "entire plot except the front setback. A <b>تسوية</b> is excluded from the floor area only — and its "
  "presence forfeits the natural-ground height relief of Article 15(c).",
  "The whole difference is <b>45 cm against 1.50 m</b>. On any sloping site that dimension is worth "
  "more than any other in the document."], BLU, colors.HexColor("#eef4fc"))
E += fig(10)
E += fig(11)
E += fig(19)
E.append(PageBreak())

# ═════════════════════════════════════ 4 ZONES
E += [P("4 · Zones and permitted uses — Articles 4 to 10", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 4 — land-use categories in a planning area", "h3")]
E += [dt([["", "Arabic", "English"],
  ["أ","المناطق السكنية","Residential areas"],["ب","المناطق التجارية","Commercial areas"],
  ["ج","مناطق أبنية متعددة الاستعمال","Multi-use building areas"],["د","المناطق الصناعية","Industrial areas"],
  ["هـ","مواقف سيارات","Car parks"],["و","المباني العامة","Public buildings"],
  ["ز","المكاتب والإدارات","Offices and administrations"]], [10*mm, 60*mm, W-70*mm])]
E += [P("Article 5 — what may be put in a residential zone", "h2")]
E += [P("The residential zone is for residential buildings, but Article 5(c) opens three routes to "
        "other uses — each at a different level of authority.", "body")]
E += [dt([["Decided by", "What may be permitted", "Conditions"],
  ["<b>The Council</b><br/>المجلس", "Private hospitals · hotels · inns · hotel suites · private schools · "
    "special education and care centres · homes for the elderly and the like",
    "<b>Double the side and rear setbacks</b> on the side of the adjoining residence · coverage "
    "<b>not exceeding 50%</b> · land area <b>not less than 3 dunums</b> for hospitals and schools · "
    "except those existing and licensed before 1/1/2017"],
  ["<b>The Council</b>", "Use of <b>existing</b> buildings as hotels, inns, hotel suites and restaurants", "—"],
  ["<b>The Competent Committee</b><br/>اللجنة المختصة", "Local services: pharmacy · water stations · florist · "
    "GP clinic · frozen goods · grocery · greengrocer · bookshop · men's barber · ladies' hairdresser · "
    "home maintenance · kindergartens and nurseries",
    "<b>Must be on the GROUND FLOOR of the building</b>"],
  ["<b>The Mayor</b><br/>رئيس البلدية", "Home-based occupations: translation · printing · fashion design · "
    "marketing and advertising design · architectural drawing · studies and consultancy · financial, "
    "administrative and technical services · IT and website design · online sales · sewing and embroidery · "
    "jewellery · ceramic decoration · mat and carpet weaving · soap · candles · jams · bakery · vegetable, "
    "herb and legume preparation · pickles · jameed", "—"]],
  [34*mm, 70*mm, W-104*mm])]
E += callout("A fee consequence that is easy to miss",
 "Article 5(d): <b>multi-use building fees</b> are levied on the uses permitted under Article 5(c)(1) — "
 "the hospitals, hotels, schools and care homes. They are not charged at the residential rate.",
 AMB, colors.HexColor("#fcf6e8"))
E += [P("Articles 6 to 9 — the other zones", "h2")]
E += [dt([["Article", "Zone", "Categories / content"],
  ["6", "Commercial — المناطق التجارية", "<b>تجاري مركزي</b> central · <b>معارض تجارية</b> showrooms · "
     "<b>تجاري محلي</b> local · <b>تجاري طولي</b> linear. Used for commerce, housing, public services, places "
     "of worship, offices, showrooms, hotels, oil-change and car-wash stations, warehouses, restaurants, "
     "renewable-energy projects and playing fields."],
  ["7", "Multi-use — متعدد الاستعمال", "Commerce · renewable-energy projects · playing fields · housing · "
     "offices · exhibitions · conferences · display halls · any other use on the structural or detailed scheme."],
  ["8", "Industrial — المناطق الصناعية", "<b>الحرفية</b> craft · <b>التقنية</b> technical · <b>الخفيفة</b> light · "
     "<b>المتوسطة</b> medium · <b>الثقيلة</b> heavy · <b>التحويلية</b> processing. Commercial uses under Article 6 "
     "are also permitted in industrial zones. Heavy industry requires <b>prior approvals</b>. "
     "Processing-industry areas take the <b>technical-industry</b> provisions and fees."],
  ["9", "Workers' housing", "The Competent Committee may permit <b>workers' housing in industrial areas</b> on "
     "the conditions it sets."]], [14*mm, 40*mm, W-54*mm])]
E += [P("Article 10 — investment projects outside the planning areas", "h2")]
E += [P("The Council may require a <b>geological study</b>, an <b>environmental impact study</b>, a "
        "<b>traffic impact study</b>, and the approval of the <b>Department of Antiquities</b>. Investment "
        "projects include universities and private schools, hospitals, hotels, restaurants, parks, malls, "
        "residential suburbs, sports fields, amusement cities, wedding and entertainment halls, cinemas "
        "and theatres, fuel stations, warehouses, car washes, grain mills, factories, housing projects "
        "and renewable-energy projects.", "body")]
E += [dt([["Obligation on the owner of a housing project — Article 10(d)", "Requirement"],
  ["Opening the streets inside the project", "at the owner's expense"],
  ["Delivering electricity and water to all plots", "at the owner's expense"],
  ["Land for basic services", "<b>not less than 8%</b> of the project's gross area, subdivided and registered "
   "in the name of the municipality or the Ministry, and suitable for the purpose"]], [W-40*mm, 40*mm])]
E += fig(31)
E.append(PageBreak())

# ═════════════════════════════════════ 5 SUBDIVISION
E += [P("5 · Subdivision — Articles 11 to 14", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 11(a) — minimum subdivision area and plot frontage", "h2")]
E += [dt([["Zone", "Min. subdivision area", "Min. frontage"],
  ["<b>Residential</b> — سكن أ", "1,000 m²", "25 m"], ["سكن ب", "750 m²", "20 m"],
  ["سكن ج", "500 m²", "18 m"], ["سكن د", "250 m²", "15 m"],
  ["السكن الأخضر / الريفي — Green / Rural", "<b>2,000 m²</b>", "<b>30 m</b>"],
  ["السكن الزراعي — Agricultural residential", "4,000 m²", "35 m"],
  ["<b>Commercial</b> — التجاري المركزي", "1,000 m²", "25 m"],
  ["المعارض التجارية — showrooms", "1,000 m²", "25 m"],
  ["التجاري الطولي — linear", "250 m²", "12 m"],
  ["التجاري المحلي — local", "as prescribed for the area", ""],
  ["<b>Multi-use</b> — متعدد الاستعمال", "1,000 m²", "25 m"],
  ["<b>Public buildings</b> — مبانٍ عامة", "1,000 m²", "25 m"],
  ["<b>Industrial</b> — الحرفية craft", "1,000 m²", "25 m"],
  ["الصناعات التقنية — technical", "1,000 m²", "25 m"],
  ["الصناعات الخفيفة — light", "2,000 m²", "30 m"],
  ["الصناعات المتوسطة — medium", "5,000 m²", "50 m"],
  ["الصناعات الثقيلة — heavy", "10,000 m²", "60 m"],
  ["<b>Agricultural facilities</b> — المنشآت الزراعية", "10,000 m²", "60 m"],
  ["<b>Offices and administrations</b>", "750 m²", "20 m"]],
  [W-64*mm, 34*mm, 30*mm], align={1,2})]
E += fig(2)
E += [P("Article 11(b) and (c) — two rules that decide a great many real cases", "h3")]
E += [P("<b>(b)</b> For planning uses not expressly provided for here, <b>the provisions under which the "
        "scheme was approved</b> apply.<br/>"
        "<b>(c)(1)</b> Buildings proposed <b>above an existing lawfully licensed building</b> are governed by "
        "the provisions under which that existing building was licensed.<br/>"
        "<b>(c)(2)</b> Where the existing building encroaches on the setback and was licensed before this "
        "Regulation came into force, <b>setback-encroachment fees are not levied</b> on the proposed building "
        "if those encroachments no longer contravene this Regulation.", "body")]
E += [P("Article 13(e)(1) — the width of a subdivision road fixes how many plots it may serve", "h2")]
E += [dt([["Road width", "Maximum plots served"], ["6 m", "1"], ["8 m", "2"],
          ["10 m", "3 – 10"], ["12 m", "11 – 19"], ["14 m", "20 and more"]],
         [W-40*mm, 40*mm], align={1})]
E += fig(3)
E += [P("Article 13(a) also allows the Committee to reduce the subdivision restrictions by up to "
        "<b>10%</b> where the land is irregular in shape, carries an existing building, has had more than a "
        "quarter expropriated, or the subdivision is between co-owners — and by up to <b>15%</b> in "
        "agricultural, rural and green residential zones. Outside the planning boundary, Article 13(e)(2) "
        "sets the subdivision road minimum at <b>six metres</b>.", "body")]
E.append(PageBreak())

# ═════════════════════════════════════ 6 HEIGHT
E += [P("6 · Height and the datum — Article 15", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 15 is the most consequential article in the Regulation for anyone working on sloping "
        "ground, because it decides the level from which every height is counted.", "lead")]
E += [P("(a)(1) — the general rule, and the 8 m test", "h3")]
E += quote("يكون ارتفاع البناء هو المسافة العامودية من متوسط مناسيب هذه الطرق الى اعلى نقطة من السطح "
           "الإنشائي للبناء ولا تعتمد الطرق التي تقل سعتها عن ٨ امتار أو الطريق التي تقل واجهة القطعة "
           "عليها عن ٥٠٪ من طول تلك الواجهة لاحتساب متوسط المنسوب",
           "Height is the vertical distance from the AVERAGE of the levels of the adjoining roads to the "
           "highest point of the structural surface. Roads narrower than 8 m are NOT relied upon, nor is a "
           "road on which the plot's frontage is less than 50% of the length of that frontage.")
E += fig(4)
E += [P("(a)(2) — where every adjoining road falls short", "h3")]
E += [P("Where the plot fronts more than one road and they all fail the (1) tests, height is computed "
        "from the average of the levels of <b>those</b> roads. Read together, (1) drops non-qualifying "
        "roads while a qualifying one survives, and (2) is the fallback when they all fail.", "body")]
E += fig(5)
E += [P("(a)(3) — more than one building on the plot", "h3")]
E += fig(6)
E += [P("(c) — the relief where natural ground sits above the road", "h3")]
E += quote("إذا كان منسوب الأرض الطبيعية لقطعة الأرض أعلى من منسوب الطريق فيسمح باحتساب ارتفاع البناء "
           "من منسوب الأرض الطبيعية شريطة أن لا يشتمل البناء على طوابق تسوية، واستعمال أول طابق من البناء "
           "مواقف سيارات او خدمات ويستثنى هذا الطابق من أحكام الارتفاع وعدد الطوابق",
           "Where the natural ground level is higher than the road level: height may be computed from "
           "natural ground, PROVIDED the building contains no semi-basement floors; and the first floor may "
           "be used for parking or services, and that floor is EXCLUDED from the height provisions and from "
           "the permitted number of floors.")
E += fig(7)
E += [P("(d), (e) and (f)", "h3")]
E += [dt([["Provision", "Rule"],
  ["15(d)", "The ground-floor slab may be raised a maximum of <b>2 m</b> above natural ground or road "
            "level, where there is <b>no</b> basement and <b>no</b> semi-basement, and provided the "
            "overall height limit is respected."],
  ["15(e)", "The floor used for <b>mechanical services</b> is excluded from the maximum height and from "
            "the floor count — unless the ground floor is used for parking under the Article 36(b)(4) exception."],
  ["15(f)", "Where the plot fronts a <b>single</b> road that has several levels, height is computed from "
            "the <b>average</b> level of that road."],
  ["15(b)", "Where the plot adjoins several roads, the <b>semi-basement</b> surface level is computed per (a). "
            "Excepted: linear commercial and commercial showrooms, where it equals the commercial street pavement level."]],
  [20*mm, W-20*mm])]
E += fig(8)
E += fig(9)
E.append(PageBreak())

# ═════════════════════════════════════ 7 DEVELOPMENT CONTROL
E += [P("7 · Development control — Article 16", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 16(a) — the master control table", "h2")]
E += [dt([["Zone", "Front", "Side", "Rear", "Coverage", "Floors", "Max height", "Green area"],
  ["<b>1 · Residential</b>","","","","","","",""],
  ["سكن أ — A","5 m","4 m","5 m","39%","4","17 m","15%"],
  ["سكن ب — B","4 m","3 m","4 m","45%","4","17 m",""],
  ["سكن ج — C","3 m","2.5 m","3 m","51%","4","17 m",""],
  ["سكن د — D","3 m","2.5 m","2.5 m","55%","4","17 m",""],
  ["<b>الأخضر / ريفي</b> — Green / Rural","<b>8 m</b>","<b>6 m</b>","<b>6 m</b>","<b>27%</b>","<b>2 + roof</b>","<b>9 m</b> excl. roof","<b>10%</b>"],
  ["السكن الزراعي — Agricultural","10 m","6 m","10 m","15%","2 + roof","9 m excl. roof",""],
  ["<b>2 · Commercial</b>","","","","","","",""],
  ["التجاري المركزي — central","10 m","6 m","6 m","50%","4","20 m","15%"],
  ["التجاري المحلي — local <i>(setbacks, coverage and floors follow the adjoining residential zone)</i>","—","—","—","—","—","20 m",""],
  ["المعارض التجارية — showrooms","10 m","6 m","6 m","60%","4","20 m",""],
  ["تجاري طولي — linear","4 m","4 m after 14 m depth","4 m","70%","4","20 m",""],
  ["<b>3 · Multi-use</b>","10 m","6 m","6 m","50%","8","30 m","15%"],
  ["<b>4 · Public buildings</b>","10 m","6 m","6 m","50%","8","30 m","15%"],
  ["<b>5 · Offices</b>","6 m","5 m","6 m","50%","8","30 m","15%"],
  ["<b>6 · Industrial</b> — الحرفية craft","10 m","—","3 m","50%","2","12 m","20%"],
  ["الصناعات الخفيفة — light","12 m","5 m","5 m","50%","4","18 m",""],
  ["الصناعات التقنية — technical","6 m","5 m","6 m","50%","4","18 m",""],
  ["الصناعات المتوسطة — medium","12 m","10 m","10 m","50%","4","18 m",""],
  ["الصناعات الثقيلة — heavy","15 m","10 m","15 m","50%","4","18 m",""],
  ["<b>7 · Agricultural facilities</b>","15 m","15 m","15 m","10%","—","12 m","20%"],
  ["<b>8 · Outside the planning boundary</b> — commercial complex and offices","12 m","10 m","10 m","50%","8","30 m","15%"],
  ["الفنادق — hotels","12 m","10 m","10 m","50%","8","30 m",""],
  ["مبانٍ متعددة الاستعمال — multi-use","15 m","10 m","10 m","35%","8","30 m",""],
  ["<b>9 · Residential suburbs</b> — in special residential areas","6 m","5 m","5 m","40%","4","15 m",""],
  ["in general residential areas","6 m","4 m","5 m","35%","8","30 m",""],
  ["<b>10 · Large factories</b>","15 m","15 m","15 m","50%","2","—",""],
  ["<b>11 · Industrial complexes</b>","15 m","15 m","15 m","50%","","",""]],
  [W-114*mm, 15*mm, 19*mm, 15*mm, 17*mm, 15*mm, 19*mm, 14*mm], align={1,2,3,4,5,6,7}, fs=7.2, pad=3.0)]
E += [P("Blank cells indicate a value merged with the row above in the Gazette. Read them as carrying "
        "the value immediately above.", "small")]
E += fig(14)
E += fig(15)
E += [P("Article 16(b) to (g) — the high-building regime and its exclusions", "h2")]
E += [P("<b>(b)</b> The competent planning committee may permit <b>high buildings</b>: residential "
        "8 m / 10 m / 10 m setbacks, 35% coverage, 8 floors, 30 m, 20% green; commercial 8/10/10, 50%, "
        "8 floors, 35 m, 20%; multi-use 15/12/12, 50%, <b>16 floors, 50 m</b>, 15%.", "body")]
E += [P("<b>(c)</b> Notwithstanding (b), the committee may increase the height and floor count: "
        "every <b>100 m²</b> above the prescribed minimum subdivision area grants <b>35 cm</b>; every "
        "<b>1 m</b> of extra side and front setback grants <b>30 cm</b>.", "body")]
E += [P("<b>(d)</b> In no case may the building height exceed <b>60 m</b>.", "body")]
E += callout("⚠  Article 16(e) — the exclusion that catches most real plots",
 ["<b>«تستثنى المناطق المنظمة بأحكام سكن أخضر أو سكن ريفي أو سكن زراعي أو المناطق المنظمة بأحكام خاصة "
  "والقطع المخدومة بطرق تقل سعتها عن ٢٠م من تطبيق أحكام الفقرات (ب) و(ج) و(د)»</b>",
  "Green, rural and agricultural residential zones, areas regulated by special provisions, "
  "<b>AND any plot served by roads narrower than 20 m</b>, are excluded from paragraphs (b), (c) and (d).",
  "So: no high-building table, <b>no height bonuses</b>, and the 60 m provision is irrelevant. The road "
  "test is independent of the zone — a plot on a 10 m street gets no bonus whatever its class."],
 RED, colors.HexColor("#fbf0ef"))
E += fig(16)
E += fig(17)
E += [P("<b>(f)</b> An <b>additional floor</b> of not more than 4 m may be licensed on plots fronting "
        "streets of not less than <b>14 m</b>, subject to providing that floor's parking. Not available "
        "where the plot's scheme was ratified before <b>16/1/2018</b>.<br/>"
        "<b>(g)</b> The Council may approve buildings <b>without being bound by the coverage percentage</b> "
        "in the (a) table, provided full plans for the whole building are submitted and the floor-area "
        "ratio and the prescribed setbacks are respected.", "body")]
E += fig(18)
E.append(PageBreak())

# ═════════════════════════════════════ 8 LICENSING
E += [P("8 · Licensing — Articles 17, 18, 21, 24, 25", "h1"), rule(INK, 1.0, 0, 8)]
E += [dt([["Article", "Subject", "Substance"],
  ["17", "الترخيص — the permit", "The application, the drawings certified by the Jordanian Engineers "
    "Association and the relevant authorities, and the conditions on which the Competent Committee issues "
    "the written authorisation to commence."],
  ["18", "ترخيص الأبنية القائمة", "Licensing buildings already erected, and the conditions attaching."],
  ["21", "تأمين الترخيص", "The licensing guarantee to be lodged, securing compliance with the permit "
    "conditions and with this Regulation."],
  ["24", "تعديل رخصة الإنشاءات", "Modification of a construction licence."],
  ["25", "وقف العمل في مشروع الإعمار", "Stop-work orders on a development project."],
  ["30", "كودات البناء الوطني", "Compliance with the National Building Codes issued under the National "
    "Building Law."],
  ["41", "إذن الإشغال", "The occupancy permit, its conditions and the certificate of conformity. "
    "<b>Amended in 2025</b> — a flagpole (سارية علم) is now a required item, to specifications set by "
    "instructions of the Minister."],
  ["42", "المباني التراثية", "Heritage buildings and the provisions applying to them."]],
  [16*mm, 40*mm, W-56*mm])]
E.append(PageBreak())

# ═════════════════════════════════════ 9 FEES
E += [P("9 · Fees and prices — Articles 19, 20 and 22", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("All figures are in <b>Jordanian Dinars (JOD)</b>. The Article 19 table is stated for "
        "<b>first-category municipalities</b>; second and third category pay a reduced share, set out "
        "below the table.", "lead")]
E += callout("Two rules that govern the whole of this section",
 ["<b>Article 19(a):</b> these fees apply in first-category municipalities <b>whether inside or outside "
  "the planning boundary</b>.",
  "<b>Article 20(b):</b> encroachment fees are levied <b>IN ADDITION</b> to the Article 19 fees, and only "
  "when licensing a building that <b>predates 1/1/2017</b>. Encroachments arising after that date may not "
  "be licensed at all unless the committee is satisfied they were technical and beyond the owner's control."],
 BLU, colors.HexColor("#eef4fc"))

E += [P("Article 19(a) — licensing fees · first-category municipalities · JOD", "h2")]
E += [dt([["Item", "Unit", "Residential", "Commercial,<br/>showrooms,<br/>offices",
           "Light, craft,<br/>technical ind.<br/>&amp; warehouses", "Medium, heavy<br/>ind. &amp; large<br/>factories",
           "Multi-use,<br/>public &amp; renewable<br/>energy buildings", "Agricultural<br/>facilities"],
  ["Site plan and demarcation<br/>رسم مخطط موقع وترسيم", "each", "5", "10", "10", "10", "10", "3"],
  ["Building licence application<br/>رسم طلب ترخيص بناء", "one time", "6", "12", "12", "12", "12", "5"],
  ["Ground floor, building floors<br/>and balconies", "per m²", "0.50", "1.5", "1.5", "3", "1.5", "0.3"],
  ["Basements, mezzanines, levelling<br/>floor, architectural projection", "per m²", "0.50", "1.5", "1.5", "1.2", "2", "—"],
  ["Covered car parking", "per m²", "0.30", "0.30", "0.30", "0.30", "0.30", "—"],
  ["Walls and fences<br/>رسم الأسوار", "per linear m", "0.15", "0.30", "0.25", "0.30", "0.30", "0.10"],
  ["Swimming pool", "per m²", "50", "100", "100", "100", "100", "(blank in source)"],
  ["Subdivision of buildings<br/>and apartments", "per unit", "10", "35", "20", "20", "35", "—"],
  ["Subdivision of land", "per parcel", "5", "35", "20", "20", "35", "5"],
  ["Commercial projection over<br/>the front setback", "per m²", "—", "30", "—", "—", "30", "—"],
  ["Commercial projection over the<br/>street above the ground floor", "per m²", "—", "60", "—", "—", "60", "—"],
  ["<b>Each telecommunications tower</b>", "one time", "<b>2,000 JOD — a single merged figure across all zone columns</b>", "", "", "", "", ""]],
  [40*mm, 16*mm] + [(W-56*mm)/6]*6, align={2,3,4,5,6,7}, fs=6.9, pad=3.0)]
E += [dt([["Reduction", "Provision"],
  ["<b>Second-category municipalities — 60%</b>", "of all Article 19(a) fees, <b>except</b> the telecommunications-tower fee — Art. 19(b)"],
  ["<b>Third-category municipalities — 50%</b>", "of all Article 19(a) fees, same exception — Art. 19(b)"],
  ["<b>Residential outside the municipal boundary — 50%</b>", "of the Article 19(a) licensing fees — Art. 19(c)"],
  ["<b>Buildings granted reductions under Art. 37 of the Law — +20%</b>", "construction-licence fees PLUS 20% of those fees — Art. 19(d)"]],
  [72*mm, W-72*mm])]
E.append(PageBreak())

E += [P("Article 20(b) — encroachment fees · JOD", "h2")]
E += [P("These are the fees for licensing a violation of the planning provisions. They are computed, "
        "not tabulated flat — the table sets the <b>ceiling and the floor</b> on the per-square-metre value.", "body")]
E += fig(32)
E += [P("20(b)(1) — encroachment on the front, side and rear setbacks", "h3")]
E += quote("يستوفى ما يعادل مساحة التجاوز مضروبة في قيمة المتر المربع حسب تقدير دائرة الأراضي والمساحة "
           "شريطة ان لا تتجاوز قيمة المتر المربع الواحد على الحد الأعلى الوارد في الجدول ولا تقل عن الحد الأدنى",
           "The fee equals the encroached area multiplied by the value of the square metre as assessed by the "
           "Department of Lands and Survey, provided the per-m² value neither exceeds the maximum nor falls "
           "below the minimum in the table.")
E += [dt([["Zone", "Unit", "Maximum JOD/m²", "Minimum JOD/m²"],
  ["Residential — سكنية", "per m²", "150", "15"],
  ["Commercial, showrooms and offices", "per m²", "200", "30"],
  ["Light, craft and technical industries, warehouses", "per m²", "150", "20"],
  ["Medium and heavy industries, large factories", "per m²", "200", "30"],
  ["Agricultural facilities", "per m²", "20", "3"],
  ["Multi-use, public buildings, renewable-energy buildings", "per m²", "200", "30"]],
  [W-72*mm, 18*mm, 27*mm, 27*mm], align={1,2,3})]
E += [P("20(b)(2) — encroachment on the coverage percentage", "h3")]
E += [dt([["Zone", "Unit", "Maximum JOD/m²", "Minimum JOD/m²"],
  ["Residential — سكنية", "per m²", "200", "25"],
  ["Commercial, showrooms and offices", "per m²", "300", "35"],
  ["Light, craft and technical industries, warehouses", "per m²", "150", "20"],
  ["Medium and heavy industries, large factories", "per m²", "300", "35"],
  ["Agricultural facilities", "per m²", "10", "3"],
  ["Multi-use, public buildings, renewable-energy buildings", "per m²", "300", "35"]],
  [W-72*mm, 18*mm, 27*mm, 27*mm], align={1,2,3})]
E += [P("20(b)(3) — encroachment on the floor-area ratio, and on building volume or height", "h3")]
E += [dt([["Zone", "On the floor-area ratio<br/>JOD per m²", "On building volume or height<br/>JOD per m³"],
  ["Residential — مناطق السكن", "50", "25"],
  ["Commercial, showrooms and offices", "70", "35"],
  ["Light, craft and technical industries, warehouses", "60", "30"],
  ["Medium and heavy industries, large factories", "70", "35"],
  ["Agricultural facilities", "2", "1"],
  ["Multi-use, public buildings, renewable-energy buildings", "70", "35"]],
  [W-76*mm, 38*mm, 38*mm], align={1,2})]
E += callout("The discount that applies here",
 "Article 20(c): <b>second-category municipalities levy 60%</b> and <b>third-category 50%</b> of the "
 "item (3) fees — the floor-area-ratio and volume/height fees immediately above. "
 "Article 20(b)(4): the Council may issue the instructions necessary to apply the paragraph.",
 AMB, colors.HexColor("#fcf6e8"))
E += [P("Article 22 — buildings erected without a licence after 1/1/2017", "h3")]
E += [P("Article 22 sets the fees for buildings put up without any licence after 1/1/2017. "
        "Article 23 addresses <b>green buildings</b> (المباني الخضراء) — buildings constructed with high "
        "environmental responsibility across the whole life cycle, from site selection to demolition.", "body")]
E.append(PageBreak())

# ═════════════════════════════════════ 10 BUILDING ELEMENTS
E += [P("10 · Building elements — Articles 26 to 35", "h1"), rule(INK, 1.0, 0, 8)]
E += [dt([["Article", "Subject", "Substance"],
  ["26","الكثافة السكانية والمواقف","Residential density and its relationship to the parking requirement."],
  ["27","المناور — light wells","Dimensions and conditions. A light well may not be roofed except at the last floor."],
  ["28","طابق القبو — the basement","Permitted uses only: <b>parking · reinforced-concrete water wells and "
      "tanks · storage rooms · heating, cooling and fuel rooms · electrical rooms</b>. In commercial zones "
      "the basement slab may be raised to the commercial street level; the pavement may not be used for "
      "any building construction."],
  ["29","البروز — projections","See the table and figure below."],
  ["31","الممرات والأدراج المكشوفة","Open passages and stairs — excluded from the coverage and the floor area."],
  ["32","التصوينة","The roof parapet."],
  ["33","الأسوار والطمم والأسقف بالارتدادات","Fences, fill and decking within the setbacks — below."],
  ["34","الأبنية الفرعية","The ancillary building — below."],
  ["35","الأبنية المؤقتة","Temporary buildings: storage of materials, workers' housing, guards' rooms and "
      "site offices during construction; event tents; mobile food vehicles in commercial and multi-use zones."]],
  [16*mm, 42*mm, W-58*mm])]
E += fig(19)
E += [P("Article 29 — projections", "h2")]
E += [dt([["Type", "Rule"],
  ["<b>البروز التجاري</b><br/>Commercial projection", "Front balconies overhanging streets, squares and plazas, "
    "projecting beyond the building line by not more than <b>1.40 m</b> where the street is not less than "
    "<b>16 m</b>, and not more than <b>1.20 m</b> where it is less."],
  ["<b>Prohibition</b>", "<b>No projection of any kind is permitted where the street is 12 m or less.</b> The "
    "distance between a projecting balcony and the adjoining plot boundary may not be less than 1.50 m, and "
    "the vertical clearance between the balcony soffit and any point of the pavement may not be less than 3.50 m."],
  ["<b>البروز المعماري</b><br/>Architectural projection", "Unoccupied parts built for the decoration of façades "
    "or for weather protection, within the prescribed setbacks, projecting not more than <b>60 cm</b> from "
    "the building line."],
  ["<b>مظلة المدخل</b><br/>Entrance canopy", "The entrance canopy and its conditions — Article 29(c)."],
  ["<b>الشرفات في الارتداد الأمامي</b>", "Balconies of proposed buildings within the front setback in "
    "residential zones — permitted on roads of not less than <b>12 m</b>, subject to the conditions of "
    "Article 29(d), and with an undertaking not to enclose them or alter their form."]],
  [34*mm, W-34*mm])]
E += fig(20)
E += [P("Article 33 — fences, fill and decking", "h2")]
E += [dt([["Provision", "Rule"],
  ["Fence height", "From natural ground level: not more than <b>1.5 m</b> on the front side, and not more "
    "than <b>2 m</b> on the rear and side boundaries."],
  ["Fill in the setbacks", "The level of fill within the setbacks may not exceed <b>1 m</b> above natural "
    "ground level at its location."],
  ["Fill under parking", "Permitted beneath any uncovered parking space in the side setback in residential "
    "zones, and at the front boundary of the plot so as to meet the street entry level."],
  ["Exemption", "The Committee may exempt ministries, government departments, public institutions, "
    "diplomatic missions, schools and special-use buildings from the fence-height limits."],
  ["<b>Decking the setbacks</b>", "The Committee may permit roofing the setbacks, <b>each case studied on its "
    "merits on the basis of an accurate topographic plan submitted with the application</b>, provided the deck "
    "supports the street, the retaining wall or the rock-cut face, and its level is below natural ground on all "
    "sides. Front-setback decking is permitted where it supports the street, provided the deck length does not "
    "exceed the building façade length on the street, the deck level follows the adjoining street and <b>in no "
    "case exceeds 45 cm</b>, and — where the plot fronts more than one street — the deck may be on the "
    "<b>upper street side, the lower, or both</b>."],
  ["Use beneath a deck", "Restricted to the building's general services: parking and vehicle passages, water, "
    "diesel and gas wells and tanks, central heating, cooling and electrical rooms, transformer stations and "
    "non-commercial storage rooms."],
  ["<b>Exclusion</b>", "<b>The area of decks within the setbacks is excluded from the total building area AND "
    "from the floor area.</b> Ramps and suspended vehicle passages are permitted in the setbacks provided their "
    "floor level is below natural ground."],
  ["Services", "The owner must provide water collection wells — <b>discharge to the sewer network, to septic "
    "tanks, to soakaways or to neighbouring land is prohibited</b> — and sealed collection pits where no sewer "
    "network exists."]], [34*mm, W-34*mm])]
E += fig(22)
E += fig(23)
E += [P("Article 34 — the ancillary building", "h2")]
E += [dt([["Condition", "Value"],
  ["Ratio of the ancillary building", "not more than <b>5%</b> of the plot area, <b>IN ADDITION</b> to the "
   "coverage permitted under this Regulation"],
  ["Absolute area cap", "in no case more than <b>25 m²</b>"],
  ["Front setback", "to be provided per the zone's planning provisions"],
  ["External height", "not more than <b>2.60 m</b> from natural ground level"],
  ["Use", "limited to serving the main building — not a boiler room, not a generator, and nothing causing "
   "nuisance to neighbours"],
  ["Roof", "no opening leading to it, and the roof is not to be used for any purpose"],
  ["Attachment", "<b>must NOT be attached</b> to the building standing on the plot"],
  ["Industrial zones — 34(b)", "ancillary buildings in the side setbacks up to <b>5%</b> of the land area and "
   "a maximum of <b>100 m²</b>, for guarding purposes, with a front setback of not less than <b>5 m</b>"]],
  [46*mm, W-46*mm])]
E += fig(24)
E += fig(21)
E.append(PageBreak())

# ═════════════════════════════════════ 11 PARKING
E += [P("11 · Parking — Articles 36 to 40", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 36(e) — the minimum number of spaces by use", "h2")]
E += [dt([["Use", "Spaces required"],
  ["<b>المناطق السكنية (أ، ب، ج، ريفي، زراعي)</b><br/>Residential A, B, C, rural and agricultural",
   "<b>one space per 300 m² of total built area, OR one space per apartment — whichever gives the greater number</b>"],
  ["<b>المناطق السكنية (د)</b><br/>Residential D", "one space per two apartments"],
  ["Commercial areas and complexes", "one space per 100 m² of total built area, plus the spaces required for the "
   "varied uses within the complex (cafés, tourist restaurants, theatres, halls and the like) where those "
   "require additional parking — whichever is the greater number"],
  ["Professions licensed within a dwelling", "one space per profession"],
  ["Industrial, craft areas and warehouses", "one space per 200 m² of total built area, and one space per 50 m² "
   "of the offices attached to them"],
  ["Hotels", "one space per four hotel rooms, plus the parking required for the other uses including wedding "
   "and conference halls, and one space per hotel suite and per hotel apartment"],
  ["Nursing / care homes — دور العناية", "one space per 75 m² of total built area"],
  ["Nurseries and kindergartens", "one space per 100 m² of the nursery or kindergarten area"],
  ["Exhibition and conference centres, function<br/>and wedding halls, display halls", "one space per 20 m² of total built area"],
  ["Ministries, departments and public institutions", "one space per 20 m² of total built area"],
  ["Offices · social centres · research centres · veterinary clinics · health and medical centres, clinics and "
   "laboratories · banks and financial institutions · private schools and public libraries · museums and civil "
   "society institutions · emergency services", "one space per 50 m² of total built area"],
  ["Sports clubs and playing fields · universities, colleges, institutes · sports halls", "one space per 25 m² of total built area"],
  ["Hospitals", "one space per bed or incubator, in addition to one space per 100 m² of total built area"],
  ["Government schools", "one space per 100 m² of total built area"]],
  [72*mm, W-72*mm])]
E += callout("The rule that catches phased schemes",
 ["<b>Article 36(b)(1):</b> no proposed building may be licensed unless the parking required for the "
  "<b>FULL permitted building on the plot</b> has been provided — <b>regardless of the areas being licensed now</b>.",
  "<b>36(b)(2):</b> where fewer spaces are provided, the committees may licence only the areas or the number "
  "of apartments matching the spaces secured, and <b>no additional area or apartment may ever be licensed</b> "
  "beyond them.",
  "<b>36(b)(3):</b> a part of a space counts as a whole space. "
  "<b>36(b)(4):</b> the ground floor allocated to parking is <b>excluded from the prescribed height</b>, and up "
  "to <b>25%</b> of its area may be used for the building's general services. "
  "<b>36(b)(5):</b> parking areas in the semi-basement are <b>excluded from the coverage percentage</b>, "
  "structural safety being observed."], RED, colors.HexColor("#fbf0ef"))
E += [P("<b>36(a):</b> no parking is imposed on buildings on plots served only by a stair or a passage less "
        "than three metres wide, provided the building has not more than <b>8 apartments</b>. "
        "<b>36(c):</b> except in residential zones, the Committee may permit parking in the front setback, "
        "subject to the Article 37 dimensions and free manoeuvring. "
        "<b>36(d):</b> the Committee may accept uncovered parking in the side and rear setbacks on four "
        "conditions: the net width is provided; the front setback behind those bays is kept clear; the entry "
        "opening is not less than the net width; and manoeuvring is entirely within the plot.", "body")]
E += fig(25)
E += [P("Article 37 — bay and aisle dimensions", "h2")]
E += [dt([["Parking angle", "Bay length", "Bay width", "Aisle width"],
  ["الوقوف الموازي — parallel to the aisle", "5.50 m", "2.50 m", "4.00 m"],
  ["زاوية ٣٠ درجة — 30°", "5.25 m", "2.50 m", "4.00 m"],
  ["زاوية ٤٥ درجة — 45°", "5.25 m", "2.50 m", "5.00 m"],
  ["زاوية ٩٠ درجة — 90°", "5.25 m", "2.50 m", "5.50 m"]],
  [W-84*mm, 28*mm, 28*mm, 28*mm], align={1,2,3})]
E += [P("<b>37(b):</b> the average area allotted per single bay is <b>25 m²</b>, including the turning aisles "
        "and the bay itself, in and out.<br/>"
        "<b>37(c):</b> the clear parking height is <b>2.25 m</b> minimum — the vertical distance from the bay "
        "floor to the underside of the ceiling, any structural element, or any electromechanical services.", "body")]
E += fig(26)
E += [P("Articles 38 to 40", "h3")]
E += [dt([["Article", "Subject"],
  ["38", "ممرات الدخول والخروج والممرات الداخلية — entry and exit passages and internal aisles: the "
         "longitudinal section (ramp gradient), the cross-section (ramp width) and the curves."],
  ["39", "أماكن اصطفاف السيارات — the location of parking areas."],
  ["40", "المواقف الآلية — mechanical and automated parking using lifts."]], [16*mm, W-16*mm])]
E += fig(27)
E.append(PageBreak())

# ═════════════════════════════════════ 12 OUTSIDE THE PLANNING AREAS
E += [P("12 · Outside the planning areas — Articles 44 to 46", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 44(a) — residential buildings outside the planning areas", "h2")]
E += [dt([["Land area", "Front", "Side", "Rear", "Floors", "Height", "Coverage"],
  ["1,000 m² and less", "7 m", "4 m", "4 m", "2 + roof", "9 m excl. roof", "10%"],
  ["1,001 to 2,000 m²", "8 m", "5 m", "5 m", "2 + roof", "9 m excl. roof", "10%"],
  ["2,001 to 4,000 m²", "10 m", "5 m", "7 m", "2 + roof", "9 m excl. roof", "10%"],
  ["more than 4,000 m²", "15 m", "5 m", "10 m", "2 + roof", "9 m excl. roof", "10%, capped at 1,000 m²"]],
  [36*mm, 16*mm, 16*mm, 16*mm, 22*mm, 30*mm, W-136*mm], align={1,2,3,4})]
E += [P("<b>44(b):</b> a building of <b>20 m²</b> may be erected within the front setback to serve the "
        "project's purposes. It is <b>not counted</b> in the prescribed coverage percentage, provided it is "
        "removed on demand of the authorities <b>without compensation</b>.", "body")]
E += fig(28)
E += [dt([["Article", "Subject", "Substance"],
  ["45", "المنشآت الزراعية خارج مناطق التنظيم", "Licensing agricultural facilities outside the planning "
    "areas — <b>45(a)</b> animal and poultry barns; <b>45(b)</b> olive presses, with their own setbacks, "
    "coverage and approvals."],
  ["46", "معامل الطوب والبلاط ومناشير الحجر والرخام", "Brick and tile works and stone and marble sawmills — "
    "licensing conditions and the building provisions applying to them."]], [16*mm, 52*mm, W-68*mm])]
E.append(PageBreak())

# ═════════════════════════════════════ 13 MISCELLANEOUS
E += [P("13 · Miscellaneous provisions — Articles 47 and 48", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Article 47 is a long lettered article running from (a) to (s). These are the paragraphs that "
        "most often decide a case.", "body")]
E += [dt([["Para.", "Provision"],
  ["<b>(l)</b>", "<b>«لا تستعمل مناطق السكن الخاص محدود الارتفاع والسكن الأخضر والسكن الريفي والسكن الزراعي "
    "إلا للسكن ودور العبادة»</b> — Special low-rise, green, rural and agricultural residential zones may be "
    "used <b>for residential purposes and places of worship only</b>. This is a hard stop on any commercial, "
    "tourism or hospitality use in those zones."],
  ["(m)", "Properties abutting ring roads, through roads or main traffic corridors may not be used for "
    "commercial or industrial purposes without the approval of the Ministry of Public Works and Housing and "
    "of the Higher Planning Council."],
  ["(n)", "Statutory setbacks are <b>not</b> counted within the areas required to be provided as school yards."],
  ["(s)", "For-hire car parking may be licensed in all planning areas under instructions of the Council."],
  ["(v)", "Energy-generating cells may be installed on the roofs of existing buildings with the Committee's "
    "approval, provided the buildings are duly licensed and hold a valid occupancy permit."],
  ["(f)", "Hotels, hospitals, cinemas, theatres, large cold stores and warehouses, commercial complexes and any "
    "use whose nature requires continuity of electrical supply must install <b>self-starting standby generators</b>."],
  ["<b>(ṣ)</b>", "<b>«لا يجوز البناء في الأراضي الخلاء المقيدة أو الشديدة الانحدار والقابلة للانهيار أو الانزلاق "
    "والتي يتم تحديدها على المخططات التنظيمية المقررة»</b> — <b>No building</b> on restricted open land, or on "
    "land that is steeply sloping and liable to collapse or sliding, <b>where the approved planning schemes so "
    "designate it</b>."]], [14*mm, W-14*mm])]
E += fig(30)
E += [P("Article 48 — the roof floor and the surface floor", "h2")]
E += [dt([["Provision", "Rule"],
  ["<b>48(a)(1)</b>", "The roof floor's percentage may not exceed <b>50%</b> of the area of the floor on which it is built."],
  ["<b>48(a)(2)</b>", "Its height may not exceed <b>3.50 m</b> from the slab level of the floor on which it is built."],
  ["<b>48(a)(3)</b>", "Setbacks on all sides from the edge of that floor's slab of <b>not less than half</b> the "
    "setbacks prescribed for the land, <b>excluding the stair house and the lift</b>."],
  ["<b>48(b)</b>", "Notwithstanding Article 16, the Committee may approve a <b>طابق سطح</b> on the front façade "
    "above the last permitted floor, <b>in residential zones أ، ب، ج، د ONLY</b>: its area plus the stair and "
    "lift house not exceeding <b>20%</b> of the last floor; height not exceeding <b>2.75 m</b> from the last "
    "floor slab; it must belong to the last floor and connect to it by an internal stair; no openings onto the "
    "remaining roof area; and no opening left in its own roof."]], [22*mm, W-22*mm])]
E += fig(29)
E.append(PageBreak())

# ═════════════════════════════════════ 14 THE 2025 AMENDMENT
E += [P("14 · The 2025 amendment", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("<b>نظام معدّل لنظام الأبنية وتنظيم المدن والقرى رقم (١٢) لسنة ٢٠٢٥</b> — issued on the decision of "
        "the Council of Ministers of <b>29/1/2025</b>, published at Gazette pages 835–837, and <b>read as one</b> "
        "with the 2022 Regulation. In force from publication.", "body")]
E += [dt([["Amending<br/>article", "Provision of the 2022 Regulation", "Effect"],
  ["2", "Article 8(d)(8) — medium-industry areas", "Repealed and replaced. The old carve-out excluding food "
    "industries, mills and pharmaceuticals is removed and replaced by: whatever is permitted in paragraphs (a) "
    "and (c), <b>provided the necessary environmental approvals are obtained</b>."],
  ["3", "Article 10 — investment projects", "Two new paragraphs added.<br/><b>(e)</b> The provisions and "
    "conditions set by the Council for licensing <b>residential-suburb projects</b> may not be amended except "
    "with the Council's prior approval and subject to the approval of the General Assembly of the Union of "
    "Owners of Residential Suburb Projects.<br/><b>(f)</b> <b>«باستثناء مشاريع الطاقة المتجددة يجب ان لا تقل "
    "سعة الشارع الواصل لأرض المشروع عن (١٢) متراً»</b> — except renewable-energy projects, the street reaching "
    "the project land must be <b>not less than 12 m</b>."],
  ["4", "Article 41(c) — the occupancy permit", "A new item (9) added: provision of a <b>flagpole</b> "
    "(سارية علم), its specifications and dimensions to be set by instructions of the Minister."],
  ["5", "Article 52(a)", "The existing text is renumbered as item (1) and new items (2), (3) and (4) are added, "
    "creating a <b>temporary licensing amnesty</b> for buildings existing between <b>1/1/2017</b> and "
    "<b>1/12/2024</b> — subject to certified engineering drawings, a structural-safety certificate, no "
    "encroachment on third-party or Treasury land or on the road, setback encroachments within a stated "
    "percentage, and use conformity — with reduced encroachment fees and parking-substitute charges. "
    "The licensing window closes <b>1/12/2028</b>.<br/><b>⚪ The percentages and two of the dates in this "
    "article were legible only in the OCR layer and are recorded as UNCLEAR IN SOURCE pending a further "
    "visual read of Gazette pages 836–837.</b>"]],
  [18*mm, 46*mm, W-64*mm])]
E += callout("Nothing else changed",
 "Regulation No. (12) of 2025 makes <b>no amendment</b> to Articles 1 to 7, 9, or 11 of the 2022 Regulation, "
 "nor to the development control table of Article 16, the height rules of Article 15, or any fee schedule.",
 GRN, colors.HexColor("#eef7f2"))
E.append(PageBreak())

# ═════════════════════════════════════ 15 FIGURE INDEX
E += [P("15 · Figure index", "h1"), rule(INK, 1.0, 0, 8)]
E += callout("These drawings are not part of the Regulation",
 "All 32 were drawn by NORMIA to illustrate the text. The Official Gazette contains no diagrams. "
 "They have no legal force; where a drawing and the regulatory text differ, <b>the text governs</b>.",
 RED, colors.HexColor("#fbf0ef"))
rows = [["Fig.", "Illustrates", "العنوان", "Article"]]
for n in sorted(FIGS):
    f = FIGS[n]
    rows.append([f"<b>JO-Fig-{n:02d}</b>", f["en"], ar(f["ar"], False), f["art"]])
E += [dt(rows, [18*mm, W-18*mm-56*mm-26*mm, 56*mm, 26*mm], fs=7.4, pad=3.2)]
E.append(PageBreak())

# ═════════════════════════════════════ 16 BASIS
E += [P("16 · Basis, limitations and sources", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Confidence register", "h2")]
E += [dt([["Item", "Status"],
  ["Identity, enabling law, commencement, signatories", "VERIFIED — Gazette p.1 and the closing pages"],
  ["Article 2 definitions, all terms", "VERIFIED — Gazette pp. 1–4, read visually"],
  ["Article 11 subdivision tables, all seven", "VERIFIED — Gazette pp. 10–11, read visually"],
  ["Article 13(e)(1) road / plot table", "VERIFIED — Gazette p. 12, read visually"],
  ["Article 15, all paragraphs", "VERIFIED — Gazette pp. 14–15, read visually"],
  ["Article 16(a) master control table", "VERIFIED — Gazette pp. 15–16, read visually and re-checked at magnification"],
  ["Article 16(b) to (g)", "VERIFIED — Gazette p. 17, read visually"],
  ["<b>Article 19 licensing fees, every cell</b>", "<b>VERIFIED — Gazette pp. 20–21, read visually</b>"],
  ["<b>Article 20 encroachment fees, every cell</b>", "<b>VERIFIED — Gazette pp. 21–23, read visually</b>"],
  ["Articles 29, 33, 34 — projections, fences, ancillary", "VERIFIED — Gazette pp. 28–32, read visually"],
  ["Articles 36 and 37 — parking and bay dimensions", "VERIFIED — Gazette pp. 33–36, read visually"],
  ["Article 44 outside-zoning table", "VERIFIED — Gazette p. 41, read visually"],
  ["Articles 47 and 48", "VERIFIED — Gazette pp. 45–47, read visually"],
  ["The 2025 amending Regulation, Articles 1–4", "VERIFIED — Gazette pp. 835–836"],
  ["2025 amendment Article 5 — percentages and two dates", "⚪ <b>UNCLEAR IN SOURCE</b> — legible only in OCR; "
   "a further visual read of pp. 836–837 is required before these are relied on"],
  ["Article 16(f) street width and the 16/1/2018 date", "VERIFIED on the second reading of p. 17"],
  ["Swimming-pool fee, agricultural column", "Recorded as printed — the cell is <b>physically empty</b> in the "
   "Gazette, carrying neither a figure nor a dash, unlike the other blank cells"],
  ["<b>All 32 diagrams</b>", "<b>DRAWN BY NORMIA — not part of the Regulation, no legal force</b>"]],
  [W-62*mm, 62*mm])]
E += callout("Limitations — please read before relying on any figure here",
 ["This is a <b>reference presentation</b> of the Regulation, not the Regulation. Where this document and "
  "the Official Gazette differ, <b>the Gazette governs</b>.",
  "<b>The diagrams are NORMIA's own work.</b> They interpret the text; they do not extend or qualify it. "
  "The Gazette contains no diagrams of any kind.",
  "<b>Zone-specific provisions override the general tables.</b> Article 16(a) opens with «مع مراعاة أي أحكام "
  "خاصة ترد على المخططات الهيكلية أو التفصيلية» — subject to any special provisions on the structural or "
  "detailed schemes. For any real plot the governing figures come from its own zoning certificate.",
  "Fee figures are as published in 2022. <b>Verify them against the current schedule before quoting a client</b> "
  "— fees are the provision most often varied by subsequent instruments and by municipal category.",
  "Where a value could not be read with certainty it is marked UNCLEAR IN SOURCE. Nothing has been inferred, "
  "rounded or filled in."], RED, colors.HexColor("#fbf0ef"))
E += [P("Sources", "h2")]
E += [P("<b>Primary.</b> نظام الأبنية وتنظيم المدن والقرى رقم (١) لسنة ٢٠٢٢ — الجريدة الرسمية — 49 pages. "
        "نظام معدّل لنظام الأبنية وتنظيم المدن والقرى رقم (١٢) لسنة ٢٠٢٥ — الجريدة الرسمية، الصفحات ٨٣٥–٨٣٧. "
        "Enabling law: قانون تنظيم المدن والقرى والأبنية المؤقت رقم (٧٩) لسنة ١٩٦٦، المادة ٦٧.", "small")]
E += [P("<b>Method.</b> Every page of both instruments was rendered as an image and read visually at "
        "magnification. OCR was used only to locate provisions, never to read a number. The drawings were "
        "prepared from the verified text.", "small")]
E += [rule(RULE, 0.6, 10, 6),
      P("Prepared by NORMIA — AEC Regulatory Intelligence &amp; Compliance Consultant. NORMIA never invents "
        "regulations. Where information cannot be verified against an official source it is marked UNVERIFIED, "
        "and no compliant result is issued in its place.", "small")]

doc.build(E)
print("built")
