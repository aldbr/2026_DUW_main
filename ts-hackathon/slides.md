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
  <div class="ts-board out"><b>Finished</b><span>1 yellow note <code>M1</code>: shout <b>“Completed!”</b></span></div>
</div>

<div class="ts-looptitle">On every board, each parcel makes the same trip</div>

<div class="ts-scope"><span class="per">one per transformation: the board's player</span><span class="shared">shared by all transformations</span></div>

<div class="ts-loop">
  <span class="ts-who">Feeder</span><span class="arr">→</span>
  <span class="ts-where">Pool</span><span class="arr">→</span>
  <span class="ts-who">Packer</span><span class="arr">→</span>
  <span class="ts-where">Ready</span><span class="arr">→</span>
  <span class="ts-who">Dispatcher</span><span class="arr">→</span>
  <span class="ts-who">Compute backend</span><span class="arr">→</span>
  <span class="ts-who">Completion</span><span class="arr">→</span>
  <span class="ts-where">✓ Done<small>new notes → Outputs</small></span>
</div>
<div class="ts-retry"><span>✗ the note goes back to the Pool, a <b>new</b> parcel takes it</span></div>

<div class="ts-legend">
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
      <li>8 seeds → 8 green → 4 blue → <b>1 yellow <code>M1</code></b>.</li>
      <li>Shout <b>“Completed!”</b> when <code>M1</code> is in Merge's Outputs.</li>
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
      <li>Shout <b>“Completed!”</b> when <code>M1</code> is in Merge's Outputs.</li>
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
      <li><b>Change seats:</b> the observers come in, two players step out. Everyone else moves one seat to the left and takes the sheet in front of them.</li>
      <li>Reconstruction receives a <b>new version of its packer plugin</b>.</li>
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
  <tr><td>Board players: feeding</td><td>Feeder, edge feeder</td></tr>
  <tr><td>Board players: packing</td><td>Packer</td></tr>
  <tr><td>Dispatcher, Compute backend</td><td>Dispatcher, dummy backend</td></tr>
  <tr><td>Completion</td><td>Completion: done, failed, split</td></tr>
  <tr><td>Nobody kept the books</td><td>Database, state machines, counters</td></tr>
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

### One table of 8, two observers

- Sticky notes: red <span class="ts-note r"></span>, green <span class="ts-note g"></span>, blue <span class="ts-note b"></span> and yellow <span class="ts-note y"></span> pads (pink too, for the 1-2-4-All)
- 8 red notes written in advance: <code>S1</code> … <code>S8</code>
- Pens, scrap paper cut in quarters (the parcels)
- 3 boards, the role sheets (Compute backend: one per executor), the two cards on the last page
- 6 players: one of each role. 7 to 8: the Compute backend gets a second and a third executor.

</div>
<div>

<table class="duw-map"><tbody>
  <tr><th>Time</th><th>Step</th></tr>
  <tr><td>3 min</td><td>Explain the game</td></tr>
  <tr><td>5 min</td><td>Read sheets, set up the table</td></tr>
  <tr><td>7 min</td><td>Round 1, happy path</td></tr>
  <tr><td>2 + 7 min</td><td>Reset, round 2, a surprise failure</td></tr>
  <tr><td>2 + 7 min</td><td>Reset, round 3, new seats and new packer rule</td></tr>
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

<div class="ts-spots">
  <div><b>Seed stack</b><span class="ts-note r"></span> S1 … S8, written in advance</div>
  <div><b>Ready</b>parcels waiting for the Dispatcher</div>
  <div><b>Backend seat</b><span class="ts-note g"></span><span class="ts-note b"></span><span class="ts-note y"></span> pads, pens; 1 to 3 executors</div>
  <div><b>Bin</b>every used parcel, done or failed. Never reused.</div>
</div>

