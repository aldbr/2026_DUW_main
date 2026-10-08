#!/usr/bin/env python3
"""Figures for the DUW12 talk, same modelling-clay language as the CHEP26 paper.

    uv run --with cairosvg --with pillow python3 duw_figures.py [name ...]

Reuses the primitives copied from ../../papers/diracx-chep26-overleaf/figures
(claylib.py, build_figures.py). Writes SVGs straight into ../public/figures/.
"""
from __future__ import annotations
import pathlib, sys
import claylib as cl
from claylib import Iso, blob, card, cube, person, shade, slab, text
from claylib import contact_shadow
from build_figures import pipeline, arrow, arrowhead, cylinder, head, pill

OUT = pathlib.Path(__file__).parent.parent / "public" / "figures"
TEXT_1, TEXT_2 = cl.TEXT_1, cl.TEXT_2
BLUE, TEAL = cl.ACCENT["legacy"], cl.ACCENT["diracx"]
SLABC = "#dfe5ee"
AMBER = "#f0d9a6"
TITLE, SUB, SMALL = 44, 34, 28


def panel(x, y, w, h, title, fill="#f3f6fa", stroke="#d8e0ea"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + text(x + 36, y + 46, title, TITLE, "bold", anchor="start", fill=TEXT_2))


def bank(px, py, n, base, gid, title=None, sub=None, scale=0.6):
    it = Iso(px, py, scale)
    s = [slab(it, -112, -44, 224, 88, 10, SLABC, gid)]
    for i in range(n):
        s.append(cube(it, -84 + i * 56, -20, 38, 38, 26, base, r=6))
    if title:
        s.append(text(px, py + 112, title, SUB, "bold", fill=TEXT_1))
    if sub:
        s.append(text(px, py + 146, sub, SMALL, fill=TEXT_2))
    return "".join(s)


def dbs(cx, ytop, gid, base="#bfc7d3", n=3, label=None):
    o = []
    for i in range(n):
        o.append(cylinder(cx + (i - (n - 1) / 2) * 96, ytop, 38, 54, base, f"{gid}{i}"))
    if label:
        o.append(text(cx, ytop + 128, label, SMALL, fill=TEXT_2))
    return "".join(o)


def _frame(dirac_sub: str):
    W, H = 1600, 770
    o = [head(W, H)]
    o.append(panel(40, 70, 640, 450, "DIRAC", "#eef3fa", "#d3deec"))
    o.append(panel(760, 70, 800, 450, "DiracX"))
    o.append(f'<rect x="40" y="580" width="1520" height="170" rx="26" fill="#f6f7f9" stroke="#dde2e9" stroke-width="3"/>')
    return o


def step1() -> str:
    """The future client: DIRAC code calls a DiracX endpoint instead of its own service."""
    o = _frame("")
    o.append(bank(360, 330, 4, BLUE, "dbk", "services", "unchanged for users"))
    o.append(bank(1160, 330, 3, TEAL, "xbk", "job status endpoint", "JobStateUpdate"))
    o.append(pill(400, 92, 230, 62, AMBER, "fc", r=20))
    o.append(text(515, 133, "future client", SMALL + 2, "bold", fill="#5b4a1f"))
    o.append(arrow(640, 135, 1030, 238, -50, sw=4.4))
    o.append(text(1180, 128, "used first to load-test", SMALL, "bold", fill="#22456f"))
    o.append(text(1180, 162, "the new installation", SMALL, "bold", fill="#22456f"))
    o.append(dbs(800, 616, "db1", label="the same databases, no data moved"))
    o.append(arrow(360, 524, 700, 626, 14))
    o.append(arrow(1160, 524, 900, 626, 14))
    o.append("</svg>")
    return "".join(o)


