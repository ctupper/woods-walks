# `bmad-prd`: How the PRD Skill Works

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-prd/` (P20, see `../sources.md`): `SKILL.md`, `assets/prd-template.md`, first ~30 lines of `references/validate.md` and `references/headless.md`. Tags: [V, P20] traced to those files, [I] inferred, [?] unclear, [V-lab] observed in a lab run. Run in the lab twice (Experiment 12, Update mode; Experiment 15, Create → finalize → Validate; see [lab-log.md](lab-log.md)). `references/validate.md` and `assets/prd-validation-checklist.md` read in full 2026-10-07. Written unattended 2026-09-19; reviewed by Carl 2026-09-24; lab sections added 2026-10-02 and 2026-10-08 (the latter not yet reviewed).*

*Release check: read from the clone's `skills/` path. The installed-vs-clone diff (2026-09-19) found this skill differs from the `v6.12.0` release only in `SKILL.md` activation lines (the release loads `user_name`/language and greets by name) and `lint_spine.py` formatting; substantive claims stand at the release. See [build-step-by-step.md](build-step-by-step.md), last section.*

!!! tip "TL;DR"
    `bmad-prd` is the tool for "agreement and sign-off among people" — one skill with three intents: **Create** a PRD from scratch, **Update** an existing one against a change, or **Validate** one without changing anything. It elicits rather than authors (it hands the pen back rather than proposing MVP cuts itself), keeps an append-only memlog like `bmad-spec`, and gates finalizing behind a parallel-subagent reviewer pass, except at hobby stakes, where the pass may be skipped (Experiment 15: it was).

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

- **Stakes-calibrated:** "hobby/solo may run quietly or skip; higher stakes get the explicit all/subset/skip menu." [V, SKILL.md:75]
- The gate assembles a rubric walker (against `assets/prd-validation-checklist.md`), any configured extra reviewers, and ad-hoc reviewers, run as parallel subagents. `validate.md` says the extra list is adversarial-general "by default", but the shipped 6.12.0 `customize.toml` has `finalize_reviewers = []`. [V, validate.md; V-lab, installed `customize.toml`] Each writes a full review file and returns only a compact summary. Findings are surfaced tiered: verdict, then critical and high, then a tail count. [V, P20]
- The rubric walker rates each of seven dimensions strong / adequate / thin / broken: decision-readiness, substance over theater, strategic coherence, done-ness clarity ("be unforgiving here"), scope honesty, downstream usability, shape fit; plus a mechanical-notes tail (glossary drift, ID continuity, Assumptions Index roundtrip). Severity ranks impact, not ease of fix. [V, `prd-validation-checklist.md`]
- Grade rules: *Excellent* (all strong/adequate, no high/critical), *Good* (≤1 thin, no critical), *Fair* (several thin or any high), *Poor* (any broken or any critical). So one critical finding makes a PRD Poor regardless of the rest. [V, validate.md]
- Under Validate the skill also synthesizes one HTML plus markdown report and opens it; it does not run Finalize. [V, P20]
- Headless mode exists (caller supplies intent, inputs; gaps are recorded as `assumptions[]` and `open_questions[]`, never invented). [V, P20]

## Update mode

Source-extract against PRD, addendum, memlog, and original inputs. If the memlog is missing, a bootstrap subagent reverse-engineers a thin one from the PRD. Conflicts with prior decisions are surfaced before applying. [V, P20]

### Observed in the lab: Update on a hand-written PRD (Experiment 12)

Run on a one-page PRD written by hand for a community library's room-booking system (no memlog, never touched by BMAD), with a change that conflicts with it: weekly recurring 4-hour bookings for a season, against a board-decided 2-hour maximum, a "no recurring bookings" non-goal, a 2-booking limit and a 14-day window. [V-lab, [lab-log.md](lab-log.md) Experiment 12]

- **Conflicts were surfaced before anything was written,** as documented. The first round changed no file and named every planted conflict, including the two implicit ones (the booking limit and the 14-day window), quoting the board's reason for the 2-hour rule and flagging the PRD's "approved by the board" status. [V-lab; V, P20]
- **The bootstrap memlog was thin and sensible, but written with the first edit, not before the conflict check.** It opened with two "Recovered (Mar 2026)" decision entries reconstructed from the PRD, then the change and the answers. It credited every answer to the configured user, though they were relayed (same attribution gap as in [systemic-findings.md](systemic-findings.md)). [V-lab]
- **An approved baseline was annotated, not overwritten.** The change went into a separate "Proposed change" section marked pending board approval, with "until the board approves it, the March 2026 rules and non-goals above stand", and the old rule and non-goal point to it. [V-lab]
- **The reviewer gate caught a flaw in an answer the human had approved:** defining "evening" by start time let a session starting just before the cutoff take a whole evening uncounted, defeating the cap meant to protect the board's intent. It also found a counter-measure that could never fail. [V-lab]
- **A pre-existing contradiction unrelated to the change was not caught.** The PRD lets walk-ins without a card book, while its user list says only cardholders book; both reviewers looked at the walk-in rule only in relation to the new feature. Update and its reviewers check the change against the PRD, not the PRD against itself. [V-lab; I on the generalization]
- Not tested: finalize to `status: final`, input reconciliation, Validate mode on its own. [?] → Later: finalize and Validate tested in Experiment 15 (below); input reconciliation still not (no source inputs given).

### Observed in the lab: Create, finalize, then Validate (Experiment 15)

A hobby-stakes PRD for a neighborhood tool-lending shelf, fast path, every answer Carl's (relayed). After finalize, one contradiction was planted by hand (a Non-Goal ruling out email, against an FR and the MVP scope that require it), then Validate ran in a fresh session. [V-lab, [lab-log.md](lab-log.md) Experiment 15]

- **It elicited even on the fast path.** Told "you decide" on deposit rules, it declined and offered options instead. The cost was turns: six rounds for a two-page PRD, against the docs' "two or three". Each answer opened new questions (choosing in-app deposits added four). [V-lab]
- **It proposed one thing itself and flagged it:** a counter-metric (loans per month), marked for confirmation, as the template asks. [V-lab; V, P20]
- **`status: final` with no review.** At hobby stakes, finalize skipped the reviewer gate (allowed), ran the memlog audit and a wording pass, and surfaced two blockers at the top of the PRD as open items owned by Carl. "Final" here meant the human chose to stop, not that a review passed. [V-lab; V, SKILL.md:75; I on the reading]
- **Validate caught the planted contradiction, with all four reviewers** (rubric walker, adversarial, edge-case, verification gap), checked it against the memlog, and noted the PRD file was edited after the finalize entry without a log record. That is the gap Experiment 12's Update missed: Validate reads the PRD against itself, Update reads a change against the PRD. [V-lab; I on the generalization]
- **It also found real gaps the skipped gate would have caught:** an undefined Request/Loan lifecycle, a success metric that lost tools would inflate, `status: final` beside two blockers, and the finalize audit's own miscount (claimed 30 memlog entries, there were 26). Grade **Poor** (one critical); without the plant, 8 high findings would still grade *Fair*. [V-lab]
- Read-only as documented: PRD and memlog untouched, report in `.html` + `.md`, no browser in headless mode, ends by offering an Update. [V-lab; V, validate.md]
- Harness caveat: the fast path's `[ASSUMPTION]` tags became `[CONFIRM]` + Open Questions because the relay prompt said every decision must come from the human; the memlog records that as the reason. [V-lab]

## Inference

- The same append-only-log-then-derive pattern appears in both `bmad-spec` and `bmad-prd`; it looks like a house pattern of the v6.12 planning skills, not a one-off. [I]
- The PRD's globally numbered FR, UJ, and SM IDs are the stable handles `bmad-spec` and later skills can cite; how `bmad-spec` maps them to `CAP-N` is not stated in the files read. [?]

## Not yet checked

- ~~`assets/prd-validation-checklist.md`, the rest of `references/validate.md`~~ (read 2026-10-07). Still unread: the Adapt-In Menu section of the template, `assets/headless-schemas.md`. [?]
- Input reconciliation at finalize (needs source documents). A finalize at internal or launch stakes, where the gate should offer the all/subset/skip menu. [?]
