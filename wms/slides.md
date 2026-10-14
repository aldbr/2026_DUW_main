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

# The end of two decades of homogeneity

<div class="duw-quote" style="font-size:.8rem">Sites buy from the same market as everyone else: "Hardware technology evolution now is dominated by the needs of AI" (<a href="https://indico.cern.ch/event/1678348/contributions/7172397/" target="_blank">A. Sciabà, CERN IT, July 2026</a>).</div>

<div class="duw-chain3 mt-3">
<div class="h">Why it changes</div><div class="h">What sites now offer</div><div class="h">What the WMS must do</div>

<div class="d gpu"><b>AI</b>expected productivity gains drive the market</div>
<div>GPUs, before they can be pledged or accounted</div>
<div class="w">Match on capabilities; run CPU and GPU work side by side</div>

<div class="d arm"><b>Energy and hardware cost</b>2022 energy shock, climate targets, AI-driven prices</div>
<div>ARM next to x86: first WLCG ARM pledges in 2025</div>
<div class="w">One image name for every architecture; send each job to a node it can run on</div>

<div class="d tok"><b>Identity</b>X.509 gives way to the tokens industry uses</div>
<div>CEs that accept tokens; site accounting that still reads X.509 proxies</div>
<div class="w">Pilots carry a token <i>and</i> a proxy (DIRAC, stop 2); DiracX built on tokens</div>
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

