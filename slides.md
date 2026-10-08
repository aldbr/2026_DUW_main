---
theme: default
title: "DiracX developments: directions"
info: |
  ## DiracX developments: directions — DIRAC(X) Users' Workshop 12
  Alexandre F. Boyer (CERN).
  13–16 October 2026, FZU Prague. 20 minutes.
colorSchema: light
class: text-left
transition: slide-left
mdc: true
fonts:
  sans: 'IBM Plex Sans'
  serif: 'Playfair Display'
  mono: 'IBM Plex Mono'
  weights: '400,500,600,700,800'
  italic: true
---

# DiracX developments: directions

<span class="dx-author">Alexandre F. Boyer</span> · CERN

12th DIRAC(X) Users' Workshop · FZU Prague · 13–16 October 2026

<div class="dx-logobar mt-10">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC — The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX — The Interware" />
</div>

---
layout: section
---

# 1 · Where we are now

DIRAC and DiracX today

---

<div class="duw-sec">1 · Where we are now</div>

# Maintaining DIRAC, progressing on DiracX

<img :src="'/figures/fig-galaxies.svg'" alt="DIRAC and DiracX, each surrounded by its companion projects; components move from DIRAC to DiracX over the same databases" style="width:54%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.1rem">

<div>

**DIRAC** v9.1.21 · v9.0.27 · v8.0.85<br/>
WebAppDIRAC 6.0.6 · DIRACOS2 2.63<br/>
**Patched, not developed**: security fixes, and performance fixes when needed.

</div>

<div>

**DiracX** v0.6.0: foundations, authentication, jobs (search, status), sandboxes, read-only resource status, and experimental observability (OpenTelemetry).<br/>
The web app (diracx-web 0.1.0-a11) and the `dirac` CLI are still experimental.

</div>

</div>

<div class="dx-key mt-1"><b>Adopt what already exists in DiracX.</b> DIRAC is only patched, so that DiracX can progress. LHCb runs one service and one task in production; two other installations are certifying DiracX.</div>

---
layout: section
---

# 2 · Evolving requirements, fruitful collaboration

New communities, new use cases, and two systems running side by side

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# What DIRAC is for, and what it values

<div class="dx-key">Running large-scale workflows of embarrassingly parallel jobs on heterogeneous, distributed computing and storage resources: high-throughput computing.</div>

<div class="duw-three3 mt-3">

<div class="dx-card dx-card-blue">

### Minimal dependencies
A database and a search index, on a few hosts.

**In DiracX:** standard protocols for what is external (S3, OpenTelemetry, OIDC), and options without Kubernetes.

</div>

<div class="dx-card dx-card-blue">

### Multi-VO installations
One installation serves several communities.

**In DiracX:** multi-VO from the start.

</div>

<div class="dx-card dx-card-blue">

### Extendable
Communities add their own pieces.

**In DiracX:** extensions, with a reference extension.

</div>

</div>

<div class="duw-small mt-2">My own reading of what communities have asked for over the last few years.</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# Requirements keep evolving

<div class="duw-three3">

<div class="dx-card dx-card-blue">

### New communities
**CMS and FCC**, who joined this summer, bring new requirements. CMS has no DIRAC installation and runs its own workload management.

</div>

<div class="dx-card dx-card-new">

### Advanced needs, in extensions
**CTAO, LHCb, Belle II and JUNO** built extensions for advanced needs that are now close to each other. They belong in the common project: CTAO's use of **CWL** turned out useful for DiracX as a whole.

</div>

<div class="dx-card dx-card-legacy">

### Constant needs
**GridPP** has few resources: DiracX must stay very simple to deploy, with minimal dependencies.

</div>

</div>

<div class="dx-key mt-3">Share your needs early, at DOps, before building around the system: someone else may need the same thing.</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# What stays stable, what is new

<div class="duw-two dx-tight mt-2">

<div class="dx-card dx-card-legacy">

### Stable

- **DIRAC keeps running**, with security and performance patches.
- Components move **one at a time**, over the same databases.
- **Extensions keep working** while components move.

