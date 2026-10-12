---
theme: default
title: "DiracX developments: directions"
info: |
  ## DiracX developments: directions — DIRAC(X) Users' Workshop 12
  Alexandre F. Boyer (CERN).
  13–16 October 2026, FZU Prague. 30 minutes (Tue 13 Oct, 10:00–10:30).
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

# DiracX developments

<div class="duw-subtitle">Directions</div>

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
WebAppDIRAC 6.0.7 · DIRACOS2 2.63<br/>
**Maintained**: security fixes, and performance fixes when needed.

</div>

<div>

**DiracX** v0.6.1<br/>
diracx-charts 1.1.17<br/>
**Developed**, one component at a time.<br/>
The web app (diracx-web 0.1.0-a11) and the `dirac` CLI are still experimental.

</div>

</div>

<div class="dx-key mt-1"><b>Adopt what already exists in DiracX.</b> DIRAC is only patched, so that DiracX can progress.</div>

---

<div class="duw-sec">1 · Where we are now</div>

# The journey so far

<img :src="'/figures/fig-journey.svg'" alt="Timeline of DiracX milestones from July 2023 to July 2026, with proofs of concept running in parallel: web app, pilot security, matchmaking, interCEde, analytics and observability" style="width:84%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **From 2023, three hackathons a year** onboarded new contributors, with no dashboard or regular meeting to follow progress. **Scrum** brought both in 2026.
- **Proofs of concept run in parallel**, not mandatory: we try an idea before committing to it.

</div>

---

<div class="duw-sec">1 · Where we are now</div>

# Many part-time hands

<img :src="'/figures/fig-collab.svg'" alt="Groups of contributors linked by dashed two-way arrows around the question: how do we work best together?" style="width:66%;margin:0 auto;display:block" />

<div class="dx-tight mt-1">

- **36 people** contributed since the last workshop, **10 to 18** in any given month, almost all part-time: about **5 to 6 full-time equivalents** in total, LHCb core developers included.
- They maintain DIRAC and develop DiracX at the same time.

</div>

<div class="dx-key mt-2"><b>Finding the best way to work with each other is paramount.</b></div>

---

<div class="duw-sec">1 · Where we are now</div>

# Delivered since the last workshop

<div class="duw-three3 mt-2">

<div class="dx-card dx-card-new">

### DiracX, in use
- From alpha to **23 releases**, the latest **v0.6.1** on 9 October 2026.
- **LHCb in production**; two other installations certifying.

</div>

<div class="dx-card dx-card-blue">

### Usable now
**Sandboxes in S3**, **job status** through the future client, **resource status** read in DiracX, the **tasks framework**, and experimental **OpenTelemetry** observability.

</div>

<div class="dx-card dx-card-legacy">

### DIRAC kept safe
v8, v9.0 and v9.1 patched: **security fixes** and **SQL hardening**, with GridPP.

</div>

</div>

---
layout: section
---

# 2 · Evolving requirements

New communities and new use cases

---

<div class="duw-sec">2 · Evolving requirements</div>

# What DIRAC is for, and what it values

<div class="dx-key">Running large-scale workflows of embarrassingly parallel jobs on heterogeneous, distributed computing and storage resources: high-throughput computing.</div>

<div class="duw-three3 mt-3">

<div class="dx-card dx-card-blue">

### Minimal dependencies
A database and a search index, on a few hosts.

**In DiracX:** standard protocols for what is external, with a minimal option for each.

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

<div class="duw-sec">2 · Evolving requirements</div>

# Requirements keep evolving

<div class="duw-two">

<div class="dx-card dx-card-blue">

