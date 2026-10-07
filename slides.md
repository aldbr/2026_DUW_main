---
theme: default
title: "DiracX developments: directions"
info: |
  ## DiracX developments: directions — DIRAC(X) Users' Workshop 12
  Alexandre F. Boyer (CERN), on behalf of the DIRAC Consortium.
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

<span class="dx-author">Alexandre F. Boyer</span> · CERN, on behalf of the DIRAC Consortium

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

<img :src="'/figures/fig-galaxies.svg'" alt="DIRAC and DiracX, each surrounded by its companion projects; components move from DIRAC to DiracX over the same databases" style="width:60%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.1rem">

<div>

**DIRAC** v9.1.21 · v9.0.27 · v8.0.85 · WebAppDIRAC 6.0.6 · DIRACOS2 2.63. **Patched, not developed**: security fixes, and performance fixes when needed.

</div>

<div>

**DiracX** v0.5.0 (29 Sep): authentication, jobs (search, status, submission), sandboxes, read-only resource status, a task framework. The web app (diracx-web 0.1.0-a11) and the `dirac` CLI are still experimental.

</div>

</div>

<div class="dx-key mt-1"><b>Move to what exists today as soon as you can.</b> DIRAC only gets patches so that DiracX can progress. LHCb runs one service and one task in production; two other installations are certifying DiracX.</div>

---
layout: section
---

# 2 · Evolving requirements, fruitful collaboration

New communities, new use cases, and two systems running side by side

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# New communities, new use cases

<div class="duw-two dx-tight mt-2">

<div class="dx-card dx-card-blue">

### What we heard

- **CMS**, who joined this summer, has no DIRAC installation and runs its own workload management (HTCondor with GlideinWMS). It needs to hand work to a system we do not own, to separate taking requests from executing them, and to describe work in CWL.
- **GridPP**, contributing for a while, wants to deploy DiracX without Kubernetes, with multi-VO from the start. It is mostly interested in the WMS and the DMS.
- **CTAO, IN2P3, FCC, EGI, Belle II and IHEP** contribute too, several of them for a long time.

</div>

<div class="dx-card dx-card-new">

### DIRAC's values, in DiracX

<table class="duw-map" style="font-size:.82rem">
<tbody>
<tr><td>Few dependencies: MySQL, OpenSearch</td><td>Standard protocols: S3, OpenTelemetry, OIDC</td></tr>
<tr><td>Several communities, one installation</td><td>Multi-VO from the start</td></tr>
<tr><td>Communities add their own pieces</td><td>Extensions, with a reference extension</td></tr>
<tr><td>Small installations on a few hosts</td><td>Options that do not need Kubernetes</td></tr>
</tbody></table>

</div>

</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# Two audiences, one project

<div class="duw-two dx-tight mt-2">

<div class="dx-card dx-card-legacy">

### Communities on DIRAC today

They want **stability and a smooth transition.**

- Move **component by component**, over the same databases. No flag day.
- DIRAC keeps running, with **security and performance patches**.
- Your extension keeps working while you move.
- **The whole production chain is new**: production (workgraph), transformation and job (parcel). We plan it with you.

</div>

<div class="dx-card dx-card-new">

### Communities without DIRAC

They should **not feel DIRAC's legacy technical choices.**

- A **new data model** for transformations, not DIRAC's.
- **Standard protocols**, multi-VO from the start.
- **Their own execution** (HTCondor, for example) behind a compute backend.
- Their requirements go through **the same process** as everyone's.

</div>

</div>

<div class="dx-key mt-3">One project, one process, two paths. We respond to both as requirements arrive.</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# Side by side, step 1: future clients

<img :src="'/figures/fig-step1.svg'" alt="A future client in DIRAC calls the DiracX job status endpoint; both sides share the same databases" style="width:64%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- Job status goes through DiracX over the **same databases, no data moved**: the first step of a deployment, to check the new system works as expected.
- **Jobs themselves are not carried over.** Parcels replace them.

