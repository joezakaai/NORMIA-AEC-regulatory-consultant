import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
"""Original technical drawings for the Jordanian Building Regulation No.1/2022.
Drawn by NORMIA to illustrate the rules; the gazette itself contains no diagrams.
Style follows the Lebanese decree's drawing conventions.
"""
import math, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.patches import Polygon as Poly, FancyArrowPatch
from matplotlib.font_manager import FontProperties
import arabic_reshaper
from bidi.algorithm import get_display

OUT = HERE + "/figs"
os.makedirs(OUT, exist_ok=True)

INK, INK2, INK3 = "#111111", "#4a4a46", "#8d8b84"
RED, GRN, BLU = "#c0332f", "#1f8a4c", "#2a6fd6"
BLD, BLDE = "#f2c4bb", "#a8382c"          # building fill / edge
GRD, GRDE = "#cfe3b8", "#4b7a2e"          # ground
CAR, CARE = "#aee6f2", "#2b8ba8"          # cars
HATCH = "#e8e6de"
ARP = "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf"
ARB = "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf"
from matplotlib import font_manager as _fm
for _p in (ARP, ARB):
    _fm.fontManager.addfont(_p)
plt.rcParams.update({"font.family": ["DejaVu Sans", "Noto Naskh Arabic"],
                     "font.size": 7.4,
                     "figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white"})
FA  = FontProperties(family=["Noto Naskh Arabic","DejaVu Sans"], size=8.4)
FAB = FontProperties(family=["Noto Naskh Arabic","DejaVu Sans"], size=9.2, weight="bold")
def ar(s):
    return get_display(arabic_reshaper.reshape(s))

_ARRE = __import__("re").compile(r"[\u0600-\u06ff\u0750-\u077f]")
def mx(s):
    """Shape + bidi-order any string that mixes Arabic with Latin.
    Rendering relies on the DejaVu Sans -> Noto Naskh Arabic font fallback."""
    s = str(s)
    if not _ARRE.search(s):
        return s
    return "\n".join(get_display(arabic_reshaper.reshape(l)) for l in s.split("\n"))
IDX = []   # figure catalogue


# ───────────────────────────────────────────── primitives
def newfig(w=7.2, h=4.4):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax

def caption(ax, n, en, arabic, x=0.5, y=-0.085):
    ax.text(0.015, y, f"JO-Fig-{n:02d}", transform=ax.transAxes, fontsize=7.6,
            color=INK2, ha="left", va="top", weight="bold")
    ax.text(0.985, y, ar(arabic), transform=ax.transAxes, fontproperties=afp(9.2, True),
            color=INK, ha="right", va="top")
    ax.text(0.985, y-0.085, en, transform=ax.transAxes, fontsize=8.0,
            color=INK2, ha="right", va="top")

def ground(ax, x0, x1, ys, lw=1.7):
    """ys: callable or constant"""
    xs = np.linspace(x0, x1, 200)
    yy = np.array([ys(x) if callable(ys) else ys for x in xs])
    ax.fill_between(xs, yy-40, yy, color=GRD, zorder=1, lw=0)
    ax.plot(xs, yy, color=GRDE, lw=lw, zorder=4)
    return yy

def blk(ax, x, y, w, h, fc=BLD, ec=BLDE, lw=1.0, z=6, alpha=1.0, ls="-"):
    ax.add_patch(mp.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                              lw=lw, zorder=z, alpha=alpha, linestyle=ls))

def dim(ax, p, q, txt, off=0.0, side=1, fs=7.2, color=INK2, z=12, rot=None):
    p = np.array(p, float); q = np.array(q, float)
    v = q-p; L = np.linalg.norm(v)
    if L == 0: return
    n = np.array([-v[1], v[0]])/L * off * side
    a, b = p+n, q+n
    ax.annotate("", xy=tuple(b), xytext=tuple(a), zorder=z,
                arrowprops=dict(arrowstyle="<->", lw=0.8, color=color,
                                shrinkA=0, shrinkB=0))
    m = (a+b)/2
    if rot is None:
        rot = math.degrees(math.atan2(v[1], v[0]))
        if rot > 90: rot -= 180
        if rot < -90: rot += 180
    ax.text(m[0], m[1], mx(txt), ha="center", va="center", fontsize=fs, color=color,
            rotation=rot, zorder=z+1,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92))

def lvl(ax, x, y, txt, color=BLU, dx=0.0, fs=7.0):
    ax.plot([x], [y], marker="o", ms=4, color=color, zorder=13)
    ax.text(x+dx, y, mx(txt), fontsize=fs, color=color, weight="bold",
            ha="center", va="center", zorder=14,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=color, lw=0.7))

def note(ax, x, y, txt, color=INK2, fs=7.0, ha="left", va="center", box=True, w="normal"):
    kw = dict(bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=color,
                        lw=0.7, alpha=0.95)) if box else {}
    ax.text(x, y, mx(txt), fontsize=fs, color=color, ha=ha, va=va, zorder=15,
            weight=w, **kw)

def afp(fs, bold=False):
    fp = FontProperties(family=["Noto Naskh Arabic", "DejaVu Sans"])
    fp.set_size(fs); fp.set_weight("bold" if bold else "normal"); return fp

def arabel(ax, x, y, txt, fs=8.4, color=INK, ha="center", va="center", bold=False):
    ax.text(x, y, ar(txt), fontproperties=afp(fs, bold), color=color,
            ha=ha, va=va, zorder=15)

def road(ax, x0, x1, y, w=1.0, label=None, arlabel=None, fs=7.2):
    ax.add_patch(mp.Rectangle((x0, y-w), x1-x0, w, facecolor="#e6e4dc",
                              edgecolor=INK3, lw=0.8, zorder=2))
    if label:
        ax.text((x0+x1)/2, y-w/2, mx(label), ha="center", va="center",
                fontsize=fs, color=INK2, zorder=3)
    if arlabel:
        ax.text((x0+x1)/2, y-w/2-0.55, ar(arlabel), fontproperties=afp(8.0),
                ha="center", va="center", color=INK2, zorder=3)

def save(fig, n, en, arabic, art):
    fig.tight_layout(rect=[0, 0.055, 1, 1])
    p = f"{OUT}/JO-Fig-{n:02d}.png"
    fig.savefig(p, dpi=210, bbox_inches="tight")
    plt.close(fig)
    IDX.append(dict(n=n, file=os.path.basename(p), en=en, ar=arabic, art=art))


# ═════════════════════════════════════════════ FIGURES
def f01():
    fig, ax = newfig(6.4, 4.6)
    W, H = 10, 8
    ax.add_patch(mp.Rectangle((0, 0), W, H, facecolor="#faf9f5", edgecolor=INK, lw=1.8, zorder=3))
    fr, sd, rr = 2.0, 1.4, 1.6
    blk(ax, sd, fr, W-2*sd, H-fr-rr, fc=BLD, ec=BLDE, lw=1.2)
    arabel(ax, W/2, (fr+H-rr)/2, "البناء", 11, bold=True)
    road(ax, -1.2, W+1.2, 0, 1.3, "road  الطريق")
    dim(ax, (W+0.7, 0), (W+0.7, fr), "front", 0, 1, 6.8)
    dim(ax, (0, H+0.7), (sd, H+0.7), "side", 0, 1, 6.8)
    dim(ax, (W-sd, H+0.7), (W, H+0.7), "side", 0, 1, 6.8)
    dim(ax, (-0.8, H-rr), (-0.8, H), "rear", 0, 1, 6.8)
    for x, y, t in [(sd/2, H*0.55, "الجانبي"), (W-sd/2, H*0.55, "الجانبي")]:
        arabel(ax, x, y, t, 7.4, INK2)
    arabel(ax, W/2, H-rr/2, "الخلفي", 7.6, INK2)
    note(ax, W/2, -2.3, "Setback (الارتداد) = the space separating the building from the plot\n"
                        "boundary, or from the line of the road abutting the plot   [Art. 2]",
         INK2, 7.2, "center")
    ax.set_xlim(-2.6, W+3.4); ax.set_ylim(-3.4, H+2.0)
    save(fig, 1, "The four setbacks and what a setback is", "الارتدادات الأربعة وتعريف الارتداد", "Art 2")


