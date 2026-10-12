---
theme: default
title: "Building together: the DiracX Transformation System"
info: |
  ## Building together: the DiracX Transformation System — DUW 12 hackathon
  Programme, ice-breaker game, 1-2-4-All, mob programming, planning poker.
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

# Building together

<p class="ts-subtitle">The DiracX Transformation System</p>

DiracX hackathon · 12th DIRAC(X) Users' Workshop · FZU Prague

<div class="dx-logobar mt-10">
  <img :src="'/logos/DIRAC-logo.webp'" alt="DIRAC — The Interware" />
  <img :src="'/logos/diracx.png'" alt="DiracX — The Interware" />
</div>

---

<div class="duw-sec">Programme</div>

# From a game to working code

<div class="ts-program">
  <div class="ts-step"><span class="n">Tue 16:10</span><b>Ice-breaker game</b><span class="t">40 min</span><p>Run a workgraph by hand, with sticky notes.</p></div>
  <div class="ts-step"><span class="n">Tue 16:50</span><b>1-2-4-All</b><span class="t">1 h</span><p>What must exist, and how do we split the work?</p></div>
  <div class="ts-step"><span class="n">Wed 14:00</span><b>Mob programming</b><span class="t">1 h 50</span><p>We build the database and the state machines together, with Claude.</p></div>
  <div class="ts-step"><span class="n">Wed 16:10</span><b>Planning poker</b><span class="t">45 min</span><p>We size the work items and form pairs.</p></div>
  <div class="ts-step"><span class="n">Wed 17:00 → Fri</span><b>We build</b><span class="t">about 6 h</span><p>Pairs and small pull requests. Demo on Friday.</p></div>
</div>

<div class="ts-message mt-8">Code is becoming cheap.<br/>What we need is a <b>common understanding</b> of what to build, and of how we <b>review</b> it.</div>

---
layout: section
---

# 1 · Ice-breaker game

Run a Monte Carlo workgraph by hand

---

<div class="duw-sec">1 · Ice-breaker game</div>

# The game: 8 seeds become 1 merged file

<div class="ts-chain">
  <div class="ts-board src"><b>Seed stack</b><span>8 red notes, S1 … S8</span><span class="io"><span class="ts-note r"></span><span class="ts-note r"></span><span class="ts-note r"></span></span></div>
  <div class="arr">→</div>
  <div class="ts-board sim"><b>SIMULATION</b><span>1 seed per parcel</span><span class="io"><span class="ts-note r"></span> → <span class="ts-note g"></span></span></div>
  <div class="arr">→</div>
  <div class="ts-board reco"><b>RECONSTRUCTION</b><span>2 green per parcel</span><span class="io"><span class="ts-note g"></span><span class="ts-note g"></span> → <span class="ts-note b"></span></span></div>
  <div class="arr">→</div>
  <div class="ts-board merge"><b>MERGE</b><span>4 blue per parcel</span><span class="io"><span class="ts-note b"></span><span class="ts-note b"></span><span class="ts-note b"></span><span class="ts-note b"></span>→<span class="ts-note y"></span></span></div>
  <div class="arr">→</div>
  <div class="ts-board out"><b>Finished</b><span>1 yellow note in Merge's Outputs: shout <b>“Completed!”</b></span></div>
</div>

<div class="ts-looptitle">Three players per table, one board at a time: Simulation, then Reconstruction, then Merge</div>

<div class="ts-loop">
  <span class="ts-who">Feeder</span><span class="arr">→</span>
  <span class="ts-where">Pool<small>at most 2 notes at a time</small></span><span class="arr">→</span>
  <span class="ts-who">Packer</span><span class="arr">→</span>
  <span class="ts-who">Compute backend</span><span class="arr">→</span>
  <span class="ts-where">✓ Done<small>new notes → Outputs</small></span>
</div>
<div class="ts-retry" style="margin-left:162px;width:254px"><span style="top:.95rem;background:none">✗ the note goes back to the Pool, a <b>new</b> parcel takes it</span></div>

<div class="ts-legend" style="margin-top:2.6rem">
  <span><span class="ts-who" style="font-size:.7rem;padding:.15rem .5rem">dark</span> a player</span>
  <span><span class="ts-where" style="font-size:.7rem;padding:.05rem .4rem">dashed</span> a place on the table</span>
  <span><b>Parcel</b>: a quarter sheet with its input notes stuck on it, one job</span>
