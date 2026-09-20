# `bmad-architecture`: The Architecture Spine

*Describes BMAD-METHOD v6.12.0. Source: `skills/bmad-architecture/` (P21, see `../sources.md`): `SKILL.md`, first ~70 lines of `assets/spine-template.md`, first ~25 lines of `references/reviewer-gate.md` and of `scripts/lint_spine.py`. Tags: [V, P21] traced to those files, [I] inferred, [?] unclear. Not run in a lab. Written unattended 2026-09-19.*

## What it produces

An **architecture spine** (`ARCHITECTURE-SPINE.md`): a "consistency contract" fixing only the **invariants** that keep independently built units from diverging: design paradigm, boundary and dependency rules, how state is mutated, who owns shared data. Stack, source tree, and full data shape are **seed**: true at cold start, owned by the code once it exists. [V, P21] It leads with a named paradigm (hexagonal, layered, actor...) because "a known one loads a whole model for free." [V, P21]

## The inclusion test

> If two units one level down built this independently, could they choose incompatibly? Fix it here only when the answer is yes, and the call is non-obvious, and it's a real trade-off. Otherwise name it under Deferred.

[V, P21] (Same test as `flow.md`'s architecture-spine test, [V, P6].) Decisions are recorded, rationale is not: rationale lives in the memlog. Shape goes in diagrams, not prose. Named technologies must be verified current on the web before being bound. [V, P21]

## Purposes and altitudes

- **Purpose** (frontmatter): `build-substrate` (default, terse, for agents), `discussion` (keeps open questions up front, for aligning people), `report`, or `deck`. [V, P21]
- **Altitude**: `initiative` (keeps features coherent), `feature` (keeps epics), `epic` (keeps stories). An epic spine can inherit a parent spine: parent `AD`s are binding and read-only, listed under Inherited Invariants with original IDs; a new `AD` that contradicts one is "a conflict to surface, not a local override." [V, P21]
- Before drafting, the skill must ask whether the spine is the only deliverable, and draw out purpose and audience instead of a document type, to prevent "an architecture doc" from ballooning. [V, P21]

## How it works

- **Coaching path is the default.** The skill's own words: the elicitation "cuts against the instinct to just produce an architecture, so hold the line." Fast path drafts everything with `[ASSUMPTION]` tags. The load-bearing calls (paradigm, stack or starter, major boundaries) are "shown, not silently made": alternatives laid out, then the user chooses. [V, P21]
- **Greenfield:** recommend a well-known current starter, checked on the web. **Brownfield:** read the real code first and ratify existing conventions rather than invent new ones. [V, P21]
- **Memlog again.** Working memory is the append-only `.memlog.md` (types: decision, constraint, version, assumption, question, direction, event). The spine is distilled from it at the end, not written as you go. Each surviving decision becomes an `AD-n` with **Binds / Prevents / Rule**, tagged `[ADOPTED]` if already settled. Same pattern as `spec-skill.md` and `prd-skill.md`. [V, P21]
- **Template sections:** Design Paradigm, Inherited Invariants (epic only), Invariants and Rules (the `AD` blocks, plus a dependency-direction mermaid diagram that "IS a rule"), Consistency Conventions (naming, data formats, state and cross-cutting), Stack (name plus pinned version), Structural Seed (diagrams, tree), Capability to Architecture Map. Empty sections are cut. [V, P21]
- **Altitude sweep:** every structural dimension must be decided, deferred, or an open question. A whole dimension left silent, such as deployment, infra, or operations, "is the failure, not a clean spine." [V, P21]

## Finalize and reviewer gate

- Finalize: distill, reconcile inputs (subagent per input catches "quiet requirements" the `AD` structure dropped), reviewer gate, triage open items, optional human-facing renderings (interactive HTML and SVG deck, C4 set, team-split view), handoffs, close with `status: final`. [V, P21]
- Next step guidance: **lead with `bmad-spec`** to adopt the spine as a spec companion (keeping `AD` IDs stable), then `bmad-create-epics-and-stories`, or `bmad-build` at epic altitude. [V, P21]
- **Gate** runs a deterministic linter first, `scripts/lint_spine.py`, which checks placeholders, duplicate or non-monotonic `AD` IDs, `AD` blocks missing Binds/Prevents/Rule, and Stack rows without versions ("LLMs miscount IDs and miss literal placeholders; a grep does not"). It always exits 0; findings go out as JSON. Then a rubric walker plus configured reviewers run as parallel subagents. [V, P21]
- Good-spine checklist highlights: every `AD` Rule is enforceable and actually prevents its stated divergence; nothing under Deferred could let two units diverge; it ratifies rather than contradicts a brownfield codebase. [V, P21]
- Under Validate the gate delivers an HTML report and changes nothing; at Finalize the skill applies clear fixes itself. [V, P21]

## Update rule

Resume from the memlog, not the rendered spine. Keep `AD` IDs stable: amend a Rule in place, add the next `AD-n` for a new decision, never renumber or reuse retired IDs. [V, P21]

## Inference

- The spine's `AD` IDs play the same role for architecture that `CAP-N` plays for the spec and FR/UJ/SM IDs play for the PRD: stable handles for downstream citation. [I]
- The linter is the first piece of deterministic tooling seen in the planning skills; the others read so far rely on prompts and subagents. [I, from the skills read so far]

## Not yet checked

- The rest of `spine-template.md`, the remaining reviewer-gate text, the linter's checks beyond its header, `references/headless.md`, and `customize.toml`'s default `finalize_reviewers`. [?]
- `bmad-ux` (the parallel skill for UX docs). [?]
