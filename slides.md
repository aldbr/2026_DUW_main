---
theme: default
title: "Workload Management"
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

# Workload Management

<div class="duw-subtitle">DIRAC and DiracX as compute backends</div>

<span class="dx-author">Alexandre F. Boyer</span> · CERN

12th DIRAC(X) Users' Workshop · FZU Prague · 13–16 October 2026

<div class="dx-logobar mt-10">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC, The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX, The Interware" />
</div>

---

# ARM and GPUs are spreading

<div style="display:grid;grid-template-columns:2.3fr 1fr;gap:1rem;align-items:center;margin-top:.6rem">

<img :src="'/figures/fig-worldmap.svg'" alt="World map of ARM and GPU systems: TOP500 systems in the US, Europe, Asia, Australia, Brazil and Saudi Arabia, and the WLCG ARM sites at Glasgow and GridKa" style="width:100%" />

<div class="duw-stats1">
<div><b>276 / 500</b>TOP500 systems with GPUs, June 2026 (110 in 2018)</div>
<div><b>35</b>ARM systems in the TOP500 (5 in 2020)</div>
<div class="grid"><b>Our communities</b>run mostly on grid sites, and use a few HPCs opportunistically.</div>
</div>

</div>

---

# HPC and clouds see them first

<img :src="'/figures/fig-history.svg'" alt="Timeline: HPC, clouds and industry above the line (2005 multicore CPUs, 2010 first GPU system at the top of the TOP500, 2018 ARM in AWS, 2020 first ARM system at the top of the TOP500); the grid below (2023 ARM in production at Glasgow, 2025 first ARM pledges in WLCG, GPUs cannot be pledged yet)" style="width:94%;margin:.6rem auto 0;display:block" />

<div class="dx-key mt-3">The grid follows, years later: sites buy from the same market, once the experiments can use the hardware.</div>

---

# The end of two decades of homogeneity

<div class="duw-quote" style="font-size:.8rem">Sites buy from the same market as everyone else: "Hardware technology evolution now is dominated by the needs of AI" (<a href="https://indico.cern.ch/event/1678348/contributions/7172397/" target="_blank">A. Sciabà, CERN IT, July 2026</a>).</div>

<div class="duw-chain3 mt-3">
<div class="h">Why it changes</div><div class="h">What sites now offer</div><div class="h">What the WMS must do</div>

<div class="d gpu"><b>AI</b>expected productivity gains drive the market</div>
<div>GPUs, before they can be pledged or accounted</div>
<div class="w">Match on capabilities; run CPU and GPU work side by side</div>

<div class="d arm"><b>Energy and hardware cost</b>2022 energy shock, climate targets, AI-driven prices</div>
<div>ARM next to x86: first WLCG ARM pledges in 2025</div>
<div class="w">One image and one match per architecture</div>

<div class="d core"><b>More cores per node</b>clock speed stopped rising around 2005</div>
<div>Whole nodes (HPC), multicore slots (grid)</div>
<div class="w">Fill nodes, not single slots</div>

<div class="d tok"><b>Identity</b>X.509 gives way to the tokens industry uses</div>
<div>CEs that accept tokens, or only tokens</div>
<div class="w">Pilots submitted with tokens (DIRAC v8.0); DiracX built on tokens</div>
</div>

<div class="dx-key mt-3"><b>In DIRAC</b>: temporary solutions, to keep it stable. <b>In DiracX</b>: the long-term solutions, designed for this.</div>

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

<div class="duw-figside">

<img :src="'/figures/fig-path-reliable.svg'" alt="The DIRAC WMS path with TaskQueueDB, SiteDirector, Pilot, JobAgent and JobWrapper highlighted in blue" />

<div class="duw-details">

**Task queues keep their restrictions** · <a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>, v9.1.20<br/>A race could leave a task queue briefly without its site rows: a pilot at any site could then match jobs meant for other sites.

**Banned CEs skipped** · <a href="https://github.com/DIRACGrid/DIRAC/pull/8340" target="_blank">#8340</a>, v9.0.2<br/>The SiteDirector kept trying to submit pilots to banned CEs.

**Rescheduled jobs left alone** · <a href="https://github.com/DIRACGrid/DIRAC/pull/8441" target="_blank">#8441</a>, v9.0.17<br/>A job rescheduled after an early failure could already run elsewhere when the JobAgent, minutes later, marked it Failed.

