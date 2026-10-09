# BMAD v7 Preview: What Changes

*Describes **unreleased** BMAD-METHOD `main` at commit `bda3c59` (2026-10-06), which its own changelog calls "a first draft for v7". **Nothing here is a release.** npm `latest` is 6.12.1 and there are no v7 tags (both checked 2026-10-09). Main changes daily, so treat every claim as a snapshot of that commit. Source: the worktree `labs\BMAD-METHOD-v7p-bda3c592` (P34 in `../sources.md`): `CHANGELOG.md` "Unreleased", `docs/start/install-bmad.md`, `docs/plan/set-up-the-ticket-tree.md`, `skills/bmod-method/migration-1.toml` and `retired.toml`, `skills/bmad-build/customize.toml` and `plan-template.md`, `skills/bmad-retrospective/` file list and `references/aggregate-views.md`, and a skill-by-skill diff against the v6.12.0 tag. Tags: [V, P34] traced to those files at that commit, [I] inferred, [?] unclear. Nothing here has been run in a lab. Written unattended-style 2026-10-09; not yet reviewed.*

!!! tip "TL;DR"
    v7 is a restructure, not an update. Install moves from `npx bmad-method install` to `npx skills add` plus a `bmad` setup skill. The `planning_artifacts` / `implementation_artifacts` folders give way to one folder per **initiative**. `epics.md` and `sprint-status.yaml` become a **ticket tree** managed by a new `bmad-ticket` skill, which also replaces `bmad-sprint-planning` and `bmad-create-epics-and-stories`. A `bmad migrate method` command moves a v6 project across. `bmad-build` now defaults to a single quick review lens. BMB becomes Toolsmith. NGA runs 6.12.0, so nothing here changes the wiki's existing claims until NGA updates. [V, P34; I on NGA]

## Install and update

- **Install:** `npx skills add bmad-code-org/BMAD-METHOD`, selecting skills plus the `bmad` hub and module records (`bmod-core-tools`, `bmod-method`); or a Claude Code / Codex plugin marketplace. Then ask the `bmad` skill to run `bmad setup`, which installs the shared runtime under `_bmad/`. [V, P34 install doc] The repo no longer has a `package.json` at its root; it ships a Python `pyproject.toml` and uses `uv`. [V, P34 tree]
- **Update:** ask `bmad` to run `bmad setup` again. It runs `npx skills update` when a module has a newer version, asks any new config questions, moves `_bmad/custom/` files for renamed skills, offers to delete renamed or removed skills (each module lists them in a `retired.toml`), and ends by checking whether a migration applies. [V, P34 install doc, CHANGELOG]
- `bmad status` checks versions and lists uninstalled skills of each module. [V, P34 CHANGELOG]
- **"Team and personal customizations live under `_bmad/custom/` and survive setup refreshes."** That is the same rule [updating-bmad.md](updating-bmad.md) tested on 6.12.0. Whether it holds under `bmad setup` is untested. [V, P34 install doc; ? untested]
- So most of [updating-bmad.md](updating-bmad.md) is about an installer v7 drops: `--pin`, `--action`, quick-update vs full update, `manifest.yaml`. [I]

## Where documents go: initiatives

- **Every document lands in the active initiative**, as `<type>-<slug>/<type>-<slug>.md` under `output_folder`, inside `initiative-<slug>/` when one is active. `planning_artifacts` and `implementation_artifacts` "are no longer read or seeded". [V, P34 CHANGELOG]
- `active_initiative` is a personal setting in `_bmad/custom/config.user.toml` under `[core]`. The `bmad` skill shows, switches, creates and clears it. [V, P34]
- Multi-repo work: install BMad at a workspace folder above the repos and give the store its own `git init`, so planning history stays apart from code history. [V, P34 ticket-tree doc]
- Every artifact path the wiki cites (`_bmad-output/specs/spec-*/SPEC.md`, `implementation-artifacts/spec-*.md`, `deferred-work.md`, `sprint-status.yaml`) moves under v7. The claims about what those files *contain* may still hold; the paths won't. [I]

## Planning and tracking: the ticket tree and `bmad-ticket`

