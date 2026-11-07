# Updating BMAD: What Survives and What Doesn't

*Describes BMAD-METHOD v6.12.0 and its installer. Sources: `docs/customize/customize-bmad.md` (P30) and `docs/customize/add-modules.md` (P27) at the release tag, see `../sources.md`. Tags: [V, Pn] traced to those docs, [V-lab] observed in a lab run (Experiments 8 and 13, see [lab-log.md](lab-log.md)), [I] inferred, [?] unclear. No release newer than 6.12.0 existed when this was written, so the "update" tested was a same-version reinstall. Written 2026-10-03. Re-pin notes for 6.12.1 and Experiment 16 (first real update, 6.12.0 → 6.12.1) added 2026-10-07, not yet reviewed. Team-customization section from `docs/customize/adopt-bmad-across-a-team.md` (P35) install-docs bullet (P38, read at 6.12.1), and "How 6.12 got here" changelog section (P42) added 2026-10-18, docs-only, not yet reviewed.*

!!! note "v7 preview"
    BMAD's unreleased v7 draft replaces this installer (`npx skills add` plus a `bmad setup` skill). Most of this page applies to 6.x only. See [v7-preview.md](v7-preview.md).

!!! tip "TL;DR"
    Put every customization in `_bmad/custom/`. Those files survived a reinstall byte for byte. A direct edit to a skill's own `customize.toml` was overwritten with no backup. A direct edit to the installer's `_bmad/config.toml` was regenerated but kept as `config.toml.bak`. Skill folders you add yourself were left alone. On 6.12.0, a central override in `_bmad/custom/config.toml` survives but most skills ignore it; 6.12.1 fixes that. Check versions in `_bmad/_config/manifest.yaml`, not on npm, and read `lastUpdated` as "last install run", not "last real change".

## Check what you have installed

`_bmad/_config/manifest.yaml` lists every installed module with `version`, `installDate` and `lastUpdated`. External modules also record `source: external`, a `repoUrl`, a `channel` (for example `pinned`) and the git `sha` they were installed from. [V, P27; V-lab, Experiment 8]

- **Check an add-on module's currency against its GitHub tags, not its npm page.** The installer's `--pin CODE=TAG` resolves against tags on the module's own repository. In the lab, two modules' npm pages were a major version behind the versions actually installed from GitHub. [V-lab, Experiment 8]
- **`lastUpdated` moves on every module at every install,** even when nothing changed; `installDate` stays. It tells you when the installer last ran, not when a module last changed. [V-lab, Experiment 13]

## What an update keeps and what it replaces

Tested by planting one change of each kind, snapshotting, reinstalling, and diffing. [V-lab, Experiment 13]

| You changed | Docs say | Observed after reinstall |
|---|---|---|
| A per-skill override, `_bmad/custom/<skill>.toml` | "Updates do not touch your files" [V, P30] | Survived, byte-identical |
| A central override, `_bmad/custom/config.toml` | "never touched by the installer" [V, P30] | Survived, byte-identical |
| A skill's own `customize.toml`, edited directly | "Never edit it; updates overwrite it" [V, P30] | **Overwritten, no backup** |
| The installer's `_bmad/config.toml`, edited directly | "regenerated on every install" [V, P30] | Regenerated; your version saved as **`_bmad/config.toml.bak`** (not documented) |
| A skill folder you added under `.claude/skills/` | Not documented | Left alone |
| A skill built with the Builder module (BMB), in `skills/` | Not documented | Left alone; it was never installed into `.claude/skills/` in the first place |

!!! warning "On 6.12.0, surviving is not the same as applying (Experiment 16, 2026-10-07)"
    The table shows that `_bmad/custom/config.toml` **survives**. On 6.12.0 it is **not applied** by most skills. The 6.12.1 changelog says 23 bmm skills (including `bmad-code-review`, `bmad-prd`, `bmad-ux`, `bmad-correct-course`, `bmad-retrospective`, `bmad-walkthrough`, the five agents, and the v6 shims) loaded config from `_bmad/bmm/config.yaml` directly; 6.12.1 routes them through `resolve_config.py`. [V, CHANGELOG v6.12.1 and the tag diff] **Observed for `bmad-code-review`:** with `communication_language = "French"` in `_bmad/custom/config.toml`, the resolver returned French on both versions, but the 6.12.0 skill read `bmm/config.yaml` and reviewed in English; after a 6.12.1 update, the same untouched file made the review come out in French. The run traces show which config each read. [V-lab, Experiment 16] The other 22 skills are covered by the changelog, not tested one by one. [I] Also, 6.12.1's `_bmad/config.toml` now carries user-scope defaults, including `user_name = "BMad"` (the module default; the real name stays in `config.user.toml`, which wins). [V-lab, Experiment 16] The fix takes effect only after re-running the installer. [V, CHANGELOG] **Per-skill overrides are a separate path:** the same 6.12.0 trace shows the skill calling `resolve_customization.py`, so `_bmad/custom/<skill>.toml` is read on 6.12.0. [V-lab, trace] Whether a given per-skill value then takes effect was not planted here. [I] On 6.12.0, change a central setting by re-running the installer with the new answer; a hand edit to `_bmad/bmm/config.yaml` is regenerated on the next install. [V-lab, Experiment 13; I]

