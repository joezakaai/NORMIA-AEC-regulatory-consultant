import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
"""Figures for the architect's capacity study - Plot 3+4, Parcel 96, Makawir."""
import math, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon as MplPoly
from matplotlib.font_manager import FontProperties
import arabic_reshaper
from bidi.algorithm import get_display
from calc import (PLOT, A, B, C, D, ENV_A, S_FRONT, N_FRONT, W_SIDE, E_SIDE,
                  AREA_LEGAL, cov_max, env_a_area, floor_area, green_min, gf, ff,
                  roof_max, far, base_env, DATUM, CEIL, CEIL_R, Z, shoelace)

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
RED, VIOLET, YELLOW = "#e34948", "#4a3aa7", "#eda100"
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8880"
SURF = "#fcfcfb"
GROUND = "#cfc6ad"; GROUND_L = "#8a7b55"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF,
                     "savefig.facecolor": SURF})
AR = FontProperties(fname="/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf", size=9)
ar = lambda s: get_display(arabic_reshaper.reshape(s))
OUT = HERE + "/fig"


# ===================================================== F1  SITE PLAN
def fig_site():
    fig, ax = plt.subplots(figsize=(7.0, 7.4))
    ax.add_patch(MplPoly([tuple(p) for p in PLOT], closed=True,
                         facecolor="#f2f1ea", edgecolor=INK, lw=2.0, zorder=3))
    ax.add_patch(MplPoly([tuple(p) for p in ENV_A], closed=True,
                         facecolor=BLUE, alpha=0.16, edgecolor="none", zorder=4))
    ax.add_patch(MplPoly([tuple(p) for p in ENV_A], closed=True, facecolor="none",
                         edgecolor=BLUE, lw=1.5, ls=(0, (6, 3)), zorder=6))

    # --- indicative terraced footprint: 8 units in 2 rows stepping down west
    ex = np.array(ENV_A); x0, x1 = ex[:, 0].min(), ex[:, 0].max()
    y0, y1 = ex[:, 1].min(), ex[:, 1].max()
    uw, uh = 13.0, 10.4                      # 135 m2 each
    gapx, gapy = 5.0, 5.6
    ox = x0 + 1.4; oy = y0 + 2.0
    for r in range(4):
        for c_ in range(2):
            px = ox + c_*(uw+gapx); py = oy + r*(uh+gapy)
            ax.add_patch(mpatches.Rectangle((px, py), uw, uh, facecolor=ORANGE,
                         alpha=0.62, edgecolor="#a83f10", lw=0.9, zorder=7))

    # --- roads
    ax.add_patch(mpatches.Rectangle((-8, -11.0), S_FRONT+34, 10.0,
                 facecolor="#e4e2d9", edgecolor=INK3, lw=0.8, zorder=1))
    ax.text(S_FRONT/2-3, -6.0, ar("شارع 10 متر"), ha="center", va="center",
            fontproperties=AR, color=INK2)
    ax.text(S_FRONT/2+11, -6.0, "10 m street", ha="center", va="center",
            fontsize=8.4, color=INK2, weight="bold")
    ny = max(C[1], D[1])
    ax.add_patch(mpatches.Rectangle((-8, ny+0.6), N_FRONT+34, 6.0,
                 facecolor="#e4e2d9", edgecolor=INK3, lw=0.8, zorder=1))
    ax.text(N_FRONT/2-3, ny+3.6, ar("طريق 6 متر"), ha="center", va="center",
            fontproperties=AR, color=INK2)
    ax.text(N_FRONT/2+11, ny+3.6, "6 m road", ha="center", va="center",
            fontsize=8.4, color=INK2, weight="bold")

    # --- dimensions, kept clear of the neighbour captions
    def dim(p, q, txt, off, rot):
        p, q = np.array(p), np.array(q)
        v = q-p; n = np.array([-v[1], v[0]]); n /= np.linalg.norm(n)
        if np.dot((p+q)/2 - np.mean(PLOT, axis=0), n) < 0: n = -n
        a2, b2 = p+n*off, q+n*off
        ax.annotate("", xy=tuple(b2), xytext=tuple(a2),
                    arrowprops=dict(arrowstyle="<->", lw=0.8, color=INK2, shrinkA=0, shrinkB=0))
        m = (a2+b2)/2 + n*2.2
        ax.text(m[0], m[1], txt, ha="center", va="center", fontsize=7.6,
                color=INK2, rotation=rot, weight="bold")
    dim(A, B, f"{S_FRONT:.2f} m", 13.5, 0)
    dim(C, D, f"{N_FRONT:.2f} m", 9.0, 0)
    dim(D, A, f"{W_SIDE:.2f} m", 13.0, 90)
    dim(B, C, f"{E_SIDE:.2f} m", 10.5, 90)
    ax.text(-19.5, W_SIDE*0.62, "Parcel 321  ·  no road", fontsize=7.4,
            color=INK3, rotation=90, ha="center", va="center")
    ax.text(S_FRONT+20.0, E_SIDE*0.30, "Plots 1 & 2  ·  no road", fontsize=7.4,
            color=INK3, rotation=90, ha="center", va="center")

    # --- setback callouts
    for p, q, lab, dx in [(A, B, "8 m front", 5.2), (C, D, "8 m front", 5.2),
                          (D, A, "6 m side", 4.4), (B, C, "6 m side", 4.4)][:2]:
        mid = (np.array(p)+np.array(q))/2
        v = np.mean(PLOT, axis=0)-mid; v /= np.linalg.norm(v)
        ax.text(*(mid+v*dx), lab, ha="center", va="center", fontsize=7.0, color=BLUE,
                zorder=10, weight="bold",
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=BLUE, lw=0.6, alpha=0.95))

    for yy in (W_SIDE*0.22, W_SIDE*0.22):
        pass
    for lab, px, py in [("6 m side", 3.6, W_SIDE*0.30), ("6 m side", S_FRONT-3.6, E_SIDE*0.30)]:
        ax.text(px, py, lab, ha="center", va="center", fontsize=7.0, color=BLUE,
                rotation=90, zorder=10, weight="bold",
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=BLUE, lw=0.6, alpha=0.95))

    # --- levels
    for txt, pos in [("+15.0", (N_FRONT-5.5, W_SIDE-5.0)), ("+4.5", (5.5, W_SIDE-5.0)),
                     ("+12.0", (S_FRONT-5.5, 5.0)), ("0.0", (5.0, 5.0))]:
        ax.text(*pos, txt, fontsize=7.6, color="#0b5c40", ha="center", va="center",
                weight="bold", zorder=11,
                bbox=dict(boxstyle="circle,pad=0.22", fc="white", ec=AQUA, lw=1.0))

    # --- slope + view direction (west, toward the Dead Sea)
    yA = W_SIDE*0.70
    ax.annotate("", xy=(-11.0, yA), xytext=(S_FRONT-1.0, yA),
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color=AQUA), zorder=12)
    ax.text((S_FRONT-12)/2, yA+1.6, "ground falls  ≈ 25%  west", fontsize=7.8,
            color="#0b5c40", weight="bold", ha="center", va="bottom", zorder=13,
            bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=AQUA, lw=0.7, alpha=0.95))
    ax.text(-26.0, W_SIDE*0.30, "DEAD  SEA", fontsize=10.0, color=BLUE,
            weight="bold", ha="center", va="center", rotation=90)
    ax.text(-21.0, W_SIDE*0.30, "2.0 km  ·  the view", fontsize=7.6, color=BLUE,
            ha="center", va="center", rotation=90)
    ax.annotate("", xy=(-29.5, W_SIDE*0.30), xytext=(-29.5, W_SIDE*0.30+14),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=BLUE))

    # --- north
    ax.annotate("", xy=(S_FRONT+22, W_SIDE*0.90), xytext=(S_FRONT+22, W_SIDE*0.76),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=INK))
    ax.text(S_FRONT+22, W_SIDE*0.925, "N", ha="center", fontsize=10, weight="bold", color=INK)

    h = [mpatches.Patch(fc="#f2f1ea", ec=INK, label=f"Plot 3+4 combined  —  {AREA_LEGAL:,.0f} m²"),
         mpatches.Patch(fc=BLUE, alpha=0.16, ec=BLUE, label=f"Buildable envelope  —  {env_a_area:,.0f} m²"),
         mpatches.Patch(fc=ORANGE, alpha=0.62, ec="#a83f10",
                        label=f"Max footprint 27%  —  {cov_max:,.0f} m²   (shown as 8 terraced units)")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.46, -0.015),
              frameon=False, fontsize=8.0, handlelength=1.6)
    ax.set_xlim(-38, S_FRONT+30); ax.set_ylim(-14, W_SIDE+10)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(f"{OUT}_site.png", dpi=215, bbox_inches="tight"); plt.close(fig)