<div class="duw-two mt-4">
<div class="duw-small"><b>A parcel</b> is a quarter sheet with the input notes stuck on it (<code>P5 · RECO</code>). After the job: ✓ inputs go to Done, ✗ inputs go back to their Pool, the empty parcel goes to the Bin.</div>
<div class="duw-small"><b>A note's name</b> says where it comes from: <code>G3</code> is the green file made from seed <code>S3</code>; <code>B1 = G3 + G5</code>.</div>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Simulation

<div class="ts-role sim">
<div class="side"><div class="real">You play the Simulation transformation's two plugins: its <b>feeder</b> and its <b>packer</b>. Each transformation has its own.</div><div class="real"><b>You hold:</b> the seed stack S1 … S8, paper quarters, a pen.</div></div>
<ol>
  <li><b>Feed:</b> put seeds <span class="ts-note r"></span> from the stack into your Pool, two or three at a time.</li>
  <li>When the stack is empty, say aloud: <b>“Simulation feed is over.”</b></li>
  <li><b>Pack:</b> 1 seed per parcel. Write <code>P1 · SIM</code> (then P2…) on a paper quarter, stick the seed on it, put it on <b>Ready</b>.</li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Reconstruction

<div class="ts-role reco">
<div class="side"><div class="real">You play the Reconstruction transformation's feeder and packer. Your feeder is an <b>edge feeder</b>: its inputs are the outputs of Simulation.</div><div class="real"><b>You hold:</b> paper quarters, a pen. Your packer rule may change in round 3.</div></div>
<ol>
  <li><b>Feed:</b> move each <span class="ts-note g"></span> green note from the Simulation Outputs into your Pool.</li>
  <li>When Simulation's feed is over, its <b>Done holds all 8 seeds</b> and its Outputs is empty, say: <b>“Reconstruction feed is over.”</b></li>
  <li><b>Pack:</b> 2 green <span class="ts-note g"></span><span class="ts-note g"></span> per parcel (<code>P7 · RECO</code>), on Ready. Not enough notes? Wait. Once your feed is over, pack what is left.</li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Merge

<div class="ts-role merge">
<div class="side"><div class="real">You play the Merge transformation's feeder and packer. Your feeder is an <b>edge feeder</b>: its inputs are the outputs of Reconstruction.</div><div class="real"><b>You hold:</b> paper quarters, a pen.</div></div>
<ol>
  <li><b>Feed:</b> move each <span class="ts-note b"></span> blue note from the Reconstruction Outputs into your Pool.</li>
  <li>When Reconstruction's feed is over, its <b>Done holds all 8 green notes</b> and its Outputs is empty, say: <b>“Merge feed is over.”</b></li>
  <li><b>Pack:</b> 4 blue <span class="ts-note b"></span><span class="ts-note b"></span><span class="ts-note b"></span><span class="ts-note b"></span> per parcel (<code>P12 · MERGE</code>), on Ready. Not enough notes? Wait. Once your feed is over, pack what is left.</li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Dispatcher

<div class="ts-role core">
<div class="side"><div class="real">In the real system: the part that hands each parcel to a backend. There can be several backends; the dispatcher chooses one.</div><div class="real"><b>You hold:</b> nothing.</div></div>
<ol>
  <li>Take the oldest parcel on <b>Ready</b>.</li>
  <li>Give it to an executor of the Compute backend that is <b>free</b>: no parcel in its hands.</li>
  <li>If every executor is busy, wait with the parcel. Never give an executor two parcels.</li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Compute backend

<div class="ts-role core">
<div class="side"><div class="real">In the real system: where jobs run. All three transformations send their jobs here; the boards only keep the books. You are one <b>executor</b>: one parcel at a time.</div><div class="real"><b>You share:</b> the <span class="ts-note g"></span> <span class="ts-note b"></span> <span class="ts-note y"></span> pads, pens. If the backend gets a card, read it in secret.</div></div>
<ol>
  <li><b>SIM</b> parcel: for seed <code>S3</code>, write a green <span class="ts-note g"></span> <code>G3</code> and stick it on the parcel.</li>
  <li><b>RECO</b> parcel: for two green notes, write one blue <span class="ts-note b"></span> <code>B1 = G3 + G5</code>.</li>
  <li><b>MERGE</b> parcel: for the blue notes, write one yellow <span class="ts-note y"></span> <code>M1 = B1 + B2 + B3 + B4</code>.</li>
  <li>Write <b>✓</b> next to each input that worked (<b>✗</b> if not), then give the parcel to the Completion.</li>
