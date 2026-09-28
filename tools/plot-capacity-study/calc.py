import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
"""Regulatory capacity study - Plot 3+4 combined, Parcel 96, Makawir.
Computes the envelope, coverage, area schedule and yields; emits JSON + figures.
Basis: Jordan Building Regulation No.1/2022, Green/Rural Residential zone.
"""
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly, FancyArrow
from matplotlib.path import Path
import matplotlib.patches as mpatches

# ---------------------------------------------------------------- palette
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
YELLOW, RED, VIOLET = "#eda100", "#e34948", "#4a3aa7"
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8880"
SURF = "#fcfcfb"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.2,
    "axes.edgecolor": INK3, "axes.linewidth": 0.7,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF,
})

OUT = HERE + "/fig"

# ---------------------------------------------------------------- plot geometry
# Trapezoid built to the dimensions printed on the approved (merged) plan.
# A = SW on the 10 m street; B = SE; C = NE on the 6 m road; D = NW.
S_FRONT, N_FRONT = 47.88, 47.26      # street frontages
W_SIDE,  E_SIDE  = 86.27, 82.23      # internal flanks
A = np.array([0.0, 0.0])
B = np.array([S_FRONT, 0.0])
D = np.array([0.0, W_SIDE])
# solve C from |C-B| = E_SIDE and |C-D| = N_FRONT
a = 1 + (E_SIDE**2 - ... if False else 0)
k = (2*W_SIDE)
y_of_x = lambda x: (2*S_FRONT*x - S_FRONT**2 + E_SIDE**2 - N_FRONT**2 + W_SIDE**2) / (2*W_SIDE)
# substitute into (x-S_FRONT)^2 + y^2 = E_SIDE^2
m = (2*S_FRONT)/(2*W_SIDE)
c0 = (-S_FRONT**2 + E_SIDE**2 - N_FRONT**2 + W_SIDE**2)/(2*W_SIDE)
qa = 1 + m*m
qb = -2*S_FRONT + 2*m*c0
qc = S_FRONT**2 + c0*c0 - E_SIDE**2
x = (-qb + math.sqrt(qb*qb - 4*qa*qc))/(2*qa)
C = np.array([x, y_of_x(x)])
PLOT = [A, B, C, D]
def shoelace(pts):
    s=0.0
    for i in range(len(pts)):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%len(pts)]
        s+=x1*y2-x2*y1
    return abs(s)/2
AREA_GEOM = shoelace([tuple(p) for p in PLOT])
AREA_LEGAL = 4000.0                      # scheduled area on the approved plan

# ---------------------------------------------------------------- controls
Z = dict(zone="Green / Rural Residential",
         front=8.0, side=6.0, rear=6.0,
         coverage=0.27, floors=2, roof=True, height=9.0,
         roof_ratio=0.50, roof_h=3.5, green=0.10)

def offset_envelope(front_both=True):
    """Inward offset: streets take `front`, flanks take `side`.
    front_both=False treats the 6 m road end as rear."""
    d_s, d_n = Z["front"], (Z["front"] if front_both else Z["rear"])
    d_w = d_e = Z["side"]
    # offset each edge inward by its own distance, then intersect half-planes
    edges = [(A, B, d_s), (B, C, d_e), (C, D, d_n), (D, A, d_w)]
    lines = []
    cen = np.mean(PLOT, axis=0)
    for p, q, d in edges:
        v = q - p; n = np.array([v[1], -v[0]]); n = n/np.linalg.norm(n)
        if np.dot(cen - p, n) < 0: n = -n         # inward normal
        lines.append((n, np.dot(n, p) + d))       # n.x >= c
    pts = []
    for i in range(4):
        for j in range(i+1, 4):
            n1, c1 = lines[i]; n2, c2 = lines[j]
            M = np.array([n1, n2]); det = np.linalg.det(M)
            if abs(det) < 1e-9: continue
            pts.append(np.linalg.solve(M, np.array([c1, c2])))
    keep = [p for p in pts if all(np.dot(n, p) >= c - 1e-6 for n, c in lines)]
    cen2 = np.mean(keep, axis=0)
    keep.sort(key=lambda p: math.atan2(p[1]-cen2[1], p[0]-cen2[0]))
    return keep

ENV_A = offset_envelope(True)
ENV_B = offset_envelope(False)
env_a_area = shoelace([tuple(p) for p in ENV_A])
env_b_area = shoelace([tuple(p) for p in ENV_B])

