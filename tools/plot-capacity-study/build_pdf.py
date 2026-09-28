import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
"""Architect's Regulatory Capacity & Feasibility Study - PDF build."""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, PageBreak,
                                KeepTogether, HRFlowable, NextPageTemplate)
import arabic_reshaper
from bidi.algorithm import get_display
from calc import (AREA_LEGAL, cov_max, env_a_area, env_b_area, floor_area, far,
                  green_min, gf, ff, roof_max, base_legal, base_env, base_sides,
                  n_steps, band_w, env_w, env_l, DATUM, CEIL, CEIL_R,
                  S_FRONT, N_FRONT, W_SIDE, E_SIDE, apts, villas, net_saleable,
                  AREA_GEOM)

# ---------------------------------------------------------------- fonts
pdfmetrics.registerFont(TTFont("AR", "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf"))
pdfmetrics.registerFont(TTFont("ARB", "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf"))
def ar(s):  # shaped + bidi, wrapped in the Arabic face
    return f'<font name="ARB">{get_display(arabic_reshaper.reshape(s))}</font>'

# ---------------------------------------------------------------- palette
INK   = colors.HexColor("#0b0b0b"); INK2 = colors.HexColor("#3f3e3a")
INK3  = colors.HexColor("#6f6d66"); RULE = colors.HexColor("#d6d4ca")
BLUE  = colors.HexColor("#2a78d6"); ORANGE = colors.HexColor("#c2470f")
AQUA  = colors.HexColor("#0b7a55"); RED = colors.HexColor("#c0332f")
AMBER = colors.HexColor("#a06a00"); PAPER = colors.HexColor("#fcfcfb")
BOXBG = colors.HexColor("#f4f3ed"); HDRBG = colors.HexColor("#e9e7dd")

PW, PH = A4
M = 19*mm
REF = "NORMIA · JO-MKW-96-P34 · Rev A"

# ---------------------------------------------------------------- styles
def S(n, **kw):
    base = dict(name=n, fontName="Helvetica", fontSize=9, leading=13,
                textColor=INK2, alignment=TA_LEFT, spaceAfter=0)
    base.update(kw); return ParagraphStyle(**base)

st = {
 "h1":    S("h1", fontName="Helvetica-Bold", fontSize=16.5, leading=19.5,
            textColor=INK, spaceBefore=2, spaceAfter=7),
 "h2":    S("h2", fontName="Helvetica-Bold", fontSize=11.6, leading=14.5,
            textColor=INK, spaceBefore=11, spaceAfter=5),
 "h3":    S("h3", fontName="Helvetica-Bold", fontSize=9.6, leading=12.5,
            textColor=ORANGE, spaceBefore=8, spaceAfter=3),
 "body":  S("body", fontSize=9.05, leading=13.3, spaceAfter=5.5),
 "small": S("small", fontSize=7.9, leading=11.2, textColor=INK3, spaceAfter=3),
 "cap":   S("cap", fontSize=7.6, leading=10.4, textColor=INK3, spaceBefore=3, spaceAfter=7),
 "lead":  S("lead", fontSize=10.4, leading=15.2, textColor=INK, spaceAfter=7),
 "kick":  S("kick", fontName="Helvetica-Bold", fontSize=7.6, leading=10,
            textColor=ORANGE, spaceAfter=2.5),
 "tb":    S("tb", fontSize=8.1, leading=10.8, spaceAfter=0),
 "tbb":   S("tbb", fontName="Helvetica-Bold", fontSize=8.1, leading=10.8,
            textColor=INK, spaceAfter=0),
 "th":    S("th", fontName="Helvetica-Bold", fontSize=7.7, leading=9.8,
            textColor=INK, spaceAfter=0),
 "tnum":  S("tnum", fontName="Helvetica-Bold", fontSize=8.4, leading=10.8,
            textColor=INK, alignment=TA_RIGHT, spaceAfter=0),
 "cvtit": S("cvtit", fontName="Helvetica-Bold", fontSize=27, leading=31,
            textColor=INK, spaceAfter=6),
 "cvsub": S("cvsub", fontSize=12.6, leading=17.5, textColor=INK2, spaceAfter=4),
}
SUP = {"\u00b2": "<super>2</super>", "\u00b3": "<super>3</super>"}
def fx(t):
    t = str(t)
    for k, v in SUP.items(): t = t.replace(k, v)
    return t
def P(t, s="body"): return Paragraph(fx(t), st[s])

# ---------------------------------------------------------------- components
def rule(c=RULE, w=0.7, sb=4, sa=6):
    return HRFlowable(width="100%", thickness=w, color=c,
                      spaceBefore=sb, spaceAfter=sa, lineCap="butt")

def callout(title, body, accent=ORANGE, bg=BOXBG):
    inner = [Paragraph(fx(title), S("ct", fontName="Helvetica-Bold", fontSize=8.7,
                                leading=11.4, textColor=accent, spaceAfter=3))]
    for b in ([body] if isinstance(body, str) else body):
        inner.append(Paragraph(fx(b), S("cb", fontSize=8.6, leading=12.2, spaceAfter=3)))
    t = Table([[inner]], colWidths=[PW-2*M])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LINEBEFORE", (0,0), (0,-1), 2.4, accent),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP")]))
    return [Spacer(1, 4), t, Spacer(1, 7)]

def dtable(rows, widths, align=None, hdr=True, fs=8.1, pad=4.6):
    data = []
    for i, r in enumerate(rows):
        row = []
        for j, c in enumerate(r):
            if isinstance(c, Paragraph): row.append(c)
            else:
                sty = "th" if (hdr and i == 0) else "tb"
                if align and j in align and not (hdr and i == 0): sty = "tnum"
                row.append(Paragraph(fx(c), st[sty]))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=1 if hdr else 0)
    cmds = [("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("TOPPADDING", (0,0), (-1,-1), pad), ("BOTTOMPADDING", (0,0), (-1,-1), pad),
            ("LINEBELOW", (0,0), (-1,-2), 0.4, RULE)]
    if hdr:
        cmds += [("BACKGROUND", (0,0), (-1,0), HDRBG),
                 ("LINEBELOW", (0,0), (-1,0), 0.9, INK3)]
    else:
        cmds += [("BACKGROUND", (0,0), (-1,-1), colors.white)]
    t.setStyle(TableStyle(cmds))
    return t

def fig(path, w, cap=None):
    from PIL import Image as PImage
    iw, ih = PImage.open(path).size
    out = [Spacer(1, 3), Image(path, width=w, height=w*ih/iw)]
    if cap: out.append(P(cap, "cap"))
    else: out.append(Spacer(1, 6))
    return out

def hero(items):
    """Big-number row."""
    cells = []
    for val, lab, col in items:
        cells.append([Paragraph(fx(val), S("hv", fontName="Helvetica-Bold", fontSize=19.5,
                                       leading=22, textColor=col, alignment=TA_CENTER)),
                      Paragraph(fx(lab), S("hl", fontSize=7.5, leading=9.8, textColor=INK3,
                                       alignment=TA_CENTER))])
    inner = [Table([[c[0]] , [c[1]]], colWidths=[(PW-2*M)/len(items)-4]) for c in cells]
    for t in inner:
        t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),2),
                               ("BOTTOMPADDING",(0,0),(-1,-1),2),
                               ("LEFTPADDING",(0,0),(-1,-1),1),
                               ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    outer = Table([inner], colWidths=[(PW-2*M)/len(items)]*len(items))
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BOXBG),
        ("LINEABOVE", (0,0), (-1,0), 1.4, INK),
        ("LINEBELOW", (0,-1), (-1,-1), 0.6, RULE),
        ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE")]))
    return [Spacer(1,3), outer, Spacer(1,9)]

