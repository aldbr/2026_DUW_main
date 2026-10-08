---
theme: default
title: "Workload Management: DIRAC v9 and the way to DiracX"
info: |
  ## Workload Management: DIRAC v9 and the way to DiracX. DIRAC(X) Users' Workshop 12
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

# Workload Management: DIRAC v9 and the way to DiracX

<span class="dx-author">Alexandre F. Boyer</span> · CERN

12th DIRAC(X) Users' Workshop · FZU Prague · 13–16 October 2026

<div class="dx-logobar mt-10">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC, The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX, The Interware" />
</div>

---

# One year after the last workshop

<div class="duw-small mb-1">What the DUW11 WMS talk said would come next</div>

<table class="duw-map">
<thead><tr><th>Announced in 2025</th><th>Where it is</th><th></th></tr></thead>
<tbody>
<tr><td>SSH computing element on Fabric</td><td>done</td><td>DIRAC #7703, v9.0</td></tr>
<tr><td>CPU and memory limits with cgroup2</td><td>done</td><td>#8110, plus memory-aware matching (#8366, #8414)</td></tr>
<tr><td>Python 2 out of the pilot</td><td>done</td><td>Pilot #268, Nov 2025</td></tr>
<tr><td>Multi-architecture images from CVMFS</td><td>pull request open</td><td>DIRAC #8456, to certify</td></tr>
<tr><td>Pilots managed by DiracX</td><td>started, then paused</td><td>pilot database and router in DiracX (#570)</td></tr>
<tr><td>CWL job submission in DiracX</td><td>redirected</td><td>now part of the transformation system ADRs</td></tr>
<tr><td>Job monitoring and job manager in DiracX</td><td>stopped</td><td>no central JobDB in DiracX: section 4</td></tr>
<tr><td>A decision on DB12</td><td>open</td><td>DB12 #15, #16</td></tr>
</tbody>
</table>

<div class="dx-key mt-3">Most of what was planned for DIRAC landed. The DiracX part changed direction, for a reason explained in section 4.</div>

---
layout: section
---

# 1 · Resources and interfaces

What we run on, and how we reach it

---

<div class="duw-sec">1 · Resources and interfaces</div>

# Resources keep diversifying

<img :src="'/figures/fig-landscape.svg'" alt="Grid sites, HPC centres and clouds, with x86_64, aarch64 and GPUs, reached through DIRAC computing elements or, later, interCEde; the DIRAC WMS and DiracX on top" style="width:58%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- Grid, HPC and clouds, now with **aarch64** and GPUs beside x86_64.
- HPC centres often have no outbound network and no CVMFS.

</div>
<div>

- DIRAC v9 dropped the CREAM, ARC, ARC6 and BOINC CEs; AREX is the ARC interface, with tokens.
- One computing element interface per DIRAC installation today: no sharing with other WMSs.

</div>
</div>

---

<div class="duw-sec">1 · Resources and interfaces</div>

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

<div class="duw-small mt-3">Contributions from several communities; the HTCondor grid universe through a local schedd is deferred, not adopted.</div>

---
layout: section
---

# 2 · The DIRAC WMS since v9

Faster, more reliable, and the same two models

---

<div class="duw-sec">2 · The DIRAC WMS since v9</div>

# Two models, unchanged

<img :src="'/figures/fig-pullpush.svg'" alt="Pull: the SiteDirector submits pilots through a CE; the pilot's JobAgent asks the Matcher for a job and runs it in the JobWrapper. Push: the PushJobAgent asks the Matcher and submits the JobWrapper to an HPC node without outbound network" style="width:66%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- **Pull**: one SiteDirector per VO, CEs handled in parallel.
- **Push**: for nodes that cannot reach DIRAC; pre- and post-processing stay with the agent.

</div>
<div>

- The changes since v9 are inside the boxes: the task queues, the Matcher, the JobAgent and the JobWrapper.

</div>
</div>

---

<div class="duw-sec">2 · The DIRAC WMS since v9</div>

# Faster

<table class="duw-stat">
<thead><tr><th>Measured on production-sized databases</th><th>before</th><th>after</th><th>release</th></tr></thead>
<tbody>
<tr><td>Task queue matching query</td><td>~30 ms</td><td><b>~3 ms</b></td><td>v9.1.0 · #8462</td></tr>
<tr><td>Finding matching task queues (323 queues)</td><td>3.4 s</td><td><b>0.2 s</b></td><td>v9.1.20 · #8801</td></tr>
<tr><td>Job insertion</td><td>~115 jobs/s</td><td><b>~190 jobs/s</b></td><td>v9.1.20 · #8801</td></tr>
<tr><td>Duplicate task queues during a burst</td><td>64</td><td><b>1</b></td><td>v9.1.20 · #8801</td></tr>
<tr><td>Delay between matches, per job type</td><td>1 s or more</td><td><b>sub-second</b></td><td>v9.1.16 · #8711</td></tr>
</tbody>
</table>

<div class="dx-tight mt-2">

- Also: missing indices on pilots and jobs (#8463, manual `ALTER TABLE`), hot paths found with py-spy (#8524), fewer calls in the pilot agents (#8569, #8624).

</div>

<div class="dx-key mt-2">Several fixes made the DIRAC WMS faster and more reliable, for installations at v9 and above. Most of the numbers above need v9.1.</div>

---

<div class="duw-sec">2 · The DIRAC WMS since v9</div>

# More reliable, safer, simpler

<div class="duw-three3">

<div class="dx-card dx-card-blue">

### Reliable
- Task queues no longer lose their site, platform or tag restrictions under concurrency (#8801).
- Memory-aware matching; cgroup2 limits in containers (#8366, #8414, #8110).
- Banned CEs skipped; rescheduled jobs not failed; no NaN parameters (#8340, #8441, #8750).

</div>

<div class="dx-card dx-card-blue">

### Safer
- SQL parameterised in every WMS database (v9.1.13 to v9.1.15).
- Five WMS advisories fixed: job state access, sandbox store, pilot logging, pilot manager, pilot download.
- Patched in v9.1.20, v9.0.26, v8.0.85.

</div>

<div class="dx-card dx-card-legacy">

### Simpler
- Removed: CREAM, ARC, ARC6, BOINC CEs; pilot bundles; private pilots; Python 2 in the pilot.
- Tokens: pilots submitted with tokens in multi-VO setups; proxy pilots also carry one.

</div>

</div>

<div class="dx-concludes mt-3"><carbon-arrow-right class="dx-concludes-arrow" /><span>DIRAC is patched, not developed: <strong>upgrading is how you get these</strong></span></div>

---

<div class="duw-sec">2 · The DIRAC WMS since v9</div>

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

<img :src="'/figures/fig-slot.svg'" alt="A slot split into pilot, payload and StopMargin; the margin is reserved before matching, a stop signal ends the payload cleanly, and a killed job reports why" style="width:56%;margin:0 auto;display:block" />

<div class="dx-key mt-1">The three fixes above are in <b>v9.1.21</b> only. Set the <code>StopSig*</code> options in the CS or per job; see "Allocated time management" in the Administrator Guide.</div>

---

<div class="duw-sec">2 · The DIRAC WMS since v9</div>

# Multi-architecture: one image name, every architecture

<div class="duw-two">
<div>

**DIRAC #8456** (pull request open)
- The pilot detects the node's architecture and resolves the container image under the CVMFS `.multiarch` layout: `<base>/<arch>/<image>`.
- Used by the Singularity CE and `dirac-apptainer-exec`; falls back to `ContainerRoot`.
- Left to do: certify against `unpacked.cern.ch`, review, merge.

</div>
<div>

**What a community needs**
- Images published as multi-architecture (OCI index) images; otherwise the layout has dangling links.
- Platform tags in the pilot's architecture script.

**Not solved yet**: a job that can run on x86_64 *or* aarch64 has a single set of requirements in today's matcher. Section 3.

</div>
</div>

<div class="dx-key mt-3">The same job description on any architecture, without per-architecture configuration.</div>

---
layout: section
---

# 3 · Proofs of concept

Matching, and the pilot

---

<div class="duw-sec">3 · Proofs of concept</div>

# A matcher for DiracX

<div class="duw-two">
<div>

**Goal** (diracx #843): match pilots to jobs at **1 kHz** (200 Hz at least), with 10 million waiting jobs per VO. Redis holds an index that can be rebuilt from the database.

**Built**: matching with tag expressions, prioritisation, a benchmark harness, a Redis data model (release 0.4.0, Sep 2026).

**Measured**: the pure Python baseline only, 210 ms per match at 50k candidate jobs, 5.7 s at 750k. No Redis numbers yet.

</div>
<div>

**What we learned**
- Real requirements vary little: LHCb has 872k waiting jobs but 14 distinct (CPU time, group) pairs. Group jobs by profile, as task queues do; do not test them one by one.
- A job eligible at ~49 sites must not be stored 49 times.
- A job runnable on two architectures needs a *list* of requirements.

</div>
</div>

<div class="dx-card dx-card-new mt-3" style="height:auto">

**Next**: matching inside Redis (Lua) and its benchmark on realistic data (#873), then scale tests (#874). **Then an ADR**, written from those numbers, for the matcher of the `diracx-pilot` backend.

</div>

---

<div class="duw-sec">3 · Proofs of concept</div>

# Pilots: the re-thinking has not started

<div class="duw-three3">

<div class="dx-card dx-card-new">

### Landed
- A pilot database and router in DiracX (#570, Aug 2026).
- Pilot: Python 2 removed; maintenance fixes.

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
layout: section
---

# 4 · DiracX: the WMS follows the transformation system

No JobDB at the centre, CWL everywhere

---

<div class="duw-sec">4 · DiracX</div>

# Work is a parcel, dispatched to a backend

<img :src="'/figures/fig-parcels.svg'" alt="User jobs and workgraphs, both CWL, become parcels; a dispatcher hands each parcel to a backend: legacy-dirac (the DIRAC WMS), diracx-pilot (to be designed), htcondor, diracx-remote" style="width:64%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.1rem">
<div>

- DiracX has no "Systems". The transformation system ADRs cover productions, transformations **and the job part of the WMS**: user jobs are parcels too.

</div>
<div>

- First, every parcel goes to DIRAC. A native WMS backend comes when the transformation system needs it: **there will be a WMS plan**, not yet.

</div>
</div>

---

<div class="duw-sec">4 · DiracX</div>

# No JobDB at the centre

<div class="duw-two">
<div>

**In DIRAC**, the JobDB was the first database, and every system reads or writes it.

**In DiracX**, the record of work is the **parcel**. A jobs table, if any, would be private to the WMS backend (`diracx-pilot`), like any backend's own state.

</div>
<div>

**The JobDB already in DiracX stays**, with a narrow use:
- job status updates from DIRAC, through the future client;
- load-testing a new installation, and checking it is deployed correctly.

We do not port the rest of job management (monitoring, manager) to it.

</div>
</div>

<div class="dx-key mt-3">The DiracX WMS will evolve slowly, in parallel, until the transformation system needs a native backend.</div>

---

<div class="duw-sec">4 · DiracX</div>

# CWL describes all the work

<div class="duw-two">
<div>

**One format** (DX-ADR-007, draft): a user job, a workgraph and each transformation are CWL v1.2 documents.

- DiracX settings are **hints** under `dirac:`, never requirements: every document stays plain, runnable CWL.
- The same document runs with `cwltool`, locally against grid data, and at scale.
- Processes are resolved before dispatch: the node runs without fetching definitions.

</div>
<div>

**What this means for the WMS**
- Matching requirements come from the hints.
- The job wrapper resolves inputs (`lfn:`, `sandbox:`), captures the output sandbox, and writes a status report per input.
- Outputs are registered by DiracX after the parcel ends, not by the wrapper.

**Today**: `dirac-cwl` 1.3.0; an experimental CWL job wrapper in DIRAC (#8425).

</div>
</div>

---

<div class="duw-sec">4 · DiracX</div>

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

<div class="dx-eyebrow">For installations</div>

- Upgrade to v9.1: faster matching and job insertion, time-left fixes (v9.1.21), security patches.
- Multi-architecture images: #8456, soon.

<div class="dx-eyebrow mt-3">Proofs of concept</div>

- Matcher: Redis numbers next, then an ADR.
- interCEde: ADRs close to merge, core in progress.
- Pilots: re-thinking not started.

</div>
<div>

<div class="dx-eyebrow">For DiracX</div>

- The transformation system comes first; the WMS follows when it is needed.
- No JobDB at the centre: work is a parcel.
- CWL describes everything that runs.

<div class="dx-eyebrow mt-3">We need you</div>

- Owners for the job wrapper: requirements, priorities, acceptance.

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