</div>

<div class="dx-card dx-card-new">

### New

- **The transformation system**: a new data model, new logic, and a much richer scope than DIRAC's.
- **Decoupled from DIRAC**, so DIRAC's databases need no large changes and stay stable.
- **Standard protocols** (sandboxes in S3, observability in OpenTelemetry) and multi-VO from the start.

</div>

</div>

<div class="dx-key mt-3">A stable path for what exists, and room for what is new.</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# Many part-time hands

<img :src="'/figures/fig-collab.svg'" alt="Groups of contributors linked by dashed two-way arrows around the question: how do we work best together?" style="width:66%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **36 people** contributed since the last workshop, most of them at **20 to 30 %** of their time: about **4 to 5 full-time equivalents**.
- They maintain DIRAC and develop DiracX at the same time.

</div>

<div class="dx-key mt-2"><b>Finding the best way to work with each other is paramount.</b></div>

---
layout: section
---

# 3 · Adapting quickly

Responding to changing requirements, in small steps

---

<div class="duw-sec">3 · Adapting quickly</div>

# The journey so far

<img :src="'/figures/fig-journey.svg'" alt="Timeline of DiracX milestones from July 2023 to July 2026, with proofs of concept running in parallel: web app, pilot security, matchmaking, interCEde, analytics and observability" style="width:84%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **From 2023, three to four hackathons a year** onboarded new contributors, with no dashboard or regular meeting to follow progress. **Scrum** brought both in 2026.
- **Proofs of concept run in parallel**, not mandatory: we try an idea before committing to it.

</div>

---

<div class="duw-sec">3 · Adapting quickly</div>

# Almost the current process

<img :src="'/figures/fig-pipeline.svg'" alt="One round from requirement to delivered package, nine steps" style="width:56%;margin:0 auto;display:block" />

<div class="dx-tight mt-2">

- **Scrum since 21 January 2026**: two-week sprints; planning and refinement in one weekly meeting; a monthly meeting with the representatives (DOps); hackathons.
- **Large changes start with a proof of concept, then an ADR** that the other developers approve. ADRs and roadmap are public; the board is not.
- **We are moving towards this process; it is not there yet.** Like the roadmap, it adapts as we learn.

</div>

---

<div class="duw-sec">3 · Adapting quickly</div>

# Not a port: a reimplementation

<div class="duw-three3">

<div class="dx-card dx-card-blue">

### A new data model
**The spine**: workgraph, transformations, parcels. New requirements need new tables and new logic. The RMS is used as it is, as a backend.

<img :src="'/figures/fig-mini-model.svg'" alt="The DiracX transformation system uses DIRAC's WMS, with new tables of its own" style="width:100%;margin-top:.4rem" />

</div>

<div class="dx-card dx-card-legacy">

### Future clients
**DMS**: a DIRAC client calls DiracX instead of DIRAC, over the same databases. **RSS**: the read side first, through an adapter.

<img :src="'/figures/fig-mini-future.svg'" alt="A DIRAC client calls either the DIRAC service or the DiracX service; both use the same databases" style="width:100%;margin-top:.4rem" />

</div>

<div class="dx-card dx-card-new">

### Standard protocols
**Systems internal to DIRAC give way to standards**: monitoring to OpenTelemetry, accounting to analytics. Details later.

<img :src="'/figures/fig-mini-protocols.svg'" alt="Monitoring becomes OpenTelemetry and accounting becomes analytics" style="width:100%;margin-top:.4rem" />

</div>

</div>

---
layout: section
---

# 4 · Results so far

Numbers since the last workshop

---

<div class="duw-sec">4 · Results so far</div>

# Activity since the last workshop