# ---------------------------------------------------------------- area schedule
cov_max   = Z["coverage"] * AREA_LEGAL          # 1080
gf = ff   = cov_max
roof_max  = Z["roof_ratio"] * ff                # 540
floor_area = gf + ff + roof_max                 # 2700  (المساحة الطابقية)
far       = floor_area / AREA_LEGAL
green_min = Z["green"] * AREA_LEGAL             # 400

# basement (قبو): whole plot except the FRONT setbacks
front_strip = Z["front"]*S_FRONT + Z["front"]*N_FRONT
base_legal  = AREA_LEGAL - front_strip

# terraced-basement model: a buried level spans the band over which the ground
# falls <= the structural floor-to-floor height.
SLOPE      = 0.25                                # ~25% measured E->W
FFH        = 3.0                                 # structural floor-to-floor
band_w     = FFH / SLOPE                         # 12.0 m per buried step
env_w      = (N_FRONT + S_FRONT)/2 - 2*Z["side"] # ~35.6 m across
env_l      = (W_SIDE + E_SIDE)/2 - 2*Z["front"]  # ~68.3 m along
n_steps    = math.ceil(env_w / band_w)
base_env   = env_w * env_l                       # basement inside the envelope
# plus the side setbacks, which a قبو may occupy
base_sides = 2 * Z["side"] * env_l

# ---------------------------------------------------------------- levels
DATUM   = 6.0        # avg level of the 10 m street along the 47.88 m frontage
CEIL    = DATUM + Z["height"]           # +15.0 structural top of 2nd floor
CEIL_R  = CEIL + Z["roof_h"]            # +18.5 top of roof floor
CORNERS = {"SW (10 m street, W end)": 0.0, "NW (6 m road, W end)": 4.5,
           "SE (E flank, S end)": 12.0, "NE (6 m road, E end)": 15.0}

