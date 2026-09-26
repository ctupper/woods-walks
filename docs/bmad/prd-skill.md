# `bmad-prd`: How the PRD Skill Works

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-prd/` (P20, see `../sources.md`): `SKILL.md`, `assets/prd-template.md`, first ~30 lines of `references/validate.md` and `references/headless.md`. Tags: [V, P20] traced to those files, [I] inferred, [?] unclear. Not run in a lab. Written unattended 2026-09-19; reviewed by Carl 2026-09-24.*

*Release check: read from the clone's `skills/` path. The installed-vs-clone diff (2026-09-19) found this skill differs from the `v6.12.0` release only in `SKILL.md` activation lines (the release loads `user_name`/language and greets by name) and `lint_spine.py` formatting; substantive claims stand at the release. See [build-step-by-step.md](build-step-by-step.md), last section.*

## What it is

One skill with three intents: **Create** (no PRD yet), **Update** (reconcile an existing PRD with a change), **Validate** (critique only, change nothing). [V, P20] In [flow.md](flow.md) terms it is the Clarify-stage tool for "agreement and sign-off among people". [V, P3]

## Stance

The skill's opening line: "master facilitator and coach ... Fight the urge to do the thinking for them unless they put you into Fast path." [V, P20]
- **Elicitation, not direction.** Open-ended "tell me about X" beats multiple choice. Naming wedges, picking MVP cuts, or proposing phases means the skill has "crossed from elicitation into authoring": hand the pen back. Infer-and-confirm is fine. [V, P20]
- Misroute check on the first message: a game, express build, one-pager, product-idea vetting, or agent-building request gets pointed to another skill (`bmad-build`, `bmad-product-brief`, `bmad-prfaq`, ...). [V, P20]

## Discovery order

Brain dump, then stakes calibration (hobby / internal / launch), then working mode, then mode-scoped work. "Two or three turns, not ten." [V, P20]

- **Fast path:** batch the remaining gaps into one or two questions, draft the full PRD with `[ASSUMPTION]` tags, user reviews. **Coaching path:** walk the sections together, entering via **Vision + Features** or **Journey-led**. [V, P20]
- Web-research subagents run by default during Discovery; the parent receives a digest. Source documents go to subagents for extraction ("extract, don't ingest"). [V, P20]
- A **concern scan** names what this product actually carries (compliance, integrations, SLAs, hardware, data governance) and that decides which optional sections to pull in. The list is open. [V, P20]
- **User journeys are captured, not authored:** the user narrates a real session with a named protagonist ("Mary, mom of three, not 'the user'"), and the skill structures it as UJ-N. Dropped or downscaled for single-operator internal tools. [V, P20]

## Files

- `prd.md` (frontmatter: title, status, created, updated; `status: final` only at finalize). [V, P20]
- `.memlog.md`: canonical, append-only record of every decision, change, override, and assumption, written only through `memlog.py`. Same mechanism as `bmad-spec` ([spec-skill.md](spec-skill.md)). "Whatever isn't logged is lost on resume." [V, P20]
- `addendum.md`: depth that belongs downstream or doesn't fit the PRD (rejected alternatives, technical-how, sizing data). Audit and override information never goes here. [V, P20]
- Review and reconcile outputs: `review-{slug}.md`, `reconcile-{slug}.md`. [V, P20]
- Run folders are found under a configurable output path; unfinished runs (`status` not `final`) are offered for resume. [V, P20]

## Template (Essential Spine)

Sections 0 to 9: Document Purpose, Vision, Target User (JTBD, non-users, journeys), **Glossary**, Features with nested FRs, Non-Goals, MVP Scope, Success Metrics, Open Questions, Assumptions Index. [V, P20]
- FRs have globally numbered stable IDs (FR-1...FR-N) with "Consequences (testable)" lines and optional Out of Scope; features carry their own optional NFRs. Cross-cutting NFRs get their own section; traceability matrices are skipped. [V, P20]
- The Glossary is enforced: introducing a synonym for a defined term anywhere in the PRD "is a discipline violation". [V, P20]
- Success Metrics must name **counter-metrics** ("do not optimize") alongside primary ones. [V, P20]
- The spine is the expected default; an **Adapt-In Menu** of conditional sections is pulled in per concern, and the skill may invent a section when no menu item fits. [V, P20]
- Capabilities, not implementation: tech choices go in `addendum.md`. Length scales with stakes: hobby about 2 pages, internal 5 to 8, launch as long as needed. [V, P20]

## Finalize sequence

1. Memlog audit. 2. Input reconciliation (subagent per source input; surfaces qualitative ideas the FR structure drops). 3. Reviewer pass. 4. Triage open items (phase-blockers resolved one at a time; others deferred with owner and revisit condition). 5. Polish (last, so it doesn't redo work after reviewer fixes). 6. External handoffs. 7. Close: set `status: final`. Common next skills: `bmad-ux`, `bmad-architecture`, `bmad-create-epics-and-stories`. [V, P20]

## Reviewer gate and Validate

- The gate assembles a rubric walker (against `assets/prd-validation-checklist.md`), any configured extra reviewers (default: adversarial-general), and ad-hoc reviewers, run as parallel subagents. Each writes a full review file and returns only a compact summary. Findings are surfaced tiered: verdict, then critical and high, then a tail count. [V, P20]
- The rubric walker rates each of seven dimensions strong / adequate / thin / broken. [V, P20]
- Under Validate the skill also synthesizes one HTML plus markdown report and opens it; it does not run Finalize. [V, P20]
- Headless mode exists (caller supplies intent, inputs; gaps are recorded as `assumptions[]` and `open_questions[]`, never invented). [V, P20]

## Update mode

Source-extract against PRD, addendum, memlog, and original inputs. If the memlog is missing, a bootstrap subagent reverse-engineers a thin one from the PRD. Conflicts with prior decisions are surfaced before applying. [V, P20]

## Inference

- The same append-only-log-then-derive pattern appears in both `bmad-spec` and `bmad-prd`; it looks like a house pattern of the v6.12 planning skills, not a one-off. [I]
- The PRD's globally numbered FR, UJ, and SM IDs are the stable handles `bmad-spec` and later skills can cite; how `bmad-spec` maps them to `CAP-N` is not stated in the files read. [?]

## Not yet checked

- `assets/prd-validation-checklist.md` (the seven dimensions in full), the Adapt-In Menu section of the template, `assets/headless-schemas.md`, and the rest of `references/validate.md`. [?]
