#!/usr/bin/env python3
"""Build the report maps, one SVG per section: an isometric scene in modelling clay.

    python3 build_maps.py     # writes six maps into ../deck/public/figures/svg/

Variants: title (everything in colour), infra, dirac, grid, core (that section in
colour, the rest in cool greys). Text is always dark. Logos are embedded as PNG data URIs,
greyscaled when their section is not highlighted. Transparent background.

The look: one rounded silhouette per object with the faces clipped to it, matte per-face
gradients, a highlight spot on each top face, rim light along the top edges, and a soft
contact shadow underneath. Everything 3D shares one isometric frame (x right-down, y
left-down, z up).

The maps are written straight into the deck, at the size the deck uses. There is no second
copy to keep in step.
"""
from __future__ import annotations

import base64
import io
import itertools
import math
import pathlib

from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).parent
# Logos: the copy in this repository, so a fresh clone can regenerate the
# figures. Falls back to a personal folder if that is where you keep them.
LOGOS = HERE / "logos"
if not LOGOS.is_dir():
    LOGOS = pathlib.Path.home() / "Pictures" / "Logos"
CA, SA = math.cos(math.radians(30)), math.sin(math.radians(30))
FONT = "Lato, 'Noto Sans', 'Liberation Sans', Helvetica, Arial, sans-serif"
_gid = itertools.count()  # unique gradient ids

# Where the maps go: the deck serves its assets out of public/, so they are written there
# rather than copied. The drawing occupies x 40..1166, y 118..695 of a 1280x720 canvas, so
# the viewBox is cropped to it with a 10-unit margin; otherwise a quarter of every slide
# would be empty.
OUT = HERE.parent / "deck" / "public" / "figures" / "svg"
VIEWBOX = 'viewBox="30 108 1146 597" width="1146" height="597"' 

# ----------------------------------------------------------------------------- palette
TEXT_1, TEXT_2 = "#1f2937", "#6b7280"
ARROW, ARROW_LIGHT = "#4b5563", "#9ca3af"
CARD_EDGE, CARD_WELL = "#e5e7eb", "#f3f4f6"
GREY_FACE, GREY_SLAB = "#e6e9ee", "#eaedf1"

ACCENT = {
    "infra": "#93c0ea",   # CERN IT slab, soft blue
    "grid": "#f3cf7e",    # resource slabs, amber
    "server": "#e1e7f0",  # worker-node faces when the grid is shown
    "legacy": "#adc3e3",  # LHCbDIRAC crates
    "diracx": "#84cdc3",  # the two crates already on DiracX
}
# The applications, each tinted with the colour its job type carries in the job-type
# plot, so a name here and a band there are the same thing. Boole and Moore share a
# colour because they share a job type: MCReconstruction runs both, in the same job.
# Keep in step with JOBTYPE_COLOURS in scripts/plot_grid_usage.py.
APP_COLOUR = {
    "Gauss": "#4e8fd9",    # MCSimulation
    "Boole": "#6a4c93",    # MCReconstruction
    "Moore": "#6a4c93",    # MCReconstruction
    "DaVinci": "#e8911c",  # WGProduction
}
# The coloured crates riding on the worker nodes are those same applications, running.
# They take the same colours, so a cube here, a name in the caption and a band in the
# job-type plot are all one thing. Three colours, not four: Boole and Moore share one
# because they share a job type, and cycling four over a three-crate cluster would put
# two purples side by side and drop the orange.
CORE = list(dict.fromkeys(APP_COLOUR.values()))
# The framework the applications are built on, drawn as a thin slab under each of them.
# Gaudi and LHCb are one layer in the picture because they are one layer in the stack.
FRAMEWORK = "#2154ac"


def accent(key):
    return ACCENT[key]


def core_palette():
    return CORE


def grey_face():
    return GREY_FACE


def grey_slab():
    return GREY_SLAB


