#!/usr/bin/env python3
"""People per month and sprint velocity.

    ~/Documents/dirac-scrum-metrics/.pixi/envs/default/bin/python velocity.py
"""
import os, sys, pathlib, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("DSM_PROJECT_ROOT", str(pathlib.Path.home() / "Documents/dirac-scrum-metrics"))
sys.path.insert(0, str(pathlib.Path.home() / "Documents/dirac-scrum-metrics/src"))
import pandas as pd
from dirac_scrum_metrics import metrics as M
OUT = pathlib.Path(__file__).parent / "data"
d = M.load(warn_missing=False)
CORE = {"fstagni", "chaen", "chrisburr", "aldbr", "ryuwd"}
P = M.prepare_pulls(d); P = P[~P.is_bot & P.merged & (P.merged_at >= pd.Timestamp("2025-01-01", tz="UTC")) & (P.merged_at < pd.Timestamp("2026-09-01", tz="UTC"))].copy()
P["m"] = P.merged_at.dt.tz_localize(None).dt.to_period("M").astype(str)
P["core"] = P.author.isin(CORE)
ppl = P.groupby(["m", "core"]).author.nunique().unstack(fill_value=0).rename(columns={True: "core five", False: "others"})
ppl["total"] = ppl.sum(axis=1); ppl.to_csv(OUT / "8_people_per_month.csv"); print(ppl.to_string())
v = M.sprint_summary_adjusted(d)
print(v.columns.tolist())
v.to_csv(OUT / "8_sprint_velocity.csv", index=False)
print(v.to_string()[:3000])
