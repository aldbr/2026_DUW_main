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

<img :src="'/figures/fig-hetero.svg'" alt="CVMFS holds one directory per architecture under .multiarch; an x86_64 node and an aarch64 node each pull their own image into a container limited by cgroup2; an HPC centre is reached through the SSH CE" style="width:44%;margin:-1.2rem auto 0;display:block" />

<div class="duw-two dx-tight" style="font-size:.8rem">
<div>

- **One image for x86_64 and aarch64** (<a href="https://github.com/DIRACGrid/DIRAC/pull/8456" target="_blank">#8456</a>, open) <span class="duw-was">DUW11</span>. A job names one container image; the pilot reads the node's architecture and takes the matching copy under CVMFS `/.multiarch`. Publishing needs CVMFS 2.14 (DUCC 2.14.1); any client reads it.
- **CPU and memory limits** (v9.0) <span class="duw-was">DUW11</span>. Memory requests count when matching and when sharing a multi-core slot; cgroup2 keeps each job within its share.

</div>
<div>

- **HPC through SSH** (v9.0) <span class="duw-was">DUW11</span>. The SSH computing element, rewritten on Fabric, submits through an HPC login node to its batch system.
- **Still missing in DIRAC: alternatives.** A job states one platform and one set of requirements. It cannot say "x86_64, or aarch64, or a GPU of type A". The DiracX matcher is designed for this (section 3).

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

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# CWL describes all the work

<img :src="'/logos/cwl.svg'" alt="Common Workflow Language logo" style="position:absolute;top:2.5rem;right:2.6rem;height:2.4rem" />

<div class="duw-two">
<div>

**One format** (DX-ADR-007, draft): a user payload, a workgraph and each transformation are CWL v1.2 documents.

- DiracX settings are `dirac:` **hints**: every document stays plain, runnable CWL.
- The same document runs with `cwltool`, locally, and at scale.
- Processes are resolved before dispatch: the node fetches no definitions.

</div>
<div>

**For a WMS backend**
- Matching requirements come from the hints.
- The job wrapper resolves inputs (`lfn:`, `sandbox:`) and reports a status per input.
- DiracX registers the outputs after the parcel ends.

**Yesterday**: hands-on sessions to convert DIRAC workflows to CWL.

</div>
</div>

<div class="dx-card dx-card-new mt-2" style="height:auto;padding:.45em .8em">

**With the CWL community**: <a href="https://github.com/common-workflow-language/cwltool/pull/2302" target="_blank">cwltool#2302</a> path mapper, <a href="https://github.com/common-workflow-language/cwltool/pull/2166" target="_blank">cwltool#2166</a> Apptainer sandboxes, <a href="https://github.com/common-workflow-language/schema_salad/pull/1064" target="_blank">schema_salad#1064</a>: merged. <a href="https://github.com/common-workflow-language/cwl-utils/pull/446" target="_blank">cwl-utils#446</a> QuickJS engine: in review.

</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# interCEde: computing elements, explored from use cases

<div class="duw-two" style="grid-template-columns:1fr 1.5fr;align-items:center">
<div class="dx-tight">

- **An exploratory project**, from the use cases DIRAC covers, and those it does not but should.
- **Its own repository**: integration tests against real CEs, so that a change cannot break a production instance.
- **Ends with ADRs and a first implementation**; the ADRs are merged once that implementation works.

</div>
<div>

<img :src="'/figures/fig-intercede.svg'" alt="Communities send requirements to interCEde and test its increments; interCEde is tested against real HTCondor, ARC and Slurm CEs, then released to DiracX, where a WMS backend uses it" style="width:100%" />

</div>
</div>

<div class="dx-card dx-card-blue mt-2" style="height:auto">

**Open call**: if you work with DIRAC computing elements, test the increments of <a href="https://github.com/DIRACGrid/intercede" target="_blank">interCEde</a> and tell us what does not fit your needs, or what DIRAC does not cover: in an issue, or at a DOps.

</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# A matcher for the DiracX WMS

<div class="duw-two dx-tight">
<div>

**Why**
- DIRAC's matcher will not be fast enough for what is coming for some communities, such as LHCb.
- It cannot describe heterogeneous needs: a payload that runs on GPU A, *or* GPU B, *or* CPU C.

</div>
<div>

**The proof of concept** (<a href="https://github.com/devlink42/poc-dirac-job-matchmaking" target="_blank">poc-dirac-job-matchmaking</a>)
- A deliberately simple Python matcher, and load tests on LHCb-shaped data to compare solutions.
- The solution must be easy to deploy and to rebuild: chaos tests with Redis switched off.

</div>
</div>

<img :src="'/figures/fig-matcher.svg'" alt="The POC matcher for one pilot request: all waiting jobs, then match against the node, filter by job-type limits and priority, rank by fair share, and hand one job to the pilot" style="width:64%;margin:0 auto;display:block" />

<div class="dx-key mt-1">Next: matching in Redis, measured against this baseline. Then an ADR, then the implementation in DiracX.</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# Pilot management: port paused

<div class="duw-three3">

<div class="dx-card dx-card-new">

### We started
Porting pilot management from DIRAC to DiracX as it is: a pilot database and router landed (<a href="https://github.com/DIRACGrid/diracx/pull/570" target="_blank">diracx#570</a>) <span class="duw-was">DUW11</span>.

</div>

<div class="dx-card dx-card-blue">

### We learned
The data model could be much better. Changing it would mean large changes in DIRAC, which we keep stable.

</div>

<div class="dx-card dx-card-legacy">

### So we paused
Registration, pilot tokens and logging wait for the DiracX WMS backend. The re-thinking has not started.

</div>

</div>

<div class="dx-key mt-3">Pilots belong to the DiracX WMS backend, which comes after the transformation system. The DIRAC pilot keeps being patched.</div>

---

<div class="duw-sec">3 · DiracX: parcels, not jobs</div>

# The job wrapper: one for all of us

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

**We are looking for someone** to gather the requirements and the feedback, build a proof of concept, then design the ADR, working alongside someone who has been through the process once. Come and talk to us this week.

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
