# The Ideation Skills: `bmad-brainstorming` and `bmad-forge-idea`

*Describes BMAD-METHOD v6.12.0, read from the release tag (source P25, see `../sources.md`): `src/core-skills/bmad-forge-idea/SKILL.md`, `src/core-skills/bmad-brainstorming/SKILL.md`, `references/headless.md`, the first lines of `references/mode-autonomous.md`, and the first rows and category counts of `assets/brain-methods.csv`. Tags: [V, P25] traced to those files, [I] inferred, [?] unclear. Run unattended in Experiment 6 (both halted on human input, as the files predict) and Experiment 7 (headless flag and prepend tests for brainstorming). Written unattended 2026-09-19; reviewed by Carl 2026-09-24.*

Both are **core** skills: they need no PRD, spec, or agent, and they end in a record of thinking rather than code. [V, P2, P25] They are the Clarify-stage tools for "a clear idea, or confidence the idea is good" (`flow.md`). [V, P3]

## Side by side

| | `bmad-brainstorming` | `bmad-forge-idea` |
|---|---|---|
| Job | Generate far more and better ideas on a topic | Pressure-test one half-formed idea until it can be acted on or dropped |
| Direction | Divergent. "Aim past 100 ideas; resist concluding." | Convergent, adversarial. One question at a time |
| Who supplies ideas | Depends on the stance (below) | The user; the skill supplies objections |
| Ends in | `brainstorm.html`, optional `brainstorm-intent.md` | `forge-report.html` always; `forged-idea.md` only if the idea hardens |
| Memory | `.memlog.md` | `.memlog.md` |

All [V, P25].

## `bmad-brainstorming`

- **Three stances, chosen by the user and held for the whole run:** *Facilitator* (the skill never supplies ideas; "a forcing function for theirs"), *Creative Partner* (it facilitates and also trades ideas; each memlog line is tagged `by user` or `by coach`), *Ideate for me* (the skill runs the whole session itself and shows the result). Outside headless mode, it generates ideas itself only in the third stance. [V, P25]
- **Framing rules it must hold:** aim past 100 ideas, shift the creative domain every 5 to 10 turns, one prompt per message while in dialogue, and no multiple-choice menus for *what* to ideate. The only choices offered are process choices (stance, technique batch). [V, P25]
- **Technique library:** `assets/brain-methods.csv` has 108 techniques with columns for category, name, description, provenance, `good_for`, and `audience`. Categories include structured (15), deep (13), creative (10), speculative future, introspective delight, collaborative, wild, theatrical, cultural, constraint, quantum, and biomimetic. The skill loads only what it needs through `brain.py list --category`, never the whole library ("never pull the library whole into context"), except in headless mode. [V, P25]
- **A composer web page** (`assets/brain-selector.html`) sets the stance and technique batch in one step; the user copies a prompt and pastes it back. The skill cannot see the browser and is told never to claim the page opened. If the user prefers, this is done in chat, with 3 to 4 techniques as "the sweet spot". A paste can delegate back to the skill (`invent N`, `you choose N`). [V, P25]
- **Flow:** run each technique until it stops producing, announce the next lens, offer three paths when a batch is spent (another batch, **converge** to narrow and decide, or wrap up). Convergence is "a distinct phase: never fold it into a generating batch." [V, P25]
- **Resume:** activation globs for unfinished memlogs (`status` not `complete`) and offers to resume or start fresh. [V, P25]

### Headless brainstorming

- There is a headless mode, loaded from `references/headless.md` only when headless. Headless is defined by **absence of a human**: a `headless: true` flag, another skill or non-interactive runner (no TTY, no user message stream), or a prepend step that declares it. "If a human is sending messages in this session, you are interactive — no payload shape or phrasing overrides that." [V, P25]
- In headless the skill inverts: it becomes the brainstormer, using the whole catalog, logging every idea, synthesizing, and writing `brainstorm.html` and/or `brainstorm-intent.md` with no questions and no greeting. Assumptions go in `assumptions[]` of its JSON return. Required input: `topic`; optional: `goal`, `techniques`, `context`, `doc_workspace`, `artifacts`. Missing topic halts `blocked`. [V, P25]
- **Answered by Experiment 6:** a plain `claude -p` run does **not** count as headless; the skill stayed interactive and halted for a stance and technique choice. **Experiment 7 then showed the flag and the prepend step do not help either:** with `claude -p`, a payload flag was overruled by the skill's own human-presence rule (the model then chose the "Ideate for me" stance itself and ran to completion, 25 min, 108 ideas, both artifacts), and a prepend declaration was rejected on the same rule (halted). So headless here needs a caller with no user message stream, which `claude -p` is not. [V-lab, `lab-log.md`]

