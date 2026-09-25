---
colorSchema: light
favicon: /public/images/diracx-logo-square.svg
color: diracx-light
layout: cover
routerMode: hash
title: The 12th Dirac(X) Users' Workshop
theme: neversink
neversink_string: "DIRAC(X) DUW12"
download: true
---

# The 12th Dirac(X) Users' Workshop
## DiracGrid, DiracX, and the Road Ahead

**Federico Stagni** <Email v="federico.stagni@cern.ch" />

DiracGrid Technical Coordinator

<br>

13–16 October 2026, FZU Prague

<a href="https://indico.cern.ch/event/1588323/" class="ns-c-iconlink"><mdi-open-in-new />indico.cern.ch/event/1588323</a>

---
layout: section
color: diracx
title: Monolith to Puzzle
---

# From the Monolith to the Puzzle

---
layout: top-title
color: diracx-light
align: cm
title: DiracGrid
---

:: title::

# The shortened Dirac's story

:: content ::

Timeline:

```mermaid
%%{init: {'theme': 'base', 'timeline': {'disableMulticolor': true}}}%%
timeline
        section LHCb software
          around 2000 : MC production system: bash scripts running at production sites
          2002 : DIRAC2 <br> Rewritten in Python, using xml-rpc, interfacing to EDG
          Data Challenge 04 : First successful grid usage ever.
                            : First use of pilot jobs based WMS
          2006-2007 : DIRAC3<br> Full rewriting, development of the DISET protocol -- still in use today!
                    : the current DIRAC framework is still based on this work
        section Open sourced, wider adoption
          2008 : Large-ish reshuffling to become multi-VO
               : LHCbDIRAC extension separated from core DIRAC code
          2009 : CLIC community adopts DIRAC
          2011 : France-Grilles is the first multi-VO DIRAC installation
          2012 : Belle2, BES3, CTA adopt DIRAC
        section The DiracX era
          2023 : First DiracX prototype
          2025 : LHCb puts DiracX in production
          2026 : CMS and FCC join the effort
```