**No NaN parameters** · <a href="https://github.com/DIRACGrid/DIRAC/pull/8750" target="_blank">#8750</a>, v9.1.16<br/>Jobs shorter than the first Watchdog cycle reported NaN: invalid JSON, so DiracX rejected the whole update.

**Python 3 only pilot** · <a href="https://github.com/DIRACGrid/Pilot/pull/268" target="_blank">Pilot #268</a> <span class="duw-was">DUW11</span>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Safer

<div class="duw-figside">

<img :src="'/figures/fig-path-safer.svg'" alt="The DIRAC WMS path with SandboxStore, JobStateUpdate, pilot logging, PilotManager, the pilot and the databases highlighted" />

<div class="duw-details">

**Job state updates** · <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-j3xg-cjx8-qjpw" target="_blank">GHSA-j3xg</a>, high<br/>Any authenticated user could change any job's owner, group or VO, or force its status.

**Sandbox store** · <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-pwvr-x92w-xmp8" target="_blank">GHSA-pwvr</a>, critical<br/>A file name ending in `../` could write anywhere the service user can.

**Pilot logging** · <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vm3r-6cmw-8p5v" target="_blank">GHSA-vm3r</a>, critical<br/>A crafted file name could read any file on the server.

**Pilot manager** · <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-7xw9-549r-8jrc" target="_blank">GHSA-7xw9</a>, high<br/>Parameters reached SQL unescaped, without access control.

**Pilot download** · <a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vg99-gr89-qhw9" target="_blank">GHSA-vg99</a>, high<br/>The pilot code was fetched over HTTPS without checking the certificate, then run.

<span class="duw-small">First three fixed in v9.1.20, v9.0.26, v8.0.85; last two in v9.1.10, v9.0.22. All WMS SQL parameterised in v9.1.13 to v9.1.15.</span>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# One image for every architecture

<img :src="'/figures/fig-multiarch.svg'" alt="CVMFS holds one directory per architecture under .multiarch; on an x86_64 node and on an aarch64 node the pilot reads uname -m and runs the matching copy of the same image" style="width:62%;margin:-1rem auto 0;display:block" />

<div class="duw-two dx-tight" style="font-size:.86rem">
<div>

- Sites now offer x86_64 and aarch64 nodes. A job names one container image; the pilot reads the node's architecture and runs the matching copy. <a href="https://github.com/DIRACGrid/DIRAC/pull/8456" target="_blank">#8456</a>, open, to certify <span class="duw-was">DUW11</span>.
- Publishing needs CVMFS 2.14 (DUCC 2.14.1); any CVMFS client reads the result.

</div>
<div>

- **Still missing in DIRAC: alternatives.** A job states one platform and one set of requirements. It cannot say "x86_64, or aarch64, or a GPU of type A". The DiracX matcher is designed for this.

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Sharing a node, reaching an HPC

<img :src="'/figures/fig-limits-hpc.svg'" alt="Left: one multi-core slot shared by three jobs, each inside its own cgroup2 limit; right: the SSH CE reaching an HPC login node whose batch system runs the pilots" style="width:66%;margin:-.6rem auto 0;display:block" />

<div class="duw-two dx-tight" style="font-size:.86rem">
<div>