def f02():
    fig, ax = newfig(7.4, 3.9)
    rows = [("سكن أ", "A", 1000, 25), ("سكن ب", "B", 750, 20), ("سكن ج", "C", 500, 18),
            ("سكن د", "D", 250, 15), ("الأخضر/الريفي", "Green/Rural", 2000, 30),
            ("الزراعي", "Agric.", 4000, 35)]
    x = 0
    for a, e, area, fr in rows:
        w = fr/35*3.0; h = area/4000*3.0 + 0.5
        blk(ax, x, 0, w, h, fc="#eef3fb", ec=BLU, lw=1.1)
        ax.text(x+w/2, h+0.30, f"{area:,} m²", ha="center", fontsize=7.4, color=INK, weight="bold")
        ax.text(x+w/2, h+0.08, f"{fr} m frontage", ha="center", fontsize=6.6, color=INK2)
        arabel(ax, x+w/2, -0.42, a, 7.8, INK)
        ax.text(x+w/2, -0.80, e, ha="center", fontsize=6.8, color=INK2)
        dim(ax, (x, -0.12), (x+w, -0.12), "", 0, 1, 6)
        x += w + 0.55
    note(ax, x/2, 4.5, "Article 11(a)(1) — minimum subdivision area and minimum plot frontage,\n"
                       "residential zones.  Bar width ∝ frontage, bar height ∝ area.",
         INK2, 7.2, "center")
    ax.set_xlim(-0.5, x); ax.set_ylim(-1.5, 5.2)
    save(fig, 2, "Minimum subdivision area and plot frontage — residential",
         "الحد الأدنى لمساحة الإفراز وواجهة القطعة — المناطق السكنية", "Art 11")


def f03():
    fig, ax = newfig(7.2, 3.4)
    data = [(6, "1"), (8, "2"), (10, "3 – 10"), (12, "11 – 19"), (14, "20 +")]
    x = 0
    for w, plots in data:
        ww = w/14*2.4
        ax.add_patch(mp.Rectangle((x, 0), ww, 1.5, facecolor="#e6e4dc", edgecolor=INK3, lw=0.9))
        ax.text(x+ww/2, 0.75, f"{w} m", ha="center", va="center", fontsize=8.4,
                color=INK, weight="bold")
        ax.text(x+ww/2, 1.85, plots, ha="center", fontsize=8.6, color=BLU, weight="bold")
        ax.text(x+ww/2, 2.25, "plots served", ha="center", fontsize=6.4, color=INK2)
        for k in range(min(4, 1 if plots == "1" else 3)):
            blk(ax, x+0.12+k*(ww-0.24)/3, -0.95, (ww-0.30)/3.4, 0.62, fc=BLD, ec=BLDE, lw=0.7)
        x += ww + 0.5
    arabel(ax, x/2, 3.05, "سعة الطريق المفرزة وعدد القطع المخدومة", 9.4, INK, bold=True)
    note(ax, x/2, -1.7, "Article 13(e)(1) — the width of a subdivision road fixes how many plots it may serve.",
         INK2, 7.2, "center")
    ax.set_xlim(-0.4, x); ax.set_ylim(-2.3, 3.6)
    save(fig, 3, "Subdivision road width against the number of plots served",
         "سعة الطريق المفرزة مقابل عدد القطع المخدومة", "Art 13")


def f04():
    fig, ax = newfig(7.2, 4.2)
    ground(ax, -1, 13, 0)
    road(ax, -1, 0.1, 0, 1.2, "6 m road", None)
    road(ax, 11.9, 13, 0, 1.2, "12 m street", None)
    ax.text(-0.45, -2.0, "6 m\n< 8 m", ha="center", fontsize=7.0, color=RED, weight="bold")
    ax.text(12.45, -2.0, "12 m\n≥ 8 m", ha="center", fontsize=7.0, color=GRN, weight="bold")
    blk(ax, 2.2, 0, 7.6, 5.4)
    arabel(ax, 6.0, 2.7, "البناء", 11, bold=True)
    ax.plot([-1, 13], [0, 0], color=BLU, lw=1.4, ls=(0, (7, 4)), zorder=8)
    note(ax, 13.2, 0, "datum", BLU, 7.0, "left")
    dim(ax, (10.4, 0), (10.4, 5.4), "9 m", 0, 1, 7.6, RED)
    ax.plot([2.0, 11.0], [5.4, 5.4], color=RED, lw=1.8, zorder=9)
    ax.add_patch(mp.Circle((-0.45, -1.15), 0.42, facecolor="white", edgecolor=RED, lw=1.4, zorder=12))
    ax.text(-0.45, -1.15, "✗", ha="center", va="center", fontsize=11, color=RED, weight="bold", zorder=13)
    ax.add_patch(mp.Circle((12.45, -1.15), 0.42, facecolor="white", edgecolor=GRN, lw=1.4, zorder=12))
    ax.text(12.45, -1.15, "✓", ha="center", va="center", fontsize=11, color=GRN, weight="bold", zorder=13)
    note(ax, 6.0, 7.2, "Height is measured from the AVERAGE level of the adjoining roads.\n"
                       "A road narrower than 8 m is NOT counted in that average.", INK, 7.6, "center", w="bold")
    arabel(ax, 6.0, 6.35, "ولا تعتمد الطرق التي تقل سعتها عن (٨) امتار لاحتساب متوسط المنسوب", 8.6, INK2)
    ax.set_xlim(-2.4, 14.6); ax.set_ylim(-3.2, 8.2)
    save(fig, 4, "Height datum — roads narrower than 8 m are disregarded",
         "احتساب الارتفاع — لا تعتمد الطرق التي تقل سعتها عن ٨ أمتار", "Art 15(a)(1)")


def f05():
    fig, ax = newfig(7.2, 4.0)
    gy = lambda x: 0 if x < 6 else (x-6)*0.30
    ground(ax, -1, 13, gy)
    road(ax, -1, 0.4, 0, 1.0, "6 m", None)
    road(ax, 11.6, 13, gy(12.3), 1.0, "7 m", None)
    blk(ax, 2.2, 0, 7.6, 4.6)
    arabel(ax, 6.0, 2.3, "البناء", 11, bold=True)
    ax.plot([-1, 13], [0.9, 0.9], color=BLU, lw=1.4, ls=(0, (7, 4)), zorder=8)
    note(ax, 13.2, 0.9, "average of\nBOTH roads", BLU, 6.8, "left")
    lvl(ax, 0.2, 0, "0.0", BLU, -0.0)
    lvl(ax, 11.8, gy(11.8), "+1.8", BLU, 0.0)
    dim(ax, (10.4, 0.9), (10.4, 4.6+0.9), "9 m", 0, 1, 7.6, RED)
    note(ax, 6.0, 6.6, "Where the plot fronts MORE THAN ONE road and they ALL fall short of the\n"
                       "8 m test, the datum becomes the average of those roads.",
         INK, 7.6, "center", w="bold")
    ax.set_xlim(-2.4, 15.2); ax.set_ylim(-1.8, 7.6)
    save(fig, 5, "Where every adjoining road is under 8 m — average them",
         "في حال وقوع القطعة على أكثر من طريق تقل سعتها — متوسط مناسيب هذه الطرق", "Art 15(a)(2)")