# ---------------------------------------------------------------- yields
COMMON = 0.12
net_saleable = floor_area * (1 - COMMON)
apt_mix = [120, 150, 180, 200]
apts = []
for g in apt_mix:
    n = int(floor_area // g)
    park = max(math.ceil(floor_area/300), n)
    apts.append(dict(unit_gross=g, units=n, parking=park))
villa_mix = [6, 8, 10, 12]
villas = []
for n in villa_mix:
    fp = cov_max / n
    per = fp*2 + fp*Z["roof_ratio"]
    park = max(math.ceil(floor_area/300), n)
    villas.append(dict(units=n, footprint=round(fp,1), gross_each=round(per,1), parking=park))

RES = dict(area_geom=round(AREA_GEOM,1), area_legal=AREA_LEGAL,
           env_a=round(env_a_area,1), env_b=round(env_b_area,1),
           cov_max=cov_max, gf=gf, ff=ff, roof=roof_max,
           floor_area=floor_area, far=round(far,4), green=green_min,
           base_legal=round(base_legal,1), base_env=round(base_env,1),
           base_sides=round(base_sides,1), n_steps=n_steps, band_w=band_w,
           env_w=round(env_w,2), env_l=round(env_l,2),
           datum=DATUM, ceil=CEIL, ceil_roof=CEIL_R,
           util=round(cov_max/env_a_area,4),
           net_saleable=round(net_saleable,1),
           apts=apts, villas=villas, corners=CORNERS)

# ================================================================ FIGURES
def _poly(ax, pts, **kw):
    ax.add_patch(MplPoly([tuple(p) for p in pts], closed=True, **kw))

def _dim(ax, p, q, text, off=2.6, fs=7.4, color=INK2):
    p, q = np.array(p), np.array(q)
    v = q - p; n = np.array([-v[1], v[0]]); n = n/np.linalg.norm(n)
    cen = np.mean(PLOT, axis=0)
    if np.dot(np.mean([p,q],axis=0) - cen, n) < 0: n = -n
    a2, b2 = p + n*off, q + n*off
    ax.annotate("", xy=tuple(b2), xytext=tuple(a2),
                arrowprops=dict(arrowstyle="<->", lw=0.7, color=color, shrinkA=0, shrinkB=0))
    m = (a2+b2)/2 + n*1.6
    ang = math.degrees(math.atan2(v[1], v[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    ax.text(m[0], m[1], text, ha="center", va="center", fontsize=fs,
            color=color, rotation=ang, rotation_mode="anchor")

# ---- FIG 1 : site plan, setbacks, envelope ----------------------
def fig_site():
    fig, ax = plt.subplots(figsize=(6.6, 7.0))
    _poly(ax, PLOT, facecolor="#f0efe9", edgecolor=INK, lw=1.6, zorder=2)
    _poly(ax, ENV_A, facecolor=BLUE, edgecolor=BLUE, lw=1.3, alpha=0.20, zorder=3)
    _poly(ax, ENV_A, facecolor="none", edgecolor=BLUE, lw=1.4, ls=(0,(5,3)), zorder=4)

    # indicative footprint at 27% placed on the lower (western) half
    ex = np.array(ENV_A)
    x0, x1 = ex[:,0].min(), ex[:,0].max()
    y0, y1 = ex[:,1].min(), ex[:,1].max()
    fw = 18.0; fh = cov_max / fw
    fx = x0 + 1.0; fy = y0 + (y1-y0-fh)/2
    ax.add_patch(mpatches.Rectangle((fx, fy), fw, fh, facecolor=ORANGE,
                 alpha=0.55, edgecolor=ORANGE, lw=1.3, zorder=5))
    ax.text(fx+fw/2, fy+fh/2, f"indicative footprint\n{cov_max:,.0f} m²  (27%)",
            ha="center", va="center", fontsize=7.6, color="#5a2408", weight="bold", zorder=6)

    # roads
    ax.add_patch(mpatches.Rectangle((-4, -10.5), S_FRONT+30, 10.0,
                 facecolor="#e2e0d8", edgecolor=INK3, lw=0.8, zorder=1))
    ax.text(S_FRONT/2, -5.6, "شارع 10 متر  ·  10 m street", ha="center",
            va="center", fontsize=8.2, color=INK2, weight="bold")
    ny = max(C[1], D[1])
    ax.add_patch(mpatches.Rectangle((-4, ny), N_FRONT+30, 6.0,
                 facecolor="#e2e0d8", edgecolor=INK3, lw=0.8, zorder=1))
    ax.text(N_FRONT/2, ny+3.0, "طريق 6 متر  ·  6 m road", ha="center",
            va="center", fontsize=8.2, color=INK2, weight="bold")

    # neighbours
    ax.text(-9.5, W_SIDE/2, "Parcel 321\n(no road)", ha="center", va="center",
            fontsize=7.4, color=INK3, rotation=90)
    ax.text(S_FRONT+10.5, E_SIDE/2, "Plots 1 & 2\n(no road)", ha="center",
            va="center", fontsize=7.4, color=INK3, rotation=90)

    # dimensions
    _dim(ax, A, B, f"{S_FRONT:.2f} m", off=12.0)
    _dim(ax, C, D, f"{N_FRONT:.2f} m", off=8.0)
    _dim(ax, D, A, f"{W_SIDE:.2f} m", off=7.0)
    _dim(ax, B, C, f"{E_SIDE:.2f} m", off=8.0)

    # setback callouts
    for p, q, lab in [(A, B, "8 m front"), (C, D, "8 m front"),
                      (D, A, "6 m side"), (B, C, "6 m side")]:
        mid = (np.array(p)+np.array(q))/2
        cen = np.mean(PLOT, axis=0)
        v = (cen-mid); v = v/np.linalg.norm(v)
        ax.text(*(mid + v*4.0), lab, ha="center", va="center", fontsize=7.0,
                color=INK2, zorder=7,
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=INK3, lw=0.5, alpha=0.92))

    # slope arrow (ground falls E -> W)
    ax.annotate("", xy=(2, W_SIDE*0.86), xytext=(S_FRONT-2, W_SIDE*0.86),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=AQUA))
    ax.text(S_FRONT/2, W_SIDE*0.895, "ground falls  ≈ 25%  →  W",
            ha="center", fontsize=7.8, color="#0d6b4a", weight="bold")
    for txt, pos in [("+15.0", (N_FRONT-4, W_SIDE-3)), ("+4.5", (4, W_SIDE-3)),
                     ("+12.0", (S_FRONT-4, 3.5)), ("0.0", (3.5, 3.5))]:
        ax.text(*pos, txt, fontsize=7.4, color="#0d6b4a", ha="center",
                weight="bold", zorder=8,
                bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=AQUA, lw=0.8))

    # north arrow
    ax.annotate("", xy=(S_FRONT+14, W_SIDE*0.93), xytext=(S_FRONT+14, W_SIDE*0.80),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=INK))
    ax.text(S_FRONT+14, W_SIDE*0.955, "N", ha="center", fontsize=9, weight="bold", color=INK)

    h = [mpatches.Patch(fc="#f0efe9", ec=INK, label=f"Plot 3+4 combined — {AREA_LEGAL:,.0f} m²"),
         mpatches.Patch(fc=BLUE, alpha=0.20, ec=BLUE, label=f"Buildable envelope — {env_a_area:,.0f} m²"),
         mpatches.Patch(fc=ORANGE, alpha=0.55, ec=ORANGE, label=f"Max coverage 27% — {cov_max:,.0f} m²")]
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(0.0, -0.045),
              frameon=False, fontsize=7.8, ncol=1, handlelength=1.5)
    ax.set_xlim(-16, S_FRONT+22); ax.set_ylim(-13, W_SIDE+10)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(f"{OUT}_site.png", dpi=210, bbox_inches="tight"); plt.close(fig)