</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# What changes for transformations

<img :src="'/figures/fig-mapping.svg'" alt="DIRAC's production, transformation and job against DiracX's workgraph, transformation and parcel: not compatible, except that a parcel runs as a job on the DIRAC backend; resource status and data management are reused" style="width:78%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **New concepts, no compatibility**: production and workgraph, old and new transformation, job and parcel do not map onto each other.
- **One bridge**: a parcel can run as a DIRAC job. **Resource status and data management are reused.**

</div>

---

<div class="duw-sec">2 · Evolving requirements, fruitful collaboration</div>

# Side by side, step 2: a backend for each parcel

<img :src="'/figures/fig-step2.svg'" alt="The DiracX Transformation System sends part of its parcels to the DIRAC WMS backend and the rest to a DiracX backend; it uses new tables that nothing else shares" style="width:82%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **Your DIRAC WMS keeps running the jobs.** DiracX keeps the books, in new tables.
- **Move gradually and reversibly**: start at 100% on DIRAC, raise the DiracX share per installation, VO and type.

</div>

---
layout: section
---

# 3 · Adapting quickly

Responding to changing requirements, in small steps

---

<div class="duw-sec">3 · Adapting quickly</div>

# The journey so far

<div class="duw-vt">

<div class="d">July 2023</div><div class="r"></div><div><b>DiracX development starts.</b> A prototype, then the first future clients.</div><div class="l">Prove the foundations on one small service.</div>

<div class="d">2025</div><div class="r"></div><div><b>In production for LHCb.</b> Authentication, job status, sandboxes.</div><div class="l">Real traffic shows where the cost really is.</div>

<div class="d">2025</div><div class="r"></div><div><b>Web app and pilot security.</b> Both experimental: the web app will be largely rewritten, pilots restart from scratch.</div><div class="l">Explore early, rewrite when requirements are clearer.</div>

<div class="d">January 2026</div><div class="r"></div><div><b>Scrum.</b> A weekly meeting that aims at removing bottlenecks and welcoming contributions; old issues cleaned up, 295 → 195 open.</div><div class="l">A shared rhythm lets part-time people contribute.</div>

<div class="d">Feb – Aug 2026</div><div class="r"></div><div><b>First community migration: the RSS.</b> Read side released.</div><div class="l">Design first, and let the team own the plan.</div>

<div class="d">Spring 2026 →</div><div class="r"></div><div><b>Two proofs of concept, still open:</b> matchmaking and interCEde.</div><div class="l">Try an idea cheaply before committing to it.</div>

<div class="d">Since 1 July 2026</div><div class="r"></div><div><b>The transformation system.</b> Requirements gathered with the communities, eight ADRs drafted.</div><div class="l">Specification is real work.</div>

</div>

---

<div class="duw-sec">3 · Adapting quickly</div>

# The current process, open to change

<img :src="'/figures/fig-pipeline.svg'" alt="One round from requirement to delivered package, nine steps" style="width:56%;margin:0 auto;display:block" />

<div class="dx-tight mt-2">

- **Scrum since 21 January 2026**: two-week sprints; planning and refinement in one weekly meeting; a monthly meeting with installation administrators; hackathons.
- **Each community has representatives.** Design decisions are ADRs by a main architect. ADRs and roadmap are public; the board is not.
- **It is not fixed.** Like the roadmap, we adapt the process as we learn, and we are open to optimising it.

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

</div>

</div>

---

<div class="duw-sec">4 · Results so far</div>

# Where work waits

<img :src="'/figures/fig-pipe.svg'" alt="Work flows through specification, development and review; development was widened by Scrum, specification and review remain the narrow parts" style="width:92%;margin:0 auto;display:block" />

<div class="dx-tight mt-2">

- **Scrum widened development**: more contributors, a shrinking backlog.
- **Specification and review are the narrow parts**, and they will matter more with every new component.