# ===================================================== F2  SECTION
def fig_section():
    fig, ax = plt.subplots(figsize=(7.6, 4.7))
    W = 47.6
    gx = np.linspace(0, W, 300)
    gy = np.interp(gx, [0, 6, 18, 30, 40, W], [0.0, 1.4, 5.2, 9.2, 12.4, 13.4])
    g = lambda x: float(np.interp(x, gx, gy))
    ax.fill_between(gx, -9, gy, color=GROUND, zorder=1)
    ax.plot(gx, gy, color=GROUND_L, lw=2.0, zorder=9)

    ax.axhline(DATUM, color=BLUE, lw=1.5, ls=(0, (7, 4)), zorder=4)
    ax.axhline(CEIL, color=RED, lw=2.2, zorder=10)
    ax.axhline(CEIL_R, color=RED, lw=1.0, ls=(0, (3, 3)), zorder=10)
    ax.text(0.5, CEIL+0.6, f"9 m limit  \u2192  ceiling  +{CEIL:.1f}",
            fontsize=8.8, color=RED, weight="bold")
    ax.text(0.5, CEIL_R+0.45, f"roof floor +3.5 m  \u2192  +{CEIL_R:.1f}   (outside the 9 m)",
            fontsize=7.0, color="#a12c2b")
    ax.text(W-0.4, DATUM-1.25, f"height datum  +{DATUM:.1f}   =   average level of the 10 m street",
            fontsize=7.4, color=BLUE, weight="bold", ha="right")

    # two terraces stepping up the slope, each on its own ground
    for tx, tw in [(3.4, 11.0), (16.6, 11.0)]:
        base = g(tx) + 0.30
        for k, (h, lab, al) in enumerate([(3.3, "Ground", 0.58),
                                          (3.3, "First", 0.44),
                                          (3.0, "Roof \u226450%", 0.24)]):
            z0 = base + k*3.3 if k < 2 else base + 6.6
            wk = tw if k < 2 else tw*0.55
            ax.add_patch(mpatches.Rectangle((tx, z0), wk, h-0.16, facecolor=ORANGE,
                         alpha=al, edgecolor="#a83f10", lw=0.9, zorder=11))
            ax.text(tx + wk/2, z0 + h/2 - 0.08, lab, ha="center", va="center",
                    fontsize=7.0, color="#4a1d06", weight="bold", zorder=12)
        # buried basement under each terrace
        ax.add_patch(mpatches.Rectangle((tx, base-3.2), tw, 3.05, facecolor=AQUA,
                     alpha=0.38, edgecolor="#0b5c40", lw=1.0, ls=(0, (3, 2)), zorder=8))
    # a third buried band continues east under the garden
    ax.add_patch(mpatches.Rectangle((29.6, g(29.6)-3.2), 11.0, 3.05, facecolor=AQUA,
                 alpha=0.38, edgecolor="#0b5c40", lw=1.0, ls=(0, (3, 2)), zorder=8))

    ax.annotate("", xy=(3.2, -1.9), xytext=(27.8, -1.9),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color="#4a1d06"))
    ax.text(15.5, -2.9, "the developable half  \u2014  build here", ha="center",
            fontsize=7.8, color="#4a1d06", weight="bold")
    ax.text(21.5, -6.4, ar("\u0642\u0628\u0648") + "   terraced basement  \u2014  parking \u00b7 tanks \u00b7 plant \u00b7 storage",
            ha="center", fontsize=7.6, color="#0b5c40", weight="bold")
    ax.text(21.5, -7.7, "excluded from coverage AND from floor area",
            ha="center", fontsize=7.0, color="#0b5c40")

    ax.plot([W], [13.4], marker="o", ms=7, color=RED, zorder=13)
    ax.annotate("", xy=(43.5, 12.9), xytext=(43.5, CEIL),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=RED))
    ax.text(42.6, 13.6, "2.0 m", fontsize=7.6, color=RED, weight="bold", ha="right")
    ax.annotate("ground reaches the ceiling\nzero height at the NE corner",
                xy=(W, 13.4), xytext=(36.0, 19.6), fontsize=7.6, color=RED,
                weight="bold", ha="center",
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color=RED,
                                connectionstyle="arc3,rad=0.25"))
    ax.annotate("", xy=(-0.6, 21.4), xytext=(7.0, 21.4),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=BLUE))
    ax.text(7.7, 21.4, "Dead Sea view  \u00b7  west  \u00b7  2.0 km", fontsize=7.8,
            color=BLUE, weight="bold", va="center")

    ax.set_xlim(-1.5, W+2.5); ax.set_ylim(-9.0, 23.4)
    ax.set_xlabel("Distance across the plot,  west (low)  \u2192  east (high)   [m]",
                  fontsize=8, color=INK2)
    ax.set_ylabel("Level  [survey datum, m]", fontsize=8, color=INK2)
    ax.set_title("Section across the slope \u2014 the height limit is a flat ceiling "
                 "over rising ground", fontsize=9.6, color=INK, weight="bold",
                 loc="left", pad=10)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(INK3); ax.spines["bottom"].set_color(INK3)
    ax.grid(axis="y", color="#eceae2", lw=0.6); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(f"{OUT}_section.png", dpi=215, bbox_inches="tight"); plt.close(fig)


