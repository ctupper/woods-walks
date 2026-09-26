# BMAD in One Page

*For someone who has never seen BMAD. Describes BMAD-METHOD v6.12.0. Tags: [V] traced to the project's own docs or skill files (detail and source IDs on the linked pages), [V-lab] seen in a lab run, [I] inferred. Drafted unattended 2026-09-19 and read by the project owner on 2026-09-20, who found it good. The owner had followed the research closely, so a read by someone who has never seen BMAD would still be stronger evidence.*

!!! tip "TL;DR"
    BMAD adds named commands ("skills") to an AI coding tool. A few turn a written-down intent into a one-page spec, then implement and independently review the change against it. Small work can skip straight to building; bigger work starts with planning skills instead. It halts and asks rather than guessing when your intent is unclear, and it doesn't sync with your tracker or decide what you want. The rest of this page is the detail, with a citation for every claim.

## What it is

BMAD is a set of named commands ("skills") you add to an AI coding tool such as Claude Code. Some help you think (explore an idea, research a decision, write down what you settled on). Others help you build (turn a described change into reviewed, tested code). You can use either group alone. [V, [agents.md](agents.md)]

Its central bet: the AI writes better code when the human intent is written down first, briefly and precisely, and when the AI's work is checked by reviewers who don't share the author's assumptions. [I, from [flow.md](flow.md), [build-step-by-step.md](build-step-by-step.md)]

## The loop

The released docs' delivery diagram shows one loop of four steps: **Clarify, Plan, Build and verify, Learn and adjust.** Bigger work enters earlier (the sizing table in [flow.md](flow.md) supports this), rather than using a different method. [V for the diagram labels, I for the rest; see [flow.md](flow.md)]

| Your starting point | Enter at |
|---|---|
| A vague notion | Clarify |
| A big, clear idea | Plan |
| A small change | Build and verify |

## The shortest path

For a change that fits in one session, you can skip planning documents entirely: write down the intent, let `bmad-spec` turn it into a one-page contract, and let `bmad-build` implement and review it. In a lab run, a small command-line tool went from idea to passing tests this way. [V, [flow.md](flow.md); V-lab, [lab-log.md](lab-log.md)]

## What the parts do

- **Five agents** (named personas that route you to skills): Mary the analyst (research, briefs), John the product manager (requirements, epics), Winston the architect, Sally the UX designer, Amelia the developer (build, review). An agent is mostly a personality plus a menu; the real work lives in the skills. [V, [agents.md](agents.md)]
- **`bmad-spec`** condenses any input into `SPEC.md`: why, capabilities each with a testable success condition, constraints, non-goals, success signal. It keeps a running log and re-derives the spec from it, so the spec is never hand-edited. [V, [spec-skill.md](spec-skill.md)]
- **`bmad-prd`** and **`bmad-architecture`** are the heavier planning tools, for when several people must agree. The PRD is a requirements document; the architecture "spine" records only the decisions that would make separately built parts clash. [V, [prd-skill.md](prd-skill.md), [architecture-skill.md](architecture-skill.md)]
- **`bmad-build`** takes a described change, plans it, (for bigger changes) has a subagent implement it, has independent reviewers check it (one reviewer for a small change, three for a larger one), and fixes what they find. Human-owned intent is locked in the spec once approved. [V, [build-step-by-step.md](build-step-by-step.md)]
- **Retrospective and course-correction skills** close an epic or handle a change too big for one story. [V, [flow.md](flow.md)]

## What it does not do

- It does not sync with Jira or Linear. The tracker stays yours; BMAD only updates its own status file. [V, [flow.md](flow.md)]
- It does not decide what you want. The spec skill "does not help you figure out what you want"; the thinking tools do. [V, [flow.md](flow.md)]
- It halts and asks when intent is unclear rather than guessing. In a lab run it stopped with three open questions even though the input was labeled complete. [V-lab, [lab-log.md](lab-log.md)]

## Practical facts from the lab

Six things observed running BMAD for real, each collapsed by default — expand the ones you care about.

??? note "Install requirements"
    Install works on Windows with Node, git, and `uv` (a Python tool the installer requires). [V-lab, [lab-log.md](lab-log.md)]

??? note "How long a build actually takes"
    A larger build with three independent reviewers took about 32 minutes; a small change in an existing codebase, with one reviewer, took about 6.5. [V-lab, [lab-log.md](lab-log.md)]

??? note "Review catches real flaws, but stops for human decisions"
    In a code-review test, both review modes caught all six planted flaws in a small flawed commit, but the review workflow stopped three times for human decisions until they were answered in advance. [V-lab, [lab-log.md](lab-log.md)]

??? note "A requirement change, routed the right way"
    A requirement change went through the whole loop (spec, stories, change proposal, spec update, stories re-run) with a person answering each question. Routing the change through `bmad-spec`, not by hand-editing `SPEC.md`, kept it in the spec's log; hand-edits were lost when the spec was regenerated. [V-lab, [lab-log.md](lab-log.md)]

??? note "A four-story epic, built end to end"
    That epic was then built end to end: four stories, each gated by real checkpoints (dirty tree, approval, token count), each reviewed independently, 61 tests passing at the end. Review caught one real bug (an id gets reissued after its note is deleted) and correctly left it deferred rather than smuggling a fix into an unrelated story. A different finding was raised and rejected three separate times across three stories — and BMAD flagged that pattern to the human itself, unprompted, as the likely place its own reasoning was wrong. [V-lab, [lab-log.md](lab-log.md)]

??? note "Your own rules still apply"
    A personal "confirm before committing" rule overrode BMAD's default commit step, on every single story, not just once. [V-lab, [lab-log.md](lab-log.md)]

## Where to go next

- [Flow](flow.md): the loop, the flow diagram, and the artifact each step leaves
- [Agents](agents.md): the five agents, their inputs and outputs, and the skills
- [Building](build-step-by-step.md): how `bmad-build` runs, step by step
- Skills: [spec](spec-skill.md), [PRD](prd-skill.md), [architecture](architecture-skill.md), [UX](ux-skill.md), [ideation](ideation-skills.md)
- [Glossary](glossary.md)
- [Lab log](lab-log.md): what actually happened in each experiment
- [Systemic findings](systemic-findings.md): patterns that only show up across several experiments at once

## Known gaps

Not yet covered or run: customization for teams; the PRD, architecture, UX and sprint-planning skills in a lab run (all four are read, none run); the walkthrough skill (offered at the end of every build in the lab, never taken); the ideation skills beyond their opening steps (both stopped for human input when run unattended, so the ideas they produce were not judged). Lab experiments run so far: install, one small idea through the loop, code review on a flawed commit, a change in an existing codebase, unattended runs of the ideation skills, a spec-backed epic taken through a requirement change and built out story by story, and a retrospective on that finished epic that found a defect no single story's review could have (see [lab-log.md](lab-log.md), Experiment 5i). [I]