- **CPU and memory limits** (v9.0) <span class="duw-was">DUW11</span>. Memory requests count when matching and when sharing a multi-core slot (<a href="https://github.com/DIRACGrid/DIRAC/pull/8366" target="_blank">#8366</a>, <a href="https://github.com/DIRACGrid/DIRAC/pull/8414" target="_blank">#8414</a>); cgroup2 keeps each job within its share (<a href="https://github.com/DIRACGrid/DIRAC/pull/8110" target="_blank">#8110</a>).

</div>
<div>

- **HPC through SSH** (v9.0) <span class="duw-was">DUW11</span>. The SSH computing element, rewritten on Fabric, submits through an HPC login node to its batch system (<a href="https://github.com/DIRACGrid/DIRAC/pull/7703" target="_blank">#7703</a>).

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Time left in the slot: before and after

<img :src="'/figures/fig-slot2.svg'" alt="Before: the payload is sized for the whole slot and is killed at the end, outputs lost. After: a margin is reserved before matching, a stop signal lets the payload wind down, and the uploads fit; a killed job reports why" style="width:84%;margin:.2rem auto 0;display:block" />

<div class="duw-two dx-tight mt-2" style="font-size:.88rem">
<div>

**An example**: an MC job sized for 183 events produced 150, was killed, and its output was never uploaded.

</div>
<div>

**One source of truth** since v9.1.4 (<a href="https://github.com/DIRACGrid/DIRAC/pull/8479" target="_blank">#8479</a>): the pilot reads the time left once, jobs read it from the pilot configuration, even inside containers.

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Time left in the slot: configuration

<div class="duw-two">
<div>

`/Systems/WorkloadManagement/JobWrapper`, or per job in the JDL:

```ini
StopMargin = 300            # seconds kept for the uploads
# graceful stop, off unless set; example for Gauss
StopSigRegex = ^\S*python\S*\s+\S*/gaudirun\.py\s.*/options/Gauss/
StopSigNumber = 10          # SIGUSR1
StopSigFinishWork = 16740   # CPU work to wind down
StopSigStartWork = 8370     # minimum work before stopping
```

</div>
<div class="dx-tight">

- **StopMargin** is wall clock: uploading takes the same time on any node. It is subtracted once, before matching.
- **StopSig\*** thresholds are in CPU work, divided by the node's power: one value fits slow and fast nodes.
- The application must handle the signal (Gauss: `StopOnSignal`). The Watchdog still stops it when the budget is spent.

</div>
</div>

<div class="dx-key mt-2">In <b>v9.1.21</b> only. Details: "Allocated time management" in the Administrator Guide. CPU work is normalised with DB12: <a href="https://indico.cern.ch/event/1588323/contributions/7264656/" target="_blank">next talk</a>.</div>

---
layout: section
---

# 3 · DiracX: parcels, not jobs

And the proofs of concept around the future WMS

---

<div class="duw-sec">3 · DiracX</div>

# No jobs in DiracX

<img :src="'/figures/fig-parcels-only.svg'" alt="User jobs and workgraphs, both CWL, become parcels, the record of work, which a dispatcher sends to a backend; the JobDB in DiracX is legacy, used only to test deployments and deleted once everyone is on DiracX" style="width:68%;margin:-.6rem auto 0;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- A user payload is a parcel, like a bundle of transformation inputs. A failed parcel is final: resubmitting creates a new one.
- We do not port job monitoring or the job manager <span class="duw-was">DUW11</span>.

</div>
<div>

- The JobDB in DiracX is legacy. It receives job status updates from DIRAC, to **test that a DiracX deployment works**.
- It also feeds the **dummy job executor** (<a href="https://github.com/diracgrid/diracx/pull/995" target="_blank">diracx#995</a>): jobs go `Waiting → Matched → Running → Done` without running anything. A stand-in backend, to test the transformation system end to end.
- **Once everyone is on DiracX, it is deleted.**

</div>
</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# CWL describes all the work

<img :src="'/logos/cwl.svg'" alt="Common Workflow Language logo" style="position:absolute;top:2.5rem;right:2.6rem;height:2.4rem" />

<div class="duw-pocfig duw-code">

```yaml
cwlVersion: v1.2
class: CommandLineTool
$namespaces: {dirac: https://diracgrid.org/cwl#}
hints:
  dirac:Job: {}       # a user payload (draft syntax)
baseCommand: [python, fit.py]
inputs:
  data: {type: File, inputBinding: {position: 1}}   # lfn:/... on the grid
outputs:
  plots: {type: File, outputBinding: {glob: "*.png"}}
```

</div>

<div class="duw-poc3">
<div><h4>Why</h4>

One format for a user payload, a workgraph and each transformation. DiracX settings are `dirac:` hints: the same document runs on a laptop and at scale.

</div>
<div><h4>Where it stands</h4>

DX-ADR-007, draft. `dirac-cwl` 1.3.0; an experimental CWL wrapper in DIRAC (#8425). Upstream: <a href="https://github.com/common-workflow-language/cwltool/pull/2302" target="_blank">cwltool#2302</a>, <a href="https://github.com/common-workflow-language/cwltool/pull/2166" target="_blank">#2166</a>, <a href="https://github.com/common-workflow-language/schema_salad/pull/1064" target="_blank">schema_salad#1064</a> merged; <a href="https://github.com/common-workflow-language/cwl-utils/pull/446" target="_blank">cwl-utils#446</a> in review.

</div>
<div><h4>Next</h4>

Implemented with the transformation system, from this week's hackathon.

</div>
</div>

<div class="duw-ask"><b>From you</b>: convert one of your workflows (yesterday's hands-on) and tell us what CWL cannot express.</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# interCEde: computing elements, explored from use cases

<img class="duw-pocfig" :src="'/figures/fig-intercede.svg'" alt="Communities send requirements to interCEde and test its increments; interCEde is tested against real HTCondor, ARC and Slurm CEs, then released to DiracX, where a WMS backend uses it" />

<div class="duw-poc3">
<div><h4>Why</h4>

Talking to CEs is needed by every WMS. Explored from the use cases DIRAC covers, and those it does not but should.

</div>
<div><h4>Where it stands</h4>

ADRs under review; core contract proposed (#27). Its own repository: integration tests against real CEs, so a change cannot break production.

</div>
<div><h4>Next</h4>

Increments you can test. The ADRs are merged once a first implementation works.

</div>
</div>

<div class="duw-ask"><b>From you</b>: if you use DIRAC computing elements, test the increments of <a href="https://github.com/DIRACGrid/intercede" target="_blank">interCEde</a> and report what does not fit, in an issue or at a DOps.</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# A matcher for the DiracX WMS

<img class="duw-pocfig" :src="'/figures/fig-matcher.svg'" alt="A pilot sends its node description; the POC matcher takes all waiting jobs, matches them against the node, filters them using the configuration and the running jobs, ranks them by fair share using the running jobs, and hands one job to the pilot" />

<div class="duw-poc3">
<div><h4>Why</h4>

DIRAC's matcher will not be fast enough for what is coming (e.g. LHCb), and cannot express alternatives: GPU A, or GPU B, or CPU C.

</div>
<div><h4>Where it stands</h4>

A deliberately simple Python matcher (<a href="https://github.com/devlink42/poc-dirac-job-matchmaking" target="_blank">POC</a>), and load tests on LHCb-shaped data: 210 ms per match at 50k candidates.

</div>
<div><h4>Next</h4>

Redis, measured against this baseline, easy to rebuild (chaos tests with Redis off). Then an ADR, then DiracX.

</div>
</div>

<div class="duw-ask"><b>From you</b>: the requirements your jobs cannot express today.</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# Pilot management: port paused

<img class="duw-pocfig" :src="'/figures/fig-pilots.svg'" alt="DIRAC pilot management ported as is to a DiracX pilot database and router, then paused; what comes next is a question mark, to be re-thought with the DiracX WMS" />

<div class="duw-poc3">
<div><h4>Why</h4>

Pilots belong to the DiracX WMS backend, which comes after the transformation system.

</div>
<div><h4>Where it stands</h4>

Pilot database and router ported as is (<a href="https://github.com/DIRACGrid/diracx/pull/570" target="_blank">diracx#570</a>) <span class="duw-was">DUW11</span>. The data model could be much better, and changing it would mean large changes in DIRAC: paused.

</div>
<div><h4>Next</h4>

Re-thought with the DiracX WMS backend. Meanwhile the DIRAC pilot keeps being patched.

</div>
</div>

<div class="duw-ask"><b>From you</b>: what you need from pilots: identity, logging, push or pull.</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# The job wrapper: one for all of us

<img class="duw-pocfig" :src="'/figures/fig-wrappers.svg'" alt="Today: the DIRAC JobWrapper, the dirac-cwl wrapper and DiracX executor prototypes, each with community steps around them; to build: one job wrapper for all, still a question mark" />

<div class="duw-poc3">
<div><h4>Why</h4>

Several wrappers today, and each community adds its own steps around the payload.

</div>
<div><h4>Where it stands</h4>

Requirements to gather: inputs, time left and graceful stop, containers, nodes without outbound network, reporting, failed uploads.

</div>
<div><h4>Next</h4>

A proof of concept, then an ADR.

</div>
</div>

<div class="duw-ask"><b>From you</b>: someone to gather requirements and feedback, build the proof of concept, then design the ADR, with someone who has done it once.</div>

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
- interCEde and the matcher: exploratory, with tests; ADRs after a first implementation. Pilot management: paused.

<div class="dx-eyebrow mt-3">We need you</div>

- Someone to lead the job wrapper requirements and proof of concept; your requirements for interCEde and the matcher.

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
