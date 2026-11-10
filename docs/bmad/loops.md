# Loops: How BMAD Builds Unattended

*How an autonomous development loop works in BMAD: what runs, what it checks, where it stops for a person, and what it can't see. Sources: BMAD's own loop doc (P15, `docs/build/autonomous-development-loops.md` at v6.12.1) and the bmad-loop repo's `README.md` and `docs/FEATURES.md` at commit `795a55a` (2026-11-06; latest tag v0.13.2, 2026-10-09) (P43). Tags: [V, Pxx] traced to those files, [V-lab] seen in this project's lab, [I] inferred, [?] unclear. **No loop has been run in this project's lab.** Written 2026-11-10 on demand (Carl asked to understand loops); not reviewed.*

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
| A story uses up its attempts | **Sets it aside** ("plateau-defer"), notes where the attempt's work was saved, and moves to the next story. [V, P43] |
| The AI reports a **CRITICAL** problem (for example, the plan contradicts itself) | **Pauses the whole run** and notifies you. `bmad-loop resolve` opens an interactive session to fix the spec, then re-runs the story. [V, P43] |
| The AI reports a **PREFERENCE** | Logs it and keeps going. [V, P43] |
| The environment is broken (database down, tool missing, provider outage) | Pauses **without** charging the story an attempt. `resume` rechecks first. [V, P43] |
| The AI tool hits its usage limit | Waits for the reset (up to 5 hours by default) or pauses; can be set to relaunch. [V, P43] |
| The story needs something only a person can do (buy a domain, say) | Commits the AI's part, parks the story at `awaiting-operator`, and continues with other stories. `bmad-loop confirm` finishes it. [V, P43] |
| An epic finishes | By default, pauses so a person can look before the next epic (`per-epic` gate). Other settings: never pause, or also pause after every story's build. [V, P43] |

Before any attempt is thrown away, its commits and uncommitted work are saved on git refs you can restore from. [V, P43]

## Deferred work

Builds and reviews find things that aren't the current story's job: a pre-existing bug, a split-off goal, an open question. BMAD's worker reports these as a `deferred` list, "intentionally not a backlog"; the driver decides what to do with them. [V, P15] bmad-loop writes them to a ledger (`deferred-work.md`, entries `DW-1`, `DW-2`...). A **sweep** then triages each entry against the code: already fixed, buildable, blocked, skipped, or a question for you. Buildable entries go through the same build-check-review-commit pipeline. [V, P43] A ledger entry can also block named stories until it's resolved (a `gate:` line). [V, P43]

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

- bmad-loop's other guides (escalations, sweep, tickets, configuration) beyond what README and FEATURES summarize.
- Any lab run of bmad-loop or `bmad-build-auto`. The natural test is the tags epic from Experiments 5 to 10, which has the cross-story defect (B1): would a loop commit it?
- The author's "5 fundamentals" video on loops (S3, not yet pulled).