</div>

---

<div class="duw-sec">1 · Ice-breaker game</div>

# Round 1

<div class="ts-round">
  <div class="ts-roundno"><div class="k">Round</div><div class="v">1</div><div class="t">7 min</div></div>
  <div>
    <ul class="ts-big">
      <li>Read your sheet. Ask your team, not us.</li>
      <li>Start when we say <b>go</b>.</li>
      <li>One board at a time: 8 seeds → 8 green → 4 blue → <b>1 yellow</b>.</li>
      <li>Shout <b>“Completed!”</b> when the yellow note is in Merge's Outputs.</li>
    </ul>
  </div>
</div>

---

<div class="duw-sec">1 · Ice-breaker game</div>

# Round 2

<div class="ts-round">
  <div class="ts-roundno"><div class="k">Round</div><div class="v">2</div><div class="t">7 min</div></div>
  <div>
    <ul class="ts-big">
      <li>Reset the table: notes back in the stack, new parcels.</li>
      <li><b>Same game, same goal.</b></li>
      <li>Shout <b>“Completed!”</b> when the yellow note is in Merge's Outputs.</li>
    </ul>
  </div>
</div>

---

<div class="duw-sec">1 · Ice-breaker game</div>

# Round 3

<div class="ts-round">
  <div class="ts-roundno"><div class="k">Round</div><div class="v">3</div><div class="t">7 min</div></div>
  <div>
    <ul class="ts-big">
      <li><b>Change roles:</b> Feeder → Packer → Compute backend → Feeder. Take the sheet of your new role.</li>
      <li>The Packer receives a <b>new version of the Reconstruction packer plugin</b>.</li>
      <li>Same goal. Shout <b>“Completed!”</b></li>
    </ul>
  </div>
</div>

---

<div class="duw-sec">1 · Ice-breaker game</div>

# Debrief

<div class="duw-two">
<div>

### What happened

- Where did you **wait**? Who was the bottleneck?
- When a job failed, what was **retried**: the parcel or the seed?
- How did you know the work was **finished**?
- Who knew how many notes were where? Now imagine **100 million** notes.

</div>
<div>

<table class="duw-map"><tbody>
  <tr><th>You played</th><th>We will build</th></tr>
  <tr><td>Feeder</td><td>Feeder, edge feeder</td></tr>
  <tr><td>Packer</td><td>Packer</td></tr>
  <tr><td>Packer → backend</td><td>Dispatcher</td></tr>
  <tr><td>Backend: the job</td><td>Dummy backend</td></tr>
  <tr><td>Backend: ✓ and ✗</td><td>Completion</td></tr>
  <tr><td>Nobody kept the books</td><td>Database, counters</td></tr>
  <tr><td>The rules on the boards</td><td>CWL submission</td></tr>
</tbody></table>

</div>
</div>

<div class="dx-key mt-4">In the game, you moved the notes yourselves. In DiracX, a feeder or a packer only <b>says</b> what should happen. The core then updates the database in one step, so a note is never lost or counted twice.</div>

---
layout: section
---

# 2 · 1-2-4-All

What must exist, and how do we split it?

---

<div class="duw-sec">2 · 1-2-4-All</div>

# 1-2-4-All

<div class="ts-question">What must exist for the whole Transformation System to work? What do we build first? What is unclear?</div>

<p class="duw-small" style="margin:.4rem 0 0"><b>Already known:</b> 2-week sprints · 4 to 5 pairs · the dummy executor exists and must be adapted to parcels · <code>simulation.cwl</code> in the <a href="https://diracx--1042.org.readthedocs.build/en/1042/playground/">simulator</a></p>

<div class="ts-124" style="margin-top:.5rem">
  <div><div class="who">1</div><div class="min">5 min · alone</div><p>One piece of work per note <span class="ts-note y"></span>, one question per note <span class="ts-note p"></span>. In silence.</p></div>
  <div><div class="who">2</div><div class="min">10 min · in pairs</div><p>Merge your notes, remove duplicates, sharpen the words.</p></div>
  <div><div class="who">4</div><div class="min">15 min · in fours</div><p>Group into <b>work items</b>: one behaviour, one pair, one sprint. Say when it is <b>done</b>.</p></div>
  <div><div class="who">All</div><div class="min">25 min · together</div><p>All items on the wall, in order, to the full system. Add only what is new. Pick the first sprint.</p></div>