<div class="dx-key mt-1">The transformation system (Tuesday's talks) sends parcels to compute backends. <b>DIRAC is one of them</b>: it keeps its data, and gets fixes and performance only. DiracX is free of DIRAC's job model and <b>will get its own backends</b> (pull, push): not a priority, most communities rely on DIRAC or their own WMS for now (<a href="https://indico.cern.ch/event/1588323/contributions/7264642/" target="_blank">CMS talk</a>).</div>

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

<div class="duw-headline">Jobs reach their task queue 1.6× faster, and only match where they should.</div>

<div v-click class="duw-stopsec fast"><h4>Faster</h4>

- Jobs reach their task queue at ~190 jobs/s, not ~115; one queue instead of 64 duplicates during a burst (<a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>, v9.1.20).
- Missing index on job names (<a href="https://github.com/DIRACGrid/DIRAC/pull/8463" target="_blank">#8463</a>, v9.1.0, manual `ALTER TABLE`).

</div>
<div v-click class="duw-stopsec rel"><h4>More reliable</h4>

- A task queue could briefly lose its site restriction: a pilot at any site could then match jobs meant for other sites (<a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>).

</div>
<div v-click class="duw-stopsec safe"><h4>Safer</h4>

- Sandbox store: a file name ending in `../` could write anywhere the service user can (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-pwvr-x92w-xmp8" target="_blank">GHSA-pwvr</a>, fixed in v9.1.20, v9.0.26, v8.0.85).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 2 of 6</div>

# Sending pilots

<div class="duw-stop">

<img :src="'/figures/fig-stop-2.svg'" alt="The DIRAC WMS path with SiteDirector, PilotManager, PilotAgentsDB and the CE highlighted" />

<div>

<div class="duw-headline">Pilots only go where they can run.</div>

<div v-click class="duw-stopsec fast"><h4>Faster</h4>

- Indices for counting pilots per site and queue (<a href="https://github.com/DIRACGrid/DIRAC/pull/8463" target="_blank">#8463</a>, manual `ALTER TABLE`).

</div>
<div v-click class="duw-stopsec rel"><h4>More reliable</h4>

- The SiteDirector no longer submits to banned CEs (<a href="https://github.com/DIRACGrid/DIRAC/pull/8340" target="_blank">#8340</a>, v9.0.2).
- HPC: the SSH computing element, rewritten on Fabric, submits through a login node to the batch system (<a href="https://github.com/DIRACGrid/DIRAC/pull/7703" target="_blank">#7703</a>, v9.1.3) <span class="duw-was">DUW11</span>.

</div>
<div v-click class="duw-stopsec safe"><h4>Safer</h4>

- PilotManager: SQL injection and missing access checks (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-7xw9-549r-8jrc" target="_blank">GHSA-7xw9</a>, fixed in v9.1.10, v9.0.22).
- Pilots with tokens, still with a proxy: next slide.

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 2, zoom</div>

# Tokens: why pilots still carry a proxy

<div class="duw-two dx-tight">
<div>

- Since v8.0 (<a href="https://github.com/DIRACGrid/DIRAC/pull/6803" target="_blank">#6803</a>), the SiteDirector can submit pilots with a token, to CEs tagged `Token` or `Token:<VO>`.
- Sites still need the proxy that comes with the job: the accounting needs its VOMS information, and many ARC CEs need a proxy to run the job at all.
- So pilots must bring **both a token and a proxy**.

</div>
<div>

| CE | with a token | |
|---|---|---|
| HTCondorCE | token **and** proxy | works |
| ARC (AREX) | token only | fails at many sites |
| ARC (AREX), `AlwaysIncludeProxy` | token and proxy | ARC6 uses the proxy only |

<div style="font-size:.8rem;margin-top:.4rem">On ARC, pilots are in practice submitted with a proxy, as before tokens (<a href="https://github.com/DIRACGrid/DIRAC/issues/7908" target="_blank">#7908</a>, <a href="https://github.com/DIRACGrid/DIRAC/pull/7913" target="_blank">#7913</a>).</div>

</div>
</div>

<div class="dx-key mt-3"><b>No progress yet</b> on token-only pilots: ARC7 can account from token claims, but some sites' accounting still relies on X.509 proxies. DiracX itself is built on tokens.</div>

---

<div class="duw-sec">2 · DIRAC · stop 3 of 6</div>

# The pilot on the node

<div class="duw-stop">

<img :src="'/figures/fig-stop-3.svg'" alt="The DIRAC WMS path with the pilot highlighted on the worker node" />

<div>

<div class="duw-headline">Python 3 only, one source of time left, a verified download.</div>

<div v-click class="duw-stopsec rel"><h4>More reliable</h4>

- The pilot is now Python 3 only: no more Python 2 code paths (<a href="https://github.com/DIRACGrid/Pilot/pull/268" target="_blank">Pilot #268</a>) <span class="duw-was">DUW11</span>.
- The pilot reads the time left once and writes it to its configuration; jobs read it there, even in containers (<a href="https://github.com/DIRACGrid/DIRAC/pull/8479" target="_blank">#8479</a>, v9.1.4).
- One image for every architecture (open PR): next slide.

</div>
<div v-click class="duw-stopsec safe"><h4>Safer</h4>

- The pilot code was fetched over HTTPS without checking the certificate, then run (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vg99-gr89-qhw9" target="_blank">GHSA-vg99</a>, fixed in v9.1.10, v9.0.22).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 3, zoom</div>

# One image for every architecture

<img :src="'/figures/fig-multiarch.svg'" alt="CVMFS holds one directory per architecture under .multiarch; on an x86_64 node and on an aarch64 node the pilot reads uname -m and runs the matching copy of the same image" style="width:52%;margin:-1rem auto 0;display:block" />

<div class="duw-two dx-tight" style="font-size:.86rem">
<div>

- **CVMFS 2.14 supports multi-architecture images**: one image name, one copy per architecture, published by DUCC 2.14.1. Any CVMFS client reads them. We aim at relying on it.

</div>
<div>

- **In DIRAC**: a job names one container image, and the pilot runs the copy built for the node's architecture (x86_64 or aarch64). One of the last features added to DIRAC: <a href="https://github.com/DIRACGrid/DIRAC/pull/8456" target="_blank">#8456</a>, open, to certify <span class="duw-was">DUW11</span>.

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 4 of 6</div>

# Matching

<div class="duw-stop">

<img :src="'/figures/fig-stop-4.svg'" alt="The DIRAC WMS path with the Matcher and TaskQueueDB highlighted" />

<div>

<div class="duw-headline">Matching up to ~17× faster.</div>

<div v-click class="duw-stopsec fast"><h4>Faster</h4>

- Matching query: ~30 ms to ~3 ms (<a href="https://github.com/DIRACGrid/DIRAC/pull/8462" target="_blank">#8462</a>, v9.1.0, manual `ALTER TABLE`).
- When 323 task queues could serve a pilot, finding them took 3.4 s; now 0.2 s (<a href="https://github.com/DIRACGrid/DIRAC/pull/8801" target="_blank">#8801</a>, v9.1.20).

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 5 of 6</div>

# The JobAgent

<div class="duw-stop">

<img :src="'/figures/fig-stop-5.svg'" alt="The DIRAC WMS path with the JobAgent highlighted on the worker node" />

<div>

<div class="duw-headline">A job that restarts elsewhere is not failed by the node it left; each job keeps to its CPU and memory share.</div>

<div v-click class="duw-stopsec rel"><h4>More reliable</h4>

- A job that cannot start (e.g. its input sandbox fails to download) is rescheduled, and may soon run at another site. Minutes later, the JobAgent on the first node saw the error and set the job to Failed, while it was running elsewhere. It now leaves rescheduled jobs alone (<a href="https://github.com/DIRACGrid/DIRAC/pull/8441" target="_blank">#8441</a>, v9.0.17).
- Memory counts when matching and when filling a multi-core slot (<a href="https://github.com/DIRACGrid/DIRAC/pull/8366" target="_blank">#8366</a>, <a href="https://github.com/DIRACGrid/DIRAC/pull/8414" target="_blank">#8414</a>); cgroup v2 keeps each job within its CPU and memory share, where the site allows it (<a href="https://github.com/DIRACGrid/DIRAC/pull/8110" target="_blank">#8110</a>) <span class="duw-was">DUW11</span>.

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 6 of 6</div>

# The JobWrapper and its reports

<div class="duw-stop">

<img :src="'/figures/fig-stop-6.svg'" alt="The DIRAC WMS path with the JobWrapper, JobStateUpdate and pilot logging highlighted" />

<div>

<div class="duw-headline">Reports DiracX accepts; nobody edits someone else's job.</div>

<div v-click class="duw-stopsec rel"><h4>More reliable</h4>

- Jobs shorter than the first Watchdog cycle reported NaN: invalid JSON, so DiracX, which receives DIRAC's job reports, rejected the whole batch (<a href="https://github.com/DIRACGrid/DIRAC/pull/8750" target="_blank">#8750</a>, v9.1.16).
- Time left, graceful stop, the reason of a kill: next slide. The JobWrapper in pull and push: the one after.

</div>
<div v-click class="duw-stopsec safe"><h4>Safer</h4>

- Job state updates: any user could change any job's owner or status (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-j3xg-cjx8-qjpw" target="_blank">GHSA-j3xg</a>).
- Pilot logging: a crafted file name could read any file on the server (<a href="https://github.com/DIRACGrid/DIRAC/security/advisories/GHSA-vm3r-6cmw-8p5v" target="_blank">GHSA-vm3r</a>). Both fixed in v9.1.20, v9.0.26, v8.0.85.

</div>

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stops 5–6, zoom</div>

# Time left in the slot: before and after

<img :src="'/figures/fig-slot2.svg'" alt="Before: the payload is sized for the whole slot and is killed at the end, outputs lost. After: a margin is reserved before matching, a stop signal lets the payload wind down, and the uploads fit; a killed job reports why" style="width:84%;margin:.2rem auto 0;display:block" />

<div class="duw-two dx-tight mt-2" style="font-size:.88rem">
<div>

**An example**: an MC job sized for 183 events produced 150, was killed, and its output was never uploaded.

</div>
<div>

**To use it**: `StopMargin` and `StopSig*` in `/Systems/WorkloadManagement/JobWrapper`, or per job in the JDL; the graceful stop is off unless set. **v9.1.21 only.** Details: "Allocated time management" in the Administrator Guide. CPU work is normalised with DB12: <a href="https://indico.cern.ch/event/1588323/contributions/7264656/" target="_blank">next talk</a>.

</div>
</div>

---

<div class="duw-sec">2 · DIRAC · stop 6, zoom</div>

# The JobWrapper in pull and push

<div class="duw-two" style="grid-template-columns:1.05fr 1fr">
<div>

<img :src="'/figures/fig-pullpush.svg'" alt="Pull: the SiteDirector submits pilots to a CE, the pilot starts on the worker node, its JobAgent matches a job and runs the JobWrapper and the payload there. Push: a PushJobAgent next to the Matcher matches a job and submits the JobWrapper with its inputs to a CE in front of an HPC without outbound network; pre- and post-processing stay with the agent" style="width:100%;margin-top:-.4rem" />

<div class="dx-tight" style="font-size:.78rem">

- **Pull** (JobAgent, in the pilot): all three phases on the node, which needs outbound network.
- **Push** (PushJobAgent, on a DIRAC host): before and after run on the DIRAC host with the owner's proxy; the node only runs the payload, with DIRAC from CVMFS. Outputs come back with checksums.

</div>
</div>
<div class="dx-tight" style="font-size:.8rem">

**Before**: download the input sandbox, resolve the input data, the community's own pre-processing hook, prepare the command and environment.

**Payload**: runs under the Watchdog (CPU, memory, time left, stalled).

**After**: the community's own post-processing hook, upload the output sandbox, upload and register the output data, failover requests when an upload fails, accounting, final status.

</div>
</div>

<div class="dx-key mt-1" style="font-size:.8rem"><b>Pre- and post-processing only exist since v9.0</b> (<a href="https://github.com/DIRACGrid/DIRAC/pull/7587" target="_blank">#7587</a>), so communities still do these steps inside their workflows (e.g. uploading outputs). With CWL this should change: a CWL workflow must also run locally, so it holds no DIRAC-specific step; the job wrapper does them.</div>

---
layout: section
---

# 3 · DiracX: parcels, not jobs

And the proofs of concept around future DiracX compute backends

---

<div class="duw-sec">3 · DiracX</div>

# No jobs in DiracX

<img :src="'/figures/fig-parcels-only.svg'" alt="User jobs and workgraphs, both CWL, become parcels, the record of work, which a dispatcher sends to a backend; the JobDB in DiracX is legacy, used only to test deployments and deleted once everyone is on DiracX" style="width:48%;margin:-.6rem auto 0;display:block" />

<div class="duw-two dx-tight" style="margin-top:.2rem">
<div>

- A user payload is a parcel, like a bundle of transformation inputs. A failed parcel is final: resubmitting creates a new one.
- We do not port job monitoring or the job manager <span class="duw-was">DUW11</span>.

</div>
<div>

- The JobDB in DiracX is legacy: it receives job status updates from DIRAC, to **test a DiracX deployment**.
- It also feeds the **dummy job executor** (<a href="https://github.com/diracgrid/diracx/pull/995" target="_blank">diracx#995</a>): jobs go `Waiting → Done` without running anything, to test the transformation system. JobDB now, parcels later.
- **Once everyone is on DiracX, it is deleted.**

</div>
</div>

<div class="dx-key mt-2"><b>For you</b>: in DIRAC, nothing changes until your community moves. In DiracX you will submit CWL: you can start writing it now, and we can help during the hackathon session.</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# Proofs of concept around the DiracX backends

<img class="duw-pocfig" :src="'/figures/fig-pocmap.svg'" alt="From a parcel to a worker node: CWL describes the payload; DiracX pull (with pilot management) and DiracX push may share a matcher; interCEde talks to the CEs, and the job wrapper runs the payload on the worker node; all five are proofs of concept" style="max-height:14rem;width:86%" />

<div class="duw-poc5">
<div><h4>CWL</h4>ADR in draft; implemented with the transformation system</div>
<div><h4>Pilot management</h4>for DiracX pull; ported as is (<a href="https://github.com/DIRACGrid/diracx/pull/570" target="_blank">diracx#570</a>), paused: the data model needs redoing</div>
<div><h4>Matcher</h4>Python baseline and load tests; Redis next; maybe shared by pull and push</div>
<div><h4>interCEde</h4>ADRs in review; core proposed; integration tests</div>
<div><h4>Job wrapper</h4>requirements to gather: needs an owner</div>
</div>

<div class="duw-ask"><b>The same path for each</b>: explore, write an ADR, then implement in DiracX, in small increments you can try.</div>

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

DX-ADR-007, draft. `dirac-cwl` was a first proof of concept (with CTAO): only minor details may carry over. Upstream: <a href="https://github.com/common-workflow-language/cwltool/pull/2302" target="_blank">cwltool#2302</a>, <a href="https://github.com/common-workflow-language/cwltool/pull/2166" target="_blank">#2166</a>, <a href="https://github.com/common-workflow-language/schema_salad/pull/1064" target="_blank">schema_salad#1064</a> merged; <a href="https://github.com/common-workflow-language/cwl-utils/pull/446" target="_blank">cwl-utils#446</a> in review.

</div>
<div><h4>Next</h4>

Implemented with the transformation system, from this week's hackathon, where we can help you write your first CWL.

</div>
</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# Pilot management: port paused

<img class="duw-pocfig" :src="'/figures/fig-pilots.svg'" alt="DIRAC pilot management ported as is to a DiracX pilot database and router, then paused; what comes next is a question mark, to be re-thought with the DiracX compute backends" />

<div class="duw-poc3">
<div><h4>Why</h4>

Pilots belong to the DiracX pull backend, which comes after the transformation system.

</div>
<div><h4>Where it stands</h4>

Pilot database and router ported as is (<a href="https://github.com/DIRACGrid/diracx/pull/570" target="_blank">diracx#570</a>) <span class="duw-was">DUW11</span>. The data model could be much better, and changing it would mean large changes in DIRAC: paused.

</div>
<div><h4>Next</h4>

Re-thought with the DiracX compute backends. Meanwhile the DIRAC pilot keeps being patched.

</div>
</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# A matcher for DiracX compute backends

<img class="duw-pocfig" :src="'/figures/fig-matcher.svg'" alt="A pilot sends its node description; the POC matcher takes all waiting jobs, matches them against the node, filters them using the configuration and the running jobs, ranks them by fair share using the running jobs, and hands one job to the pilot" />

<div class="duw-poc3">
<div><h4>Why</h4>

DIRAC's matcher will likely not be fast enough for what is coming: we aim for <b>1,000 requests per second</b>. It also cannot express alternatives: GPU A, or GPU B, or CPU C.

</div>
<div><h4>Where it stands</h4>

A deliberately simple Python matcher (<a href="https://github.com/devlink42/poc-dirac-job-matchmaking" target="_blank">POC</a>), and load tests on LHCb-shaped data: 210 ms per match at 50k candidates.

</div>
<div><h4>Next</h4>

Redis, measured against this baseline, easy to rebuild (chaos tests with Redis off). Then an ADR, then DiracX.

</div>
</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# Computing elements, explored from use cases

<img :src="'/logos/intercede-logo.svg'" alt="interCEde logo" style="position:absolute;top:2.4rem;right:2.6rem;height:2.6rem" />

<img class="duw-pocfig" :src="'/figures/fig-intercede.svg'" alt="Communities send requirements to interCEde and test its increments; interCEde is tested against real HTCondor, ARC and Slurm CEs, then released to DiracX, where a WMS backend uses it" />

<div class="duw-poc3">
<div><h4>Why</h4>

Talking to CEs is needed by every WMS. Explored from the use cases DIRAC covers, and those it does not but should.

</div>
<div><h4>Where it stands</h4>

ADRs under review; core contract proposed (<a href="https://github.com/DIRACGrid/intercede/pull/27" target="_blank">interCEde#27</a>). Its own repository: integration tests against real CEs, so a change cannot break production.

</div>
<div><h4>Next</h4>

Increments you can test. The ADRs are merged once a first implementation works.

</div>
</div>

---
class: duw-poc
---

<div class="duw-sec">3 · DiracX · exploratory</div>

# The job wrapper: one for all of us

<img class="duw-pocfig" :src="'/figures/fig-wrappers.svg'" alt="The DIRAC JobWrapper in production, the dirac-cwl wrapper (an attempt at a new one), diracx#877 (a CWL port with new features, too big too soon) and CMS's solutions all feed a job wrapper to revisit for the different compute backends" />

<div class="duw-poc3">
<div><h4>Why</h4>

One JobWrapper in production. dirac-cwl: an attempt at a new one; diracx#877: its port with new features, too big, too soon. CMS joined, with interesting solutions.

</div>
<div><h4>Where it stands</h4>

Requirements to gather: inputs, time left and graceful stop, containers, nodes without outbound network, reporting, failed uploads.

</div>
<div><h4>Next</h4>

Revisit what we have and what CMS brings, for the different compute backends: a proof of concept, then an ADR.

</div>
</div>

<div class="duw-ask"><b>From you</b>: someone, or a group of people (not necessarily the same for each step): requirements, proof of concept, ADR.</div>

---
layout: cover
---

<div class="duw-thanks">
<div>

# Thank you

<div class="duw-contact">Questions and comments welcome, this week and after.</div>

<div class="duw-contact"><b>Alexandre F. Boyer</b> · alexandre.boyer@cern.ch</div>

<div class="duw-contact">github.com/DIRACGrid · diracx.diracgrid.org</div>

<div class="dx-logobar mt-8">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC, The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX, The Interware" />
</div>

</div>
<div class="duw-takeaways">

<div class="dx-eyebrow">Take-aways</div>

- **DIRAC is one compute backend** of the transformation system. It stays stable: upgrade to **v9.1.21** (with its manual `ALTER TABLE` steps) for faster matching and insertion, the time-left fixes and the security patches.
- **DiracX works on parcels, not jobs.** Its own backends come later; interCEde and the matcher are explored now, with tests, and get an ADR after a first implementation.
- **Tokens**: pilots still carry a proxy, because some sites' accounting relies on it.

<div class="duw-ask mt-3"><b>We need you</b>: someone, or a group of people, for the job wrapper: requirements, proof of concept, ADR.</div>

</div>
</div>
