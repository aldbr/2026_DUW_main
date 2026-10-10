#!/usr/bin/env python3
"""Figures for the CHEP 2026 DiracX paper, in the same modelling-clay language
as the LHCb-week decks.

    uv run --with cairosvg python3 build_figures.py

Writes out/fig-coexistence.svg and .pdf.

The primitives live in claylib.py, copied from the LHCb-week deck
(presentations/lhcbweek/figures/build_maps.py), so the paper and the talks look
like the same project.

Sizing note: the text column in this class is 13.0 cm wide (369.9 pt). A label
at size 44 in a 1600-unit viewBox therefore prints at about 10 pt, and size 34 at
about 7.8 pt. Do not scale a deck figure down to fit here: the labels have to be
have to be re-tuned, which is why the sizes below look large.
"""
from __future__ import annotations

import math
import pathlib
import subprocess
import sys

import claylib as cl
from claylib import Iso, blob, card, contact_shadow, cube, person, shade, slab, text

OUT = pathlib.Path(__file__).parent / "out"
FONT = cl.FONT
TEXT_1, TEXT_2 = cl.TEXT_1, cl.TEXT_2

BLUE = cl.ACCENT["legacy"]     # the legacy side
TEAL = cl.ACCENT["diracx"]     # DiracX
OFF = "#e6e9ee"                # a service already switched off
SLABC = "#dfe5ee"

TITLE, SUB = 44, 34


def head(w: int, h: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">'
        '<defs>'
        '<marker id="arr" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="22" markerHeight="20" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 Z" fill="#6b7280"/></marker>'
        '</defs>'
    )


def pill(x, y, w, h, base, gid, r=None) -> str:
    """A rounded clay tile: matte gradient, rim light along the top."""
    r = r if r is not None else h / 2
    return (
        contact_shadow(x + w / 2, y + h + 4, w * 0.5, 11, f"{gid}-cs", 0.16)
        + f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0.25" y2="1">'
          f'<stop offset="0" stop-color="{shade(base, 0.5)}"/>'
          f'<stop offset="1" stop-color="{shade(base, -0.14)}"/></linearGradient></defs>'
          f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
          f'rx="{r:.1f}" fill="url(#{gid})"/>'
          f'<path d="M{x + r * 0.7:.1f},{y + 2.6:.1f} L{x + w - r * 0.7:.1f},{y + 2.6:.1f}" '
          f'stroke="{shade(base, 0.85)}" stroke-width="2.8" stroke-linecap="round" '
          f'opacity="0.75" fill="none"/>'
    )


def cylinder(cx, ytop, rx, body_h, base, gid) -> str:
    """A database, drawn as a 3D cylinder: a lid ellipse over a shaded body."""
    ry = rx * 0.16
    ybot = ytop + body_h
    out = [contact_shadow(cx, ybot + ry + 8, rx * 0.9, 14, f"{gid}-cs", 0.18)]
    out.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="{shade(base, 0.05)}"/>'
               f'<stop offset="1" stop-color="{shade(base, -0.22)}"/></linearGradient></defs>')
    out.append(f'<path d="M{cx - rx:.1f},{ytop:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx + rx:.1f},{ytop:.1f} '
               f'L{cx + rx:.1f},{ybot:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {cx - rx:.1f},{ybot:.1f} Z" '
               f'fill="url(#{gid})"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{ytop:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{shade(base, 0.42)}"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{ytop:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" '
               f'stroke="{shade(base, 0.65)}" stroke-width="2" opacity="0.6"/>')
    return "".join(out)


def arrowhead(x, y, ux, uy, length=20, half_width=9, color="#6b7280") -> str:
    """A filled triangle, tip at (x, y), pointing along the unit vector (ux, uy).

    Drawn by hand rather than as an SVG marker: cairosvg does not reliably honour
    marker orient="auto"/"auto-start-reverse" on straight (unbowed) paths, which
    left every vertical arrow in these figures pointing sideways."""
    px, py = -uy, ux
    bx, by = x - ux * length, y - uy * length
    left = (bx + px * half_width, by + py * half_width)
    right = (bx - px * half_width, by - py * half_width)
    return (f'<polygon points="{x:.1f},{y:.1f} {left[0]:.1f},{left[1]:.1f} '
            f'{right[0]:.1f},{right[1]:.1f}" fill="{color}"/>')


