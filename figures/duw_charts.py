#!/usr/bin/env python3
"""Charts for the DUW12 talk, from figures/data (copied from the stats run of 6 Oct 2026).

    ~/Documents/dirac-scrum-metrics/.pixi/envs/default/bin/python duw_charts.py

Community groups: only LHCb core, CMS and GridPP are documented. Everything else is
'not yet attributed' until someone labels the logins in data/2d_top15_unattributed_logins.csv.
"""
import pathlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams.update({"svg.fonttype": "none", "font.family": "DejaVu Sans",
                            "font.size": 12, "axes.spines.top": False, "axes.spines.right": False})
D = pathlib.Path(__file__).parent / "data"
OUT = pathlib.Path(__file__).parent.parent / "public" / "figures"
INK, MUTE = "#2b3a42", "#768b96"
COL = {"LHCb core": "#1f78c1", "other LHCb": "#8ab9e0", "CMS": "#6aa84f", "CTAO": "#8e7cc3", "IN2P3": "#c9604b",
       "GridPP": "#e0a030", "EGI": "#3a9d9d", "FCC": "#c27ba0", "IHEP": "#7a5230", "Belle II": "#2b8a3e", "not attributed": "#c3ccd2"}


def communities():
    d = pd.read_csv(D / "2_monthly_merged_by_community.csv")
    d = d[d.month < "2026-09"]  # September 2026 is four days
    fig, ax = plt.subplots(figsize=(8.6, 3.7))
    bottom = pd.Series(0, index=d.index)
    for g, c in COL.items():
        ax.bar(range(len(d)), d[g], bottom=bottom, color=c, width=0.78, label=g)
        bottom += d[g]
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels([pd.Timestamp(m + "-01").strftime("%b\n%y") if m[5:] in ("01", "07") else pd.Timestamp(m + "-01").strftime("%b") for m in d.month], color=MUTE, fontsize=10)
    ax.tick_params(axis="y", colors=MUTE); ax.tick_params(length=0)
    for s in ("left", "bottom"): ax.spines[s].set_color("#d8dee2")
    ax.yaxis.grid(True, color="#e4e8eb"); ax.set_axisbelow(True)
    k = list(d.month).index("2026-01") - 0.5 + 20 / 31
    ax.axvline(k, color=INK, ls="--", lw=1)
    ax.text(k + 0.15, ax.get_ylim()[1] * 0.97, "Scrum", color=INK, fontweight="bold", va="top")
    ax.set_ylabel("merged pull requests a month", color=MUTE)
    ax.legend(frameon=False, ncol=5, loc="upper left", bbox_to_anchor=(0, 1.27), labelcolor=INK, fontsize=9.5, columnspacing=1.0, handlelength=1.2)
    fig.tight_layout()
    fig.savefig(OUT / "fig-communities.svg", transparent=True)


def review():
    d = pd.read_csv(D / "3_review_concentration_quarterly.csv")
    q = [s.replace("20", "", 1).replace("Q", " Q") if False else s[:4] + " " + s[4:] for s in d.quarter]
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    x = range(len(d))
    ax.bar(x, d.top2_share * 100, color="#a8c8e4", width=0.62, label="top two reviewers")
    ax.bar(x, d.top1_share * 100, color="#1f78c1", width=0.62, label="top reviewer")
    for i, (a, b) in enumerate(zip(d.top1_share, d.top2_share)):
        ax.text(i, b * 100 + 1.5, f"{b*100:.0f}%", ha="center", color=INK, fontsize=10.5, fontweight="bold")
    ax.set_xticks(list(x)); ax.set_xticklabels(q, color=MUTE, fontsize=9.5)
    ax.set_ylim(0, 92); ax.set_yticks([]); ax.tick_params(length=0)
    for s in ("left", "bottom"): ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, 1.16), ncol=2, labelcolor=INK, fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "fig-review.svg", transparent=True)