def f06():
    fig, ax = newfig(7.2, 4.0)
    gy = lambda x: 0.0 if x < 5 else (x-5)*0.42
    ground(ax, -1, 14, gy)
    road(ax, -1, 0.4, 0, 1.0, "road A", None)
    road(ax, 13.0, 14.4, gy(13.6), 1.0, "road B", None)
    blk(ax, 1.6, 0, 4.2, 4.2)
    blk(ax, 8.2, gy(8.2), 4.2, 4.2)
    arabel(ax, 3.7, 2.1, "بناء ١", 9.6, bold=True)
    arabel(ax, 10.3, gy(8.2)+2.1, "بناء ٢", 9.6, bold=True)
    ax.plot([1.2, 6.4], [0, 0], color=BLU, lw=1.3, ls=(0, (6, 3)), zorder=8)
    ax.plot([7.8, 13.0], [gy(13.6)]*2, color=BLU, lw=1.3, ls=(0, (6, 3)), zorder=8)
    dim(ax, (6.1, 0), (6.1, 4.2), "9 m", 0, 1, 7.2, RED)
    dim(ax, (12.7, gy(13.6)), (12.7, gy(8.2)+4.2), "9 m", 0, 1, 7.2, RED)
    note(ax, 3.7, -1.5, "from road A", BLU, 6.8, "center")
    note(ax, 10.3, gy(13.6)-1.5, "from road B", BLU, 6.8, "center")
    note(ax, 6.8, 7.4, "More than one road AND more than one building on the plot:\n"
                       "each building takes its height from the NEAREST road.",
         INK, 7.6, "center", w="bold")
    ax.set_xlim(-2.0, 15.6); ax.set_ylim(-3.0, 8.4)
    save(fig, 6, "Several buildings — each takes the nearest road",
         "أكثر من بناء — يحسب ارتفاع كل بناء من متوسط منسوب الطريق الأقرب له", "Art 15(a)(3)")


def f07():
    fig, ax = newfig(7.2, 4.4)
    gy = lambda x: 0 if x < 2 else min((x-2)*0.55, 4.4)
    ground(ax, -1, 14, gy)
    road(ax, -1, 1.2, 0, 1.1, "road", None)
    base = 4.4
    blk(ax, 4.2, base, 6.6, 2.6, fc="#dfe9d9", ec=GRDE, lw=1.1)
    arabel(ax, 7.5, base+1.55, "مواقف / خدمات", 8.6, "#2c5c1c", bold=True)
    ax.text(7.5, base+0.75, "parking / services — EXCLUDED from\nheight and from the floor count",
            ha="center", fontsize=6.4, color="#2c5c1c")
    for k in range(2):
        blk(ax, 4.2, base+2.6+k*2.5, 6.6, 2.4)
        arabel(ax, 7.5, base+2.6+k*2.5+1.2, f"طابق {k+1}", 8.6, bold=True)
    ax.plot([-1, 14], [0, 0], color=BLU, lw=1.2, ls=(0, (6, 3)), zorder=8)
    note(ax, 14.2, 0, "road level", BLU, 6.8, "left")
    ax.plot([3.6, 11.6], [base]*2, color=GRDE, lw=1.4, ls=(0, (5, 3)), zorder=9)
    note(ax, 3.3, base+0.9, "natural\nground", "#2c5c1c", 6.6, "right")
    dim(ax, (11.2, base+2.6), (11.2, base+2.6+4.9), "9 m", 0, 1, 7.6, RED)
    note(ax, 7.0, 13.2, "Where NATURAL GROUND is higher than the road, height may be taken from natural\n"
                        "ground — provided the building has NO semi-basement.",
         INK, 7.6, "center", w="bold")
    ax.set_xlim(-2.4, 16.0); ax.set_ylim(-2.0, 14.4)
    save(fig, 7, "Natural ground above road level — the Article 15(c) relief",
         "احتساب الارتفاع من منسوب الأرض الطبيعية — شريطة عدم وجود طوابق تسوية", "Art 15(c)")


def f08():
    fig, ax = newfig(6.6, 3.4)
    ground(ax, -1, 12, 0)
    road(ax, -1, 1.0, 0, 1.0, "road", None)
    blk(ax, 3.0, 2.0, 6.4, 3.0)
    arabel(ax, 6.2, 3.5, "الطابق الأرضي", 9.2, bold=True)
    ax.plot([2.6, 9.8], [2.0, 2.0], color=BLDE, lw=1.6, zorder=9)
    dim(ax, (2.4, 0), (2.4, 2.0), "max 2.00 m", 0, 1, 7.4, RED)
    ax.plot([-1, 12], [0, 0], color=BLU, lw=1.2, ls=(0, (6, 3)), zorder=8)
    note(ax, 6.2, 7.0, "The ground-floor slab may be raised a MAXIMUM of 2 m above natural ground or\n"
                       "road level — only where there is NO basement and NO semi-basement.",
         INK, 7.4, "center", w="bold")
    arabel(ax, 6.2, 6.0, "يسمح برفع منسوب بلاط الطابق الأرضي بحد أقصى (٢م)", 8.8, INK2)
    ax.set_xlim(-2.0, 13.2); ax.set_ylim(-1.6, 7.8)
    save(fig, 8, "Raising the ground-floor slab — maximum 2 m",
         "رفع منسوب بلاط الطابق الأرضي بحد أقصى مترين", "Art 15(d)")


def f09():
    fig, ax = newfig(7.2, 3.6)
    xs = np.linspace(0, 12, 200)
    ry = 0.26*xs
    ax.plot(xs, ry, color=INK3, lw=2.0, zorder=4)
    ax.fill_between(xs, ry-0.8, ry, color="#e6e4dc", zorder=2)
    avg = 0.26*6
    ax.plot([0, 12], [avg, avg], color=BLU, lw=1.5, ls=(0, (7, 4)), zorder=8)
    note(ax, 12.3, avg, "average level\nof THIS road", BLU, 6.8, "left")
    for x in (0.4, 6.0, 11.6):
        lvl(ax, x, 0.26*x, f"+{0.26*x:.1f}", BLU)
    blk(ax, 2.0, avg, 8.0, 4.0)
    arabel(ax, 6.0, avg+2.0, "البناء", 11, bold=True)
    dim(ax, (10.6, avg), (10.6, avg+4.0), "9 m", 0, 1, 7.4, RED)
    note(ax, 6.0, 8.0, "A plot on a SINGLE road that has several levels along its frontage:\n"
                       "height is computed from the AVERAGE level of that road.",
         INK, 7.6, "center", w="bold")
    ax.set_xlim(-1.2, 15.0); ax.set_ylim(-1.4, 8.8)
    save(fig, 9, "One road with several levels — use its average",
         "قطعة تقع على طريق واحد وفيه مناسيب متعددة — متوسط منسوب هذا الطريق", "Art 15(f)")


def f10():
    fig, ax = newfig(7.0, 4.0)
    ground(ax, -1, 13, 0)
    road(ax, -1, 0.8, 0, 1.0, "road", None)
    fr = 2.0
    blk(ax, 0.8+fr, -2.8, 10.0-fr, 2.8, fc="#dfe9d9", ec=GRDE, lw=1.3)
    arabel(ax, 6.4, -1.4, "طابق القبو", 10.4, "#2c5c1c", bold=True)
    ax.text(6.4, -2.15, "basement — parking, RC water tanks, storage,\n"
                        "heating/cooling plant, electrical rooms.  NOT habitable.",
            ha="center", fontsize=6.5, color="#2c5c1c")
    blk(ax, 0.8+fr, 0, 10.0-fr, 3.0)
    arabel(ax, 6.4, 1.5, "الطابق الأرضي", 9.2, bold=True)
    ax.plot([0.8+fr, 10.8], [0.45]*2, color=RED, lw=1.5, zorder=10)
    dim(ax, (11.1, 0), (11.1, 0.45), "≤ 45 cm", 0, 1, 7.4, RED)
    note(ax, 11.6, 1.6, "above natural ground OR the average\nroad level — WHICHEVER IS LOWER",
         RED, 6.6, "left")
    dim(ax, (0.8, -3.4), (0.8+fr, -3.4), "front setback\nkept clear", 0, 1, 6.8, BLU)
    dim(ax, (0.8+fr, -3.4), (10.8, -3.4), "the basement may occupy the whole plot", 0, 1, 6.8, GRN)
    ax.set_xlim(-2.0, 16.4); ax.set_ylim(-5.0, 4.4)
    save(fig, 10, "The basement (قبو) — the 45 cm test and its permitted extent",
         "طابق القبو — اختبار الـ ٤٥ سم ومدى امتداده", "Art 2 / Art 28")