def shade(col: str, f: float) -> str:
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)
    if f >= 0:
        r, g, b = (round(c + (255 - c) * f) for c in (r, g, b))
    else:
        r, g, b = (round(c * (1 + f)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


# ----------------------------------------------------------------------------- primitives
class Iso:
    def __init__(self, ox: float, oy: float, scale: float = 1.0):
        self.ox, self.oy, self.k = ox, oy, scale

    def p(self, x, y, z=0.0):
        return (self.ox + (x - y) * CA * self.k, self.oy + (x + y) * SA * self.k - z * self.k)


def poly(pts, fill, stroke, sw=0.6):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def soft_poly(pts, fill, r):
    """Polygon with a thick same-colour round-joined stroke: a puffy, rounded silhouette."""
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{fill}" stroke-width="{r}" stroke-linejoin="round" stroke-linecap="round"/>'


def rim(pts, color, r, opacity=0.55):
    """Rim light along the top edges of a face (open polyline, round caps)."""
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{r}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'


def rounded_path(pts, r):
    """Closed path through pts with each corner rounded by radius r (quadratic corners)."""
    n = len(pts)
    def towards(a, b, dist):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        k = min(dist, L / 2) / L
        return (a[0] + dx * k, a[1] + dy * k)
    segs = []
    for i in range(n):
        A, V, B = pts[i - 1], pts[i], pts[(i + 1) % n]
        p1, p2 = towards(V, A, r), towards(V, B, r)
        segs.append((p1, V, p2))
    d = f"M{segs[0][2][0]:.1f},{segs[0][2][1]:.1f}"
    for i in range(1, n + 1):
        p1, V, p2 = segs[i % n]
        d += f" L{p1[0]:.1f},{p1[1]:.1f} Q{V[0]:.1f},{V[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + " Z"


def contact_shadow(cx, cy, rx, ry, gid, strength=0.22):
    return (f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="#0f172a" stop-opacity="{strength}"/>'
            f'<stop offset="0.6" stop-color="#0f172a" stop-opacity="{strength * 0.35:.3f}"/><stop offset="1" stop-color="#0f172a" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{gid})"/>')


def cube(iso: Iso, x, y, w, d, h, base, z0=0.0, stripe=None, slots=False, r=None):
    """A box: rounded silhouette, matte per-face gradients, highlight, rim light, shadow."""
    P = lambda X, Y, Z: iso.p(X, Y, Z + z0)
    k = iso.k
    r = r if r is not None else max(2.5, min(w, d, h) * k * 0.16)
    n = next(_gid)
    top = [P(x, y, h), P(x + w, y, h), P(x + w, y + d, h), P(x, y + d, h)]
    left = [P(x, y + d, 0), P(x + w, y + d, 0), P(x + w, y + d, h), P(x, y + d, h)]
    right = [P(x + w, y, 0), P(x + w, y + d, 0), P(x + w, y + d, h), P(x + w, y, h)]
    out = []
    # contact shadow on the ground
    gx, gy = P(x + w / 2, y + d / 2, 0)
    out.append(contact_shadow(gx + 2, gy + 2 * k, (w + d) * CA * k * 0.55, (w + d) * SA * k * 0.55, f"cs{n}", 0.20))
    out.append(f'<defs>'
               f'<linearGradient id="ct{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(base, 0.62)}"/><stop offset="1" stop-color="{shade(base, 0.28)}"/></linearGradient>'
               f'<linearGradient id="cl{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(base, 0.06)}"/><stop offset="1" stop-color="{shade(base, -0.20)}"/></linearGradient>'
               f'<linearGradient id="cr{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(base, -0.12)}"/><stop offset="1" stop-color="{shade(base, -0.36)}"/></linearGradient>'
               f'</defs>')
    # one rounded silhouette for the whole box; the faces are clipped to it
    outline = [P(x, y, h), P(x + w, y, h), P(x + w, y, 0), P(x + w, y + d, 0), P(x, y + d, 0), P(x, y + d, h)]
    out.append(f'<defs><clipPath id="cp{n}"><path d="{rounded_path(outline, r)}"/></clipPath></defs>')
    out.append(f'<g clip-path="url(#cp{n})">')
    out += [poly(left, f"url(#cl{n})", "none", 0), poly(right, f"url(#cr{n})", "none", 0), poly(top, f"url(#ct{n})", "none", 0)]
    # rim light along the top edges and the front vertical edge, and a soft highlight spot
    out.append(rim([top[3], top[0], top[1]], shade(base, 0.85), r * 0.7, 0.75))
    out.append(rim([top[1], top[2], top[3]], shade(base, 0.80), r * 0.5, 0.45))
    out.append(rim([top[2], P(x + w, y + d, 0)], shade(base, 0.55), r * 0.35, 0.35))
    tx = sum(q[0] for q in top) / 4
    ty = sum(q[1] for q in top) / 4
    out.append(f'<defs><radialGradient id="hl{n}"><stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>'
               f'<ellipse cx="{tx - w * CA * k * 0.15:.1f}" cy="{ty - (w + d) * SA * k * 0.12:.1f}" rx="{(w + d) * CA * k * 0.30:.1f}" ry="{(w + d) * SA * k * 0.28:.1f}" fill="url(#hl{n})"/>')
    if slots:
        for cz in (h * 0.36, h * 0.62):
            y0, y1, hh = y + d * 0.24, y + d * 0.76, h * 0.07
            out.append(soft_poly([P(x + w, y0, cz - hh), P(x + w, y1, cz - hh), P(x + w, y1, cz + hh), P(x + w, y0, cz + hh)], "#7c879a", r * 0.5))
    if stripe:
        a, b = 0.40, 0.60
        out.append(poly([P(x + w * a, y, h), P(x + w * b, y, h), P(x + w * b, y + d, h), P(x + w * a, y + d, h)], stripe, "none", 0))
        out.append(poly([P(x + w * a, y + d, 0), P(x + w * b, y + d, 0), P(x + w * b, y + d, h), P(x + w * a, y + d, h)], shade(stripe, -0.12), "none", 0))
    out.append("</g>")
    return "".join(out)


def slab(iso: Iso, x, y, w, d, t, base, gid):
    """An isometric platform. The clay look wants a chunkier edge than the flat one did,
    hence the +8: every call site was written against the thinner slab."""
    t = t + 8
    P = iso.p
    n = next(_gid)
    r = 14
    top = [P(x, y, 0), P(x + w, y, 0), P(x + w, y + d, 0), P(x, y + d, 0)]
    left = [P(x, y + d, -t), P(x + w, y + d, -t), P(x + w, y + d, 0), P(x, y + d, 0)]
    right = [P(x + w, y, -t), P(x + w, y + d, -t), P(x + w, y + d, 0), P(x + w, y, 0)]
    xs, ys = [q[0] for q in top], [q[1] for q in top]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2 + t + 10
    rx, ry = (max(xs) - min(xs)) / 2 * 1.06, (max(ys) - min(ys)) / 2 * 1.35
    out = [contact_shadow(cx, cy, rx, ry, f"{gid}-sh", 0.20)]
    out.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(base, 0.60)}"/><stop offset="1" stop-color="{shade(base, 0.22)}"/></linearGradient>'
               f'<linearGradient id="{gid}-l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(base, 0.02)}"/><stop offset="1" stop-color="{shade(base, -0.22)}"/></linearGradient>'
               f'<linearGradient id="{gid}-r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(base, -0.14)}"/><stop offset="1" stop-color="{shade(base, -0.38)}"/></linearGradient></defs>')
    outline = [P(x, y, 0), P(x + w, y, 0), P(x + w, y, -t), P(x + w, y + d, -t), P(x, y + d, -t), P(x, y + d, 0)]
    out.append(f'<defs><clipPath id="cp{n}"><path d="{rounded_path(outline, r)}"/></clipPath></defs>')
    out.append(f'<g clip-path="url(#cp{n})">')
    out += [poly(left, f"url(#{gid}-l)", "none", 0), poly(right, f"url(#{gid}-r)", "none", 0), poly(top, f"url(#{gid})", "none", 0)]
    out.append(rim([top[3], top[0], top[1]], shade(base, 0.85), r * 0.5, 0.65))
    out.append(rim([top[1], top[2], top[3]], shade(base, 0.80), r * 0.35, 0.45))
    out.append(rim([top[2], P(x + w, y + d, -t)], shade(base, 0.55), r * 0.25, 0.35))
    out.append("</g>")
    return "".join(out)


