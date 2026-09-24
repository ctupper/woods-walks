# `bmad-build` Step by Step

> **Re-verified against the v6.12.0 release (2026-09-19).** This page was first written from a later, unreleased clone (`f033e70`). The route, review, and step-3 sections below were re-read from the release tag (`labs\BMAD-METHOD-v6.12.0\src\bmm-skills\ship\bmad-build`, identical to the installed skill) and rewritten. The clone-only differences are kept in the last section. Tags [V, P18r] mean the release-tag files.

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-build/` (source ID P18, see `../sources.md`). Tags: [V, P18] traced to the skill's own files, [I] inferred, [?] unclear. Read from the files only; not yet observed in a lab run except where marked [V-lab]. Written unattended 2026-09-19.*

This page is the mechanism behind the "Build and verify" stage in `flow.md`. That page says what `bmad-build` does. This one says how the skill is put together.

## How it starts

- `SKILL.md` is only a launcher. It runs `uv run ... _bmad/scripts/render_skill.py` once, which renders the skill's templates with the `customize.toml` values and prints the path of a rendered `workflow.md`. If `uv` is missing it halts. [V, P18]
- **The release `SKILL.md` takes no route or review arguments.** It runs the launcher and follows the rendered workflow. (The clone added `--set workflow.route` / `workflow.review`.) [V, P18r]
- `workflow.md` is a step-file workflow: read one step file at a time, in order, and halt at checkpoints for the human. Steps carry state in the spec's frontmatter. [V, P18]
- Goal stated there: "Turn user intent into a hardened, reviewable artifact." [V, P18]

## Two standards the whole run is judged against

- **Ready for Development:** every task has a file path and action, ordered by dependency, acceptance criteria in Given/When/Then, no placeholders or TBDs, no unresolved gaps or contradictions. [V, P18]
- **Scope:** one user-facing goal, 900 to 1600 tokens. "Neither limit is a gate"; both are proposals the user can override. Multi-goal means two or more independently shippable deliverables. [V, P18]

## The steps

| Step | What it does | Human checkpoint |
|---|---|---|
| 1 Clarify and route | Resolves state: explicit spec path, else recent conversation, else scans for active specs and asks. Loads planning artifacts (an epic-story gets a cached `epic-<N>-context.md`, compiled by a subagent if stale). Halts if the git tree is dirty. Multi-goal check; splits go to `deferred-work.md`. Picks the spec filename. | Dirty tree; multiple goals; which spec to resume |
| 2 Plan | Investigates the codebase, writing findings into the spec's Code Map. Chooses route. Fills the spec template, self-reviews against Ready for Development. Open Questions must be answered by the human. | Open Questions; token-count split; **Checkpoint 1: approve** |
| 3 Implement | Records `baseline_commit`, sets status `in-progress`, dispatches implementation to a subagent (or does it directly if none). Stages the diff to a temp file and reads it ("judge against the diff, not against the implementation subagent's report"). Verifies every task in the spec is done and every acceptance criterion is satisfied, ticking tasks `[x]`. Audits the I/O & Edge-Case Matrix: every row needs a test that actually ran and passed. [P18r] | Only if a matrix row is ambiguous |
| 4 Review | Sets status `in-review`. Runs review lenses as parallel subagents against the diff file. Triage, then route findings. | Loopbacks, or after 5 loops |
| 5 Present | Sets status `done`, makes a **local commit** if the tree is dirty, prints a one or two sentence summary, offers PR or walkthrough. Never pushes. | None |

All [V, P18]. Step 1 and 2 check `status` frontmatter (`draft`, `ready-for-dev`, `in-progress`, `in-review`, `done`) so a run can resume mid-way. [V, P18]

## Route choice: oneshot vs dispatch

At the release, step 2 investigates the codebase, then "writes down three facts about the plan, as it is now, not as a guess": [V, P18r]

- **Intent gaps:** things the request does not say, the code cannot settle, and the user would notice in the result. Only the human can answer these. Choices the user would not notice are the skill's to decide and record.
- **Irreversibles:** migrations, data deletion or mutation, external side effects, deploy or config triggers.
- **Footprint:** files to change, and anything new that other code will call or depend on.

**No intent gaps, nothing irreversible, and a small change: `route: oneshot`.** The skill writes a minimal spec (frontmatter, Intent inside the frozen block, Implementation Notes; every other section deleted), sets status `in-progress`, and goes straight to `step-oneshot.md`: implement in the same session, review, classify, present. **Otherwise the full spec is written and `route: dispatch`**: Code Map, Open Questions, tasks, and the step 3 subagent handoff. [V, P18r]

- This is exactly the docs' "three checks: intent gaps, irreversible actions, footprint" (`flow.md`). Experiment 2 took the dispatch path and left `route: dispatch` in its spec. [V, P18r; V-lab]
- A oneshot run that discovers something step 2 missed stops and replans: the request left out something the user would notice, it needs something irreversible, or the change is growing beyond the plan. It records the trigger in Implementation Notes, restores Code Map and Open Questions, sets `route: dispatch` and `status: draft`, and returns to step 2 step 6. [V, P18r]
- The clone replaced this gate with `route` and `review` settings and a line-count estimate ("100 lines or fewer: oneshot"); that is not in the release. [V, clone `customize.toml`]

## Review: the part with the most machinery

- Review layers run as subagents at the same model level as the session, launched together and awaited in the same turn. At the release there is no quick/thorough choice: the **dispatch** route runs `workflow.review_layers` (three layers), and the **oneshot** route runs `workflow.oneshot_review_layers` (**Blind Hunter only**). [V, P18r]
- Reviewers' own severity ratings are discarded. The main session verifies each finding at the cited location and gives exactly one verdict: `high`, `medium`, `low`, `false`, or `maybe-false`. Every finding gets a row in a `## Review Triage Log` in the spec; none may be dropped. [V, P18]
- Survivors are grouped by shared root cause and routed to one of four categories: **intent_gap** (frozen intent incomplete; revert code, ask the human, re-plan), **bad_spec** (the spec should have prevented it; revert, amend the non-frozen sections, log it in `## Spec Change Log`, re-implement), **patch** (trivial fix; send back to the same implementer subagent), **defer** (pre-existing; append to `deferred-work.md`). [V, P18]
- Loopbacks are capped: `review_loop_iteration` above 5 halts and escalates to the human. [V, P18]
- Two guard rules: a finding whose fix would edit this build's spec is rejected, and a finding whose fix edits agent-context files (CLAUDE.md, AGENTS.md) is deferred. [V, P18]
- Without subagents, the workflow writes each lens's full prompt to a file and halts, asking the human to run it in a separate session (ideally a different LLM) and paste the findings back. [V, P18]

