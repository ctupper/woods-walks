# `bmad-spec`: How the Hub Skill Works

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-spec/` (P19, see `../sources.md`): `SKILL.md`, `assets/spec-template.md`, `assets/stories-schema.md`. Tags: [V, P19] traced to those files, [I] inferred, [?] unclear. Not yet run in a lab except as noted. Written unattended 2026-09-19.*

`flow.md` calls `bmad-spec` the hub of Plan. This page covers what it actually does.

## What it is

The one skill that turns any intent input (idea, brief, PRD, transcript, Slack thread, mixed notes) into `SPEC.md`, a short contract downstream skills build from. It also updates and validates specs and can break one into stories. [V, P19]

## Workspace: a folder, not a file

`{output_folder}/specs/spec-{slug}/` by default. [V, P19]

```
SPEC.md         the kernel; derived, never hand-edited
<companion>.md  optional, named for the content type (glossary.md, stack.md ...)
stories.yaml    optional; only written by Story Breakdown
.memlog.md      canonical append-only log SPEC.md is derived from
```

The same slug means the same folder: a second run updates in place. [V, P19]

## The memlog: the real source of truth

- `.memlog.md` is canonical: append-only, one line per decision, constraint, capability (with stable `CAP-N`), assumption, question, or direction. Written through `_bmad/scripts/memlog.py` (`init`, `append --type ...`). [V, P19]
- `SPEC.md` and spec-authored companions are **re-derived on every run** from the log plus cited sources. A later entry supersedes an earlier one while history stays. A hand-edit to `SPEC.md` "is overwritten on the next derive." [V, P19]
- Stated reason: this lets PRD, UX, architecture, and epics run in any order and feed the same spec without merge drift. [V, P19]

## The five-field kernel

Why, Capabilities (each with `intent` and `success`, ID'd `CAP-N`), Constraints, Non-goals, Success signal. Optional Assumptions and Open Questions sections. Frontmatter carries `id`, `companions:` (files downstream must read), and `sources:` (files fully absorbed, audit only). [V, P19]

## Spec Law (eight rules)

1. Each capability has both intent and success. 2. Intents say WHAT, not HOW. 3. Constraints must actually bend design. 4. At least one explicit non-goal. 5. Success signal concrete enough to test or demo. 6. Capability IDs stable, unique, never reused or renumbered. 7. Preservation: every load-bearing source claim lands in the spec or a companion. 8. Lean prose. [V, P19]

"Load-bearing" is defined as: a claim any consumer would change a decision without. [V, P19]

## Companions

Content that does not fit one kernel-shape line (catalogs, tables, long reference) goes into a companion; the kernel cites it. Two kinds: **spec-authored** (written and owned by `bmad-spec`) and **adopted** (written by another skill, such as `DESIGN.md` from UX; referenced, never edited). **Diagrams always go in a companion**; the kernel is prose only. [V, P19]

## Behavior worth knowing

- **Express vs guided** for sparse input: express drafts best-effort and turns every gap into an open question; guided walks the five fields with the user. Headless defaults to express. [V, P19]
- **Headless vs interactive** is detected (no TTY, programmatic caller, or all inputs pre-supplied). Headless with no input returns `error_code: "insufficient_intent"`; missing slug returns `missing_slug`. [V, P19]
- **Too thin** ("an app for hikers") is refused and redirected to `bmad-prd`: "This skill distills; it does not coach." [V, P19]
- **Domain gaps are flagged, not filled:** input silent on PHI/HIPAA, PCI, or fail-safe becomes an open question. [V, P19]
- **Two-pass self-validate** after every create or update: coherence (Spec Law 1 to 6, 8) and preservation (walk the source claim by claim; drops of wrapper ceremony are logged as "Wrapper-only content"). Verdicts are appended to the memlog as `event` entries. [V, P19]
- **Conflicting live sources** are surfaced to the user, not silently chosen between. [V, P19]

## Story Breakdown (optional)

- Interactive only. Headless runs never do it, "even when the invocation text asks for it." Requires `SPEC.md` on disk. Offered at most once per run. [V, P19]
- A conversation, not a silent render: for each story, the user is asked for `spec_checkpoint`, `done_checkpoint`, and any `invoke_dev_with` note. [V, P19]
- `stories.yaml` is a list in execution order. Fields: `id` (quoted string, unique, no zero-padding), `title`, `description` (two sentences, points into SPEC.md), `spec_checkpoint`, `done_checkpoint` (both caller-only: read by the dispatcher, never by the dev skill), `invoke_dev_with` (free text appended verbatim to the dispatch prompt). **No `status` field, ever.** [V, P19]
- An id is pinned once its story spec file exists (`stories/<id>-*.md`); retired ids are never reassigned. Ids must be prefix-free (`"3"` and `"3-2"` cannot coexist). [V, P19]
- An update to a spec never rewrites `stories.yaml`; it flags stale descriptions and offers to re-run breakdown. [V, P19]

This matches how `bmad-build` step 1 looks up a story: `{spec_folder}/stories.yaml` by `id`, then `stories/{id}-*.md` (see `build-step-by-step.md`). [V, P18, P19]

## Inference

- Because the spec is derived from a log, "edit the spec" is really "append to the memlog and re-run `bmad-spec`". This changes how a team would handle a requirement change: the human owner talks to the skill, not the file. [I]
- No status in `stories.yaml` fits `flow.md`'s finding that status lives in `sprint-status.yaml`, not in the story list. [I]

## Observed in a lab (Experiment 5, `lab-log.md`)

- Interactive spec run: asked a slug, then express or guided, then wrote `SPEC.md` (3 capabilities, 4 assumptions, 7 open questions), both self-validate passes PASS. [V-lab]
- Story Breakdown ran on request, asked for each story's `spec_checkpoint`, `done_checkpoint`, and `invoke_dev_with`, wrote `stories.yaml`, and then **refused to let a scope decision live in `invoke_dev_with`**, requiring it to land in `SPEC.md` (mint a new capability, or resolve the open question in place). Re-derivation kept ids stable. [V-lab]
- Story Breakdown was not offered unprompted after the express spec. [V-lab]

- **Hand-edits and re-derivation (Experiment 5b):** a one-sentence editorial update kept all six hand-applied edits and did not flag that the memlog lacked them; only the requested line changed. The "overwritten on the next derive" rule was not borne out for a small change. The memlog and `SPEC.md` silently disagree afterward. [V-lab] **Experiment 5c** repeated it with a real decision (Carl's "normalize" answer): three surgical edits, every hand-edit kept, nine memlog entries, no mention of the drift; it did spot a stale clause in `stories.yaml` and asked before touching it. [V-lab] **Experiment 5d then removed `SPEC.md`:** the skill regenerated it wholesale from the memlog (345 s, 66 lines reworded), lost all content that existed only in the old file (the six two-tag edits), and flagged that `stories.yaml` no longer matched. So the "derived from the memlog" rule holds for a true re-derive; small updates edit in place. [V-lab] **Experiment 5e:** routing the same requirement change through `bmad-spec` found the approved change proposal in the folder, logged 15 memlog entries, produced the same spec content, and left `stories.yaml` alone (stale, flagged). [V-lab]

## Not yet checked

- `assets/headless-schemas.md` (JSON contract for headless runs). [?]
- What a real memlog and rendered SPEC.md look like in practice; Experiment 2's lab spec may show this. [?]
- Whether `spec_checkpoint` and `done_checkpoint` are honored by `bmad-build-auto` or only by `bmad-loop`. [?]