<table class="duw-stat">
<thead><tr><th>17 Sep 2025 – 4 Sep 2026</th><th>DIRAC stack</th><th>DiracX stack</th><th>Both</th></tr></thead>
<tbody>
<tr><td>Merged pull requests</td><td><b>367</b></td><td><b>261</b></td><td>634</td></tr>
<tr><td>People who merged one</td><td>20</td><td>28</td><td>36</td></tr>
<tr><td>People who gave a first review</td><td>12</td><td>11</td><td>17</td></tr>
<tr><td>New contributors</td><td>9</td><td>14</td><td>17</td></tr>
<tr><td>Issues opened</td><td>89</td><td>206</td><td>296</td></tr>
<tr><td>Issues closed (completed / not planned)</td><td>117 (76 / 41)</td><td>224 (191 / 33)</td><td>343 (268 / 75)</td></tr>
</tbody></table>

<div class="duw-small mt-2">DIRAC stack: DIRAC, WebAppDIRAC, DIRACOS2, Pilot. DiracX stack: diracx, diracx-charts, diracx-web, signurlarity, dirac-cwl, interCEde. Bots excluded; copies of one change on several release branches counted once. Issues to 2 Sep.</div>

---

<div class="duw-sec">4 · Results so far</div>

# Since Scrum: the backlog is shrinking

<div class="duw-stats3">
<div><b>295 → 195</b>open issues, January 2026 to September</div>
<div><b>10.6 → 36.6</b>closures a month; 26.6 completed, 10.0 not planned or duplicate</div>
<div><b>16.3 → 27.3</b>issues opened a month</div>
</div>

<img :src="'/figures/fig-burnup.svg'" alt="Cumulative issues in the DIRACGrid repositories since January 2024: open issues rose from 156 to 295 before January 2026 and fell to 195 by September" style="width:66%;margin:0 auto;display:block" />

<div class="duw-small" style="text-align:center">All issues in the DIRACGrid repositories, bots excluded. Part of the fall is triage.</div>

---

<div class="duw-sec">4 · Results so far</div>

# Velocity

<div class="grid grid-cols-12 gap-5">

<div class="col-span-7">

<img :src="'/figures/fig-velocity.svg'" alt="Story points per person and sprint, expected against delivered, for sprints 1 to 23: expected is about twice what is delivered in almost every sprint" style="width:100%" />

</div>

<div class="col-span-5 dx-tight">

- **We expect about twice what we deliver**: a median of 13 story points per person and sprint expected, 5.3 delivered.
- Delivered velocity follows availability: workshops, conferences, holidays.
- Only one sprint delivered what was expected.

</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# Where an issue goes

<img :src="'/figures/fig-flow.svg'" alt="Issues on the board: 121 in Needs triage, 13 in Needs design, 34 in Backlog, 34 in In progress, 317 Done. Those who left a column stayed 3, 27, 7 and 3 days; those still there have waited 227, 190, 50 and 67 days" style="width:100%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **Issues that move on do so quickly. The ones still waiting have waited far longer.**
- **121 issues sit in triage**, most since the January board sweep. 34 are "in progress" with a median of two months.

</div>

---

<div class="duw-sec">4 · Results so far</div>

# Unplanned work lives in DIRAC

<div class="grid grid-cols-12 gap-5">

<div class="col-span-6">

<img :src="'/figures/fig-unplanned.svg'" alt="Since January 2026, 56% of story points delivered on DIRAC were unplanned against 11% on DiracX, and 84% of merged pull requests on DIRAC have no linked issue against 49% on DiracX" style="width:100%" />

</div>

<div class="col-span-6 dx-tight">

- Since January, **56% of the story points delivered on DIRAC were unplanned**, against 11% on DiracX.
- **84% of DIRAC pull requests have no linked issue**, against 49% on DiracX.
- Security and performance work arrives when it arrives. It is the cost of keeping DIRAC running, and why DIRAC only gets patches.

<div class="dx-card dx-card-blue mt-2" style="height:auto;padding:.5em .8em"><b>For developers:</b> we overestimate what a sprint can hold because we do not count the unplanned DIRAC maintenance. Plan for it.</div>

</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# More hands, from more communities

<img :src="'/figures/fig-communities.svg'" alt="Merged pull requests a month from January 2025 to August 2026, stacked by community: LHCb core, other LHCb, CMS, CTAO, IN2P3, GridPP, EGI, FCC, IHEP, Belle II, not attributed" style="width:62%;margin:0 auto;display:block" />

