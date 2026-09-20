# BMAD — Lab Log

*Observations from running BMAD in throwaway repos under `C:\Users\ctupp\labs\`. Tag [V-lab] = seen happening. Each entry says what the docs predicted and what actually happened.*

## Experiment 1 — Install and skill load (2026-09-19)

**Setup:** fresh folder `labs\lab1-toy`, `git init`, then `npx bmad-method install --yes --modules bmm --tools claude-code --directory <path> --user-name Carl`.

| Expected (docs) | Observed |
|---|---|
| Installer writes one dir per skill into `.claude/skills/` for Claude Code [P2] | **Matches.** 29 skill directories written [V-lab] |
| Version 6.12.0 | Core and BMad Method both report v6.12.0 [V-lab] |
| Core module ships eight skills; Method adds agents and workflow skills [P2] | Both modules installed ("2 module(s)"). `bmad-help` is among the 29 and is not in the repo's `skills/` list of 30, so the install set differs from the repo directory listing [V-lab]. Which repo skills are excluded (e.g. `bmad-preview-ticketing`, a prerelease skill [P-v7]) was not checked [?] |
| `uv` needed for scripts [not in P1-P9 reading] | Installer states `uv` is **required**: "Without it, bmad-build and bmad-build-auto halt on activation." It detected uv 0.9.18 here [V-lab] |
| Non-interactive install possible | Yes: `--yes` with `--tools` (required for fresh non-interactive installs) and `--modules` [V-lab] |

**Files created in the target repo:** `.claude/skills/` (29 skills), `_bmad/` (config.toml, config.user.toml, `bmm/` and `core/` config + module-help, `custom/` overrides folder, `scripts/` with Python helpers, `_config/` manifests) and `_bmad-output/` (empty output folder). [V-lab]

**Environment answer:** a full BMAD install works in this environment, outside Google Drive. Node 22, npm 10.9.2, git 2.55, uv 0.9.18 all present. **The open unknown in the spec is closed: install works.**

**Skill run test:** in `lab1-toy`, headless `claude -p "/bmad-help I have a tiny idea: a command-line tool that counts word frequencies in a text file. Where do I start? Do not create any files."` [V-lab]:
- The skill loaded and ran from `.claude/skills/`. The repo stayed clean apart from the install (`git status` showed only `.claude/` and `_bmad/`).
- It **recommended skipping the full pipeline**: start at `bmad-spec`, then `bmad-build`, with `bmad-forge-idea` optional. It reasoned that the full path (Brief → PRD → Architecture → Epics → Sprint Planning → Build) is for multi-epic projects and that this idea is "one story."
- It refused to write a file because the prompt said not to, and asked before running `bmad-spec` ("it writes `SPEC.md`, so say the word first").
- This matches the docs' sizing rule that the smallest path that safely fits is right. [P3, P8] It is one observation, not a general claim about how `bmad-help` routes.

**Observed while reading the installed agent files:** the Developer agent's `customize.toml` defines the persona (see `agents.md`, "Persona anatomy"). The file says "DO NOT EDIT -- overwritten on every update"; customization goes in `_bmad/custom/`. [V-lab]

**Minor:** some characters in the installed TOML (the agent's icon, an em dash) displayed as mojibake in Windows PowerShell output. This looks like a console encoding issue, not corrupted files, but the bytes were not checked [?].

## Experiment 2 — one toy idea through the loop (2026-09-19, done)

**Toy:** `wordfreq`, a Node CLI printing the N most frequent words in a UTF-8 file. Run headless with `claude -p ... --permission-mode acceptEdits` from `labs\lab1-toy`. Each `-p` call is a fresh session, so state passes between steps only through files.

**Step 1: `bmad-spec` with a complete intent (224 s).** [V-lab]
- Wrote `_bmad-output/specs/spec-wordfreq/SPEC.md` (Why, 5 capabilities each with intent + success, Constraints, Non-goals, Success signal) plus `.memlog.md`. No companions, no `stories.yaml`. Matches the docs' five-field contract [P5].
- The `.memlog.md` is a running log of decisions, assumptions, questions, and events, including two self-validate passes (coherence, preservation), both PASS. This file type is not described in the docs pages I read for the spec skill, only listed as an output of `bmad-prd` and `bmad-ux` [P3]. [V-lab]
- I said the intent was complete and to ask nothing. It still recorded **2 assumptions and 3 open questions** (tokenization boundary, `--top N` out of range, wrong arity) instead of inventing answers, and it did not start the build. Docs predicted "every gap becomes an open question" for sparse input [P5]; here it applied to a rich input too.

**Step 2: `bmad-build` on the spec, no answers given (208 s).** [V-lab]
- It **halted with the three open questions** and wrote nothing but a draft implementation spec (`_bmad-output/implementation-artifacts/spec-wordfreq.md`, `status: draft`, `route: dispatch`). No code, no commit.
- For each question it offered lettered options and a recommendation with the reason. It also said the spec could be reviewed or pressure-tested first with `bmad-advanced-elicitation` or `bmad-party-mode`, ideally in a fresh session.
- This matches the docs: intent gaps become open questions answered before approval [P8]. The drafted spec has a frozen human-owned Intent block, an I/O and edge-case matrix, a code map, tasks with acceptance criteria, and empty Design Notes / Review Triage Log / Verification sections that fill in later.
- The docs said light-path vs full-plan routing depends on intent gaps, irreversible actions, and footprint [P8]. Here open questions forced the full-plan path. The spec field `route: dispatch` was not explained in the docs pages I read [?]. **Later explained (diff, 2026-09-19):** the installed `bmad-build` step 2 sets `route: 'dispatch'` when the change has intent gaps, irreversibles, or a large footprint, and `oneshot` when all three are clean. The clone's `oneshot`/`full` naming is a later change. [V-lab files]

**Step 3: resume with answers.** I answered the questions myself, choosing the recommendations: Unicode letters with apostrophes stripped and no digits; `--top` out of range handled per option (a); wrong arity uses the same exit-1 path. **These were my choices, not Carl's**, made to keep the experiment moving; in real use they are the "most expensive kind of mistake" decisions the docs say a human should own [P8].
- Observed by 07:56: `wordfreq.js`, `test/wordfreq.test.js`, `package.json` created and staged; spec status `in-review`, `review_loop_iteration: 0`, `baseline_commit` recorded. The build made a judgment call not in my answers: tokenizer `[\p{L}\p{M}]+` so decomposed accents stay in one word. Review triage log still empty; last file write 07:49, several minutes of quiet during the review stage.
**Step 3 result (checked 08:05, about 28 minutes after the resume was launched).** [V-lab]
- Spec status `done`. `node --test` passes 18 of 18 in the lab repo (13 when I peeked mid-review), with no `node_modules`.
- **Review ran three lenses**, named in the triage log as blind-hunter, edge-case-hunter, and verification-gap. It logged **17 findings** in a table (finding, verdict, evidence, route). Every finding was verified at its cited location before grading: it reproduced the claim with a real input.
- **Routing:** 7 patch, 10 reject (5 of those graded `false`). Rejections carried a reason each, following the docs' "dismiss with a recorded reason, never silently" [P14]. The reasons cite numbered rules in the skill (frozen intent text can't be edited; a fix that adds public surface against the frozen contract is rejected) rather than taste. Examples: `--help` exits 1 (the frozen rule sends every unknown flag to the failure path, so rejected); an accent-mark-only run counted as a word (patched); the tiebreak used UTF-16 code-unit order where the frozen rule said codepoint order, shown with a reproduced input (graded medium, patched).
- **Most instructive finding (#17, medium):** every above-cap fixture had uniform counts, so a mutant that caps *before* ranking passed all 13 tests, and on a non-uniform file would drop the two most frequent words. The suite could not fail on the tool's central promise. It was patched by adding tests, which explains the jump from 13 to 18. This is the docs' review-triage claim in action, and a small live case of "a green suite isn't correctness."
- **Commit state (resolved when the run exited, 1929 s = 32 min):** the build finished with the tree **uncommitted**, and told me why: "your rule is confirm first." It had picked up Carl's global instruction to confirm before committing and let that override the docs' "commits locally" step [P8]. **So a personal CLAUDE.md rule beat BMAD's default workflow step.** The run ended by offering to commit, or to run `bmad-walkthrough` for a guided review. [V-lab] (The earlier "staged" state was the run working; the staged files had been un-staged by the end.)
- **The run surfaced two decisions for the human instead of hiding them:** (1) it changed the tokenizer to `\p{L}[\p{L}\p{M}]*` because the frozen `[\p{L}\p{M}]+` matched an orphan combining mark, but left the frozen bullet untouched and said reverting is a one-token change. (2) Whether `Hawaiʻi` should fold to `Hawaii` (U+02BB not in the frozen apostrophe list) was left to the human. [V-lab]
- **Side effect:** the headless run wrote something to *its own* Claude memory (a `package.json` pin note it expects to hit every Node project under `labs\`). Memory is per working directory, so this landed in the lab project's memory, not PAI's. It also means headless BMAD runs are not stateless with respect to memory. [V-lab; memory contents not inspected] Worth checking before trusting a lab as clean [?].
- **Time:** spec 224 s, first build attempt 208 s (halted on questions), resumed build 1929 s including three-lens review and patching. The docs' explanation for slow runs (exhaustive review on purpose) matches [P8, P14].

**What the docs predicted vs. what happened:**

| Prediction | Result |
|---|---|
| Spec from a complete intent is short (5 fields) [P5] | Matched: 5 capabilities |
| Build halts on intent gaps as open questions before a plan [P8] | Matched, even though the intent was called complete |
| Review runs independent reviewers, triage verifies and dismisses with reasons [P14] | Matched, with 17 findings and a reasoned verdict on each |
| Non-trivial findings after repeated review mean an upstream problem [P14] | Not tested; one review round only |
| Build commits locally [P8] | Unconfirmed at 08:05 |
| Light path for clean designs [P8] | Not exercised; the open questions forced the full path |

**What a human still had to do:** answer the three intent questions. Here I answered them, which the run's design leaves to a human.


## Experiment 3 — `bmad-code-review` on a flawed diff (2026-09-19, done; first attempt halted, rerun ran)

**Setup:** `labs\lab3-review` (throwaway, outside Drive): a Node cart module, baseline commit `4580d6d` (3 tests passing), then a deliberately flawed commit `92c1ace` "Add coupon support". BMAD v6.12.0 installed with the same flags as Experiment 1 (29 skills; install files excluded via `.git/info/exclude` so the diff stayed clean). Copied to `lab3-quick` and `lab3-thorough`; both run headless at once with `claude -p ... --permission-mode acceptEdits`, prompt naming the mode, the commit, and a one-paragraph intent statement, and telling it to stop on any human question.

**Planted flaws (written down before the run):** (A) `pct` unvalidated in `applyDiscount`; (B) unknown coupon gives `undefined` pct, so the total is NaN, contradicting "unchanged price"; (C) `qty` guard removed from `addItem` (an existing test now fails); (D) `applyDiscount` mutates the caller's cart, contradicting "never mutated"; (E) `applyDiscount` untested; (F) the new "coupon works" test asserts nothing; (G) case-sensitive coupon lookup (minor).

**Result: neither run reviewed anything.** Both halted at step 1 of the workflow (105 s quick, 251 s thorough) on the same question. [V-lab]

- **Question, verbatim from `step-01-gather-context.md` item 5:** "ask the user to choose: 1. Provide a spec or story file path for context; or 2. Continue without a spec."
- The workflow resolved the target correctly (commit range `HEAD~1..HEAD`, 2 files, +22/-4, 53-line diff), staged the diff and a claims file (commit message plus my intent paragraph), then stopped. No review layer launched. Nothing was written to the repo.
- **Why it asked:** the step says to set `review_mode` = `no-spec` only when the request explicitly says so ("no spec", "without a spec", "no-spec"), and forbids inferring it from a missing path. My intent paragraph is text, not a spec file path, so neither branch applied. [V-lab; V, P18-style step file `bmad-code-review/step-01-gather-context.md`]
- **Mistake in my prompt, not a BMAD defect:** I did not say "no spec". A rerun needs either that phrase or a real spec file path. Which one is a design choice about what the experiment tests (a spec adds the acceptance-auditing layer), so I left it for Carl.
- The step ends with a second halt right behind this one: a CHECKPOINT that shows diff stats and `review_mode` and waits for confirmation. [V, step-01 file] So even a correct prompt needs a confirmation in headless mode; a rerun prompt should pre-authorize it, or the run will halt again.
- **The thorough run said "thorough isn't an option in this skill".** I first marked that wrong because the cloned repo's `bmad-code-review` has a `review = "thorough"` setting and quick/thorough lens sets. **Corrected after the rerun: the run was right about the installed skill.** The npm-installed 6.12.0 in the lab has no quick/thorough selection (see the rerun section below); the clone at `f033e70` does. [V-lab, installed files]
- **Side observation (from the thorough run):** `npm test` on HEAD fails (`addItem rejects bad qty`), i.e. planted flaw C is visible to a plain test run, before any review. It mentioned this as a "pre-review fact, not a finding".
- **Docs vs observed:** docs say "quality depends on being given intent (a spec) as well as the diff" [P14]. Observed: the skill enforces this with a hard question rather than a soft preference. [V-lab] Two reads of that, untested: a strict gate that prevents context-free reviews, or friction for automated use. [?]

**Resolved:** Carl chose "no spec" and a rerun followed (below). Original question kept for the record: how to rerun. (1) provide a spec file path (I'd have to write one for the toy, which tests the full four-layer path including the acceptance layer), or (2) say "no spec" (three layers). Either way the prompt should also pre-approve the step-1 checkpoint. Quick vs thorough comparison against A to G has not happened; scores are blank.


### Rerun with "no spec" (Carl's choice, 2026-09-19)

Same labs. The prompt now said "no spec (no-spec mode)", supplied the intent as the change narrative, and pre-approved the step-1 checkpoint. Both ran to the presented findings. **Times: quick 382 s, thorough 527 s.** [V-lab]

**Both runs ran the same three layers: Blind Hunter, Edge Case Hunter, Verification Gap.** The Acceptance Auditor was skipped because there was no spec. [V-lab] So "quick" and "thorough" did not select different reviewer sets. Cause: the installed skill's `customize.toml` has `[[workflow.review_layers]]` (four layers, the Acceptance Auditor gated on `review_mode = full`) and no quick/thorough selection. [V-lab, installed file] The quick/thorough behavior in the repo docs [P14] and in the cloned repo's `bmad-code-review` (`quick_lenses` / `thorough_lenses`, an Intent Alignment lens instead of an Acceptance Auditor) is not what the npm-installed 6.12.0 does. [V-lab vs V, `f033e70` files]

**Version finding, important for the wiki:** the clone (`f033e70`, 2026-09-18, main) is **ahead of the npm 6.12.0 package** for at least this skill. Several installed skill files differ from the clone's (`bmad-build`, `bmad-spec`, `bmad-code-review` all show file differences). Some differences may be installer processing; the review-layer structure difference is real. Wiki pages built from the clone describe unreleased main, not the installed release, wherever they touch these skills. [V-lab diff; cause inferred, I]

**Scoring against the planted flaws (ground truth written before the run):**

| Flaw | Quick run | Thorough run |
|---|---|---|
| A `pct` unvalidated | Caught, G6, medium, **defer** (public API) | Caught, #5, low, patch (drop the export) |
| B unknown coupon gives NaN and corrupts cart | Caught, G2, high, patch | Caught, #2, high, patch (also `total(c)` and `'constructor'`) |
| C `qty` guard removed, suite red | Caught, G1, high, patch | Caught, #3, high, patch (also noted `npm test` red up front) |
| D mutation, discounts compound | Caught, G3, high, patch | Caught, #1, high, patch |
| E `applyDiscount` untested | Caught (inside G5 and G6) | Caught (#4, #5) |
| F "coupon works" asserts nothing | Caught, G5, high | Caught, #4, medium |
| G case-sensitive coupon | Partial (named "wrong case" inside G2) | Not called out |

Both caught all six main flaws (A to F); quick also touched G. Every claim was re-verified by executing the code before being graded, as the docs said [P14]. [V-lab]

**Findings I had not planted:**
- **Per-item rounding overcharges** (`{priceCents:333, qty:10}` with SAVE10 gives 3000, correct 2997). Quick: high, patch. Thorough: medium, **defer** ("both rounding policies are defensible"). A real bug found by both, graded differently. [V-lab]
- "Duplicate `require('../cart')` mid-file": found by both, low, patch.
- "Unit of `COUPONS` values is ambiguous": quick kept it (low, patch); thorough rejected it as `false` (the name `pct` and `/ 100` state it). Same claim, opposite verdicts across runs. [V-lab]

**Counts:** quick 0 decision-needed, 7 patch, 1 defer, 1 rejected. Thorough 0 decision-needed, 6 patch, 1 defer, 1 rejected. [V-lab]

**Observations**
- **The narrative worked as the claims input:** the quick run opened with a table of the four narrative claims, three of them false on the code. [V-lab] This is the Edge Case Hunter's claims check (`claims-check.md`) working even without a spec. [I]
- **Triage variance between two runs of the same skill is real:** the same rounding finding was high-and-patch in one run, medium-and-defer in the other; the unit-ambiguity finding was kept in one and refuted in the other. Two runs is a small sample. [V-lab; I on significance]
- **Both runs halted at the next human decision, and I did not answer it.** Verbatim: "How would you like to handle the N `patch` findings? 1. Apply every patch, 2. Walk through each patch." The workflow does not apply patches without that choice. [V-lab] Neither run modified source; the thorough run wrote `_bmad-output/implementation-artifacts/deferred-work.md` with the deferred item. [V-lab]
- **Headless BMAD needs three pre-approvals to finish a review:** no-spec declared, checkpoint approved, patch handling chosen. A fully unattended run needs all three in the prompt. [V-lab; I]


## Experiment 4 — existing-codebase start (2026-09-19, done; project-context halted on questions)

**Docs read first (release tag, P24):** `docs/existing-codebases/start-in-an-existing-codebase.md` and `set-and-maintain-project-context.md`. Claims tested: (1) `bmad-project-context` reads what exists, shows the complete block, and asks before it writes; it never commits. (2) It skips what the repo already states and asks what a scan cannot answer. (3) Skipping it "does not fail a Build". (4) "You do not inventory conventions beforehand": `bmad-build` investigates the repo, follows what it finds, and does not stop to ask whether to match the codebase. (5) A small change goes straight to `bmad-build`.

**Setup:** `labs\lab4-base`, a small existing library `notes-lib` (CommonJS, `node:test`) with one baseline commit, no `AGENTS.md`, BMAD 6.12.0 installed (29 skills). Two identical copies run at once, headless with `claude -p ... --permission-mode acceptEdits`: `lab4-context` (`bmad-project-context`, told not to answer questions or approve writes) and `lab4-build` (`bmad-build` with no project context, request: "Add `removeNote(store, id)` ... returns the removed note. An unknown id must fail."). Conventions written down before the run: errors are `NoteError` with `E_*` codes; the store is injected and `src/notes.js` never touches the filesystem; tests live in `tests/*.spec.js` with `node:test` and a `memoryStore` helper; ids are `nN` strings; exports are listed at the bottom.

**Project-context run (135 s): halted before writing anything, as documented.** [V-lab]
- It found no instruction files, so it chose intent "setup". It ran `npm test` (4 pass), read `package.json`, checked for CI, `docs/`, `engines`, nested manifests, and git history, and reported what the repo already states "and therefore stays out of the block". Matches the docs' "it skips what the repo already says". [V-lab; V, P24]
- It could not run `resolve_customization.py` and `resolve_config.py` without approval in headless mode, and read `customize.toml` and `_bmad/config*.toml` directly instead. Headless runs may hit permission prompts the skill routes around. [V-lab]
- **Questions it asked, verbatim, and left unanswered (per the no-unattended-answers rule):** "1. Rules you want followed regardless of what this repo does — governance, security/compliance, coding standards, style guides, frozen or off-limits paths? 2. Any outside documents to draw on — handbooks, wikis, architecture docs, MCP knowledgebases? Paths only; I won't read them yet. 3. What Node version does the team target? `package.json` has no `engines` field. 4. Where do planning docs and tickets live for this repo, if anywhere? 5. Has an agent already gotten something wrong in this repo?"
- The docs list four kinds of thing a scan cannot answer (what agents get wrong, what is off limits, domain terms, commands with a catch); the run asked those plus a Node-version and a where-do-tickets-live question. [V-lab; V, P24]
- The repo stayed clean; nothing was proposed as a block yet. So the "shows the complete block before writing" step was not reached. [V-lab]

**Build run (389 s): matched the docs, and followed every convention.** [V-lab]
- Route `oneshot` (spec frontmatter). No human question was asked. It did not stop to ask whether to match the codebase. The spec kept only Intent and Implementation Notes, as the release's oneshot gate specifies (`build-step-by-step.md`). [V-lab]
- **Conventions scored:** `NoteError('E_NOT_FOUND', ...)` reused, with the same message shape as `getNote`: followed. Store injected, no filesystem: followed. Tests added to `tests/notes.spec.js` with `node:test`: followed. Export added to the bottom `module.exports`: followed. Verified with `npm test` (the script, not a guessed command): followed. 5 of 5. It also wrote down why it reused the existing error code: "the library has exactly one failure convention." [V-lab]
- **Review:** Blind Hunter only (oneshot), as in the release step files. 9 findings: 5 patched, 1 deferred, 3 rejected (`false`/`low` with reasons). The two rejections that cite the codebase's own behavior ("matches `getNote` exactly", "the library validates input in `addNote` only") show the review applying the same investigate-and-follow rule. [V-lab]
- **Real finding surfaced:** removing the highest-id note lets the next `addNote` reuse that id, because `nextId` is max plus one. Deferred to `deferred-work.md` as pre-existing behavior the new function makes reachable, and recorded in the spec. The change was not blocked on it. [V-lab]
- **Cost of patching low findings:** 4 of the 5 patches were `low` verdicts, applied "because the fix was a simple correction". The test helper `memoryStore` was extended with a save counter, and the tests grew from 1 planned to 3 removeNote tests. Small scope creep in tests, not in behavior. The release's rule allows this: only `low` findings whose fix adds more than a direct correction are rejected. [V-lab; V, P18r]
- **Commit:** none, again. "Commit skipped per your instruction" (I had said not to commit). Same conflict with BMAD's default commit step as Experiment 2, this time from an explicit prompt rather than a global rule. [V-lab]

**Weak spot in my own setup:** I planned "the test command catch" as a hidden convention, but the catch (a glob) is already written in `package.json`'s `test` script, so a scan finds it. It did not test whether project-context finds something a scan cannot. [I]

**Docs vs observed**

| Claim (P24) | Observed |
|---|---|
| Project-context asks before it writes | Yes; halted with 5 questions, wrote nothing |
| It skips what the repo states | Yes, explicitly reported |
| Skipping context does not fail a Build | Yes; build succeeded with no `AGENTS.md` |
| Build follows conventions, does not ask | Yes; 5 of 5 conventions, 0 questions |
| Small change goes straight to build, light path | Yes; `route: oneshot` |
| Never commits (project-context) | Not reached; the build declined to commit under my instruction |

**Not tested:** whether adding project context changes a later build's result (would need answers to the five questions, which a human owns); a change big enough for the dispatch route in an existing codebase; the docs' "Try It on a Known Tree" walkthrough (`getting-deeper.md`).

## Experiment 6 — ideation skills, unattended (2026-09-20, done; both halted on human input as predicted)

**Docs read first (release tag, P25):** `wiki/ideation-skills.md`. Claims tested: (1) `bmad-brainstorming` outside headless mode generates no ideas in the two dialogue stances and needs the user to choose a stance and technique batch; headless is defined by "the absence of a human", so a `claude -p` prompt may or may not count. (2) `bmad-forge-idea` has no headless mode and should stop at its opening questions.

**Setup:** `labs\lab6-base` (empty git repo plus one commit, BMAD 6.12.0 installed, 29 skills) copied to `lab6-brain` and `lab6-forge`, run at once with `claude -p ... --permission-mode acceptEdits`. Prompts named the skill plus a topic (brainstorming: "ways a solo developer can keep small side projects from going stale; goal: a list of directions I could try") or an idea (forge: "a weekly email digest that summarizes my own git commits across all my repos"), and told the skill not to be answered on my behalf. No `headless: true` flag was passed. Predictions were written before the run (in `STATE.md`).

**Brainstorming (88 s): treated the run as interactive and halted before starting. Prediction confirmed.** [V-lab]
- Because topic and goal were in the prompt, it skipped the kickoff question, as the skill allows ("if the kickoff already made both clear, skip the question and confirm"). It stopped at the next required step: the stance (Facilitator, Creative Partner, Ideate for me, quoted from the skill) and technique batch.
- It tried to open the composer page and reported that the session "can't get approval to launch it", then gave the file path (`.claude\skills\bmad-brainstorming\assets\brain-selector.html`) and offered the in-chat alternative ("let's do it in chat", 3 to 4 techniques). It did not claim the page had opened, following the skill's rule.
- It also asked the skill's other opening question, "any inputs or special requests?", and mentioned that `bmad-party-mode` and `bmad-advanced-elicitation` are installed.
- **Answers the open question from the wiki:** a plain `claude -p` prompt does **not** count as headless for `bmad-brainstorming`. The skill's rule is that a present human message makes it interactive ("no payload shape or phrasing overrides that"), and the run followed it. A real headless run would need the flag or a prepend step. [V-lab; V, P25]
- Nothing was written: no memlog, no `_bmad-output/` file. State is only created once topic, goal, and stance are known. [V-lab]

**Forge idea (79 s): halted at intent discovery with two questions, wrote nothing. Prediction confirmed.** [V-lab]
- Activation completed: it greeted by name ("Morning, Carl"), resolved config and the persona roster, and checked for a session to resume. It took the idea from the prompt as given and asked the user to correct it if wrong.
- **Questions, verbatim, unanswered:** "do you want to clarify and understand it, test whether it holds up, or make it better?" and "is it a new idea or a change to an existing project? If the latter, what project is it, and where can I find its files or other relevant materials?"
- The memlog was not created: the skill creates it "once the goal is known", and the goal was the unanswered question. So an unattended run leaves no trace at all. [V-lab; V, P25]
- Matches the file's design: it opens by asking what the session is for and whether the idea is new or a change to an existing project. It asked only what the prompt had not supplied. [V-lab]

**Both skills honor "ask only what's missing":** each accepted what the prompt supplied (topic and goal, or the idea) and asked only for the next required input. [V-lab; I on the generalization]

**Not tested, and what would test it:** the ideation content itself (idea quality, the attack/defend modes, the two-voice persona turns, the HTML outputs). Two follow-ups are possible without a human: (a) pass a real headless signal to `bmad-brainstorming` (`headless: true` and a topic in the payload) and check for `brainstorm.html`, a memlog, and a JSON return; (b) run brainstorming in the "Ideate for me" stance, which the skill says a human can choose in advance and which would need the stance stated in the prompt (a choice the docs put on the user, so it is Carl's call). Forge idea has no unattended path in the file, so it cannot be run to completion without answers. [I]


## Experiment 5 — a spec-backed epic, then `bmad-correct-course` (2026-09-20, done, interactive with Carl)

**Method change:** first experiment where the human answers were Carl's, not mine. Each skill ran as one headless `claude -p` call per step (`--continue` to keep the session); I relayed every question to Carl verbatim in chat and passed his answer back verbatim. The prompt told the skill to ask, not choose. So the questions and answers below are real BMAD prompts and real human choices. [V-lab]

**Setup:** `labs\lab5-epic`, a copy of `lab4-base` (`notes-lib`, no `removeNote`, BMAD 6.12.0). Input intent for `bmad-spec`: "Add tags to the notes library ..." (add tag, remove tag, list by tag, lowercase 1 to 20 chars, at most 5 per note, removing a note removes its tags).

**The spec and story stage (Carl's answers in brackets):**

| Step | BMAD asked | Carl | Time |
|---|---|---|---|
| 1 | Spec folder slug | note-tag | 99 s |
| 2 | Express or guided (input sparse) | express | 14 s |
| 3 | (wrote the spec) 3 capabilities, 4 assumptions, 7 open questions; both self-validate passes PASS; offered to walk the questions | leave open, "break this into stories" | 181 s |
| 4 | Proposed 3 stories; the cascade constraint had no story because `removeNote` was unresolved | add the cascade as a fourth story | 22 s |
| 5 | Per story: `spec_checkpoint`, `done_checkpoint`, `invoke_dev_with` | all false and none, except story 4: spec_checkpoint true, note "removeNote doesn't exist yet, add it first" | 17 s |
| 6 | (wrote `stories.yaml`, schema PASS) then stopped: the story-4 note decides open question 1, and `invoke_dev_with` may carry dispatch notes only, so the decision must land in `SPEC.md`. Options: (a) mint CAP-4, re-derive stories; (b) resolve the question in place | (a) | 101 s |
| 7 | Minted CAP-4, re-derived `stories.yaml` (story 4 retitled, ids unchanged), both validate passes PASS, count of open questions back to 7 (a new one: removing a note id that does not exist) | none | 52 s |

**Observations on the spec stage**
- **The skill policed its own rules against the human's input.** Carl's story-4 note put a scope decision into `invoke_dev_with`; the skill refused to carry it there and made him place it in the spec. That is the schema's "dispatch notes only" rule and Spec Law rule 7 enforced live. [V-lab; V, `spec-skill.md`]
- **Re-derivation worked as documented:** story ids stayed, CAP ids are stable and unique, `.memlog.md` logged each event (re-derived, both passes, schema check, finalized). [V-lab]
- **Story Breakdown was not offered unprompted** after the spec was written; the closing message only offered to walk the open questions. It ran when Carl asked. The docs say interactive mode offers it "at most once per run when the input reads as multiple independently shippable slices". [V-lab; V, `spec-skill.md`] Whether the offer was skipped or would have come later is unknown. [?]
- **Minting a capability creates new gaps:** answering one question opened another. Open questions are a living list, not a shrinking one. [V-lab]
- **The 7 original open questions were never answered** (Carl chose to leave them). They stayed open through the change proposal. [V-lab]

**The requirement change and `bmad-correct-course`**

Carl picked the trigger from three options: "filtering notes by tag must now support two tags at once, so a caller can list notes that carry both tags", issued before story 2 starts, nothing built yet. The spec lists multi-tag filtering as a **non-goal**, so this contradicts the spec. My prompt named `SPEC.md` and `stories.yaml` as the planning documents.

| Step | BMAD asked | Carl | Time |
|---|---|---|---|
| 8 | Found no PRD or epics in `planning-artifacts/`; said it would use `SPEC.md` and `stories.yaml` "per your instruction". Asked: incremental or batch | batch | 55 s |
| 9 | Wrote the Sprint Change Proposal (257 lines, 7 sections) and asked Continue or Edit | Continue | 97 s |
| 10 | Asked: "Do you approve this Sprint Change Proposal for implementation? (yes/no/revise)" | yes | 7 s |
| 11 | Classified scope Minor, handed off to the Developer agent, logged the handoff, finished | none | 55 s |

**Findings**
- **It caught the contradiction:** the issue summary says the change "negates SPEC.md line 42 verbatim" and calls it "a spec-contract change, not a story tweak". It correctly located the change in story 3, not story 2, and said story 2 starts unblocked. [V-lab]
- **Six specific edits** (Non-goals, CAP-3, a Constraint, the Success signal, two new open questions, story 3's description); stories 1, 2 and 4 and all source files listed as not changed. Path: Direct Adjustment, effort Low, risk Low. Scope: Minor. [V-lab]
- **The workflow changed exactly one file, the proposal.** After approval, `SPEC.md` and `stories.yaml` were byte-identical to before (checked by diff). Applying the six edits was left to the Developer agent, with success criteria listed in the closing message. `sprint-status.yaml` was N/A (none exists). [V-lab]
- **Docs vs observed:** the tag's doc says apply the proposal then re-run Story Breakdown; the release skill's checklist says update `sprint-status.yaml` (`flow.md`). Observed: proposal written and approved, nothing else touched, `sprint-status.yaml` N/A. Consistent with the skill file; no `sprint-status.yaml` to update. [V-lab; V, skill files at v6.12.0]
- **A tension the proposal does not resolve:** `bmad-spec` says `SPEC.md` is derived from `.memlog.md` and "a hand-edit to `SPEC.md` from outside is unsupported and is overwritten on the next derive" (`spec-skill.md`). The proposal tells the Developer agent to edit `SPEC.md` and `stories.yaml` directly, and never mentions `bmad-spec`, the memlog, or re-deriving (checked by search). Following it literally would put the change only in the derived file. Whether the Developer agent, or a later `bmad-spec` run, would reconcile this is untested. [V-lab for the proposal text; ? for the consequence]
- **Confound:** because my prompt told it which documents to use, the run does not show what `bmad-correct-course` does when the planning documents it expects (PRD, epics) are missing and nobody says otherwise. It said "no PRD/epics" and used my substitution. [V-lab; ?]
- **Human decisions:** 9 answers from Carl across about 12 minutes of skill time (the skill time excludes waiting for the answers). Every decision was a real branch (slug, mode, whether to leave questions open, story shape, checkpoints, scope placement, propose mode, approve).

**Not done:** applying the six edits and re-running `bmad-spec`; building any story after the change; the seven original open questions.

## Experiment 7 — real-headless brainstorming (2026-09-20, done; both predictions wrong)

Follow-up to Experiment 6. Two copies of `lab6-base`: `lab7-flag` (prompt carries "headless: true" plus a topic, goal, and artifacts payload) and `lab7-prepend` (a team override `_bmad/custom/bmad-brainstorming.toml` whose `activation_steps_prepend` declares the run headless, the skill's documented third signal). **Predictions written beforehand: the flag alone stays interactive and halts; the prepend override goes headless and writes both artifacts. Both were wrong.** [V-lab]

- **`lab7-flag` (1509 s = 25 min): ran to completion and produced everything, without asking.** The model reasoned that the flag does not make it headless ("no payload shape or phrasing overrides that"), so it treated the run as interactive, and then **picked the "Ideate for me" stance itself**. It generated 108 ideas across 8 techniques, wrote `brainstorm.html` ("The Dormant Garden", self-contained), `brainstorm-intent.md` (8 directions) and a memlog of 127 entries with `status: complete`. It reported the deviation openly. It also corrected its own wrap-up note (it had said 104 ideas across 7 techniques; the real counts were 108 and 8), after an HTML subagent caught the discrepancy independently. [V-lab]
- **`lab7-prepend` (69 s): halted at the stance and technique step, wrote nothing.** It ran the prepend step, then checked it against the skill's own gate, "headless requires the absence of an interactive user ... a conjunction": the prepend supplies the signal, but a prompt is a message from a person, so the precondition fails. It quoted the skill's line that a present human asking to "brainstorm X and give me the HTML" is "a normal interactive opening". It did not open the composer page ("opening it is a side effect on a run you've halted"). [V-lab]
- **So in this environment no `claude -p` run counts as headless for `bmad-brainstorming`:** a payload flag, a prepend declaration, and a plain prompt all read as a present human. A real headless run needs a caller that supplies no user message stream (another skill or a runner). [V-lab; V, P25]
- **The stance was chosen by the model, not the user, in the one run that completed.** The skill says the stance is the user's choice, "set explicitly at the start, or already implied by how they asked". The flag run inferred "Ideate for me" from a prompt that asked for artifacts and said not to ask. It stated that it had done so. That is within the skill's "already implied by how they asked", but it is a judgment the skill leaves to the model. [V-lab; I]
- **Cost:** the completed run took 25 minutes and used subagents for the HTML and intent artifacts ("delegating each to a subagent that reads the log as its sole source", as the file says). [V-lab; V, P25]
- **Ideation quality is a different question:** the 8 directions and the dormancy-versus-rot reframe look sensible, but no one has judged them. Not assessed. [?]


### Experiment 5b — do hand-edits to `SPEC.md` survive a `bmad-spec` re-run? (2026-09-20, done)

**Question from Experiment 5:** the Sprint Change Proposal told the Developer agent to hand-edit `SPEC.md` and `stories.yaml`, but `bmad-spec` says `SPEC.md` is derived from `.memlog.md` and a hand-edit "is overwritten on the next derive". Which wins?

**Setup:** `labs\lab5-apply`, a copy of `lab5-epic`. I acted as the Developer agent and applied the proposal's edits 4.1 to 4.6 mechanically (a script extracting each OLD and NEW block, run against `SPEC.md` and `stories.yaml`; this step was mine, not BMAD's). The memlog was left untouched (49 lines). Then `bmad-spec` was run on the same spec folder with an editorial-only update signal: "shorten the Why paragraph by one sentence; no decisions change". Predictions, in my order of confidence: (1) the hand-edits silently vanish; (2) it notices the drift and asks; (3) it keeps them. [V-lab setup]

**Result (164 s): prediction 3. Every hand-edit survived.** [V-lab]
- Diffing `SPEC.md` before and after the run shows one changed line, the Why paragraph, which lost its second sentence. The rewritten non-goal, CAP-3, the new constraint, the success signal, and the two new open questions were all intact. `stories.yaml` was byte-identical.
- The skill's report said "4 assumptions and 9 open questions carry over unchanged from the last run", so it counted the two hand-added questions as part of the spec. It logged the trim as a decision, both self-validate passes PASS, and a note that `stories.yaml` was checked against the updated spec ("all 4 descriptions still match") and left as-is, per the rule that an update never rewrites `stories.yaml`.
- **The skill did not notice or flag the drift.** The memlog has no entry for the two-tag change (four new lines: the trim decision, two validate passes, the stories check). So `SPEC.md` and the memlog now disagree, and nothing said so. A later re-derive strictly from the memlog would lose the change. [V-lab; ? for the later re-derive]
- **What the result does and does not show.** It shows a small edit to one section does not overwrite the rest of the file: in practice the skill worked from the current `SPEC.md` too, not from the memlog alone. It does not show the memlog-derivation rule is wrong, because a one-sentence trim is a weak forcing case: the skill may have edited in place. A stronger test would need a change that forces regenerating whole sections. [I]
- **Doc vs behavior:** `spec-skill.md` quotes "a hand-edit ... is overwritten on the next derive" [V, P19]. Observed for one editorial change: not overwritten, and not detected. [V-lab] The practical risk is silent drift, not silent loss. [I]
- **Attribution note:** the memlog entry credits the trim to "Carl", although I issued the signal. The skill assumes the configured user (`user_name`) is the author of any instruction it receives. In a relay setup like this one, memlog authorship is unreliable. [V-lab]

**Not tested:** a derive that regenerates sections (for example, answering one of the open questions, which is Carl's decision), and applying the Developer-agent handoff through `bmad-agent-dev` instead of by script.


### Experiment 5c — a real decision as the update signal (2026-09-20, Carl's answer, done)

**Purpose:** the stronger drift test from 5b. Carl answered one open question, and that answer was passed to `bmad-spec` on the hand-edited spec in `lab5-apply` (copies of `SPEC.md`, `stories.yaml`, and the memlog were saved beforehand as `labs\lab5-*.before-normalize.*`).

**Carl's decision (relayed verbatim):** "Is 'tags are lowercase' a reject rule or a normalize rule?" Answer: **normalize** (uppercase input is lowercased and stored). The prediction I wrote beforehand was that a decision touching several sections would force more regeneration than the trim did, which might expose the drift. [V-lab]

**Result (137 s): another surgical update; all hand-edits survived again.** [V-lab]
- `SPEC.md` changed in exactly three places: the CAP-1 success line (now demonstrates `WORK` stored as `work`), the case constraint (normalize on add, out-of-length still rejected), and the answered open question, which was replaced by a new one the answer opened ("does lowercasing apply to the remove and filter paths too, or only on add?"). Open questions stayed at 9.
- Every two-tag edit from the change proposal was still present (the non-goal, CAP-3, the one-or-two-tags constraint, the success signal, both added open questions), confirmed by searching for each phrase. `stories.yaml` was byte-identical.
- **Memlog:** nine new entries: the direction (Carl's answer), a constraint that "supersedes entries 12 and 32", two decisions, the new question, a re-render event, both validate passes, and a stories check. The memlog **still has no record of the two-tag change**, so the drift from 5b is unchanged. [V-lab]
- **Attribution is correct here** ("Carl answered ..."), unlike 5b: the person answering really was Carl. [V-lab]
- **It found a stale phrase in `stories.yaml` and left it alone:** story 1's "the open case question in SPEC.md still applies" is now out of date, so it said so, kept the file as-is "per the update-never-rewrites-stories rule", and asked whether to re-run Story Breakdown. This matches `spec-skill.md` exactly. [V-lab; V, P19]
- It did not touch the hand-edits or mention them. [V-lab]

**Conclusion across 5b and 5c:** in two updates the skill edited `SPEC.md` surgically, keeping everything it was not asked to change, whether or not that content was in the memlog. So the documented rule ("re-derived on every run ... a hand-edit is overwritten") is not how it behaves in practice for these updates. What breaks is the record: the memlog stays incomplete, so anyone who relies on it (a resume, an audit, a future full re-derive) will not see the two-tag change. The change proposal's direct-edit route is therefore workable but leaves the memlog behind. [V-lab; I]

**Still untested:** a run from a nearly empty `SPEC.md` (a true re-derive), which is what the docs promise the memlog enables; and whether a new-session `bmad-spec` run with no `SPEC.md` at all rebuilds the two-tag content (it would not, the memlog lacks it). [?]


### Experiment 5d — true re-derive from the memlog (2026-09-20, done)

**Purpose:** the remaining test from 5c. `SPEC.md` was moved away in a copy of the hand-edited spec (`labs\lab5-rederive`, copy of `lab5-apply`; the old file is saved in `labs\lab5-rederive-saved\`), leaving `.memlog.md` and `stories.yaml`. `bmad-spec` was told SPEC.md was lost and to regenerate it. Prediction written beforehand: it regenerates from the memlog, and the two-tag content (which the memlog never recorded) is lost. [V-lab setup]

**Result (345 s, no question asked): prediction confirmed.** [V-lab]
- The skill said it "re-derived from `.memlog.md` rather than restored" (nothing was committed). Nothing in the run needed the user: mode, slug and scope were all in the log.
- **All two-tag content is gone.** Searching the new `SPEC.md` for the six phrases from the proposal's edits (rewritten non-goal, "both of two given tags", "one or two tags", the success-signal wording, both hand-added open questions) found none. The normalize decision (recorded in the memlog in 5c) is present, as is CAP-4. Open questions: 7 (the two hand-added ones gone; two others retired by CAP-4 and by the normalize answer, as the skill explained).
- **The rewrite is not verbatim:** 66 lines differ from the hand-edited file. The title changed ("Note Tags" became "Tags for the notes library"), the Why paragraph was reworded, and CAP intents and successes were rephrased ("detach" became "remove", and so on) with the same content. Capability ids stayed. Two more "wording fixes after the validate passes" were logged. So the derivation is a fresh generation each time, stable in meaning for logged decisions, not in wording. [V-lab; I on the generalization]
- **The mismatch was surfaced through `stories.yaml`.** The skill said story 3 "describes two-tag AND filtering with three-or-more rejected and cites an 'open API-shape question' — none of that appears anywhere in the memlog, and it contradicts the live non-goal", and that story 1's case clause is stale. It left the file untouched and offered to re-run Story Breakdown. So the drift did show up, but only because a second file still carried the change. [V-lab]
- The memlog got four new events (lost and re-derived, both validate passes, the stories check, two wording fixes). [V-lab]

**What 5b to 5d together show:**

| Situation | Behavior |
|---|---|
| `SPEC.md` exists, small update or a decision (5b, 5c) | Edited in place; unrelated hand-edits kept; memlog gets the new entries only; drift not mentioned |
| `SPEC.md` missing (5d) | Regenerated wholesale from the memlog; anything only in the old file is lost; mismatch with `stories.yaml` flagged |

So the docs' rule ("re-derived from the memlog ... a hand-edit is overwritten") holds when a full re-derive happens, and the earlier "no loss" result held only because the update was small. [V-lab]

**Practical consequence for the change-proposal route:** editing `SPEC.md` by hand (as the proposal prescribes) works day to day but is fragile: the change survives only as long as `SPEC.md` is never regenerated. Routing the change through `bmad-spec` (so it lands in the memlog) is the durable path, and it is what the requirement-change path in the docs describes (update the PRD, re-run `bmad-spec`, re-run Story Breakdown; `flow.md`). [I]


### Experiment 5e — the requirement change routed through `bmad-spec` (the docs' route) (2026-09-20, done)

**Purpose:** compare with the hand-edit route of 5b to 5d. `labs\lab5-route` is a copy of `lab5-epic`: the original spec (before any hand-edits, 49-line memlog), the four stories, and the approved Sprint Change Proposal from Experiment 5 sitting in `_bmad-output/planning-artifacts/`. `bmad-spec` was run on the spec folder with the same requirement change Carl chose ("filtering notes by tag must now support two tags at once, so a caller can list notes that carry both tags"). Prediction written beforehand: the skill puts the change in the memlog, re-derives the spec, flags story 3 as stale, and possibly surfaces the non-goal conflict as a question. [V-lab setup]

**Result (319 s, no question asked): the durable route works, and it found the proposal on its own.** [V-lab]
- **It used the approved proposal as its source.** The first memlog entry reads "Requirement change from Carl ... carried by the approved sprint change proposal ... (APPROVED 2026-09-20, unconditional)". I had not named the proposal in the prompt; it was in the planning-artifacts folder. Its summary: "the sprint change proposal's verbatim-patch handoff was applied as substance, not as hand-edits." So the correct-course to `bmad-spec` handoff the docs describe (update, then re-run) is what the skill itself does when both are present. [V-lab]
- **Fifteen new memlog entries** recorded the direction, three decisions (the non-goal narrowed rather than dropped; the widening lands on CAP-3 and not a new CAP-5; the success signal extended), the widened capability, the new constraint, three questions, a note that CAP-1, 2 and 4 are unaffected, the re-render, both validate passes, the stories check, and a decision to widen the Why paragraph. [V-lab]
- **The resulting `SPEC.md` matches the hand-edited version of 5b to 5d except for 7 lines.** It made the same edits to the non-goal, CAP-3, the constraint, the success signal, and the two open questions, plus two changes the proposal did not contain: the Why paragraph was widened to name the two-label retrieval, and the error-code open question was extended to cover the over-arity rejection. [V-lab] The skill also worded the arity constraint to "bound arity only", deliberately saying nothing about the function signature, so it would not pre-answer the API-shape question. [V-lab]
- **`stories.yaml` was untouched** ("this skill's update path never writes it"), and the skill flagged story 3 as stale, said stories 1, 2 and 4 still match, and offered to re-run Story Breakdown. It explicitly did not apply the proposal's edit 4.6. [V-lab]
- **Open questions:** 9 (the original 7 plus the two new ones), listed in full at the end. [V-lab]

**Comparison of the two routes**

| | Hand-edit (5b to 5d) | Through `bmad-spec` (5e) |
|---|---|---|
| Change in `SPEC.md` | Yes, verbatim | Yes, same substance, 7 lines different |
| Change in the memlog | No | Yes, 15 entries with reasons |
| Survives regenerating `SPEC.md` | No (5d) | Yes, by construction (the memlog holds it) [I] |
| `stories.yaml` | Edited by hand | Left alone, flagged stale, re-run offered |
| Time | Script instant, later update runs 137 to 164 s | 319 s |

So routing the change through `bmad-spec` costs about five minutes and leaves a complete record. [V-lab; I]

**Attribution:** the memlog credits the change to "Carl", citing the approved proposal. In this experiment Carl did approve the proposal, but the update signal itself came from me. The skill attributes a request to the configured user in either case. [V-lab]

**Not tested:** regenerating `SPEC.md` from this memlog (which should keep the two-tag content); re-running Story Breakdown after the change; the Developer agent (`bmad-agent-dev`) actually performing the handoff instead of a script or a `bmad-spec` run. [?]


### Experiment 5f — Story Breakdown re-run after the change (2026-09-20, Carl answered, done)

**Purpose:** close the loop from 5e: `stories.yaml` in `lab5-route` was stale after the spec change. Story Breakdown was re-run on the spec folder (saved copy of the old file: `labs\lab5-route-stories.before-rebreakdown.yaml`). Prediction written beforehand: it proposes the same four stories with only story 3 changed, and asks about checkpoints again. [V-lab setup]

**Step 1 (101 s): it proposed and asked, writing nothing.** It proposed the same four stories with only story 3's description changed (adds "or carrying both of two given tags", AND, three or more rejected, the open API-shape question applies), noted that no `stories/` spec files exist so no ids are pinned, and offered a **five-story alternative** that would split story 3 into single-tag and two-tag filters. It asked two questions: which list, and whether to carry the old checkpoint values and story-4 dispatch note forward "rather than my defaulting them". Prediction confirmed, plus the alternative I had not predicted. [V-lab]

**Carl's answer (verbatim):** "4 stories, carry the checkpoints forward".

**Step 2 (138 s): written and verified.** [V-lab]
- `stories.yaml` differs from the old file in one hunk: story 3's description. Stories 1, 2 and 4, and every checkpoint value including story 4's `spec_checkpoint: true` and its "removeNote doesn't exist yet, add it first" note, are byte-identical. It checked this by diffing and logged the check.
- Schema check PASS (four quoted ids, unique and prefix-free, no `status` field). Three memlog events: re-derived, schema check, byte-identity check.
- It said `git diff` could not verify the file because my lab setup excludes `_bmad-output/` from git, so it diffed against the previous content instead. That is an artifact of my setup, and it reported it honestly. [V-lab]
- It stated that one open question gates the next story: whether the two-tag filter is a separate function or one parameter taking one or two tags. The approved proposal had said it must be answered before story 3 starts; it does not block story 2. [V-lab]

**The whole change loop, as observed (Experiments 5, 5e, 5f):** spec and stories (Experiment 5) then requirement change, then correct-course proposal (Experiment 5), then `bmad-spec` update using the proposal (5e), then Story Breakdown re-run (5f). Each step asked the human only what it needed, changed only what the previous step made stale, and flagged what it left alone. This matches the docs' requirement-change path (update the spec, re-run Story Breakdown; `flow.md`) and the "Learn and adjust" stage. [V-lab; V, P3, P7]

**Human effort for the loop:** 13 answers from Carl in total across Experiments 5 to 5f (slug; express; leave questions open; story shape; checkpoints; scope placement (a); change picked (1); batch mode; Continue; approve; the normalize answer; 4 stories; carry checkpoints). About 20 to 30 minutes of skill runtime in the interactive paths, excluding the true re-derive.

**Not tested:** building any of the stories. The loop from spec to code after a change is Experiment 2's territory, not repeated here. [?]
