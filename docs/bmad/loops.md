# Loops: How BMAD Builds Unattended

!!! tip "TL;DR"
    A loop is a batch job for stories. A plain program (not an AI) picks the next story, starts a fresh AI coding session to build it, checks the result itself (files, git, your tests), sends it to a second, separate AI session for review, checks again, and commits. Then it moves to the next story. The AI never decides whether its own work is done. When a story won't converge, the loop sets it aside and carries on. When something needs a person, it pauses and waits. It works one story at a time, in list order, and its idea of "done" is only as good as the checks you give it.

## Two pieces: a worker and a driver

| Piece | What it is | What it owns |
|---|---|---|
| **Worker:** `bmad-build-auto` (a BMAD skill; called `bmad-dev-auto` before 6.11) | One AI session that clarifies, plans, builds and reviews **one** story, then writes a status into the story's file: `done`, `blocked`, and so on. [V, P15] | Only its own run. It "does not choose the next story, repeat across a backlog, coordinate epics, or run a retrospective." [V, P15] |
| **Driver:** `bmad-loop` (a separate tool, opt-in in the installer since 6.10) | A Python program that reads the plan, starts one worker per story, checks the result, and commits. [V, P43; CHANGELOG v6.10.0] | Which story is next, retries, pauses, commits. "No LLM in the control loop." [V, P43] |

BMAD's docs allow other drivers too: a person, or an ordinary AI coding session acting as the orchestrator. [V, P15] bmad-loop is the one BMAD ships.

The general idea is often called a **"Ralph loop"**: run an agent on the same goal again and again until the work is done. bmad-loop calls itself "a deterministic ralph-loop orchestrator". [V, P43] What it adds is that ordinary code, not the model, decides when to go again and when to stop. [I]

## One story, start to finish

```text
pick the next story          (in plan order; skips done ones)
  │
  ├─ BUILD    fresh AI session runs bmad-build-auto on the story
  │           it plans, codes, self-reviews, marks its file done
  ├─ CHECK    the driver looks for itself: story file status, a real code change,
  │           the plan updated, then YOUR test/lint commands
  │           fail → a fix session gets the error output and tries again
  ├─ REVIEW   a SEPARATE fresh session reviews the finished story
  │           (only when the build asked for one, unless set to always)
  ├─ CHECK    the same checks again
  └─ COMMIT   the driver commits the story itself, then moves on
```

[V, P43 README "How a story flows"]

Four rules make this trustworthy rather than hopeful:

- **The AI's word doesn't count.** A session is finished only when the coding tool's own "stopped" hook fires or its window closes, "never because of what the model writes in its reply". [V, P43]
- **Fresh context for review.** The reviewer never inherits the builder's conversation, and can run on a different tool or model. [V, P43] This is the same idea as BMAD's own review subagents. [I]
- **Your checks decide.** The driver runs the test and lint commands you list (`[verify] commands`) before every commit. [V, P43] If you list none, "done" rests on the AI's file status plus a non-empty diff. [I]
- **Everything has a budget.** Two build attempts and three review rounds per story by default, a 90-minute cap per session, and a nudge then a "stalled" verdict after 10 silent minutes. [V, P43]

## When it can't finish a story on its own

| Situation | What the loop does |
|---|---|
| A story uses up its attempts | **Sets it aside** ("plateau-defer"), notes where the attempt's work was saved, and moves to the next story. [V, P43] **Except in the default setup:** building in place with work left in the tree, the run *pauses* for you to roll back by hand, because `rollback_on_failure` defaults to off. It only moves on by itself with that setting on, a clean tree, or worktree isolation. [V, P43 escalations-guide "Plateau-defer"] |
| The AI reports a **CRITICAL** problem (for example, the plan contradicts itself) | **Pauses the whole run** and notifies you. `bmad-loop resolve` opens an interactive session to fix the spec, then re-runs the story. [V, P43] |
| The AI reports a **PREFERENCE** | Logs it and keeps going. [V, P43] |
| The environment is broken (database down, tool missing, provider outage) | Pauses **without** charging the story an attempt. `resume` rechecks first. [V, P43] |
| The AI tool hits its usage limit | Waits for the reset (up to 5 hours by default) or pauses; can be set to relaunch. [V, P43] |
| The story needs something only a person can do (buy a domain, say) | Commits the AI's part, parks the story at `awaiting-operator`, and continues with other stories. `bmad-loop confirm` finishes it. [V, P43] |
| An epic finishes | By default, pauses so a person can look before the next epic (`per-epic` gate). Other settings: never pause, or also pause after every story's build. [V, P43] |