### New communities
**CMS and FCC**, who joined this summer, bring new requirements. CMS has no DIRAC installation and runs its own workload management: [Wednesday's CMS talk](https://indico.cern.ch/event/1588323/contributions/7264642/).

</div>

<div class="dx-card dx-card-new">

### Advanced needs, in extensions
**CTAO, LHCb, Belle II and JUNO** built extensions for advanced needs that are now close to each other. They belong in the common project: CTAO's use of **CWL** turned out useful for DiracX as a whole.

</div>

</div>

<div class="dx-key mt-2" style="font-size:1.15em;padding:.6em 1em"><b>DOps is where you share your use cases.</b> The representatives of the communities decide together whether the vanilla project will fulfil them, or say clearly that it will not. Bring them early: someone else may need the same thing.</div>

---
layout: section
---

# 3 · Adapting quickly

Responding to changing requirements, in small steps

---

<div class="duw-sec">3 · Adapting quickly</div>

# Almost the current process

<img :src="'/figures/fig-pipeline.svg'" alt="One round from requirement to delivered increment, seven steps" style="width:47%;margin:0 auto;display:block" />

<div class="dx-tight mt-2">

- **Scrum since 21 January 2026**: two-week sprints; planning and refinement in one weekly meeting; a monthly meeting with the representatives (DOps); hackathons.
- **Large changes start with a proof of concept, then an ADR** that the other developers approve. ADRs and roadmap are public; the board is not.

</div>

<div class="dx-key mt-2"><b>Individuals and interactions over processes and tools.</b> The process is a guide, not a rule, and it adapts as we learn.</div>

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
**DMS**: a DIRAC client calls DiracX instead of DIRAC, over the same databases. **RSS**: the read side is in DiracX; DIRAC's adapter is in review.

<img :src="'/figures/fig-mini-future.svg'" alt="A DIRAC client calls either the DIRAC service or the DiracX service; both use the same databases" style="width:100%;margin-top:.4rem" />

</div>

<div class="dx-card dx-card-new">

### Standard protocols
**Systems internal to DIRAC give way to standards**: monitoring to OpenTelemetry, accounting to analytics.

<img :src="'/figures/fig-mini-protocols.svg'" alt="Monitoring becomes OpenTelemetry and accounting becomes analytics" style="width:100%;margin-top:.4rem" />

</div>

</div>

<div class="duw-small mt-2">This week: <a href="https://indico.cern.ch/event/1588323/contributions/7286647/" target="_blank">Data Management for DiracX</a> · <a href="https://indico.cern.ch/event/1588323/contributions/7264662/" target="_blank">Analytics for DiracX</a> · <a href="https://indico.cern.ch/event/1588323/contributions/7264658/" target="_blank">RSS in DIRAC and DiracX</a> (all Wednesday)</div>

---

<div class="duw-sec">3 · Adapting quickly</div>

# Standard protocols: one project, many contexts

<div class="grid grid-cols-12 gap-5 mt-1">

<div class="col-span-5 dx-tight">

- **We choose our tooling**: standard implementations work, not one product we have to maintain.
- **You connect DiracX to what you already run**: your identity provider, your storage, your monitoring, your databases.
- **Small or large**: a small installation does not need a cutting-edge stack; a large one plugs in its own.

</div>

<div class="col-span-7">

<table class="duw-map"><thead><tr><th>For</th><th>Protocol</th><th>In the charts</th><th>Or yours</th></tr></thead><tbody>
<tr><td>identity</td><td>OIDC</td><td>Dex; INDIGO IAM optional</td><td>your SSO or IAM</td></tr>
<tr><td>sandboxes</td><td>S3</td><td>SeaweedFS, optional</td><td>your site's S3 service</td></tr>
<tr><td>metrics, traces</td><td>OpenTelemetry</td><td>collector, Jaeger, Grafana, optional</td><td>your monitoring</td></tr>
<tr><td>state, job parameters</td><td>SQL, OpenSearch</td><td>MySQL, OpenSearch: <b>tests and demos only</b></td><td>your IT's databases: <b>required in production</b></td></tr>
</tbody></table>

</div>

</div>

<div class="dx-key mt-4"><b>We ship a minimal option for each, so DiracX works out of the box, as DIRAC does.</b> Databases are the exception: running MySQL or OpenSearch from the charts is not supported in production. Running without Kubernetes: <a href="https://indico.cern.ch/event/1588323/contributions/7288348/" target="_blank">Thursday's talk</a>.</div>

---
layout: section
---

# 4 · How we work, measured

What the numbers tell us about our process

---

<div class="duw-sec">4 · How we work, measured</div>

# More hands, from more communities

<img :src="'/figures/fig-communities.svg'" alt="Merged pull requests a month from January 2025 to August 2026, stacked by community: LHCb core, other LHCb, CMS, CTAO, IN2P3, GridPP, EGI, FCC, IHEP, Belle II, not attributed" style="width:62%;margin:0 auto;display:block" />

<div class="duw-three dx-tight" style="margin-top:.2rem">

<div>

**634 pull requests** merged across all DIRACGrid repositories since the last workshop (367 DIRAC, 261 DiracX), from nine communities; **17 new contributors**.

</div>

<div>

Outside the five core developers: **36% of merged PRs, 28% of issues opened, 53% of story points.**

</div>

<div>

Read with care: about half of the 2026 rise in PRs is **one GridPP developer** hardening DIRAC's SQL. CMS merged 14 changes since July.

</div>

</div>

---

<div class="duw-sec">4 · How we work, measured</div>

# Since Scrum: the backlog is shrinking

<div class="duw-stats3">
<div><b>295 → 195</b>open issues, January 2026 to September</div>
<div><b>10.6 → 36.6</b>closures a month; 26.6 completed, 10.0 not planned or duplicate</div>
<div><b>16.3 → 27.3</b>issues opened a month</div>
</div>

<img :src="'/figures/fig-burnup.svg'" alt="Cumulative issues in the DIRACGrid repositories since January 2024: open issues rose from 156 to 295 before January 2026 and fell to 195 by September" style="width:66%;margin:0 auto;display:block" />

<div class="duw-small" style="text-align:center">All issues in the DIRACGrid repositories, bots excluded. Part of the fall is triage, and about 120 of the 195 still open are not triaged yet.</div>

---

<div class="duw-sec">4 · How we work, measured</div>

# We plan for twice what we deliver

<div class="grid grid-cols-12 gap-5">

<div class="col-span-7">

<img :src="'/figures/fig-velocity.svg'" alt="Story points per person and sprint, expected against delivered, for sprints 1 to 23, sprints 1 to 5 shaded as the pilot with CTAO: expected is about twice what is delivered in every sprint since January" style="width:100%" />

</div>

<div class="col-span-5 dx-tight">

- Since January, a median of **14 story points** per person and sprint expected, **6.6 delivered**. No sprint delivered what was expected.
- Delivered velocity follows availability: workshops, conferences, holidays.
- **Unplanned work lives in DIRAC**: 56% of the story points delivered on DIRAC were unplanned, against 11% on DiracX.

<div class="dx-card dx-card-blue mt-2" style="height:auto;padding:.5em .8em"><b>For developers:</b> we overestimate what a sprint can hold, partly because we do not count the unplanned DIRAC maintenance. Plan for it.</div>

</div>

</div>

---

<div class="duw-sec">4 · How we work, measured</div>

# The bottleneck is review

<div class="grid grid-cols-12 gap-5">

<div class="col-span-6">

<img :src="'/figures/fig-review.svg'" alt="Share of first reviews given by the top reviewer and the top two reviewers each quarter, rising from 62% in 2025 Q1 to 75% in 2026 Q3" style="width:100%" />

<div class="dx-ref mt-1">Share of first reviews, by quarter</div>

</div>

<div class="col-span-6 dx-tight">

- **Two people give three quarters of first reviews.** None of the 14 contributors new since January has given one yet.
- **Smaller pull requests get reviewed sooner**: 2.6 hours under 10 lines, 23 hours from 500 lines. On small changes the core five wait 2.5 hours, everyone else 11.
- Design review (ADRs, in meetings and on chat) is not in these numbers.

<div class="dx-card dx-card-blue mt-2" style="height:auto;padding:.5em .8em"><b>Question for developers:</b> kanban style, should you review before starting something new once your tasks are done?</div>

<div class="mt-2"><a href="https://diracx.diracgrid.org/en/latest/dev/explanations/splitting-prs/" target="_blank" class="dx-ref">How to split a large change into stacked pull requests</a></div>

</div>

</div>

---

<div class="duw-sec">4 · How we work, measured</div>

# Where work waits

<img :src="'/figures/fig-pipe.svg'" alt="Work flows through specification, development and review; development was widened by Scrum, specification and review remain the narrow parts" style="width:92%;margin:0 auto;display:block" />

<div class="dx-tight mt-2">

- **Specification and review are the narrow parts**, and they will matter more with every new component.

<div class="dx-card dx-card-blue mt-2" style="height:auto;padding:.5em .8em"><b>For everyone in the room:</b> representatives, developers and users, where would you improve how we work?</div>

</div>

---
layout: section
---

# 5 · What’s next

How we could improve, and the roadmap

---

<div class="duw-sec">5 · What’s next</div>

# Cheaper code: easier to explore, same bottlenecks

<div class="grid grid-cols-5 gap-6">

<div class="col-span-2">

<div class="duw-quote">"AI's primary role in software development is that of an amplifier."</div>
<div class="duw-small mt-1"><a href="https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/">DORA 2025 State of AI-assisted Software Development</a></div>

<div class="dx-tight mt-3">

- Writing code got cheap, so **spikes and proofs of concept** are easier to try.
- **Deciding what to build and checking it** did not get cheaper.
- It does **not change our process**. It shows its weak points sooner.

</div>

</div>

<div class="col-span-3 dx-tight">

**Each one maps to what we saw**

- **Vague specification** → verbose, AI-generated issues that go stale. A clear ADR with a scenario test is what an agent, or a newcomer, can implement.
- **Review bottleneck** → more code means more to read, by the same two people.
- **Unplanned work** → faster code does not shrink urgent maintenance.
- **A new kind of user** → DiracX speaks HTTP and OAuth2, so an agent can use it through MCP.

<div class="dx-concludes"><carbon-arrow-right class="dx-concludes-arrow" /><span>invest in <strong>specifications, tests and review</strong>, not in typing</span></div>

</div>

</div>

---

<div class="duw-sec">5 · What’s next</div>

# Next: building the transformation system

<div class="dx-key" style="font-size:1.1em"><b>Implementation follows the ADRs; code starts on Wednesday.</b> The technical details are in the next talk.</div>

<div class="duw-two dx-tight mt-3">

<div>

**Where it comes from**

- **Use cases from the communities**: CMS, CTAO, FCC, Belle II and LHCb.
- **A design that comes from a proof of concept**, written down as ADRs.

</div>

<div>

**How it will be delivered**

- **Increments you can test**, at DOps.
- **The more we are, and the better organised, the sooner.**

</div>

</div>

<div class="dx-card dx-card-blue mt-3" style="height:auto;padding:.5em .9em"><b>This afternoon:</b> adapting your community's workflows to <b>CWL</b> from 14:00, then building the <b>transformation system</b> on them from 16:10.</div>

---

<div class="duw-sec">5 · What’s next</div>

# The roadmap moves with the communities

<img :src="'/figures/fig-roadmap2.svg'" alt="Long-running lines of work: Transformation System, Job Wrapper, Data Management System, Resource status; and exploratory spikes: WMS, analytics and observability, MCP server, clients" style="width:84%;margin:0 auto;display:block" />

<div class="dx-oneline mt-2">Priorities, not commitments. New requirements can reorder this page, and the team writes the detailed plan.</div>

---

<div class="duw-sec">5 · What’s next</div>

# A word on the web app

<div class="duw-small" style="margin-top:-.4rem">Announced at past workshops, not on this week's agenda.</div>

<div class="grid grid-cols-12 gap-5 mt-2">

<div class="col-span-7">

<img :src="'/figures/diracx-web-job-monitor.png'" alt="The DiracX web app's job monitor: a filterable list of jobs with a status chart beside it" style="width:100%;border:1px solid #d8dee2;border-radius:6px" />

</div>

<div class="col-span-5 dx-tight">

- **Today: a job monitor**, smooth and responsive; extensible, unit and end-to-end tested.
- **We promised a simple app on popular libraries.** AI changes the game: richer interfaces from simple components, fewer dependencies.
- **Next: a consistent, user-centric experience** around the new transformation system and its components.

<div class="dx-key mt-2"><b>Increments at DOps</b> once the transformation system is usable. Feedback welcome any time.</div>

</div>

</div>

---

<div class="duw-sec">5 · What’s next</div>

# If you run an installation today

<div class="dx-card dx-card-new" style="height:auto">

### What you can count on

- **DIRAC keeps running**, with security patches and performance fixes when needed.
- **You choose when to switch each component**, usually at a shutdown; DIRAC and DiracX run in parallel meanwhile.
- **No data migration** for anything but the transformation system, which has its own tables.
- **Your extension keeps working** on DIRAC while you move.
- **Increments to test**, shown at DOps whenever a sprint delivers one. You test them with your own workflows in **CWL**; we give guidance on writing them, starting with this afternoon's hands-on.

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

- **Join the hackathon**: your workflows in CWL from 14:00, then the transformation system from 16:10.

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