</div>

<div class="dx-key mt-2"><b>Outcome:</b> the whole system in order; the first sprint as items, sized on Wednesday.<br/><b>Example:</b> <i>a failed parcel sends its inputs to Failed</i> · done: a test sees them Failed, ErrorCount 1 · needs: transitions</div>

---
layout: section
---

# 3 · Mob programming

The shared core, built together

---

<div class="duw-sec">3 · Mob programming</div>

# Mob programming: the shared core, with Claude

<div class="ts-build">
  <span class="lbl">What we build</span>
  <span class="dx-chip">database tables · DX-ADR-004</span>
  <span class="dx-chip">state machines as data · DX-ADR-005</span>
  <span class="dx-chip">transitions module: the only code that changes a status</span>
  <span class="dx-chip">one transition + its test</span>
</div>

<div class="ts-mob">
  <div class="ts-mobnode"><span class="k">1 · the room</span><b>Decides the next prompt</b><span>architects check it against the ADRs</span></div>
  <div class="arr">→</div>
  <div class="ts-mobnode dark"><span class="k">2 · one person</span><b>Types it into Claude</b><span>on the projector</span></div>
  <div class="arr">→</div>
  <div class="ts-mobnode"><span class="k">3 · git</span><b>One prompt, one commit</b><span>pushed to a draft pull request</span></div>
  <div class="arr">→</div>
  <div class="ts-mobnode"><span class="k">4 · everyone</span><b>Reviews the diff live</b><span>and comments on GitHub</span></div>
</div>
<div class="ts-mobback"><span>the comments become the next prompt</span></div>

<div class="dx-key mt-6">Every pair will build on this code, so we learn it together.</div>

---
layout: section
---

# 4 · Planning poker

How big is each item?

---

<div class="duw-sec">4 · Planning poker</div>

# Planning poker

<div class="ts-fib">
  <div class="ts-card"><span class="v">1</span><p>Trivial. We know exactly what to change.</p><span class="hand"><i>☝️</i>1 finger</span></div>
  <div class="ts-card"><span class="v">2</span><p>Small and clear.</p><span class="hand"><i>✌️</i>2 fingers</span></div>
  <div class="ts-card"><span class="v">3</span><p>Medium. Some thinking, few unknowns.</p><span class="hand"><i>🤟</i>3 fingers</span></div>
  <div class="ts-card"><span class="v">5</span><p>Large. Several parts, some unknowns.</p><span class="hand"><i>🖐️</i>one hand</span></div>
  <div class="ts-card"><span class="v">8</span><p>Very large. Try to split it.</p><span class="hand"><i>🖐️🤟</i>5 + 3</span></div>
  <div class="ts-card warn"><span class="v">13</span><p>Too big. Split it before we start.</p><span class="hand"><i>🙅</i>arms crossed</span></div>
  <div class="ts-card meta"><span class="v">?</span><p>I do not understand the item.</p><span class="hand"><i>✊</i>fist</span></div>
</div>

<div class="duw-two mt-4">
<div>

- Points measure **size**: effort, complexity, uncertainty. Not hours.
- “3, 2, 1, **show**”: everyone shows their fingers at the same time.

</div>
<div>

- The **highest** and the **lowest** explain. Then one more vote.
- Our usual pace: about **6 points per person per sprint**.

</div>
</div>

---
layout: cover
---

# Now, let's build it

<div class="ts-next">
  <span>Pick your first item</span>
  <span>Small pull requests to <code>main</code></span>
  <span>Review another pair's pull request before your next item</span>
  <span>Demo on Friday</span>
</div>

---
layout: section
---

# Backup

Game material: set-up, table, role sheets

---

<div class="duw-sec">Backup · game</div>

# Game set-up and timing

<div class="duw-two">
<div>

### Tables of 3 players