# ---------------------------------------------------------------- page furniture
def page_chrome(canv, doc):
    canv.saveState()
    canv.setFillColor(PAPER); canv.rect(0, 0, PW, PH, stroke=0, fill=1)
    if doc.page > 1:
        canv.setStrokeColor(RULE); canv.setLineWidth(0.6)
        canv.line(M, PH-14*mm, PW-M, PH-14*mm)
        canv.setFont("Helvetica", 7); canv.setFillColor(INK3)
        canv.drawString(M, PH-12.4*mm, "Plot 3 + 4 combined · Parcel 96 · Al-Zara North (7) · Makawir · Dhiban · Madaba")
        canv.drawRightString(PW-M, PH-12.4*mm, "Architect's Regulatory Capacity Study")
        canv.line(M, 13.5*mm, PW-M, 13.5*mm)
        canv.setFont("Helvetica", 6.8)
        canv.drawString(M, 10.6*mm, REF)
        canv.drawCentredString(PW/2, 10.6*mm,
            "Basis: Green / Rural Residential — ASSUMED, not certified")
        canv.setFont("Helvetica-Bold", 7.6); canv.setFillColor(INK2)
        canv.drawRightString(PW-M, 10.5*mm, str(doc.page))
    canv.restoreState()

def cover_chrome(canv, doc):
    canv.saveState()
    canv.setFillColor(PAPER); canv.rect(0, 0, PW, PH, stroke=0, fill=1)
    canv.setFillColor(colors.HexColor("#e9e7dd")); canv.rect(0, PH-30*mm, PW, 30*mm, stroke=0, fill=1)
    canv.setFillColor(ORANGE); canv.rect(0, PH-30*mm, PW, 2.4*mm, stroke=0, fill=1)
    canv.setStrokeColor(RULE); canv.setLineWidth(0.6); canv.line(M, 20*mm, PW-M, 20*mm)
    canv.setFont("Helvetica", 7.2); canv.setFillColor(INK3)
    canv.drawString(M, 16*mm, REF)
    canv.drawRightString(PW-M, 16*mm, "Prepared by NORMIA — AEC Regulatory Intelligence")
    canv.restoreState()

doc = BaseDocTemplate(HERE + "/NORMIA_Plot3+4_Capacity_Study.pdf",
                      pagesize=A4, leftMargin=M, rightMargin=M,
                      topMargin=20*mm, bottomMargin=18*mm,
                      title="Plot 3+4 Combined — Architect's Regulatory Capacity Study",
                      author="NORMIA", subject="Parcel 96, Al-Zara North, Makawir, Jordan")
fr  = Frame(M, 18*mm, PW-2*M, PH-38*mm, id="n", showBoundary=0)
frc = Frame(M, 24*mm, PW-2*M, PH-58*mm, id="c", showBoundary=0)
doc.addPageTemplates([PageTemplate(id="cover", frames=[frc], onPage=cover_chrome),
                      PageTemplate(id="body",  frames=[fr],  onPage=page_chrome)])

E = []
W = PW - 2*M

# ================================================================= COVER
E += [Spacer(1, 14*mm),
      P("ARCHITECT'S REGULATORY CAPACITY &amp; FEASIBILITY STUDY", "kick"),
      P("Plot 3 + 4 Combined", "cvtit"),
      P("4,000 m² · Parcel 96 · Basin Al-Zara North (7) · Makawir<br/>"
        "Dhiban District · Madaba Governorate · Hashemite Kingdom of Jordan", "cvsub"),
      Spacer(1, 4*mm), rule(INK, 1.2, 0, 8)]
E += hero([(f"{cov_max:,.0f} m²", "MAX FOOTPRINT  ·  27% coverage", ORANGE),
           (f"{floor_area:,.0f} m²", "TOTAL FLOOR AREA  ·  2 floors + roof", BLUE),
           ("2 + roof", "STOREYS  ·  9 m height limit", AQUA),
           (f"{far:.3f}", "FLOOR AREA RATIO", INK)])
E += [Spacer(1, 3*mm),
      P("This study answers one question — <b>how much can be built on the combined plot, "
        "and in what form</b> — and then says plainly what stands in the way. It is written "
        "from the drawings and the survey you supplied, and from the verified text of "
        "<b>Building and Town &amp; Village Planning Regulation No. (1) of 2022</b>.", "lead")]
E += callout("⚠  THE STUDY RESTS ON ONE UNCERTIFIED ASSUMPTION",
  ["Every number above assumes the land is zoned <b>" + ar("السكن الأخضر / الريفي") +
   " — Green / Rural Residential</b>. That is the best reading of the evidence, "
   "but <b>no document in the file states the zoning class</b> and Jordan publishes no "
   "register from which it can be read.",
   "If the certificate returns a different class the footprint moves by a factor of up to "
   "2.7×. <b>Obtain the " + ar("كشف أحكام تنظيمية") + " from the Dhiban Directorate of "
   "Municipal Affairs before committing to any design.</b>"], RED,
  colors.HexColor("#fbf0ef"))
E += [Spacer(1, 2*mm),
      P("Contents — 1 Executive summary · 2 The site · 3 Planning envelope · "
        "4 What you can occupy · 5 Height, levels and the ceiling · 6 Total exploitable "
        "area · 7 Design strategy · 8 Yield and parking · 9 Constraints and challenges · "
        "10 Approvals roadmap · 11 Compliance schedule · 12 Basis, limitations and sources",
        "small")]
E += [NextPageTemplate("body"), PageBreak()]