def text(x, y, s, size=12, weight="normal", anchor="middle", italic=False, fill=TEXT_1, rotate=None):
    st = ' font-style="italic"' if italic else ""
    tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}"{st} '
            f'text-anchor="{anchor}" fill="{fill}"{tr}>{s}</text>')


def arrow(d, dashed=False, sw=1.6, light=False):
    color = ARROW_LIGHT if light else ARROW
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    m = "arr-light" if light else "arr"
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{dash} marker-end="url(#{m})"/>'


def iso_arrow(iso: Iso, a, b, **kw):
    (x1, y1), (x2, y2) = iso.p(*a), iso.p(*b)
    return arrow(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", **kw)


_img_cache: dict = {}


def img(name: str, x, y, w, grey: bool, opacity=1.0, shadow=False):
    key = (name, grey)
    if key not in _img_cache:
        im = Image.open(LOGOS / name).convert("RGBA")
        if im.width > 300:
            im = im.resize((300, round(im.height * 300 / im.width)), Image.LANCZOS)
        if grey:
            g = ImageOps.grayscale(im.convert("RGB"))
            im = Image.merge("RGBA", (g, g, g, im.split()[3]))
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        _img_cache[key] = (base64.b64encode(buf.getvalue()).decode(), im.width / im.height)
    b64, ar = _img_cache[key]
    h = w / ar
    uri = f"data:image/png;base64,{b64}"
    fil = ' filter="url(#logo-sh)"' if shadow else ""
    return (f'<image x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h:.1f}" href="{uri}" xlink:href="{uri}" '
            f'opacity="{opacity}"{fil} preserveAspectRatio="xMidYMid meet"/>')


def img_fit(name: str, cx, cy, box_w, box_h, grey: bool, opacity=1.0):
    """Logo centred in a box, keeping its aspect ratio."""
    im = Image.open(LOGOS / name)
    ar = im.width / im.height
    w = min(box_w, box_h * ar)
    h = w / ar
    return img(name, cx - w / 2, cy - h / 2, w, grey, opacity)


def blob(cx, cy, rx, ry, base, gid, highlight=True):
    """A clay ellipse: matte vertical gradient, highlight spot, contact shadow.
    From presentations/lhcbweek/figures/build_slides.py."""
    out = [contact_shadow(cx, cy + ry * 0.95, rx * 1.05, ry * 0.34, f"{gid}-cs", 0.18)]
    out.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0.3" y2="1">'
               f'<stop offset="0" stop-color="{shade(base, 0.55)}"/>'
               f'<stop offset="1" stop-color="{shade(base, -0.16)}"/></linearGradient></defs>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{gid})"/>')
    if highlight:
        out.append(f'<defs><radialGradient id="{gid}-hl">'
                   f'<stop offset="0" stop-color="#ffffff" stop-opacity="0.6"/>'
                   f'<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>'
                   f'<ellipse cx="{cx - rx * 0.28:.1f}" cy="{cy - ry * 0.38:.1f}" '
                   f'rx="{rx * 0.46:.1f}" ry="{ry * 0.36:.1f}" fill="url(#{gid}-hl)"/>')
    return "".join(out)