def f11():
    fig, ax = newfig(7.0, 3.8)
    ground(ax, -1, 13, 0)
    road(ax, -1, 0.8, 0, 1.0, "road", None)
    blk(ax, 2.4, -2.2, 8.4, 3.7, fc="#e6e0ef", ec="#6a4fa3", lw=1.3)
    arabel(ax, 6.6, -0.35, "طابق التسوية", 10.4, "#4a3580", bold=True)
    blk(ax, 2.4, 1.5, 8.4, 2.8)
    arabel(ax, 6.6, 2.9, "الطابق الأرضي", 9.2, bold=True)
    ax.plot([-1, 13], [0, 0], color=BLU, lw=1.2, ls=(0, (6, 3)), zorder=8)
    note(ax, 13.2, 0, "average\nroad level", BLU, 6.6, "left")
    dim(ax, (11.2, 0), (11.2, 1.5), "≤ 1.50 m", 0, 1, 7.4, "#4a3580")
    note(ax, 6.6, 6.0, "The SEMI-BASEMENT is defined only by its slab sitting no more than 1.50 m above\n"
                       "the average road level.  It is excluded from the floor area — but a building that\n"
                       "contains one FORFEITS the Article 15(c) natural-ground relief.",
         INK, 7.3, "center", w="bold")
    ax.set_xlim(-2.0, 15.4); ax.set_ylim(-3.4, 7.2)
    save(fig, 11, "The semi-basement (تسوية) — the 1.50 m test, and what it costs",
         "طابق التسوية — اختبار المتر والنصف", "Art 2")


def f12():
    fig, ax = newfig(7.4, 4.2)
    W, H = 11, 7
    ax.add_patch(mp.Rectangle((0, 0), W, H, facecolor="#faf9f5", edgecolor=INK, lw=1.6, zorder=2))
    blk(ax, 2.0, 1.6, 6.0, 4.0, fc=BLD, ec=BLDE, lw=1.3, z=5)
    arabel(ax, 5.0, 3.6, "أكبر مسقط أفقي", 9.4, bold=True)
    ax.text(5.0, 3.0, "largest horizontal projection\n= the coverage", ha="center",
            fontsize=6.8, color="#7a2a1e")
    exc = [(8.4, 4.4, 2.0, 1.2, "مواقف"), (8.4, 2.6, 2.0, 1.4, "أقبية"),
           (2.0, 0.3, 2.2, 1.0, "أدراج مكشوفة"), (5.0, 0.3, 3.0, 1.0, "بروزات معمارية")]
    for x, y, w, h, t in exc:
        blk(ax, x, y, w, h, fc="#eceae2", ec=INK3, lw=0.9, z=4, ls=(0, (4, 2)))
        arabel(ax, x+w/2, y+h/2, t, 7.2, INK2)
    note(ax, 5.5, -1.3, "النسبة المئوية للبناء  =  area of the LARGEST horizontal projection ÷ plot area", INK, 7.6, "center", w="bold")
    note(ax, 5.5, -2.3, "EXCLUDED:  commercial and architectural projections · car parking · basements ·\n"
                        "open passages and stairs · water wells and collection pits · fuel and water tanks ·\n"
                        "electrical rooms and generators · light wells · mechanical ventilation voids",
         INK2, 6.9, "center")
    ax.set_xlim(-0.8, W+0.8); ax.set_ylim(-3.6, H+0.8)
    save(fig, 12, "Coverage (النسبة المئوية) — what counts and what is excluded",
         "النسبة المئوية للبناء — ما يحتسب وما يستثنى", "Art 2")


def f13():
    fig, ax = newfig(6.8, 4.6)
    lv = [("طابق الروف", 0.55, BLD, "counts"), ("الطابق الثاني", 1.0, BLD, "counts"),
          ("الطابق الأول", 1.0, BLD, "counts"), ("الطابق الأرضي", 1.0, BLD, "counts"),
          ("طابق التسوية", 1.0, "#e6e0ef", "EXCLUDED"), ("طابق القبو", 1.0, "#dfe9d9", "EXCLUDED")]
    y = 0
    for name, frac, fc, st in reversed(lv):
        w = 7.0*frac
        blk(ax, 0, y, w, 1.5, fc=fc, ec=(BLDE if fc == BLD else INK3), lw=1.1)
        arabel(ax, w/2, y+0.75, name, 9.0, bold=True)
        c = GRN if st == "counts" else RED
        ax.text(7.4, y+0.75, st, fontsize=7.4, color=c, va="center", weight="bold")
        y += 1.65
    note(ax, 3.5, y+0.9, "المساحة الطابقية  =  the sum of the ROOFED horizontal projections of all floors",
         INK, 7.6, "center", w="bold")
    note(ax, 3.5, -1.5, "Also excluded from the floor area:  commercial mezzanines (السدد) · mechanical\n"
                        "service floors · commercial and architectural projections · car parking ·\n"
                        "open passages and stairs · light wells · the lift-room and last-stair roofs",
         INK2, 6.9, "center")
    ax.set_xlim(-0.6, 10.4); ax.set_ylim(-2.6, y+1.8)
    save(fig, 13, "Floor area (المساحة الطابقية) — the basement and semi-basement drop out",
         "المساحة الطابقية — تستثنى طوابق التسوية والأقبية", "Art 2")


def f14():
    fig, ax = newfig(7.2, 4.6)
    ground(ax, -1, 13, 0)
    road(ax, -1, 0.8, 0, 1.1, "road", None)
    fr, sd = 1.4, 1.1
    n, fh = 4, 1.05
    for k in range(n):
        blk(ax, 0.8+fr, k*fh, 8.4, fh-0.06)
        arabel(ax, 5.0, k*fh+fh/2, f"طابق {k+1}", 7.8, bold=True)
    dim(ax, (9.6, 0), (9.6, n*fh), "17 m max", 0, 1, 7.4, RED)
    note(ax, 10.6, n*fh/2, "4 floors", RED, 7.2, "left")
    dim(ax, (0.8, -1.5), (0.8+fr, -1.5), "5 m front", 0, 1, 6.8, BLU)
    note(ax, 5.0, 7.0, "سكن أ  —  Residential A", INK, 9.0, "center", w="bold")
    tbl = [("Front", "5 m"), ("Side", "4 m"), ("Rear", "5 m"), ("Coverage", "39 %"),
           ("Floors", "4"), ("Height", "17 m"), ("Green area", "15 %")]
    for i, (k, v) in enumerate(tbl):
        ax.text(11.4, 5.4-i*0.62, k, fontsize=7.2, color=INK2, ha="left")
        ax.text(14.6, 5.4-i*0.62, v, fontsize=7.6, color=INK, ha="right", weight="bold")
    ax.add_patch(mp.Rectangle((11.2, 1.2), 3.7, 4.8, facecolor="#f6f5f0",
                              edgecolor=INK3, lw=0.8, zorder=1))
    ax.set_xlim(-2.0, 15.4); ax.set_ylim(-2.6, 7.8)
    save(fig, 14, "Development control — Residential A (سكن أ)",
         "الأحكام التنظيمية — سكن أ", "Art 16(a)")


def f15():
    fig, ax = newfig(7.2, 4.6)
    ground(ax, -1, 13, 0)
    road(ax, -1, 0.8, 0, 1.1, "road", None)
    fr = 2.1
    for k in range(2):
        blk(ax, 0.8+fr, k*1.5, 7.4, 1.44)
        arabel(ax, 4.9, k*1.5+0.72, f"طابق {k+1}", 8.0, bold=True)
    blk(ax, 0.8+fr+1.0, 3.0, 3.7, 1.2, fc="#f8ded8", ec=BLDE, lw=1.0)
    arabel(ax, 4.9, 3.6, "الروف", 8.4, bold=True)
    dim(ax, (8.6, 0), (8.6, 3.0), "9 m", 0, 1, 7.4, RED)
    note(ax, 9.3, 1.5, "excluding\nthe roof floor", RED, 6.6, "left")
    dim(ax, (0.8, -1.5), (0.8+fr, -1.5), "8 m front", 0, 1, 6.8, BLU)
    note(ax, 4.9, 6.4, "السكن الأخضر / الريفي  —  Green / Rural Residential", INK, 9.0, "center", w="bold")
    tbl = [("Front", "8 m"), ("Side", "6 m"), ("Rear", "6 m"), ("Coverage", "27 %"),
           ("Floors", "2 + roof"), ("Height", "9 m excl. roof"), ("Green area", "10 %")]
    for i, (k, v) in enumerate(tbl):
        ax.text(11.0, 5.0-i*0.62, k, fontsize=7.2, color=INK2, ha="left")
        ax.text(14.7, 5.0-i*0.62, v, fontsize=7.6, color=INK, ha="right", weight="bold")
    ax.add_patch(mp.Rectangle((10.8, 0.8), 4.2, 4.8, facecolor="#f6f5f0",
                              edgecolor=INK3, lw=0.8, zorder=1))
    ax.set_xlim(-2.0, 15.6); ax.set_ylim(-2.6, 7.2)
    save(fig, 15, "Development control — Green / Rural Residential",
         "الأحكام التنظيمية — السكن الأخضر / الريفي", "Art 16(a)")


