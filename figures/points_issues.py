#!/usr/bin/env python3
"""Story points and issues opened by community.

    ~/Documents/dirac-scrum-metrics/.pixi/envs/default/bin/python points_issues.py

Story points sit on board issues. Owner of a done item = its assignees, else the authors of its merged linked PRs.
"""
import os, sys, pathlib, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("DSM_PROJECT_ROOT", str(pathlib.Path.home() / "Documents/dirac-scrum-metrics"))
sys.path.insert(0, str(pathlib.Path.home() / "Documents/dirac-scrum-metrics/src"))
import re, numpy as np, pandas as pd
from dirac_scrum_metrics import metrics as M
import community_groups as G   # reuses the mapping (and prints its tables, ignore)

OUT = pathlib.Path(__file__).parent / "data"
grp = G.grp
d = M.load(warn_missing=False)
pulls = M.prepare_pulls(d, dedupe=False)
pulls = pulls[pulls.merged]
key = {f"{r.repo}#{r.number}": r.author for r in pulls.itertuples()}
SCRUM = pd.Timestamp("2026-01-21", tz="UTC")
it = d["items"]
done = it[it.is_done & (it.done_at >= SCRUM) & it.points.notna()].copy()
pts, how = {}, {"assignee": 0, "linked PR": 0, "nobody": 0}
for r in done.itertuples():
    who = [x for x in str(r.assignees).split(";") if x and x != "nan"]
    src = "assignee"
    if not who and str(r.item_type).upper().startswith("PULL"):
        who, src = [r.author], "pull request author"
    if not who:
        who = sorted({key.get(k.strip()) for k in str(r.linked_prs).split(";") if key.get(k.strip())})
        src = "linked PR"
    if not who:
        how["nobody"] += 1; continue
    how[src] = how.get(src, 0) + 1
    for x in who:
        pts[grp(x)] = pts.get(grp(x), 0) + r.points / len(who)
tab = pd.Series(pts).round(0).sort_values(ascending=False)
tab.to_csv(OUT / "2g_story_points_by_community.csv", header=["story points"])
print("pointed done items since 21 Jan:", len(done), how); print(tab)
tot = sum(pts.values()); print("share outside core five:", round(100 * (1 - pts.get("LHCb core", 0) / tot), 1), "%")

# issues opened per quarter by community, humans only
iss = pd.read_parquet(pathlib.Path.home() / "Documents/dirac-scrum-metrics/data/flow/flow_issues.parquet")
iss = iss[~iss.author.fillna("").str.contains(M.BOT_PATTERN, case=False, regex=True)]
iss = iss[(iss.created_at >= "2025-01-01") & (iss.created_at < "2026-09-03")].copy()
iss["g"] = iss.author.map(grp)
iss["q"] = iss.created_at.dt.tz_localize(None).dt.to_period("Q").astype(str)
t = iss.pivot_table(index="q", columns="g", values="number", aggfunc="size", fill_value=0)
t["total"] = t.sum(axis=1); t["outside core five %"] = (100 * (1 - t.get("LHCb core", 0) / t.total)).round(0)
t.to_csv(OUT / "2h_issues_opened_by_community_quarter.csv"); print(t.to_string())

# which stack do the pointed items belong to, and how are they attributed?
done["stack"] = done.repo.map(lambda r: "DIRAC" if r.split("/")[-1] in ("DIRAC","WebAppDIRAC","DIRACOS2","Pilot") else "DiracX")
print(done.groupby(["stack", "item_type"]).size())
