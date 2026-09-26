# BMAD — Agents and Skills

*Describes BMAD-METHOD v6.12.0 (see `../sources.md`). Tags: [V] traced to a primary doc, [I] inferred, [?] unclear. Source IDs (P2 etc.) refer to the ledger. Reviewed by Carl 2026-09-24.*

## The core idea

BMAD adds named commands called **skills** to AI coding tools such as Claude Code and Cursor. [V, P1] Some skills help you *think* (explore, research, argue against an idea, write down what you settled on). Others help you *build*. [V, P1] Either group works alone; a small fix can go straight to building with no planning. [V, P1]

A skill does one of three things: loads an **agent persona**, runs a **multi-step workflow**, or runs a **single task**. [V, P2] On Claude Code, skills are installed into `.claude/skills/`, one directory per skill holding a `SKILL.md`. [V, P2]

## Two ways to start work

| Mechanism | How | Effect |
|---|---|---|
| Skill | Type the skill name (e.g. `bmad-help`) | Loads an agent, runs a workflow, or runs a task directly [V, P2] |
| Agent menu trigger | Load an agent, then type a short code (e.g. `BD`) | The agent starts the matching workflow and stays in character [V, P2] |

Codes are scoped to the agent that shows them: `CR` is competitive teardown for the Analyst and code review for the Developer. [V, P2]

## The five agents

The BMad Method module installs five named agents. [V, P2]

| Agent | Skill ID | Codes | What its menu offers |
|---|---|---|---|
| **Analyst (Mary)** | `bmad-agent-analyst` | `BP` `MR` `DR` `TR` `TS` `CR` `UV` `CB` `WB` `PC` | Brainstorm; market, domain, technical research; technology selection; competitive teardown; user-voice research; product brief; PRFAQ challenge; project context |
| **Product Manager (John)** | `bmad-agent-pm` | `PRD` `CE` `IR` `CC` | Create/update/validate a PRD; epics and stories; implementation readiness; correct course |
| **Architect (Winston)** | `bmad-agent-architect` | `CA` `IR` | Architecture spine; implementation readiness |
| **Developer (Amelia)** | `bmad-agent-dev` | `BD` `QA` `CR` `SP` `ER` | Build; QA test generation; code review; sprint plan; epic retrospective |
| **UX Designer (Sally)** | `bmad-agent-ux-designer` | `CU` | UX design |

- The Technical Writer (Paige) is **on hiatus**; project context lives on via the Analyst's `PC` code or `bmad-project-context`. [V, P2]
- The Developer's `QA` runs `bmad-qa-generate-e2e-tests`; the full Test Architect is a **separate module**. [V, P2]
- Each agent is "an identity plus a customizable layer." [V, P2]
- All five agent skill directories exist in the clone's `skills/` folder [V, P11], and at the `v6.12.0` tag under `src/bmm-skills/`, identical to the lab install [V-lab, re-pin 2026-09-19].

**Not in the current roster:** there is no Scrum Master or QA agent in the v6.12.0 docs. [V, P2 — absence in the roster] Descriptions of BMAD from earlier versions may list different agents. [?, not checked against older versions] `bmad-correct-course` still hands Moderate and Major changes to "Product Owner" and "Solution Architect", neither of which is one of the five agents (see `flow.md`). [V, skill files at v6.12.0; I on the mismatch]

### Agent inputs and outputs (spec criterion 1)

What each agent reads and produces, through the skills its menu dispatches. The agents themselves hold no workflow logic; inputs and outputs are those of the skills. [V, P22; V, P19 to P25 for the skills]

| Agent | Typical inputs | Outputs |
|---|---|---|
| **Mary** (Analyst) | A topic, idea, or decision to research; existing product notes; the repo (for `PC`) | `brainstorm.html` and optional `brainstorm-intent.md`; cited `research.md`; `brief.md` + `addendum.md`; `prfaq-<project>.md`; the `AGENTS.md` context block |
| **John** (Product Manager) | A brain dump plus existing inputs (brief, research, transcripts, competitive analysis, prior PRD); the PRD and planning documents for epics; the change trigger for course correction | `prd.md`, `addendum.md`, `.memlog.md` (or a validation report); epic files with stories; a readiness verdict and `sprint-status.yaml`; a sprint change proposal |
| **Winston** (Architect) | A spec package (`SPEC.md` plus its memlog), a raw idea, an existing codebase, or an existing spine; the PRD and UX in the agent's own description | `ARCHITECTURE-SPINE.md` (numbered `AD` decisions with Binds, Prevents, Rule); a readiness verdict |
| **Sally** (UX Designer) | User needs, the PRD, product sources, user-supplied visuals (Figma, sketches, brand decks) | `DESIGN.md` (visual identity tokens and rules) and `EXPERIENCE.md` (behavior, states, flows); optional mockups and wireframes |
| **Amelia** (Developer) | An approved story, spec, or plain intent (a sentence or issue is enough); the repo | Code and tests; the per-change build spec with review triage log; `deferred-work.md`; test suites (`QA`); a code review with patches; a sprint plan; an epic retrospective |

