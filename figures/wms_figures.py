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
from claylib import CA as CA_, SA as SA_, Iso, contact_shadow, cube, shade, slab, text
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
    o.append(label_pill(40, 60, 340, 100, GREEN, "po1", "user payload", "#2d5a33", "a CWL document"))
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
    o.append(text(1180, 430, "deployment tests, dummy executor;", SMALL - 6, anchor="start", fill=TEXT_2))
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


# ----------------------------------------------------------------------------- the DIRAC WMS path, in 3D
# Components of the submission and matching path. kind: svc (cube) or db (cylinder).
# Iso coordinates: the central services platform runs along x, the site platform along y.
WMS_PARTS = {
    # central installation, grouped by who talks to whom:
    # near the user (back), near the site (front)
    "JobManager":     ("svc", 40, 40),
    "Optimizers":     ("agent", 260, 40),
    "SandboxStore":   ("svc", 480, 40),
    "JobDB":          ("db", 40, 250),
    "TaskQueueDB":    ("db", 260, 250),
    "PilotManager":   ("svc", 620, 250),
    "PilotAgentsDB":  ("db", 840, 250),
    "SiteDirector":   ("agent", 40, 470),
    "Matcher":        ("svc", 260, 470),
    "JobStateUpdate": ("svc", 480, 470),
    "Pilot logging":  ("svc", 700, 470),
    # site: the CE, and a worker node beside it
    "CE":             ("svc", 30, 760),
    "Pilot":          ("svc", 240, 760),
    "JobAgent":       ("svc", 240, 900),
    "JobWrapper":     ("svc", 240, 1040),
}
WMS_FLOW = [("user", "JobManager", "submit", 60), ("SiteDirector", "CE", "send pilots", 0),
            ("Pilot", "Matcher", "ask for a job", 0), ("JobWrapper", "JobStateUpdate", "report", 0)]


