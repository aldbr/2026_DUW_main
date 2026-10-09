#!/usr/bin/env python3
"""Figures for the DUW12 WMS talk, same modelling-clay language as the directions talk.

    uv run --with cairosvg --with pillow python3 figures/wms_figures.py [name ...]

Primitives come from claylib.py and build_figures.py (shared with the other DUW12
deck and the CHEP26 paper). Writes SVGs straight into ../public/figures/.
"""
from __future__ import annotations

import pathlib
import sys

import claylib as cl
from claylib import Iso, contact_shadow, cube, shade, slab, text
from build_figures import arrow, arrowhead, cylinder, head, pill


def dbs(cx, ytop, gid, base="#bfc7d3", n=3):
    return "".join(cylinder(cx + (i - (n - 1) / 2) * 96, ytop, 38, 54, base, f"{gid}{i}") for i in range(n))

OUT = pathlib.Path(__file__).parent.parent / "public" / "figures"
TEXT_1, TEXT_2 = cl.TEXT_1, cl.TEXT_2
BLUE, TEAL = cl.ACCENT["legacy"], cl.ACCENT["diracx"]
GREEN = "#9fd3a8"
AMBER = "#f0d9a6"
SLABC = "#dfe5ee"
TITLE, SUB, SMALL = 44, 34, 28
INK_BLUE, INK_TEAL, INK_AMBER = "#25405f", "#1f4a44", "#5b4a1f"


def panel(x, y, w, h, title, fill="#f3f6fa", stroke="#d8e0ea", size=TITLE - 6):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + text(x + 30, y + 46, title, size, "bold", anchor="start", fill=TEXT_2))


