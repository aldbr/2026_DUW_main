#!/usr/bin/env python3
"""Unplanned work by stack since the start of Scrum.

    ~/Documents/dirac-scrum-metrics/.pixi/envs/default/bin/python unplanned.py
"""
import os, sys, pathlib, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("DSM_PROJECT_ROOT", str(pathlib.Path.home() / "Documents/dirac-scrum-metrics"))
sys.path.insert(0, str(pathlib.Path.home() / "Documents/dirac-scrum-metrics/src"))
import pandas as pd
from dirac_scrum_metrics import metrics as M
OUT = pathlib.Path(__file__).parent / "data"
SCRUM = pd.Timestamp("2026-01-21", tz="UTC"); END = pd.Timestamp("2026-09-05", tz="UTC")
d = M.load(warn_missing=False)
LEG = {"DIRAC", "WebAppDIRAC", "DIRACOS2", "Pilot"}
stk = lambda r: "DIRAC" if r.split("/")[-1] in LEG else "DiracX"
P = M.prepare_pulls(d); P = P[~P.is_bot & P.merged & (P.merged_at >= SCRUM) & (P.merged_at < END)].copy()
P["stack"] = P.repo.map(stk)
P["no_issue"] = P.n_linked_issues.fillna(0).eq(0)
g = P.groupby("stack").agg(merged=("number", "size"), no_linked_issue=("no_issue", "mean"), fix_shaped=("is_fix", "mean"), median_lines=("churn", "median"))
print(g.round(2))
it = d["items"]; it = it[it.is_done & (it.done_at >= SCRUM)].copy(); it["stack"] = it.repo.map(stk)
b = it.groupby("stack").agg(done=("number", "size"), unplanned=("unplanned", "mean"), points=("points", "sum"))
print(b.round(2))
# unplanned points = points of done items not tagged with the sprint they finished in
pts = it[it.points.notna()].groupby(["stack", "unplanned"]).points.sum().unstack(fill_value=0); print(pts)
g.to_csv(OUT / "7_unplanned_prs_by_stack.csv"); b.to_csv(OUT / "7b_unplanned_items_by_stack.csv")
P["q"] = P.merged_at.dt.tz_localize(None).dt.to_period("M").astype(str)
m = P.pivot_table(index="q", columns="stack", values="number", aggfunc="size", fill_value=0); print(m)