# ================================================================= 1 EXEC
E += [P("1 · Executive summary", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("<b>The combined plot gives you 1,080 m² of footprint and 2,700 m² of countable "
        "floor area over two storeys and a roof floor.</b> Combining plots 3 and 4 was "
        "worth doing — but not for the reason owners usually expect. It buys you a single "
        "well-proportioned development parcel and the freedom to place the building on the "
        "half of the site that can actually take it. <b>It buys you no additional height "
        "whatsoever.</b>", "body"),
      P("Two findings govern everything that follows.", "body")]
E += callout("FINDING 1 — the height bonus for a bigger plot does not apply here",
  ["Article 16(" + "c" + ") normally grants <b>+35 cm of height for every 100 m² above the "
   "minimum subdivision area</b>. On a 2,000 m² minimum that would read as a 2,000 m² "
   "surplus and <b>+7.00 m</b> — and it is exactly the kind of number that gets designed against.",
   "Article 16(" + "e" + ") disapplies paragraphs (b), (c) and (d) for <b>plots served by "
   "roads narrower than 20 m</b>. This plot is served by a 6 m road and a 10 m street. "
   "No height bonus, no high-building table, no additional floor under 16(" + "f" + ") "
   "either, which needs a 14 m street. <b>This holds whatever the zoning class turns out to be.</b>"], RED,
  colors.HexColor("#fbf0ef"))
E += callout("FINDING 2 — the topography, not the coverage, is the design problem",
  ["The site falls about <b>15 m across its 47 m width — roughly 25%, one in four</b> — and it "
   "falls east to west, across the short dimension, with <b>no road on either the high or the "
   "low side</b>. Measured from the 10 m street the 9 m limit becomes a <b>flat ceiling at "
   "roughly +15.0</b>, and the natural ground at the north-east corner is <b>already at +15.0</b>.",
   "So the height available above natural ground runs from 15 m at the south-west corner to "
   "<b>zero at the north-east corner</b>. A conventional block on the upper half of this plot "
   "cannot be built. The scheme has to step."], AMBER,
  colors.HexColor("#fcf6e8"))
E += [P("And one asset that is easy to miss:", "body")]
E += callout("THE SLOPE FALLS TOWARD THE VIEW",
  ["The ground falls <b>west — straight toward the Dead Sea, 2.0 km away</b>. The site's "
   "topographic problem and its commercial asset are the same feature. A terraced scheme "
   "stepping down westward gives <b>every unit an unobstructed sea view over the roof of the "
   "one below</b>, and the regulation pushes you in precisely that direction: you are given "
   "1,080 m² of footprint inside a 2,420 m² envelope and forbidden to go up. "
   "<b>Spread out, step down, face west.</b>"], AQUA, colors.HexColor("#eef7f2"))

E += [PageBreak(), P("The headline schedule", "h2")]
E += [dtable([
  ["Measure", "Value", "Control"],
  ["Plot area (registered)", f"{AREA_LEGAL:,.0f} m²", "Approved area schedule, stamped 25/4/2026"],
  ["Buildable envelope after setbacks", f"{env_a_area:,.0f} m²", "8 m front (both streets) / 6 m sides"],
  ["<b>Maximum footprint</b>", f"<b>{cov_max:,.0f} m²</b>", "Art. 16(" + "a" + ") — coverage 27%"],
  ["Envelope actually used", f"{cov_max/env_a_area*100:.0f}%", "coverage binds, not geometry"],
  ["Ground floor", f"{gf:,.0f} m²", "at full coverage"],
  ["First floor", f"{ff:,.0f} m²", "at full coverage"],
  ["Roof floor (" + ar("الروف") + ")", f"{roof_max:,.0f} m²", "Art. 48(" + "a" + ") — ≤ 50% of the floor below"],
  ["<b>Total countable floor area</b>", f"<b>{floor_area:,.0f} m²</b>", ar("المساحة الطابقية")],
  ["Floor area ratio", f"{far:.3f}", "derived"],
  ["Basement — terraced, not habitable", f"≈ {base_env:,.0f} m²", "excluded from coverage AND floor area"],
  ["<b>Total constructed area</b>", f"<b>≈ {floor_area+base_env:,.0f} m²</b>", "including the basement"],
  ["Minimum landscaped area", f"{green_min:,.0f} m²", "Art. 16(" + "a" + ") — 10%"],
  ["Storeys", "2 + roof floor", "Art. 16(" + "a" + ")"],
  ["Height limit", "9.00 m excluding the roof floor", "Art. 16(" + "a" + ")"],
], [58*mm, 34*mm, W-92*mm], align={1})]
E.append(PageBreak())

# ================================================================= 2 SITE
E += [P("2 · The site", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("The plot is the western pair of a four-plot subdivision of parcel 96, merged into "
        "a single 4,000 m² holding. It is a long north–south trapezoid with a street at each "
        "end and private land along both flanks.", "body")]
E += fig(HERE + "/fig_site.png", W*0.90,
         "Site plan — dimensions as printed on the approved subdivision plan; spot levels read "
         "from the topographic survey of 13-6-2026 (local datum). The eight rectangles are "
         "indicative only: they show what 27% coverage looks like distributed as terraced units, "
         "not a proposal. Schematic — not a survey drawing.")
E.append(PageBreak())

E += [P("Geometry and boundaries", "h2")]
E += [dtable([
  ["Boundary", "Length", "Abuts", "Consequence"],
  ["North", f"{N_FRONT:.2f} m", ar("طريق 6 متر") + " — 6 m road",
   "Front setback. Under 8 m, so <b>excluded from the height datum</b> (Art. 15(" + "a" + ")(1))."],
  ["South", f"{S_FRONT:.2f} m", ar("شارع 10 متر") + " — 10 m street",
   "Front setback. <b>The sole road that sets the height datum.</b>"],
  ["West", f"{W_SIDE:.2f} m", "Parcel 321 — private",
   "Side setback. The <b>low</b> side and the <b>view</b> side."],
  ["East", f"{E_SIDE:.2f} m", "Plots 1 &amp; 2 — private",
   "Side setback. The <b>high</b> side, where the ceiling bites."],
], [17*mm, 19*mm, 40*mm, W-76*mm])]
E += [P("Verification — the coordinate schedule on the plan shoelaces to 9,236.03 m² against "
        "the printed total of 9,236.720 m², an agreement of 0.007%. Re-drawing the merged plot "
        "from its four printed dimensions returns " + f"{AREA_GEOM:,.0f} m²" + " against the "
        "scheduled 4,000 m². <b>The plan is internally consistent and the geometry can be relied on.</b>", "small")]

E += [P("Position, elevation and setting", "h2")]
E += [dtable([
  ["Item", "Value", "Note"],
  ["Position", "31.5995° N   35.5659° E", "Palestine Grid (Cassini) → WGS84, from the plan's own coordinates"],
  ["Elevation", "−226 m to −361 m", "SRTM 30 m, sampled across the parcel — below sea level"],
  ["Dead Sea shore", "≈ 2.0 km west", "the downhill direction"],
  ["Zarqa Ma'in springs", "≈ 2.4 km", ""],
  ["Machaerus / " + ar("قلعة مكاور"), "≈ 6.6 km", "archaeological setting — see §9"],
  ["Statutory status", "inside the Jordan Valley", "Jordan Valley Development Law — hence the JVA seal"],
], [33*mm, 38*mm, W-71*mm])]
E += [P("The independent elevation model shows a fall of the same order and direction as the "
        "surveyor's contours. <b>The 25% gradient is corroborated, not merely asserted.</b>", "small")]
E.append(PageBreak())

# ================================================================= 3 ENVELOPE
E += [P("3 · The planning envelope", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Setbacks for Green / Rural Residential are <b>8 m front, 6 m side, 6 m rear</b>. "
        "Because the plot fronts a street at each end, the conservative reading — and the one "
        "this study adopts — is that <b>both ends take the 8 m front setback</b> and the two "
        "private flanks take 6 m.", "body")]
E += [dtable([
  ["Case", "Setbacks applied", "Envelope", "Footprint permitted", "Envelope used"],
  ["<b>A — adopted</b><br/>both streets treated as front",
   "8 / 6 / 6 / 8", f"<b>{env_a_area:,.0f} m²</b>", f"{cov_max:,.0f} m²", f"{cov_max/env_a_area*100:.0f}%"],
  ["B — upside<br/>6 m road treated as rear",
   "8 / 6 / 6 / 6", f"{env_b_area:,.0f} m²", f"{cov_max:,.0f} m²", f"{cov_max/env_b_area*100:.0f}%"],
], [40*mm, 26*mm, 24*mm, 28*mm, W-118*mm])]
E += callout("The coverage cap binds — the geometry does not",
  ["The envelope is roughly <b>68 m × 36 m ≈ " + f"{env_a_area:,.0f}" + " m²</b>, but you may "
   "only cover <b>1,080 m²</b> of it. You are therefore using <b>"
   f"{cov_max/env_a_area*100:.0f}%</b> of the room you have.",
   "On a flat site that would be a constraint. <b>On a 25% slope it is a gift</b> — it is exactly "
   "the latitude a terraced scheme needs to spread along the contours instead of cutting across "
   "them. Which of case A or B applies changes the envelope by 3% and changes nothing you can build.",
   "<b>Confirm case A with the Committee in writing</b> — it is a question of practice, not of text."],
  BLUE, colors.HexColor("#eef4fc"))
E += [P("If more footprint is needed — Article 16(" + "g" + ")", "h3"),
      P("The Council may approve a building <b>without being bound by the coverage percentage</b>, "
        "provided complete plans for the whole building are submitted and the floor-area ratio and "
        "setbacks are respected. On a steep site this is worth pursuing: it lets you trade height "
        "you cannot use for footprint you can, which is the right trade here. Treat it as an "
        "application to be argued, not an entitlement.", "body")]
E.append(PageBreak())

# ================================================================= 4 OCCUPY
E += [P("4 · What you can occupy", "h1"), rule(INK, 1.0, 0, 8)]
E += fig(HERE + "/fig_cascade.png", W,
         "From title to buildable: the setbacks take 40% of the plot, and the coverage rule then "
         "limits you to 27% of the title area — under half the envelope the setbacks left.")
E += [P("Area schedule", "h2")]
E += [dtable([
  ["Component", "Area", "Counts toward<br/>coverage", "Counts toward<br/>floor area", "Authority"],
  ["Ground floor", f"{gf:,.0f} m²", "Yes", "Yes", "Art. 16(" + "a" + ")"],
  ["First floor", f"{ff:,.0f} m²", "—", "Yes", "Art. 16(" + "a" + ")"],
  ["Roof floor " + ar("الروف"), f"{roof_max:,.0f} m²", "—", "Yes", "Art. 48(" + "a" + ")"],
  ["<b>Countable total</b>", f"<b>{floor_area:,.0f} m²</b>", "", "", ar("المساحة الطابقية")],
  ["Basement " + ar("قبو"), f"≈ {base_env:,.0f} m²", "<b>No</b>", "<b>No</b>", "Art. 2 definitions"],
  ["Parking", "as designed", "<b>No</b>", "<b>No</b>", "Art. 2 / 36(" + "b" + ")(5)"],
  ["Setback decks", "as designed", "—", "<b>No</b>", "Art. 33(" + "d" + ")(5)"],
  ["Mechanical services floor", "as designed", "—", "—", "Art. 15(" + "e" + ") — outside height &amp; floor count"],
  ["Ancillary building", "≤ 25 m²", "<b>No — additional</b>", "—", "Art. 34(" + "a" + ")"],
  ["Landscaped area (minimum)", f"{green_min:,.0f} m²", "—", "—", "Art. 16(" + "a" + ") — 10%"],
], [38*mm, 22*mm, 22*mm, 22*mm, W-104*mm], align={1})]
E += [P("The exclusions are where the real capacity of this site sits. A "
        + ar("قبو") + " is by definition below natural ground on every side, may occupy "
        "<b>the entire plot except the front setback</b>, and is excluded from both the coverage "
        "percentage and the floor area. On a plot with 15 m of fall that is a very large volume "
        "of free space — provided it is detailed as a basement and not as a semi-basement. §6 "
        "quantifies it.", "body")]
E.append(PageBreak())

# ================================================================= 5 HEIGHT
E += [P("5 · Height, levels and the ceiling", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("This is the part of the study that most changes what can be drawn.", "body")]
E += [P("How the datum is established", "h3"),
      P("Article 15(" + "a" + ")(1) measures height from the <b>average of the levels of the "
        "adjoining roads</b>, and expressly <b>disregards roads narrower than 8 m</b>. "
        "The 6 m road on the north therefore drops out. The 10 m street on the south survives — "
        "the plot fronts 100% of that side — and Article 15(" + "f" + ") then requires its "
        "<b>average</b> level to be used where the road itself has several levels, which this one "
        "certainly does: it runs from about 0.0 at its western end to about 12.0 at its eastern end.", "body")]
E += [dtable([
  ["Step", "Value", "Authority"],
  ["Height datum (average of the 10 m street)", f"≈ +{DATUM:.1f}", "Art. 15(" + "a" + ")(1) and 15(" + "f" + ")"],
  ["Permitted height", "9.00 m", "Art. 16(" + "a" + ")"],
  ["<b>Ceiling — structural top of the 2nd floor</b>", f"<b>≈ +{CEIL:.1f}</b>", "derived"],
  ["Roof floor above that", "+3.50 m", "Art. 48(" + "a" + ")(2)"],
  ["Top of roof floor", f"≈ +{CEIL_R:.1f}", "outside the 9 m"],
], [62*mm, 28*mm, W-90*mm], align={1})]
E += fig(HERE + "/fig_section.png", W,
         "Section across the slope, west (low) to east (high). The 9 m limit is a horizontal line "
         "at ≈ +15.0 while the ground climbs to meet it. Terracing is not a stylistic choice here — "
         "it is the only way to keep two storeys and a roof floor under that line across the plot.")
E.append(PageBreak())

E += [P("What the ceiling means corner by corner", "h2")]
E += [dtable([
  ["Corner", "Natural ground", "Ceiling", "Height available", "What binds"],
  ["SW — 10 m street, west end", "≈ 0.0", f"+{CEIL:.1f}", "15.0 m", "the <b>storey count</b>, not height"],
  ["NW — 6 m road, west end", "≈ +4.5", f"+{CEIL:.1f}", "10.5 m", "the storey count"],
  ["SE — east flank, south end", "≈ +12.0", f"+{CEIL:.1f}", "<b>3.0 m</b>", "the <b>ceiling</b>"],
  ["NE — 6 m road, east end", "≈ +15.0", f"+{CEIL:.1f}", "<b>0.0 m</b>", "<b>unbuildable as measured</b>"],
], [42*mm, 24*mm, 18*mm, 24*mm, W-108*mm], align={1,2,3})]
E += callout("The binding constraint flips across the plot",
  ["On the <b>western half</b> you run out of storeys before you run out of height — there is "
   "roughly 6 m of unused headroom under the ceiling.",
   "On the <b>eastern half</b> the ceiling arrives first, and at the north-east corner it has "
   "already arrived. <b>Measured from the street datum, you cannot put a building there at all.</b>"],
  RED, colors.HexColor("#fbf0ef"))

E += [P("The three reliefs that make the upper half buildable", "h2")]
E += [P("These are in the regulation. None is discretionary invention; each has a price.", "small")]
E += [dtable([
  ["Relief", "What it gives", "What it costs"],
  ["<b>Art. 15(" + "c" + ")</b> — measure from natural ground where natural ground is above road level",
   "Height taken from <b>local natural ground</b> instead of the street datum. <b>And the first "
   "floor may be used for parking or services and is excluded from both the height and the storey count.</b>",
   "The building may contain <b>no " + ar("طابق تسوية") + " (semi-basement)</b> anywhere."],
  ["<b>Art. 36(" + "b" + ")(4)</b> — ground floor as parking",
   "The ground floor given over to parking is <b>excluded from the permitted height</b>; up to "
   "25% of it may be building services.",
   "That floor is parking, not saleable area."],
  ["<b>Art. 33(" + "d" + ")</b> — deck the setbacks",
   "Decks over the setbacks supporting the street, retaining wall or rock cut. <b>Excluded from "
   "total built area and from floor area.</b> Where a plot fronts more than one street the deck "
   "may be on the <b>upper street side, the lower, or both</b>.",
   "Deck level must follow the adjoining street and in no case exceed 45 cm; use beneath is "
   "restricted to parking and services; an accurate topographic plan must accompany the application."],
], [40*mm, 62*mm, W-102*mm])]
E += callout("The design move that unlocks the site",
  ["Article 15(" + "c" + ") forfeits the <b>" + ar("تسوية") + " (semi-basement)</b> — but a "
   "<b>" + ar("قبو") + " (true basement)</b> is a different creature under the Article 2 "
   "definitions and is <b>not</b> forfeited.",
   "So: <b>bury the uphill side as a " + ar("قبو") + ", never as a " + ar("تسوية") + ".</b> "
   "The " + ar("قبو") + " is excluded from coverage and from floor area, may run to the plot "
   "boundary except in the front setback, carries the parking and the plant — and leaves "
   "Article 15(" + "c" + ") intact so the storeys above can be measured from natural ground.",
   "Detail it to the <b>45 cm</b> test (concrete surface no more than 45 cm above natural ground "
   "or the average road level, whichever is lower) and it is a " + ar("قبو") + ". Let it drift to "
   "<b>1.5 m</b> above the average road level and it becomes a " + ar("تسوية") + " — and the "
   "relief is gone. <b>That 45 cm is the single most valuable dimension on this project.</b>"],
  AQUA, colors.HexColor("#eef7f2"))
E.append(PageBreak())

# ================================================================= 6 EXPLOITABLE
E += [P("6 · Total exploitable area", "h1"), rule(INK, 1.0, 0, 8)]
E += fig(HERE + "/fig_stack.png", W,
         "The countable stack is 2,700 m². The basement sits outside both ratios entirely.")
E += [P("The basement — how much is actually achievable", "h2")]
E += [P("The legal allowance and the buildable reality are different numbers, and it is worth "
        "being honest about the gap.", "body")]
E += [dtable([
  ["", "Area", "Basis"],
  ["Legal maximum footprint of a " + ar("قبو"), f"≈ {base_legal:,.0f} m²",
   "whole plot less the two front setbacks (Art. 2 definition)"],
  ["Achievable within the building envelope",
   f"≈ {base_env:,.0f} m²",
   f"{env_w:.0f} m × {env_l:.0f} m, delivered as <b>{n_steps} terraced steps</b> of ≈ {band_w:.0f} m"],
  ["Further area available under the side setbacks", f"≈ {base_sides:,.0f} m²",
   "a " + ar("قبو") + " may occupy the side and rear setbacks"],
], [56*mm, 24*mm, W-80*mm], align={1})]
E += [P("Why it has to be terraced — a single buried level can only span the band over which the "
        "ground falls less than one floor-to-floor height. At a 3.0 m structural height and a 25% "
        f"gradient that band is <b>{band_w:.0f} m wide</b>. Across a {env_w:.0f} m envelope you "
        f"therefore need <b>{n_steps} stepped levels</b>, each following a contour band, to stay "
        "within the 45 cm test along its whole perimeter. Anything drawn as one flat basement slab "
        "across the full width will fail the definition and be reclassified as a "
        + ar("تسوية") + ".", "body")]
E += [P("Total constructed area", "h2")]
E += [dtable([
  ["", "Area", "Character"],
  ["Countable floor area (" + ar("المساحة الطابقية") + ")", f"{floor_area:,.0f} m²", "<b>habitable / saleable</b>"],
  ["Net of circulation and cores at 12%", f"≈ {net_saleable:,.0f} m²", "indicative net saleable"],
  ["Terraced basement", f"≈ {base_env:,.0f} m²", "parking, tanks, plant, storage — <b>not habitable</b>"],
  ["<b>Total constructed</b>", f"<b>≈ {floor_area+base_env:,.0f} m²</b>", ""],
], [64*mm, 26*mm, W-90*mm], align={1})]
E += callout("Read the basement correctly",
  ["Article 38(" + "a" + ") restricts the " + ar("قبو") + " to <b>parking, reinforced-concrete "
   "water tanks, storage, heating and cooling plant with fuel tanks, and electrical rooms</b>. "
   "<b>It cannot be habitable and cannot be sold as accommodation.</b>",
   "Its value is indirect and considerable: it absorbs all the parking and all the plant, which "
   "frees the whole of the 2,700 m² above ground for saleable area, and it does so without "
   "consuming a square metre of either ratio."],
  AMBER, colors.HexColor("#fcf6e8"))
E.append(PageBreak())

# ================================================================= 7 STRATEGY
E += [P("7 · Design strategy", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("What the regulation and the ground are jointly telling you to do.", "lead")]
E += fig(HERE + "/fig_strategy.png", W,
         "Three responses to the same section. Only the third survives both the height ceiling "
         "and the 1 m cap on fill within the setbacks.")
E += [P("The eight moves", "h2")]
moves = [
 ("Put the mass on the lower, western half.",
  "That is where the ceiling at ≈ +15.0 leaves real headroom and where the storey count, not the "
  "height, is what limits you. The upper third of the plot is better as landscape, parking deck "
  "and the 400 m² of green area you owe anyway."),
 ("Run the building north–south and step it east–west.",
  "The contours run north–south; the fall runs east–west. A long, narrow, stepped form parallel "
  "to the contours works with the site. A compact block across them fights it and loses."),
 ("Take the coverage, not the height.",
  "You are permitted 1,080 m² of footprint inside a 2,420 m² envelope and forbidden to go up. "
  "Spread out. If the scheme wants more footprint, Article 16(" + "g" + ") is the route — full "
  "plans, floor-area ratio and setbacks respected."),
 ("Bury the uphill side as a " + ar("قبو") + ", never as a " + ar("تسوية") + ".",
  "Excluded from coverage and floor area, may run to the boundary except in the front setback, and "
  "preserves the Article 15(" + "c" + ") relief. The 45 cm test governs the detail."),
 ("Where mass must go on the upper half, take Article 15(" + "c" + ") there.",
  "Measure from natural ground and use the first floor for parking and services so it drops out of "
  "both the height and the storey count. This is what converts the eastern half from unbuildable "
  "to buildable."),
 ("Build as several buildings, not one.",
  "Article 15(" + "a" + ")(3) computes each building's height from the <b>nearest</b> road where "
  "a plot fronts more than one road and carries more than one building. On a 15 m fall a terraced "
  "villa scheme can have each unit read the ground it stands on. <b>This is the strongest structural "
  "argument for villas over a single apartment block here.</b>"),
 ("Deck the setbacks at both street ends.",
  "Article 33(" + "d" + ") recovers usable service area that counts against neither ratio, and "
  "handles the level change at the street edge within the 45 cm rule — rather than filling, which "
  "is capped at 1 m."),
 ("Orient everything west.",
  "The fall, the view and the Dead Sea are the same direction. Step the terraces so each unit "
  "looks out over the roof of the one below — then shade that west elevation properly (see §9)."),
]
for i, (t, b) in enumerate(moves, 1):
    E += [Paragraph(fx(f"<b>{i}. {t}</b><br/>{b}"),
                    S(f"mv{i}", fontSize=8.8, leading=12.6, spaceAfter=6.5))]
E.append(PageBreak())

# ================================================================= 8 YIELD
E += [P("8 · Yield and parking", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Brief: <b>multiple villas or apartments for sale or rent</b>. The Green / Rural zone "
        "permits this — Article 47(" + "l" + ") restricts these zones to <b>residential use and "
        "places of worship</b>, and multi-unit residential sits squarely inside that. "
        "<b>Tourism, chalets, hospitality and retail do not.</b>", "body")]
E += [P("Option A — apartments", "h3")]
E += [dtable([["Gross area per apartment", "Units", "Parking required", "Basis"]] +
  [[f"{a['unit_gross']} m²", f"<b>{a['units']}</b>", f"{a['parking']}",
    "1 per apartment (exceeds the area rate)"] for a in apts],
  [44*mm, 20*mm, 28*mm, W-92*mm], align={1,2})]
E += [P("On 2,700 m² of countable floor area, less roughly 12% for cores and circulation, "
        f"about {net_saleable:,.0f} m² is net saleable.", "small")]
E += [P("Option B — villas", "h3")]
E += [dtable([["Villas", "Footprint each", "Gross each<br/>(2 floors + roof)", "Parking required", "Comment"]] +
  [[f"<b>{v['units']}</b>", f"{v['footprint']:,.0f} m²", f"{v['gross_each']:,.0f} m²", f"{v['parking']}",
    c] for v, c in zip(villas, [
      "generous; best terracing rhythm",
      "the balanced option — ≈13 m × 10.4 m plates",
      "tighter plates, more repetition",
      "plates get narrow for a 2-storey villa"])],
  [16*mm, 26*mm, 30*mm, 26*mm, W-98*mm], align={0,1,2,3})]
E += callout("Parking — the rule that catches phased schemes",
  ["Rate for residential zones including " + ar("ريفي") + ": <b>one space per 300 m² of total built "
   "area, or one space per apartment — whichever gives the greater number.</b> Above nine units the "
   "per-unit rate always governs here.",
   "<b>Article 36(" + "b" + ")(1): no building may be licensed unless the parking for the FULL "
   "permitted building on the plot has been provided — regardless of how much you are licensing "
   "now.</b> Under 36(" + "b" + ")(2), if you provide fewer spaces the Committee may licence "
   "only the matching area or unit count, and <b>no further area may ever be licensed</b>. "
   "Design the parking for the whole entitlement on day one even if you build in phases.",
   "Article 36(" + "c" + "): <b>parking is not permitted in the front setback in residential "
   "zones.</b> Article 36(" + "d" + ") does allow open parking in the side and rear setbacks, "
   "subject to clear width, manoeuvring within the plot, and the front setback being kept clear."],
  BLUE, colors.HexColor("#eef4fc"))
E += [P("<b>Recommendation.</b> On this section, <b>8 terraced villas</b> is the strongest fit. It "
        "keeps plates at a workable ≈13 m × 10.4 m, gives a terracing rhythm that suits a 25% "
        "gradient, opens Article 15(" + "a" + ")(3) so each unit takes its height from the "
        "ground it stands on, needs only 9 parking spaces, and puts every unit on the west "
        "elevation with a sea view. An apartment block of 15–18 units yields the same floor area "
        "but concentrates it into one mass that has to solve the whole 15 m of fall in a single "
        "building — and it needs 15–18 spaces instead of 9.", "body")]
E.append(PageBreak())

# ================================================================= 9 CONSTRAINTS
E += [P("9 · Constraints and challenges", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Set out in order of how badly each can hurt the project. Severity is NORMIA's "
        "assessment; the authority column is verified.", "lead")]

CON = [
 ("CRITICAL", RED, "Zoning class is not established",
  "No document in the file states the " + ar("فئة المنطقة") + ", and Jordan publishes no register "
  "from which it can be read. If the land proves to be outside the zoning boundary, Article 44 "
  "applies instead and coverage drops from 27% to <b>10% — 400 m² instead of 1,080 m²</b>.",
  "Request the " + ar("كشف أحكام تنظيمية") + " from the Dhiban Directorate before any design spend. "
  "Nothing in this study is safe until it is in hand."),
 ("CRITICAL", RED, "The merger is not yet final",
  "The stamped plan carries only a <i>no objection to proceed <b>after</b> the Committee's approval "
  "and payment of the legal fees</i>, dated 25/4/2026. Until the merger is registered these remain "
  "<b>two separate 2,000 m² parcels</b> and no single building may be licensed across both.",
  "Complete the Committee approval, pay the fees and register the new title. Also resolve why a "
  "four-plot print is dated 15/6/2026, after the merged version was endorsed."),
 ("CRITICAL", RED, "The height ceiling collides with natural ground on the east",
  "Measured from the 10 m street the 9 m limit is a flat line at ≈ +15.0, and the north-east corner "
  "of the plot is already at +15.0. <b>Roughly the eastern third cannot carry a building measured "
  "the conventional way.</b>",
  "Design the scheme terraced on the western half; take Article 15(" + "c" + ") on any mass "
  "above the datum; put a written question to the Committee on the datum before design freeze."),
 ("HIGH", AMBER, "The datum question is unresolved and worth metres",
  "Article 15(" + "a" + ")(1) excludes roads under 8 m; 15(" + "a" + ")(2) provides a "
  "fallback where <i>all</i> adjoining roads fail. The natural reading drops the 6 m road and leaves "
  "the 10 m street alone — but the 6 m road sits on the <b>high</b> side, and including it would "
  "lift the datum by several metres and change the entire massing.",
  "Obtain the Committee's position <b>in writing</b>. This is the single most consequential "
  "interpretive question on the site."),
 ("HIGH", AMBER, "Slope stability and Article 47(" + "s" + ")",
  "Building is prohibited on land that is steeply sloping and liable to collapse or sliding "
  "<b>where the approved zoning plans so designate it</b>. At 25%, with locally steeper bands on "
  "the eastern third, this plot is in the territory the provision contemplates.",
  "Obtain written confirmation that no part of parcel 96 is so designated, and commission a "
  "geotechnical and slope-stability investigation regardless — the retaining design needs it and "
  "Article 33(" + "d" + ") decking is conditioned on the structure supporting the street, "
  "retaining wall or rock cut."),
 ("HIGH", AMBER, "You cannot regrade your way out of the slope",
  "Article 33(" + "b" + ")(2) caps <b>fill within the setbacks at 1 m above natural ground</b>. "
  "On a 25% gradient that removes platforming as a strategy — the obvious engineering answer is "
  "simply not available.",
  "Terrace, and use Article 33(" + "d" + ") decking as the compliant alternative to fill. "
  "Retaining structures are unavoidable; budget them early rather than discovering them at tender."),
 ("HIGH", AMBER, "Antiquities — the Kallirhoe / " + ar("عين الزارة") + " landscape",
  "The basin is named after the Herodian spa and its ancient Dead Sea harbour, the waterborne "
  "approach to Machaerus, and is under active archaeological survey by ACOR with the Department "
  "of Antiquities. The parcel is ≈2 km inland, so probably outside any immediate perimeter — but "
  "this scheme involves very substantial excavation.",
  "Raise Department of Antiquities clearance <b>now</b>. A chance find during basement excavation "
  "would stop the job at the worst possible moment."),
 ("HIGH", AMBER, "No sewer — and discharge is prohibited",
  "Article 33(" + "e" + ") obliges the owner to provide water collection wells and expressly "
  "<b>prohibits discharging them to the sewer network, to septic tanks, to soakaways, or to "
  "neighbouring land</b>. Sealed collection pits are required where no network exists. For 8–18 "
  "units on a steep site this is a material cost and a real planning constraint.",
  "Confirm the availability of any network with the municipality and the Jordan Valley Authority. "
  "Size sealed pits for the full unit count and plan tanker access on a 25% gradient."),
 ("MEDIUM", AMBER, "Stormwater from a 25% escarpment",
  "The area schedule itself allocates land to " + ar("الأودية") + " (wadis). Runoff across a "
  "one-in-four slope, in a flash-flood landscape, is a design problem before it is a drainage "
  "problem — and the prohibition above means it cannot simply be pushed onto the neighbour or "
  "into a soakaway.",
  "Model the catchment, intercept upslope at the eastern boundary, and integrate the attenuation "
  "into the terrace retaining structure rather than bolting it on."),
 ("MEDIUM", AMBER, "West orientation — the view and the heat are the same direction",
  "Every unit will want to face west for the Dead Sea. West is also the afternoon sun, at an "
  "elevation of about −300 m where summer temperatures are among the most extreme in Jordan. "
  "Unshaded west glazing here is an expensive mistake.",
  "Deep terraces, brise-soleil or overhangs on the west elevation; the roof-floor setback of half "
  "the prescribed setbacks (Art. 48(" + "a" + ")(3)) can be exploited as usable shading depth. "
  "Comply with the national thermal insulation code."),
 ("MEDIUM", AMBER, "Dead Sea atmosphere is aggressive",
  "High salinity and bromide-laden air 2 km from the shore attacks reinforcement, fixings, "
  "external metalwork and plant far faster than inland specification allows for.",
  "Specify corrosion protection deliberately: cover and concrete mix design, stainless or "
  "hot-dip galvanised fixings, and protected condenser and plant locations."),
 ("MEDIUM", AMBER, "Access on a one-in-four gradient",
  "Both streets meet the plot at its ends — the flat dimension — while the site falls across its "
  "width. Getting vehicles from street level to three terraced basement levels is the hardest "
  "plan-making problem here, and Article 36(" + "c" + ") forbids parking in the front setback.",
  "Resolve the ramp strategy at concept stage, not at detail design. Article 33(" + "d" + ")(4) "
  "permits ramps and suspended vehicle passages within the setbacks provided their floor level is "
  "below natural ground."),
 ("MEDIUM", AMBER, "Parking must be built for the full entitlement",
  "Article 36(" + "b" + ")(1) and (2): the parking for the entire permitted building must exist "
  "before <b>any</b> licence issues, and under-providing permanently caps what can ever be licensed.",
  "Build the full parking count in phase one, or accept a permanent ceiling on the scheme."),
 ("LOW", INK3, "No balconies or projections over either street",
  "Article 39 permits no projection where the street is <b>12 m or less</b>. Both streets are. "
  "Architectural projections of up to 60 cm within the setbacks remain available.",
  "Design terraces and balconies to face <b>west, inboard</b> — which is where the view is anyway. "
  "No loss in practice."),
 ("LOW", INK3, "Jordan Valley Authority and Development Zone status",
  "The parcel is inside the statutory Jordan Valley, hence the JVA seal. Evidence indicates it is "
  "<b>not</b> in the Dead Sea Development Zone — that zone's core is 16 km north and a Development "
  "Zone would be licensed by the Development and Free Zones Commission, not by a municipal "
  "directorate — but the gazetted boundary is not published.",
  "Obtain written confirmation from both bodies, and confirm no JVA servitude, wadi buffer or "
  "water-resource restriction affects the parcel."),
]
for sev, col, title, desc, action in CON:
    badge = Paragraph(f'<font color="#ffffff"><b>{sev}</b></font>',
                      S("bdg", fontSize=6.6, leading=8.6, alignment=TA_CENTER))
    bt = Table([[badge]], colWidths=[17*mm])
    bt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),col),
                            ("TOPPADDING",(0,0),(-1,-1),2.6),("BOTTOMPADDING",(0,0),(-1,-1),2.6),
                            ("LEFTPADDING",(0,0),(-1,-1),1),("RIGHTPADDING",(0,0),(-1,-1),1)]))
    head = Table([[bt, Paragraph(fx(f"<b>{title}</b>"),
                   S("cth", fontName="Helvetica-Bold", fontSize=9.3, leading=12, textColor=INK))]],
                 colWidths=[19*mm, W-19*mm])
    head.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                              ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    body = Table([[Paragraph(fx(desc), S("cd", fontSize=8.5, leading=11.9)),
                   Paragraph(fx(f'<font color="#0b7a55"><b>Mitigation.</b></font> {action}'),
                             S("ca", fontSize=8.5, leading=11.9))]],
                 colWidths=[(W-6*mm)*0.54, (W-6*mm)*0.46])
    body.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                              ("LEFTPADDING",(0,0),(0,-1),0),("LEFTPADDING",(1,0),(1,-1),7),
                              ("RIGHTPADDING",(0,0),(-1,-1),4),
                              ("LINEBEFORE",(1,0),(1,-1),0.5,RULE),
                              ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    E += [KeepTogether([head, body, HRFlowable(width="100%", thickness=0.5, color=RULE,
                                               spaceBefore=7, spaceAfter=8)])]