</div>

---
layout: section
---

# 5 · What’s next

How we could improve, and the roadmap

---

<div class="duw-sec">5 · What’s next</div>

# How you can help, and what we would like to ask

<div class="duw-two dx-tight mt-2">

<div>

**Where a part-time contributor helps most**

- **Review pull requests.** Our scarcest resource.
- **Port your plugins** (a catalogue feeder, a packer) when the transformation system lands.
- **Write a compute backend** (HTCondor, push to HPC).
- **Check the ADRs against your practice.** They lean toward LHCb today.

</div>

<div class="dx-card dx-card-blue" style="height:auto">

### Questions for developers and product owners

1. **Kanban style:** when your tasks are done, should you review before starting something new?
2. What would make you review a pull request from **another community**?
3. What should **the team own** that architects decide today, starting with the plan for the transformation system?

</div>

</div>

<div class="dx-eyebrow mt-2">Ideas for developers and product owners to weigh, not decisions</div>

<span class="dx-chips mt-1">
<span class="dx-chip">finished your tasks? review before starting more (kanban style)</span>
<span class="dx-chip">limit work in progress</span>
<span class="dx-chip">split big changes, announce them early</span>
<span class="dx-chip">named reviewers per component</span>
<span class="dx-chip">time-boxed ADR reviews</span>
<span class="dx-chip">the team owns its plan</span>
</span>

---

<div class="duw-sec">5 · What’s next</div>

# Agentic AI amplifies what the process already gets wrong

<div class="grid grid-cols-5 gap-6">

<div class="col-span-2">

<div class="duw-quote">"AI does not resolve ambiguity. It amplifies it."</div>
<div class="duw-small mt-1">Nir Yechiel, <a href="https://nyechiel.com/blog/2026/07/02/the-bottleneck-moved/">The bottleneck moved</a>, July 2026</div>

<div class="dx-tight mt-3">

- Writing code got cheap. **Deciding what to build and checking it** did not.
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

<div class="duw-sec">5 · What’s next</div>

# The roadmap moves with the communities

<div class="duw-cols">

<div class="duw-col now">
<div class="when">Now → end 2026</div>
<h3>Prove the bridge, settle the design</h3>
<ul>
<li>Future client for job status: load-test the new installation</li>
<li>Resource status: DIRAC adapter (two pull requests open)</li>
<li>Transformation ADRs: review, decision makers</li>
</ul>
</div>

<div class="duw-col">
<div class="when">Then</div>
<h3>The transformation system, bottom-up</h3>
<ul>
<li>CWL jobs become parcels, on a dummy backend</li>
<li>Transformations, then workgraphs</li>
<li>A <code>legacy-dirac</code> backend in parallel, so real runs start early</li>
</ul>
</div>

<div class="duw-col later">
<div class="when">After</div>
<h3>Real execution</h3>
<ul>
<li>Data transformations through the RMS</li>
<li>Native backends, and a share of work moved gradually</li>
<li>One real production shadowed end to end</li>
</ul>
</div>

</div>

<div class="duw-cols" style="margin-top:.6rem">
<div class="duw-col later" style="grid-column: span 3">
<div class="when">In parallel, at their own pace</div>
<span class="dx-chips mt-1">
<span class="dx-chip">matchmaking proof of concept</span>
<span class="dx-chip">interCEde</span>
<span class="dx-chip">web application (to be largely rewritten)</span>
<span class="dx-chip">MCP and agent interface</span>
<span class="dx-chip">accounting and observability</span>
</span>
</div>
</div>

<div class="dx-oneline mt-2">Priorities, not commitments. New requirements can reorder this page; the team writes the detailed plan.</div>

---

<div class="duw-sec">5 · What’s next</div>

# If you run an installation today

<div class="grid grid-cols-2 gap-6 dx-tight">

<div class="dx-card dx-card-new">

### What you can count on