(full history in [this presentation](https://indico.cern.ch/event/1252369/contributions/5515343/attachments/))

Nowadays, the DiracGrid project develops/maintains DIRAC, DiracX, Web, etc... (everything in https://github.com/DIRACGrid).

[diracgrid.org](https://diracgrid.org) is hosting "everything" else you need.

<br>

Also the **logos changed**: we moved from the DIRAC branding to the new **DiracX** identity.

<img src="/public/images/diracx-logo-full.svg" class="mx-auto w-2/5 diracx-logo"> </img>

---
layout: top-title
color: diracx-light
align: cm
title: 2026-pivotal
---

:: title ::

# 2026 is a pivotal year

:: content ::

- **CMS and FCC are joining the effort** – bringing new requirements, scale, and energy to the project
- **New development process adopted** since the beginning of 2026
  - SCRUM-based, with 2-week sprints and regular checkpoint meetings
- **ADRs for everything** – Architecture Design Records guide every major decision before code is written
  - Transparent, reviewable, community-driven design process
  - [DX-ADR series](https://github.com/DIRACGrid/diracx/pulls?q=is%3Apr+is%3Aopen+label%3AADR) covers Transformation System, compute backends, CWL, and more

---
layout: top-title-two-cols
color: diracx-light
align: c-lm-lm
title: disambiguation
columns: is-4
---

:: title ::

# "Just rewriting" vs "Rethink and write"

:: left ::

**Just rewriting**
- Port existing functionality line-by-line
- Same architecture, new language/framework
- Fast, but locks in past limitations

:: right ::

**Rethink and write** (our approach)
- Question every assumption from the ground up
- Cloud-native, multi-VO from the get-go, standards-based
- Slower upfront, but the result is **younger, faster, better, stronger**
- DiracX is not DIRAC in a new language — it's DIRAC reimagined

<AdmonitionType type='important' >
A DIRAC++, in terms of functionalities — not just a port.
</AdmonitionType>

---
layout: top-title
color: diracx-light
align: cm
title: strategies
---

:: title ::

# Migration strategies we use (and when)

:: content ::

| Strategy | What | When adopted | Why |
|----------|------|-------------|-----|
| **FutureAdaptors** | 1-to-1 service replacements | Early prototypes | Quick wins, but bound to old DB schema; partially adopted |
| **RSS strategy** | Replace subsystem by subsystem | Ongoing | Minimizes disruption, allows gradual validation |
| **Legacy DIRAC as a backend** | DIRAC WMS as a compute backend from TransformationSystem POV | Current design | Eases transition, reuses investment |
| **Canary releases** | Gradual replacement on specific workloads | As features mature | Low-risk, real-world validation before full rollout |

<AdmonitionType type='note' >
<strong>Migrating extension code?</strong> Start by identifying which strategy fits your use case. FutureAdaptors work for direct service replacements, but for larger rewrites, plan around the new ADR-driven architecture.
</AdmonitionType>

---
layout: top-title
color: diracx-light
align: cm
title: roadmap
---

:: title ::

# The new roadmap

:: content ::

**TBD** – This will be discussed and finalized during the workshop.

Key areas under consideration:
- Transformation System completion
- Data Management integration (Rucio or native)
- Pilot / WMS development
- Job wrapper design (CMS-proposed ADR?)
- User-facing interfaces (analysis productions)

---
layout: top-title
color: diracx-light
align: cm
title: game-changed
---

:: title ::

# How the game has changed

:: content ::

> "The bottleneck for software development has always been writing code. With AI, **the bottleneck is our imagination**."
> — Jonathan Heyne, COO of DeepLearning.AI ([The Register, Apr 2026](https://www.theregister.com/2026/04/28/software_development_ai_dev25xsf))

<br>

| Before | Now |
|--------|-----|
| Bottleneck: **not enough developers** | Bottleneck: **specifications** |
| Every line hand-crafted by experts | LLMs write most of the code |
| Slow progress, long backlogs | Good ADRs are the real multiplier |

<AdmonitionType type='important' >
The value is no longer in writing code — it's in <strong>knowing what code to write</strong>.
</AdmonitionType>

> "If I have to review the code, I become the bottleneck."
> — Andrew Ng, [AI Dev 26 x SF](https://www.theregister.com/2026/04/28/software_development_ai_dev25xsf)

---
layout: section
color: diracx-green
title: Numbers
---

# Numbers since the previous workshop

---
layout: top-title-two-cols
color: diracx-light
align: cm-lm-lm
title: numbers-dirac
columns: is-5
---

:: title ::

# DIRAC stack activity

:: left ::

<!-- TODO: Update with actual numbers from previous DUW -->

- **Commits / PRs:** TBD
- **Issues created:** TBD
- **Issues closed:** TBD
- **Contributors:** TBD

:: right ::

<!-- Reference: slides 20+21 from https://gitlab.cern.ch/alboyer/slides-computing-report-lhcb-week/-/raw/master/deck/20260915-LHCbWeek121-Compute.pdf -->

<AdmonitionType type='note' >
See [LHCb Computing Report slides 20-21](https://gitlab.cern.ch/alboyer/slides-computing-report-lhcb-week/-/raw/master/deck/20260915-LHCbWeek121-Compute.pdf) for detailed metrics.
</AdmonitionType>

---
layout: top-title-two-cols
color: diracx-light
align: cm-lm-lm
title: numbers-diracx
columns: is-5
---

:: title ::

# DiracX stack activity

:: left ::

<!-- TODO: Update with actual numbers from previous DUW -->

- **Commits / PRs:** TBD
- **Issues created:** TBD
- **Issues closed:** TBD
- **Contributors:** TBD

:: right ::

<AdmonitionType type='note' >
See [LHCb Computing Report slides 20-21](https://gitlab.cern.ch/alboyer/slides-computing-report-lhcb-week/-/raw/master/deck/20260915-LHCbWeek121-Compute.pdf) for detailed metrics.
</AdmonitionType>

---
layout: top-title
color: diracx-light
align: cm
title: releases
---

:: title ::

# Releases

:: content ::

**DIRAC v9**
- Regular releases continue
- Changelog: [github.com/DIRACGrid/DIRAC/releases](https://github.com/DIRACGrid/DIRAC/releases)

**DiracX**
- Ongoing development releases
- Changelog: [github.com/DIRACGrid/diracx/releases](https://github.com/DIRACGrid/diracx/releases)

---
layout: top-title
color: diracx-light
align: cm
title: v8-update
---

:: title ::

# Update process for v8 users

:: content ::

For v8 users still on the legacy stack:

- The only significant change is that **you should now target v9.0**
- v8 is in maintenance mode; new features go to v9 and DiracX
- Migration path is straightforward: update your dependencies and test against v9.0
- Contact the DiracGrid team if you need help with the transition

---
layout: top-title
color: diracx-light
align: cm
title: timeline-future
---

:: title ::

# Timeline (looking ahead)

:: content ::

<!-- TODO: Add future timeline once roadmap is finalized -->

```mermaid
%%{init: {'theme': 'base', 'timeline': {'disableMulticolor': false}}}%%
timeline
        title Roadmap outlook
        2026 Q4 : ADR reviews concluded at DUW12
                : Development plan finalized
        2027 H1 : Transformation System implementation
                : First canary releases
        2027 H2 : Wider adoption by early-adopter communities
        2028    : ...
```

---
layout: top-title
color: diracx-light
align: cm
title: hsf
---

:: title ::

# HSF Affiliated Project

:: content ::

<br>

DiracGrid is an [**HSF affiliated project**](https://hepsoftwarefoundation.org/projects/projects.html).

<br>

<div class="flex justify-center items-center">
  <img src="/public/images/hsf-logo.png" class="h-40 mx-auto" alt="HSF Logo">
</div>

<br>

This affiliation recognizes DiracGrid's contribution to the HEP software ecosystem and ensures alignment with community-wide best practices.

---
layout: section
color: diracx-green
title: Publications
---

# Publications and Outreach

---
layout: top-title
color: diracx-light
align: cm
title: chep-papers
---

:: title ::

# CHEP papers

:: content ::

<!-- TODO: Add CHEP paper references -->

- CHEP 2025 papers on DiracX architecture and deployment
- Links and DOIs to be added

---
layout: top-title
color: diracx-light
align: cm
title: other-conferences
---

:: title ::

# DiracX at other conferences

:: content ::

<!-- TODO: Add conference references -->

- DiracX presentations at various HEP computing conferences
- Community outreach and engagement

---
layout: section
color: diracx
title: Program
---

# Program of Work for These Days

---
layout: top-title
color: diracx-light
align: cm
title: program-details
---

:: title ::

# What we'll do together

:: content ::

<!-- TODO: Fill in with actual workshop program -->

- Review and finalize the ADRs
- Iron out the last details on the Transformation System design
- Prepare the development plan
- Code some of the tasks together
- Discuss migration strategies for each community

See the [full agenda](https://indico.cern.ch/event/1588323/timetable/) on Indico.

---
layout: section
color: diracx
title: Conclusions
---

# Summary

---
layout: top-title-two-cols
align: cm-cm-lm
color: diracx-light
columns: is-3
title: summary
---
:: title ::

# Summary

:: left ::

<img src="/public/images/diracx-logo-square.svg" class="mx-auto w-3/5 diracx-logo"> </img>

:: right ::

- DiracGrid has a very active community of users and developers
- **2026 is a pivotal year**: CMS and FCC joined, new dev process, ADRs for everything
- DiracX is the **rethought** DIRAC — cloud-native, modular, standards-based
- Multiple migration strategies are available depending on your needs
- The **Transformation System** is the next big thing
- **Let's build it together** during this workshop

---
layout: credits
color: diracx
loop: true
speed: 1.4
title: credits/people
---

<div class="grid text-size-4 grid-cols-3 w-3/4 gap-y-10 auto-rows-min ml-auto mr-auto">
    <div class="grid-item text-center mr-0- col-span-3">
        <strong>People</strong><br>
    </div>
    <div class="grid-item text-right mr-4 col-span-1">
        <strong>Current Developers, maintainers, supporters (non-exhaustive list)</strong>
    </div>
    <div class="grid-item col-span-2">
        Chris Burr <i>CERN, LHCb</i><br/>
        Christophe Haen <i>CERN, LHCb</i><br/>
        Alexandre Boyer <i>CERN, LHCb</i><br/>
        Natthan Pigoux <i>LUPM (FR), CTAO</i><br/>
        Cedric Serfon <i>Brookhaven National Laboratory (US), Belle2</i><br/>
        Ryunosuke O'Neil <i>CERN, LHCb</i><br/>
        Daniela Bauer <i>Imperial college (UK), GridPP</i><br/>
        Simon Fayer <i>Imperial college (UK), GridPP</i><br/>
        Janusz Martyniak <i>Imperial college (UK), GridPP</i><br/>
        Xiaomei Zhang <i>Beijing, Inst. High Energy Phys. (CN), Juno</i><br/>
        Luisa Arrabito <i>LUPM (FR), CTAO</i><br/>
        André Sailer <i>CERN, ILC</i><br/>
        Jorge Lisa Laborda <i>Univ. of Valencia and CSIC (ES), LHCb</i><br/>
        Bertrand Rigaud <i>IN2P3 (FR), France-Grilles</i><br/>
        Heloise Joffe <i>IN2P3 (FR), France-Grilles</i><br/>
        Stella Maria Renucci <i>LUPM (FR), CTAO</i><br/>
        Mazen Ezzeddine <i>CPPM (FR), EGI</i><br/>
        Loris Vankatwijk <i>LUPM (FR), CTAO</i><br/>
        Alan Malta <i>Notre Dame university (US), CMS</i><br/>
        Andrea Piccinelli <i>Notre Dame university (US), CMS</i><br/>
        Valentin Kuznetsov <i>Cornell University (US), CMS</i><br/>
        Marco Mascheroni <i>(US), University of California San Diego (US), CMS</i><br/>
        Todor Ivanov <i>Notre Dame university (US), CMS</i><br/>
        Francesco Brivio <i>(IT), Milano Bicocca University, CMS</i><br/>
        Juraj Smiesko <i>(CERN), FCC</i><br/>
        Benedikt Wach <i>(CERN), FCC</i><br/>
    </div>
    <div class="grid-item text-right mr-4 col-span-1">
        <strong>Project lead</strong>
    </div>
    <div class="grid-item col-span-2">
        Federico Stagni <i>CERN, LHCb</i><br/>
        Andrei Tsaregorodtsev <i>CPPM (FR), EGI, LHCb, Juno</i>
    </div>
</div>

&nbsp;
&nbsp;
&nbsp;
---
layout: section
color: diracx
title: Questions
---

# Questions?