E.append(PageBreak())

# ================================================================= 10 ROADMAP
E += [P("10 · Approvals roadmap", "h1"), rule(INK, 1.0, 0, 8)]
E += [dtable([
  ["#", "Action", "With whom", "Why it is on the critical path"],
  ["1", "Obtain the " + ar("كشف / شهادة أحكام تنظيمية") + " — inside or outside the zoning "
        "boundary, and the " + ar("فئة المنطقة"),
   "Directorate of Municipal Affairs, Dhiban District",
   "<b>Everything in this study depends on it.</b> Changes the footprint by up to 2.7×."],
  ["2", "Complete the merger — Committee approval, fees, registration of the new title",
   "The competent Committee (" + ar("اللجنة المختصة") + ")",
   "Until registered you own two 2,000 m² plots and cannot licence one building across them."],
  ["3", "Confirm the <b>adopted</b> widths of the 6 m road and the 10 m street on the approved "
        "zoning plan", "Directorate of Municipal Affairs",
   "The 8 m, 12 m, 14 m and 20 m thresholds each gate a different entitlement."],
  ["4", "Written ruling on the height datum — does the 6 m road enter the average?",
   "The competent Committee", "Worth several metres of massing. Settle it before design freeze."],
  ["5", "Written ruling on whether both street ends take the 8 m front setback",
   "The competent Committee", "Changes the envelope by 3%; settles the site plan."],
  ["6", "Confirm no part of parcel 96 is designated steep or unstable under Art. 47(" + "s" + ")",
   "Directorate of Municipal Affairs", "A designation would prohibit building outright."],
  ["7", "Date of ratification of the zoning plan for this area",
   "Directorate of Municipal Affairs", "Art. 16(" + "f" + ") turns on whether it predates 16/1/2018."],
  ["8", "Antiquities clearance for parcel 96",
   "Department of Antiquities (" + ar("دائرة الآثار العامة") + ")",
   "Active archaeological landscape; deep excavation proposed."],
  ["9", "Jordan Valley Authority position — servitudes, wadi buffers, water resources; confirm "
        "the municipal licensing route",
   "JVA, Ministry of Water and Irrigation", "The seal on the plan is jurisdictional, not a formality."],
  ["10", "Confirmation that the parcel lies outside the Dead Sea Development Zone",
   "Development and Free Zones Commission", "Would change the licensing authority entirely."],
  ["11", "Geotechnical investigation and slope-stability assessment",
   "Specialist consultant", "Required for the retaining design and for Art. 33(" + "d" + ") decking."],
  ["12", "Confirm sewer, water and power availability; size sealed collection pits",
   "Municipality / JVA / utilities", "Art. 33(" + "e" + ") prohibits the usual disposal routes."],
], [8*mm, 58*mm, 38*mm, W-104*mm])]
E.append(PageBreak())