Before any attempt is thrown away, its commits and uncommitted work are saved on git refs you can restore from. [V, P43]

## Getting a paused run going again

A pause tells you in two places: a desktop notice and a line in the run's `ATTENTION` file. `bmad-loop status` names the stage and the reason. [V, P43 escalations-guide] Which command clears it depends on why it stopped:

| Why it stopped | What you do |
|---|---|
| A gate or checkpoint you configured (epic boundary, spec approval) | `bmad-loop resume` [V, P43] |
| The environment was broken before a session started | Fix it, then `resume`. The checks re-run first. [V, P43] |
| A story escalated (a real problem in the spec) | `bmad-loop resolve`, below. A plain `resume` skips the stuck story, runs the rest of the list, then pauses again. The run is never marked finished while a story is escalated. [V, P43] |

**`resolve` has five ways out**, one per kind of problem: [V, P43 escalations-guide]

- **Fix the spec with an AI's help** (the default). An interactive "resolve agent" opens with the escalation and the frozen spec. You fix the spec together, exit, and confirm the re-arm. The story starts over with fresh budgets.
- **Fix the spec yourself**, then `resolve --no-interactive`. Same re-arm, no agent.
- **Re-apply saved work** (`--restore-patch`). When the build stopped on an intent gap, it saves its patch, and the re-run starts at review rather than rebuilding. In-place runs only.
- **Re-check kept work** (`--reverify`). For an environment fault where the code itself was fine: your test commands re-run on the existing work, with no new build session. A failure is never retried.
- **Take the kept branch as it is** (`--adopt-branch`, worktree runs only). Merges it and marks the story done. The tool warns that review and your test commands are **not** re-run. It's meant for false alarms. [V, P43] It's also the one exit that skips every check the loop exists for. [I]

Two cases worth knowing:

- **A review that overrules the build** doesn't get extra rounds. When review sends a story back after the build marked it done, the loop treats that as a contradiction and escalates. Setting the status back to done by hand doesn't clear it; you resolve it. [V, P43] This is the loop declining to referee two AI sessions that disagree. [I]
- **A parked story isn't reviewed until you confirm it.** Parking at `awaiting-operator` skips the review loop. If the build asked for a follow-up review, that review is still owed after `confirm`, and you run it yourself. [V, P43] So parked work sits unreviewed in the meantime. [I]

Usage limits have their own exit: `resolve --at-reset` waits until the coding tool's limit resets, then re-arms and resumes. Running out of credits never resets by itself, so that one needs a person. [V, P43]

## Where a run keeps its memory

Every session is a fresh AI conversation, so the loop's memory is files on disk, one folder per run: `.bmad-loop/runs/<run-id>/`, gitignored. [V, P43 run-state] This is the "state kept outside the chat" that Lewis lists as one of a loop's five needs (S4, below). [I] The pieces that matter for reading a run: [V, P43 run-state, unless tagged]

- **`state.json`** is the resumable state: stories, phases, tokens, and whether the run is finished, stopped, crashed, or paused (with the reason). `bmad-loop status` reads it.
- **`journal.jsonl`** is an append-only decision log, one JSON line per event, starting with `run-start`. It's the audit trail: every launch, decision, pause and retry. Commands that act on the run (`stop`, `resume`, `resolve`) write to it too.
- **`ATTENTION`** collects plain-text alerts from gates. **`feedback/<story>-<n>.md`** is how a failed check talks to the next attempt: the failure is written down and handed to the next session. A dropped unit's diff is kept in **`failed/<unit>/changes.patch`**, a deferred story's spec in **`deferred/<story>/`**.
- **One folder per AI session** (`tasks/<story>-dev-1`, `-review-2` and so on) holds the prompt it got, its `result.json` verdict, and a heartbeat rewritten about every 30 seconds while it runs. The old result is deleted before a relaunch, so a retry never inherits the last session's verdict.

**Status is derived, first match wins:** finished, paused, stopped, crashed, running (engine alive), interrupted (engine dead), unknown. [V, P43 run-state] So "interrupted" means the engine died without recording why, which is different from a crash it caught. [I]

**Stopping.** `bmad-loop stop` is a hard stop: the engine is signalled and the current session aborted. `stop --graceful` lets the current story finish through its commit, then stops. Both leave the run resumable. On native Windows the engine ignores Ctrl+C, so use `bmad-loop stop`. [V, P43 run-state]