def f16():
    fig, ax = newfig(7.2, 3.8)
    blk(ax, 0.6, 0, 4.2, 4.0)
    arabel(ax, 2.7, 2.0, "الارتفاع المقرر", 8.6, bold=True)
    blk(ax, 6.2, 0, 4.2, 4.0)
    blk(ax, 6.2, 4.0, 4.2, 1.05, fc="#f8ded8", ec=BLDE, lw=1.1, ls=(0, (4, 2)))
    arabel(ax, 8.3, 4.5, "زيادة", 8.2, "#7a2a1e", bold=True)
    dim(ax, (10.7, 4.0), (10.7, 5.05), "+35 cm", 0, 1, 7.2, GRN)
    note(ax, 2.7, -1.3, "per 100 m² of plot area ABOVE\nthe minimum subdivision area", INK2, 6.9, "center")
    note(ax, 8.3, -1.3, "per 1 m of EXTRA side and\nfront setback  →  +30 cm", INK2, 6.9, "center")
    note(ax, 5.5, 7.4, "Article 16(c) — the height bonuses", INK, 8.6, "center", w="bold")
    note(ax, 5.5, 6.2, "⚠  Article 16(e) disapplies paragraphs (b), (c) and (d) — and therefore these bonuses —\n"
                       "for green, rural and agricultural zones, specially-regulated areas,\n"
                       "AND for any plot served by roads narrower than 20 m.", RED, 7.1, "center")
    ax.set_xlim(-0.6, 12.4); ax.set_ylim(-2.6, 8.4)
    save(fig, 16, "The height bonuses of Article 16(c) — and when they vanish",
         "زيادة الارتفاع وفق المادة ١٦(ج) واستثناءاتها", "Art 16(c)(e)")


def f17():
    fig, ax = newfig(7.0, 3.6)
    for i, (w, ok) in enumerate([(10, False), (14, False), (20, True), (24, True)]):
        x = i*3.3
        c = GRN if ok else RED
        ax.add_patch(mp.Rectangle((x, 0), 2.6, w/24*2.2, facecolor="#e6e4dc",
                                  edgecolor=INK3, lw=0.8))
        ax.text(x+1.3, w/24*2.2/2, f"{w} m", ha="center", va="center",
                fontsize=8.6, color=INK, weight="bold")
        ax.text(x+1.3, -0.55, "✓ bonuses apply" if ok else "✗ no bonuses",
                ha="center", fontsize=7.0, color=c, weight="bold")
    note(ax, 5.3, 3.6, "Article 16(e) — plots served by roads NARROWER THAN 20 m are excluded from the\n"
                       "high-building table, the height bonuses and the 60 m provision alike.",
         INK, 7.4, "center", w="bold")
    arabel(ax, 5.3, 2.7, "والقطع المخدومة بطرق تقل سعتها عن (٢٠)م", 9.0, INK2)
    ax.set_xlim(-0.6, 13.4); ax.set_ylim(-1.6, 4.6)
    save(fig, 17, "The 20 m road test of Article 16(e)",
         "اختبار الطريق ٢٠ متراً — المادة ١٦(هـ)", "Art 16(e)")


def f18():
    fig, ax = newfig(6.8, 3.8)
    ground(ax, -1, 12, 0)
    road(ax, -1, 1.0, 0, 1.2, "≥ 14 m street", None)
    for k in range(4):
        blk(ax, 2.6, k*1.0, 6.6, 0.95)
    blk(ax, 2.6, 4.0, 6.6, 1.0, fc="#f8ded8", ec=BLDE, lw=1.2, ls=(0, (4, 2)))
    arabel(ax, 5.9, 4.5, "طابق إضافي", 8.6, "#7a2a1e", bold=True)
    dim(ax, (9.5, 4.0), (9.5, 5.0), "≤ 4 m", 0, 1, 7.2, GRN)
    note(ax, 5.9, 7.2, "Article 16(f) — an ADDITIONAL floor of up to 4 m may be licensed on plots fronting\n"
                       "streets of not less than 14 m, subject to providing that floor's parking.",
         INK, 7.4, "center", w="bold")
    note(ax, 5.9, 6.1, "Not available where the plot's planning scheme was ratified before 16/1/2018.",
         RED, 7.0, "center")
    ax.set_xlim(-2.0, 12.6); ax.set_ylim(-1.8, 8.0)
    save(fig, 18, "The additional floor — Article 16(f)",
         "الطابق الإضافي — المادة ١٦(و)", "Art 16(f)")


def f19():
    fig, ax = newfig(7.0, 3.4)
    items = [("مواقف سيارات", "parking"), ("آبار وخزانات\nمياه خرسانية", "RC water tanks"),
             ("غرف التخزين", "storage"), ("غرف التدفئة\nوالتبريد والوقود", "heating / cooling / fuel"),
             ("غرف الكهرباء", "electrical rooms")]
    for i, (a, e) in enumerate(items):
        x = i*2.6
        blk(ax, x, 0, 2.3, 1.9, fc="#dfe9d9", ec=GRDE, lw=1.1)
        arabel(ax, x+1.15, 1.30, a, 7.6, "#2c5c1c", bold=True)
        ax.text(x+1.15, 0.45, e, ha="center", fontsize=6.4, color="#2c5c1c")
    note(ax, 6.2, 3.3, "Article 38(a) — the only permitted uses of the basement",
         INK, 7.8, "center", w="bold")
    note(ax, 6.2, -1.0, "It cannot be habitable and cannot be sold as accommodation.", RED, 7.4, "center", w="bold")
    ax.set_xlim(-0.6, 13.0); ax.set_ylim(-2.0, 4.2)
    save(fig, 19, "Permitted uses of the basement",
         "استعمالات طابق القبو المسموح بها", "Art 38(a)")


def f20():
    fig, ax = newfig(7.2, 4.4)
    ground(ax, -1, 13, 0)
    road(ax, -1, 1.2, 0, 1.3, None, None)
    ax.text(0.1, -0.65, "street width L", fontsize=7.0, color=INK2)
    fr = 2.2
    blk(ax, 1.2+fr, 0, 6.6, 6.2)
    ax.plot([1.2+fr]*2, [0, 6.6], color=BLDE, lw=1.4, ls=(0, (5, 3)), zorder=9)
    blk(ax, 1.2+fr-1.4, 2.4, 1.4, 0.35, fc="#f8ded8", ec=BLDE, lw=1.0)
    dim(ax, (1.2+fr-1.4, 3.1), (1.2+fr, 3.1), "balcony", 0, 1, 6.6, BLU)
    blk(ax, 1.2+fr-0.6, 4.4, 0.6, 0.3, fc="#eceae2", ec=INK3, lw=0.9)
    dim(ax, (1.2+fr-0.6, 5.0), (1.2+fr, 5.0), "≤ 60 cm", 0, 1, 6.6, INK2)
    blk(ax, 1.2+fr-1.1, 0.9, 1.1, 0.22, fc="#efe7d6", ec="#9a7b2e", lw=0.9)
    note(ax, 1.2+fr-1.2, 0.55, "entrance canopy", "#9a7b2e", 6.4, "right")
    rows = [("street ≥ 16 m", "balcony ≤ 1.40 m", GRN),
            ("street < 16 m", "balcony ≤ 1.20 m", "#9a7b2e"),
            ("street ≤ 12 m", "NO projection at all", RED),
            ("architectural", "≤ 0.60 m within the setback", INK2)]
    ax.add_patch(mp.Rectangle((10.4, 1.4), 5.4, 3.9, facecolor="#f6f5f0", edgecolor=INK3, lw=0.9, zorder=11))
    for i, (k, v, c) in enumerate(rows):
        ax.text(10.7, 4.72-i*0.90, k, fontsize=7.0, color=INK2, zorder=12)
        ax.text(10.7, 4.40-i*0.90, v, fontsize=7.2, color=c, weight="bold", zorder=12)
    note(ax, 6.0, 8.4, "Article 29 — projections into and over the front setback", INK, 8.0, "center", w="bold")
    ax.set_xlim(-1.6, 16.4); ax.set_ylim(-1.8, 9.2)
    save(fig, 20, "Projections — balconies, architectural projections and canopies",
         "البروز — الشرفات والبروز المعماري ومظلة المدخل", "Art 29")