def person(cx, cy, s, base, gid):
    """A clay person: head, shoulders, no face. s is the head radius, cy the head centre;
    the feet are at about cy + 3.5 s. From presentations/lhcbweek/figures/build_slides.py."""
    out = [blob(cx, cy + s * 2.35, s * 1.55, s * 1.15, base, f"{gid}-b")]
    # shoulders drawn as a rounded slab so the silhouette reads as a torso
    out.append(f'<defs><linearGradient id="{gid}-t" x1="0" y1="0" x2="0.3" y2="1">'
               f'<stop offset="0" stop-color="{shade(base, 0.5)}"/>'
               f'<stop offset="1" stop-color="{shade(base, -0.18)}"/></linearGradient></defs>')
    out.append(f'<rect x="{cx - s * 1.5:.1f}" y="{cy + s * 1.35:.1f}" width="{s * 3:.1f}" '
               f'height="{s * 1.6:.1f}" rx="{s * 0.8:.1f}" fill="url(#{gid}-t)"/>')
    out.append(blob(cx, cy, s, s, base, f"{gid}-h"))
    return "".join(out)


def card(x, y, w, h, fill="#ffffff", edge=CARD_EDGE):
    n = next(_gid)
    return (contact_shadow(x + w / 2, y + h + 4, w * 0.52, 14, f"cd{n}", 0.18)
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'
            + f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{w - 3}" height="{h - 3}" rx="16.5" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.9"/>')


def detector(iso: Iso, colour: bool) -> str:
    """Miniature LHCb spectrometer: sub-detectors growing along the beam line."""
    if colour:
        velo, rich, magnet, tracker, calo, muon = "#3d6fa8", "#9dbbe0", "#c0504d", "#3d6fa8", "#f2b134", "#7cb342"
    else:
        velo = rich = magnet = tracker = calo = muon = "#d3d8df"
    parts = []
    (x1, y1), (x2, y2) = iso.p(-6, 16, 16), iso.p(104, 16, 16)
    parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{TEXT_2}" stroke-width="0.7" stroke-dasharray="2 2"/>')
    items = [
        (0, 6, 10, 10, velo, False), (9, 6, 14, 14, rich, False), (18, 14, 26, 26, magnet, True),
        (35, 2, 26, 26, tracker, False), (39, 2, 26, 26, tracker, False), (43, 2, 26, 26, tracker, False),
        (49, 8, 28, 28, rich, False), (60, 9, 30, 30, calo, False),
        (73, 2, 32, 32, muon, False), (79, 2, 32, 32, muon, False), (85, 2, 32, 32, muon, False), (91, 2, 32, 32, muon, False),
    ]
    for x, w, d, h, col, slots in items:
        parts.append(cube(iso, x, 16 - d / 2, w, d, h, col, slots=slots))
    return "".join(parts)


# ----------------------------------------------------------------------------- scene
def build(variant: str) -> str:
    on = lambda sec: variant in ("title", sec)
    parts: list[str] = []
    A = parts.append
    W = Iso(600, 250)

    A('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
      f'{VIEWBOX}>')
    A('<defs>'
      f'<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
      f'<path d="M1,1 L9,5 L1,9 z" fill="{ARROW}"/></marker>'
      f'<marker id="arr-light" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
      f'<path d="M1,1 L9,5 L1,9 z" fill="{ARROW_LIGHT}"/></marker>'
      # The WLCG wordmark is white, and the platforms it sits over are near-white,
      # so on its own it disappears. This gives it an edge. The maps ship as PNG,
      # rendered once at build time, so the filter is resolved before any viewer
      # sees it.
      '<filter id="logo-sh" x="-25%" y="-25%" width="150%" height="160%">'
      '<feDropShadow dx="0" dy="1.1" stdDeviation="1.7" flood-color="#0f172a" flood-opacity="0.66"/>'
      '</filter>'
      '</defs>')

    srv = accent("server") if on("grid") else grey_face()
    core_cols = core_palette() if variant == "title" else ["#dfe3e8"] * 3
    fw_col = FRAMEWORK if on("core") else GREY_FACE
    well_rx = 16

    def cluster(cells, crates):
        its = []
        for (x, y) in cells:
            its.append(((x + y, 0), cube(W, x, y, 40, 40, 34, srv, slots=True)))
        for k, (x, y) in enumerate(crates):
            c = core_cols[k % len(core_cols)]
            # framework first, application on top of it: worker node, then Gaudi and LHCb,
            # then the application. Thin, because it is a layer and not a box.
            its.append(((x + y, 1), cube(W, x + 8, y + 8, 24, 24, 4, fw_col, z0=34)))
            its.append(((x + y, 2), cube(W, x + 11, y + 11, 18, 18, 16, c, z0=38, stripe=shade(c, 0.5))))
        for _, svg in sorted(its, key=lambda t: t[0]):
            A(svg)

    # --- 1. LHCb Online platform with the HLT farm (behind, up-right) -------------------
    A(slab(W, 80, -220, 180, 140, 14, accent("grid") if on("grid") else grey_slab(), "g-hlt"))
    cluster([(124, -196), (170, -196), (124, -150), (170, -150)], [(124, -196), (170, -150)])
    hx, hy = W.p(260, -220, 0)
    A(text(hx + 16, hy - 10, "HLT farm", 14, "bold", anchor="start"))
    A(text(hx + 16, hy + 9, "LHCb Online, Point 8", 12, anchor="start", fill=TEXT_2))
    A(text(hx + 16, hy + 26, "simulation between fills", 12, anchor="start", fill=TEXT_2))

    # --- 2. CERN IT platform with LHCbDIRAC (centre) -----------------------------------
    A(slab(W, 0, 0, 300, 200, 14, accent("infra") if on("infra") else grey_slab(), "g-cern"))
    if on("dirac"):
        crate_cols = [accent("legacy"), accent("diracx"), accent("diracx"), accent("legacy")]
    else:
        crate_cols = [grey_face()] * 4
    its = []
    for k, (x, y) in enumerate([(96, 48), (156, 48), (96, 108), (156, 108)]):
        its.append((x + y, cube(W, x, y, 52, 52, 46, crate_cols[k], stripe=shade(crate_cols[k], 0.5))))
    for _, svg in sorted(its, key=lambda t: t[0]):
        A(svg)
    lx, ly = W.p(100, 30, 100)
    A(img("lhcb.png", lx - 70, ly - 24, 140, grey=not on("dirac"), opacity=1.0 if on("dirac") else 0.8))
    cx, cy = W.p(300, 200, 0)
    A(text(cx - 80, cy + 44, "CERN IT", 14, "bold"))
    A(text(cx - 80, cy + 62, "accounts · SSO · mail · VPN · lxplus", 12, fill=TEXT_2))
    A(text(cx - 80, cy + 80, "CVMFS · EOS · Kubernetes for LHCbDiracX", 12, fill=TEXT_2))

    # --- 3. WLCG platform (front-right) --------------------------------------------------
    A(slab(W, 380, 20, 240, 160, 14, accent("grid") if on("grid") else grey_slab(), "g-wlcg"))
    cluster([(430, 60), (476, 60), (522, 60), (430, 106), (476, 106), (522, 106)], [(430, 60), (522, 60), (476, 106)])
    wx, wy = W.p(500, 20, 150)
    A(img("WLCG-logo.png", wx - 60, wy - 16, 120, grey=not on("grid"),
          opacity=1.0 if on("grid") else 0.8, shadow=True))
    A(text(wx, wy + 34, "WLCG sites: Tier 0, Tier 1, Tier 2", 12, "bold"))
    A(text(wx, wy + 51, "&amp; other opportunistic resources", 12, fill=TEXT_2))

    # --- 4. flows along the isometric axes -----------------------------------------------
    A(iso_arrow(W, (232, 100, 0), (372, 100, 0)))
    mx, my = W.p(300, 100, 34)
    A(text(mx, my, "pilots and jobs", 11.5, italic=True, fill=TEXT_2, rotate=30))
    A(iso_arrow(W, (216, 40, 0), (216, -74, 0)))
    mx, my = W.p(216, -16, 34)
    A(text(mx, my, "pilots and jobs", 11.5, italic=True, fill=TEXT_2, rotate=-30))

    # --- 5. sources of work: cards, left column -----------------------------------------
    tiles = [
        (118, "Analysis Productions", "lbAPI", "AP.png"),
        (236, "Simulation requests", "lbmcsubmit", "gitlab.png"),
        (354, "Data taking", "HLT2 output, sprucing", "detector"),
        (472, "User jobs", "Ganga", "ganga-mark.png" if (LOGOS / "ganga-mark.png").exists() else None),
    ]
    ex, ey = W.p(96, 134, 23)
    for k, (ty, title, sub, logo) in enumerate(tiles):
        A(card(40, ty, 286, 78))
        A(f'<rect x="52" y="{ty + 15}" width="56" height="48" rx="{well_rx}" fill="{CARD_WELL}"/>')
        if logo == "detector":
            A(detector(Iso(56, ty + 41, 0.5), colour=on("dirac")))
        elif logo:
            A(img_fit(logo, 80, ty + 39, 44, 36, grey=not on("dirac"), opacity=1.0 if on("dirac") else 0.85))
        else:
            A(text(80, ty + 45, "&gt;_", 15, "bold", fill=TEXT_1))
        A(text(124, ty + 35, title, 13, "bold", anchor="start"))
        A(text(124, ty + 55, sub, 11.5, anchor="start", fill=TEXT_2))
        dy = (k - 1.5) * 9  # spread the arrivals over the face, no knot
        A(arrow(f"M326,{ty + 39} C 385,{ty + 39} {ex - 75:.0f},{ey + dy:.0f} {ex - 16:.0f},{ey + dy:.0f}", sw=1.4))

    # --- 6. core software caption -------------------------------------------------------
    # Anchored to the CERN IT slab like the caption above it, not to a hard-coded 560,
    # which is why it used to sit off the grid. It is here because the applications are
    # what actually runs inside the jobs on both farms - the one part of the picture that
    # is software rather than a machine.
    # Coloured only on the overview, where the applications are the subject. They are NOT
    # the subject of the core software section: that is the framework underneath them, so
    # colouring them on that divider pointed the audience at the wrong layer.
    names = " ".join(
        f'<tspan fill="{c if variant == "title" else TEXT_1}">{n}</tspan>'
        + ("" if n == "DaVinci" else f'<tspan fill="{TEXT_2}"> ·</tspan>')
        for n, c in APP_COLOUR.items()
    )
    A(text(cx - 80, cy + 110, names, 13, "bold"))
    A(text(cx - 80, cy + 128, "the LHCb software inside every job", 11.5, italic=True, fill=TEXT_2))
    # ...and the layer they are all built on, which is what the core software section is
    # actually about. LHCb calls exactly these two the framework projects; Lbcom, Rec and
    # Phys are components and the rest are applications. Highlighted only on that divider,
    # where it is the subject -- without it that map named no part of its own section.
    fw = "#2154ac" if on("core") else TEXT_1          # the deck blue, so it reads as the subject
    A(text(cx - 80, cy + 152,
           f'<tspan fill="{fw}">Gaudi · LHCb</tspan>'
           f'<tspan fill="{TEXT_2}"> — the framework under all four</tspan>', 12.5, "bold"))
    # The four tiles above send work to Computing but are not part of it: they belong to
    # Simulation, DPA, RTA and Online, and to users. Ring them on the overview so the
    # boundary is explicit, not on the section maps where it would only add clutter.
    if variant == "title":
        A(f'<rect x="34" y="112" width="298" height="450" rx="18" fill="none" '
          f'stroke="{TEXT_2}" stroke-width="1.6" stroke-dasharray="7 6" opacity="0.55"/>')
        A(text(183, 583, "outside Computing — they send it work", 12.5, italic=True, fill=TEXT_2))

    # The DQCS shift card used to sit here. Computing is leaving that shift, so it is no
    # longer part of the system these maps draw; the shift keeps its slide, without a map.

    A("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for v in ["title", "infra", "dirac", "grid", "core"]:
        out = OUT / f"map-{v}.svg"
        out.write_text(build(v))
        print(out)
