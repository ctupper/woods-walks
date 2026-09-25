# BMAD Glossary

*Describes BMAD-METHOD v6.12.0. Each entry points to the wiki page where the term is sourced; tags and source IDs live there. Definitions restate what those pages already tag [V]; nothing new was read for this page. Draft written unattended 2026-09-19; reviewed by Carl 2026-09-24, when terms from the later experiments were added.*

**AD (architecture decision).** One numbered block in an architecture spine (`AD-1`, `AD-2`...) with Binds, Prevents, and Rule. IDs are stable and never reused. See `architecture-skill.md`.

**Addendum (`addendum.md`).** Side file holding depth that doesn't fit the PRD (rejected alternatives, technical-how, sizing data). See `prd-skill.md`.

**Adopted companion.** A companion written by another skill (such as `DESIGN.md` from UX) that the spec references but never edits. See `spec-skill.md`.

**Agent.** A named persona (Mary, John, Winston, Sally, Amelia) that routes to skills through a short-code menu. Mostly identity, style, and principles plus a menu. See `agents.md`.

**Altitude.** How high a spine sits: initiative (keeps features coherent), feature (keeps epics), epic (keeps stories). See `architecture-skill.md`.

**Baseline commit.** The git commit recorded in a build spec's frontmatter before any change, so review can diff against it. See `build-step-by-step.md`.

**Build-auto (`bmad-build-auto`).** Unattended worker that runs one unit of work and ends with a machine-readable status. See `agents.md`.

**CAP-N.** Stable ID of a capability in `SPEC.md`. Never reused or renumbered. See `spec-skill.md`.

**Capability.** A spec entry with an `intent` (what can be done, not how) and a testable `success` condition. See `spec-skill.md`.

**Checkpoints (`spec_checkpoint`, `done_checkpoint`).** Per-story fields in `stories.yaml`, read by the dispatcher and never by the dev skill. `spec_checkpoint` means a human reviews the story spec before implementation; `done_checkpoint` is the pause at completion. In the lab, a `spec_checkpoint` passed through with nothing recorded, since nothing requires the review to resolve anything. See `spec-skill.md`.

**Code Map.** Build-spec section where investigation findings are written (paths, symbols, what to reuse, what not to change) so implementation needn't re-investigate. See `build-step-by-step.md`.

**Companion.** A file listed in `SPEC.md` frontmatter that downstream skills must read with it. Spec-authored or adopted. Diagrams always go in one. See `spec-skill.md`.

**Coaching path / Fast path.** Two working modes on the PRD and architecture skills. Coaching draws decisions out of you, Fast drafts everything with `[ASSUMPTION]` tags. Architecture defaults to Coaching. See `prd-skill.md`, `architecture-skill.md`.

**Correct course (`bmad-correct-course`).** Handles a change too big for one story and produces a sprint change proposal. See `flow.md`.

**Deferred.** An architecture spine section for decisions deliberately not made; also `deferred-work.md` in build, where out-of-scope findings and split goals go. See `architecture-skill.md`, `build-step-by-step.md`.

**Deep recon (`bmad-deep-recon`).** Research skill producing a cited `research.md`, in Draft, Process, or Run mode. See `agents.md`.

**Delivery loop.** Clarify, Plan, Build and verify, Learn and adjust. See `flow.md`.

**Epic.** One outcome spanning several sessions of work; gets a spec, stories, and a retrospective. See `flow.md`.

**Forge exits (Hardened / Killed / Clearer).** The three valid endings of a `bmad-forge-idea` session. Hardened writes a very short `forged-idea.md`; Killed records the cause of death; Clearer writes no handoff file. All three are successes. See `ideation-skills.md`.

**FR / UJ / SM.** Numbered PRD items: functional requirement, user journey, success metric (plus `SM-C` counter-metrics). See `prd-skill.md`.

**Frozen block (`<frozen-after-approval>`).** Part of a build spec (intent, boundaries, I/O matrix) locked once the human approves it; only the human may change it. See `build-step-by-step.md`.

**Headless.** Running a skill with no interactive user (no TTY or a programmatic caller). Some skills change behavior; Story Breakdown is skipped. Each skill decides for itself: in the lab, `claude -p` did **not** count as headless for `bmad-brainstorming`, even with a `headless: true` flag, because a present user message means interactive under that skill's rule. See `spec-skill.md`, `ideation-skills.md`.

**Intent.** A statement of what should be true when the work is done, what must not change, and what is out of scope, complete enough for someone else to build without guessing. See `flow.md`.