def arrow(x1, y1, x2, y2, bow=0.0, sw=3.2) -> str:
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + bow
    dx, dy = x2 - mx, y2 - my
    length = math.hypot(dx, dy) or 1.0
    ux, uy = dx / length, dy / length
    line_end = (x2 - ux * 14, y2 - uy * 14)
    return (f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {line_end[0]:.1f},{line_end[1]:.1f}" '
            f'fill="none" stroke="#6b7280" stroke-width="{sw}" stroke-linecap="round"/>'
            + arrowhead(x2, y2, ux, uy))


def coexistence() -> str:
    """One client, one choice made per component, two sides, one set of databases."""
    W, H = 1760, 430
    o = [head(W, H)]

    # --- the clients, unchanged
    cx, cy, cw, ch = 96, 150, 250, 132
    o.append(card(cx, cy, cw, ch))
    for i, lab in enumerate(("user client", "pilot", "web portal")):
        o.append(pill(cx + 22, cy + 16 + i * 36, cw - 44, 30, BLUE, f"cli{i}", r=11))
        o.append(text(cx + cw / 2, cy + 38 + i * 36, lab, SUB, fill="#25405f"))
    o.append(text(cx + cw / 2, cy - 16, "clients, unchanged", TITLE, "bold", fill=TEXT_1))

    # --- the choice, made per component in the configuration
    sx, sy, sw_, sh = 410, 140, 320, 152
    o.append(arrow(cx + cw + 12, 216, sx - 14, 216))
    o.append(card(sx, sy, sw_, sh))
    o.append(pill(sx + 24, sy + 20, sw_ - 48, 46, "#93c0ea", "sel", r=16))
    o.append(text(sx + sw_ / 2, sy + 51, "one base class", TITLE, "bold", fill="#22456f"))
    o.append(text(sx + sw_ / 2, sy + 96, "chooses per component,", SUB, fill=TEXT_2))
    o.append(text(sx + sw_ / 2, sy + 126, "from the configuration", SUB, fill=TEXT_2))

    # --- the two sides
    def side(px, py, colours, title):
        it = Iso(px, py, 0.62)
        s = [slab(it, -96, -40, 192, 80, 10, SLABC, f"sl{int(py)}")]
        for i, base in enumerate(colours):
            s.append(cube(it, -74 + i * 50, -18, 34, 34, 24, base, r=6))
        s.append(text(px, py + 104, title, TITLE, "bold", fill=TEXT_1))
        return "".join(s)

    o.append(arrow(sx + sw_ + 12, 190, 918, 108, -26))
    o.append(arrow(sx + sw_ + 12, 244, 918, 330, 26))
    o.append(side(1040, 78, [BLUE, BLUE, OFF, OFF], "legacy DIRAC services"))
    o.append(side(1040, 300, [TEAL, TEAL, TEAL, OFF], "DiracX endpoints"))

    # --- one set of databases
    it = Iso(1546, 212, 0.66)
    o.append(slab(it, -104, -44, 208, 88, 10, "#d5dbe4", "sldb"))
    for i in range(3):
        o.append(cube(it, -78 + i * 52, -20, 40, 38, 28, "#bfc7d3", r=6))
    o.append(text(1546, 338, "one set of", TITLE, "bold", fill=TEXT_1))
    o.append(text(1546, 378, "databases", TITLE, "bold", fill=TEXT_1))
    o.append(arrow(1226, 120, 1424, 172, -14))
    o.append(arrow(1226, 316, 1424, 254, 14))

    o.append("</svg>")
    return "".join(o)