## The review layers (what each subagent is told)

Definitions live in `customize.toml` and `review-prompts/`. [V, P18r]

| Route | Layers |
|---|---|
| oneshot | **Blind Hunter** only. |
| dispatch | **Blind Hunter**, **Edge Case Hunter**, **Verification Gap Reviewer**, run together. |

- **Blind Hunter:** sees only the diff, no spec. Told to look for what is missing, with a finding floor N = min(floor(sqrt(kB)+1), 10) from diff size, and not to stop at zero findings. [V, P18r; the first-pass text came from the clone and matches]
- **Edge Case Hunter:** a "pure path tracer" that lists only unhandled branches; reads the spec's claims only after tracing, then tests each claim ("exactly as X does") against the code. Adds a deletion check when code was removed. [V, P18r]
- **Verification Gap Reviewer:** asks whether the changed behavior could break without any test failing (regression gap, missing-adoption gap, broken-verification gap); must read a test before claiming what it covers. Its gap findings arrive pre-verified. [V, P18r]
- There is no Intent Alignment or Quick layer at the release. Those are clone-only. `bmad-code-review` (a separate skill) adds an Acceptance Auditor when a spec exists. [V, P18r; V-lab]
- Every layer is told it is the reviewer: no skills, no sub-subagents, return findings as text. Layers report no severity; the main session assigns verdicts (see above). [V, P18r]
- Information is withheld on purpose: Blind Hunter never sees the spec, the Edge Case Hunter sees the claims last, and the spec is "the change's own account of itself," testimony not evidence. [V, P18r] Intent: prevent reviewers from inheriting the author's assumptions. [I]
- Layers are overridable: `instruction` can run anything (an external reviewer via bash), an empty `instruction` disables a layer, a new `id` appends. [V, P18r]