**Kernel.** The five fields of a spec: Why, Capabilities, Constraints, Non-goals, Success signal. See `spec-skill.md`.

**Load-bearing.** A claim that a downstream consumer would change a decision without. The spec must preserve every one. See `spec-skill.md`.

**Memlog (`.memlog.md`).** Append-only log of decisions, constraints, assumptions, and questions; the canonical source that specs, PRDs, and spines are derived from. Written through `memlog.py`. See `spec-skill.md`, `prd-skill.md`, `architecture-skill.md`.

**Oneshot / dispatch.** The two `bmad-build` routes at the release. Oneshot implements in the same session with a thin spec; dispatch writes a full spec and hands implementation to a subagent. Chosen in step 2 on three facts: intent gaps, irreversibles, footprint. (The unreleased clone renamed dispatch to `full` and routes by line count.) See `build-step-by-step.md`.

**Open Questions.** Gaps the input didn't settle. Skills record them instead of inventing answers; build halts for the human. See `spec-skill.md`, `build-step-by-step.md`.

**PRD.** Requirements document owned by the organization; everything downstream derives from it. See `prd-skill.md`.

**Readiness gate.** The check in `bmad-sprint-planning` asking whether a developer could implement the epics without inventing unrecorded decisions. Verdict PASS, CONCERNS, or FAIL. See `flow.md`.

**Retrospective.** End-of-epic judgment against evidence; verdict accepted, accepted-with-open-items, or rejected. See `flow.md`.

**Review layer (lens).** One reviewer's angle in code review, run as a parallel subagent. Release 6.12.0: Blind Hunter, Edge Case Hunter, Verification Gap Reviewer in `bmad-build`'s dispatch route (Blind Hunter alone in oneshot); `bmad-code-review` adds an Acceptance Auditor only when a spec exists. See `build-step-by-step.md`.

**Review triage.** Main-session step that verifies each reviewer finding and routes it: intent_gap, bad_spec, patch, or defer. See `build-step-by-step.md`.

**Skill.** A named command installed into the AI coding tool; loads an agent, runs a workflow, or runs a single task. See `agents.md`.

**Spec Law.** The eight rules `bmad-spec` validates a spec against: every capability has intent and success; intents say what, not how; constraints must bend design; at least one non-goal; a testable success signal; stable capability IDs; every load-bearing source claim preserved; lean prose. See `spec-skill.md`.

**Spec (`SPEC.md`).** The short contract downstream skills build from, written only by `bmad-spec`, in `specs/spec-<slug>/`. Not the same as the build spec (below). See `spec-skill.md`.

**Build spec.** The per-change file `bmad-build` writes and updates, with status `draft`, `ready-for-dev`, `in-progress`, `in-review`, or `done`. Distinct from `SPEC.md`. See `build-step-by-step.md`.

**Spine (`ARCHITECTURE-SPINE.md`).** Short consistency contract recording only the invariants that keep independently built units compatible. See `architecture-skill.md`.

**Sprint change proposal.** The output of `bmad-correct-course`: what changes, what stays, in what order. Approved item by item, then as a whole, then classed **Minor** (Developer implements directly), **Moderate** (backlog reorganization), or **Major** (escalation to product and architecture roles). See `flow.md`.

**Sprint status (`sprint-status.yaml`).** The engineering-side story tracking file. BMAD does not sync it with Jira or Linear. See `flow.md`.

**Stance.** The role `bmad-brainstorming` plays, chosen once and held for the run: Facilitator (never supplies ideas), Creative Partner (trades ideas, each tagged by author), or Ideate for me (runs the session itself). See `ideation-skills.md`.

**Stories (`stories.yaml`).** Optional list, in execution order, produced by Story Breakdown. Has no status field. See `spec-skill.md`.

**Story Breakdown.** Interactive step of `bmad-spec` that turns capabilities into stories, asking you about checkpoints. See `spec-skill.md`.

**Subagent.** A child session the main workflow dispatches (implementation, review lenses, research). Several skills need or prefer them; the fallback is inline work or a halt. Observed in the lab: headless `bmad-build` spawned implementation and review subagents once given permission. See `build-step-by-step.md`.

**Triage verdict.** The one verdict the main session gives each review finding after checking it at the cited location: `high`, `medium`, `low`, `false`, or `maybe-false`. Reviewers' own severities are discarded. A `false` verdict is judged against the code as it is now and is never revisited when later stories change the premise. See `build-step-by-step.md`, `systemic-findings.md`.

**`uv`.** Python tool the installer requires; `bmad-build` halts without it. See `lab-log.md`.