def step2() -> str:
    """The transformation system: new tables, and a share of the work to either backend."""
    o = _frame("")
    o.append(bank(360, 330, 4, BLUE, "dbk", "DIRAC WMS", "a backend, as it is"))
    it = Iso(1010, 300, 0.62)
    o.append(slab(it, -130, -50, 260, 100, 10, "#d9ecea", "ts"))
    for i, col in enumerate((TEAL, "#9fd3a8", TEAL, "#9fd3a8", TEAL)):
        o.append(cube(it, -104 + i * 44, -22, 34, 34, 26, col, r=6))
    o.append(text(1010, 422, "Transformation System", SUB, "bold", fill=TEXT_1))
    o.append(text(1010, 456, "hands work to a backend", SMALL, fill=TEXT_2))
    o.append(bank(1440, 330, 3, TEAL, "xbk", "DiracX", "backend"))
    o.append(arrow(880, 296, 540, 296, 0, sw=4.4))
    o.append(text(716, 246, "90 %", TITLE, "bold", fill="#22456f"))
    o.append(arrow(1140, 296, 1340, 296, 0, sw=4.4))
    o.append(text(1240, 246, "10 %", TITLE, "bold", fill="#22456f"))
    o.append(text(1160, 170, "for example: the split can be anything, per installation, VO and type", SMALL - 4, italic=True, fill=TEXT_2))
    o.append(dbs(360, 616, "dbo", label="DIRAC's databases, as they are"))
    o.append(dbs(1160, 616, "dbn", base="#9fd3cb", n=2, label="new tables, shared with nothing"))
    o.append(arrow(360, 524, 360, 616, 0))
    o.append(arrow(1010, 524, 1100, 616, 0))
    o.append("</svg>")
    return "".join(o)


def _link(x1, y1, x2, y2):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#aab4be" '
            f'stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>')