def architecture() -> str:
    """What DiracX is made of, and what it runs beside. Clients reach either side, the
    choice made per component; DiracX's endpoints and workers share one Redis, and both
    sides write to the same databases, which is the coexistence the paper is about. The
    band is labelled "DiracX" rather than by where it runs. Redis sits between endpoints
    and workers, because it is the queue between them and disposable like them."""
    MAIN = 36
    SMALL = 26
    W, H = 1500, 720
    o = [head(W, H)]

    # --- who calls it, centred over the whole width
    labels = ("user client", "pilot", "web interface")
    widths = [max(150, 34 + len(l) * 18) for l in labels]
    widths[0] = widths[2] = max(widths[0], widths[2])
    x = 750 - (sum(widths) + 18 * (len(widths) - 1)) / 2
    x0 = x
    for i, (lab, w) in enumerate(zip(labels, widths)):
        o.append(pill(x, 68, w, 56, BLUE, f"client{i}", r=18))
        o.append(text(x + w / 2, 104, lab, SUB, fill="#25405f"))
        x += w + 18
    x1 = x - 18
    o.append(text((x0 + x1) / 2, 44, "clients", TITLE, "bold", fill=TEXT_1))

    # --- DiracX: endpoints, Redis as the queue, workers, and the scheduler feeding it
    BX, BW, BY, BH = 40, 1030, 196, 330
    o.append(f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="26" fill="#f3f6fa" '
             f'stroke="#d8e0ea" stroke-width="3"/>')
    o.append(text(BX + 40, BY + 40, "DiracX", SUB, "bold", anchor="start", fill=TEXT_2))

    def bank(px, py, n, base, gid, title, sub):
        it = Iso(px, py, 0.6)
        s = [slab(it, -112, -44, 224, 88, 10, SLABC, gid)]
        for i in range(n):
            s.append(cube(it, -84 + i * 56, -20, 38, 38, 26, base, r=6))
        s.append(text(px, py + 112, title, MAIN, "bold", fill=TEXT_1))
        s.append(text(px, py + 146, sub, SUB, fill=TEXT_2))
        return "".join(s)

    o.append(bank(210, 330, 3, TEAL, "bk1", "REST endpoints", "answer requests"))
    o.append(bank(900, 330, 3, "#9fd3a8", "bk2", "task workers", "execute work"))

    rx, ry, rw, rh = 440, 316, 230, 78
    o.append(pill(rx, ry, rw, rh, "#f0d9a6", "redis1", r=18))
    o.append(text(rx + rw / 2, ry + 34, "Redis", MAIN, "bold", fill="#5b4a1f"))
    o.append(text(rx + rw / 2, ry + 64, "work in flight", SMALL, fill="#5b4a1f"))
    o.append(arrow(340, 355, rx - 8, 355))
    o.append(arrow(rx + rw + 8, 355, 770, 355))

    sx, sy, sw_, sh = 470, 222, 170, 52
    o.append(pill(sx, sy, sw_, sh, "#e6e9ee", "sched", r=16))
    o.append(text(sx + sw_ / 2, sy + 35, "scheduler", SMALL, "bold", fill="#23384d"))
    o.append(arrow(sx + sw_ / 2, sy + sh + 4, sx + sw_ / 2, ry - 6))

    # --- DIRAC, beside it
    DX, DW = 1100, 360
    o.append(f'<rect x="{DX}" y="{BY}" width="{DW}" height="{BH}" rx="26" fill="#eef3fa" '
             f'stroke="#d3deec" stroke-width="3"/>')
    o.append(text(DX + 34, BY + 40, "DIRAC", SUB, "bold", anchor="start", fill=TEXT_2))
    o.append(bank(DX + DW / 2, 330, 3, BLUE, "bk3", "services", "not yet migrated"))

    # --- clients reach one side or the other, per component
    o.append(arrow(x0 + 40, 134, 300, BY - 4, 10))
    o.append(arrow(x1 - 40, 134, DX + DW / 2, BY - 4, 10))
    o.append(text(750, 172, "one side or the other, per component", SMALL, italic=True, fill=TEXT_2))

    # --- both sides write to the same data layer
    DY = 574
    o.append(arrow(740, BY + BH + 4, 740, DY - 6))
    o.append(arrow(DX + DW / 2, BY + BH + 4, DX + DW / 2, DY - 6))
    o.append(f'<rect x="40" y="{DY}" width="1420" height="126" rx="26" fill="#f6f7f9" '
             f'stroke="#dde2e9" stroke-width="3"/>')

    def store(px, w, base, title, sub, gid):
        o.append(pill(px, DY + 18, w, 60, base, gid, r=20))
        o.append(text(px + w / 2, DY + 57, title, MAIN, "bold", fill="#23384d"))
        o.append(text(px + w / 2, DY + 106, sub, SUB, fill=TEXT_2))

    store(80, 400, "#e6e9ee", "OpenTelemetry", "metrics, traces", "st4")
    store(540, 400, "#c6cfdb", "object store", "sandboxes", "st3")
    store(1000, 420, "#c6cfdb", "databases", "shared with DIRAC", "st1")

    o.append("</svg>")
    return "".join(o)