- **DIRAC keeps running**, with security patches and performance fixes when needed.
- **You choose when to switch each component**, usually at a shutdown.
- **No data migration** for anything but the transformation system.
- **Your extension keeps working** on DIRAC while you move.
- **Transformations move last and in steps**, with your DIRAC WMS still running the jobs.

</div>

<div class="dx-card dx-card-blue">

### What we need from you

- **Tell us how many productions, plugins and workflows you have**, and which must survive. There is no compatibility with the new system, and nothing describes their migration yet.
- **Say which new transformation concepts do not fit** your practice.
- **Test in certification**; two installations already do.
- **Rename `LegacyClientEnabled`** to `FutureClientEnabled` if you set it.

</div>

</div>

---
layout: default
---
<div class="duw-sec">Take-aways</div>

# Take-aways

<div class="grid grid-cols-1 gap-4 mt-3 text-lg">

<div>
<div class="dx-eyebrow">For operators</div>
<div class="dx-tight">

- **Move to what exists as soon as you can; DIRAC is only patched.** You move one component at a time. The transformation system is the exception, and we plan it with you.

</div>
</div>

<div>
<div class="dx-eyebrow">For developers</div>
<div class="dx-tight">

- **Review is where the project is short.** New communities' requirements go through the same process as everyone's, and have already reordered the roadmap once.

</div>
</div>

<div>
<div class="dx-eyebrow">For this week</div>
<div class="dx-tight">

- **Which productions and plugins must survive the move, and what would make you review?** Both change the plan.

</div>
</div>

</div>

---
layout: cover
---

# Thank you

<span style="color:#fff">Questions and comments welcome, this week and after.</span>

<span class="dx-author" style="color:#fff">Alexandre F. Boyer</span> · <span style="color:#fff">alexandre.franck.boyer@cern.ch</span>

<span style="color:#fff">github.com/DIRACGrid · diracx.diracgrid.org</span>

<div class="dx-logobar mt-8">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC — The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX — The Interware" />
</div>

---

<div class="duw-sec">Backup</div>

# Backup: if you migrate extension code

<div class="duw-two dx-tight mt-2">

<div>

1. **Run DIRAC 9** and a released DiracX (still 0.x: the API can change).
2. **Register all your VOs in DiracX** (configuration sync) *before* enabling anything.
3. **For each service you move:** build the DiracX route, write a `FutureClient` that implements *every* method of the legacy client, then switch it in the CS.
4. **Databases:** add tables beside DIRAC's, never alter an existing column.

</div>

<div>

5. **Use `gubbins`** as the template; if you extend routes, extend the client and regenerate it for each DiracX release.
6. **Leave alone** what you do not switch: agents, DISET services, pilots, the CS.

<div class="dx-card dx-card-blue mt-3" style="padding:.5em .8em;height:auto">

**Renamed on 3 September:** `LegacyClientEnabled` is now `FutureClientEnabled` (DIRAC ≥ 9.1.18). Rename it in your CS.

</div>

</div>

</div>

---

<div class="duw-sec">Backup</div>

# Backup: what the RSS taught us

<div class="duw-timeline">
  <div><div class="y">Feb 2026</div>RSS epic opened. User stories from a questionnaire. <b>No ADR yet.</b></div>
  <div class="bad"><div class="y">Mar – Jul</div>Database, logic and service written by <b>different people</b>. <b>The interfaces did not match.</b></div>
  <div><div class="y">Apr 2026</div>First ADR merged (tasks, DX-ADR-001).</div>
  <div><div class="y">Jun – Jul</div>Read routes released (v0.3.0). The DIRAC-side adapters are still open.</div>
  <div><div class="y">Sep 2026</div>Transformation ADRs 002–009 drafted.</div>
</div>

<div class="duw-two dx-tight mt-2">

<div>

**What we saw**

- A synchronous cache met an asynchronous database.
- The legacy cache expected a VO on every row; the new API did not return one.
- Newcomers owned the change without a written design.
- **The plan was written for the team, not by the team.**