- `bmad-ticket` "is how BMad plans and tracks work": initiatives hold epics, epics hold stories, spikes and bugs. Each level keeps its breakdown in a `tickets.toml`. An entry carries what it delivers, a `verify` check, `after` prerequisites (which can name a story in another epic, or a whole epic), and any `unknown`. [V, P34 ticket-tree doc]
- **It replaces `bmad-sprint-planning` and `bmad-create-epics-and-stories`**, which are removed. [V, P34 `retired.toml`, migration-1 guide] So the readiness gate (PASS / CONCERNS / FAIL) the wiki describes in [flow.md](flow.md) has no counterpart named in the files read. [I; ? whether `bmad-ticket` carries an equivalent]
- **Stories are planned at build time.** "An entry needs no file to be built. `bmad-build` plans the story's acceptance criteria when it builds", and writes the plan beside `tickets.toml` as `story-<slug>-plan.md`. [V, P34 ticket-tree doc] The build spec becomes a **plan**: `spec-template.md` is now `plan-template.md`, the Spec Change Log is the Plan Change Log, and the `<frozen-after-approval>` block over Intent, Boundaries and the I/O matrix stays. [V, P34 `plan-template.md`]
- **New `built` status.** "Build moves it as it works and stops at `built`; only you, or an orchestrator, mark a story done." [V, P34 ticket-tree doc; `plan-template.md` status list]
- **Cutting epics:** "An epic is one capability that one owner delivers to production." After epics are agreed, the skill lists decisions more than one epic must adopt and offers `bmad-architecture`; declined, each becomes a story in the opening epic that the others wait on. [V, P34 ticket-tree doc] That is a direct mechanism for the cross-epic gap in [systemic-findings.md](systemic-findings.md) ("Freezing stops at the epic boundary"), at planning time rather than at code time. Whether it would have caught Experiment 9b's case is untested. [I; ?]
- **Trackers:** Repo (the default; markdown files in the store), GitHub Issues, Jira, Linear, Notion, Trello. The markdown files stay the working copy. **"Hooks are not integrated yet, so nothing syncs on its own"**: the tracker and files line up only when you run the skill. The docs say Repo "has been tested most" and the trackers "still need a lot of testing". [V, P34 ticket-tree doc] So the wiki's Finding 5 ("no automatic sync with Jira/Linear", STATE.md) becomes "on-demand publish and read-back, no automatic sync" in v7. [I]

## Moving a v6 project: `bmad migrate method`

`skills/bmod-method/migration-1.toml` is the v6 → v7 migration. [V, P34]

- **Detects** v6 by `epics.md`, `sprint-status.yaml`, v6 build-spec files (`route:` + `status:` frontmatter), dated artifact folders, or `specs/spec-<slug>/SPEC.md`. [V, P34]
- **Asks first, writes nothing before approval** except a plan file and a backup. Its six questions come with defaults: back up first (yes); one initiative or several; will the work touch other repos (workspace layout); keep planning history in its own repo; finish in-progress stories in v6 first (default "Finish first"); fold unstarted story files into their entries (yes). [V, P34]
- **Moves, never copies,** with `git mv` so history follows. It drops dates and v6 story/epic numbers from names. It turns `epics.md` + `sprint-status.yaml` into `tickets.toml` entries with mapped statuses and archives the originals unchanged in `archive-v6/`. Retrospectives combine into one file per epic. It rewrites live path references inside the store, but only lists (never edits) old paths found elsewhere in the project. [V, P34]
- **A `spec-<slug>/` with `stories.yaml` becomes an epic,** its stories become entries citing the spec's `CAP-N` ids, and each `stories/<id>-<slug>.md` moves as `story-<slug>-plan.md`. This is the shape of the lab's tags epic (`lab5-route`). [V, P34; I on the match]
- **It never pushes,** and it ends with an 11-item verification checklist recorded in the plan ("never skip one"). [V, P34]

## Build and review

- **`bmad-build` defaults to `review = "quick"`**: a single "Quick" subagent lens reading the plan, the repo's agent instruction files and the diff, reporting unmet criteria, broken rules and bugs. `thorough` (Blind Hunter, Edge Case Hunter, Verification Gap, Intent Alignment Auditor) is still there; `auto` picks quick for oneshot and thorough for the full route. [V, P34 `bmad-build/customize.toml`; CHANGELOG] At 6.12.0 the dispatch route ran three layers by default ([build-step-by-step.md](build-step-by-step.md)). So by default v7 reviews each story with less, and the per-story blind spot in [systemic-findings.md](systemic-findings.md) likely widens. [I]
- The quick lens reads `AGENTS.md`/`CLAUDE.md` "at the repository root and in the directories the diff touches; those are the rules". [V, P34] So project context feeds review directly, which bears on the [?]-marked escalation finding from Experiments 4b and 18. [I]
- **The retrospective was rewritten** (about 2,700 lines removed, mostly bundled files) and now takes "a finished epic folder in the ticket tree". It keeps an explicit whole-epic phase: "the defects that matter are the ones no single session — and no single diff hunk — could see." [V, P34 `SKILL.md`, `aggregate-views.md`] Whether it still accepts a v6 spec folder directly wasn't checked; the migration converts one into an epic. [?]
- Review mode (in review skills) now gives findings in chat and in markdown; "the HTML report is gone". [V, P34 CHANGELOG] Whether that covers `bmad-prd` Validate's HTML report (Experiment 15) is unclear. [?]