def size():
    d = pd.read_csv(D / "6_review_latency_by_size.csv")
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    x = list(range(len(d)))
    ax.vlines(x, d.q25_h, d.q75_h, color="#8ab9e0", lw=9, alpha=0.9, zorder=2)
    ax.plot(x, d.median_h, "o", color="#1f78c1", ms=11, zorder=3)
    ax.plot(x, d.median_h, "-", color="#1f78c1", lw=1.6, zorder=1)
    for i, m in zip(x, d.median_h):
        ax.text(i + 0.12, m, f"{m:.0f} h" if m >= 10 else f"{m:.1f} h", color=INK, fontsize=11, fontweight="bold", va="center", ha="left")
    ax.set_yscale("log"); ax.set_ylim(0.3, 300)
    ax.set_yticks([1, 10, 100]); ax.set_yticklabels(["1 h", "10 h", "100 h"], color=MUTE)
    ax.set_xticks(x); ax.set_xticklabels([f"{b.replace(' to ', '-')}\nn={n}" for b, n in zip(d.bucket, d.n)], color=MUTE, fontsize=9.5)
    ax.set_xlim(-0.4, len(d) - 0.4)
    ax.set_xlabel("lines changed in the pull request", color=MUTE)
    ax.tick_params(length=0, which="both")
    for s in ("left", "bottom"): ax.spines[s].set_color("#d8dee2")
    ax.yaxis.grid(True, color="#e4e8eb"); ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT / "fig-review-size.svg", transparent=True)


def unplanned():
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    labels = ["Story points delivered\nthat were unplanned", "Merged pull requests\nwith no linked issue"]
    dirac, dx = [73 / 131 * 100, 84], [40 / 359 * 100, 49]
    y = [1, 0]
    ax.barh([i + 0.19 for i in y], dirac, height=0.34, color="#1f78c1", label="DIRAC")
    ax.barh([i - 0.19 for i in y], dx, height=0.34, color="#84cdc3", label="DiracX")
    for i, (a, b) in enumerate(zip(dirac, dx)):
        ax.text(a + 1.5, y[i] + 0.19, f"{a:.0f}%", va="center", color=INK, fontweight="bold", fontsize=12)
        ax.text(b + 1.5, y[i] - 0.19, f"{b:.0f}%", va="center", color=INK, fontweight="bold", fontsize=11)
    ax.set_yticks(y); ax.set_yticklabels(labels, color=INK, fontsize=11)
    ax.set_xlim(0, 100); ax.set_xticks([]); ax.tick_params(length=0)
    for s in ("left", "bottom"): ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(OUT / "fig-unplanned.svg", transparent=True)


def people():
    d = pd.read_csv(D / "8_people_per_month.csv")
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    x = range(len(d))
    ax.bar(x, d["core five"], color="#1f78c1", width=0.75, label="five core developers")
    ax.bar(x, d["others"], bottom=d["core five"], color="#84cdc3", width=0.75, label="everyone else")
    ax.set_xticks(list(x))
    ax.set_xticklabels([pd.Timestamp(m + "-01").strftime("%b\n%y") if m[5:] in ("01", "07") else pd.Timestamp(m + "-01").strftime("%b") for m in d.m], color=MUTE, fontsize=9)
    ax.tick_params(length=0); ax.tick_params(axis="y", colors=MUTE)
    for s in ("left", "bottom"): ax.spines[s].set_color("#d8dee2")
    ax.yaxis.grid(True, color="#e4e8eb"); ax.set_axisbelow(True)
    ax.set_ylabel("people merging a change", color=MUTE)
    ax.legend(frameon=False, ncol=2, loc="upper left", bbox_to_anchor=(0, 1.15), labelcolor=INK, fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "fig-people.svg", transparent=True)


def velocity():
    """The team's own velocity record: story points per person, expected against delivered."""
    v = pd.read_csv(D / "9_velocity_team_record.csv")
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    x = range(len(v))
    ax.bar([i - 0.2 for i in x], v.expected, width=0.4, color="#c9dced", label="expected")
    ax.bar([i + 0.2 for i in x], v.delivered, width=0.4, color="#1f78c1", label="delivered")
    ax.set_xticks(list(x)); ax.set_xticklabels(v.sprint, color=MUTE, fontsize=8.5)
    ax.set_xlabel("sprint", color=MUTE); ax.set_ylabel("story points per person", color=MUTE)
    ax.tick_params(length=0); ax.tick_params(axis="y", colors=MUTE)
    for s in ("left", "bottom"): ax.spines[s].set_color("#d8dee2")
    ax.yaxis.grid(True, color="#e4e8eb"); ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=2, loc="upper left", bbox_to_anchor=(0, 1.15), labelcolor=INK, fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "fig-velocity.svg", transparent=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    communities(); review(); size(); unplanned(); people(); velocity(); print("ok")