**Cleanup never touches a paused run.** `clean` archives or deletes only finished or stopped runs past retention; paused, crashed and interrupted runs are left alone, and a sweep run holding ledger closes whose code hasn't landed is never removed. [V, P43 run-state] A forgotten paused run therefore sits on disk until someone looks at it. [I]

**Cost and models in the record.** Each session's end row records tokens, split per model, read from the coding tool's own usage file. The model logged at session start is the one *configured*; the models that actually ran come from the transcript at session end, and some tools (Antigravity) report none. The per-model split "never feeds any token total or budget". [V, P43 run-state] So a per-story cost can be rebuilt from the journal, but no report doing that is documented here. [I]

Two side notes: out-of-tree state is keyed to the project's path, so moving the project orphans it; and the docs say to finish or abandon a run before downgrading bmad-loop, because an older version refuses to resume a run it doesn't understand. [V, P43 run-state]

## Deferred work

Builds and reviews find things that aren't the current story's job: a pre-existing bug, a split-off goal, an open question. BMAD's worker reports these as a `deferred` list, "intentionally not a backlog"; the driver decides what to do with them. [V, P15] bmad-loop writes them to a ledger (`deferred-work.md`, entries `DW-1`, `DW-2`...). A **sweep** then triages each entry against the code: already fixed, buildable, blocked, skipped, or a question for you. Buildable entries go through the same build-check-review-commit pipeline. [V, P43] A ledger entry can also block named stories until it's resolved (a `gate:` line). [V, P43]

**How a sweep behaves** (from the sweep guide): [V, P43 sweep-guide]

- It won't start on uncommitted changes. Commit or stash first.
- `--dry-run` lists the open entries without starting any sessions. Use it first.
- **Decisions stay with you.** Run attended, it asks you about each judgment call (build it, close it, or keep it open), with a recommendation, and Enter takes the recommendation. Run unattended (`--no-prompt`), it builds only the bundles that need no decision and leaves the questions open for `bmad-loop decisions` later. It never answers them itself.
- A bundle can't pass review until every ledger entry in it reads `done`.
- `--repeat` re-triages after each cycle to pick up newly deferred work, five cycles by default. An automatic sweep can run per epic or at the end of a run; the default is off.
- A story can close ledger entries itself when it commits (`closes_deferred: [DW-5]` in its spec). A story that fails closes nothing.
- A gate is released only by an explicit `status: done`. A missing or misspelled status still blocks.

**One v6/v7 difference matters for cross-story defects.** On v6, a sweep can pull a retrospective's action items into the ledger as entries. On v7 it can't, because v7 retrospective action items are prose, not records: the sweep files none and logs that ingest was unavailable. [V, P43 sweep-guide "Sweeps on BMAD v7"] So on v7 a retrospective finding reaches the build pipeline only when a person turns it into a ticket or a ledger entry. [I]

## On v7: the ticket tree

bmad-loop has a third mode for BMAD v7, where the plan is a tree of tickets (initiative, epics, tickets) instead of a story list. It is marked **experimental**, built against an unreleased BMAD main that calls itself `6.13.0-next`, and it needs `bmad` and `bmad-build-auto` at 6.13.0 or newer. [V, P43 tickets-guide] Nothing here has been run in this project's lab.

What changes from the v6 modes: [V, P43 tickets-guide, unless tagged]

- **A different planner.** Sofia, the Product Owner agent (`bmad-agent-po`), creates the initiative, slices it into epics and tickets, readies them, replans mid-flight, and runs each epic's closure check. On v7 she replaces `bmad-spec`, `bmad-ticket` and `bmad-correct-course`.
- **Dependencies, not just order.** The driver doesn't read the tree itself. It asks the project's own `tickets.py` what's ready next, and marking a ticket done "unblocks the ticket's dependents". Picks still follow build order among the ready ones.
- **More places to stop before building.** Before each ticket it checks, in order: does an earlier open epic have a `rejected` retrospective (pause), does the ticket need refining (pause), is it a human-in-the-loop ticket (pause), does it carry a plan checkpoint whose story file isn't approved yet (pause). Only then does it dispatch. A `done_checkpoint` ticket pauses after its commit.
- **The epic boundary always stops.** Every finished epic pauses the run at `epic-boundary`, and in a multi-initiative chain "no policy key skips that pause". The retrospective itself only runs with `gates.retrospective = "auto"`; otherwise the verdict is recorded as `unknown` and the run still pauses. A `rejected` verdict holds every later pick until the epic is closed, though fix-up tickets added to that epic still run.
- **Risk sets review depth.** Each ticket carries a risk level; by default (`thorough_review = "high-risk"`) a high-risk ticket gets the thorough review pass.
- **Your repo only.** The tickets must live in a repo store. A tracker store (Jira, Linear and the like) is refused by the preflight and by `tickets.py` itself. A tree spread across several code repositories is refused too.
- **Who marks done.** By default the driver marks a ticket done once it passes verify and review. `mark_done = "never"` leaves it at `built` for a person to mark.