# ===================================================== F3  CASCADE
def fig_cascade():
    rows = [("Plot area (registered)", AREA_LEGAL, 1.00),
            ("Buildable envelope after setbacks", env_a_area, 0.78),
            ("Max footprint — coverage 27%", cov_max, 0.60),
            ("Total floor area — 2 floors + roof", floor_area, 0.42),
            ("Min landscaped area — 10%", green_min, 0.28)]
    fig, ax = plt.subplots(figsize=(7.4, 2.9))
    y = np.arange(len(rows))
    for yi, (lab, v, al) in zip(y, rows[::-1]):
        ax.barh(yi, v, height=0.56, color=BLUE, alpha=al, edgecolor=SURF, lw=2.0, zorder=3)
        ax.text(v+70, yi, f"{v:,.0f} m²", va="center", fontsize=8.6, color=INK, weight="bold")
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=8.0, color=INK2)
    ax.set_xlim(0, AREA_LEGAL*1.17); ax.set_xlabel("m²", fontsize=8, color=INK2)
    ax.set_title("What the 4,000 m² actually yields", fontsize=9.8, color=INK,
                 weight="bold", loc="left", pad=8)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(INK3)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eceae2", lw=0.6); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(f"{OUT}_cascade.png", dpi=215, bbox_inches="tight"); plt.close(fig)


