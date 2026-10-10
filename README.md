# DUW12 slides

Slides for the 12th DIRAC(X) Users' Workshop (FZU Prague, 13–16 October 2026).

| Folder | Talk | PDF |
|---|---|---|
| `directions/` | DiracX developments: directions (Tue 10:00) | `directions/DiracXDirections_DUW12.pdf` |
| `wms/` | Workload Management (Wed 12:10) | `wms/WMS_DUW12.pdf` |
| `ts-hackathon/` | Building together: the DiracX Transformation System (hackathon) | `ts-hackathon/TSHackathon_DUW12.pdf` |

All three use the same Slidev template. [Pixi](https://pixi.sh) provides Node.js and Python;
npm workspaces give the three decks one `node_modules`.

```bash
pixi run install               # npm ci, once
pixi run browser               # Chromium for the PDF export, once
pixi run dev directions        # live preview of a deck (directions, wms or ts-hackathon)
pixi run present directions    # presenter view with the speaker notes (local only)
pixi run export directions     # regenerate slides.md, then the PDF
```

Each deck keeps its source with speaker notes in `slides.private.md`, which is git-ignored; `slides.md`
is generated from it without the notes (`pixi run notes <deck>`). Edit the private file, then
regenerate before committing. Data derived from the private planning board (`figures/data/`) and the
login-to-community mapping are not committed either; see each deck's README.

Figures: `pixi run python <deck>/figures/<script>.py` (the directions charts also need the CSVs in
`directions/figures/data/`).
