#!/usr/bin/env python3
"""Merged human PRs a month by community, from dirac-scrum-metrics data.

    ~/Documents/dirac-scrum-metrics/.pixi/envs/default/bin/python community_groups.py

Affiliations come from figures/affiliations_private.py (not published). Anyone not listed stays unattributed.
"""
import os, sys, pathlib, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("DSM_PROJECT_ROOT", str(pathlib.Path.home() / "Documents/dirac-scrum-metrics"))
import pandas as pd
sys.path.insert(0, str(pathlib.Path.home() / "Documents/dirac-scrum-metrics/src"))
from dirac_scrum_metrics import metrics as M

OUT = pathlib.Path(__file__).parent / "data"
END_PR = pd.Timestamp("2026-09-05", tz="UTC")
W0 = pd.Timestamp("2025-09-17", tz="UTC")
try:
    from affiliations_private import GROUPS, BULK_CONTRIBUTOR  # git-ignored; see README
except ImportError:
    raise SystemExit("figures/affiliations_private.py is missing (it is not published): define GROUPS = {community: 'login login ...'} and BULK_CONTRIBUTOR")
LOOKUP = {a.lower(): g for g, s in GROUPS.items() for a in s.split()}
grp = lambda a: LOOKUP.get(str(a).lower(), "not attributed")

d = M.load(warn_missing=False)
P = M.prepare_pulls(d)
P = P[~P.is_bot & P.merged & (P.merged_at < END_PR)].copy()
P["group"] = P.author.map(grp)
P["month"] = P.merged_at.dt.tz_localize(None).dt.to_period("M").astype(str)
m = P[P.merged_at >= "2025-01-01"].pivot_table(index="month", columns="group", values="number", aggfunc="size", fill_value=0)
order = list(GROUPS) + ["not attributed"]
m = m.reindex(columns=order, fill_value=0)
m["total"] = m.sum(axis=1)
m.to_csv(OUT / "2_monthly_merged_by_community.csv")
W = P[P.merged_at >= W0]
a = W.groupby("group").author.nunique().reindex(order, fill_value=0)
a.to_csv(OUT / "2c_distinct_authors_by_community_since_W0.csv")
print(m.to_string()); print(a); print("authors since W0:", W.author.nunique())
un = W[W.group == "not attributed"].groupby("author").size().sort_values(ascending=False)
un.head(15).to_csv(OUT / "2d_remaining_unattributed.csv"); print(un.head(15))

# share of merged changes written outside a given definition of "LHCb"
rows = []
for name, lo, hi in (("2025", "2025-01-01", "2026-01-01"), ("since 21 Jan 2026", "2026-01-21", "2026-09-05"), ("since 20 Jun 2026", "2026-06-20", "2026-09-05")):
    s = P[(P.merged_at >= pd.Timestamp(lo, tz="UTC")) & (P.merged_at < pd.Timestamp(hi, tz="UTC"))]
    core = s.group.eq("LHCb core"); lhcb = s.group.isin(["LHCb core", "other LHCb"])
    gp = lhcb | s.author.str.lower().eq(BULK_CONTRIBUTOR)
    rows.append((name, len(s), round(100 * (1 - core.mean()), 1), round(100 * (1 - lhcb.mean()), 1), round(100 * (1 - gp.mean()), 1)))
sh = pd.DataFrame(rows, columns=["window", "n", "outside core 5 %", "outside all LHCb %", "also without the bulk contributor %"])
sh.to_csv(OUT / "2e_outside_share_definitions.csv", index=False); print(sh)

# ---- other ways to count a community's contribution, since the last workshop
SCRUM = pd.Timestamp("2026-01-21", tz="UTC")
iss = pd.read_parquet(pathlib.Path.home() / "Documents/dirac-scrum-metrics/data/flow/flow_issues.parquet")
iss = iss[~iss.author.fillna("").str.contains(M.BOT_PATTERN, case=False, regex=True)]
iss = iss[iss.created_at >= W0]
iss["group"] = iss.author.map(grp)
it = d["items"]
it = it[it.is_done & (it.done_at >= SCRUM) & it.points.notna() & it.assignees.notna()].copy()
pts = {}
for _, r in it.iterrows():
    who = [x for x in str(r.assignees).split(";") if x]
    for x in who:
        pts[grp(x)] = pts.get(grp(x), 0) + r.points / len(who)
W = P[P.merged_at >= W0]
tab = pd.DataFrame({
    "merged PRs": W.groupby("group").size(),
    "lines changed (k)": (W.groupby("group").churn.sum() / 1000).round(1),
    "median PR lines": W.groupby("group").churn.median(),
    "people": W.groupby("group").author.nunique(),
    "first reviews given": W[W.first_reviewer.notna() & ~W.first_reviewer.fillna("").str.contains(M.BOT_PATTERN, case=False, regex=True)].assign(g=lambda x: x.first_reviewer.map(grp)).groupby("g").size(),
    "issues opened": iss.groupby("group").size(),
    "story points (since Jan, assigned)": pd.Series(pts).round(0),
}).reindex(order).fillna(0)
tab.to_csv(OUT / "2f_contribution_metrics_by_community.csv"); print(tab.to_string())
tot_done = d["items"][d["items"].is_done & (d["items"].done_at >= SCRUM)]
print("done items since Jan:", len(tot_done), "with points:", tot_done.points.notna().sum(), "with points and assignee:", (tot_done.points.notna() & tot_done.assignees.notna()).sum())