# ---- FIG 2 : E-W section, datum, ceiling -------------------------
def fig_section():
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    W = 47.6
    gx = np.linspace(0, W, 240)
    gy = np.interp(gx, [0, 6, 20, 34, 42, W], [0.0, 1.2, 5.0, 9.4, 12.2, 13.2])
    ax.fill_between(gx, gy-7, gy, color="#ded9cb", zorder=1)
    ax.plot(gx, gy, color="#7a6a4a", lw=1.7, zorder=3, label="Natural ground (survey datum)")

    ax.axhline(DATUM, color=BLUE, lw=1.6, ls=(0,(6,3)), zorder=4)
    ax.text(0.4, DATUM+0.32, f"Height datum  +{DATUM:.1f}  —  average level of the 10 m street",
            fontsize=7.6, color=BLUE, weight="bold")
    ax.axhline(CEIL, color=RED, lw=2.0, zorder=5)
    ax.text(0.4, CEIL+0.35, f"9 m limit  →  absolute ceiling  +{CEIL:.1f}   (structural top, 2nd floor)",
            fontsize=8.0, color=RED, weight="bold")
    ax.axhline(CEIL_R, color=RED, lw=1.1, ls=(0,(3,3)), zorder=5)
    ax.text(0.4, CEIL_R+0.3, f"+ roof floor 3.5 m  →  +{CEIL_R:.1f}  (excluded from the 9 m)",
            fontsize=7.2, color="#a12c2b")

    # workable building on the low side
    bx, bw = 4.0, 17.0
    for i, (z0, z1, lab) in enumerate([(1.0, 4.4, "Ground"), (4.4, 7.8, "First"),
                                       (7.8, 11.0, "Roof floor")]):
        ax.add_patch(mpatches.Rectangle((bx, z0), bw, z1-z0-0.12,
                     facecolor=ORANGE, alpha=0.30 if i < 2 else 0.16,
                     edgecolor=ORANGE, lw=1.0, zorder=6))
        ax.text(bx+bw/2, (z0+z1)/2, lab, ha="center", va="center", fontsize=7.0,
                color="#5a2408", zorder=7)
    ax.text(bx+bw/2, -1.5, "WORKS on the low (western) half", ha="center",
            fontsize=7.8, color="#5a2408", weight="bold")

    # collision on the high side
    ax.annotate("", xy=(44.0, 12.6), xytext=(44.0, CEIL),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=RED))
    ax.text(43.2, 13.9, "only 2.4 m\nleft here", ha="right", fontsize=7.4,
            color=RED, weight="bold")
    ax.scatter([W], [13.2], s=42, color=RED, zorder=9)
    ax.text(W-0.6, 13.2-1.9, "ground meets the ceiling\n→ zero height at the NE corner",
            ha="right", fontsize=7.4, color=RED, weight="bold")

    # basement terracing
    for k in range(3):
        x0 = 4 + k*12
        gy0 = np.interp(x0+6, gx, gy)
        ax.add_patch(mpatches.Rectangle((x0, gy0-3.0), 11.6, 2.9, facecolor=AQUA,
                     alpha=0.22, edgecolor=AQUA, lw=1.0, ls=(0,(3,2)), zorder=2))
    ax.text(22, -4.6, "terraced قبو / basement — parking, tanks, plant, storage  "
                      "(excluded from coverage AND floor area)",
            ha="center", fontsize=7.4, color="#0d6b4a", weight="bold")

    ax.set_xlim(-1, W+2); ax.set_ylim(-6.5, 21)
    ax.set_xlabel("Distance across the plot, east → west  (m)", fontsize=8, color=INK2)
    ax.set_ylabel("Level  (survey datum, m)", fontsize=8, color=INK2)
    ax.set_title("Section across the slope — why the height limit binds on the east",
                 fontsize=9.4, color=INK, weight="bold", loc="left", pad=8)
    ax.text(W+1.4, 13.2, "EAST\n(high)", fontsize=7.4, color=INK3, ha="right", va="bottom")
    ax.text(0.2, -5.8, "WEST (low) ←", fontsize=7.4, color=INK3)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e6e4dc", lw=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(f"{OUT}_section.png", dpi=210, bbox_inches="tight"); plt.close(fig)