# ================================================================= 11 COMPLIANCE
E += [P("11 · Compliance schedule", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Every mandatory figure used in this study, traced to the gazette page it was read from. "
        "All numeric tables were read visually from the gazette rather than from OCR — Arabic-Indic "
        "numeral recognition is not reliable enough to design against.", "small")]
E += [dtable([
  ["Article", "Provision", "Value applied", "Gazette p."],
  ["Art. 2", "Definitions — " + ar("قبو") + " / " + ar("تسوية") + " / floor area / coverage",
   "45 cm and 1.5 m tests; basement excluded from coverage and floor area", "2–3"],
  ["Art. 11(" + "a" + ")", "Minimum subdivision area and frontage, Green/Rural",
   "2,000 m² / 30 m — combined plot complies", "10"],
  ["Art. 12(" + "a" + ")", "No subdivision or amendment without the Committee", "merger pending", "11"],
  ["Art. 13(" + "a" + ")", "Relief up to 15% in green / rural / agricultural zones", "noted", "12"],
  ["Art. 13(" + "e" + ")(1)", "Subdivision road capacity vs plots served",
   "10 m serves 3–10 plots; 6 m serves 1 — layout complies", "12"],
  ["Art. 15(" + "a" + ")(1)", "Height datum; roads under 8 m disregarded",
   "6 m road excluded; datum from the 10 m street", "14"],
  ["Art. 15(" + "a" + ")(3)", "Multiple buildings — height from the nearest road", "strategy move 6", "14"],
  ["Art. 15(" + "c" + ")", "Natural-ground datum where ground is above road level",
   "available; forfeits the " + ar("تسوية"), "14"],
  ["Art. 15(" + "d" + ")", "Ground slab may be raised max 2 m", "2.00 m", "14"],
  ["Art. 15(" + "e" + ")", "Mechanical services floor excluded", "noted", "15"],
  ["Art. 15(" + "f" + ")", "Single road with multiple levels — use the average", "applied", "15"],
  ["Art. 16(" + "a" + ")", "Development control table, Green/Rural",
   "8/6/6 m · 27% · 2+roof · 9 m · 10% green", "15"],
  ["Art. 16(" + "e" + ")", "<b>Exclusion of (b)(c)(d) — roads under 20 m</b>",
   "<b>no height bonus, no high-building table</b>", "17"],
  ["Art. 16(" + "f" + ")", "Additional floor requires a 14 m street", "not available", "17"],
  ["Art. 16(" + "g" + ")", "Council may waive the coverage percentage", "relief route", "17"],
  ["Art. 33(" + "b" + ")", "Fences 1.5 / 2 m; fill in setbacks max 1 m", "applied", "31"],
  ["Art. 33(" + "d" + ")", "Setback decking; 45 cm; upper or lower street or both",
   "excluded from built area and floor area", "31–32"],
  ["Art. 33(" + "e" + ")", "Water collection; discharge prohibited", "sealed pits required", "32"],
  ["Art. 34(" + "a" + ")", "Ancillary building",
   "≤ 25 m², additional to coverage, ≤ 2.6 m, detached", "32"],
  ["Art. 36(" + "b" + ")", "Parking for the full permitted building; GF parking excluded from height",
   "applied", "33"],
  ["Art. 36(" + "c" + ")(" + "d" + ")", "No parking in the front setback in residential zones",
   "applied", "33"],
  ["Art. 36(" + "e" + ")", "Parking rate, residential incl. " + ar("ريفي"),
   "1 per 300 m² or 1 per apartment, greater", "34"],
  ["Art. 38(" + "a" + ")", "Permitted uses of the " + ar("قبو"), "not habitable", "27–28"],
  ["Art. 39", "No projection where the street is ≤ 12 m", "applied", "28"],
  ["Art. 44", "Outside-zoning control table", "the alternative scenario — 10% coverage", "41"],
  ["Art. 47(" + "l" + ")", "Green/rural: residential and places of worship only",
   "multi-unit residential complies", "45"],
  ["Art. 47(" + "s" + ")", "No building on designated steep or unstable land", "to be confirmed", "46"],
  ["Art. 48(" + "a" + ")", "Roof floor — ≤ 50%, ≤ 3.5 m, half setbacks", "applied", "46"],
  ["Art. 48(" + "b" + ")", "Front " + ar("طابق سطح") + " — zones " + ar("a, b, c, d") + " only",
   "<b>not available here</b>", "46–47"],
], [22*mm, 52*mm, 52*mm, W-126*mm], fs=7.6, pad=3.4)]
E.append(PageBreak())

