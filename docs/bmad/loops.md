# Loops: How BMAD Builds Unattended

*How an autonomous development loop works in BMAD: what runs, what it checks, where it stops for a person, and what it can't see. Sources: BMAD's own loop doc (P15, `docs/build/autonomous-development-loops.md` at v6.12.1) and the bmad-loop repo at commit `795a55a` (2026-11-06; latest tag v0.13.2, 2026-10-09) (P43): `README.md`, `docs/FEATURES.md`, and since 2026-11-11 `docs/escalations-guide.md` and `docs/sweep-guide.md`. Tags: [V, Pxx] traced to those files, [V-lab] seen in this project's lab, [I] inferred, [?] unclear. **No loop has been run in this project's lab.** Written 2026-11-10 on demand (Carl asked to understand loops), extended 2026-11-11 with the escalation and sweep guides; not reviewed.*

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

## What a loop can't see

- **Order, not dependencies.** It runs stories in list order and "does not infer a dependency graph", so put prerequisites first. [V, P15]
- **One story at a time.** Running several in parallel is planned; today the setting is clamped to 1. [V, P43] Parallel work across a project means separate epic owners or a coordination layer above the loop. [V, P15]
- **Defects that span stories.** Each story is checked on its own. In this project's lab, a defect that crossed stories passed every story-level review and a whole-epic review, and only the retrospective caught it. [V-lab, Experiments 5i, 10; [systemic-findings.md](systemic-findings.md)] In bmad-loop's default sprint mode a retrospective is only *suggested*, and even an automatic one "never gates the run". [V, P43] So the check most likely to catch cross-story problems is the one a loop treats as optional. [I]
- **Whether the tests are any good.** The loop trusts your commands. Weak tests mean confident commits of wrong code. [I]
- **Safety.** By default sessions run with the coding tool's permission prompts bypassed. A sandboxed mode exists for Claude Code and Codex on Linux and macOS. bmad-loop's own docs warn that "a worktree is not a security boundary". [V, P43]

## Practical notes

- **Status:** "Early open beta", with breaking changes possible in any pre-1.0 release. [V, P43]
- **Needs:** Python 3.11+, git 2.34+, and a terminal multiplexer (tmux 3.2+); on Windows that means WSL, or an experimental native backend. [V, P43] Works with Claude Code, Codex, Gemini CLI, Copilot CLI and OpenCode, plus Antigravity (experimental). [V, P43]
- **Plans it can read:** v6's `sprint-status.yaml` (default), v6.12's `stories.yaml`, or v7's ticket tree (experimental). [V, P43]
- **Isolation:** optional git worktree per story, merged back locally; no pull requests are opened. [V, P43]

## Not yet checked

- bmad-loop's tickets, setup and TUI guides, and the configuration reference. Escalations and sweep were read 2026-11-11.
- Any lab run of bmad-loop or `bmad-build-auto`. The natural test is the tags epic from Experiments 5 to 10, which has the cross-story defect (B1): would a loop commit it?
- The author's "5 fundamentals" video on loops (S3). Its transcript was pulled 2026-11-11 and is next in line to read.