def iso_cylinder(it, x, y, d, h, base, gid):
    """A database drawn in the same isometric frame as the cubes: footprint d x d at (x, y)."""
    k = it.k
    r = d / 2
    rx, ry = 1.414 * r * CA_ * k, 1.414 * r * SA_ * k
    bx, by = it.p(x + r, y + r, 0)
    tx, ty = it.p(x + r, y + r, h)
    out = [contact_shadow(bx + 2, by + 4, rx * 1.05, ry * 1.1, f"{gid}-cs", 0.22)]
    out.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
               f'<stop offset="0" stop-color="{shade(base, 0.08)}"/><stop offset="0.45" stop-color="{shade(base, -0.06)}"/>'
               f'<stop offset="1" stop-color="{shade(base, -0.34)}"/></linearGradient></defs>')
    out.append(f'<path d="M{tx - rx:.1f},{ty:.1f} L{bx - rx:.1f},{by:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {bx + rx:.1f},{by:.1f} '
               f'L{tx + rx:.1f},{ty:.1f} Z" fill="url(#{gid})"/>')
    out.append(f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{shade(base, 0.45)}"/>')
    out.append(f'<ellipse cx="{tx - rx * 0.2:.1f}" cy="{ty - ry * 0.15:.1f}" rx="{rx * 0.5:.1f}" ry="{ry * 0.45:.1f}" fill="#ffffff" opacity="0.35"/>')
    out.append(f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{shade(base, 0.7)}" stroke-width="2" opacity="0.7"/>')
    return "".join(out)


def _halo_text(x, y, s_, size, weight, fill):
    """Text with a background-coloured halo, drawn as two layers (renderers differ on paint-order)."""
    base = (f'x="{x:.1f}" y="{y:.1f}" font-family="{cl.FONT}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="middle"')
    return (f'<text {base} fill="#f7f5ef" stroke="#f7f5ef" stroke-width="7" stroke-linejoin="round">{s_}</text>'
            f'<text {base} fill="{fill}">{s_}</text>')


def wms_path(highlight: dict, colour: str, debug: bool = False) -> str:
    """The DIRAC WMS submission and matching path as a clay scene. Components sit next to
    whom they talk to: the user side at the back, the site side at the front; four labelled
    arrows show the path. Components in `highlight` are coloured; those with a callout
    (box centre, lines) get one."""
    W, H = 1600, 900
    o = [head(W, H).replace('viewBox="0 0 1600 900" width="1600" height="900"', 'viewBox="80 0 1520 760" width="1520" height="760"')]
    it = Iso(900, 150, 0.6)
    P = it.p
    GREY, GREY_DB, GREY_AG = "#e3e6ea", "#d5dae1", "#d9dde3"
    o.append(slab(it, 0, 0, 1000, 620, 14, "#eef1f5", "wp-c"))
    o.append(slab(it, 0, 720, 380, 460, 14, "#f6efe0", "wp-s"))
    wn = [P(200, 735, 0), P(370, 735, 0), P(370, 1170, 0), P(200, 1170, 0)]
    o.append(f'<polygon points="{" ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in wn)}" fill="#efe3c6" stroke="#d9c597" stroke-width="3" stroke-dasharray="10 8"/>')
    centre, labels = {}, []
    for name, (kind, x, y) in sorted(WMS_PARTS.items(), key=lambda kv: kv[1][1] + kv[1][2]):
        on = name in highlight
        if kind == "db":
            o.append(iso_cylinder(it, x, y, 90, 60, shade(colour, -0.1) if on else GREY_DB, f"wp-{name.replace(' ', '')}"))
            top = P(x + 45, y + 45, 60)
        else:
            h = 40 if kind == "agent" else 56
            col = colour if on else (GREY_AG if kind == "agent" else GREY)
            o.append(cube(it, x, y, 90, 90, h, col, r=8))
            top = P(x + 45, y + 45, h)
        centre[name] = P(x + 45, y + 45, 30)
        labels.append(_halo_text(top[0], top[1] - 18, name, SMALL - 5, "bold" if on else "normal",
                                 TEXT_1 if on else "#98a1ac"))
    ux, uy = P(-200, -60, 0)
    o.append(cl.person(ux, uy - 60, 16, "#c9d3df", "wp-user"))
    labels.append(_halo_text(ux, uy + 16, "user", SMALL - 6, "normal", TEXT_2))
    centre["user"] = (ux + 22, uy - 30)
    for a_, b_, lab, off in WMS_FLOW:
        (x1, y1), (x2, y2) = centre[a_], centre[b_]
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        tipx, tipy = x2 - ux * 26, y2 - uy * 26
        o.append(f'<path d="M{x1 + ux * 14:.1f},{y1 + uy * 14:.1f} L{tipx - ux * 16:.1f},{tipy - uy * 16:.1f}" stroke="#7d8896" '
                 f'stroke-width="3.4" stroke-linecap="round" fill="none"/>')
        o.append(arrowhead(tipx, tipy, ux, uy, length=18, half_width=9, color="#7d8896"))
        labels.append(_halo_text((x1 + x2) / 2 - 10 + off, (y1 + y2) / 2 - 8, lab, SMALL - 6, "normal", "#5b6573"))
    o += labels
    lx, ly = P(1000, 0, 0)
    o.append(text(lx + 10, ly + 66, "DIRAC installation", SMALL - 4, "bold", fill=TEXT_2))
    lx, ly = P(380, 1180, 0)
    o.append(text(lx - 20, ly + 60, "site", SMALL - 4, "bold", anchor="end", fill=TEXT_2))
    wx, wy = P(200, 1170, 0)
    o.append(text(wx - 14, wy + 10, "worker node", SMALL - 7, italic=True, anchor="end", fill="#8a6d2c"))
    edge = shade(colour, -0.45)
    for name, spec in highlight.items():
        if not spec:
            continue
        (bx, by), lines = spec
        x, y = centre[name]
        w = max(len(l) for l in lines) * 13.5 + 36
        h = 16 + 32 * len(lines)
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{edge}" stroke-width="2.6"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{edge}"/>')
        o.append(f'<rect x="{bx - w / 2:.1f}" y="{by - h / 2:.1f}" width="{w:.1f}" height="{h}" rx="14" '
                 f'fill="#ffffff" stroke="{shade(colour, -0.25)}" stroke-width="3"/>')
        for j, l in enumerate(lines):
            o.append(text(bx, by - h / 2 + 37 + j * 32, l, SMALL - 7, "bold" if j == 0 else "normal",
                          fill=TEXT_1 if j == 0 else TEXT_2))
    if debug:
        for n, (x, y) in centre.items():
            o.append(text(x, y + 30, f"{x:.0f},{y:.0f}", 16, fill="#c00"))
    o.append("</svg>")
    return "".join(o)


def path_faster() -> str:
    return wms_path({
        "JobDB": ((420, 120), ["insertion: 115 → 190 jobs/s", "#8801 · index #8463"]),
        "TaskQueueDB": ((1360, 90), ["matching: 30 ms → 3 ms (#8462)", "323 queues: 3.4 s → 0.2 s (#8801)"]),
        "Matcher": ((700, 690), ["sub-second delay", "#8711"]),
        "PilotManager": ((1420, 300), ["fewer calls", "#8569 · #8624"]),
        "PilotAgentsDB": ((1420, 620), ["missing indices", "#8463"]),
    }, "#9fd3a8")


def path_reliable() -> str:
    return wms_path({
        "TaskQueueDB": ((1360, 90), ["keeps site, platform, tags", "#8801"]),
        "SiteDirector": ((330, 160), ["skips banned CEs", "#8340"]),
        "Pilot": ((330, 290), ["Python 3 only", "Pilot #268"]),
        "JobAgent": ((340, 700), ["leaves rescheduled jobs alone", "#8441"]),
        "JobWrapper": ((780, 715), ["no NaN parameters", "#8750"]),
    }, "#adc3e3")


def path_safer() -> str:
    return wms_path({
        "TaskQueueDB": ((1360, 90), ["parameterised SQL, all DBs", "v9.1.13 to v9.1.15"]),
        "SandboxStore": ((1400, 230), ["no writes outside", "GHSA-pwvr"]),
        "PilotManager": ((1430, 420), ["SQL injection, access", "GHSA-7xw9"]),
        "Pilot logging": ((1200, 690), ["no file reads", "GHSA-vm3r"]),
        "JobStateUpdate": ((840, 700), ["only your own jobs", "GHSA-j3xg"]),
        "Pilot": ((330, 230), ["verified HTTPS download", "GHSA-vg99"]),
        "JobDB": None, "PilotAgentsDB": None,
    }, "#f0b9a8")

def hetero() -> str:
    """One image name for every architecture (CVMFS .multiarch), CPU and memory limits with
    cgroup2, and HPC access through the SSH CE. Isometric clay."""
    W, H = 1600, 880
    o = [head(W, H)]
    it = Iso(760, 230, 0.82)
    P = it.p
    X86, ARM = "#adc3e3", "#e8a33c"
    # CVMFS, at the back
    o.append(slab(it, 0, -40, 560, 200, 14, "#eef1f5", "ht-cv"))
    stacks = {}
    for k, (x, col) in enumerate([(70, X86), (330, ARM)]):
        o.append(cube(it, x, 10, 110, 110, 30, shade(col, 0.2), r=8))
        o.append(cube(it, x, 10, 110, 110, 24, col, z0=30, r=8))
        stacks[k] = P(x + 55, 65, 54)
    tx, ty = P(280, -40, 0)
    tx = P(280, 60, 0)[0]
    o.append(text(tx, ty - 215, "CVMFS: /.multiarch/&lt;arch&gt;/&lt;image&gt;", SMALL - 2, "bold", fill=TEXT_1))
    o.append(text(tx, ty - 181, "layout built by DUCC 2.14.1", SMALL - 6, fill=TEXT_2))
    o.append(text(stacks[0][0], stacks[0][1] - 40, "amd64", SMALL - 4, "bold", fill=INK_BLUE))
    o.append(text(stacks[1][0], stacks[1][1] - 40, "arm64", SMALL - 4, "bold", fill="#7a5410"))
    # worker nodes
    nodes = [(-40, 330, X86, "x86_64 node", 0), (330, 300, ARM, "aarch64 node", 1)]
    for (x0, y0, col, name, k) in nodes:
        o.append(slab(it, x0, y0, 260, 260, 14, "#f6efe0", f"ht-n{k}"))
        o.append(cube(it, x0 + 30, y0 + 40, 70, 70, 44, "#c7cfd9", r=6))
        bx = [P(x0 + 115, y0 + 115, 0), P(x0 + 240, y0 + 115, 0), P(x0 + 240, y0 + 240, 0), P(x0 + 115, y0 + 240, 0)]
        d = " ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in bx)
        o.append(f'<polygon points="{d}" fill="#ffffff" fill-opacity="0.5" stroke="#8a6d2c" stroke-width="3" stroke-dasharray="10 8"/>')
        o.append(cube(it, x0 + 140, y0 + 140, 80, 80, 50, col, r=7))
        pl = P(x0 + 65, y0 + 75, 44)
        o.append(text(pl[0], pl[1] - 18, "pilot", SMALL - 6, "bold", fill=TEXT_1))
        c = P(x0 + 180, y0 + 180, 50)
        (sx, sy) = stacks[k]
        o.append(arrow(sx, sy + 40, c[0], c[1] - 8, -30 if k == 0 else 30, sw=4))
        lx, ly = P(x0 + 260, y0 + 260, 0)
        o.append(text(lx - 90, ly + 56, name, SUB - 4, "bold", fill=TEXT_1))
    # cgroup label, once
    cx, cy = P(330 + 240, 300 + 115, 0)
    o.append(text(cx + 20, cy + 6, "cgroup2: CPU and", SMALL - 6, anchor="start", fill="#8a6d2c"))
    o.append(text(cx + 20, cy + 36, "memory limits", SMALL - 6, anchor="start", fill="#8a6d2c"))
    o.append(text(cx + 20, cy + 66, "#8110 · #8366", SMALL - 8, anchor="start", fill=TEXT_2))
    # a batch-system node, reached over SSH
    o.append(slab(it, 760, 120, 200, 200, 14, "#e9e1f5", "ht-hpc"))
    o.append(cube(it, 810, 170, 90, 90, 56, "#c3b1e1", slots=True, r=7))
    nx, ny = P(855, 215, 56)
    o.append(text(nx, ny - 20, "HPC login node", SMALL - 6, "bold", fill=TEXT_1))
    o.append(label_pill(1300, 200, 270, 70, "#c3b1e1", "ht-ssh", "SSH CE", "#3d2a63", size=SMALL))
    o.append(arrow(1420, 276, nx + 95, ny + 40, 20, sw=4))
    o.append(text(1400, 320, "Fabric · #7703", SMALL - 6, anchor="end", fill=TEXT_2))
    hx, hy = P(960, 320, 0)
    o.append(text(hx - 60, hy + 56, "Slurm, PBS, HTCondor...", SMALL - 6, fill=TEXT_2))
    o.append(text(800, H - 20, "the pilot reads uname -m and picks the matching directory (#8456)", SMALL - 4, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def matcher_poc() -> str:
    """What the POC matcher does today for one pilot request: all waiting jobs, then match
    against the node, filter by job-type limits and priority, rank by fair share, pick one."""
    W, H = 1600, 520
    o = [head(W, H)]
    steps = [
        ("waiting jobs", ["loaded from the database", ""], 16, "#d5dbe3"),
        ("1 · match", ["site, OS, cores, memory,", "GPU, tags vs the node"], 9, "#9fd3a8"),
        ("2 · filter", ["job-type limits at the site,", "then priority (weighted)"], 5, "#f0d9a6"),
        ("3 · rank", ["fair share: group, owner,", "then oldest first"], 3, "#adc3e3"),
    ]
    for k, (title, sub, n, col) in enumerate(steps):
        cx = 170 + k * 360
        it = Iso(cx, 130, 0.5)
        o.append(slab(it, 0, 0, 280, 280, 12, "#f3f5f8", f"mp-s{k}"))
        cells = [(28 + (i % 4) * 62, 28 + (i // 4) * 62) for i in range(n)]
        for (x, y) in sorted(cells, key=lambda c: c[0] + c[1]):
            o.append(cube(it, x, y, 44, 44, 30, col, r=5))
        o.append(text(cx, 380, title, SUB - 4, "bold", fill=TEXT_1))
        o.append(text(cx, 414, sub[0], SMALL - 8, fill=TEXT_2))
        o.append(text(cx, 442, sub[1], SMALL - 8, fill=TEXT_2))
        if k < 3:
            o.append(arrow(cx + 140, 200, cx + 222, 200, 0, sw=4))
    o.append(arrow(1390, 200, 1440, 200, 0, sw=4))
    o.append(label_pill(1448, 166, 145, 68, AMBER, "mp-p", "one job", INK_AMBER, size=SMALL - 2))
    o.append(text(1520, 270, "to the pilot", SMALL - 8, fill=TEXT_2))
    o.append(label_pill(20, 20, 330, 64, AMBER, "mp-n", "pilot: node description", INK_AMBER, size=SMALL - 6))
    o.append(arrow(330, 90, 470, 150, 20, sw=3.6))
    o.append(text(800, 500, "one request at a time, in Python: every waiting job is checked", SMALL - 4, italic=True, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def intercede_flow() -> str:
    """interCEde: requirements in, then the library is checked against real CEs in integration
    tests before any release reaches DiracX."""
    W, H = 1600, 640
    o = [head(W, H)]
    # 1. the library
    it = Iso(250, 300, 0.7)
    o.append(slab(it, 0, 0, 220, 220, 14, "#fff3dd", "ic-l"))
    for z, col in [(0, "#f0d9a6"), (30, "#ecc884"), (60, "#e8b35f")]:
        o.append(cube(it, 50, 50, 120, 120, 26, col, z0=z, r=8))
    o.append(text(250, 540, "interCEde", SUB - 2, "bold", fill="#7a5410"))
    o.append(text(250, 574, "library, proof of concept", SMALL - 8, fill=TEXT_2))
    # 2. integration tests against real CEs
    it = Iso(800, 280, 0.7)
    o.append(slab(it, 0, 0, 260, 260, 14, "#eef1f5", "ic-t"))
    for k, (name, x, y) in enumerate([("HTCondor", 30, 30), ("ARC", 150, 30), ("Slurm", 90, 150)]):
        o.append(cube(it, x, y, 80, 80, 50, "#c7cfd9", slots=True, r=7))
        tx, ty = it.p(x + 40, y + 40, 50)
        o.append(text(tx, ty - 16, name, SMALL - 7, "bold", fill=TEXT_1))
    o.append(text(800, 540, "integration tests", SUB - 2, "bold", fill=TEXT_1))
    o.append(text(800, 574, "real CEs, before every release", SMALL - 8, fill=TEXT_2))
    # 3. DiracX
    it = Iso(1350, 300, 0.7)
    o.append(slab(it, 0, 0, 220, 220, 14, TEAL, "ic-x"))
    o.append(cube(it, 50, 50, 120, 120, 50, "#5fb3a8", r=8))
    o.append(text(1350, 540, "DiracX", SUB - 2, "bold", fill=INK_TEAL))
    o.append(text(1350, 574, "a WMS backend uses it", SMALL - 8, fill=TEXT_2))
    for (x1, x2, lab) in [(420, 600, "tested"), (1000, 1180, "released")]:
        o.append(arrow(x1, 400, x2, 400, 0, sw=4))
        o.append(text((x1 + x2) / 2, 386, lab, SMALL - 6, italic=True, fill=TEXT_2))
    # communities: requirements in, increments out
    for i in range(3):
        o.append(cl.person(470 + i * 60, 70, 15, ["#adc3e3", "#9fd3a8", "#f0d9a6"][i], f"ic-u{i}"))
    o.append(text(530, 160, "communities", SMALL - 4, "bold", fill=TEXT_1))
    o.append(arrow(450, 100, 250, 220, -40, sw=3.6))
    o.append(text(300, 120, "requirements:", SMALL - 7, "bold", anchor="end", fill=TEXT_1))
    o.append(text(300, 148, "issues, DOps", SMALL - 7, anchor="end", fill=TEXT_2))
    o.append(arrow(330, 250, 470, 140, 30, sw=3.6))
    o.append(text(430, 240, "increments", SMALL - 7, "bold", anchor="start", fill=TEXT_1))
    o.append(text(430, 268, "to test", SMALL - 7, anchor="start", fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)

def history() -> str:
    """Two decades on one line: HPC, clouds and industry above, the grid (WLCG) below."""
    W, H = 1600, 590
    o = [head(W, H)]
    Y = 280
    x_of = lambda yr: 110 + (yr - 2004) * (1400 / 23)
    o.append(f'<line x1="60" y1="{Y}" x2="1560" y2="{Y}" stroke="#8aa7c4" stroke-width="8" stroke-linecap="round"/>')
    o.append(arrowhead(1590, Y, 1, 0, length=34, half_width=18, color="#8aa7c4"))
    for yr in range(2005, 2027, 5):
        o.append(text(x_of(yr), Y + 44, str(yr), 22, fill="#a3acb7"))
    o.append(text(60, 40, "HPC, clouds, industry", 26, "bold", anchor="start", fill=TEXT_2))
    o.append(text(60, 560, "Grid (WLCG)", 26, "bold", anchor="start", fill="#7a5410"))
    above = [(2005, ["Clock speed stops rising:", "multicore CPUs"], "#adc3e3", 90, "start"),
             (2010, ["First GPU system at the", "top of the TOP500"], "#8e6cc9", 170, "middle"),
             (2018, ["ARM in a large", "cloud (AWS)"], "#e8a33c", 90, "end"),
             (2020, ["First ARM system at the", "top of the TOP500"], "#e8a33c", 170, "start")]
    below = [(2023, ["ARM in production at", "a grid site (Glasgow)"], "#e8a33c", 360, "end"),
             (2025, ["First ARM pledges", "in WLCG"], "#e8a33c", 440, "end"),
             (2026.6, ["GPUs cannot be", "pledged yet"], "#8e6cc9", 518, "end")]
    for i, (yr, lines, col, ty, anchor) in enumerate(above + below):
        x = x_of(yr)
        up = ty < Y
        y_end = ty + 32 * len(lines) - 14 if up else ty - 34
        o.append(f'<line x1="{x:.1f}" y1="{y_end}" x2="{x:.1f}" y2="{Y - 22 if up else Y + 22}" stroke="#c0cad4" stroke-width="3"/>')
        tx = x + {"start": -8, "end": 8, "middle": 0}[anchor]
        for j, l in enumerate(lines):
            o.append(text(tx, ty + j * 32, l, 26, "bold" if j == 0 else "normal", anchor=anchor, fill=TEXT_1))
        o.append(cl.blob(x, Y, 17, 17, col, f"hs{i}"))
    o.append("</svg>")
    return "".join(o)


def slot_before_after() -> str:
    """The end of a slot, before and after the v9.1 fixes."""
    W, H = 1600, 560
    o = [head(W, H)]
    X0, X1 = 260, 1540
    def bar(y, segs):
        for i, (a, b, col, t, ink) in enumerate(segs):
            o.append(pill(a + 4, y, b - a - 8, 80, col, f"sb{y}{i}", r=20))
            o.append(text((a + b) / 2, y + 52, t, SMALL, "bold", fill=ink))
    o.append(text(40, 132, "before", SUB - 2, "bold", anchor="start", fill="#9b4d3a"))
    bar(90, [(X0, 420, "#c7cfd9", "pilot", TEXT_1),
             (420, 1540, "#9fd3a8", "payload, sized for the whole slot", "#2d5a33")])
    o.append(f'<line x1="1500" y1="66" x2="1500" y2="196" stroke="#c0392b" stroke-width="5"/>')
    o.append(text(1490, 222, "killed: outputs lost", SMALL - 4, "bold", anchor="end", fill="#c0392b"))
    o.append(text(X0, 222, "only the Watchdog knew the margin; it could only kill", SMALL - 6, anchor="start", fill=TEXT_2))
    o.append(text(40, 372, "after", SUB - 2, "bold", anchor="start", fill="#2d5a33"))
    bar(330, [(X0, 420, "#c7cfd9", "pilot", TEXT_1),
              (420, 1060, "#9fd3a8", "payload", "#2d5a33"),
              (1060, 1260, "#fff1c9", "wind down", INK_AMBER),
              (1260, 1540, AMBER, "uploads", INK_AMBER)])
    for x, l1, l2, anc in [(420, "margin reserved", "before matching (#8746)", "middle"),
                           (1060, "stop signal sent", "StopSig*, #8814", "end"),
                           (1260, "payload exits; if killed,", "the reason is shown (#8528)", "start")]:
        o.append(f'<line x1="{x}" y1="418" x2="{x}" y2="456" stroke="#6b7280" stroke-width="3" stroke-dasharray="6 6"/>')
        dx = {"middle": 0, "end": 10, "start": -10}[anc]
        o.append(text(x + dx, 486, l1, SMALL - 6, "bold", anchor=anc, fill=TEXT_1))
        o.append(text(x + dx, 516, l2, SMALL - 8, anchor=anc, fill=TEXT_2))
    o.append("</svg>")
    return "".join(o)


def multiarch() -> str:
    """One image name for every architecture: CVMFS .multiarch, resolved by the pilot."""
    W, H = 1600, 860
    o = [head(W, H)]
    it = Iso(760, 250, 0.8)
    P = it.p
    X86, ARM = "#adc3e3", "#e8a33c"
    o.append(slab(it, 0, -40, 560, 200, 14, "#eef1f5", "ma-cv"))
    stacks = {}
    for k, (x, col) in enumerate([(70, X86), (330, ARM)]):
        o.append(cube(it, x, 10, 110, 110, 30, shade(col, 0.2), r=8))
        o.append(cube(it, x, 10, 110, 110, 24, col, z0=30, r=8))
        stacks[k] = P(x + 55, 65, 54)
    tx = P(280, 60, 0)[0]
    ty = P(280, -40, 0)[1]
    o.append(text(tx, ty - 205, "CVMFS: /.multiarch/&lt;arch&gt;/&lt;image&gt;", SMALL - 2, "bold", fill=TEXT_1))
    o.append(text(tx, ty - 171, "layout built by DUCC 2.14.1 where images are published", SMALL - 7, fill=TEXT_2))
    o.append(text(stacks[0][0], stacks[0][1] - 40, "amd64", SMALL - 4, "bold", fill=INK_BLUE))
    o.append(text(stacks[1][0], stacks[1][1] - 40, "arm64", SMALL - 4, "bold", fill="#7a5410"))
    for (x0, y0, col, name, k) in [(-60, 330, X86, "x86_64 node", 0), (340, 300, ARM, "aarch64 node", 1)]:
        o.append(slab(it, x0, y0, 260, 260, 14, "#f6efe0", f"ma-n{k}"))
        o.append(cube(it, x0 + 30, y0 + 40, 70, 70, 44, "#c7cfd9", r=6))
        o.append(cube(it, x0 + 140, y0 + 140, 80, 80, 50, col, r=7))
        pl = P(x0 + 65, y0 + 75, 44)
        o.append(text(pl[0], pl[1] - 18, "pilot: uname -m", SMALL - 7, "bold", fill=TEXT_1))
        c = P(x0 + 180, y0 + 180, 50)
        sx, sy = stacks[k]
        o.append(arrow(sx, sy + 40, c[0], c[1] - 8, -30 if k == 0 else 30, sw=4))
        lx, ly = P(x0 + 260, y0 + 260, 0)
        o.append(text(lx - 90, ly + 56, name, SUB - 4, "bold", fill=TEXT_1))
    o.append(text(1250, 420, "the job names one image;", SMALL - 4, anchor="start", fill=TEXT_1))
    o.append(text(1250, 454, "each node runs", SMALL - 4, anchor="start", fill=TEXT_1))
    o.append(text(1250, 488, "its own copy", SMALL - 4, anchor="start", fill=TEXT_1))
    o.append("</svg>")
    return "".join(o)


def limits_hpc() -> str:
    """Left: one multi-core node shared by jobs, each held to its CPU and memory share by
    cgroup2. Right: the SSH CE reaching an HPC login node and its batch system."""
    W, H = 1600, 640
    o = [head(W, H)]
    it = Iso(420, 190, 0.8)
    P = it.p
    o.append(slab(it, 0, 0, 420, 420, 14, "#f6efe0", "lh-n"))
    jobs = [(30, 30, 160, 160, "#9fd3a8", "4 cores, 8 GB"), (230, 30, 160, 160, "#adc3e3", "2 cores, 4 GB"),
            (30, 230, 160, 160, "#f0d9a6", "1 core, 6 GB"), (230, 230, 160, 160, "#e9e1f5", "free")]
    for k, (x, y, w, d, col, lab) in enumerate(jobs):
        bx = [P(x, y, 0), P(x + w, y, 0), P(x + w, y + d, 0), P(x, y + d, 0)]
        dd = " ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in bx)
        o.append(f'<polygon points="{dd}" fill="#ffffff" fill-opacity="0.55" stroke="#8a6d2c" stroke-width="3" stroke-dasharray="10 8"/>')
        if lab != "free":
            o.append(cube(it, x + 40, y + 40, 80, 80, 50, col, r=7))
            t = P(x + 80, y + 80, 50)
            o.append(text(t[0], t[1] - 18, lab, SMALL - 8, "bold", fill=TEXT_1))
        else:
            t = P(x + 80, y + 80, 0)
            o.append(text(t[0], t[1] + 8, "free", SMALL - 6, italic=True, fill=TEXT_2))
    lx, ly = P(420, 420, 0)
    o.append(text(lx - 120, ly + 56, "one multi-core slot", SUB - 4, "bold", fill=TEXT_1))
    o.append(text(lx - 120, ly + 90, "dashed: a cgroup2 limit per job", SMALL - 7, fill="#8a6d2c"))
    it2 = Iso(1250, 300, 0.8)
    o.append(slab(it2, 0, 0, 220, 220, 14, "#e9e1f5", "lh-h"))
    o.append(cube(it2, 60, 60, 100, 100, 60, "#c3b1e1", slots=True, r=7))
    t = it2.p(110, 110, 60)
    o.append(text(t[0], t[1] - 20, "HPC login node", SMALL - 6, "bold", fill=TEXT_1))
    o.append(text(1250, 560, "its batch system runs the pilots", SMALL - 7, fill=TEXT_2))
    o.append(label_pill(1120, 60, 300, 76, "#c3b1e1", "lh-ssh", "SSH CE (Fabric)", "#3d2a63", size=SMALL - 2))
    o.append(arrow(1270, 142, 1255, 300, 10, sw=4))
    o.append("</svg>")
    return "".join(o)


def pilots_paused() -> str:
    """Pilot management: ported as is, paused, then re-thought: nobody knows yet what."""
    W, H = 1600, 420
    o = [head(W, H)]
    o.append(label_pill(40, 150, 330, 110, BLUE, "pp1", "DIRAC", INK_BLUE, "pilot management", size=SUB))
    o.append(arrow(380, 205, 520, 205, 0, sw=4))
    o.append(text(450, 186, "as is", SMALL - 6, italic=True, fill=TEXT_2))
    o.append(label_pill(530, 150, 330, 110, TEAL, "pp2", "DiracX", INK_TEAL, "pilot database, router", size=SUB))
    # pause sign
    o.append(f'<rect x="935" y="165" width="22" height="80" rx="6" fill="#9aa3ae"/><rect x="975" y="165" width="22" height="80" rx="6" fill="#9aa3ae"/>')
    o.append(text(966, 300, "paused", SMALL - 4, "bold", fill=TEXT_2))
    o.append(arrow(1030, 205, 1150, 205, 0, sw=4))
    o.append(f'<rect x="1160" y="90" width="400" height="230" rx="30" fill="#fff6e4" stroke="#e0a030" stroke-width="4" stroke-dasharray="14 10"/>')
    o.append(text(1360, 230, "?", 140, "bold", fill="#e0a030"))
    o.append(text(1360, 300, "re-thought with the DiracX WMS", SMALL - 6, fill="#7a5410"))
    o.append("</svg>")
    return "".join(o)


FIGS = {"fig-slot": slot, "fig-parcels-only": parcels_only, "fig-backends3d": backends3d, "fig-worldmap": landscape_map, "fig-path-faster": path_faster, "fig-path-reliable": path_reliable, "fig-path-safer": path_safer, "fig-hetero": hetero, "fig-matcher": matcher_poc, "fig-intercede": intercede_flow, "fig-history": history, "fig-slot2": slot_before_after, "fig-multiarch": multiarch, "fig-limits-hpc": limits_hpc, "fig-pilots": pilots_paused}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    figs = {k: v for k, v in FIGS.items() if not sys.argv[1:] or k in sys.argv[1:]}
    for name, fn in figs.items():
        (OUT / f"{name}.svg").write_text(fn())
    print("wrote " + ", ".join(figs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