def f21():
    fig, ax = newfig(6.6, 3.2)
    ground(ax, -1, 11, 0)
    road(ax, -1, 1.0, 0, 1.0, "road", None)
    blk(ax, 2.4, 0, 6.6, 3.4)
    ax.plot([2.4, 9.0], [3.4]*2, color=BLDE, lw=1.6, zorder=9)
    blk(ax, 2.4, 3.4, 6.6, 0.55, fc="#eceae2", ec=INK3, lw=1.1)
    arabel(ax, 5.7, 3.68, "التصوينة", 8.4, INK2, bold=True)
    dim(ax, (9.4, 3.4), (9.4, 3.95), "parapet", 0, 1, 7.0, INK2)
    note(ax, 5.7, 6.2, "Article 32 — the roof parapet", INK, 8.0, "center", w="bold")
    note(ax, 5.7, 5.2, "Required on the roof of the last floor, to the height and specification\n"
                       "the Regulation prescribes.  See the Article 32 record for the dimension.",
         INK2, 7.0, "center")
    ax.set_xlim(-1.6, 11.6); ax.set_ylim(-1.4, 7.0)
    save(fig, 21, "The roof parapet", "التصوينة", "Art 32")


def f22():
    fig, ax = newfig(7.2, 3.8)
    ground(ax, -1, 13, 0)
    road(ax, -1, 1.0, 0, 1.0, "road", None)
    blk(ax, 1.0, 0, 0.22, 1.5, fc="#eceae2", ec=INK3, lw=1.1)
    dim(ax, (0.55, 0), (0.55, 1.5), "1.50 m", 0, 1, 7.0, BLU)
    note(ax, 0.3, 1.9, "FRONT fence", BLU, 6.8, "center")
    blk(ax, 11.6, 0, 0.22, 2.0, fc="#eceae2", ec=INK3, lw=1.1)
    dim(ax, (12.25, 0), (12.25, 2.0), "2.00 m", 0, 1, 7.0, BLU)
    note(ax, 12.5, 2.4, "REAR / SIDE fence", BLU, 6.8, "center")
    ax.add_patch(mp.Rectangle((1.3, 0), 2.4, 1.0, facecolor="#e0d5b8",
                              edgecolor="#8a7b55", lw=1.0, hatch="///", zorder=5))
    arabel(ax, 2.5, 0.5, "طمم", 8.2, "#5a4c2e", bold=True)
    dim(ax, (3.95, 0), (3.95, 1.0), "≤ 1 m", 0, 1, 7.0, RED)
    blk(ax, 4.6, 0, 6.6, 3.2)
    arabel(ax, 7.9, 1.6, "البناء", 10, bold=True)
    note(ax, 6.0, 6.0, "Article 33(b) — fences measured from NATURAL ground, and the 1 m cap on fill",
         INK, 7.6, "center", w="bold")
    note(ax, 6.0, 5.0, "Fill within the setbacks may not exceed 1 m above natural ground at its location —\n"
                       "which removes platforming as a strategy on any steep site.", RED, 7.1, "center")
    ax.set_xlim(-1.8, 14.6); ax.set_ylim(-1.4, 6.8)
    save(fig, 22, "Fences and the 1 m cap on fill within the setbacks",
         "الأسوار والطمم في الارتدادات", "Art 33(b)")


def f23():
    fig, ax = newfig(7.2, 3.8)
    gy = lambda x: 0 if x < 2 else min((x-2)*0.45, 3.2)
    ground(ax, -1, 13, gy)
    road(ax, -1, 1.2, 0, 1.0, "lower street", None)
    fr = 2.0
    ax.add_patch(mp.Rectangle((1.2, 0), fr, 0.45, facecolor="#dfe9d9",
                              edgecolor=GRDE, lw=1.3, zorder=7))
    dim(ax, (1.2, 0.95), (1.2+fr, 0.95), "setback deck", 0, 1, 6.8, GRN)
    dim(ax, (1.05, 0), (1.05, 0.45), "≤ 45 cm", 0, 1, 6.8, RED)
    blk(ax, 1.2+fr, 0, 6.4, 3.6)
    arabel(ax, 5.4, 1.8, "البناء", 10, bold=True)
    ax.add_patch(mp.Rectangle((1.3, -1.4), fr+6.2, 1.3, facecolor="#dfe9d9",
                              edgecolor=GRDE, lw=1.0, ls=(0, (4, 2)), zorder=6))
    ax.text(4.9, -1.95, "beneath: parking · vehicle passages · tanks · plant · non-commercial storage",
            ha="center", fontsize=6.4, color="#2c5c1c")
    note(ax, 6.0, 6.6, "Article 33(d) — decking the setbacks", INK, 8.0, "center", w="bold")
    note(ax, 6.0, 5.5, "Requires an accurate topographic plan with the application.  The deck must support the\n"
                       "street, the retaining wall or the rock cut.  Where the plot fronts more than one street the\n"
                       "deck may be on the UPPER street side, the LOWER, or both.  Deck area is excluded from\n"
                       "the total built area AND from the floor area.", INK2, 6.9, "center")
    ax.set_xlim(-1.8, 14.0); ax.set_ylim(-3.0, 7.4)
    save(fig, 23, "Decking the setbacks — excluded from both ratios",
         "سقف الارتدادات — يستثنى من المساحة الإجمالية والطابقية", "Art 33(d)")


def f24():
    fig, ax = newfig(6.8, 3.4)
    ground(ax, -1, 12, 0)
    road(ax, -1, 1.0, 0, 1.0, "road", None)
    fr = 1.8
    blk(ax, 1.0+fr, 0, 5.2, 3.2)
    arabel(ax, 3.6+fr/2+0.4, 1.6, "البناء الرئيسي", 9.0, bold=True)
    blk(ax, 8.6, 0, 2.2, 1.35, fc="#efe7d6", ec="#9a7b2e", lw=1.2)
    arabel(ax, 9.7, 0.68, "بناء فرعي", 8.2, "#7a5f14", bold=True)
    dim(ax, (11.2, 0), (11.2, 1.35), "≤ 2.60 m", 0, 1, 7.0, "#9a7b2e")
    dim(ax, (6.2, -0.8), (8.6, -0.8), "detached", 0, 1, 6.8, RED)
    note(ax, 6.0, 5.6, "Article 34 — the ancillary building", INK, 8.0, "center", w="bold")
    note(ax, 6.0, 4.6, "≤ 5% of the plot area and in no case more than 25 m² · external height ≤ 2.60 m\n"
                       "from natural ground · IN ADDITION to the permitted coverage · must NOT be attached\n"
                       "to the building on the plot · no opening onto its roof and the roof is not to be used.",
         INK2, 6.9, "center")
    ax.set_xlim(-1.6, 13.2); ax.set_ylim(-1.8, 6.4)
    save(fig, 24, "The ancillary building — additional to the coverage",
         "البناء الفرعي — إضافة إلى النسبة المئوية المسموح بها", "Art 34")