## The spec file (template)

`spec-template.md` sets the artifact `bmad-build` writes and updates. [V, P18]

- **Frontmatter (release):** title, `type` (feature, bugfix, refactor, chore), date, `status`, `route` (`oneshot` or `dispatch`), `review_loop_iteration`, optional `context:` list of project docs the implementer loads itself. (The clone added `route_source`, `review`, `review_source`, `lenses_ran`.) [V, P18r]
- **Human-owned (frozen after approval):** Intent (Problem, Approach), Boundaries and Constraints (Always / Never), an I/O and Edge-Case Matrix.
- **Agent-owned:** Code Map, Tasks and Acceptance (file, action, rationale; Given/When/Then), Implementation Notes (append-only), Spec Change Log (append-only, filled on bad_spec loopbacks), Review Triage Log (append-only, every pass), Design Notes, Verification (commands with expected results).
- Target size 900 to 1300 tokens; over 1600 is flagged as context-rot risk. Oneshot specs drop Boundaries, Matrix, Code Map, Tasks, and Design Notes. "Never over-specify how" (boundaries and examples instead). [V, P18]

## The frozen block

Everything inside `<frozen-after-approval>` in the spec is locked after approval. Only the human changes it. Implementation, review, and patching must not edit it. [V, P18] This is how BMAD keeps intent from drifting as code is re-derived. [I]

## Where a human is pulled in

Partial answer to the STATE.md open question "where does a human get pulled in" (from the files, not a run). From the step files: dirty git tree, choosing among multiple goals, choosing among active specs, Open Questions, token count over 1600, Checkpoint 1 approval, an ambiguous matrix row, an intent_gap finding, a loopback past 5, missing subagents for review. [V, P18] Everything else runs without asking. [I]

## Overlap with lab findings

- Experiment 2 ran this workflow and logged that the commit step did not happen because of Carl's global confirm-before-committing rule. Step 5 says to commit locally when the tree is dirty, so that is a real conflict between a user rule and BMAD's default. [V-lab, `lab-log.md`; V, P18] **Confirmed again on every story of a four-story epic (Experiment 5h):** the presentation step said each time it would normally commit, and correctly attributed skipping it to the standing rule rather than silently doing nothing. Commits happened afterward as a separate human action, never as part of the workflow. [V-lab]
- **The dirty-tree checkpoint fires with an unscripted question, not boilerplate.** Story 2 of Experiment 5h halted at step 1 because story 1's work was uncommitted, and rather than a fixed message it reasoned through the options itself (commit first, build on the mixed diff, or branch/stash) and asked which the human wanted. The workflow gives step 1 no set wording for this case; the question was the model's own judgment, not a template. [V-lab]
- **A review finding raised and rejected three separate times, across three different stories, was self-flagged.** Across Experiment 5h's stories 1 to 3, three independent review passes each raised the same finding (a note with a non-array `tags` field would substring-match a filter) and it was rejected each time on the same grounds. On the third occurrence the build told the human, unprompted, that being raised three times independently made this "the most likely place my reasoning is wrong" — noticing its own repeated dismissal and surfacing that as a signal, rather than just repeating the dismissal a fourth time. Not seen in Experiments 2 or 3, where review variance existed but nothing flagged a pattern in its own verdicts. [V-lab]
- **A deferred finding was verified empirically before being filed, with a runnable repro.** Story 4's `deferred-work.md` entry (the `nextId` id-reuse issue predicted as early as story 1's Design Notes) states the reproduction steps directly: create three notes, remove the highest-numbered one, add a new note, and the new note's id resolves an old lookup to the wrong record. It was correctly left deferred rather than fixed, because the frozen spec's Never clause barred changing `nextId` inside that story. [V-lab]
- **Whether a finding gets routed to `patch` or `HALT` depends on what documented context exists to weigh it against, not just the finding itself (Experiment 4b).** The same id-reuse bug, found by the same reviewer type, was a quiet `deferred-work.md` note with no `AGENTS.md` present and a routed `HALT` once one existed pinning the store's exact shape — the triage log named the pinned contract as the reason the fix was non-trivial. Context that exists to be checked against is what turns "deferrable" into "ask the human." [V-lab]
- **Headless `claude -p` does spawn both implementation and review subagents, when given explicit permission.** Step 1's "ask once for the whole workflow run" subagent gate fired mid-build in Experiment 5h (dispatch route); once answered yes, review ran three parallel layers and the presentation step's findings distinguish reviewer-found issues from the main session's own triage, consistent with independent subagents rather than one session role-playing several. [V-lab; resolves the open question below]