**Caveats:** these are the artifacts each skill documents; the agent adds only a persona and a menu. The lab exercised the skills without loading an agent persona, so no agent session was run. [V, P22; V-lab for the absence]

## Core skills (any project, any phase, no agent session needed)

Eight skills ship in the core module. [V, P2]

| Skill | What it does | Output |
|---|---|---|
| `bmad-help` | Inspects the project for existing artifacts and installed modules, recommends the next skill | Prioritized next steps [V, P2] |
| `bmad-advanced-elicitation` | Second pass over recent output through a named reasoning method (pre-mortem, first principles, red team, etc.) | Proposed improvements to accept or discard [V, P2] |
| `bmad-review` | Reviews a diff or document through lenses: adversarial, edge case, verification gap, structure, prose. Zero findings is valid | Findings grouped by lens [V, P2] |
| `bmad-customize` | Writes and verifies customization overrides under `_bmad/custom/` | Override files [V, P2] |
| `bmad-brainstorming` | Facilitated session aiming for 100+ ideas | `brainstorm.html` + optional `brainstorm-intent.md` [V, P2] |
| `bmad-deep-recon` | Researches a topic to support a decision | Cited `research.md` + optional HTML briefing [V, P2] |
| `bmad-forge-idea` | Pressure-tests a half-formed idea, one question at a time, with personas | `forge-report.html` always; `forged-idea.md` if it hardens [V, P2, P4] |
| `bmad-party-mode` | Puts installed agents or custom personas in one conversation | A discussion [V, P2] |

## Method skills (BMad Method module)

| Skill | Purpose | Produces |
|---|---|---|
| `bmad-product-brief` | Write down a clear product concept | `brief.md` + `addendum.md` [V, P3, P5] |
| `bmad-prfaq` | Working Backwards stress test of a concept | `prfaq-<project>.md` [V, P3, P5] |
| `bmad-prd` | Create, update, or validate a PRD | `prd.md`, `addendum.md`, `.memlog.md` (create/update); HTML + `.md` report (validate) [V, P3] |
| `bmad-ux` | Capture UX vision | `DESIGN.md`, `EXPERIENCE.md`, `.memlog.md` [V, P3, P6] |
| `bmad-spec` | Condense any intent into a short contract; optionally break into stories | `SPEC.md` + companions under `specs/spec-<slug>/`; optional `stories.yaml` [V, P3, P5] |
| `bmad-architecture` | Record decisions that would conflict if made independently | `ARCHITECTURE-SPINE.md` [V, P3, P6] |
| `bmad-create-epics-and-stories` | Break requirements into epics and stories | Epic files with stories [V, P3, P7] |
| `bmad-sprint-planning` | Readiness gate, then sprint tracking | PASS/CONCERNS/FAIL + `sprint-status.yaml` [V, P3, P7] |
| `bmad-correct-course` | Assess a significant mid-sprint change | Change proposal [V, P2, P7] |
| `bmad-project-context` | Set up/refresh/audit the repo's agent instructions | Project context [V, P2] |
| `bmad-build` | Turn a work item into reviewed, verified code | Code + implementation record [V, P2, P8] |
| `bmad-build-auto` | One unattended build iteration for an orchestrator | Code + record + terminal status [V, P2, P8] |
| `bmad-code-review` | Review code with several independent reviewers, then triage | Findings + applied patches [V, P2, P8] |
| `bmad-walkthrough` | Guided human review of a commit/PR/file | Walkthrough [V, P2] |
| `bmad-qa-generate-e2e-tests` | Generate API and e2e tests | Tests [V, P2] |
| `bmad-retrospective` | Judge a completed epic against its evidence | Retro doc, action items, verdict [V, P2, P9] |

Old names (`bmad-create-prd`, `bmad-edit-prd`, `bmad-market-research`, etc.) still resolve as forwarders. [V, P2]

## Persona anatomy (from the Developer agent, Amelia)