The epic-boundary rule matters most for this project's main finding. In v6 sprint mode the retrospective, the check that caught the cross-story defect in the lab, is optional and never gates the run. [V, P43; V-lab, Experiments 5i, 10] In v7 tickets mode the run can't move into the next epic without stopping, and a rejected retrospective blocks it until someone acts. [V, P43 tickets-guide] That is a real gate at the epic level. It still sees nothing between stories inside an epic, and an auto retrospective only gates if it actually returns `rejected`. [I] The risk field partly fills the "no risk list" gap noted under "What a good goal needs" below, but it changes how hard the review looks, not what the agent may touch. [I]

## What a loop can't see

- **Order, not dependencies.** It runs stories in list order and "does not infer a dependency graph", so put prerequisites first. [V, P15] *v7 tickets mode is different: `tickets.py` tracks which tickets wait on which (see "On v7: the ticket tree").* [V, P43 tickets-guide]
- **One story at a time.** Running several in parallel is planned; today the setting is clamped to 1. [V, P43] Parallel work across a project means separate epic owners or a coordination layer above the loop. [V, P15]
- **Defects that span stories.** Each story is checked on its own. In this project's lab, a defect that crossed stories passed every story-level review and a whole-epic review, and only the retrospective caught it. [V-lab, Experiments 5i, 10; [systemic-findings.md](systemic-findings.md)] In bmad-loop's default sprint mode a retrospective is only *suggested*, and even an automatic one "never gates the run". [V, P43] So the check most likely to catch cross-story problems is the one a loop treats as optional. [I] v7 tickets mode always pauses at the epic boundary and lets a `rejected` retrospective hold later work. [V, P43 tickets-guide]
- **Whether the tests are any good.** The loop trusts your commands. Weak tests mean confident commits of wrong code. [I]
- **Safety.** By default sessions run with the coding tool's permission prompts bypassed. A sandboxed mode exists for Claude Code and Codex on Linux and macOS. bmad-loop's own docs warn that "a worktree is not a security boundary". [V, P43]

## When a loop is worth it

BMAD's author offers four questions before building a heavy loop (secondary: [practitioner-views.md](practitioner-views.md) S3c). Each one maps to a bmad-loop feature: [I]

| Question | Where bmad-loop answers it |
|---|---|
| Does the task recur often enough to justify the setup? | Not a feature. It's your call. |
| Can the system reject bad output automatically? | Your `[verify]` commands. With none, it can't. [V, P43] |
| Can the agent finish the job end to end? | If not, the story parks at `awaiting-operator`. [V, P43] |
| Can "done" be defined beyond taste? | The spec's acceptance criteria, which the driver doesn't check itself. [I] |

The more "no" answers, the more a person should drive, with a good prompt and context instead of a loop. [secondary, S3c] He also frames "loop" as five different things, from an agent's own try-and-test cycle up to the people who decide what the loops work on; bmad-loop is the middle of that range. [secondary, S3c; [I]]

A core contributor describes how he loops in practice (secondary: [practitioner-views.md](practitioner-views.md) S3h). He watches story 1 of an epic closely, because it makes the real design choices, then lets stories 2 to 10 run unattended and reviews the result. About one epic in five gets thrown away at that review, which he accepts because it cost only machine time. He won't loop past one epic, because a bigger diff can't be reviewed. [secondary, S3h] That habit lines up with bmad-loop's default pause at each epic boundary. [V, P43] It also suggests writing epics so their first story carries the design decisions. [I]

## Compared with a loop outside BMAD