<div class="duw-three dx-tight" style="margin-top:.2rem">

<div>

**36 people** merged a change since the last workshop; **17 were new**, from ten communities. Almost all are part-time, so effort varies from month to month.

</div>

<div>

Outside the five core developers: **36% of merged PRs, 28% of issues opened, 53% of story points.**

</div>

<div>

Read with care: about half of the 2026 rise in PRs is **one GridPP developer** hardening DIRAC's SQL. CMS merged 14 changes since July.

</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# The bottleneck is review

<div class="grid grid-cols-12 gap-5">

<div class="col-span-6">

<img :src="'/figures/fig-review.svg'" alt="Share of first reviews given by the top reviewer and the top two reviewers each quarter, rising from 62% in 2025 Q1 to 75% in 2026 Q3" style="width:100%" />

<div class="dx-ref mt-1">Share of first reviews, by quarter</div>

</div>

<div class="col-span-6 dx-tight">

- **Two people give three quarters of first reviews.** The top reviewer alone went from a third to over half.
- **None of the 14 contributors new since January has given a first review yet.**
- **Design review is not in these numbers.** ADRs are reviewed by everyone, in meetings and on chat.

<div class="dx-concludes"><carbon-arrow-right class="dx-concludes-arrow" /><span>writing code has spread; <strong>reading it has not</strong></span></div>

<div class="dx-card dx-card-blue mt-2" style="height:auto;padding:.5em .8em"><b>Question for developers:</b> kanban style, should you review before starting something new once your tasks are done?</div>

</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# Smaller pull requests get reviewed sooner

<div class="grid grid-cols-12 gap-5">

<div class="col-span-6">

<img :src="'/figures/fig-review-size.svg'" alt="Median hours to first review rises from 2.6 hours for pull requests under 10 lines to 23 hours for 500 lines or more, on a log scale, with the middle half of the pull requests shown as a bar" style="width:100%" />

<div class="dx-ref mt-1">Median wait for a first review, with the middle half of the pull requests</div>

</div>

<div class="col-span-6 dx-tight">

- **Under 10 lines: 2.6 hours. 500 lines or more: 23 hours.** Time to merge goes from a few hours to five days.
- **The spread is wide at every size**, so size helps but does not decide.
- **Who writes it matters too.** For pull requests under 50 lines, the five core developers wait 2.5 hours; everyone else waits 11.

<div class="dx-concludes"><carbon-arrow-right class="dx-concludes-arrow" /><span>split the work, and <strong>announce a big change early</strong></span></div>

<div class="mt-2"><a href="https://diracx.diracgrid.org/en/latest/dev/explanations/splitting-prs/" target="_blank" class="dx-ref">How to split a large change into stacked pull requests: DiracX contributing guide</a></div>

</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# Where work waits

<img :src="'/figures/fig-pipe.svg'" alt="Work flows through specification, development and review; development was widened by Scrum, specification and review remain the narrow parts" style="width:92%;margin:0 auto;display:block" />

<div class="dx-tight mt-2">

- **Scrum widened development**: more contributors, a shrinking backlog.
- **Specification and review are the narrow parts**, and they will matter more with every new component.

<div class="dx-card dx-card-blue mt-2" style="height:auto;padding:.5em .8em"><b>For everyone in the room:</b> representatives, developers and users, where would you improve how we work?</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# Cheaper code: easier to explore, same bottlenecks

<div class="grid grid-cols-5 gap-6">

<div class="col-span-2">

<div class="duw-quote">"AI does not resolve ambiguity. It amplifies it."</div>
<div class="duw-small mt-1">Nir Yechiel, <a href="https://nyechiel.com/blog/2026/07/02/the-bottleneck-moved/">The bottleneck moved</a>, July 2026</div>

<div class="dx-tight mt-3">

- Writing code got cheap, so **spikes and proofs of concept** are easier to try: matchmaking, interCEde, analytics, observability.
- **Deciding what to build and checking it** did not get cheaper.
- It does **not change our process**. It shows its weak points sooner.

