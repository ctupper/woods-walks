# `bmad-ux`: DESIGN.md and EXPERIENCE.md

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-ux/SKILL.md` (P23, see `../sources.md`); directory listing only for `assets/` and `references/`. Tags: [V, P23] traced to that file, [I] inferred, [?] unclear. Not run in a lab. Written unattended 2026-09-19; reviewed by Carl 2026-09-24.*

*Release check: read from the clone's `skills/` path. The installed-vs-clone diff (2026-09-19) found this skill differs from the `v6.12.0` release only in `SKILL.md` activation lines (the release loads `user_name`/language and greets by name); substantive claims stand at the release. See [build-step-by-step.md](build-step-by-step.md), last section.*

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

## Not yet checked

- The contents of `assets/` (color themes, design directions, three worked DESIGN.md examples, EXPERIENCE.md examples), `references/design-md-spec.md`, `creative-tools.md`, `validate.md`, `headless.md`. [?]