Read from the clone's `skills/bmad-agent-dev/SKILL.md` and `customize.toml` (P12) and confirmed present in the lab install. [V, P12; V-lab] **Release difference:** at the `v6.12.0` tag the agents' `customize.toml` is identical to the clone, but `SKILL.md` activation also loads `user_name` and `communication_language` from config and greets the user by name; the clone dropped those lines. The activation sequence below is the clone's; the release adds that config load and named greeting. [V-lab, installed-vs-clone diff 2026-09-19]

- **Fixed identity:** `name` and `title` are hardcoded (Amelia, Senior Software Engineer). "Create a custom agent if you need a new name/title." [V, P12]
- **Configurable layer:** `icon`, `role`, `identity`, `communication_style`, `principles` (array), `persistent_facts` (array; literal sentences or `file:` paths/globs), `activation_steps_prepend` / `_append`, and the menu (`[[agent.menu]]` entries, each with a `code`, a `description`, and either a `skill` or a `prompt`). [V, P12]
- **Amelia's content:** role "implement approved stories with test-first discipline"; identity cites Kent Beck's TDD and the Pragmatic Programmer; style "ultra-succinct, speaks in file paths and AC IDs"; principles include red-green-refactor, tasks in written order, no epic/story references in code comments, comments explain why. [V, P12]
- **Activation sequence (8 steps):** resolve the agent block (base → team → user override files, via a `uv run` Python script, with a manual fallback) → run prepend steps → adopt persona and stay in character → load persistent facts → load config (planning_artifacts, project_knowledge) → greet with the agent's icon and mention `bmad-help` → run append steps → dispatch a menu item directly if the user's message already names one, otherwise show the menu and wait. [V, P12]
- **Override layers:** `customize.toml` (defaults, overwritten on update) → `_bmad/custom/<skill>.toml` (team) → `_bmad/custom/<skill>.user.toml` (personal). Scalars override, tables deep-merge, arrays of tables keyed by `code`/`id` replace matching entries and append new ones, other arrays append. [V, P12]
- So an agent is mostly **a prompt-defined persona plus a menu that routes to other skills.** Amelia's menu items are all skill dispatches (`bmad-build`, `bmad-qa-generate-e2e-tests`, `bmad-code-review`, `bmad-sprint-planning`, `bmad-retrospective`). [V, P12] The other four agents' personas are in the next section. [V, P22]

## The other four personas (P22)

Read from each agent's `customize.toml` (P22, 2026-09-19, unattended run). All five share one structure: fixed `name` and `title`, configurable `icon`, `role`, `identity`, `communication_style`, `principles`, and a menu. Diffing the four `SKILL.md` files against Amelia's shows they differ only in name, description, and title: the same activation sequence is templated across all five. [V, P22]

| Agent | Role (phase) | Identity (named influences) | Style | Principles |
|---|---|---|---|---|
| **Mary**, Business Analyst | Ideate, research, and analyze before committing to a project (analysis phase) | Michael Porter's strategic rigor, Barbara Minto's Pyramid Principle | "Treasure hunter's excitement for patterns, McKinsey memo's structure for findings" | Findings grounded in verifiable evidence; requirements stated with absolute precision; every stakeholder voice represented |
| **John**, Product Manager | Turn vision into a validated PRD, epics, and stories (planning phase) | Marty Cagan, Teresa Torres; Bezos's six-pager discipline | "Detective's 'why?' relentless. Direct, data-sharp" | PRDs come from user interviews, not template filling; ship the smallest thing that validates the assumption; user value first, feasibility is a constraint |
| **Winston**, System Architect | Turn PRD and UX into architecture decisions (solutioning phase) | Martin Fowler's pragmatism, Werner Vogels's cloud-scale realism | "Calm and pragmatic ... Answers with trade-offs, not verdicts" | Rule of Three before abstraction; boring technology for stability; developer productivity is architecture |
| **Sally**, UX Designer | Turn user needs and the PRD into UX specifications (planning phase) | Don Norman's human-centered design, Alan Cooper's persona discipline | "Paints pictures with words ... Empathetic advocate" | Every decision serves a genuine user need; start simple, evolve through feedback; data-informed but always creative |

All [V, P22]. Amelia (Developer) is in the anatomy section above [V, P12].

**Menus, as coded in the files:** [V, P22]

- **Mary:** `BP` brainstorming (skill `bmad-brainstorming`); `MR` market, `DR` domain, `TR` technical, `CR` competitive, `UV` user-voice research and `TS` technology selection, all six dispatched as prompts into `bmad-deep-recon` with the research type pre-selected; `CB` `bmad-product-brief`; `WB` `bmad-prfaq`; `PC` `bmad-project-context`.
- **John:** `PRD` `bmad-prd`; `CE` `bmad-create-epics-and-stories`; `IR` `bmad-sprint-planning` (readiness gate; can stop after the gate or continue into tracking); `CC` `bmad-correct-course`.
- **Winston:** `CA` `bmad-architecture`; `IR` `bmad-sprint-planning`.
- **Sally:** `CU` `bmad-ux` (single item).