def roadmap() -> str:
    """A timeline: what is delivered, what is planned, and who is waiting for what."""
    W, H = 1600, 520
    o = [head(W, H)]
    AXIS = 336

    o.append(f'<line x1="70" y1="{AXIS}" x2="1530" y2="{AXIS}" stroke="#c3ccd8" '
             f'stroke-width="5" stroke-linecap="round"/>')
    o.append(arrow(1500, AXIS, 1556, AXIS, sw=5))

    # Each stop is a list of groups; each group is 1+ lines rendered in one pill,
    # so a single deliverable that needs two lines does not look like two deliverables.
    stops = [
        (300, TEAL, "delivered", [["authentication"], ["job status"], ["sandboxes"]], 31),
        (790, "#9fd3a8", "Q4 2026",
         [["pilot management"], ["resource status, read only"], ["transformation system: design"]], 25),
        (1270, "#f0d9a6", "Q4 2027", [["transformation system:", "implementation"]], 31),
    ]
    for x, base, when, groups, fs in stops:
        y = AXIS - 40
        for gi, group in enumerate(reversed(groups)):
            n = len(group)
            h = 46 if n == 1 else 46 + 32 * (n - 1)
            y -= h + 10
            o.append(pill(x - 210, y, 420, h, base, f"rs{x}{gi}", r=15))
            for li, line in enumerate(group):
                ly = y + h / 2 + 10 + (li - (n - 1) / 2) * 32
                o.append(text(x, ly, line, fs, fill="#23384d"))
        o.append(f'<line x1="{x}" y1="{AXIS - 40}" x2="{x}" y2="{AXIS}" '
                 f'stroke="#9aa6b6" stroke-width="3"/>')
        o.append(f'<circle cx="{x}" cy="{AXIS}" r="13" fill="#ffffff" stroke="#6b7280" '
                 f'stroke-width="5"/>')
        o.append(text(x, AXIS + 52, when, 34, "bold", fill=TEXT_1))

    o.append(text(70, AXIS + 106, "one installation in production, two certifying",
                  SUB, anchor="start", italic=True, fill=TEXT_2))
    o.append(text(1530, AXIS + 106, "installations without DIRAC wait here",
                  SUB, anchor="end", italic=True, fill=TEXT_2))

    o.append("</svg>")
    return "".join(o)