def f25():
    fig, ax = newfig(6.6, 4.2)
    W, H = 10, 8
    ax.add_patch(mp.Rectangle((0, 0), W, H, facecolor="#faf9f5", edgecolor=INK, lw=1.7, zorder=2))
    fr, sd, rr = 2.0, 1.4, 1.5
    blk(ax, sd, fr, W-2*sd, H-fr-rr, fc=BLD, ec=BLDE, lw=1.2, z=5)
    arabel(ax, W/2, (fr+H-rr)/2, "البناء", 10, bold=True)
    ax.add_patch(mp.Rectangle((0, fr), sd, 3.2, facecolor=CAR, edgecolor=CARE, lw=1.0, zorder=6))
    ax.add_patch(mp.Rectangle((W-sd, fr), sd, 3.2, facecolor=CAR, edgecolor=CARE, lw=1.0, zorder=6))
    ax.add_patch(mp.Rectangle((sd, H-rr), W-2*sd, rr, facecolor=CAR, edgecolor=CARE, lw=1.0, zorder=6))
    ax.add_patch(mp.Rectangle((0, 0), W, fr, facecolor="#fbe4e1", edgecolor=RED,
                              lw=1.2, hatch="xx", zorder=6))
    ax.text(W/2, fr/2, "✗  NOT in the front setback\n(residential zones)", ha="center", va="center",
            fontsize=7.0, color=RED, weight="bold", zorder=9,
            bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=RED, lw=0.8, alpha=0.95))
    ax.text(sd/2, fr+1.6, "✓", ha="center", fontsize=13, color=GRN, weight="bold", zorder=8)
    ax.text(W-sd/2, fr+1.6, "✓", ha="center", fontsize=13, color=GRN, weight="bold", zorder=8)
    ax.text(W/2, H-rr/2, "✓  side and rear setbacks", ha="center", va="center",
            fontsize=7.0, color=GRN, weight="bold", zorder=8)
    road(ax, -1.2, W+1.2, 0, 1.2, "road", None)
    note(ax, W/2, -2.6, "Article 36(c) forbids parking in the front setback in residential zones.\n"
                        "Article 36(d) permits open parking in the side and rear setbacks, subject to clear\n"
                        "width, an entry opening not less than that width, the front setback kept clear,\n"
                        "and manoeuvring entirely within the plot.", INK2, 6.9, "center")
    ax.set_xlim(-1.8, W+1.8); ax.set_ylim(-4.4, H+0.8)
    save(fig, 25, "Where parking may and may not go in the setbacks",
         "مواقف السيارات في الارتدادات", "Art 36(c)(d)")


def f26():
    fig, ax = newfig(7.4, 4.0)
    cases = [(0, "parallel", "الوقوف الموازي", 5.50, 2.50, 4.00),
             (1, "30°", "زاوية ٣٠ درجة", 5.25, 2.50, 4.00),
             (2, "45°", "زاوية ٤٥ درجة", 5.25, 2.50, 5.00),
             (3, "90°", "زاوية ٩٠ درجة", 5.25, 2.50, 5.50)]
    for i, (k, en, a, L, Wd, aisle) in enumerate(cases):
        x = i*4.3
        ax.add_patch(mp.Rectangle((x, 0), 3.6, 1.0, facecolor="#e6e4dc",
                                  edgecolor=INK3, lw=0.8, zorder=2))
        ax.text(x+1.8, 0.5, f"aisle {aisle:.2f} m", ha="center", va="center",
                fontsize=6.8, color=INK2, zorder=3)
        if k == 0:
            for j in range(2):
                ax.add_patch(mp.Rectangle((x+0.15+j*1.75, 1.15), 1.6, 0.72,
                                          facecolor=CAR, edgecolor=CARE, lw=0.9, zorder=5))
        elif k == 3:
            for j in range(4):
                ax.add_patch(mp.Rectangle((x+0.12+j*0.88, 1.15), 0.76, 1.5,
                                          facecolor=CAR, edgecolor=CARE, lw=0.9, zorder=5))
        else:
            ang = 30 if k == 1 else 45
            for j in range(4):
                r = mp.Rectangle((x+0.05+j*0.88, 1.15), 0.72, 1.5, facecolor=CAR,
                                 edgecolor=CARE, lw=0.9, zorder=5,
                                 angle=-(90-ang))
                ax.add_patch(r)
        ax.text(x+1.8, 3.25, en, ha="center", fontsize=8.0, color=INK, weight="bold")
        arabel(ax, x+1.8, 2.92, a, 7.4, INK2)
        ax.text(x+1.8, -0.45, f"bay  {L:.2f} × {Wd:.2f} m", ha="center", fontsize=6.9, color=INK2)
    note(ax, 8.6, 4.5, "Article 37(a) — minimum parking bay and aisle dimensions by parking angle",
         INK, 7.8, "center", w="bold")
    note(ax, 8.6, -1.5, "Article 37(b): the average area allotted per bay is 25 m², including the turning aisles.\n"
                        "Article 37(c): clear height not less than 2.25 m to the underside of any structure or service.",
         INK2, 6.9, "center")
    ax.set_xlim(-0.8, 18.0); ax.set_ylim(-2.6, 5.4)
    save(fig, 26, "Parking bay and aisle dimensions by angle",
         "أبعاد مواقف السيارات وممراتها حسب زاوية الاصطفاف", "Art 37")


def f27():
    fig, ax = newfig(7.0, 3.6)
    ground(ax, -1, 13, 0)
    blk(ax, 1.0, 0, 10.4, 2.6, fc="#f6f5f0", ec=INK3, lw=1.1)
    ax.add_patch(Poly([(1.4, 0.2), (5.0, -2.4), (8.4, -2.4), (4.8, 0.2)],
                      closed=True, facecolor="#e6e4dc", edgecolor=INK3, lw=1.0, zorder=5))
    ax.text(4.9, -1.2, "ramp", ha="center", fontsize=7.2, color=INK2, rotation=-32, zorder=6)
    ax.add_patch(mp.Rectangle((8.8, -2.4), 3.0, 2.2, facecolor="#dfe9d9",
                              edgecolor=GRDE, lw=1.1, zorder=4))
    arabel(ax, 10.3, -0.55, "المرآب", 9.0, "#2c5c1c", bold=True)
    for j in range(3):
        ax.add_patch(mp.Rectangle((9.0+j*0.95, -2.2), 0.8, 0.85,
                                  facecolor=CAR, edgecolor=CARE, lw=0.8, zorder=6))
    dim(ax, (12.1, -2.4), (12.1, -0.2), "clear 2.25 m", 0, 1, 6.8, BLU)
    note(ax, 6.0, 5.6, "Article 38 — entry and exit passages, internal aisles and curves", INK, 7.8, "center", w="bold")
    note(ax, 6.0, 4.5, "The Regulation fixes the longitudinal section (ramp gradient), the cross-section\n"
                       "(ramp width) and the turning radii.  The governing figures are in the Article 38 record.",
         INK2, 6.9, "center")
    ax.set_xlim(-1.4, 14.4); ax.set_ylim(-3.6, 6.4)
    save(fig, 27, "Garage ramps and internal circulation",
         "ممرات الدخول والخروج والممرات الداخلية للمرآب", "Art 38")


def f28():
    fig, ax = newfig(7.4, 3.8)
    bands = [("≤ 1,000 m²", 7, 4, 4, "10 %"), ("1,001–2,000", 8, 5, 5, "10 %"),
             ("2,001–4,000", 10, 5, 7, "10 %"), ("> 4,000 m²", 15, 5, 10, "10 %*")]
    for i, (b, fr, sd, rr, cov) in enumerate(bands):
        x = i*4.4
        ax.add_patch(mp.Rectangle((x, 0), 3.7, 3.4, facecolor="#faf9f5",
                                  edgecolor=INK, lw=1.3, zorder=2))
        w = 3.7 - 2*(sd/15*1.1); h = 3.4 - (fr/15*1.1) - (rr/15*1.1)
        blk(ax, x+sd/15*1.1, fr/15*1.1, w, h, z=4)
        ax.text(x+1.85, 3.75, b, ha="center", fontsize=7.6, color=INK, weight="bold")
        ax.text(x+1.85, -0.42, f"front {fr} · side {sd} · rear {rr}", ha="center",
                fontsize=6.7, color=INK2)
        ax.text(x+1.85, -0.78, f"coverage {cov}", ha="center", fontsize=6.9, color=BLU, weight="bold")
    note(ax, 8.6, 5.1, "Article 44 — residential buildings OUTSIDE the planning areas", INK, 8.0, "center", w="bold")
    note(ax, 8.6, -1.7, "All four bands: 2 floors + roof, height 9 m excluding the roof floor.\n"
                        "* above 4,000 m² the 10% is capped at 1,000 m².  Article 44(b) allows a 20 m² service\n"
                        "building in the front setback, not counted in the coverage.", INK2, 6.9, "center")
    ax.set_xlim(-0.6, 17.8); ax.set_ylim(-2.9, 5.9)
    save(fig, 28, "Outside the planning areas — the Article 44 bands",
         "ترخيص الأبنية السكنية خارج مناطق التنظيم", "Art 44")