# ===================================================== F4  MASSING STACK
def fig_stack():
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    rows = [(ar("الروف") + "   Roof floor", roof_max, ORANGE, 0.26,
             "≤ 50% of the floor below · ≤ 3.5 m · half setbacks", True),
            ("First floor", ff, ORANGE, 0.44, "27% coverage", True),
            ("Ground floor", gf, ORANGE, 0.58, "27% coverage", True),
            (ar("قبو") + "   Basement (terraced)", base_env, AQUA, 0.34,
             "parking · tanks · plant · storage — NOT habitable", False)]
    y = 0.0
    for name, v, col, al, note, counted in rows[::-1]:
        w = v/1200*4.0
        ax.add_patch(mpatches.Rectangle((1.9, y), w, 0.76, facecolor=col, alpha=al,
                     edgecolor=SURF, lw=2.2))
        ax.text(1.80, y+0.38, name, va="center", ha="right", fontsize=8.4,
                color=INK, weight="bold")
        ax.text(1.9+w+0.12, y+0.50, f"{v:,.0f} m²", va="center", fontsize=8.6,
                color=INK, weight="bold")
        ax.text(1.9+w+0.12, y+0.23, note, va="center", fontsize=6.8, color=INK3)
        if not counted:
            ax.text(1.9+w/2, y+0.38, "excluded from coverage & floor area",
                    ha="center", va="center", fontsize=6.9, color="#0b5c40", weight="bold")
        y += 0.92
    ax.plot([1.9, 7.3], [y+0.06]*2, color=INK3, lw=0.8)
    ax.text(1.9, y+0.26, f"Floor area counted  ({ar('المساحة الطابقية')})   =   "
                         f"{floor_area:,.0f} m²        FAR  {far:.3f}",
            fontsize=9.2, color=INK, weight="bold")
    ax.set_xlim(0, 7.6); ax.set_ylim(-0.2, y+0.75); ax.axis("off")
    fig.tight_layout(); fig.savefig(f"{OUT}_stack.png", dpi=215, bbox_inches="tight"); plt.close(fig)