# ================================================================= 12 BASIS
E += [P("12 · Basis, limitations and sources", "h1"), rule(INK, 1.0, 0, 8)]
E += [P("Confidence register", "h2")]
E += [dtable([
  ["Finding", "Status"],
  ["Site identity, parcel, basin, village, surveyor", "VERIFIED — title blocks, both plans"],
  ["Coordinates cross-checked against the area schedule (9,236.03 vs 9,236.720 m²)", "VERIFIED — computed"],
  ["Combined area 4,000 m²", "VERIFIED — both area schedules, cross-checked"],
  ["Boundary lengths 47.26 / 47.88 / 86.27 / 82.23 m", "VERIFIED — stamped plan"],
  ["Adjoining roads 6 m north, 10 m south", "VERIFIED — both plans"],
  ["Relief ≈ 15 m, gradient ≈ 25% east to west", "VERIFIED — survey 13-6-2026, corroborated by SRTM"],
  ["Position and elevation (−226 to −361 m)", "VERIFIED — computed and sampled"],
  ["Art. 16(" + "e" + ") disapplies the height bonuses", "VERIFIED — gazette p.17, read visually"],
  ["All control tables and height provisions", "VERIFIED — gazette pp.10, 14, 15, 17, 41, read visually"],
  ["<b>Zoning classification</b>", "<b>UNVERIFIED — OFFICIAL SOURCE REQUIRED</b>"],
  ["Inside the zoning boundary", "Inferred — the file was handled by the municipal directorate, "
   "not the JVA's outside-boundary service"],
  ["Green / Rural as the class", "ASSUMPTION — plot-size regularity, road/plot match, municipal "
   "routing. " + ar("سكن د") + " is not excluded by the evidence"],
  ["Height datum ≈ +6.0", "ASSUMPTION — read off contours; recompute from levelled spot heights"],
  ["Whether the 6 m road enters the datum", "INTERPRETIVE — Committee ruling required"],
  ["Whether both street ends take the front setback", "INTERPRETIVE — Committee ruling required"],
  ["Art. 47(" + "s" + ") steep-land designation", "UNVERIFIED — OFFICIAL SOURCE REQUIRED"],
  ["Basement area achievable", "MODELLED — terracing model at 3.0 m floor-to-floor and 25% gradient"],
  ["Unit counts and net saleable areas", "INDICATIVE — for capacity testing, not a design proposal"],
], [W*0.52, W*0.48], fs=7.9, pad=3.6)]
E += callout("Limitations — please read before relying on any number here",
  ["This is a <b>capacity and feasibility study</b>, not a design and not a planning approval. "
   "The massing shown is indicative: it demonstrates what the permitted footprint looks like "
   "distributed across the slope, and is not a proposal.",
   "<b>The zoning classification is assumed.</b> Every area figure moves if that assumption fails.",
   "<b>The height datum is read from contours, not from levelled spot heights.</b> It must be "
   "recomputed by the surveyor along the 10 m street frontage before it is designed against.",
   "The drawings are schematic, prepared from the dimensions printed on the approved plan. They "
   "are not survey drawings and must not be scaled.",
   "Nothing here has been invented. Where a figure could not be verified it is marked UNVERIFIED "
   "and no compliant result is claimed for it."],
  RED, colors.HexColor("#fbf0ef"))
