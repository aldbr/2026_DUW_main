---
theme: default
title: "Workload Management"
info: |
  ## Workload Management: DIRAC and DiracX as compute backends. DIRAC(X) Users' Workshop 12
  Alexandre F. Boyer (CERN).
  13–16 October 2026, FZU Prague. Wed 14 Oct, 12:10 (30 min slot).
colorSchema: light
class: text-left
layout: default
transition: slide-left
mdc: true
fonts:
  sans: 'IBM Plex Sans'
  serif: 'Playfair Display'
  mono: 'IBM Plex Mono'
  weights: '400,500,600,700,800'
  italic: true
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

<img :src="'/figures/fig-backends3d.svg'" alt="The DiracX transformation system dispatches parcels to compute backends: DIRAC, DiracX pull and DiracX push to come, and HTCondor; each keeps its own data" style="width:72%;margin:-.8rem auto 0;display:block" />

<div class="dx-key mt-1">The transformation system (Tuesday's talks) sends parcels to compute backends. <b>DIRAC is one of them</b>, with its own data, as it is; DiracX may add a pull and a push backend later.</div>

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

### No rush for DiracX compute backend(s)
Most communities can rely on their existing WMS for now: DIRAC, or their own (see the <a href="https://indico.cern.ch/event/1588323/contributions/7264642/" target="_blank">CMS talk</a> just before).

</div>

</div>

<div class="dx-key mt-3">The DiracX WMS is not a priority. It will move slowly, in parallel, and get a plan when the transformation system needs a native backend.</div>

---
layout: section
---

# 2 · DIRAC: fixes and performance

Several fixes made it faster and more reliable, for v9 and above. A walk along the path.

---

<div class="duw-sec">2 · DIRAC · stop 1 of 6</div>

# Submitting a job

<div class="duw-stop">

<img :src="'/figures/fig-stop-1.svg'" alt="The DIRAC WMS path with JobManager, SandboxStore, JobDB, the optimizers and TaskQueueDB highlighted" />

<div>

<div class="duw-stopsec fast"><h4>Faster</h4>

- Jobs reach their task queue at ~190 jobs/s, not ~115; one queue instead of 64 duplicates during a burst (<a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>, v9.1.20).
- Missing index on job names (<a href="https://github.com/DIRACGrid/DIRAC/pull/8463" target="_blank">#8463</a>, v9.1.0, manual `ALTER TABLE`); database objects reused by the optimizers and agents (<a href="https://github.com/DIRACGrid/DIRAC/pull/8457" target="_blank">#8457</a>).

</div>
<div class="duw-stopsec rel"><h4>More reliable</h4>

- A task queue could briefly lose its site restriction: a pilot at any site could then match jobs meant for other sites (<a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>).

</div>
<div class="duw-stopsec safe"><h4>Safer</h4>

- Sandbox store: a file name ending in `../` could write anywhere the service user can (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-pwvr-x92w-xmp8" target="_blank">GHSA-pwvr</a>).
- SQL parameterised in JobDB, TaskQueueDB and the sandbox metadata (v9.1.13 to v9.1.15).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 2 of 6</div>

# Sending pilots

<div class="duw-stop">

<img :src="'/figures/fig-stop-2.svg'" alt="The DIRAC WMS path with SiteDirector, PilotManager, PilotAgentsDB and the CE highlighted" />

<div>

<div class="duw-stopsec fast"><h4>Faster</h4>

- Indices for counting pilots per site and queue (<a href="https://github.com/DIRACGrid/DIRAC/pull/8463" target="_blank">#8463</a>); fewer calls in the pilot agents and the PilotManager (<a href="https://github.com/DIRACGrid/DIRAC/pull/8569" target="_blank">#8569</a>, <a href="https://github.com/DIRACGrid/DIRAC/pull/8624" target="_blank">#8624</a>).

</div>
<div class="duw-stopsec rel"><h4>More reliable</h4>

- The SiteDirector no longer submits to banned CEs (<a href="https://github.com/DIRACGrid/DIRAC/pull/8340" target="_blank">#8340</a>, v9.0.2).
- HPC: the SSH computing element, rewritten on Fabric, submits through a login node to the batch system (<a href="https://github.com/DIRACGrid/DIRAC/pull/7703" target="_blank">#7703</a>, v9.0) <span class="duw-was">DUW11</span>.

</div>
<div class="duw-stopsec safe"><h4>Safer</h4>

- PilotManager: SQL injection and missing access checks (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-7xw9-549r-8jrc" target="_blank">GHSA-7xw9</a>, fixed in v9.1.10, v9.0.22).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 3 of 6</div>

# The pilot on the node

<div class="duw-stop">

<img :src="'/figures/fig-stop-3.svg'" alt="The DIRAC WMS path with the pilot highlighted on the worker node" />

<div>

<div class="duw-stopsec rel"><h4>More reliable</h4>

- Python 3 only (<a href="https://github.com/DIRACGrid/Pilot/pull/268" target="_blank">Pilot #268</a>) <span class="duw-was">DUW11</span>.
- The pilot reads the time left once and writes it to its configuration; jobs read it there, even in containers (<a href="https://github.com/DIRACGrid/DIRAC/pull/8479" target="_blank">#8479</a>, v9.1.4).
- One image for every architecture: next slide.

</div>
<div class="duw-stopsec safe"><h4>Safer</h4>

- The pilot code was fetched over HTTPS without checking the certificate, then run (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vg99-gr89-qhw9" target="_blank">GHSA-vg99</a>, fixed in v9.1.10, v9.0.22).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 3, zoom</div>

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

<div class="duw-sec">2 · DIRAC · stop 4 of 6</div>

# Matching

<div class="duw-stop">

<img :src="'/figures/fig-stop-4.svg'" alt="The DIRAC WMS path with the Matcher and TaskQueueDB highlighted" />

<div>

<div class="duw-stopsec fast"><h4>Faster</h4>

- Matching query: ~30 ms to ~3 ms (<a href="https://github.com/DIRACGrid/DIRAC/pull/8462" target="_blank">#8462</a>, v9.1.0).
- Finding the matching task queues among 323: 3.4 s to 0.2 s (<a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>, v9.1.20).
- The delay between two matches of one job type can be below a second (<a href="https://github.com/DIRACGrid/DIRAC/pull/8711" target="_blank">#8711</a>, v9.1.16).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 5 of 6</div>

# The JobAgent

<div class="duw-stop">

<img :src="'/figures/fig-stop-5.svg'" alt="The DIRAC WMS path with the JobAgent highlighted on the worker node" />

<div>

<div class="duw-stopsec rel"><h4>More reliable</h4>

- A job rescheduled after an early failure could already run elsewhere when the JobAgent, minutes later, marked it Failed (<a href="https://github.com/DIRACGrid/DIRAC/pull/8441" target="_blank">#8441</a>, v9.0.17).
- Memory counts when matching and when filling a multi-core slot (<a href="https://github.com/DIRACGrid/DIRAC/pull/8366" target="_blank">#8366</a>, <a href="https://github.com/DIRACGrid/DIRAC/pull/8414" target="_blank">#8414</a>); cgroup2 keeps each job within its CPU and memory share (<a href="https://github.com/DIRACGrid/DIRAC/pull/8110" target="_blank">#8110</a>) <span class="duw-was">DUW11</span>.
- The margin for uploads is reserved before matching (<a href="https://github.com/DIRACGrid/DIRAC/pull/8746" target="_blank">#8746</a>, v9.1.21).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 6 of 6</div>

# The JobWrapper and its reports

<div class="duw-stop">

<img :src="'/figures/fig-stop-6.svg'" alt="The DIRAC WMS path with the JobWrapper, JobStateUpdate and pilot logging highlighted" />

<div>

<div class="duw-stopsec rel"><h4>More reliable</h4>

- Jobs shorter than the first Watchdog cycle reported NaN: invalid JSON, so DiracX rejected the whole update (<a href="https://github.com/DIRACGrid/DIRAC/pull/8750" target="_blank">#8750</a>, v9.1.16).
- Graceful stop and the reason of a kill: next slides (<a href="https://github.com/DIRACGrid/DIRAC/pull/8814" target="_blank">#8814</a>, <a href="https://github.com/DIRACGrid/DIRAC/pull/8528" target="_blank">#8528</a>).

</div>
<div class="duw-stopsec safe"><h4>Safer</h4>

- Job state updates: any user could change any job's owner or status (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-j3xg-cjx8-qjpw" target="_blank">GHSA-j3xg</a>).
- Pilot logging: a crafted file name could read any file on the server (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vm3r-6cmw-8p5v" target="_blank">GHSA-vm3r</a>).
- Both fixed in v9.1.20, v9.0.26, v8.0.85.

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 6, zoom</div>

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

<div class="duw-sec">2 · DIRAC · stop 6, zoom</div>

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

<div class="dx-key mt-2">DIRAC is patched, not developed: upgrading is how you get these. Time-left fixes in <b>v9.1.21</b> only. Details: "Allocated time management" in the Administrator Guide. CPU work is normalised with DB12: <a href="https://indico.cern.ch/event/1588323/contributions/7264656/" target="_blank">next talk</a>.</div>

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

# Proofs of concept around the DiracX backends

<img class="duw-pocfig" :src="'/figures/fig-pocmap.svg'" alt="From a parcel to a worker node: CWL describes the payload; DiracX pull (with pilot management) and DiracX push may share a matcher; interCEde talks to the CEs, and the job wrapper runs the payload on the worker node; all five are proofs of concept" style="max-height:14rem;width:86%" />

<div class="duw-poc5">
<div><h4>CWL</h4>ADR in draft; implemented with the transformation system</div>
<div><h4>interCEde</h4>ADRs in review; core proposed; integration tests</div>
<div><h4>Matcher</h4>Python baseline and load tests; Redis next; maybe shared by pull and push</div>
<div><h4>Pilot management</h4>for DiracX pull; ported as is, then paused</div>
<div><h4>Job wrapper</h4>gathering requirements</div>
</div>

<div class="duw-ask"><b>The same path for each</b>: explore, write an ADR, then implement in DiracX. Each is tested in small increments you can try.</div>

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