So the documented rule held, with one undocumented safety net: the installer-owned config gets a `.bak`, but a skill's `customize.toml` does not. An edit made there is simply gone. [V-lab]

A per-skill override also wins at runtime over a direct edit to the shipped file, so there is no reason to edit the shipped file at all: the resolver returned the override's value while both existed. [V-lab, Experiment 13; V, P30] Keep overrides sparse: "A full copy locks in today's defaults, so the next update ships new values that your override silently shadows." [V, P30]

## How the installer runs an update

- **The non-interactive default is a quick-update.** `install --yes` with no `--action` on an existing install "Refreshes installed modules from their recorded sources" and does not add new modules. To add modules, pass `--action update` explicitly. [V, P27; V-lab, Experiment 8]
- **A failed update can leave a half-applied install.** In the lab, a full update failed on a malformed module-list argument (a shell quoting mistake). Before it reported failure, it had deleted every module's `config.yaml` and `module-help.csv` and added stray copies of core skill files. Overrides survived, and a correct re-run repaired everything. The trigger was a usage error, but the installer did not roll back. [V-lab, Experiment 13] Take a copy of `_bmad/` and `.claude/` before updating, and if an update fails, re-run it correctly rather than working from the half-updated state. [I]
- **A version bump of installed modules needs no `--action`.** A plain quick-update with the version named (`npx -y bmad-method@6.12.1 install ... --yes`) took core and bmm 6.12.0 → 6.12.1. Untested: an unpinned `npx bmad-method` (the npx cache could serve the older version). [V-lab, Experiment 16; ? on unpinned]
- **What the install docs cover, and what they leave out** (P38, `docs/start/install-bmad.md` at tag `v6.12.1`, added 2026-10-18). The interactive path: re-run `npx bmad-method install` in the project, and the installer detects the existing install and offers "update" (refresh) or "modification" (change modules, tools, config); verify by running `bmad-help` again. Coming from an earlier version, it warns about stale `bmad-*` entries in legacy command directories that you should remove to avoid duplicate commands. `npx bmad-method@next install` installs the prerelease. The CI example is `install --yes --modules bmm --tools claude-code`, and the docs say to check `--help` with the same version or tag you install. [V, P38] The page says nothing about backing up first, the non-interactive quick-update default, the `.bak`, or the lack of rollback, all observed above. [V-lab; I that a reader of P38 alone would miss them]
- On Windows PowerShell, quote comma lists (`--modules "bmm,tea"`); unquoted, the shell splits them. [V-lab, Experiment 13]

## How 6.12 got here: what the changelog says matters for an installed team (P42, added 2026-10-18)

*From `CHANGELOG.md` at tag `v6.12.1`, releases 6.8.0 (2026-05-25) to 6.12.1 (2026-10-04). Older entries (6.7.1 back to the 6.0 alphas) not read.*