## Skills added and removed

Diff of skill folders, v6.12.0 tag vs `main@bda3c59` (50 → 33). [V, P34]

- **Added:** `bmad` (setup / status / migrate / help hub), `bmad-ticket`, `bmad-toolsmith` and `bmad-eval` (with module records `bmod-core-tools`, `bmod-method`, `bmod-toolsmith`).
- **Removed for real:** `bmad-sprint-planning`, `bmad-create-epics-and-stories`, `bmad-help` (its job moves to `bmad`). The rest of the 24 removed names were v6 forwarding shims (old names such as `bmad-quick-dev`, `bmad-create-prd`, `bmad-dev-story`) and the old review and research skills already merged in 6.11.0. The v6 changelog said those shims would go "at the v7 cut". [V, P34; V, CHANGELOG v6.11.0]
- **BMB becomes Toolsmith:** one agent, "Smithy", and `bmad-eval`. It builds skills, agents, memory agents and modules from a conversation, converts prompts from other tools, mines skills from session logs, and migrates v6 modules. Its retired list names BMB's agent, workflow and module builders. [V, P34 CHANGELOG, `bmod-toolsmith/retired.toml`] So Experiment 13's BMB build would be a Toolsmith build in v7. [I]
- **Web bundles are removed;** Gemini Gems and ChatGPT Custom GPTs are deprecated in favor of skills. [V, P34 CHANGELOG]
- The five agents are still present (`bmad-agent-analyst`, `-pm`, `-ux-designer`, `-architect`, `-dev`). [V, P34 tree]

Change size in the skills the wiki relies on (files / lines, `git diff --shortstat`): `bmad-build` 15 / +332 −307; `bmad-build-auto` 12 / +291 −236; `bmad-code-review` 11 / +305 −367; `bmad-walkthrough` 13 / +259 −517; `bmad-retrospective` 14 / +177 −2746; `bmad-architecture` 7 / +137 −101; `bmad-spec` 6 / +42 −93; `bmad-prd` 7 / +36 −29; `bmad-correct-course` 3 / +31 −41; `bmad-project-context` 2 / +14 −5; `bmad-agent-dev` 3 / +25 −16. [V, P34] Only the build customization, plan template and retrospective entry files were read; the rest are counted, not read. [?]

## What this means for the wiki's pages

| Page | Effect under v7 (if NGA updates) |
|---|---|
| [updating-bmad.md](updating-bmad.md) | Mostly superseded: different installer and update path. The `_bmad/custom/` rule is restated in v7 docs, untested. [I] |
| [flow.md](flow.md) | Planning half changes: ticket tree instead of `epics.md` / `sprint-status.yaml`; readiness gate removed with `bmad-sprint-planning`; stories planned at build time; new `built` status. [I] |
| [build-step-by-step.md](build-step-by-step.md) | Spec → plan, Spec Change Log → Plan Change Log, review default quick (one lens). Frozen block unchanged. Step mechanics not re-read. [I] |
| [systemic-findings.md](systemic-findings.md) | Per-story review gets thinner by default; cross-epic decisions get a planning-time mechanism; the retrospective keeps its whole-epic view. Each needs a lab rerun before any claim changes. [I] |
| [spec-skill.md](spec-skill.md), [prd-skill.md](prd-skill.md), [architecture-skill.md](architecture-skill.md) | Small diffs; mostly output paths. [I] |
| [agents.md](agents.md) | Five agents unchanged in name; `bmad-help` → `bmad`; BMB → Toolsmith. [I] |
| STATE.md Finding 5 (no tracker sync) | Becomes on-demand publish and read-back via `bmad-ticket`; still no automatic sync. [I] |

## Not yet checked

- Any lab run: install, `bmad setup`, `bmad migrate method` on a v6 project, `bmad-ticket` on the repo store. [?]
- The full step files of `bmad-build`, `bmad-code-review`, `bmad-walkthrough`, `bmad-retrospective` and `bmad-ticket` at this commit. [?]
- Whether anything replaces the removed readiness gate. [?]
- Whether `_bmad/custom/` overrides survive `bmad setup` and the migration. [?]
- A v7 release date or version number; none is stated in the files read. [?]