def footprint() -> str:
    """What the whole deployment costs to run."""
    W, H = 1600, 290
    o = [head(W, H)]

    groups = [(240, 20, TEAL, "endpoint replicas"),
              (720, 3, "#9fd3a8", "task workers"),
              (1030, 1, "#c6cfdb", "web replica")]
    for px, n, base, lab in groups:
        cols = 10 if n > 6 else n
        it = Iso(px, 104, 0.78)
        for i in range(n):
            cx = -104 + (i % cols) * 23
            cy = -16 + (i // cols) * 28
            o.append(cube(it, cx, cy, 19, 19, 16, base, r=4))
        o.append(text(px, 216, f"{n}", 44, "bold", fill=TEXT_1))
        o.append(text(px, 246, lab, SUB, fill=TEXT_2))

    o.append(f'<line x1="1210" y1="34" x2="1210" y2="250" stroke="#d8e0ea" stroke-width="3"/>')
    totals = [("&lt; 10", "processor cores"), ("7 GB", "memory"),
              ("5 MB/s", "network"), ("1.5 k/s", "requests served")]
    for i, (big, lab) in enumerate(totals):
        y = 66 + i * 58
        o.append(text(1300, y, big, 44, "bold", anchor="end", fill=TEXT_1))
        o.append(text(1350, y, lab, SUB, anchor="start", fill=TEXT_2))

    o.append("</svg>")
    return "".join(o)


# Validated with the dataviz skill's validate_palette.js against a light surface:
# all checks pass, worst colour-blind separation dE 12.7 (protan).
AUTH, WORK = "#c9791a", "#0f9a8a"


def routes() -> str:
    """Request rate by route: a sorted horizontal bar chart, coloured by what the route is for.
    Two columns -- authentication routes left, work routes right -- so the figure takes less
    vertical space; both columns share one scale, so bar lengths stay comparable.

    Values are the four named routes in the CHEP 2026 deck's Grafana panel
    (chep26/public/images/otel-dashboard.png), a five-minute interval at LHCb.
    Replace them with a longer Prometheus window before publication.
    """
    cols = [
        [("/.well-known/openid-configuration", 592, AUTH), ("/api/auth/legacy-exchange", 317, AUTH)],
        [("/api/jobs/status", 308, WORK), ("/api/jobs/metadata", 166, WORK)],
    ]
    W, H = 2400, 320
    ROW, BAR, TOP = 100, 60, 40
    BARMAX = 380
    FS = 40
    X0 = [820, 1770]
    global_max = max(v for col in cols for _, v, _ in col)
    scale = BARMAX / global_max
    o = [head(W, H)]

    for x0, col in zip(X0, cols):
        for i, (route, value, colour) in enumerate(col):
            y = TOP + i * ROW
            length = value * scale
            # square at the baseline, rounded at the data end
            o.append(f'<path d="M{x0},{y} H{x0 + length - 8:.1f} Q{x0 + length:.1f},{y} '
                     f'{x0 + length:.1f},{y + 8} V{y + BAR - 8} Q{x0 + length:.1f},{y + BAR} '
                     f'{x0 + length - 8:.1f},{y + BAR} H{x0} Z" fill="{colour}"/>')
            o.append(text(x0 - 24, y + BAR / 2 + 14, route, FS, anchor="end", fill=TEXT_1))
            o.append(text(x0 + length + 20, y + BAR / 2 + 14, f"{value} req/s", FS, anchor="start", fill=TEXT_2))
        o.append(f'<line x1="{x0}" y1="{TOP - 12}" x2="{x0}" y2="{TOP + len(col) * ROW - 22}" '
                 f'stroke="#9aa6b6" stroke-width="3.5"/>')

    ly = TOP + 2 * ROW + 34
    for j, (label, colour) in enumerate((("authentication", AUTH), ("work", WORK))):
        lx = 950 + j * 460
        o.append(f'<rect x="{lx}" y="{ly - 30}" width="38" height="38" rx="6" fill="{colour}"/>')
        o.append(text(lx + 54, ly - 1, label, FS, anchor="start", fill=TEXT_2))

    o.append("</svg>")
    return "".join(o)


def execution() -> str:
    """The production system on top, the three places its work can run underneath."""
    W, H = 1600, 614
    o = [head(W, H)]
    TILE = "#23384d"

    # --- the production and transformation system
    o.append(card(300, 24, 1000, 124))
    o.append(text(800, 80, "production and transformation system", TITLE, "bold", fill=TEXT_1))
    o.append(text(800, 126, "described in CWL · priority for 2027", SUB, fill=TEXT_2))

    # --- hands work to one of three execution layers
    cols = [
        (280, BLUE, "DIRAC's WMS", ["existing installations"], "in production"),
        (800, OFF, "a community's own", ["e.g. CMS"], "external"),
        (1320, TEAL, "DiracX minimal WMS", ["for testing and", "small installations"], "planned"),
    ]
    tw, ty, th = 470, 244, 218
    o.append(arrow(560, 154, 300, ty - 8, -10))
    o.append(arrow(800, 154, 800, ty - 8))
    o.append(arrow(1040, 154, 1300, ty - 8, -10))
    o.append(text(816, 204, "hands work to", SUB, anchor="start", italic=True, fill=TEXT_2))
    for i, (cx, base, title, lines, state) in enumerate(cols):
        o.append(pill(cx - tw / 2, ty, tw, th, base, f"ex{i}", r=26))
        o.append(text(cx, ty + 56, title, 40, "bold", fill=TILE))
        for j, line in enumerate(lines):
            o.append(text(cx, ty + 102 + j * 37, line, SUB, fill=TILE))
        o.append(text(cx, ty + th - 22, state, SUB, italic=True, fill=TEXT_2))

    # --- where the minimal WMS goes next
    o.append(arrow(1320, ty + th + 6, 1320, 514))
    o.append(pill(1085, 522, 470, 66, "#f0d9a6", "exnext", r=20))
    o.append(text(1320, 568, "interCEde", 40, "bold", fill=TILE))
    o.append(text(1060, 546, "next: computing elements", SUB, anchor="end", italic=True, fill=TEXT_2))
    o.append(text(1060, 584, "and batch systems · in design", SUB, anchor="end", italic=True, fill=TEXT_2))

    o.append("</svg>")
    return "".join(o)


def layers() -> str:
    """Three levels. (i) DiracX's production and transformation system, which hands work to
    (ii) one of three execution layers, DIRAC's WMS and DiracX's minimal WMS drawn close
    together since the second aims to replace the first, a community's own kept apart since
    it is external; and (iii) the database layer beneath the first two, shared where both
    still read and write the same tables, not shared where the new schema stands alone."""
    W, H = 1600, 830
    o = [head(W, H)]
    TILE = "#23384d"

    # --- level i: DiracX's production and transformation system
    px, py, pw, ph = 460, 20, 680, 96
    o.append(card(px, py, pw, ph))
    o.append(text(px + pw / 2, py + 42, "production and transformation system", 32, "bold", fill=TILE))
    o.append(text(px + pw / 2, py + 76, "in DiracX · described in CWL · priority for 2027", 24, fill=TEXT_2))
    o.append(text(px + pw / 2, py + ph + 34, "hands work to", SUB, italic=True, fill=TEXT_2))

    branch_y = py + ph + 58
    o.append(f'<circle cx="{px + pw / 2:.1f}" cy="{branch_y:.1f}" r="7" fill="#6b7280"/>')

    # --- level ii: DIRAC's WMS and DiracX's minimal WMS close together (the second aims to
    # replace the first); a community's own kept apart, since it is external
    dw, dh, ty = 380, 200, 260
    dirac_cx, dx_cx, ext_cx = 310, 800, 1330
    o.append(arrow(px + pw / 2, branch_y, dirac_cx, ty - 8, -18))
    o.append(arrow(px + pw / 2, branch_y, dx_cx, ty - 8))
    o.append(arrow(px + pw / 2, branch_y, ext_cx, ty - 8, -18))

    cols = [
        (dirac_cx, BLUE, "DIRAC's WMS", ["existing installations"], "in production"),
        (dx_cx, TEAL, "DiracX minimal WMS", ["for testing and", "small installations"], "planned"),
        (ext_cx, OFF, "a community's own", ["e.g. CMS's WMAgent"], "external"),
    ]
    for i, (cx, base, title, lines, state) in enumerate(cols):
        o.append(pill(cx - dw / 2, ty, dw, dh, base, f"ly{i}", r=24))
        o.append(text(cx, ty + 50, title, 34, "bold", fill=TILE))
        for j, line in enumerate(lines):
            o.append(text(cx, ty + 92 + j * 33, line, 28, fill=TILE))
        o.append(text(cx, ty + dh - 20, state, 28, italic=True, fill=TEXT_2))

    # the trajectory: DiracX's minimal WMS aims to be the only native one
    gap_cx = (dirac_cx + dw / 2 + dx_cx - dw / 2) / 2
    traj_x2 = dx_cx - dw / 2 - 6
    o.append(f'<path d="M{dirac_cx + dw / 2 + 6:.1f},{ty + dh / 2:.1f} '
             f'H{traj_x2 - 14:.1f}" fill="none" stroke="#6b7280" stroke-width="3" '
             f'stroke-dasharray="8 7"/>' + arrowhead(traj_x2, ty + dh / 2, 1, 0))
    o.append(text(gap_cx, ty - 24, "aims to be the", 22, italic=True, fill=TEXT_2))
    o.append(text(gap_cx, ty - 2, "only native WMS", 22, italic=True, fill=TEXT_2))

    # --- level iii: the database layer, drawn as two cylinders. Shared where both still
    # read and write it, not shared where the new schema stands alone
    by3 = 570
    shared_cx, shared_rx, shared_h = 440, 260, 100
    solo_cx, solo_rx, solo_h = 1030, 130, 76
    shared_ry, solo_ry = shared_rx * 0.16, solo_rx * 0.16

    o.append(cylinder(shared_cx, by3, shared_rx, shared_h, "#c6cfdb", "dbshared"))
    o.append(text(shared_cx, by3 + shared_h + shared_ry + 40, "shared", 30, "bold", fill="#23384d"))
    o.append(text(shared_cx, by3 + shared_h + shared_ry + 70, "job, pilot and sandbox tables", 24, fill=TEXT_2))
    o.append(cylinder(solo_cx, by3, solo_rx, solo_h, TEAL, "dbsolo"))
    o.append(text(solo_cx, by3 + solo_h + solo_ry + 40, "not shared", 26, "bold", fill="#23384d"))
    o.append(text(solo_cx, by3 + solo_h + solo_ry + 68, "the new schema", 22, fill=TEXT_2))

    o.append(arrow(dirac_cx, ty + dh, dirac_cx, by3 - 6))
    o.append(arrow(dx_cx - 70, ty + dh, 700, by3 - 6, 14))
    o.append(arrow(dx_cx + 40, ty + dh, solo_cx, by3 - 6, 14))

    o.append("</svg>")
    return "".join(o)


def pipeline() -> str:
    """Not boxes: one artifact, changing shape in each pair of hands as it goes round a
    loop that takes one sprint or more. Each station is a clay platform with the people
    who hold the artifact standing on it, coloured by role; the representatives are drawn
    in several colours, one per community. They approve the product owner's document before
    any ADR is written, since an ADR is written mostly for the developers. The top row runs
    left to right up to the adopted ADR; the bottom row runs back, right to left, through
    the sprint's package, the representatives' review of it and the retrospective the
    scrum master leads, into the next round of requirements."""
    W, H = 2080, 960
    o = [head(W, H)]
    TOP, BOT = 280, 740            # screen y of each row's platforms
    K = 0.74                       # isometric scale of every station
    ROLE, CAP = 42, 36

    AMBER, ROSE, SAGE = cl.ACCENT["grid"], "#eeb0a2", "#b3d69a"
    LAVENDER = "#c3b4e4"
    ARCH = "#8fb3e3"
    SCRUM = "#e59cc0"
    SHEET = "#f4f6f9"
    REPS = [AMBER, ROSE, SAGE]

    def station(cx, plat, people, label, caption, gid, s=30):
        """A platform, people standing along its back edge, the role above, the step below."""
        it = Iso(cx, plat, K)
        out = [slab(it, -120, -70, 240, 140, 8, SLABC, f"{gid}-sl")]
        n = len(people)
        # along the back edge, spread in screen x; drawn back to front
        span = 0 if n == 1 else min(2.3 * s * (n - 1), 150)
        for i, base in enumerate(people):
            px = cx - span / 2 + (span / (n - 1) if n > 1 else 0) * i
            feet = plat - 8 + (6 if i % 2 else 0)
            out.append(person(px, feet - 3.45 * s, s, base, f"{gid}-p{i}"))
        out.append(text(cx, plat - 8 - 3.45 * s - s - 24, label, ROLE, "bold", fill=TEXT_1))
        for j, line in enumerate([caption] if isinstance(caption, str) else caption):
            out.append(text(cx, plat + 148 + j * 40, line, CAP, italic=True, fill=TEXT_2))
        return it, "".join(out)

    def sheet(it, x, y, base, z0=0.0, t=7):
        return cube(it, x, y, 120, 84, t, base, z0=z0, r=5)

    def lines_on(it, x, y, z, colour, wavy=False):
        """Three lines of writing on the top face of a sheet at (x, y), height z."""
        s = []
        for i, amp in enumerate((5, -4, 6)):
            yy = y + 20 + i * 22
            if wavy:
                pts = [it.p(x + 18 + j * 84 / 12, yy + amp * math.sin(j * math.pi / 3), z)
                       for j in range(13)]
            else:
                pts = [it.p(x + 18, yy, z), it.p(x + 102, yy, z)]
            d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
            s.append(f'<polyline points="{d}" fill="none" stroke="{colour}" stroke-width="3.4" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
        return "".join(s)

    def tick_badge(bx, by, gid):
        return (blob(bx, by, 24, 24, "#6fb57c", gid)
                + f'<path d="M{bx - 11:.1f},{by + 1:.1f} l7.5,9 l14,-17" fill="none" '
                  f'stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')

    def paper(it, base, ink, wavy=False, stack=1, checked=False, gid="ok"):
        x, y = -40, 14
        s = []
        for k in range(stack):
            s.append(sheet(it, x - k * 3, y - k * 3, base, z0=k * 9))
        z = (stack - 1) * 9 + 7
        s.append(lines_on(it, x - (stack - 1) * 3, y - (stack - 1) * 3, z, ink, wavy))
        if checked:
            s.append(tick_badge(*it.p(x + 104, y + 6, z + 44), gid))
        return "".join(s)

    def tasks(it):
        spots = [(-70, 22), (-26, 48), (-22, 8), (22, 30), (34, -4), (68, 46)]
        return "".join(cube(it, x, y, 30, 30, 24, TEAL, r=5)
                       for x, y in sorted(spots, key=lambda q: q[0] + q[1]))

    def parcel(it, checked=False, gid="pk"):
        s = cube(it, -14, 4, 64, 64, 54, TEAL, stripe=shade(TEAL, 0.5), r=8)
        if checked:
            s += tick_badge(*it.p(50, 4, 90), gid)
        return s

    def notes(it):
        """Retrospective notes, one colour per party at the table."""
        spots = [(-64, 18, AMBER), (-10, 44, LAVENDER), (-6, -6, TEAL), (44, 22, ROSE)]
        return "".join(cube(it, x, y, 40, 40, 4, c, r=3)
                       for x, y, c in sorted(spots, key=lambda q: q[0] + q[1]))

    # DUW12 version: no separate architects (developers design the ADR when a change is
    # large, after a proof of concept, and other developers approve it), seven steps.
    top_x = [270, 720, 1170, 1620]
    bot_x = [1620, 945, 270]
    specs = [
        (REPS, "representatives", "write requirements"),
        ([LAVENDER], "product owner", ["plans the backlog,", "sets priorities"]),
        (REPS, "representatives", "approve"),
        ([TEAL, TEAL, TEAL], "developers", ["split into tasks; large changes:", "proof of concept, then an ADR"]),
        ([TEAL, TEAL], "developers", "deliver an increment"),
        (REPS, "representatives", ["review the increment,", "their communities test it"]),
        ([SCRUM], "scrum master", "leads the retrospective"),
    ]
    places = [(x, TOP) for x in top_x] + [(x, BOT) for x in bot_x]

    stations = []
    for i, ((cx, plat), (people, label, caption)) in enumerate(zip(places, specs)):
        it, svg = station(cx, plat, people, label, caption, f"st{i}")
        stations.append(it)
        o.append(svg)
        bx, by = cx - 150, plat - 34
        o.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="22" fill="#6b7280"/>')
        o.append(text(bx, by + 10, str(i + 1), 28, "bold", fill="#ffffff"))
    o.append(paper(stations[0], SHEET, "#374151", wavy=True))
    o.append(paper(stations[1], SHEET, "#6b7280"))
    o.append(paper(stations[2], SHEET, "#6b7280", checked=True, gid="doc-ok"))
    o.append(tasks(stations[3]))
    o.append(parcel(stations[4]))
    o.append(parcel(stations[5], checked=True, gid="pk-ok"))
    o.append(notes(stations[6]))

    # hand to hand, along each row: rightwards on top, leftwards underneath
    for row, plat, sign in ((top_x, TOP, 1), (bot_x, BOT, -1)):
        for a, b in zip(row, row[1:]):
            o.append(arrow(a + sign * 140, plat + 40, b - sign * 140, plat + 40, sw=4.4))

    # round the ends: down on the right into the sprint, up on the left into the next round
    def turn(x, y1, y2, out):
        cx = x + out
        ux = -1 if out > 0 else 1
        x1 = x + (140 if out > 0 else -140)
        # the curve ends level, so the head continues it; the line stops inside the head
        tip = x1 + ux * 20
        return (f'<path d="M{x1:.1f},{y1:.1f} C{cx:.1f},{y1:.1f} {cx:.1f},{y2:.1f} '
                f'{tip - ux * 14:.1f},{y2:.1f}" fill="none" stroke="#6b7280" '
                f'stroke-width="4.4" stroke-linecap="round"/>'
                + arrowhead(tip, y2, ux, 0))
    o.append(turn(top_x[-1], TOP + 40, BOT + 40, 280))
    o.append(turn(top_x[0], BOT + 40, TOP + 40, -280))

    # in the middle of the loop, clear of both rows' captions and labels
    o.append(text(945, TOP + 222, "one or more sprints", CAP, "bold", italic=True, fill=TEXT_2))

    o.append("</svg>")
    return "".join(o)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    figs = {
        "fig-coexistence": coexistence,
        "fig-architecture": architecture,
        "fig-roadmap": roadmap,
        "fig-footprint": footprint,
        "fig-routes": routes,
        "fig-execution": execution,
        "fig-layers": layers,
        "fig-pipeline": pipeline,
    }
    # Name figures on the command line to rebuild only those; the committed PDFs of the
    # others then stay byte-identical.
    if sys.argv[1:]:
        figs = {k: v for k, v in figs.items() if k in sys.argv[1:]}
    for name, fn in figs.items():
        (OUT / f"{name}.svg").write_text(fn())
    try:
        import cairosvg
    except ImportError:
        print("wrote the SVGs; install cairosvg to get the PDFs", file=sys.stderr)
        return 0
    for name in figs:
        cairosvg.svg2pdf(url=str(OUT / f"{name}.svg"),
                         write_to=str(OUT / f"{name}.pdf"))
    print("wrote " + ", ".join(figs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