## Not yet checked

- `compile-epic-context.md` and `sync-sprint-status.md`; the second half of the Edge Case Hunter and Verification Gap prompts (output formats). [?]

## What the clone changed (kept for the record; all clone-only)

Method: `diff -r --strip-trailing-cr` of a fresh `npx bmad-method install` (`labs\lab3-review\.claude\skills`) against `labs\BMAD-METHOD\skills` at `f033e70`. The installer writes CRLF, so a plain diff shows every file as changed; normalizing that leaves the real differences. [V-lab]

| Skill | Real differences | Effect on the wiki |
|---|---|---|
| `bmad-build` | 16 files. Installed: `route` is `oneshot` or `dispatch`, chosen by a route gate in step 2 on three facts (intent gaps, irreversibles, footprint); review is a single `review_layers` list of three layers; no route/review invocation arguments. Clone: `oneshot`/`full`, `route` and `review` settings, a line-count route rule, quick/thorough lens sets plus an Intent Alignment lens, `lenses_ran` and `review_source` frontmatter. | Route and review claims on this page are clone-only, marked above. Explains Experiment 2's unexplained `route: dispatch`. |
| `bmad-code-review` | Installed: `steps/` folder, four `review_layers` (Blind Hunter, Edge Case Hunter, Verification Gap, Acceptance Auditor gated on a spec), no quick/thorough. Clone: step files at top level, `review = "thorough"`, quick/thorough lens sets. | `agents.md` code-review bullet and the docs page it cites (P14) describe the clone. Marked. |
| `bmad-spec`, `bmad-prd`, `bmad-architecture`, `bmad-ux` | `SKILL.md` activation lines only: installed loads `user_name` / `communication_language` config and greets by name; the clone dropped those. `lint_spine.py` differs in formatting and a Python floor (3.10 installed, 3.11 clone). One example file and one comment line differ. Spec assets and templates are identical. | Substantive claims stand. |
| Five agents | `SKILL.md` config-loading lines only (same language-config change); `customize.toml` identical. | Persona claims stand. |

Reading: the clone is a later snapshot of main. It removed the language config from activation and reworked build/review (route setting, quick/thorough). The npm release is what a user gets today. [I]

**Still unchecked:** other skills not diffed (`bmad-sprint-planning`, `bmad-retrospective`, `bmad-build-auto`, `bmad-correct-course`, deep-recon, and others), and the docs pages P1 to P17, which came from the clone's `docs/` and may describe unreleased behavior. [?]

### Re-pin result (2026-09-19)

The installed 29 skills are **byte-identical (CRLF-normalized) to the `v6.12.0` git tag** (commit `05bfbd4`, which is also the npm package's `gitHead`). Skills at the tag live under `src/bmm-skills/...`, not the top-level `skills/` of the clone. A worktree of the tag is at `C:\Users\ctupp\labs\BMAD-METHOD-v6.12.0`. So the installed behavior *is* the release; the clone at `f033e70` is a later main snapshot. [V-lab] The marks that were on this page have been resolved against the tag; see the top note. [I]
