---
theme: default
title: "Workload Management: DIRAC and DiracX as compute backends"
info: |
  ## Workload Management: DIRAC and DiracX as compute backends. DIRAC(X) Users' Workshop 12
  Alexandre F. Boyer (CERN).
  13–16 October 2026, FZU Prague. Wed 14 Oct, 12:10 (30 min slot).
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

# Workload Management: DIRAC and DiracX as compute backends

<span class="dx-author">Alexandre F. Boyer</span> · CERN

12th DIRAC(X) Users' Workshop · FZU Prague · 13–16 October 2026

<div class="dx-logobar mt-10">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC, The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX, The Interware" />
</div>

---

# ARM and GPUs: HPC sees them first

<div style="display:grid;grid-template-columns:1.75fr 1fr;gap:1rem;align-items:center">

<img :src="'/figures/fig-worldmap.svg'" alt="World map of ARM and GPU systems: TOP500 systems in the US, Europe, Asia, Australia, Brazil and Saudi Arabia, and the WLCG ARM sites at Glasgow and GridKa" style="width:100%" />

<div class="duw-stats1">
<div><b>276 / 500</b>TOP500 systems with GPUs, June 2026 (110 in 2018)</div>
<div><b>35</b>ARM systems in the TOP500 (5 in 2020)</div>
<div class="grid"><b>Our communities</b>run mostly on grid sites. Some use a few HPCs opportunistically: LHCb on MareNostrum 5, up to 732 jobs at once.</div>
</div>

</div>

<div class="dx-key mt-2">What appears in HPC and clouds first reaches the grid next. The question is what it asks of the WMS.</div>

---

# From HPC to the grid, and to the WMS

<div class="duw-chain">
<div class="h">Driver</div><div class="h">HPC and clouds first</div><div class="h">Grid sites now</div><div class="h">What the WMS must do</div>

<div class="d gpu"><b>AI demand</b>NVIDIA data-centre revenue: $194B in FY2026, 90% of its total</div>
<div>GPUs in 276 of the TOP500</div>
<div>ATLAS: ~280 GPUs at 8 grid sites, little used; no GPU pledge unit before 2028</div>
<div class="w">Schedule CPU and GPU work together; match on capabilities</div>

<div class="d arm"><b>Energy and hardware cost</b>"badly hit by AI factories" (WLCG, 2026)</div>
<div>ARM in 35 of the TOP500; most new AWS CPU capacity is ARM</div>
<div>ATLAS: ARM up to half of a pledge, 11k slots at 5 sites; Glasgow ~20% ARM</div>
<div class="w">One site, two architectures: images and matching per architecture</div>

<div class="d core"><b>More cores per node</b>32 per socket in 2017, 192 in 2024; memory getting scarcer</div>
<div>HPCs hand out whole nodes: 112 cores on MareNostrum 5</div>
<div>Multicore pilots: 8 cores for 48 h (CMS)</div>
<div class="w">Fill nodes, not slots: multicore payloads, bundling, memory-aware matching</div>
</div>

<div class="duw-two mt-3">
<div class="dx-card dx-card-blue" style="height:auto">

**In DIRAC: temporary solutions**, to keep running on these resources without changing DIRAC, and keep it stable.

</div>
<div class="dx-card dx-card-new" style="height:auto">

**In DiracX: the long-term solutions**, designed for heterogeneous resources from the start.

</div>
</div>

---
layout: section
---

# 1 · Starting from the transformation system

What it changes for workload management

---

<div class="duw-sec">1 · Starting from the transformation system</div>

# The transformation system sees compute backends

<img :src="'/figures/fig-backends3d.svg'" alt="The DiracX transformation system dispatches parcels to three compute backends: the DIRAC WMS, a DiracX WMS to come, and HTCondor; each keeps its own data" style="width:72%;margin:-.8rem auto 0;display:block" />