def galaxies() -> str:
    """DIRAC and DiracX, each with the projects that orbit it."""
    W, H = 1600, 640
    o = [head(W, H)]

    def galaxy(cx, cy, base, name, sat, gid, sat_fill):
        out = []
        # satellites first, so the centre sits on top of the links
        for i, (label, dx, dy, w) in enumerate(sat):
            out.append(_link(cx, cy, cx + dx, cy + dy))
        it = Iso(cx, cy - 6, 0.95)
        out.append(slab(it, -112, -44, 224, 88, 10, SLABC, gid))
        for i in range(4):
            out.append(cube(it, -84 + i * 56, -20, 38, 38, 26, base, r=6))
        out.append(text(cx, cy + 112, name, TITLE + 8, "bold", fill=TEXT_1))
        for i, (label, dx, dy, w) in enumerate(sat):
            x, y = cx + dx - w / 2, cy + dy - 28
            out.append(pill(x, y, w, 56, sat_fill, f"{gid}s{i}", r=18))
            out.append(text(cx + dx, cy + dy + 10, label, SMALL, "bold", fill="#25405f"))
        return "".join(out)

    o.append(galaxy(400, 300, BLUE, "DIRAC", [
        ("WebAppDIRAC", -250, -190, 250), ("Pilot", 40, -225, 130), ("DIRACOS2", 250, -150, 190),
        ("extensions", -300, 120, 190), ("LHCbDIRAC, ...", 240, 195, 260)], "gd", "#cddcf0"))
    o.append(galaxy(1200, 300, TEAL, "DiracX", [
        ("diracx-web (experimental)", -270, -195, 400), ("diracx-charts", 110, -235, 250), ("signurlarity", 270, -125, 220),
        ("dirac CLI (experimental)", -300, 115, 380), ("interCEde", 280, 95, 190), ("extensions", 20, 215, 190)], "gx", "#c4e6e1"))
    # the bridge: the future client, and the databases both sides share
    o.append(arrow(560, 292, 1040, 292, 0, sw=4.4))
    o.append(text(800, 262, "components move over", SMALL + 2, "bold", fill="#22456f"))
    o.append(text(800, 346, "same databases while both run", SMALL - 2, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def flow() -> str:
    """How an issue moves across the board: how many are in each column, how fast the ones that leave go,
    and how long the ones still there have waited."""
    W, H = 1600, 640
    o = [head(W, H)]
    cols = [("Needs triage", "121", "227", "3", "#e6e9ee"),
            ("Needs design", "13", "190", "27", "#cddcf0"),
            ("Backlog", "34", "50", "7", "#c4e6e1"),
            ("In progress", "34", "67", "3", "#f0d9a6"),
            ("Done", "317", "", "", "#bfe0c4")]
    x0, w, gap = 40, 252, 52
    for i, (name, n, wait, left, base) in enumerate(cols):
        x = x0 + i * (w + gap)
        o.append(pill(x, 60, w, 84, base, f"fl{i}", r=28))
        o.append(text(x + w / 2, 113, name, SUB - 4, "bold", fill="#23384d"))
        o.append(text(x + w / 2, 226, n, 58, "bold", fill=TEXT_1))
        o.append(text(x + w / 2, 276, "issues", SMALL, fill=TEXT_2))
        if wait:
            o.append(f'<rect x="{x}" y="310" width="{w}" height="116" rx="18" fill="#fbe9dd"/>')
            o.append(text(x + w / 2, 362, wait + " days", 40, "bold", fill="#9a4a1f"))
            o.append(text(x + w / 2, 406, "median wait so far", SMALL - 5, fill="#9a4a1f"))
            o.append(text(x + w / 2, 486, left + " days", 36, "bold", fill=TEXT_1))
            o.append(text(x + w / 2, 524, "median stay of", SMALL - 5, fill=TEXT_2))
            o.append(text(x + w / 2, 552, "those who moved on", SMALL - 5, fill=TEXT_2))
        if i < len(cols) - 1:
            o.append(arrow(x + w + 8, 102, x + w + gap - 8, 102, 0, sw=4.4))
    o.append(text(800, 618, "issues on the planning board, data to 4 September 2026", SMALL - 4, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def _unused_flow() -> str:
    return ""


def mapping() -> str:
    """What changes for transformations: new names, no compatibility, and one bridge."""
    W, H = 1600, 640
    o = [head(W, H)]
    o.append(panel(40, 40, 600, 400, "DIRAC", "#eef3fa", "#d3deec"))
    o.append(panel(960, 40, 600, 400, "DiracX"))
    rows = [(160, "Production", "Workgraph"), (265, "Transformation", "Transformation"), (370, "Job", "Parcel")]
    for i, (y, a, b) in enumerate(rows):
        o.append(pill(150, y - 34, 380, 68, BLUE, f"ml{i}", r=24))
        o.append(text(340, y + 11, a, SUB, "bold", fill="#25405f"))
        o.append(pill(1070, y - 34, 380, 68, TEAL, f"mr{i}", r=24))
        o.append(text(1260, y + 11, b, SUB, "bold", fill="#1f4a44"))
    for y in (160, 265):
        o.append(f'<line x1="700" y1="{y}" x2="900" y2="{y}" stroke="#c0675a" stroke-width="5" stroke-dasharray="14 12" stroke-linecap="round"/>')
        o.append(text(800, y - 18, "not compatible", SMALL - 2, italic=True, fill="#9a4a1f"))
    o.append(arrow(1050, 370, 560, 370, 0, sw=5.4))
    o.append(text(800, 336, "a parcel runs as a job", SMALL, "bold", fill="#1f4a44"))
    o.append(text(800, 420, "on the DIRAC backend", SMALL - 2, fill=TEXT_2))
    o.append(f'<rect x="40" y="500" width="1520" height="110" rx="26" fill="#eaf4e6" stroke="#cfe3c8" stroke-width="3"/>')
    o.append(text(800, 546, "Reused, not rewritten", SUB, "bold", fill="#3d6b2c"))
    o.append(text(800, 586, "resource status (RSS) and data management", SMALL, fill="#3d6b2c"))
    o.append("</svg>")
    return "".join(o)


def pipe() -> str:
    """Work flows through specification, development and review. Development was widened by Scrum."""
    W, H = 1600, 560
    o = [head(W, H)]
    cy = 210
    segs = [(40, 430, 90, "#f0c9a0", "Specification", "requirements gathered since 1 July,", "then eight ADRs written", "sp"),
            (520, 560, 250, "#84cdc3", "Development", "optimised with Scrum:", "more contributors, a shrinking backlog", "dv"),
            (1130, 430, 90, "#f0c9a0", "Review", "two people give three quarters", "of the first reviews", "rv")]
    for x, w, h, col, name, l1, l2, gid in segs:
        o.append(pill(x, cy - h / 2, w, h, col, gid, r=h / 2 if h < 120 else 60))
        o.append(text(x + w / 2, cy + 12, name, TITLE, "bold", fill="#23384d"))
        o.append(text(x + w / 2, 400, l1, SMALL - 4, fill=TEXT_1))
        o.append(text(x + w / 2, 434, l2, SMALL - 4, fill=TEXT_1))
    o.append(arrow(478, cy, 512, cy, 0, sw=5))
    o.append(arrow(1088, cy, 1122, cy, 0, sw=5))
    o.append(text(255, 500, "bottleneck", SMALL + 2, "bold", fill="#9a4a1f"))
    o.append(text(1345, 500, "bottleneck", SMALL + 2, "bold", fill="#9a4a1f"))
    o.append(text(800, 500, "widened by Scrum", SMALL + 2, "bold", fill="#1f4a44"))
    o.append("</svg>")
    return "".join(o)


def roadmap2() -> str:
    """Long-running lines of work, and short exploratory spikes. No dates: priorities, not commitments."""
    W, H = 1600, 700
    o = [head(W, H)]
    LX, X0, X1 = 40, 470, 1540
    o.append(arrow(X0, 52, X1 + 40, 52, 0, sw=4))
    o.append(text(X0, 38, "now", SMALL, "bold", anchor="start", fill=TEXT_2))
    o.append(text(X1 + 40, 38, "later: not fixed in time", SMALL - 2, italic=True, anchor="end", fill=TEXT_2))
    lanes = [("Transformation System", X0, "#84cdc3", "starts at the hackathon this afternoon"),
             ("Job Wrapper", 700, "#9fd3a8", ""),
             ("Data Management System", 930, "#c4e6e1", ""),
             ("Resource status", X0, "#adc3e3", "read side first")]
    for i, (name, xs, col, note) in enumerate(lanes):
        y = 120 + i * 92
        o.append(text(LX, y + 46, name, SUB - 6, "bold", anchor="start", fill=TEXT_1))
        o.append(pill(xs, y + 8, X1 - xs, 62, col, f"ln{i}", r=31))
        o.append(arrowhead(X1 + 36, y + 39, 1, 0, length=26, half_width=14, color="#6b7280"))
        if note:
            o.append(text(xs + 34, y + 49, note, SMALL, italic=True, anchor="start", fill="#23384d"))
    o.append(f'<line x1="{LX}" y1="500" x2="{X1 + 40}" y2="500" stroke="#c9d0d8" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round"/>')
    o.append(text(LX, 560, "Spikes", SUB - 2, "bold", anchor="start", fill=TEXT_1))
    o.append(text(LX, 596, "exploratory work", SMALL - 2, italic=True, anchor="start", fill=TEXT_2))
    spikes = [("WMS", "matcher, interCEde", 470), ("Analytics and", "observability", 740), ("MCP server", "for agents", 1010), ("Clients", "web app, CLI", 1280)]
    for i, (t1, t2, x) in enumerate(spikes):
        o.append(contact_shadow(x + 125, 640, 120, 12, f"spsh{i}", 0.16))
        o.append(f'<rect x="{x}" y="530" width="250" height="104" rx="26" fill="#fff6e4" stroke="#e0a030" stroke-width="4" stroke-dasharray="12 9"/>')
        o.append(text(x + 125, 578, t1, SMALL + 2, "bold", fill="#7a5410"))
        o.append(text(x + 125, 614, t2, SMALL - 2, fill="#7a5410"))
    o.append("</svg>")
    return "".join(o)


def _box(x, y, w, h, title, fill, stroke):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + text(x + 22, y + 44, title, 34, "bold", anchor="start", fill=TEXT_2))


def mini_model() -> str:
    """DiracX's new transformation system uses DIRAC's WMS as one backend; its tables are its own."""
    W, H = 760, 420
    o = [head(W, H)]
    o.append(_box(20, 20, 300, 300, "DIRAC", "#eef3fa", "#d3deec"))
    o.append(_box(440, 20, 300, 300, "DiracX", "#f3f6fa", "#d8e0ea"))
    o.append(pill(60, 150, 220, 80, BLUE, "mm1", r=26))
    o.append(text(170, 202, "WMS", 40, "bold", fill="#25405f"))
    o.append(pill(462, 130, 256, 120, TEAL, "mm2", r=30))
    o.append(text(590, 182, "Transformation", 28, "bold", fill="#1f4a44"))
    o.append(text(590, 220, "System", 28, "bold", fill="#1f4a44"))
    o.append(arrow(462, 190, 290, 190, 0, sw=5))
    o.append(dbs(590, 342, "mmd", base="#9fd3cb", n=2))
    o.append(text(420, 400, "new tables", 30, italic=True, anchor="end", fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def mini_future() -> str:
    """A DIRAC client reaches either the DIRAC service or the DiracX one; both share the databases."""
    W, H = 760, 420
    o = [head(W, H)]
    o.append(pill(250, 20, 260, 76, AMBER, "mf0", r=24))
    o.append(text(380, 70, "DIRAC client", 36, "bold", fill="#5b4a1f"))
    o.append(pill(40, 170, 270, 80, BLUE, "mf1", r=26))
    o.append(text(175, 222, "DIRAC service", 32, "bold", fill="#25405f"))
    o.append(pill(450, 170, 270, 80, TEAL, "mf2", r=26))
    o.append(text(585, 222, "DiracX service", 32, "bold", fill="#1f4a44"))
    o.append(arrow(330, 104, 200, 162, -10, sw=5))
    o.append(arrow(430, 104, 560, 162, -10, sw=5))
    o.append(dbs(380, 300, "mfd", n=3))
    o.append(arrow(175, 258, 300, 304, 10, sw=4))
    o.append(arrow(585, 258, 460, 304, 10, sw=4))
    o.append(text(380, 410, "same databases", 30, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def mini_protocols() -> str:
    """Systems internal to DIRAC give way to standard protocols."""
    W, H = 760, 420
    o = [head(W, H)]
    rows = [("Monitoring", "OpenTelemetry", 70), ("Accounting", "Analytics", 230)]
    for i, (a, b, y) in enumerate(rows):
        o.append(pill(30, y, 270, 90, BLUE, f"mp{i}a", r=28))
        o.append(text(165, y + 58, a, 36, "bold", fill="#25405f"))
        o.append(pill(440, y, 300, 90, "#9fd3a8", f"mp{i}b", r=28))
        o.append(text(590, y + 57, b, 31, "bold", fill="#2d5a33"))
        o.append(arrow(312, y + 45, 430, y + 45, 0, sw=5))
    o.append(text(165, 380, "DIRAC", 30, italic=True, fill=TEXT_2))
    o.append(text(590, 380, "DiracX", 30, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def journey() -> str:
    """The main line of DiracX milestones (labels above), and the proofs of concept that ran
    beside it (below), each tied to the line by a dashed arrow at the time it started."""
    W, H = 1600, 680
    o = [head(W, H)]
    Y = 330
    ms = [("Jul 2023", ["DiracX starts:", "services, authentication"]),
          ("2025", ["Job status through", "a future client"]),
          ("Apr 2025", ["LHCb extension", "in production"]),
          ("Oct 2025", ["First official", "release"]),
          ("Jan 2026", ["Scrum"]),
          ("Feb 2026", ["RSS:", "read side"]),
          ("Apr 2026", ["Tasks", "framework"]),
          ("Jul 2026", ["Transformation", "system: ADRs"])]
    xs = [200 + i * 180 for i in range(len(ms))]
    o.append(f'<line x1="60" y1="{Y}" x2="1560" y2="{Y}" stroke="#8aa7c4" stroke-width="8" stroke-linecap="round"/>')
    o.append(arrowhead(1590, Y, 1, 0, length=34, half_width=18, color="#8aa7c4"))
    for i, (x, (date, lines)) in enumerate(zip(xs, ms)):
        top = 20 if i % 2 else 150
        o.append(f'<line x1="{x}" y1="{top + 40 + 32 * len(lines)}" x2="{x}" y2="{Y - 20}" stroke="#c0cad4" stroke-width="3"/>')
        o.append(text(x, top + 22, date, 24, "bold", fill=TEXT_2))
        for j, l in enumerate(lines):
            o.append(text(x, top + 54 + j * 32, l, 27, "bold" if j == 0 else "normal", fill=TEXT_1))
        o.append(blob(x, Y, 17, 17, TEAL if i < 7 else "#9fd3a8", f"jm{i}"))
    o.append(text(60, 662, "In parallel: proofs of concept, linked to when they started", 26, "bold", anchor="start", fill="#7a5410"))
    pocs = [("dirac-cwl", "2023, with CTAO", 170, 230), ("Web app", "2025", 410, 420), ("Pilot security", "2025", 650, 470),
            ("Matchmaking", "2026", 930, 1110), ("interCEde", "2026", 1170, 1250), ("Analytics,", "observability", 1410, 1300)]
    for i, (t1, t2, cx, lx) in enumerate(pocs):
        w = 220
        o.append(f'<path d="M{cx},520 C{cx},470 {lx},440 {lx},{Y + 40}" fill="none" stroke="#e0a030" stroke-width="3.5" stroke-dasharray="9 8"/>')
        o.append(arrowhead(lx, Y + 22, 0, -1, length=18, half_width=9, color="#e0a030"))
        o.append(f'<rect x="{cx - w / 2}" y="520" width="{w}" height="92" rx="24" fill="#fff6e4" stroke="#e0a030" stroke-width="4" stroke-dasharray="12 9"/>')
        o.append(text(cx, 560, t1, 27, "bold", fill="#7a5410"))
        o.append(text(cx, 594, t2, 23, fill="#7a5410"))
    o.append("</svg>")
    return "".join(o)


def collab() -> str:
    """Groups of part-time contributors, each a small cluster of clay people, linked by dashed
    two-way arrows: the point is how they work together, not who does how much."""
    import math
    W, H = 1600, 700
    o = [head(W, H)]
    groups = [("LHCb", "#8fb3e3"), ("CTAO", "#c3b4e4"), ("CMS", "#b3d69a"), ("FCC", "#eeb0a2"),
              ("GridPP", "#f3cf7e"), ("IN2P3", "#e59cc0"), ("EGI", "#84cdc3"), ("Belle II, IHEP, ...", "#d3d8df")]
    cx, cy, rx, ry = 800, 350, 620, 250
    pts = []
    for i, _ in enumerate(groups):
        ang = -math.pi / 2 + 2 * math.pi * i / len(groups)
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    def link(p, q):
        (x1, y1), (x2, y2) = p, q
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        sx, sy, ex, ey = x1 + ux * 100, y1 + uy * 80, x2 - ux * 100, y2 - uy * 80
        return (f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#9aa6b2" stroke-width="3.2" stroke-dasharray="10 9"/>'
                + arrowhead(ex, ey, ux, uy, length=16, half_width=8, color="#9aa6b2")
                + arrowhead(sx, sy, -ux, -uy, length=16, half_width=8, color="#9aa6b2"))
    n = len(pts)
    for i in range(n):
        o.append(link(pts[i], pts[(i + 1) % n]))
    for i, j in ((0, 4), (2, 6), (1, 5), (3, 7)):
        o.append(link(pts[i], pts[j]))
    o.append(card(cx - 230, cy - 64, 460, 128))
    o.append(text(cx, cy - 10, "how do we work", 38, "bold", fill=TEXT_1))
    o.append(text(cx, cy + 36, "best together?", 38, "bold", fill=TEXT_1))
    for i, ((x, y), (name, col)) in enumerate(zip(pts, groups)):
        for k, dx in enumerate((-36, 0, 36)):
            o.append(person(x + dx, y - 56 + (8 if k != 1 else 0), 15, col, f"cp{i}{k}"))
    o.append("</svg>")
    return "".join(o)


FIGS = {"fig-collab": collab, "fig-journey": journey, "fig-mini-model": mini_model, "fig-mini-future": mini_future, "fig-mini-protocols": mini_protocols, "fig-pipeline": pipeline, "fig-roadmap2": roadmap2, "fig-mapping": mapping, "fig-pipe": pipe, "fig-step1": step1, "fig-step2": step2, "fig-galaxies": galaxies, "fig-flow": flow}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    figs = {k: v for k, v in FIGS.items() if not sys.argv[1:] or k in sys.argv[1:]}
    for name, fn in figs.items():
        (OUT / f"{name}.svg").write_text(fn())
    print("wrote " + ", ".join(figs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
