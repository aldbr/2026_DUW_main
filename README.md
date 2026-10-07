# DiracX developments: directions — DUW 12 (Prague, 13–16 Oct 2026)

20-minute Slidev deck, same template as `../chep26`.

```bash
npm install        # node_modules here are hardlinked from ../chep26
npm run dev
npm run export     # PDF; --per-slide is safer: npx slidev export --per-slide
```

- `slides.md` — 16 slides, speaker notes carry sources and caveats
- `public/figures/` — copied from the CHEP26 proceedings (`fig-pipeline`, `fig-burnup`, `fig-roadmap`); numbers match the paper, which supersedes the lhcbweek slides
- `styles/duw.css` — additions to the CHEP26 theme

## Figures and data

`figures/*.py` rebuild every figure into `public/figures/`. They read CSVs under `figures/data/`, which are derived from the private DIRACGrid planning board and are therefore **not committed**: regenerate them with the scripts in `~/Documents/dirac-scrum-metrics` (`community_groups.py`, `process_checks.py`, `points_issues.py`, `unplanned.py`) or ask the author.

The speaker notes in `slides.md` carry the sources and caveats for every number.

## Speaker notes

The notes live in `slides.private.md`, which is **not published** (git-ignored). `slides.md` is generated from it without the notes:

```bash
npm run strip-notes   # slides.private.md -> slides.md, notes removed
npm run present       # presenter view with the notes (local only)
```

Edit `slides.private.md`, then regenerate `slides.md` before committing. The login-to-community mapping used by the community chart is also private (`figures/affiliations_private.py`).