</div>

<div>

**What we do now**

- **Design first**: an ADR before the code, reviewed by those who will use it.
- **Vertical tickets**: one person takes a behaviour from database to API, closed by a scenario test.
- **The team owns the plan.** Developers and product owners decide how the transformation system is cut and ordered.

</div>

</div>

---

<div class="duw-sec">Backup</div>

# Backup: what each retrospective changed

<div class="duw-two">

<div class="duw-act">

**Done**

- <span class="dn">✓</span>Define what "done" means for a PR, and avoid new technical debt
- <span class="dn">✓</span>Do not plan dependent tasks in the same sprint
- <span class="dn">✓</span>Define the Scrum roles
- <span class="dn">✓</span>Estimates and velocity, with bonus points for external contributions
- <span class="dn">✓</span>Ask for reviews in the chat channel
- <span class="dn">✓</span>Announce a big PR early, and split the work

</div>

<div class="duw-act">

**In progress**

- <span class="ip">→</span>Developers with spare time review PRs, at least a first pass
- <span class="ip">→</span>Architects share a more detailed roadmap
- <span class="ip">→</span>Reviewers double-check PR titles before merging
- <span class="ip">→</span>Feature PRs are tested in certification
- <span class="ip">→</span>Avoid verbose, AI-generated issues full of details that go stale
- <span class="ip">→</span>A better view of PRs ready for review versus needing changes

</div>

</div>

<div class="dx-oneline mt-3">Nine months in, the open items are mostly about review and about the roadmap.</div>

---

<div class="duw-sec">Backup</div>

# Backup: what the new transformation system looks like

<div class="duw-loop">
  <div class="duw-node ext"><b>Catalogue</b>DFC, Rucio, bookkeeping</div>
  <div class="duw-arrow">→</div>
  <div class="duw-node"><b>Feeder</b>tops up the pool <em>(plugin)</em></div>
  <div class="duw-arrow">→</div>
  <div class="duw-node pool"><b>Input pool</b>one row per input, exact counters</div>
  <div class="duw-arrow">→</div>
  <div class="duw-node"><b>Packer</b>groups inputs into parcels <em>(plugin)</em></div>
  <div class="duw-arrow">→</div>
  <div class="duw-node pool"><b>Dispatcher</b>core: picks a backend, submits</div>
</div>

<div class="duw-backends">
  <div class="duw-node bridge"><b>legacy-dirac</b>DiracX keeps the books, your DIRAC WMS runs the work</div>
  <div class="duw-node"><b>diracx-pilot / remote</b>native, pull and push</div>
  <div class="duw-node"><b>htcondor</b>for communities that already run it</div>
  <div class="duw-node"><b>data (RMS)</b>replicate and remove</div>
</div>

<table class="duw-map mt-3" style="font-size:.92rem">
<thead><tr><th>In DIRAC</th><th>In DiracX</th></tr></thead>
<tbody>
<tr><td>Production</td><td>Workgraph: a DAG of transformations, written in CWL</td></tr>
<tr><td>Task</td><td>Parcel: immutable, never retried (retries live on the input)</td></tr>
<tr><td>XML workflow, plugin classes</td><td>CWL 1.2 with <code>dirac:</code> hints; feeder, packer, hooks, actions</td></tr>
<tr><td>Integer TransformationID</td><td>UUID</td></tr>
</tbody></table>

<div class="duw-small mt-2">DX-ADR-002 to 009 are drafts, in a fork at the time of writing (decision makers TBD).</div>

---

<div class="duw-sec">Backup</div>

# Backup: the web application, and what we are weighing

<div class="duw-opts">

<div class="duw-opt">
<h3>A · Stay: React + Next.js + MUI</h3>
<ul>
<li>The 2024 plan: popular libraries, many developers</li>
<li>Next.js now favours server rendering; we ship a static app</li>
<li>July audit: hard to reuse outside its monorepo; extensions copy ~12 files that drifted</li>
</ul>
</div>

