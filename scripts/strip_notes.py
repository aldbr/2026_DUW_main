#!/usr/bin/env python3
"""Write the public slides.md from slides.private.md: speaker notes (HTML comments) removed.

    python3 scripts/strip_notes.py

slides.private.md is git-ignored and keeps the notes for presenting (`npm run present`).
"""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "slides.private.md").read_text()
out = re.sub(r"\n*<!--.*?-->\n*", "\n\n", src, flags=re.S)
out = re.sub(r"\n{3,}", "\n\n", out).rstrip() + "\n"
(root / "slides.md").write_text(out)
print("slides.md written without notes:", len(src.splitlines()), "->", len(out.splitlines()), "lines")