- 3 players per table: Feeder, Packer, Compute backend. About 10 people: 3 tables, one observer.
- Per table: red <span class="ts-note r"></span>, green <span class="ts-note g"></span>, blue <span class="ts-note b"></span> and yellow <span class="ts-note y"></span> notes; 8 red notes written in advance, <code>S1</code> … <code>S8</code>
- Per table: pens, scrap paper cut in quarters (the parcels), 3 boards, 3 role sheets, the two cards on the last page
- Pink and yellow pads for the 1-2-4-All

</div>
<div>

<table class="duw-map"><tbody>
  <tr><th>Time</th><th>Step</th></tr>
  <tr><td>3 min</td><td>Explain the game</td></tr>
  <tr><td>5 min</td><td>Read sheets, set up the table</td></tr>
  <tr><td>7 min</td><td>Round 1, happy path</td></tr>
  <tr><td>2 + 7 min</td><td>Reset, round 2, a surprise failure</td></tr>
  <tr><td>2 + 7 min</td><td>Reset, round 3, roles rotate and new packer rule</td></tr>
  <tr><td>7 min</td><td>Debrief</td></tr>
</tbody></table>

</div>
</div>

---

<div class="duw-sec">Backup · game</div>

# The table

<div class="ts-table">
  <div class="bd" style="border-top-color:var(--ts-red)"><b>SIMULATION board</b><span class="duw-small">1 red per parcel</span><div class="cols"><span>Pool</span><span>Done</span><span>Outputs</span></div></div>
  <div class="bd" style="border-top-color:var(--ts-green)"><b>RECONSTRUCTION board</b><span class="duw-small">2 green per parcel</span><div class="cols"><span>Pool</span><span>Done</span><span>Outputs</span></div></div>
  <div class="bd" style="border-top-color:var(--ts-blue)"><b>MERGE board</b><span class="duw-small">4 blue per parcel</span><div class="cols"><span>Pool</span><span>Done</span><span>Outputs</span></div></div>
</div>

<div class="ts-spots" style="grid-template-columns:repeat(3,1fr)">
  <div><b>Seed stack</b><span class="ts-note r"></span> S1 … S8, written in advance</div>
  <div><b>Backend seat</b><span class="ts-note g"></span><span class="ts-note b"></span><span class="ts-note y"></span> pads, pens; one parcel at a time</div>
  <div><b>Bin</b>every used parcel, done or failed. Never reused.</div>
</div>

<div class="duw-two mt-4">
<div class="duw-small"><b>A parcel</b> is a quarter sheet with the input notes stuck on it (<code>P5 · RECO</code>). After the job, the Compute backend puts ✓ inputs in Done, new notes in Outputs, ✗ inputs back in their Pool, and the empty parcel in the Bin.</div>
<div class="duw-small"><b>Only the seeds have names</b>, written in advance. The other notes stay blank: green is what Simulation makes, blue Reconstruction, yellow Merge.</div>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Feeder

<div class="ts-role core">
<div class="side"><div class="real">You play the <b>feeder</b> plugin of all three transformations, one board at a time. On Reconstruction and Merge you are an <b>edge feeder</b>: your inputs are the outputs of the board before.</div><div class="real"><b>You hold:</b> the seed stack S1 … S8. Never more than <b>2 notes</b> in your hands.</div></div>
<ol>
  <li><b>Simulation:</b> move seeds <span class="ts-note r"></span> from the stack into its Pool, <b>at most 2 at a time</b>. Stack empty? Say <b>“Simulation feed is over.”</b></li>
  <li><b>Reconstruction</b>, once Simulation's Done holds all 8 seeds: move the green notes <span class="ts-note g"></span> from Simulation's Outputs into its Pool, at most 2 at a time. Outputs empty? Say <b>“Reconstruction feed is over.”</b></li>
  <li><b>Merge</b>, once Reconstruction's Done holds all 8 green notes: the same with the blue notes <span class="ts-note b"></span>. Then say <b>“Merge feed is over.”</b></li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Packer

<div class="ts-role core">
<div class="side"><div class="real">You play the <b>packer</b> plugin of all three transformations, one board at a time: you decide which notes go together in one job.</div><div class="real"><b>You hold:</b> paper quarters, a pen. A rule may change in round 3.</div></div>
<ol>
  <li>Take notes from the Pool of the current board: <b>Simulation</b> 1 seed per parcel, <b>Reconstruction</b> 2 green, <b>Merge</b> 4 blue.</li>
  <li>Write <code>P1 · SIM</code> (then P2, P3…) on a paper quarter and stick the notes on it.</li>
  <li>Hand the parcel to the <b>Compute backend</b>. It already holds one? Wait.</li>
  <li>Not enough notes? Wait. Once the Feeder says the feed is over, pack what is left.</li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Compute backend