**Observations**

- Every agent menu item resolves to a skill or a prompt that invokes one; none contains workflow logic itself. The agents are entry points and personas over the same skills anyone can invoke directly. [V, P22 menus; I, the generalization]
- Six of Mary's ten codes are one skill, `bmad-deep-recon`, entered with a different pre-selected type. [V, P22]
- `IR` (implementation readiness) appears on both John and Winston and both open `bmad-sprint-planning`. [V, P22] So a code is scoped to the agent showing it: the same code can mean different things on different agents (`CR`: competitive teardown for Mary, code review for Amelia) or the same thing on two (`IR`). [V, P2; I on the pattern]
- Each agent's `role` names a BMad Method phase (analysis, planning, solutioning), so the roster reads as a phase-ordered handoff: Mary, John and Sally, Winston, Amelia. [I]
- Personas cite real practitioners as shorthand (Porter, Minto, Cagan, Torres, Fowler, Vogels, Norman, Cooper, Beck). Whether the model's behavior changes measurably because of these names is not tested. [?]

## Other skills worth knowing

- **`bmad-deep-recon`** has three modes: **Draft** (writes a research prompt for your own deep-research tool such as ChatGPT, Gemini, Grok or Perplexity), **Process** (files a finished report, extracts claims, flags what it never covered, writes a standard `research.md` summary), and **Run** (does the research in-session after you approve a plan). Types: market, domain, technical, competitive, user-voice, academic-lit; plus Explore vs Select. Claims come from sources retrieved during the run, not model memory, and each carries publisher, date, and inline citation. Stale figures are reported as history. Refresh re-checks only fast-aging claims. [V, P13]
- **`bmad-code-review`:** at the release, four review layers run in parallel on the same diff (Blind Hunter, Edge Case Hunter, Verification Gap, and an Acceptance Auditor when a spec is given), with no depth selector. [V, tag docs P14; V-lab, Experiment 3] Triage then verifies each finding, assigns severity, dismisses noise with a recorded reason, and routes survivors to patch, defer, or decision-needed. Quality depends on being given intent (a spec) as well as the diff. Several rounds of review that keep finding non-trivial issues signal a problem upstream (weak spec, contradiction), not more review passes. [V, P14] ~~`thorough` is the default, `quick` is one reviewer.~~ Clone-only (P14 as read from the clone's docs); not in the release.
- **`bmad-project-context`:** reads what the repo already states, asks what a scan cannot answer (five questions in the lab), then proposes the complete `AGENTS.md` block and asks before writing; it never commits. [V, P24; V-lab, Experiment 4] It keeps only what is expensive to rediscover: of five planted conventions it recorded two, judging the other three discoverable from the code. It also refused its own evidence: it found a real test-glob pitfall only by running a deliberately non-matching glob, and left it out because "a constructed trap isn't evidence." [V-lab, `lab-log.md` Experiment 4 follow-up] Whether the resulting file changes a later build: see Experiment 4b (same code, different escalation; `systemic-findings.md`). [V-lab]
- **`bmad-build-auto`:** the unattended worker for one unit. Needs subagents (otherwise halts `blocked`: `no subagents`). Reads `stories.yaml` for a story by id, writes `stories/<id>-<slug>.md`, ends with a machine-readable status in the spec's frontmatter: `draft`, `ready-for-dev`, `in-progress`, `in-review`, `done`, `blocked`. It commits but does not push. Blocked is "a routing signal, not just a failure signal." An orchestrator (a coding session or the optional `bmad-loop` tool) picks the next story; build-auto never does. [V, P15]

## Open

- Which skills spawn subagents and which run in one context. `bmad-build`, `bmad-code-review` and `bmad-build-auto` are documented as needing or preferring subagents. [V, P8, P14, P15] **Observed for `bmad-build`:** headless `claude -p` spawned implementation and review subagents once permission was given (Experiment 5h, `build-step-by-step.md`). [V-lab] `bmad-code-review` and `bmad-build-auto` not observed; the no-subagent fallback not observed. [?]
- What loading an agent persona changes. Every lab run invoked skills directly; no agent session (e.g. Amelia's `BD`) has been run. [?] Candidate experiment in `STATE.md` Next.