# ---- FIG 3 : area cascade (single hue, direct labels) ------------
def fig_cascade():
    rows = [("Plot area (registered)", AREA_LEGAL, 1.00),
            ("Buildable envelope after setbacks", env_a_area, 0.80),
            ("Max footprint — coverage 27%", cov_max, 0.62),
            ("Total floor area — 2 floors + roof", floor_area, 0.44),
            ("Min landscaped area — 10%", green_min, 0.30)]
    fig, ax = plt.subplots(figsize=(7.4, 3.0))
    labs = [r[0] for r in rows][::-1]
    vals = [r[1] for r in rows][::-1]
    alphas = [r[2] for r in rows][::-1]
    y = np.arange(len(rows))
    for yi, v, al in zip(y, vals, alphas):
        ax.barh(yi, v, height=0.56, color=BLUE, alpha=al,
                edgecolor=SURF, linewidth=2.0, zorder=3)
        ax.text(v + 70, yi, f"{v:,.0f} m²", va="center", fontsize=8.4,
                color=INK, weight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=8.0, color=INK2)
    ax.set_xlim(0, AREA_LEGAL*1.16)
    ax.set_xlabel("m²", fontsize=8, color=INK2)
    ax.set_title("What the 4,000 m² actually yields", fontsize=9.6,
                 color=INK, weight="bold", loc="left", pad=8)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eceae2", lw=0.6); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(f"{OUT}_cascade.png", dpi=210, bbox_inches="tight"); plt.close(fig)

# ---- FIG 4 : massing stack --------------------------------------
def fig_stack():
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    levels = [("قبو  Basement — terraced, 3 steps", base_env, AQUA, 0.30, "excluded from coverage & floor area"),
              ("Ground floor", gf, ORANGE, 0.55, "27% coverage"),
              ("First floor", ff, ORANGE, 0.42, "27% coverage"),
              ("Roof floor (الروف)", roof_max, ORANGE, 0.26, "≤50% of the floor below, ≤3.5 m")]
    y = 0
    for name, v, col, al, note in levels:
        w = v / 1200 * 4.2
        ax.add_patch(mpatches.Rectangle((0, y), w, 0.78, facecolor=col, alpha=al,
                     edgecolor=SURF, lw=2.0))
        ax.text(0.14, y+0.39, name, va="center", fontsize=8.2, color=INK, weight="bold")
        ax.text(w+0.12, y+0.50, f"{v:,.0f} m²", va="center", fontsize=8.4, color=INK, weight="bold")
        ax.text(w+0.12, y+0.24, note, va="center", fontsize=6.9, color=INK3)
        y += 0.95
    ax.text(0.0, y+0.25, f"Floor area counted (المساحة الطابقية)  =  {floor_area:,.0f} m²   "
                         f"·   FAR {far:.3f}", fontsize=9.0, color=INK, weight="bold")
    ax.set_xlim(0, 7.2); ax.set_ylim(-0.25, y+0.75); ax.axis("off")
    fig.tight_layout(); fig.savefig(f"{OUT}_stack.png", dpi=210, bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    json.dump(RES, open(HERE + "/res.json", "w"), indent=1, ensure_ascii=False)
    for k, v in RES.items():
        if not isinstance(v, (list, dict)): print(f"{k:14s} {v}")
    print("\nenvelope A (8/6/6/8):", round(env_a_area,1))
    print("envelope B (8/6/6/6):", round(env_b_area,1))
    print("basement legal cap  :", round(base_legal,1))
    print("basement in envelope:", round(base_env,1), f"over {n_steps} steps of {band_w:.0f} m")
    print("apts:", apts)
    print("villas:", villas)
