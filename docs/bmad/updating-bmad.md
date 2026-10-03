# Updating BMAD: What Survives and What Doesn't

*Describes BMAD-METHOD v6.12.0 and its installer. Sources: `docs/customize/customize-bmad.md` (P30) and `docs/customize/add-modules.md` (P27) at the release tag, see `../sources.md`. Tags: [V, Pn] traced to those docs, [V-lab] observed in a lab run (Experiments 8 and 13, see [lab-log.md](lab-log.md)), [I] inferred, [?] unclear. No release newer than 6.12.0 existed when this was written, so the "update" tested was a same-version reinstall. Written 2026-10-03.*

!!! tip "TL;DR"
    Put every customization in `_bmad/custom/`. Those files survived a reinstall byte for byte. A direct edit to a skill's own `customize.toml` was overwritten with no backup. A direct edit to the installer's `_bmad/config.toml` was regenerated but kept as `config.toml.bak`. Skill folders you add yourself were left alone. Check versions in `_bmad/_config/manifest.yaml`, not on npm, and read `lastUpdated` as "last install run", not "last real change".

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

So the documented rule held, with one undocumented safety net: the installer-owned config gets a `.bak`, but a skill's `customize.toml` does not. An edit made there is simply gone. [V-lab]

A per-skill override also wins at runtime over a direct edit to the shipped file, so there is no reason to edit the shipped file at all: the resolver returned the override's value while both existed. [V-lab, Experiment 13; V, P30] Keep overrides sparse: "A full copy locks in today's defaults, so the next update ships new values that your override silently shadows." [V, P30]

## How the installer runs an update

- **The non-interactive default is a quick-update.** `install --yes` with no `--action` on an existing install "Refreshes installed modules from their recorded sources" and does not add new modules. To add modules, pass `--action update` explicitly. [V, P27; V-lab, Experiment 8]
- **A failed update can leave a half-applied install.** In the lab, a full update failed on a malformed module-list argument (a shell quoting mistake). Before it reported failure, it had deleted every module's `config.yaml` and `module-help.csv` and added stray copies of core skill files. Overrides survived, and a correct re-run repaired everything. The trigger was a usage error, but the installer did not roll back. [V-lab, Experiment 13] Take a copy of `_bmad/` and `.claude/` before updating, and if an update fails, re-run it correctly rather than working from the half-updated state. [I]
- On Windows PowerShell, quote comma lists (`--modules "bmm,tea"`); unquoted, the shell splits them. [V-lab, Experiment 13]

## What to re-read after a version bump

Most skills changed only cosmetically between releases this project compared. The two that changed substantively between the 6.12.0 release and the later unreleased code were **`bmad-build`** (how it picks a route) and **`bmad-code-review`** (how its review layers are chosen). See [build-step-by-step.md](build-step-by-step.md), "What the clone changed". After a version bump, re-read those two first, and diff their installed `SKILL.md` and step files against the previous version. [V-lab; I on the priority]

## A lightweight stance (options, not a recommendation)

None of these were tested as a team practice; they follow from what was observed. [I]

- **Update deliberately, not continuously.** Pin modules (`--pin`), and treat a version bump as a change of its own, between epics rather than mid-epic.
- **Read the release notes first,** then the two skills above.
- **Customizations only in `_bmad/custom/`.** Commit the team files; keep the `.user.toml` files personal.
- **Snapshot before updating** (copy `_bmad/` and `.claude/`), and diff after. The diff should show only regenerated config and manifest files.
- **After updating, check `_bmad/config.toml.bak`** if anyone may have edited the installer's config directly; that edit is now only in the backup.

## Not yet checked

- A real version-to-version update (no newer release existed). Whether a new release changes `customize.toml` fields that existing overrides depend on. [?]
- Whether a full update treats direct edits the same way as a quick-update (the edits were not re-planted before the full run). [?]
- Personal `.user.toml` overrides and `config.user.toml` (only team files were tested). [?]
