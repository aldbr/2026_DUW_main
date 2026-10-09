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
layout: section
---

# 1 · Starting from the transformation system

What it changes for workload management

---

<div class="duw-sec">1 · Starting from the transformation system</div>

# From porting services to compute backends

<img :src="'/figures/fig-backends.svg'" alt="Before: DIRAC WMS services ported one by one to DiracX over the same databases; only JobStateUpdate was ported. Now: the DiracX transformation system dispatches parcels to separate backends, the DIRAC WMS, a later DiracX WMS, and HTCondor, each with its own data" style="width:74%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- **Before**: move each DIRAC service and agent to DiracX, over the same databases and the same data model.

</div>
<div>

- **Now**: the transformation system (Tuesday's talks) sends parcels to **compute backends**. The DIRAC WMS is one of them.

</div>
</div>

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

<div class="duw-sec">1 · Starting from the transformation system</div>

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
<tr><td>CWL job submission in DiracX</td><td>redirected</td><td>part of the transformation system</td></tr>
<tr><td>Job monitoring and job manager in DiracX</td><td>dropped</td><td>no jobs in DiracX: section 3</td></tr>
<tr><td>A decision on DB12</td><td>open</td><td><a href="https://indico.cern.ch/event/1588323/contributions/7264656/" target="_blank">next talk</a></td></tr>
</tbody>
</table>

<div class="dx-key mt-3">The DIRAC items landed, as fixes. The DiracX items changed with the backend model.</div>

---
layout: section
---

# 2 · DIRAC: fixes and performance

What keeps it running while we migrate

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Resources keep diversifying

<img :src="'/figures/fig-landscape.svg'" alt="Grid sites, HPC centres and clouds, with x86_64, aarch64 and GPUs, reached through DIRAC computing elements or, later, interCEde; the DIRAC WMS and DiracX on top" style="width:58%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- Grid, HPC and clouds, now with **aarch64** and GPUs beside x86_64.
- HPC centres often have no outbound network and no CVMFS.

</div>
<div>

- DIRAC has to keep up, without new features: what follows are **fixes and performance improvements**.
- v9 dropped the CREAM, ARC, ARC6 and BOINC CEs; AREX is the ARC interface, with tokens.

</div>
</div>

---

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

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

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# More reliable, safer, simpler

<div class="duw-three3">

<div class="dx-card dx-card-blue">

### Reliable
- Task queues no longer lose their site, platform or tag restrictions under concurrency (#8801).
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

<div class="duw-sec">2 · DIRAC: fixes and performance</div>

# Heterogeneous nodes: architectures and limits

<div class="duw-two">
<div>

**aarch64 beside x86_64** (DIRAC #8456, pull request open)
- The pilot detects the node's architecture and resolves the container image under the CVMFS `.multiarch` layout: `<base>/<arch>/<image>`.
- Used by the Singularity CE and `dirac-apptainer-exec`; falls back to `ContainerRoot`.
- Communities publish multi-architecture (OCI index) images.
- Left to do: certify against `unpacked.cern.ch`, review, merge.

</div>
<div>

**CPU and memory limits**
- cgroup2 limits for jobs in containers (#8110).
- Memory taken into account when matching and when filling a multi-core slot (#8366, #8414).

**Not solved in DIRAC**: a job that can run on x86_64 *or* aarch64 has a single set of requirements.

</div>
</div>

<div class="dx-key mt-3">Fixes to run on the nodes sites now provide, not a new model: the same job description, on any architecture.</div>

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

<img :src="'/figures/fig-slot.svg'" alt="A slot split into pilot, payload and StopMargin; the margin is reserved before matching, a stop signal ends the payload cleanly, and a killed job reports why" style="width:56%;margin:0 auto;display:block" />

<div class="dx-key mt-1">The three fixes above are in <b>v9.1.21</b> only. Set the <code>StopSig*</code> options in the CS or per job; see "Allocated time management" in the Administrator Guide.</div>

---
layout: section
---

# 3 · DiracX: parcels, not jobs

And the proofs of concept around the future WMS

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# No jobs in DiracX

<img :src="'/figures/fig-parcels-only.svg'" alt="User jobs and workgraphs, both CWL, become parcels, the record of work, which a dispatcher sends to a backend; the JobDB in DiracX is legacy, used only to test deployments and deleted once everyone is on DiracX" style="width:82%;margin:0 auto;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- A user job is a parcel, like a bundle of transformation inputs. A failed parcel is final: resubmitting creates a new one.
- A jobs table, if the DiracX WMS needs one, stays private to that backend.

</div>
<div>

- The JobDB in DiracX today only receives job status updates from DIRAC, to **test that a DiracX deployment works**.
- We do not port job monitoring or the job manager. **Once everyone is on DiracX, it is deleted.**

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

**Today**: `dirac-cwl` 1.3.0; an experimental CWL job wrapper in DIRAC (#8425).

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