Owain Lewis's "Loop Engineering" tutorial is a non-BMAD baseline (secondary: S4, `tutorials/loop-engineering/LESSON.md`, undated). He defines loop engineering as "designing the system around a recurring agent job", and says every loop needs five things: a job, permissions, a schedule, state kept outside the chat, and evaluation. His example is two loops that only talk through GitHub Issues. A *manager* triages tickets, labels risk, and marks only clear low-risk work `agent:ready`. A *worker* takes one ready ticket, works in a fresh worktree, runs tests, has a second agent review the diff, opens a PR, and waits for a person to merge. [secondary, S4]

| | Lewis's baseline | bmad-loop |
|---|---|---|
| Who picks the work | A manager loop labels risk; the worker only takes `risk:low` + `agent:ready` | A person writes the stories; the driver runs them in list order [V, P15] |
| Stuck or unclear | Label `needs:human` with a specific question | The story parks at `awaiting-operator` [V, P43] |
| Found something out of scope | Report it, don't fix it | Deferred work (above) |
| Isolation | Fresh worktree per ticket | Optional worktree per story [V, P43] |
| Where the result lands | A PR; a person approves every merge | Committed (or merged back from the worktree) locally; no PRs opened. By default the run pauses for a person at each epic boundary; `per-story-spec-approval` pauses every story after its verified dev pass, before review and commit [V, P43] |
| First run | Dry run that changes nothing | `bmad-loop run --dry-run` prints the per-story plan and spawns nothing [V, P43] |
| Security caveat | Labels are "routing metadata, not a security boundary" | "A worktree is not a security boundary" [V, P43] |

The two agree on the shape: one job per run, state on disk, a person on anything ambiguous. [I] The real difference is where the human gate sits by default. Lewis puts a person on every change. bmad-loop's default puts one at each epic boundary, so the stories inside an epic land without a person seeing them, and the closest check is the epic retrospective, which bmad-loop treats as optional (see "What a loop can't see"). [I] A per-story gate exists (`[gates] mode = "per-story-spec-approval"`), but it pauses before review rather than before the merge, and it's off by default. [V, P43] *Corrected 2026-11-15: an earlier version of this section said bmad-loop's merge doesn't stop at a person, which contradicted this page's own escalation table above.* Lewis's risk triage step also has no bmad-loop counterpart. Anything in the story list gets run, so the "is this safe to hand off?" judgment happens when a person writes the plan. [I]

### What a good goal needs

Lewis's companion tutorial, "Agent Goals and Loops" (secondary: S4, `tutorials/agent-goals-and-loops/LESSON.md`, undated), separates a prompt (one action), a goal (keep working until an outcome is true), an interval loop (repeat a check), and a schedule (start at a set time). He notes "loop" is mostly a Claude Code feature name for the interval idea. His test for a goal: could a reviewer tell whether it succeeded? If not, rewrite it. He lists six parts, and most map onto a BMAD story: [secondary, S4; mapping [I]]

| Goal part (S4) | In a bmad-loop run |
|---|---|
| Outcome: what should be true | The story's acceptance criteria |
| Evidence: how it's checked | Your `[verify]` commands [V, P43] |
| Boundary: what it may touch | The spec's scope and its Never clause; optional worktree [V, P43] |
| Risk: what's forbidden (auth, billing, secrets, deletes) | No separate risk list. Permission prompts are bypassed by default; `[adapter] permission_mode = "sandboxed"` turns a denied action into an error for the agent instead (Claude Code and Codex on Linux/macOS only) [V, P43] |
| Retry rule | `[limits] max_dev_attempts = 2`, `max_review_cycles = 3` [V, P43] |
| Stop rule: when to ask a person | `awaiting-operator`, the `[gates]` pauses, and CRITICAL escalations, which always pause [V, P43] |

He also bounds every goal with an attempt limit and a time limit (for example three failed deploys, or 60 minutes), and calls out "Merge when done" as an instruction that removes the review gate. [secondary, S4] bmad-loop has both kinds of limit: the attempt caps above and a 90-minute wall clock per session (`session_timeout_min`). [V, P43] Its spend cap is softer. `max_tokens_per_story` (2M weighted tokens) only raises a notice and "the story runs on"; a per-session cap (4M) can end a session only with `session_budget_mode = "enforce"`, and the default is `warn`. [V, P43] The risk row is the clearest gap: a BMAD story says what to build, not what the agent must never touch outside the code, and the sandbox that would enforce it doesn't run on Windows. [I]

