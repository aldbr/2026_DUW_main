# Workload Management: DIRAC v9 and the way to DiracX — DUW 12 (Prague, 13–16 Oct 2026)

20-minute Slidev deck, same template as the `duw12-talk` branch ("DiracX developments: directions").

```bash
npm install
npm run dev
npx slidev export --per-slide   # PDF
```

- `slides.private.md`: the source, with speaker notes (sources and caveats for every number). Git-ignored.
- `slides.md`: generated without the notes by `npm run strip-notes`. Edit the private file, then regenerate.
- `figures/wms_figures.py`: rebuilds every figure into `public/figures/`
  (`uv run --with cairosvg --with pillow python3 figures/wms_figures.py`).
  Primitives in `figures/claylib.py` and `figures/build_figures.py` are shared with the directions deck.