def f29():
    fig, ax = newfig(6.8, 3.8)
    ground(ax, -1, 12, 0)
    for k in range(3):
        blk(ax, 1.4, k*1.25, 8.2, 1.2)
        arabel(ax, 5.5, k*1.25+0.6, f"طابق {k+1}", 7.8, bold=True)
    top = 3.75
    blk(ax, 2.6, top, 4.1, 1.15, fc="#f8ded8", ec=BLDE, lw=1.2)
    arabel(ax, 4.65, top+0.58, "الروف", 8.8, "#7a2a1e", bold=True)
    dim(ax, (10.0, top), (10.0, top+1.15), "≤ 3.50 m", 0, 1, 7.0, RED)
    dim(ax, (1.4, top+1.5), (2.6, top+1.5), "≥ ½ setback", 0, 1, 6.6, BLU)
    dim(ax, (6.7, top+1.5), (9.6, top+1.5), "", 0, 1, 6.6, BLU)
    note(ax, 5.5, 7.2, "Article 48(a) — the roof floor", INK, 8.0, "center", w="bold")
    note(ax, 5.5, 6.2, "Area ≤ 50% of the floor below · height ≤ 3.50 m above that floor's slab ·\n"
                       "setbacks on all sides ≥ HALF the prescribed setbacks, excluding the stair house and lift.",
         INK2, 6.9, "center")
    ax.set_xlim(-1.4, 12.6); ax.set_ylim(-1.4, 8.0)
    save(fig, 29, "The roof floor — 50%, 3.50 m, half setbacks",
         "طابق الروف — النسبة والارتفاع والارتدادات", "Art 48(a)")


def f30():
    fig, ax = newfig(6.8, 3.4)
    xs = np.linspace(0, 11, 200)
    ys = 0.42*xs
    ax.fill_between(xs, ys-3, ys, color=GRD, zorder=1)
    ax.plot(xs, ys, color=GRDE, lw=2.0, zorder=4)
    blk(ax, 3.2, 0.42*3.2, 4.0, 2.4, fc="#fbe4e1", ec=RED, lw=1.4, ls=(0, (4, 2)))
    ax.text(5.2, 0.42*3.2+1.2, "✗", ha="center", va="center", fontsize=22, color=RED,
            weight="bold", zorder=9)
    note(ax, 5.5, 6.8, "Article 47(s) — no building on designated steep or unstable land", INK, 7.8, "center", w="bold")
    arabel(ax, 5.5, 5.9, "لا يجوز البناء في الأراضي الخلاء المقيدة أو الشديدة الانحدار والقابلة للانهيار أو الانزلاق", 8.4, INK2)
    note(ax, 5.5, -1.5, "The prohibition bites only where the APPROVED ZONING PLAN so designates the land —\n"
                        "it is not a free-standing gradient test.  Confirm the designation in writing.",
         INK2, 6.9, "center")
    ax.set_xlim(-0.8, 12.4); ax.set_ylim(-2.6, 7.6)
    save(fig, 30, "Steeply sloping and unstable land",
         "الأراضي الشديدة الانحدار والقابلة للانهيار أو الانزلاق", "Art 47(s)")


def f31():
    fig, ax = newfig(6.8, 3.2)
    ax.add_patch(mp.Rectangle((0, 0), 11, 3.4, facecolor="#faf9f5", edgecolor=INK, lw=1.4, zorder=2))
    arabel(ax, 5.5, 1.8, "أرض المشروع", 10.5, INK, bold=True)
    ax.text(5.5, 1.15, "the project land", ha="center", fontsize=7.2, color=INK2)
    road(ax, -1.6, 12.6, 0, 1.5, None, None)
    dim(ax, (-1.2, -1.5), (-1.2, 0), "≥ 12 m", 0, 1, 7.6, GRN, rot=90)
    ax.text(5.5, -0.75, "the street reaching the project land", ha="center",
            va="center", fontsize=7.2, color=INK2)
    note(ax, 5.5, 5.2, "Article 10(f) — ADDED by the 2025 amending Regulation No. (12)", INK, 7.8, "center", w="bold")
    arabel(ax, 5.5, 4.35, "باستثناء مشاريع الطاقة المتجددة يجب ألا تقل سعة الشارع الواصل لأرض المشروع عن (١٢) متراً", 8.4, INK2)
    note(ax, 5.5, -2.6, "Renewable-energy projects are excepted.", INK2, 7.0, "center")
    ax.set_xlim(-2.6, 13.6); ax.set_ylim(-3.6, 5.8)
    save(fig, 31, "The 12 m street serving an investment project — 2025 amendment",
         "سعة الشارع الواصل لأرض المشروع — تعديل ٢٠٢٥", "Art 10(f) / 2025")


def f32():
    fig, ax = newfig(7.2, 3.8)
    boxes = [("area of the\nENCROACHMENT", "مساحة التجاوز", "#eef3fb", BLU),
             ("value of the m²\nas assessed by DLS", "قيمة المتر المربع", "#eef3fb", BLU),
             ("= FEE PAYABLE", "الرسم المستحق", "#e7f4ec", GRN)]
    for i, (en, a, fc, ec) in enumerate(boxes):
        x = i*4.6
        ax.add_patch(mp.Rectangle((x, 1.4), 3.6, 1.9, facecolor=fc, edgecolor=ec, lw=1.3, zorder=3))
        ax.text(x+1.8, 2.62, en, ha="center", va="center", fontsize=7.2, color=INK, weight="bold")
        arabel(ax, x+1.8, 1.85, a, 8.0, ec)
        if i < 2:
            ax.text(x+4.1, 2.35, "×" if i == 0 else "=", ha="center", va="center",
                    fontsize=15, color=INK2, weight="bold")
    ax.add_patch(mp.Rectangle((9.2, -1.5), 3.6, 2.3, facecolor="#fdf3e7",
                              edgecolor="#9a7b2e", lw=1.2, zorder=3))
    ax.text(11.0, 0.25, "but CAPPED between\nthe max and min\nper m² in the table",
            ha="center", va="center", fontsize=7.0, color="#7a5f14", weight="bold")
    ax.annotate("", xy=(11.0, 0.9), xytext=(11.0, 1.4),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#9a7b2e"))
    note(ax, 6.4, 5.4, "Article 20(b) — how an encroachment fee is computed", INK, 8.0, "center", w="bold")
    note(ax, 6.4, -2.8, "Levied IN ADDITION to the Article 19 licensing fees.  Second-category municipalities\n"
                        "pay 60% and third-category 50% of the item (3) fees.  Encroachments arising after\n"
                        "1/1/2017 may not be licensed at all unless technical and beyond the owner's control.",
         INK2, 6.9, "center")
    ax.set_xlim(-0.8, 13.8); ax.set_ylim(-4.0, 6.0)
    save(fig, 32, "How an encroachment fee is computed",
         "طريقة احتساب رسوم التجاوز على الأحكام التنظيمية", "Art 20(b)")


if __name__ == "__main__":
    for f in [f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12, f13,
              f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26,
              f27, f28, f29, f30, f31, f32]:
        f()
    json.dump(IDX, open(HERE + "/figs_index.json", "w"), ensure_ascii=False, indent=1)
    print("figures:", len(IDX))
