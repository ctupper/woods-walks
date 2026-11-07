# `bmad-ux`: DESIGN.md and EXPERIENCE.md

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-ux/SKILL.md` (P23, see `../sources.md`); directory listing only for `assets/` and `references/`. Tags: [V, P23] traced to that file, [I] inferred, [?] unclear. Not run in a lab. Written unattended 2026-09-19; reviewed by Carl 2026-09-24. Section on references and assets (P41, read at 6.12.1) added unattended 2026-10-18, not yet reviewed.*

*Release check: read from the clone's `skills/` path. The installed-vs-clone diff (2026-09-19) found this skill differs from the `v6.12.0` release only in `SKILL.md` activation lines (the release loads `user_name`/language and greets by name); substantive claims stand at the release. See [build-step-by-step.md](build-step-by-step.md), last section.*

!!! tip "TL;DR"
    `bmad-ux` produces two peer contracts — `DESIGN.md` (how it looks) and `EXPERIENCE.md` (how it behaves) — both of which win over any mock, wireframe, or import on conflict. Same elicit-don't-author stance and memlog-then-derive pattern as the PRD and architecture skills, plus a third mode unique to UX: handing Discovery's output off to an external design tool and folding the result back in later.

## What it produces

Two peer contracts: **`DESIGN.md`** (how the product looks) and **`EXPERIENCE.md`** (how it behaves). [V, P23] Both win over any mock, wireframe, or import on conflict. EXPERIENCE.md references DESIGN.md tokens by name with `{path.to.token}` syntax. [V, P23]

- **DESIGN.md** follows the Google Labs `design.md` spec: YAML tokens (colors, typography, rounded, spacing, components) plus a body in a locked order: Brand and Style, Colors, Typography, Layout and Spacing, Elevation and Depth, Shapes, Components, Do's and Don'ts. Sections may be omitted; the order is fixed. [V, P23]
- **EXPERIENCE.md** always has: Foundation (form factor, UI system), Information Architecture, Voice and Tone (microcopy), Component Patterns (behavioral), State Patterns, Interaction Primitives, Accessibility Floor (behavioral), Key Flows (named-protagonist journeys with a climax beat). Inspiration and Anti-patterns and Responsive and Platform are added when triggered; product-specific sections may be invented. [V, P23]
- When Foundation names a UI system (shadcn, MUI, UIKit, Compose, an internal design system), both files inherit from it and EXPERIENCE.md specifies only the behavioral delta. [V, P23]

## Stance

"Elicit and capture the user's vision, never impose yours." The skill must never volunteer colors, patterns, or directions; creative tools render options when seeing helps, and the picks are the user's. [V, P23] Same elicitation-not-authoring stance as [prd-skill.md](prd-skill.md). [V, P20, P23]

## How a run goes

- Same skeleton as the PRD and architecture skills: intent detection (Create, Update, Validate), a bound run folder with `.memlog.md` as canonical memory, brain dump first, stakes calibration (hobby, internal, consumer, regulated), Fast or Coaching path, subagent extraction of big inputs, a reviewer gate, and a Finalize sequence ending with `status: final`. [V, P23]
- **Third working mode, unique to this skill: Design handoff.** The skill assembles what Discovery captured into a prompt for an external tool (default registry entry: Google Stitch); the user runs it and saves the output back. EXPERIENCE.md can follow later through Update. [V, P23]
- **Creative tools** (defaults: HTML color themes, design directions, Excalidraw wireframes, key-screen HTML mocks at Finalize). Their artifacts go to `.working/`; user-supplied visuals (Figma, sketches, brand decks) go to `imports/`, each logged in the memlog. [V, P23; asset files listed in the directory, contents not read]
- **Surface closure rule:** the information architecture is done when every stated need has a surface that delivers it and every surface has a journey that lands there. When closure fails, "probe, never invent the missing piece." [V, P23]
- Form factor (mobile, web, desktop, multi-surface) must be resolved before IA closes; named-protagonist journeys often imply it. [V, P23]
- At Finalize, each IA surface is classed as mocked or spine-only, and the user is asked whether any spine-only surface needs a visual reference. Mocks and wireframes that survive are promoted to `mockups/` or `wireframes/`. [V, P23]
- **The reviewer gate is opt-in and lens-selectable** because reviewers cost parallel subagent tokens. This differs from `bmad-architecture`, where the configured reviewers always run once the gate runs. [V, P23; V, P21 for the contrast]

## Where it sits in the flow

Documented next steps: `bmad-architecture`, `bmad-create-epics-and-stories`, `bmad-build`. UX "may lead, follow, or stand alone" relative to the product documents. Misroutes are redirected: PRD to `bmad-prd`, architecture to `bmad-architecture`, game UX to a separate BMad module (GDS), briefs to `bmad-product-brief`. [V, P23]

## Inference

- All four planning skills read so far (`spec`, `prd`, `architecture`, `ux`) share one pattern: an append-only memlog as canonical memory, a distilled artifact derived from it at Finalize, subagent extraction, and a reviewer gate. That looks like a common template of the v6.12 planning skills. [I]

## Inside the skill's references and assets (P41, added unattended 2026-10-18)

*Read at tag `v6.12.1`; nothing under `assets/` or `references/` changed from 6.12.0 (only one `SKILL.md` config line did). The three DESIGN.md and two EXPERIENCE.md worked examples were listed, not read.*

**Validate and the reviewer gate** (`references/validate.md`). Validate critiques the spine pair "without changing it", and the same pipeline is the Finalize gate. [V, P41] At Finalize it first asks whether to validate at all (offered by default, easy to skip); then, unless headless, it shows a lens menu (rubric walker + configured `finalize_reviewers` + ad-hoc lenses it judges relevant, such as accessibility) and dispatches only the picked lenses, in parallel. [V, P41] The rubric walker checks eight categories in two passes:

| Pass | Category | What it checks |
|---|---|---|
| Mechanical | Flow coverage | every source journey/requirement has a Key Flow with protagonist, steps, climax, failure path |
| | Token completeness | every token defined; **color tokens without hex are critical** |
| | Component coverage | every component has a visual row in DESIGN.md *and* a behavior row in EXPERIENCE.md |
| | State coverage | empty, cold-load, focus, error, offline, permission-denied, as they apply |
| | Visual reference coverage | every mockup/wireframe linked inline; orphans listed |
| Judgment | Bloat | pixel specs where tokens would do, restated sources, unused sections |
| | Inheritance | names verbatim from sources; glossary and component names identical across files |
| | Shape fit | DESIGN.md sections in canonical order; EXPERIENCE.md's eight required defaults present |

[V, P41] Verdicts are *strong / adequate / thin / broken* per category, severity is "downstream impact, not fix difficulty", and the consolidated report (HTML plus a Markdown twin) has **"No overall grade."** [V, P41] That differs from `bmad-prd` Validate, which grades the whole document (Experiment 15 graded a PRD Poor; [prd-skill.md](prd-skill.md)). [V-lab] The difference is deliberate: the 6.8.0 changelog describes `bmad-ux` as "Per-category verdicts, no misleading headline grade." [V, P42 CHANGELOG v6.8.0]

**Headless** (`references/headless.md`, `assets/headless-schemas.md`). Triggered by `headless: true`, a skill or non-interactive caller, a prepend step, or an automation-style first message; "Ambiguous → default interactive." Headless never asks or greets, keeps creative tools off, and ends with JSON per intent (paths to DESIGN.md, EXPERIENCE.md and memlog; a `changes_summary` and `conflicts_with_prior_decisions[]` on Update; `findings_summary` counts and `offer_to_update: true` on Validate). [V, P41] **It has a third status that `bmad-spec` lacks: `partial`, meaning an artifact was produced but `open_questions[]` is non-empty or critical inputs were inferred.** A caller can tell an unfinished UX spine from a finished one by status alone; with `bmad-spec` it has to open `SPEC.md` ([spec-skill.md](spec-skill.md), "The headless contract"). [V, P40, P41] What a headless Validate dispatches when the lens menu is skipped is not stated (all configured lenses? the rubric walker only?). [?]

**DESIGN.md follows an outside spec.** The format is Google Labs' `design.md` (Apache 2.0, April 2026), summarized in `references/design-md-spec.md`, which says "the URL wins on conflict": YAML front-matter tokens (`colors` as hex, `typography`, `rounded`, `spacing`, `components` with `{path.to.token}` references) and eight optional but order-locked body sections. Inherited systems (shadcn, MUI, Tailwind, native platforms) are referenced by name, and only the deltas are written. [V, P41] So the DESIGN.md format can change upstream without a BMAD release. [I]

**Creative tools** are subagent renderers that write to `.working/` and return only a short summary: 4 to 6 HTML color themes, 3 to 6 full "visual personality" directions on the hero screen, Excalidraw IA/flow wireframes, and 2 to 4 1:1 key-screen mocks at Finalize. All are inline CSS with no JS and no network, and use real content from the conversation ("no lorem"). [V, P41 `assets/`] Teams can add renderers such as a Figma MCP by override. [V, P41 `references/creative-tools.md`] Only artifacts that pass "would a future reader of `DESIGN.md` or `EXPERIENCE.md` open this?" get promoted to `mockups/` or `wireframes/`; the rest stay in `.working/`. Key-screen mocks may not invent layout: every composition choice must trace to a `.working/` artifact or a memlog confirmation. [V, P41] The Excalidraw renderer carries a hard-won warning: three-character element `index` values make the file fail as "invalid file" with no diagnostic. [V, P41]

## Not yet checked

- ~~The contents of `assets/` ..., `references/design-md-spec.md`, `creative-tools.md`, `validate.md`, `headless.md`.~~ Read 2026-10-18 (section above), except the five worked examples and `validation-report-template.html`. [?]
- The skill has never been run in a lab: no DESIGN.md/EXPERIENCE.md, no creative-tool output, no Validate. [?]