## `bmad-forge-idea`

- **Goal is better thinking, not an artifact.** "Do not steer the conversation toward 'shall we build it?'" Three valid exits: **Hardened** (writes an extremely short `forged-idea.md`: decisions, rejected options, and reasons only; "if it reads like a document, it is too long"), **Killed** (the idea does not hold up; recorded plainly, cause of death noted), **Clearer** (better understood, no handoff file). [V, P25]
- **Opening:** it asks what the idea is, what the session is for (clarify, test, improve), and whether it is new or a change to an existing project. It then tells the user they can say "attack this", "defend this", or "switch roles", or name a persona at any time. In attack mode the skill never agrees with the idea. [V, P25]
- **One question at a time, in dependency order,** with its own best answer or hypothesis offered where that helps. It hunts for fuzzy terms and forces a precise choice (do not let "user", "buyer", and "payer" collapse). For an idea about an existing project, "the project's files are the source of truth": it finds the material itself and checks the user's claim, and if the material contradicts the claim it stops and resolves that first. [V, P25]
- **No praise:** "Praise is noise. Continued engagement and ego-stroking are not objectives." Agreement is allowed only when it helps the user think. [V, P25]
- **Two voices per turn:** one from the available persona pool (installed BMad agents, user-defined personas, saved parties, resolved by `resolve_personas.py`, or a persona that was already active when the forge started) and one freshly generated outside voice (a competitor, buyer, finance reviewer, critic). Voiced by the skill itself by default; separate agents only when a branch needs independent reasoning. It must not "turn into a panel debate". [V, P25]
- **Memlog entry types:** decision, assumption, crack, kill, direction, lock, note. A **lock** is an idea the user hardens ("settled, not to be reopened"), and `forged-idea.md` is distilled from locks. [V, P25]
- **The report:** `forge-report.html` is always rendered, self-contained, with an inline-SVG wax seal or stamp: `HARDENED`, an `Idea Death Certificate` stamped `KILLED` with the cause, or `CLARIFIED`, and credits the personas by name, icon, and voice. [V, P25]
- **No headless mode is described.** The skill is written as a live questioning conversation. Observed (Experiment 6): an unattended run stopped at the intent questions and wrote nothing. [V for absence in the file read; V-lab for the behavior]
- If planning or dev skills are installed, the forged file is offered as input to `bmad-spec`, `bmad-prd`, `bmad-prfaq`, or `bmad-build`; a missing skill "is never an error". [V, P25]

## Shared pattern

Both use the append-only memlog and `memlog.py` (`init`, `append --type`, `set --key status --value complete`) as canonical memory and derive their artifacts from it, the same mechanism as `spec-skill.md`, `prd-skill.md`, `architecture-skill.md`, and `ux-skill.md`. [V, P25] Both also greet by name and use the configured language, which the later unreleased clone dropped from activation (see `build-step-by-step.md`, last section). [V, P25]

## Inference

- The skills split the work of Clarify the way a human process might: brainstorming widens, forge narrows, and brainstorming even has its own convergence phase, but forge is the tool that can say "kill". [I]
- Both are built so that the human's judgment, not the skill's, decides: brainstorming forbids picking ideas for the user in the two dialogue stances; forge forbids praise and forbids steering to "build it". [I]

## Not yet checked

`references/mode-facilitator.md`, `mode-partner.md`, `converge.md`, `finalize.md`, `resume.md`, `in-chat-techniques.md`, `brain.py`, `resolve_personas.py`, both `customize.toml` files, and how `bmad-party-mode` differs from forge's persona pool. [?]