E += [P("Sources", "h2")]
E += [P("<b>Regulation.</b> " + ar("نظام الأبنية وتنظيم المدن والقرى رقم (1) لسنة 2022") +
        " — Official Gazette. Articles 2, 11, 12, 13, 15, 16, 33, 34, 35, 36, 38, 39, 44, 47, 48. "
        "As amended by " + ar("النظام المعدّل رقم (12) لسنة 2025") + ".", "small"),
      P("<b>Site documents.</b> Subdivision plan, four plots, printed 15/4/2026 and 15/6/2026. "
        "Subdivision plan, three plots with 3 and 4 merged, endorsed by the Directorate of "
        "Municipal Affairs for Dhiban District 25/4/2026, bearing the Jordan Valley Authority seal. "
        "Topographic survey of natural ground for " + ar("3 مؤقت + 4 مؤقت من اصل 96") +
        ", dated 13-6-2026, Eng. Orwah El-Hawawsha Surveying Office, Madaba.", "small"),
      P("<b>Corroborating sources.</b> Jordan Valley Development Law (jordanianlaw.com); Jordan "
        "Valley Authority outside-boundary building permit service (Jordan Government Portal); "
        "Department of Lands and Survey mapping portal (maps.dls.gov.jo); Dead Sea Development "
        "Zone master plan (Sasaki) and Jordan Free and Development Zones Group; Kallirhoe / "
        "'Ain az-Zara archaeological project (ACOR Jordan); SRTM 30 m elevation via OpenTopoData.", "small")]
E += [rule(RULE, 0.6, 10, 6),
      P("Prepared by NORMIA — AEC Regulatory Intelligence &amp; Compliance Consultant. "
        "NORMIA never invents regulations. Where information cannot be verified against an "
        "official source it is marked UNVERIFIED, and no compliant result is issued in its place.",
        "small")]

doc.build(E)
print("built")