def spike(x, y, w, h, t1, t2=None):
    """A proof of concept: dashed amber outline, as on the directions roadmap."""
    o = [contact_shadow(x + w / 2, y + h + 6, w * 0.48, 12, f"sp{x}{y}", 0.14),
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="#fff6e4" stroke="#e0a030" stroke-width="4" stroke-dasharray="12 9"/>']
    if t2:
        o += [text(x + w / 2, y + h / 2 - 4, t1, SMALL + 2, "bold", fill="#7a5410"),
              text(x + w / 2, y + h / 2 + 30, t2, SMALL - 4, fill="#7a5410")]
    else:
        o.append(text(x + w / 2, y + h / 2 + 10, t1, SMALL + 2, "bold", fill="#7a5410"))
    return "".join(o)


def label_pill(x, y, w, h, base, gid, t1, ink, t2=None, size=SMALL):
    o = [pill(x, y, w, h, base, gid, r=min(h / 2, 26))]
    if t2:
        o += [text(x + w / 2, y + h / 2 - 4, t1, size, "bold", fill=ink),
              text(x + w / 2, y + h / 2 + 28, t2, size - 6, fill=ink)]
    else:
        o.append(text(x + w / 2, y + h / 2 + size * 0.36, t1, size, "bold", fill=ink))
    return "".join(o)


def site(px, py, n, base, gid, scale=0.55, chips=()):
    """A resource: a slab with clay boxes on it (worker nodes)."""
    it = Iso(px, py, scale)
    o = [slab(it, -120, -48, 240, 96, 10, SLABC, gid)]
    for i in range(n):
        o.append(cube(it, -92 + i * 58, -22, 40, 40, 30, base, r=6))
    return "".join(o)


def chip(x, y, s, fill="#ffffff", ink=TEXT_2, w=None):
    w = w or 18 * len(s) + 30
    return (f'<rect x="{x - w / 2:.0f}" y="{y}" width="{w:.0f}" height="40" rx="20" fill="{fill}" stroke="#cfd6df" stroke-width="2.5"/>'
            + text(x, y + 29, s, 24, fill=ink))


# ----------------------------------------------------------------------------- figures

def landscape() -> str:
    """Resources at the bottom, the interfaces that reach them, and the WMS on top."""
    W, H = 1600, 860
    o = [head(W, H)]
    # layer labels, left
    for y, t in [(110, "WMS"), (370, "Interfaces"), (640, "Resources")]:
        o.append(text(40, y, t, SUB, "bold", anchor="start", fill=TEXT_2))
    # WMS
    o.append(label_pill(300, 60, 560, 96, BLUE, "lw1", "DIRAC WMS", INK_BLUE, "pull (pilots) and push", size=SUB))
    o.append(label_pill(960, 60, 600, 96, TEAL, "lw2", "DiracX", INK_TEAL, "transformation system first", size=SUB))
    # interfaces
    o.append(f'<rect x="300" y="290" width="1260" height="150" rx="26" fill="#f3f6fa" stroke="#d8e0ea" stroke-width="3"/>')
    ces = [("HTCondorCE", 320, 210), ("AREX", 550, 160), ("SSH + batch", 730, 230), ("Cloud", 980, 170)]
    for i, (n, x, w) in enumerate(ces):
        o.append(label_pill(x, 312, w, 64, BLUE, f"lce{i}", n, INK_BLUE, size=SMALL - 2))
    o.append(text(760, 420, "DIRAC computing elements", SMALL - 4, italic=True, fill=TEXT_2))
    o.append(spike(1250, 306, 290, 116, "interCEde", "shared CE library (POC)"))
    o.append(arrow(580, 162, 580, 284, 0, sw=4))
    o.append(arrow(1260, 162, 1395, 298, 0, sw=4))
    # resources
    res = [(560, "Grid sites", "CE, outbound network, CVMFS", ["x86_64", "aarch64"]),
           (1000, "HPC centres", "often no outbound, no CVMFS", ["aarch64", "GPU"]),
           (1400, "Clouds", "VMs on demand", ["x86_64"])]
    for i, (cx, t, sub, chips) in enumerate(res):
        o.append(site(cx, 600, 4 if i < 2 else 3, "#f3cf7e" if i == 0 else ("#d9b8e8" if i == 1 else "#bfe3f0"), f"lr{i}"))
        o.append(text(cx, 720, t, SUB - 2, "bold", fill=TEXT_1))
        o.append(text(cx, 756, sub, SMALL - 6, fill=TEXT_2))
        for j, c in enumerate(chips):
            o.append(chip(cx - (len(chips) - 1) * 75 + j * 150, 784, c))
        o.append(arrow(cx, 446, cx, 540, 0, sw=3))
    o.append("</svg>")
    return "".join(o)


def pullpush() -> str:
    """DIRAC's two models. Pull: pilots on the node ask the matcher. Push: an agent next to the
    matcher asks on behalf of a resource that cannot reach DIRAC, and submits the wrapper."""
    W, H = 1600, 820
    o = [head(W, H)]
    o.append(panel(30, 20, 1010, 780, "Pull: pilots fetch jobs", "#eef3fa", "#d3deec"))
    o.append(panel(1080, 20, 490, 780, "Push: an agent submits", "#f6f3ec", "#e6dfcf"))
    # central services, pull side
    o.append(cylinder(150, 120, 60, 70, "#bfc7d3", "pq"))
    o.append(text(150, 250, "task queues", SMALL - 2, fill=TEXT_2))
    o.append(label_pill(260, 110, 230, 80, BLUE, "pm", "Matcher", INK_BLUE, size=SMALL + 2))
    o.append(label_pill(600, 110, 280, 80, BLUE, "psd", "SiteDirector", INK_BLUE, size=SMALL + 2))
    o.append(label_pill(640, 300, 200, 70, "#c7cfd9", "pce", "CE", TEXT_1))
    o.append(arrow(740, 196, 740, 294, 0, sw=4))
    o.append(text(760, 255, "1  submit pilots", SMALL - 4, anchor="start", fill=TEXT_2))
    # worker node
    o.append(f'<rect x="100" y="420" width="900" height="350" rx="24" fill="#fbf7ee" stroke="#e8dcc0" stroke-width="3"/>')
    o.append(text(130, 462, "worker node", SMALL - 2, "bold", anchor="start", fill="#8a6d2c"))
    o.append(label_pill(150, 500, 230, 72, AMBER, "ppi", "pilot", INK_AMBER, size=SMALL + 2))
    o.append(label_pill(450, 500, 250, 72, AMBER, "pja", "JobAgent", INK_AMBER, size=SMALL + 2))
    o.append(label_pill(450, 640, 250, 72, GREEN, "pjw", "JobWrapper", "#2d5a33", size=SMALL + 2))
    o.append(label_pill(770, 640, 200, 72, "#e9eef4", "ppl", "payload", TEXT_1, size=SMALL))
    o.append(arrow(740, 376, 300, 494, 30, sw=4))
    o.append(text(790, 430, "2  pilot starts", SMALL - 4, anchor="start", fill=TEXT_2))
    o.append(arrow(384, 536, 444, 536, 0, sw=4))
    o.append(arrow(575, 494, 380, 196, -60, sw=4))
    o.append(text(470, 330, "3  match a job", SMALL - 4, anchor="end", fill=TEXT_2))
    o.append(arrow(575, 578, 575, 634, 0, sw=4))
    o.append(arrow(704, 676, 764, 676, 0, sw=4))
    # push side
    o.append(label_pill(1110, 110, 230, 80, BLUE, "qm", "Matcher", INK_BLUE, size=SMALL + 2))
    o.append(label_pill(1110, 250, 420, 80, AMBER, "qpa", "PushJobAgent", INK_AMBER, size=SMALL + 2))
    o.append(arrow(1225, 244, 1225, 196, 0, sw=4))
    o.append(label_pill(1210, 400, 200, 70, "#c7cfd9", "qce", "CE", TEXT_1))
    o.append(arrow(1310, 336, 1310, 394, 0, sw=4))
    o.append(f'<rect x="1110" y="520" width="430" height="250" rx="24" fill="#fbf7ee" stroke="#e8dcc0" stroke-width="3"/>')
    o.append(text(1130, 562, "HPC, no outbound", SMALL - 4, "bold", anchor="start", fill="#8a6d2c"))
    o.append(label_pill(1200, 590, 250, 72, GREEN, "qjw", "JobWrapper", "#2d5a33", size=SMALL + 2))
    o.append(text(1325, 720, "pre/post-processing", SMALL - 6, italic=True, fill=TEXT_2))
    o.append(text(1325, 750, "stay with the agent", SMALL - 6, italic=True, fill=TEXT_2))
    o.append(arrow(1390, 476, 1400, 584, 0, sw=4))
    o.append("</svg>")
    return "".join(o)


def slot() -> str:
    """The time budget of a slot, and where each v9.1 change acts on it."""
    W, H = 1600, 520
    o = [head(W, H)]
    X0, X1, Y, BH = 60, 1540, 200, 90
    segs = [(X0, 230, "#c7cfd9", "pilot", TEXT_1),
            (230, 1180, "#9fd3a8", "payload: events, files", "#2d5a33"),
            (1180, X1, AMBER, "StopMargin", INK_AMBER)]
    for i, (a, b, col, t, ink) in enumerate(segs):
        o.append(pill(a + 4, Y, b - a - 8, BH, col, f"sl{i}", r=20))
        o.append(text((a + b) / 2, Y + 56, t, SMALL + 2, "bold", fill=ink))
    # top scale: the slot
    o.append(arrow(X0, 120, X1, 120, 0, sw=3))
    o.append(arrowhead(X0, 120, -1, 0, length=20, half_width=9))
    o.append(text((X0 + X1) / 2, 100, "CPU time left in the slot: read once, from the pilot configuration", SMALL - 2, fill=TEXT_2))
    # markers below
    marks = [(230, "#8746", "margin reserved", "before matching"),
             (1180, "#8814", "stop signal:", "payload ends cleanly"),
             (1400, "#8528", "if killed, the reason", "is reported")]
    for x, pr, l1, l2 in marks:
        o.append(f'<line x1="{x}" y1="{Y + BH + 8}" x2="{x}" y2="{Y + BH + 70}" stroke="#6b7280" stroke-width="3" stroke-dasharray="6 6"/>')
        o.append(text(x, Y + BH + 108, pr, SMALL - 2, "bold", fill=TEXT_1))
        o.append(text(x, Y + BH + 142, l1, SMALL - 6, fill=TEXT_2))
        o.append(text(x, Y + BH + 172, l2, SMALL - 6, fill=TEXT_2))
    o.append(text(1360, Y - 18, "outputs uploaded", SMALL - 6, italic=True, fill=INK_AMBER))
    o.append("</svg>")
    return "".join(o)


def parcels() -> str:
    """DX-ADR-002/003: CWL documents become parcels; a dispatcher hands each parcel to a backend.
    The parcel table is the record; a jobs table, if any, is private to one backend."""
    W, H = 1600, 760
    o = [head(W, H)]
    # sources
    o.append(label_pill(40, 70, 330, 96, GREEN, "pc1", "user job", "#2d5a33", "a CWL document"))
    o.append(label_pill(40, 220, 330, 96, GREEN, "pc2", "workgraph", "#2d5a33", "CWL: steps = transformations"))
    o.append(arrow(376, 118, 520, 190, 10, sw=4))
    o.append(arrow(376, 268, 520, 220, -6, sw=4))
    o.append(label_pill(530, 150, 300, 96, TEAL, "pc3", "parcels", INK_TEAL, "the record", size=SUB))
    o.append(cylinder(590, 300, 60, 50, "#9fd3cb", "pcdb"))
    o.append(text(590, 396, "no central JobDB", SMALL - 4, italic=True, fill=TEXT_2))
    o.append(arrow(836, 198, 960, 198, 0, sw=4))
    o.append(label_pill(970, 150, 300, 96, TEAL, "pc4", "dispatcher", INK_TEAL, "picks a backend", size=SUB))
    # backends
    o.append(panel(40, 470, 1520, 270, "Backends", "#f6f7f9", "#dde2e9", size=SUB - 2))
    bks = [(80, 350, BLUE, "legacy-dirac", INK_BLUE, "DIRAC WMS, as it is", False),
           (470, 400, TEAL, "diracx-pilot", INK_TEAL, "matcher, pilots, jobs table", True),
           (910, 300, "#c7cfd9", "htcondor", TEXT_1, "glideins", False),
           (1250, 280, "#c7cfd9", "diracx-remote", TEXT_1, "push", True)]
    for i, (x, w, col, t, ink, sub, future) in enumerate(bks):
        if future:
            o.append(f'<rect x="{x}" y="560" width="{w}" height="110" rx="26" fill="#ffffff" stroke="#8fb9b2" stroke-width="4" stroke-dasharray="12 9"/>')
            o.append(text(x + w / 2, 606, t, SMALL + 2, "bold", fill=ink))
            o.append(text(x + w / 2, 644, sub, SMALL - 6, fill=ink))
        else:
            o.append(label_pill(x, 560, w, 110, col, f"bk{i}", t, ink, sub, size=SMALL + 2))
        o.append(arrow(1120, 252, x + w / 2 + (60 if i == 0 else 0), 552, 0, sw=3))
    o.append(text(255, 712, "first: DIRAC runs every parcel", SMALL - 6, italic=True, fill=TEXT_2))
    o.append(text(670, 712, "the DiracX WMS: to be designed", SMALL - 6, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def backends() -> str:
    """Before: port DIRAC services one by one onto the same databases.
    Now: the DiracX transformation system dispatches to compute backends, each with its own data."""
    W, H = 1600, 760
    o = [head(W, H)]
    o.append(panel(30, 20, 680, 720, "Before: port piece by piece", "#f6f7f9", "#dde2e9", size=SUB))
    o.append(panel(750, 20, 820, 720, "Now: separate compute backends", "#eef7f5", "#cfe6e1", size=SUB))
    # before
    rows = ["JobStateUpdate", "JobMonitoring", "JobManager", "Matcher"]
    for i, n in enumerate(rows):
        y = 150 + i * 88
        o.append(label_pill(70, y, 250, 66, BLUE, f"bp{i}", n, INK_BLUE, size=SMALL - 4))
        o.append(arrow(328, y + 33, 404, y + 33, 0, sw=3.4))
        if i == 0:
            o.append(label_pill(412, y, 250, 66, TEAL, f"bq{i}", n, INK_TEAL, size=SMALL - 4))
        else:
            o.append(f'<rect x="412" y="{y}" width="250" height="66" rx="26" fill="#ffffff" stroke="#8fb9b2" stroke-width="3" stroke-dasharray="10 8"/>')
            o.append(text(537, y + 43, n, SMALL - 4, fill="#5f8781"))
    o.append(text(195, 132, "DIRAC", SMALL - 2, "bold", fill=TEXT_2))
    o.append(text(537, 132, "DiracX", SMALL - 2, "bold", fill=TEXT_2))
    o.append(dbs(366, 540, "bdb", n=3))
    o.append(text(366, 646, "the same databases,", SMALL - 4, italic=True, fill=TEXT_2))
    o.append(text(366, 680, "the same data model", SMALL - 4, italic=True, fill=TEXT_2))
    # now
    o.append(label_pill(940, 90, 440, 100, TEAL, "nts", "Transformation System", INK_TEAL, "parcels, in DiracX", size=SUB - 2))
    bk = [(790, BLUE, "DIRAC WMS", INK_BLUE, "stable, fixes only", False),
          (1060, TEAL, "DiracX WMS", INK_TEAL, "later, when needed", True),
          (1330, "#c7cfd9", "HTCondor", TEXT_1, "glideins", False)]
    for i, (x, col, t, ink, sub, fut) in enumerate(bk):
        if fut:
            o.append(f'<rect x="{x}" y="330" width="220" height="104" rx="26" fill="#ffffff" stroke="#8fb9b2" stroke-width="4" stroke-dasharray="12 9"/>')
            o.append(text(x + 110, 374, t, SMALL, "bold", fill=ink))
            o.append(text(x + 110, 410, sub, SMALL - 8, fill=ink))
        else:
            o.append(label_pill(x, 330, 220, 104, col, f"nb{i}", t, ink, sub, size=SMALL))
        o.append(arrow(1160, 196, x + 110, 322, 0, sw=3.4))
    o.append(dbs(900, 520, "ndb1", base="#bfc7d3", n=2))
    o.append(dbs(1170, 520, "ndb2", base="#9fd3cb", n=2))
    o.append(text(1035, 646, "each backend keeps its own data", SMALL - 4, italic=True, fill=TEXT_2))
    o.append(text(1035, 680, "and its own data model", SMALL - 4, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def parcels_only() -> str:
    """No jobs in DiracX: user jobs and workgraphs become parcels. The JobDB already in DiracX is legacy."""
    W, H = 1600, 520
    o = [head(W, H)]
    o.append(label_pill(40, 60, 340, 100, GREEN, "po1", "user job", "#2d5a33", "a CWL document"))
    o.append(label_pill(40, 220, 340, 100, GREEN, "po2", "workgraph", "#2d5a33", "CWL: steps = transformations"))
    o.append(arrow(386, 110, 540, 176, 10, sw=4))
    o.append(arrow(386, 270, 540, 206, -6, sw=4))
    o.append(label_pill(550, 140, 320, 100, TEAL, "po3", "parcel", INK_TEAL, "the record of work", size=SUB))
    o.append(arrow(876, 190, 1000, 190, 0, sw=4))
    o.append(label_pill(1010, 140, 320, 100, TEAL, "po4", "dispatcher", INK_TEAL, "to a backend", size=SUB))
    o.append(arrow(1336, 190, 1440, 190, 0, sw=4))
    o.append(text(1460, 200, "...", SUB, "bold", anchor="start", fill=TEXT_2))
    o.append(cylinder(710, 330, 60, 50, "#9fd3cb", "podb"))
    o.append(text(710, 440, "parcel tables", SMALL - 4, italic=True, fill=TEXT_2))
    # legacy JobDB, greyed and dashed
    o.append(f'<rect x="1000" y="330" width="560" height="160" rx="26" fill="#f6f7f9" stroke="#c3c9d2" stroke-width="3" stroke-dasharray="12 9"/>')
    o.append(cylinder(1090, 370, 50, 44, "#d5d9df", "pojdb"))
    o.append(text(1180, 392, "JobDB in DiracX: legacy", SMALL - 2, "bold", anchor="start", fill=TEXT_2))
    o.append(text(1180, 430, "tests a deployment only;", SMALL - 6, anchor="start", fill=TEXT_2))
    o.append(text(1180, 462, "deleted once all are on DiracX", SMALL - 6, anchor="start", fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def backends3d() -> str:
    """The transformation system (DiracX) on its platform, dispatching parcels to three
    compute backends, each its own platform with its own data. Isometric clay."""
    W, H = 1600, 860
    o = [head(W, H)]
    it = Iso(800, 150, 0.95)
    P = it.p
    # transformation system, at the back
    o.append(slab(it, 20, 0, 240, 180, 14, TEAL, "t3-ts"))
    cubes = []
    for i in range(3):
        for j in range(2):
            x, y = 50 + i * 66, 40 + j * 70
            cubes.append((x + y, cube(it, x, y, 40, 40, 26, "#5fb3a8", r=6)))
    o += [c for _, c in sorted(cubes)]
    tx, ty = P(20, 0, 0)
    o.append(text(tx - 30, ty - 40, "Transformation System", SUB, "bold", anchor="end", fill=INK_TEAL))
    o.append(text(tx - 30, ty - 4, "in DiracX: work is a parcel", SMALL - 2, anchor="end", fill=TEXT_2))
    # backends, in a row in front
    S = 760
    arrows = []
    specs = [(-600, "#adc3e3", "DIRAC WMS", "stable: fixes only", INK_BLUE, "solid"),
             (0, TEAL, "DiracX WMS", "later, when needed", INK_TEAL, "ghost"),
             (600, "#c7cfd9", "HTCondor", "glideins", TEXT_1, "solid")]
    for k, (D, col, name, sub, ink, kind) in enumerate(specs):
        cx, cy = (S + D) / 2, (S - D) / 2
        x0, y0 = cx - 110, cy - 110
        start = {-600: P(20, 180, 0), 0: P(260, 180, 0), 600: P(260, 0, 0)}[D]
        end = P(x0 + 12, y0 + 12, 0)
        arrows.append(arrow(start[0], start[1] + 8, end[0], end[1] - 4, 0, sw=4.4))
        if kind == "ghost":
            top = [P(x0, y0, 0), P(x0 + 220, y0, 0), P(x0 + 220, y0 + 220, 0), P(x0, y0 + 220, 0)]
            d = " ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in top)
            o.append(f'<polygon points="{d}" fill="#eef7f5" stroke="#8fb9b2" stroke-width="4" stroke-dasharray="14 10" stroke-linejoin="round"/>')
            for (x, y) in [(x0 + 50, y0 + 60), (x0 + 120, y0 + 60), (x0 + 85, y0 + 130)]:
                o.append(f'<g opacity="0.35">{cube(it, x, y, 46, 46, 34, TEAL, r=6)}</g>')
        else:
            o.append(slab(it, x0, y0, 220, 220, 14, col, f"t3-b{k}"))
            cs = []
            for (x, y) in [(x0 + 40, y0 + 40), (x0 + 110, y0 + 40), (x0 + 40, y0 + 110), (x0 + 110, y0 + 110)]:
                cs.append((x + y, cube(it, x, y, 46, 46, 34, shade(col, -0.05), slots=True, r=6)))
            o += [c for _, c in sorted(cs)]
        # its own data: two cylinders beside the platform
        dx, dy = P(x0 + 220, y0 + 220, 0)
        base = "#9fd3cb" if kind == "ghost" else "#bfc7d3"
        for m in range(2):
            o.append(cylinder(dx - 150 + m * 70, dy + 10, 28, 40, base, f"t3-db{k}{m}"))
        lx, ly = P(x0 + 220, y0 + 220, 0)
        o.append(text(lx - 70, ly + 112, name, SUB, "bold", fill=ink))
        o.append(text(lx - 70, ly + 148, sub, SMALL - 2, fill=TEXT_2))
    o += arrows
    o.append(text(800, H - 24, "each backend keeps its own data and its own data model", SMALL - 2, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


# ----------------------------------------------------------------------------- world map
LAND = pathlib.Path(__file__).parent / "land-110m.json"   # Natural Earth via world-atlas 2.0.2, public domain


def _equal_earth(lon, lat):
    """Equal Earth projection (Savric, Patterson, Jenny 2018), unit radius."""
    import math
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
    M = math.sqrt(3) / 2
    p = math.asin(M * math.sin(math.radians(lat)))
    p2 = p * p
    p6 = p2 * p2 * p2
    x = math.radians(lon) * math.cos(p) / (M * (A1 + 3 * A2 * p2 + p6 * (7 * A3 + 9 * A4 * p2)))
    y = p * (A1 + A2 * p2 + p6 * (A3 + A4 * p2))
    return x, y


def _land_rings():
    import json
    topo = json.loads(LAND.read_text())
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    def ring(idx):
        out = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(a if not out else a[1:])
        return out
    rings = []
    for geom in topo["objects"]["land"]["geometries"]:
        polys = geom["arcs"] if geom["type"] == "MultiPolygon" else [geom["arcs"]]
        for poly_ in polys:
            for r in poly_:
                rings.append(ring(r))
    return rings


class WorldMap:
    def __init__(self, x0, y0, width, lat_min=-58, lat_max=84):
        self.x0, self.y0 = x0, y0
        xmax, _ = _equal_earth(180, 0)
        self.k = width / (2 * xmax)
        self.ytop = _equal_earth(0, lat_max)[1]

    def p(self, lon, lat):
        x, y = _equal_earth(lon, lat)
        return self.x0 + (x + _equal_earth(180, 0)[0]) * self.k, self.y0 + (self.ytop - y) * self.k

    def land(self, fill="#e3e7ec", stroke="#cfd5dc"):
        d = []
        for r in _land_rings():
            if all(lat < -58 for _, lat in r):
                continue   # Antarctica: off the map
            # split where a ring crosses the 180th meridian; each piece is closed along it
            pieces, cur = [], [r[0]]
            for a, b in zip(r, r[1:]):
                if abs(a[0] - b[0]) > 180:
                    pieces.append(cur)
                    cur = []
                cur.append(b)
            pieces.append(cur)
            if len(pieces) > 1 and abs(pieces[-1][-1][0] - pieces[0][0][0]) < 180:
                pieces[0] = pieces.pop() + pieces[0]
            for pc in pieces:
                if len(pc) < 3:
                    continue
                pts = [self.p(lon, max(lat, -58)) for lon, lat in pc]
                d.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z")
        return (f'<path d="{" ".join(d)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round" '
                f'transform="translate(0,6)" opacity="0.55"/>'
                f'<path d="{" ".join(d)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>')


def pin(x, y, kind, gid):
    """A clay dot: ARM (amber), GPU (violet), both (split)."""
    ARM_C, GPU_C = "#e8a33c", "#8e6cc9"
    o = [contact_shadow(x, y + 13, 16, 5, f"{gid}-s", 0.25)]
    if kind == "both":
        o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{GPU_C}" stroke="#ffffff" stroke-width="3"/>')
        o.append(f'<path d="M{x},{y - 13} A13,13 0 0 0 {x},{y + 13} Z" fill="{ARM_C}"/>')
        o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="#ffffff" stroke-width="3"/>')
    else:
        o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{ARM_C if kind == "arm" else GPU_C}" stroke="#ffffff" stroke-width="3"/>')
    o.append(f'<circle cx="{x - 4}" cy="{y - 4}" r="4" fill="#ffffff" opacity="0.55"/>')
    return "".join(o)


# (label, lon, lat, kind, dx, dy, anchor). TOP500 June 2026 ranks; WLCG ARM sites from
# Glasgow (WLCG sustainability workshop, Dec 2024) and GridKa (KIT publication). See the notes.
PINS = [
    ("LineShine #1", 114.1, 22.5, "arm", 40, 60, "start"),
    ("El Capitan", -121.7, 37.7, "gpu", -36, 50, "end"),
    ("Frontier", -84.3, 35.9, "gpu", 30, 52, "start"),
    (None, -88.0, 41.7, "gpu", 0, 0, "start"),            # Aurora
    ("JUPITER", 6.4, 50.9, "both", 110, 2, "start"),
    ("Fugaku", 135.2, 34.7, "arm", 46, 40, "start"),
    ("Alps", 9.0, 46.0, "both", 80, 50, "start"),
    ("LUMI", 27.7, 64.2, "gpu", 44, -6, "start"),
    (None, 11.3, 44.5, "gpu", 0, 0, "start"),             # Leonardo
    (None, -2.6, 51.5, "both", 0, 0, "start"),            # Isambard-AI
    (None, 2.1, 41.4, "gpu", 0, 0, "start"),              # MareNostrum 5
    ("Shaheen III", 39.1, 22.3, "both", -30, 56, "end"),
    (None, 139.9, 35.9, "both", 0, 0, "start"),           # Miyabi-G
    ("Setonix", 115.9, -32.0, "gpu", -40, 30, "end"),
    ("Santos Dumont", -43.2, -22.5, "both", 40, 34, "start"),
    ("AIRAWAT", 73.9, 18.5, "gpu", -20, 64, "end"),
    ("Glasgow (WLCG)", -4.3, 55.9, "arm", -46, -40, "end"),
    ("GridKa (WLCG)", 8.4, 49.1, "arm", -150, 70, "end"),
]


def landscape_map() -> str:
    W, H = 1600, 760
    o = [head(W, H)]
    m = WorldMap(30, 20, 1540)
    o.append(m.land())
    for i, (label, lon, lat, kind, dx, dy, anchor) in enumerate(PINS):
        x, y = m.p(lon, lat)
        o.append(pin(x, y, kind, f"pin{i}"))
        if label:
            o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + dx * 0.8:.1f}" y2="{y + dy * 0.8:.1f}" stroke="#9aa3ae" stroke-width="2"/>')
            o.append(text(x + dx, y + dy + 8, label, SMALL - 6, "bold", anchor=anchor, fill=TEXT_1))
    # legend
    lx, ly = 60, H - 60
    for j, (kind, lab) in enumerate([("arm", "ARM"), ("gpu", "GPU"), ("both", "ARM and GPU")]):
        o.append(pin(lx + j * 200, ly, kind, f"lg{j}"))
        o.append(text(lx + j * 200 + 26, ly + 9, lab, SMALL - 4, anchor="start", fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


FIGS = {"fig-landscape": landscape, "fig-pullpush": pullpush, "fig-slot": slot, "fig-parcels": parcels, "fig-backends": backends, "fig-parcels-only": parcels_only, "fig-backends3d": backends3d, "fig-worldmap": landscape_map}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    figs = {k: v for k, v in FIGS.items() if not sys.argv[1:] or k in sys.argv[1:]}
    for name, fn in figs.items():
        (OUT / f"{name}.svg").write_text(fn())
    print("wrote " + ", ".join(figs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