# ===================================================== F5  STRATEGY
def fig_strategy():
    fig, axs = plt.subplots(1, 3, figsize=(7.6, 3.1))
    titles = ["✗  One block across the slope",
              "✗  Tall block on the high side",
              "✓  Terraces stepping with the contours"]
    notes = ["Needs 9 m of cut and fill.\nSetback fill is capped at 1 m.\nBlocks the view from behind.",
             f"Ceiling +{CEIL:.0f} is already at\nnatural ground here.\nNo height left to build in.",
             "Each terrace reads the ground it\nsits on. Every unit sees west\nover the roof below."]
    cols = [RED, RED, AQUA]
    for ax, t, n, c in zip(axs, titles, notes, cols):
        gx = np.linspace(0, 10, 100); gy = gx*0.82
        ax.fill_between(gx, -2, gy, color=GROUND, zorder=1)
        ax.plot(gx, gy, color=GROUND_L, lw=1.6, zorder=3)
        ax.axhline(8.6, color=RED, lw=1.4, zorder=2)
        if t.startswith("✗  One"):
            ax.add_patch(mpatches.Rectangle((1.4, 3.6), 7.0, 4.6, facecolor=ORANGE,
                         alpha=0.5, edgecolor="#a83f10", lw=1.0, zorder=5))
        elif t.startswith("✗  Tall"):
            ax.add_patch(mpatches.Rectangle((6.2, 5.1), 3.4, 5.6, facecolor=ORANGE,
                         alpha=0.35, edgecolor=RED, lw=1.2, ls=(0, (3, 2)), zorder=5))
            ax.text(7.9, 11.2, "over", ha="center", fontsize=7.2, color=RED, weight="bold")
        else:
            for k in range(3):
                x0 = 1.0 + k*2.9; g0 = x0*0.82
                ax.add_patch(mpatches.Rectangle((x0, g0), 2.5, 3.0, facecolor=ORANGE,
                             alpha=0.55, edgecolor="#a83f10", lw=1.0, zorder=5+k))
            ax.annotate("", xy=(0.1, 7.6), xytext=(2.4, 7.6),
                        arrowprops=dict(arrowstyle="-|>", lw=1.3, color=BLUE))
        ax.text(0.02, 1.02, t, transform=ax.transAxes, fontsize=8.0, color=c,
                weight="bold", va="bottom")
        ax.text(0.02, -0.30, n, transform=ax.transAxes, fontsize=6.9, color=INK2, va="top")
        ax.set_xlim(-0.2, 10.2); ax.set_ylim(-2, 12.6); ax.axis("off")
    fig.text(0.012, 0.012, "west (low)  ←→  east (high)      ——— red line = the +15.0 ceiling",
             fontsize=6.9, color=INK3, va="bottom")
    fig.tight_layout(rect=[0, 0.16, 1, 1])
    fig.savefig(f"{OUT}_strategy.png", dpi=215, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_site(); fig_section(); fig_cascade(); fig_stack(); fig_strategy()
    print("figures written")