</ol>
</div>

---

<div class="duw-sec">Backup · role sheet</div>

# Completion

<div class="ts-role core">
<div class="side"><div class="real">In the real system: the step that reads the job's report and decides what happens to each input.</div><div class="real"><b>You hold:</b> nothing.</div></div>
<ol>
  <li><b>✓</b> input: put it in the <b>Done</b> column of its board. Put the new notes in <b>Outputs</b>.</li>
  <li><b>✗</b> input: put it back in the <b>pool</b> of its board. The Packer will make a new parcel.</li>
  <li>Put the empty parcel in the <b>Bin</b>. A parcel is never reused.</li>
  <li>When <code>M1</code> is in Merge's Outputs, every Pool and Ready are empty and nobody holds a parcel, shout <b>“Completed!”</b></li>
</ol>
</div>

---

<div class="duw-sec">Backup · board</div>

# Simulation board

<div class="ts-mat-sub">1 red per parcel · print on A4 landscape</div>

<div class="ts-mat sim">
<div><b>Pool</b><span class="what">waiting to be packed</span><span class="who">In: Simulation (seeds), Completion (✗ inputs)<br>Out: Simulation, when packing</span></div>
<div><b>Done</b><span class="what">processed by exactly one parcel</span><span class="who">In: Completion only (✓ inputs)<br>Out: nobody</span></div>
<div><b>Outputs</b><span class="what">green notes, for the next board</span><span class="who">In: Completion only (new notes)<br>Out: Reconstruction takes the green notes</span></div>
</div>

---

<div class="duw-sec">Backup · board</div>

# Reconstruction board

<div class="ts-mat-sub">2 green per parcel · print on A4 landscape</div>

<div class="ts-mat reco">
<div><b>Pool</b><span class="what">waiting to be packed</span><span class="who">In: Reconstruction (green notes), Completion (✗ inputs)<br>Out: Reconstruction, when packing</span></div>
<div><b>Done</b><span class="what">processed by exactly one parcel</span><span class="who">In: Completion only (✓ inputs)<br>Out: nobody</span></div>
<div><b>Outputs</b><span class="what">blue notes, for the next board</span><span class="who">In: Completion only (new notes)<br>Out: Merge takes the blue notes</span></div>
</div>

---

<div class="duw-sec">Backup · board</div>

# Merge board

<div class="ts-mat-sub">4 blue per parcel · print on A4 landscape</div>

<div class="ts-mat merge">
<div><b>Pool</b><span class="what">waiting to be packed</span><span class="who">In: Merge (blue notes), Completion (✗ inputs)<br>Out: Merge, when packing</span></div>
<div><b>Done</b><span class="what">processed by exactly one parcel</span><span class="who">In: Completion only (✓ inputs)<br>Out: nobody</span></div>
<div><b>Outputs</b><span class="what">the yellow <code>M1</code>: the finished product</span><span class="who">In: Completion only (new notes)<br><code>M1</code> stays here: the game is over</span></div>
</div>

---

<div class="duw-sec">Backup · cards · cut along the dashed lines</div>

# Cards

<div class="ts-cards">
<div class="ts-cut core"><span class="k">Compute backend · round 2 · secret</span><b>A job fails</b><p>Parcel <code>P3 · SIM</code> fails: write ✗ next to its seed, make no green note, pass the parcel on as usual.</p><p>When that seed comes back on a new parcel, it works.</p></div>
<div class="ts-cut reco"><span class="k">Reconstruction · round 3</span><b>New packer version</b><p><b>3 green</b> <span class="ts-note g"></span><span class="ts-note g"></span><span class="ts-note g"></span> per parcel, instead of 2.</p><p>Once your feed is over, pack what is left.</p></div>
</div>
