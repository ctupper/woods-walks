# BMAD in One Page

*For someone who has never seen BMAD. Describes BMAD-METHOD v6.12.0. Tags: [V] traced to the project's own docs or skill files (detail and source IDs on the linked pages), [V-lab] seen in a lab run, [I] inferred. Draft written unattended 2026-09-19; **not yet cold-read by a human**, which the project's success criteria require.*

## What it is

BMAD is a set of named commands ("skills") you add to an AI coding tool such as Claude Code. Some help you think (explore an idea, research a decision, write down what you settled on). Others help you build (turn a described change into reviewed, tested code). You can use either group alone. [V, `agents.md`]

Its central bet: the AI writes better code when the human intent is written down first, briefly and precisely, and when the AI's work is checked by reviewers who don't share the author's assumptions. [I, from `flow.md`, `build-step-by-step.md`]

## The loop

The released docs' delivery diagram shows one loop of four steps: **Clarify, Plan, Build and verify, Learn and adjust.** Bigger work enters earlier (the sizing table in `flow.md` supports this), rather than using a different method. [V for the diagram labels, I for the rest; see `flow.md`]

| Your starting point | Enter at |
|---|---|
| A vague notion | Clarify |
| A big, clear idea | Plan |
| A small change | Build and verify |

[V, `flow.md`]

## The shortest path

For a change that fits in one session, you can skip planning documents entirely: write down the intent, let `bmad-spec` turn it into a one-page contract, and let `bmad-build` implement and review it. In a lab run, a small command-line tool went from idea to passing tests this way. [V, `flow.md`; V-lab, `lab-log.md`]

## What the parts do

- **Five agents** (named personas that route you to skills): Mary the analyst (research, briefs), John the product manager (requirements, epics), Winston the architect, Sally the UX designer, Amelia the developer (build, review). An agent is mostly a personality plus a menu; the real work lives in the skills. [V, `agents.md`]
- **`bmad-spec`** condenses any input into `SPEC.md`: why, capabilities each with a testable success condition, constraints, non-goals, success signal. It keeps a running log and re-derives the spec from it, so the spec is never hand-edited. [V, `spec-skill.md`]
- **`bmad-prd`** and **`bmad-architecture`** are the heavier planning tools, for when several people must agree. The PRD is a requirements document; the architecture "spine" records only the decisions that would make separately built parts clash. [V, `prd-skill.md`, `architecture-skill.md`]
- **`bmad-build`** takes a described change, plans it, (for bigger changes) has a subagent implement it, has independent reviewers check it (one reviewer for a small change, three for a larger one), and fixes what they find. Human-owned intent is locked in the spec once approved. [V, `build-step-by-step.md`]
- **Retrospective and course-correction skills** close an epic or handle a change too big for one story. [V, `flow.md`]

## What it does not do

- It does not sync with Jira or Linear. The tracker stays yours; BMAD only updates its own status file. [V, `flow.md`]
- It does not decide what you want. The spec skill "does not help you figure out what you want"; the thinking tools do. [V, `flow.md`]
- It halts and asks when intent is unclear rather than guessing. In a lab run it stopped with three open questions even though the input was labeled complete. [V-lab, `lab-log.md`]

## Practical facts from the lab

- Install works on Windows with Node, git, and `uv` (a Python tool the installer requires). [V-lab, `lab-log.md`]
- A larger build with three independent reviewers took about 32 minutes; a small change in an existing codebase, with one reviewer, took about 6.5. [V-lab, `lab-log.md`]
- In a code-review test, both review modes caught all six planted flaws in a small flawed commit, but the review workflow stopped three times for human decisions until they were answered in advance. [V-lab, `lab-log.md`]
- Your own instructions still apply: a personal "confirm before committing" rule overrode BMAD's default commit step. [V-lab, `lab-log.md`]

## Where to go next

`flow.md` (the loop and its artifacts), `agents.md` (agents and skills), `build-step-by-step.md`, `spec-skill.md`, `prd-skill.md`, `architecture-skill.md`, `ux-skill.md`, `glossary.md`, `lab-log.md` (what actually happened).

## Known gaps

Not yet covered: customization for teams, the retrospective and course-correction skills in a lab run, and the ideation skills (brainstorming, forge idea). Lab experiments run so far: install, one small idea through the loop, code review on a flawed commit, and an existing-codebase change. `bmad-ux` is read but not run. [I]