<div class="ts-role core">
<div class="side"><div class="real">You play where the jobs run, for all three transformations, and you record what each job did on the boards. One parcel at a time.</div><div class="real"><b>You hold:</b> the <span class="ts-note g"></span> <span class="ts-note b"></span> <span class="ts-note y"></span> pads, a pen. If you get a card, read it in secret.</div></div>
<ol>
  <li><b>Run:</b> take blank notes of the next colour, nothing to write: one green <span class="ts-note g"></span> per <b>SIM</b> parcel, one blue <span class="ts-note b"></span> per <b>RECO</b> parcel, one yellow <span class="ts-note y"></span> per <b>MERGE</b> parcel.</li>
  <li><b>Record:</b> ✓ inputs go to the board's <b>Done</b>, the new notes to its <b>Outputs</b>. A ✗ input goes back to its <b>Pool</b>.</li>
  <li>Put the empty parcel in the <b>Bin</b>. A parcel is never reused.</li>
  <li>When the yellow note is in Merge's Outputs and every Pool is empty, shout <b>“Completed!”</b></li>
</ol>
</div>

---

<div class="duw-sec">Backup · board</div>

# Simulation board

<div class="ts-mat-sub">1 red per parcel · print on A4 landscape</div>

<div class="ts-mat sim">
<div><b>Pool</b><span class="what">waiting to be packed</span><span class="who">In: Feeder (seeds), Compute backend (✗ inputs)<br>Out: Packer</span></div>
<div><b>Done</b><span class="what">processed by exactly one parcel</span><span class="who">In: Compute backend only (✓ inputs)<br>Out: nobody</span></div>
<div><b>Outputs</b><span class="what">green notes, for the next board</span><span class="who">In: Compute backend only (new notes)<br>Out: the Feeder takes them to Reconstruction</span></div>
</div>

---

<div class="duw-sec">Backup · board</div>

# Reconstruction board

<div class="ts-mat-sub">2 green per parcel · print on A4 landscape</div>

<div class="ts-mat reco">
<div><b>Pool</b><span class="what">waiting to be packed</span><span class="who">In: Feeder (green notes), Compute backend (✗ inputs)<br>Out: Packer</span></div>
<div><b>Done</b><span class="what">processed by exactly one parcel</span><span class="who">In: Compute backend only (✓ inputs)<br>Out: nobody</span></div>
<div><b>Outputs</b><span class="what">blue notes, for the next board</span><span class="who">In: Compute backend only (new notes)<br>Out: the Feeder takes them to Merge</span></div>
</div>

---

<div class="duw-sec">Backup · board</div>

# Merge board

<div class="ts-mat-sub">4 blue per parcel · print on A4 landscape</div>

<div class="ts-mat merge">
<div><b>Pool</b><span class="what">waiting to be packed</span><span class="who">In: Feeder (blue notes), Compute backend (✗ inputs)<br>Out: Packer</span></div>
<div><b>Done</b><span class="what">processed by exactly one parcel</span><span class="who">In: Compute backend only (✓ inputs)<br>Out: nobody</span></div>
<div><b>Outputs</b><span class="what">the yellow note: the finished product</span><span class="who">In: Compute backend only (new notes)<br>The yellow note stays here: the game is over</span></div>
</div>

---

<div class="duw-sec">Backup · cards · cut along the dashed lines</div>

# Cards

<div class="ts-cards">
<div class="ts-cut core"><span class="k">Compute backend · round 2 · secret</span><b>A job fails</b><p>Parcel <code>P3 · SIM</code> fails: make no green note and put its seed back in the Simulation Pool.</p><p>When that seed comes back on a new parcel, it works.</p></div>
<div class="ts-cut reco"><span class="k">Packer · round 3</span><b>New Reconstruction packer</b><p><b>3 green</b> <span class="ts-note g"></span><span class="ts-note g"></span><span class="ts-note g"></span> per parcel, instead of 2.</p><p>Once the Feeder says the feed is over, pack what is left.</p></div>
</div>