All of these live in `.bmad-loop/policy.toml`, which `bmad-loop init` writes and gitignores, so policy is per machine, not shared with the team through the repo. [V, P43, `docs/reference/configuration.md` at `5721f1e`] Two other defaults worth knowing: `[scm] isolation = "none"` (work in place on your checked-out branch), and `rollback_on_failure = false`, so a failed attempt pauses with recovery steps instead of reverting your tree. [V, P43]

## Practical notes

- **Status:** "Early open beta", with breaking changes possible in any pre-1.0 release. [V, P43]
- **Needs:** Python 3.11+, git 2.34+, and a terminal multiplexer (tmux 3.2+); on Windows that means WSL, or an experimental native backend. [V, P43] Works with Claude Code, Codex, Gemini CLI, Copilot CLI and OpenCode, plus Antigravity (experimental). [V, P43]
- **Plans it can read:** v6's `sprint-status.yaml` (default), v6.12's `stories.yaml`, or v7's ticket tree (experimental). [V, P43]
- **Isolation:** optional git worktree per story, merged back locally; no pull requests are opened. [V, P43]

## Not yet checked

- bmad-loop's setup and TUI guides, and the CLI reference. Escalations and sweep were read 2026-11-11, the configuration reference 2026-11-15, the tickets guide 2026-11-17, the run-state reference 2026-11-21.
- Whether BMAD 7.0 ships as 6.13.0. bmad-loop's tickets mode targets main at `6.13.0-next` and requires 6.13.0 or newer, so the version watch should look for 6.13.0 as well as 7.0. [?]
- Tickets mode end to end: Sofia's planning, the per-ticket pauses, and whether an auto retrospective returns `rejected` on the tags epic's B1 defect. Needs v7 installed.
- Any lab run of bmad-loop or `bmad-build-auto`. The natural test is the tags epic from Experiments 5 to 10, which has the cross-story defect (B1): would a loop commit it?
- Whether bmad-loop reports tokens or cost per story (the author's "cost per accepted change" measure, S3c). *Partly answered 2026-11-15: it tracks each story's weighted token spend for its budget checks [V, P43]; whether that shows up as a per-story report isn't checked.* *2026-11-21: the run-state reference shows the journal records tokens per session and per model, so the data exists; no per-story report is documented there.*
- The author says stories within one epic can run in parallel (S3d); bmad-loop clamps parallel runs to 1 today, so that's untested.
- ~~Whether bmad-loop has a dry-run mode, a human gate before merge, and retry or time limits.~~ Answered 2026-11-15 from the configuration reference: `run --dry-run`, `[gates]` and story checkpoints, `[limits]` (see "What a good goal needs"). Still open: no setting pauses *after* review and *before* commit, which is where S4 puts its gate. `done_checkpoint` pauses only after the commit.

---

??? info "About this page"

    *How an autonomous development loop works in BMAD: what runs, what it checks, where it stops for a person, and what it can't see. Sources: BMAD's own loop doc (P15, `docs/build/autonomous-development-loops.md` at v6.12.1) and the bmad-loop repo at commit `795a55a` (2026-11-06; latest tag v0.13.2, 2026-10-09) (P43): `README.md`, `docs/FEATURES.md`, and since 2026-11-11 `docs/escalations-guide.md` and `docs/sweep-guide.md`. Tags: [V, Pxx] traced to those files, [V-lab] seen in this project's lab, [I] inferred, [?] unclear. **No loop has been run in this project's lab.** Written 2026-11-10 on demand (Carl asked to understand loops), extended 2026-11-11 with the escalation and sweep guides, and unattended 2026-11-14 with "When a loop is worth it" from the author's 2026-07-11 video (S3c, secondary), plus one open item from S3d; and on demand 2026-11-15 with "Compared with a loop outside BMAD" from Owain Lewis's Loop Engineering tutorial (S4, secondary), then "What a good goal needs" from his Agent Goals and Loops tutorial (S4, secondary); then the same day bmad-loop's `docs/reference/configuration.md` at commit `5721f1e` (2026-11-15), which filled in the goal table and corrected the merge-gate claim; and unattended 2026-11-17 with "On v7: the ticket tree" from `docs/tickets-guide.md` at `5721f1e`; and on demand 2026-11-20 with a contributor's epic-at-a-time habit (S3h, secondary) in "When a loop is worth it"; and unattended 2026-11-21 with "Where a run keeps its memory" from `docs/reference/run-state.md` at `origin/HEAD` `8224d53` (2026-11-16); not reviewed.*