<div class="duw-opt">
<h3>B · Keep React, drop Next.js</h3>
<ul>
<li>Vite plus a client-side router, a drafted proposal</li>
<li>Smallest change; fixes the framework mismatch</li>
<li>Keeps the dependency and upgrade treadmill</li>
</ul>
</div>

<div class="duw-opt lean">
<h3>C · Plain web components</h3>
<ul>
<li>Browser standards, almost no dependencies, no build step</li>
<li>An extension is a component you register, not files you copy</li>
<li>Written with LLM help; <b>reviewed by people</b></li>
</ul>
</div>

</div>

<div class="dx-key mt-3"><b>Not decided.</b> C must prove: the job monitor stays fast on 500+ rows, accessibility and theming hold, and the review burden does not grow.</div>

---

<div class="duw-sec">Backup</div>

# Backup: where the numbers differ from the proceedings

<div class="dx-tight mt-2">

- **Share of changes from outside the LHCb group**, 2025 / since January / since June: **19 / 42 / 54%** in the proceedings (merged pull requests, not de-duplicated); **20 / 42 / 56%** de-duplicated across release branches; **19 / 22 / 29%** if the GridPP developer is counted as core; **11 / 41 / 54%** if the three other LHCb contributors are counted as LHCb too.
- **Issue rates** (opened / closed a month, before and after January 2026): 16.3 → 27.3 and 10.6 → 36.6 in the proceedings; 16.7 → 27.6 and 10.9 → 37.6 recomputed. Not yet reconciled.
- **Top-two share of first reviews**: 61 → 75% (proceedings); 61 → 74% de-duplicated.
- **Window "since the last workshop"** starts 17 September 2025; the proceedings compare September 2024 – 20 January 2026 against 21 January – 4 September 2026.

</div>

---

<div class="duw-sec">Backup</div>

# Backup: counting a community's contribution

<table class="duw-stat" style="font-size:.78rem;line-height:1.1">
<thead><tr><th>Since 17 Sep 2025</th><th>Merged PRs</th><th>Lines changed (k)</th><th>People</th><th>First reviews given</th><th>Issues opened</th><th>Story points</th></tr></thead>
<tbody>
<tr><td>LHCb core (5)</td><td>403</td><td>158</td><td>5</td><td>499</td><td>213</td><td>193</td></tr>
<tr><td>Other LHCb</td><td>13</td><td>13</td><td>4</td><td>1</td><td>1</td><td>26</td></tr>
<tr><td>CTAO</td><td>49</td><td>34</td><td>7</td><td>11</td><td>45</td><td>60</td></tr>
<tr><td>GridPP</td><td>109</td><td>10</td><td>3</td><td>9</td><td>23</td><td>36</td></tr>
<tr><td>IN2P3</td><td>16</td><td>45</td><td>2</td><td>0</td><td>3</td><td>33</td></tr>
<tr><td>FCC</td><td>9</td><td>39</td><td>2</td><td>8</td><td>1</td><td>12</td></tr>
<tr><td>EGI</td><td>15</td><td>1</td><td>2</td><td>0</td><td>1</td><td>7</td></tr>
<tr><td>CMS</td><td>14</td><td>1</td><td>6</td><td>0</td><td>4</td><td>15</td></tr>
<tr><td>Belle II · IHEP · not attributed</td><td>6</td><td>0</td><td>5</td><td>4</td><td>9</td><td>25</td></tr>
</tbody></table>

<div class="duw-small mt-2">Pull requests are what the project counts, but they hide size: GridPP's 109 changes are small SQL fixes, FCC's 9 and IN2P3's 16 are large. Story points: finished items since 21 January; 253 of 264 attributed (126 by assignee, 102 by the author of the pull request, 25 by the linked pull request). First reviews given by bots are excluded.</div>
