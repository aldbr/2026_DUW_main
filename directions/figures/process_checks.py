#!/usr/bin/env python3
"""Checks behind the 'Where an issue goes' and review-latency slides.

    ~/Documents/dirac-scrum-metrics/.pixi/envs/default/bin/python process_checks.py
"""
import os, sys, pathlib, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("DSM_PROJECT_ROOT", str(pathlib.Path.home() / "Documents/dirac-scrum-metrics"))
sys.path.insert(0, str(pathlib.Path.home() / "Documents/dirac-scrum-metrics/src"))
import numpy as np, pandas as pd
from dirac_scrum_metrics import metrics as M

OUT = pathlib.Path(__file__).parent / "data"
d = M.load(warn_missing=False)
tl = M.status_timeline(d)
# the timeline closes open spells at today's date; the extraction is older, so age them as of the extraction
as_of = max(d["status"]["at"].max(), d["items"]["item_updated_at"].max())
print("extraction as of", as_of)
tl.loc[tl.is_open, "days"] = (as_of - tl.loc[tl.is_open, "start"]) / pd.Timedelta(days=1)
items = d["items"].set_index("item_id")
tl = tl.join(items[["item_type", "state"]], on="item_id")
iss = tl[tl.item_type.eq("ISSUE")]
rows = []
for st in ("triage", "design", "backlog", "in_progress"):
    s = iss[iss.stage.eq(st)]
    ended = s[~s.is_open & ~s.admin].days
    ended_all = s[~s.is_open].days
    now = s[s.is_open & s.item_id.map(items.state).eq("OPEN")].days
    now_noadmin = s[s.is_open & ~s.admin & s.item_id.map(items.state).eq("OPEN")].days
    rows.append(dict(stage=st, n_ended=len(ended), median_ended_days=ended.median(), mean_ended=ended.mean(),
                     n_waiting_now=len(now), median_age_now_days=now.median(), p75_age_now=now.quantile(.75),
                     n_now_not_admin_start=len(now_noadmin), median_age_now_not_admin=now_noadmin.median(),
                     median_ended_incl_admin=ended_all.median()))
r = pd.DataFrame(rows); r.to_csv(OUT / "4e_stage_survivorship.csv", index=False)
print(r.round(1).T.to_string())

# ---- time to first review against size of the pull request
W0 = pd.Timestamp("2025-09-17", tz="UTC"); END = pd.Timestamp("2026-09-05", tz="UTC")
P = M.prepare_pulls(d)
P = P[~P.is_bot & P.merged & (P.merged_at >= W0) & (P.merged_at < END)].copy()
P = P[~P.first_reviewer.fillna("").str.contains(M.BOT_PATTERN, case=False, regex=True)]
P = P[P.hours_to_first_review.notna() & (P.hours_to_first_review >= 0)]
print("PRs with a human first review, merged since W0:", len(P))
big = P.churn.quantile(0.99); print("99th percentile of lines changed:", big)
Q = P[P.churn <= big]          # drop the largest 1% (generated files, vendored code, bulk renames)
BINS = [0, 10, 50, 200, 500, np.inf]; LAB = ["< 10", "10 to 49", "50 to 199", "200 to 499", "500 or more"]
Q["bucket"] = pd.cut(Q.churn, BINS, labels=LAB, right=False)
g = Q.groupby("bucket", observed=True).hours_to_first_review
t = pd.DataFrame({"n": g.size(), "q25_h": g.quantile(.25), "median_h": g.median(), "q75_h": g.quantile(.75), "p90_h": g.quantile(.9),
                  "median_days_to_merge": Q.groupby("bucket", observed=True).days_to_merge.median()}).round(1)
t.to_csv(OUT / "6_review_latency_by_size.csv"); print(t.to_string())
rho = Q[["churn", "hours_to_first_review"]].corr(method="spearman").iloc[0, 1]; print("spearman churn vs hours to first review:", round(rho, 3))
core = {"fstagni", "chaen", "chrisburr", "aldbr", "ryuwd"}
Q["who"] = np.where(Q.author.isin(core), "core five", "everyone else")
w = Q.groupby("who").hours_to_first_review.agg(["size", "median"]).round(1); print(w)
# like for like: small PRs only, core against the rest
S = Q[Q.churn < 50].groupby("who").hours_to_first_review.agg(["size", "median"]).round(1); print("PRs under 50 lines:\n", S)