<div class="dx-key mt-1">The transformation system (Tuesday's talks) sends parcels to compute backends. <b>The DIRAC WMS is one of them</b>, with its own data, as it is.</div>

---

<div class="duw-sec">1 · Starting from the transformation system</div>

# What separate backends give us

<div class="duw-three3">

<div class="dx-card dx-card-blue">

### A stable DIRAC
The DIRAC WMS keeps its data and its behaviour. No large change: fixes and performance only, until communities move away from it.

</div>

<div class="dx-card dx-card-new">

### A DiracX free of the legacy model
DiracX does not inherit DIRAC's jobs, tables or states. Work is a **parcel**; the WMS behind it is designed for it.

</div>

<div class="dx-card dx-card-legacy">

### No rush for a DiracX WMS
Most communities can rely on their existing WMS for now: DIRAC, or their own (see the <a href="https://indico.cern.ch/event/1588323/contributions/7264642/" target="_blank">CMS talk</a> just before).

</div>

</div>

<div class="dx-key mt-3">The DiracX WMS is not a priority. It will move slowly, in parallel, and get a plan when the transformation system needs a native backend.</div>

---
layout: section
---

# 2 · DIRAC: fixes and performance

What keeps it running while we migrate

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Faster

<img :src="'/figures/fig-path-faster.svg'" alt="The DIRAC WMS submission and matching path in clay: JobDB, TaskQueueDB, Matcher, PilotAgentsDB and PilotManager highlighted in green with their improvements; other components grey" style="width:64%;margin:-1rem auto 0;display:block" />

<div class="duw-prs"><a href="https://github.com/DIRACGrid/DIRAC/pull/8462" target="_blank">#8462</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8711" target="_blank">#8711</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8463" target="_blank">#8463</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8569" target="_blank">#8569</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8624" target="_blank">#8624</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8524" target="_blank">#8524</a></div>

<div class="dx-key mt-1">Several fixes made the DIRAC WMS faster, for installations at v9 and above. Most of these numbers need v9.1.</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# More reliable

<img :src="'/figures/fig-path-reliable.svg'" alt="The same path: TaskQueueDB, SiteDirector, JobAgent and JobWrapper highlighted in blue with their fixes" style="width:64%;margin:-1rem auto 0;display:block" />

<div class="duw-prs"><a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8340" target="_blank">#8340</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8441" target="_blank">#8441</a> <a href="https://github.com/DIRACGrid/DIRAC/pull/8750" target="_blank">#8750</a></div>

<div class="dx-key mt-1">None of these change how DIRAC works. They remove ways it could fail.</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Safer

<img :src="'/figures/fig-path-safer.svg'" alt="The same path: SandboxStore, JobStateUpdate, pilot logging, PilotManager, pilot files and the databases highlighted with the advisory each fix addresses" style="width:64%;margin:-1rem auto 0;display:block" />

<div class="duw-prs"><a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-j3xg-cjx8-qjpw" target="_blank">GHSA-j3xg</a> <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-pwvr-x92w-xmp8" target="_blank">GHSA-pwvr</a> <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vm3r-6cmw-8p5v" target="_blank">GHSA-vm3r</a> <span>fixed in v9.1.20 · v9.0.26 · v8.0.85</span> <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-7xw9-549r-8jrc" target="_blank">GHSA-7xw9</a> <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vg99-gr89-qhw9" target="_blank">GHSA-vg99</a> <span>fixed in v9.1.10 · v9.0.22</span></div>

<div class="dx-concludes mt-1"><carbon-arrow-right class="dx-concludes-arrow" /><span>DIRAC is patched, not developed: <strong>upgrading is how you get these</strong></span></div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Heterogeneous nodes

<img :src="'/figures/fig-hetero.svg'" alt="CVMFS holds one directory per architecture under .multiarch; an x86_64 node and an aarch64 node each pull their own image into a container limited by cgroup2; an HPC centre is reached through the SSH CE" style="width:60%;margin:-1rem auto 0;display:block" />

<div class="duw-two dx-tight">
<div>

- **aarch64 images** <span class="duw-was">DUW11</span>: <a href="https://github.com/DIRACGrid/DIRAC/pull/8456" target="_blank">#8456</a>, open, to certify. Needs CVMFS 2.14 (DUCC 2.14.1) where images are published; any client reads it.

</div>
<div>

- **Limits** <span class="duw-was">DUW11</span> and **HPC** <span class="duw-was">DUW11</span>: in v9.0.
- **Not solved in DIRAC**: a job for x86_64 *or* aarch64.

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Time left in the slot

<div class="duw-two dx-tight">
<div>

**The problem**
- Jobs in containers could not ask the batch system for the time left.
- The post-processing margin was known only to the Watchdog, which could only kill.

</div>
<div>

**An example**: an MC job sized for 183 events produced 150, was killed, and its output was never uploaded.

**Since v9.1.4** (#8479): the pilot reads the time left once; jobs read it from the pilot configuration.

</div>
</div>

<img :src="'/figures/fig-slot.svg'" alt="A slot split into pilot, payload and StopMargin; the margin is reserved before matching, a stop signal ends the payload cleanly, and a killed job reports why" style="width:52%;margin:0 auto;display:block" />

<div class="dx-key mt-1">The three fixes above are in <b>v9.1.21</b> only; see "Allocated time management" in the Administrator Guide. CPU work is normalised with DB12: <a href="https://indico.cern.ch/event/1588323/contributions/7264656/" target="_blank">next talk</a>.</div>

---
layout: section
---

# 3 · DiracX: parcels, not jobs

And the proofs of concept around the future WMS

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# No jobs in DiracX

<img :src="'/figures/fig-parcels-only.svg'" alt="User jobs and workgraphs, both CWL, become parcels, the record of work, which a dispatcher sends to a backend; the JobDB in DiracX is legacy, used only to test deployments and deleted once everyone is on DiracX" style="width:68%;margin:-.6rem auto 0;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- A user job is a parcel, like a bundle of transformation inputs. A failed parcel is final: resubmitting creates a new one.
- We do not port job monitoring or the job manager <span class="duw-was">DUW11</span>.

</div>
<div>

- The JobDB in DiracX is legacy. It receives job status updates from DIRAC, to **test that a DiracX deployment works**.
- It also feeds the **dummy job executor** (<a href="https://github.com/diracgrid/diracx/pull/995" target="_blank">diracx#995</a>): jobs go `Waiting → Matched → Running → Done` without running anything. A stand-in backend, to test the transformation system end to end.
- **Once everyone is on DiracX, it is deleted.**

</div>
</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# CWL describes all the work

<div class="duw-two">
<div>

**One format** (DX-ADR-007, draft): a user job, a workgraph and each transformation are CWL v1.2 documents.

- DiracX settings are **hints** under `dirac:`, never requirements: every document stays plain, runnable CWL.
- The same document runs with `cwltool`, locally against grid data, and at scale.
- Processes are resolved before dispatch: the node runs without fetching definitions.

</div>
<div>

**What this means for a WMS backend**
- Matching requirements come from the hints.
- The job wrapper resolves inputs (`lfn:`, `sandbox:`), captures the output sandbox, and writes a status report per input.
- Outputs are registered by DiracX after the parcel ends, not by the wrapper.

**Today**: `dirac-cwl` 1.3.0; an experimental CWL job wrapper in DIRAC (#8425). The CWL job submission prototype for DiracX <span class="duw-was">DUW11</span> became part of the transformation system.

</div>
</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# interCEde: one library for computing elements

<div class="dx-key">A typed, asynchronous library to submit to and manage computing elements, usable by DIRAC, DiracX and other workload managers. <span class="duw-small">github.com/DIRACGrid/intercede, proof of concept</span></div>

<div class="duw-three3 mt-3">

<div class="dx-card dx-card-blue">

### Design
Three ADRs under review (intercede #4): computing elements, integration tests, credentials.

Open points: per-site submit options, whole-node and GPU requests, ARC delegation renewal, cleaning up cloud VMs.

</div>

<div class="dx-card dx-card-blue">

### Code
Core contract proposed this week (#27).

Integration-test scaffolding (#25), and test setups from the communities: HTCondor, ARC with Slurm, Slurm.

</div>

<div class="dx-card dx-card-new">

### Next
Merge the ADRs, then: core, registry, integration tests, backends.

Last, a synchronous facade and an adapter so DIRAC can use it (#24).

</div>

</div>

<div class="duw-small mt-3">In the backend model, a WMS backend owns the policy (matching, pilots); interCEde owns the mechanics of talking to a CE.</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# A matcher for the DiracX WMS

<div class="duw-two">
<div>

**Goal** (diracx #843): match pilots to work at **1 kHz** (200 Hz at least), with 10 million waiting items per VO. Redis holds an index that can be rebuilt from the database.

**Built**: matching with tag expressions, prioritisation, a benchmark harness, a Redis data model (release 0.4.0, Sep 2026).

**Measured**: the pure Python baseline only, 210 ms per match at 50k candidates, 5.7 s at 750k. No Redis numbers yet.

</div>
<div>

**What we learned**
- Real requirements vary little: LHCb has 872k waiting jobs but 14 distinct (CPU time, group) pairs. Group work by profile, as task queues do; do not test items one by one.
- An item eligible at ~49 sites must not be stored 49 times.
- Work runnable on two architectures needs a *list* of requirements.

</div>
</div>

<div class="dx-card dx-card-new mt-3" style="height:auto">

**Next**: matching inside Redis (Lua) and its benchmark on realistic data (#873), then scale tests (#874). **Then an ADR**, written from those numbers, for the matcher of the DiracX WMS backend.

</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# Pilots: the re-thinking has not started

<div class="duw-three3">

<div class="dx-card dx-card-new">

### Landed
- A pilot database and router in DiracX (#570, Aug 2026) <span class="duw-was">DUW11</span>.
- Pilot: Python 2 removed <span class="duw-was">DUW11</span>; maintenance fixes.

</div>

<div class="dx-card dx-card-legacy">

### Paused
- Pilot registration and authentication with pilot tokens (#421).
- Pilot logging through DiracX (#550).
- Untouched since mid-2025.

</div>

<div class="dx-card dx-card-blue">

### Questions for later
- What does a pilot need to know about parcels?
- What belongs to the pilot, what to the job wrapper?
- One model for pull and push?

</div>

</div>

<div class="dx-key mt-3">Pilots belong to the DiracX WMS backend, which comes after the transformation system. We continue to patch the DIRAC pilot.</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# The job wrapper: one for all of us, owners wanted

<div class="duw-two">
<div>

**Today there are several**
- DIRAC's JobWrapper: pre-processing, payload, post-processing; an offline variant for push.
- The `dirac-cwl` wrapper, experimental in DIRAC.
- Executor prototypes in DiracX.

Each community also adds its own steps around the payload.

</div>
<div>

**Requirements to gather**
- Inputs: data, sandboxes, protocol access.
- Time left, graceful stop, containers, architectures.
- Nodes without outbound network.
- Reporting: status, parameters, logs.
- What happens when an upload fails.

</div>
</div>

<div class="dx-card dx-card-blue mt-3" style="height:auto">

**We are looking for owners**: people who collect the requirements from the communities, set priorities, and accept the result, in a product-owner role. Come and talk to us this week.

</div>

---

<div class="duw-sec">Take-aways</div>

# Take-aways

<div class="duw-two dx-tight">
<div>

<div class="dx-eyebrow">The model</div>

- The transformation system sends parcels to compute backends; the DIRAC WMS is one of them.
- DIRAC stays stable; DiracX is free of DIRAC's job model.

<div class="dx-eyebrow mt-3">For installations</div>

- Upgrade to v9.1: faster matching and job insertion, time-left fixes (v9.1.21), security patches.
- Multi-architecture images: #8456, soon.

</div>
<div>

<div class="dx-eyebrow">For DiracX</div>

- No jobs: parcels. The JobDB in DiracX only tests deployments, then goes.
- The DiracX WMS is not a priority; it will get a plan when needed.
- CWL describes everything that runs.
- Matcher: Redis numbers, then an ADR. interCEde: ADRs close to merge. Pilots: not started.

<div class="dx-eyebrow mt-3">We need you</div>

- Owners for the job wrapper.

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
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC, The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX, The Interware" />
</div>