</div>

</div>

<div class="col-span-3 dx-tight">

**Each one is something we just saw**

- **Vague specification** → verbose, AI-generated issues that go stale (an open action). A clear ADR with a scenario test is what an agent, or a newcomer, can implement.
- **Review bottleneck** → more code means more to read, by the same two people.
- **Unplanned work** → faster code does not shrink urgent maintenance.
- **A new kind of user** → DiracX speaks HTTP and OAuth2, so an agent can use it through MCP.

<div class="dx-concludes"><carbon-arrow-right class="dx-concludes-arrow" /><span>invest in <strong>specifications, tests and review</strong>, not in typing</span></div>

</div>

</div>

---
layout: section
---

# 5 · What’s next

How we could improve, and the roadmap

---

<div class="duw-sec">5 · What’s next</div>

# Next: building the transformation system

<div class="dx-key" style="font-size:1.1em"><b>Implementation starts at the hackathon this afternoon.</b> The technical details are in the next talk.</div>

<div class="duw-two dx-tight mt-3">

<div>

**Where it comes from**

- **Use cases from the communities**: CMS, CTAO, FCC, Belle II and LHCb.
- **A design that comes from a proof of concept**, written down as ADRs.

</div>

<div>

**How it will be delivered**

- **Increments the representatives can test**, shown at DOps whenever a sprint delivers one.
- **The more we are, and the better organised, the sooner.**

</div>

</div>

<div class="dx-card dx-card-blue mt-3" style="height:auto;padding:.5em .9em"><b>This afternoon, two hackathons:</b> adapting your community's workflows to <b>CWL</b>, and building the <b>transformation system</b>.</div>

---

<div class="duw-sec">5 · What’s next</div>

# The roadmap moves with the communities

<img :src="'/figures/fig-roadmap2.svg'" alt="Long-running lines of work: Transformation System, Job Wrapper, Data Management System, Resource status; and exploratory spikes: WMS, analytics and observability, MCP server, clients" style="width:84%;margin:0 auto;display:block" />

<div class="dx-oneline mt-2">Priorities, not commitments. New requirements can reorder this page, and the team writes the detailed plan.</div>

---

<div class="duw-sec">5 · What’s next</div>

# If you run an installation today

<div class="dx-card dx-card-new" style="height:auto">

### What you can count on

- **DIRAC keeps running**, with security patches and performance fixes when needed.
- **You choose when to switch each component**, usually at a shutdown.
- **No data migration** for anything but the transformation system, which has its own tables.
- **Your extension keeps working** on DIRAC while you move.
- **DIRAC and DiracX live in parallel**, and work can move gradually from one to the other.
- **Increments to test**, shown at DOps whenever a sprint delivers one.

</div>

---
layout: default
---

<div class="duw-sec">Take-aways</div>

# Take-aways

<div class="grid grid-cols-1 gap-4 mt-3 text-lg">

<div>
<div class="dx-eyebrow">For installations</div>
<div class="dx-tight">

- **Adopt what exists; DIRAC is only patched.** You move one component at a time, and the transformation system runs in parallel.

</div>
</div>

<div>
<div class="dx-eyebrow">For representatives and developers</div>
<div class="dx-tight">

- **Specification and review are the bottlenecks.** Increments you can test, shown at DOps, keep us close to your needs.

</div>
</div>

<div>
<div class="dx-eyebrow">For this afternoon</div>
<div class="dx-tight">

- **Join one of the two hackathons**: adapting your workflows to CWL, or building the transformation system.

</div>
</div>

</div>

---
layout: cover
---

# Thank you

<div class="duw-contact">Questions and comments welcome, this week and after.</div>

<div class="duw-contact"><b>Alexandre F. Boyer</b> · alexandre.boyer@cern.ch</div>

<div class="duw-contact">github.com/DIRACGrid · diracx.diracgrid.org</div>

<div class="dx-logobar mt-8">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC — The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX — The Interware" />
</div>