- **The config gap Experiment 16 found was a planned halfway state.** 6.11.0 moved config to layered TOML and said so outright: "The per-module `_bmad/bmm/config.yaml` still ships and the older skills still read it, so this release is the migration, not the cutover." 6.12.1 finished the cutover. [V, P42 v6.11.0, v6.12.1] So anyone on 6.11.x or 6.12.0 has central overrides that only some skills honor (see the warnings above). [I]
- **A broken override stops the skill.** Since 6.11.0, a `{{.var}}` missing from the merged config, or an unparseable `_bmad/custom/<skill>.toml`, makes the renderer "exit 1 with a clean halt" (it used to render empty or ignore the file). [V, P42 v6.11.0 #2588] A typo in a team override is no longer silent, but it blocks everyone who pulls it until fixed. [I]
- **6.12.0's breaking changes that touch customizations:** `persistent_facts` now ships empty ("Re-add `project-context.md` to your override if you relied on the auto-load"); review overrides must rename `{diff_output}` to `{diff_file}`; deprecated shims are opt-in on fresh installs (`--shims`); `bmad-checkpoint-preview` became `bmad-walkthrough` (`CK` → `WT`, old ID forwards); build no longer auto-triggers on interactive edits or chores. [V, P42 v6.12.0]
- **6.11.0 renamed things your override files are named after.** `bmad-quick-dev` → `bmad-build`, `bmad-dev-auto` → `bmad-build-auto`, and `_bmad/custom/bmad-quick-dev{,.user}.toml` must be renamed by hand. The forwarding shim offers the migration but won't overwrite, and "unattended runs on the old name with a legacy customization file will refuse to start." Also retired into shims: three review skills and two editorial ones (now lenses on `bmad-review`), the research trio (now `bmad-deep-recon`), `bmad-document-project` and `bmad-generate-project-context` (now `bmad-project-context`), `bmad-sprint-status`, and `bmad-create-story`/`bmad-dev-story`. Shims last until v7. [V, P42 v6.11.0]
- **`uv` went from "recommended" to required for rendered skills in two steps:** 6.9.0 warned, and 6.11.0 made `bmad-build`/`bmad-build-auto` halt without it. Even 6.11.0's installer still showed uv as optional inside the green "ready" box until #2704 fixed the wording. [V, P42 v6.9.0, v6.11.0] Matches the install-doc correction on [overview.md](overview.md). [V]
- **Unpublished evidence behind design choices.** Several entries cite internal trials: the adversarial-reviewer A/B (see [agents.md](agents.md)), "seven real commits from a production HIPAA platform" for the verification-gap reviewer, "16 reviewer runs" for its false-gap fix, and a "50% to 100%" catch-rate gain for Edge Case Hunter's named-set pass. None link to data. [V that they are claimed; ? on the results]

## What to re-read after a version bump

Most skills changed only cosmetically between releases this project compared. The two that changed substantively between the 6.12.0 release and the later unreleased code were **`bmad-build`** (how it picks a route) and **`bmad-code-review`** (how its review layers are chosen). See [build-step-by-step.md](build-step-by-step.md), "What the clone changed". After a version bump, re-read those two first, and diff their installed `SKILL.md` and step files against the previous version. [V-lab; I on the priority]

**The first real bump, 6.12.0 → 6.12.1 (2026-10-04), did not follow that pattern:** `bmad-build`, `bmad-build-auto`, and `bmad-spec` did not change at all; 23 other skills changed one config-loading line each; `bmad-create-epics-and-stories` now saves `epics.md` as `status: draft` and sets `status: final` only when every validation check passes; party mode's collision check now sees aliases. [V, CHANGELOG v6.12.1 and `git diff v6.12.0 v6.12.1`] The changelog is the faster first read; the "re-read build and review first" advice above is [?] re-check as a general rule. [I]

## Customizing for a whole team (the docs' recipes)

*Added 2026-10-18 from `docs/customize/adopt-bmad-across-a-team.md` at the tag (P35). Docs-only; no recipe has been run in the lab.*

The docs give six recipes, each one override file under `_bmad/custom/`, committed so everyone inherits it on pull. Every per-skill file has a team form (`<skill>.toml`, committed) and a personal form (`<skill>.user.toml`, gitignored); central config splits the same way. [V, P35] The `bmad-customize` skill writes and verifies recipes 1 to 4 and 6; recipe 5 is written by hand. [V, P35; skill exists at the tag]

| Scope of the rule | Where it goes | Key(s) |
|---|---|---|
| All dev work, whatever workflow the agent dispatches | `_bmad/custom/bmad-agent-dev.toml` | `[agent] persistent_facts` (recipe 1) |
| One workflow's output (compliance fields, conventions doc via `file:`) | `_bmad/custom/<workflow>.toml` | `[workflow] persistent_facts` (recipe 2) |
| Publish when a workflow finishes (Confluence, Jira) | same | `[workflow] on_complete`, runs once after output is written (recipe 3) |
| Your own output template | same | e.g. `brief_template`, `prd_template` (recipes 4, 6) |
| Who is on the roster; shared paths and output language | `_bmad/custom/config.toml` | `[agents.<code>]`, `[modules.bmm]`, `[core]` (recipe 5) |
| On-demand knowledge sources, stacked handoffs, finalize-time writing standards | `_bmad/custom/<workflow>.toml` | `external_sources`, `external_handoffs`, `doc_standards` (recipe 6; check the workflow's `customize.toml` for which it has) |

[V, P35; each key checked present in the tag's `customize.toml` for `bmad-product-brief`, `bmad-prd`, `bmad-agent-dev`]

- **Rules that must hold outside BMAD go in the IDE session file too** (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`): BMAD customizations load only when a skill activates. Keep that file short; the model reads it every turn. [V, P35]
- **The recipes describe intent; they do not change approval behavior.** Recipe 3's example asks before creating a Jira epic and publishes to Confluence without asking, because the prose in `on_complete` says so. Whatever confirmation a team wants has to be written into that text. [V, P35; I on the generalization]
- **A misnamed file or a disconnected MCP server fails quietly.** The file must carry the exact skill directory name, and an MCP tool named in `persistent_facts` or `on_complete` "does nothing if that server is not connected." [V, P35] For `external_sources` and `external_handoffs` the docs say the gap is noted or flagged; for `persistent_facts` they promise no such note. [V, P35; I on the contrast]

!!! warning "On 6.12.0, recipe 5's shared-path pin splits the team's output (source reading, not lab-tested)"
    Recipe 5c pins `planning_artifacts` and `document_output_language` in `_bmad/custom/config.toml`. At the 6.12.0 tag, the skills that use `planning_artifacts` split by how they load config. **Through the merged config (would see the pin):** `bmad-architecture` and `bmad-deep-recon` (via `resolve_config.py`), and `bmad-build` (its step files use `{{.planning_artifacts}}`, filled by the renderer from the merged config). **Straight from `_bmad/bmm/config.yaml` (would not):** `bmad-prd`, `bmad-product-brief` (the recipe page's own running example), `bmad-ux`, `bmad-prfaq`, `bmad-create-epics-and-stories`, `bmad-sprint-planning`, `bmad-code-review`, `bmad-correct-course`, `bmad-retrospective`, `bmad-walkthrough`, and all five agents. [V, each skill's activation step at the tag (grep); V, P42 CHANGELOG v6.11.0 on the renderer's merged config] `bmad-spec` is not affected either way: it writes to `{output_folder}/specs/`, not the planning folder. [V, `bmad-spec/SKILL.md` line 32] 6.12.1 moves the 23 direct readers to the resolver. [V, CHANGELOG v6.12.1] So on 6.12.0, a pinned planning path would likely put the PRD, UX spines, and epics in the installer's folder while `bmad-architecture` writes to the pinned one and `bmad-build` looks for planning docs in the pinned one, where the PRD and epics aren't. [I, not observed] That is the same gap Experiment 16 observed for `bmad-code-review` (see the warning above). The roster recipes (5a, 5b) look unaffected for party mode, which reads the roster through the resolver at 6.12.0. [V, source; I on effect] *(Corrected 2026-10-18 by a claim-check pass: the first version named `bmad-spec` and party mode as the skills that would follow the pin, but neither reads `planning_artifacts`.)*

## A lightweight stance (options, not a recommendation)

None of these were tested as a team practice; they follow from what was observed. [I]

- **Update deliberately, not continuously.** Pin modules (`--pin`), and treat a version bump as a change of its own, between epics rather than mid-epic.
- **Read the release notes first,** then the two skills above.
- **Customizations only in `_bmad/custom/`.** Commit the team files; keep the `.user.toml` files personal.
- **Snapshot before updating** (copy `_bmad/` and `.claude/`), and diff after. The diff should show only regenerated config and manifest files.
- **After updating, check `_bmad/config.toml.bak`** if anyone may have edited the installer's config directly; that edit is now only in the backup.

## Not yet checked

- ~~Whether a central override reaches `bmad-code-review` on 6.12.0 vs 6.12.1.~~ Answered by Experiment 16 (see the warning above).
- ~~A real version-to-version update.~~ Done 2026-10-07 (Experiment 16): a plain `npx -y bmad-method@6.12.1 install --directory . --modules bmm --tools claude-code --yes` (quick-update, no `--action`) took core and bmm to 6.12.1, kept `_bmad/custom/` byte-identical, and left the file count unchanged. [V-lab] For 6.12.1, no skill's `customize.toml` changed (tag diff stat). [V] Still open in general: whether a new release changes `customize.toml` fields that existing overrides depend on. [?]
- Whether a full update treats direct edits the same way as a quick-update (the edits were not re-planted before the full run). [?]
- Personal `.user.toml` overrides and `config.user.toml` (only team files were tested). [?]
- Any of the six team recipes in a live run, in particular recipe 5c's pinned planning path on 6.12.0 vs 6.12.1 (would show the split predicted above) and whether a `persistent_facts` entry naming a missing MCP tool produces any notice. [?]
