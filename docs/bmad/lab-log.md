# BMAD — Lab Log

*Observations from running BMAD in throwaway repos under `C:\Users\ctupp\labs\`. Tag [V-lab] = seen happening. Each entry says what the docs predicted and what actually happened.*

*This is a log: entries are kept as written at the time. Where a later experiment answered an entry's "not tested" or "unconfirmed" line, a `→ Later:` pointer was added (Carl review pass, 2026-09-24) instead of rewriting the entry.*

!!! tip "Index — one line per entry, in order run"
    - [Experiment 1](#experiment-1-install-and-skill-load-2026-09-19) — full install works; 29 skills confirmed.
    - [Experiment 2](#experiment-2-one-toy-idea-through-the-loop-2026-09-19-done) — spec through build round trip, dispatch route, 18/18 tests, review found real issues.
    - [Experiment 3](#experiment-3-bmad-code-review-on-a-flawed-diff-2026-09-19-done-first-attempt-halted-rerun-ran) — caught all six planted flaws; surfaced that the clone repo was ahead of the npm release.
    - [Experiment 4](#experiment-4-existing-codebase-start-2026-09-19-done-project-context-halted-on-questions) — project-context halted with five questions; a small oneshot build followed five of five planted conventions.
    - [Experiment 6](#experiment-6-ideation-skills-unattended-2026-09-20-done-both-halted-on-human-input-as-predicted) — both ideation skills halted for human input unattended, as the files predict.
    - [Experiment 5](#experiment-5-a-spec-backed-epic-then-bmad-correct-course-2026-09-20-done-interactive-with-carl) — a spec-backed epic, then a requirement change handled through a Sprint Change Proposal, interactively with Carl.
    - [Experiment 7](#experiment-7-real-headless-brainstorming-2026-09-20-done-both-predictions-wrong) — both predictions about what makes a run headless were wrong; a present human message always means interactive.
    - [Follow-ups with Carl's answers](#follow-ups-with-carls-answers-2026-09-21) — smaller open questions from earlier experiments, answered.
    - [Experiment 5h](#experiment-5h-all-four-stories-built-interactively-2026-09-21-to-2026-09-23-done) — the full four-story epic built end to end, 61/61 tests, every checkpoint fired as documented.
    - [Experiment 4b](#experiment-4b-does-agentsmd-change-a-build-once-it-exists-2026-09-23-carl-answered-done) — same code, same bug found either way; project context changed only whether it escalated to a human.
    - [Experiment 5i](#experiment-5i-bmad-retrospective-on-the-finished-tags-epic-2026-09-2324-carl-answered-done) — retrospective on the finished epic found B1 (a live-object aliasing defect) and 16 action items.
    - [R1/R1b](#r1r1b-fixing-retrospective-finding-b1-2026-09-2425-carl-answered-done) — B1 fixed and committed: all eight leaking exits closed across two builds.
    - [Experiment 8](#experiment-8-add-on-setup-tea-2026-09-26-done) — TEA/BMB/CIS installed and pinned; TEA would not have caught B1 through any workflow examined.
    - [Experiment 9 / 9b](#experiment-9-cross-epic-frozen-test-2026-09-27-to-09-29-done-interactive-with-carl) — frozen story blocks are guarded within their own spec, but a second epic changes their code without anything noticing.
    - [Experiment 10](#experiment-10-bmad-code-review-over-the-whole-tags-epic-2026-092930-done-interactive-with-carl) — a whole-epic range review found B1's pieces but rejected B1 as spec-sanctioned; it did catch the missing mutation test (B6) mid-epic.
    - [Experiment 11](#experiment-11-bmad-architecture-brownfield-on-a-legacy-shaped-toy-2026-09-30-to-10-01-done-interactive-with-carl) — on a legacy app with rules in UI handlers, the spine bound every rule by making the old code a frozen parity oracle, and found that the form wiring isn't in the code at all.
    - [Experiment 12](#experiment-12-bmad-prd-update-mode-on-a-hand-written-prd-2026-10-02-done-interactive-with-carl) — Update mode surfaced every planted conflict before editing, kept the board decision as a baseline, and its reviewer gate caught a loophole in an approved answer.
    - [Experiment 13](#experiment-13-bmb-build-what-survives-a-reinstall-2026-10-03-done-interactive-with-carl) — _bmad/custom overrides and hand-added skills survive a reinstall; direct edits to a skill's customize.toml are lost with no backup; a failed update is not atomic.
    - [Experiment 14](#experiment-14-cis-carson-vs-bmad-brainstorming-directly-2026-10-03-done-interactive-with-carl) — CIS brainstorming is the core skill behind a persona; through Carson the session was structurally identical, but repeats (14b, three runs per arm) showed no mechanical difference and only a weak lean toward a costed shortlist.

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

**Observed while reading the installed agent files:** the Developer agent's `customize.toml` defines the persona (see [agents.md](agents.md), "Persona anatomy"). The file says "DO NOT EDIT -- overwritten on every update"; customization goes in `_bmad/custom/`. [V-lab]

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
| Build commits locally [P8] | Unconfirmed at 08:05. → Later: did not commit; Carl's global confirm-before-committing rule overrode it (Step 3 result above) |
| Light path for clean designs [P8] | Not exercised; the open questions forced the full path. → Later: Experiment 4 took `oneshot` |

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

**Resolved:** Carl chose "no spec" and a rerun followed (below). Original question kept for the record: how to rerun. (1) provide a spec file path (I'd have to write one for the toy, which tests the full four-layer path including the acceptance layer), or (2) say "no spec" (three layers). Either way the prompt should also pre-approve the step-1 checkpoint. Quick vs thorough comparison against A to G has not happened; scores are blank. → Later: scored in the rerun below.


### Rerun with "no spec" (Carl's choice, 2026-09-19)

Same labs. The prompt now said "no spec (no-spec mode)", supplied the intent as the change narrative, and pre-approved the step-1 checkpoint. Both ran to the presented findings. **Times: quick 382 s, thorough 527 s.** [V-lab]

**Both runs ran the same three layers: Blind Hunter, Edge Case Hunter, Verification Gap.** The Acceptance Auditor was skipped because there was no spec. [V-lab] So "quick" and "thorough" did not select different reviewer sets. Cause: the installed skill's `customize.toml` has `[[workflow.review_layers]]` (four layers, the Acceptance Auditor gated on `review_mode = full`) and no quick/thorough selection. [V-lab, installed file] The quick/thorough behavior in the repo docs [P14] and in the cloned repo's `bmad-code-review` (`quick_lenses` / `thorough_lenses`, an Intent Alignment lens instead of an Acceptance Auditor) is not what the npm-installed 6.12.0 does. [V-lab vs V, `f033e70` files]

**Version finding, important for the wiki:** the clone (`f033e70`, 2026-09-18, main) is **ahead of the npm 6.12.0 package** for at least this skill. Several installed skill files differ from the clone's (`bmad-build`, `bmad-spec`, `bmad-code-review` all show file differences). Some differences may be installer processing; the review-layer structure difference is real. Wiki pages built from the clone describe unreleased main, not the installed release, wherever they touch these skills. [V-lab diff; cause inferred, I] → Later: the CRLF-normalized diff and re-pin (same day) showed only `bmad-build` and `bmad-code-review` differ substantively; `bmad-spec` differs only in activation lines. See [build-step-by-step.md](build-step-by-step.md), last section.

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
- **Both runs halted at the next human decision, and I did not answer it.** Verbatim: "How would you like to handle the N `patch` findings? 1. Apply every patch, 2. Walk through each patch." The workflow does not apply patches without that choice. [V-lab] → Later: Carl chose "apply all" on 2026-09-21 (Follow-ups section). Neither run modified source; the thorough run wrote `_bmad-output/implementation-artifacts/deferred-work.md` with the deferred item. [V-lab]
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
- Route `oneshot` (spec frontmatter). No human question was asked. It did not stop to ask whether to match the codebase. The spec kept only Intent and Implementation Notes, as the release's oneshot gate specifies ([build-step-by-step.md](build-step-by-step.md)). [V-lab]
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

**Not tested:** whether adding project context changes a later build's result (would need answers to the five questions, which a human owns; → Later: answered 2026-09-21, tested in Experiment 4b); a change big enough for the dispatch route in an existing codebase; the docs' "Try It on a Known Tree" walkthrough (`getting-deeper.md`).

## Experiment 6 — ideation skills, unattended (2026-09-20, done; both halted on human input as predicted)

**Docs read first (release tag, P25):** `wiki/ideation-skills.md`. Claims tested: (1) `bmad-brainstorming` outside headless mode generates no ideas in the two dialogue stances and needs the user to choose a stance and technique batch; headless is defined by "the absence of a human", so a `claude -p` prompt may or may not count. (2) `bmad-forge-idea` has no headless mode and should stop at its opening questions.

**Setup:** `labs\lab6-base` (empty git repo plus one commit, BMAD 6.12.0 installed, 29 skills) copied to `lab6-brain` and `lab6-forge`, run at once with `claude -p ... --permission-mode acceptEdits`. Prompts named the skill plus a topic (brainstorming: "ways a solo developer can keep small side projects from going stale; goal: a list of directions I could try") or an idea (forge: "a weekly email digest that summarizes my own git commits across all my repos"), and told the skill not to be answered on my behalf. No `headless: true` flag was passed. Predictions were written before the run (in `STATE.md`).

**Brainstorming (88 s): treated the run as interactive and halted before starting. Prediction confirmed.** [V-lab]
- Because topic and goal were in the prompt, it skipped the kickoff question, as the skill allows ("if the kickoff already made both clear, skip the question and confirm"). It stopped at the next required step: the stance (Facilitator, Creative Partner, Ideate for me, quoted from the skill) and technique batch.
- It tried to open the composer page and reported that the session "can't get approval to launch it", then gave the file path (`.claude\skills\bmad-brainstorming\assets\brain-selector.html`) and offered the in-chat alternative ("let's do it in chat", 3 to 4 techniques). It did not claim the page had opened, following the skill's rule.
- It also asked the skill's other opening question, "any inputs or special requests?", and mentioned that `bmad-party-mode` and `bmad-advanced-elicitation` are installed.
- **Answers the open question from the wiki:** a plain `claude -p` prompt does **not** count as headless for `bmad-brainstorming`. The skill's rule is that a present human message makes it interactive ("no payload shape or phrasing overrides that"), and the run followed it. A real headless run would need the flag or a prepend step. [V-lab; V, P25] → Later: Experiment 7 showed neither works under `claude -p`; a present user message overrides both.
- Nothing was written: no memlog, no `_bmad-output/` file. State is only created once topic, goal, and stance are known. [V-lab]

**Forge idea (79 s): halted at intent discovery with two questions, wrote nothing. Prediction confirmed.** [V-lab]
- Activation completed: it greeted by name ("Morning, Carl"), resolved config and the persona roster, and checked for a session to resume. It took the idea from the prompt as given and asked the user to correct it if wrong.
- **Questions, verbatim, unanswered:** "do you want to clarify and understand it, test whether it holds up, or make it better?" and "is it a new idea or a change to an existing project? If the latter, what project is it, and where can I find its files or other relevant materials?"
- The memlog was not created: the skill creates it "once the goal is known", and the goal was the unanswered question. So an unattended run leaves no trace at all. [V-lab; V, P25]
- Matches the file's design: it opens by asking what the session is for and whether the idea is new or a change to an existing project. It asked only what the prompt had not supplied. [V-lab]

**Both skills honor "ask only what's missing":** each accepted what the prompt supplied (topic and goal, or the idea) and asked only for the next required input. [V-lab; I on the generalization]

**Not tested, and what would test it:** the ideation content itself (idea quality, the attack/defend modes, the two-voice persona turns, the HTML outputs). Two follow-ups are possible without a human: (a) pass a real headless signal to `bmad-brainstorming` (`headless: true` and a topic in the payload) and check for `brainstorm.html`, a memlog, and a JSON return; (b) run brainstorming in the "Ideate for me" stance, which the skill says a human can choose in advance and which would need the stance stated in the prompt (a choice the docs put on the user, so it is Carl's call). Forge idea has no unattended path in the file, so it cannot be run to completion without answers. [I] → Later: (a) and, by the model's own stance choice, (b) were run as Experiment 7. Ideation quality is still unjudged.


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
- **The skill policed its own rules against the human's input.** Carl's story-4 note put a scope decision into `invoke_dev_with`; the skill refused to carry it there and made him place it in the spec. That is the schema's "dispatch notes only" rule and Spec Law rule 7 enforced live. [V-lab; V, [spec-skill.md](spec-skill.md)]
- **Re-derivation worked as documented:** story ids stayed, CAP ids are stable and unique, `.memlog.md` logged each event (re-derived, both passes, schema check, finalized). [V-lab]
- **Story Breakdown was not offered unprompted** after the spec was written; the closing message only offered to walk the open questions. It ran when Carl asked. The docs say interactive mode offers it "at most once per run when the input reads as multiple independently shippable slices". [V-lab; V, [spec-skill.md](spec-skill.md)] Whether the offer was skipped or would have come later is unknown. [?]
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
- **Docs vs observed:** the tag's doc says apply the proposal then re-run Story Breakdown; the release skill's checklist says update `sprint-status.yaml` ([flow.md](flow.md)). Observed: proposal written and approved, nothing else touched, `sprint-status.yaml` N/A. Consistent with the skill file; no `sprint-status.yaml` to update. [V-lab; V, skill files at v6.12.0]
- **A tension the proposal does not resolve:** `bmad-spec` says `SPEC.md` is derived from `.memlog.md` and "a hand-edit to `SPEC.md` from outside is unsupported and is overwritten on the next derive" ([spec-skill.md](spec-skill.md)). The proposal tells the Developer agent to edit `SPEC.md` and `stories.yaml` directly, and never mentions `bmad-spec`, the memlog, or re-deriving (checked by search). Following it literally would put the change only in the derived file. Whether the Developer agent, or a later `bmad-spec` run, would reconcile this is untested. [V-lab for the proposal text; ? for the consequence] → Later: tested in 5b to 5e (hand-edits survive small updates, are lost on a true re-derive; routing through `bmad-spec` is durable).
- **Confound:** because my prompt told it which documents to use, the run does not show what `bmad-correct-course` does when the planning documents it expects (PRD, epics) are missing and nobody says otherwise. It said "no PRD/epics" and used my substitution. [V-lab; ?]
- **Human decisions:** 9 answers from Carl across about 12 minutes of skill time (the skill time excludes waiting for the answers). Every decision was a real branch (slug, mode, whether to leave questions open, story shape, checkpoints, scope placement, propose mode, approve).

**Not done:** applying the six edits and re-running `bmad-spec`; building any story after the change; the seven original open questions. → Later: all three done in 5b to 5h.

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
- **Doc vs behavior:** [spec-skill.md](spec-skill.md) quotes "a hand-edit ... is overwritten on the next derive" [V, P19]. Observed for one editorial change: not overwritten, and not detected. [V-lab] The practical risk is silent drift, not silent loss. [I]
- **Attribution note:** the memlog entry credits the trim to "Carl", although I issued the signal. The skill assumes the configured user (`user_name`) is the author of any instruction it receives. In a relay setup like this one, memlog authorship is unreliable. [V-lab]

**Not tested:** a derive that regenerates sections (for example, answering one of the open questions, which is Carl's decision), and applying the Developer-agent handoff through `bmad-agent-dev` instead of by script. → Later: the first was run as 5c and 5d. The second is still untested (no agent persona has been loaded in any experiment; candidate in `STATE.md` Next).


### Experiment 5c — a real decision as the update signal (2026-09-20, Carl's answer, done)

**Purpose:** the stronger drift test from 5b. Carl answered one open question, and that answer was passed to `bmad-spec` on the hand-edited spec in `lab5-apply` (copies of `SPEC.md`, `stories.yaml`, and the memlog were saved beforehand as `labs\lab5-*.before-normalize.*`).

**Carl's decision (relayed verbatim):** "Is 'tags are lowercase' a reject rule or a normalize rule?" Answer: **normalize** (uppercase input is lowercased and stored). The prediction I wrote beforehand was that a decision touching several sections would force more regeneration than the trim did, which might expose the drift. [V-lab]

**Result (137 s): another surgical update; all hand-edits survived again.** [V-lab]
- `SPEC.md` changed in exactly three places: the CAP-1 success line (now demonstrates `WORK` stored as `work`), the case constraint (normalize on add, out-of-length still rejected), and the answered open question, which was replaced by a new one the answer opened ("does lowercasing apply to the remove and filter paths too, or only on add?"). Open questions stayed at 9.
- Every two-tag edit from the change proposal was still present (the non-goal, CAP-3, the one-or-two-tags constraint, the success signal, both added open questions), confirmed by searching for each phrase. `stories.yaml` was byte-identical.
- **Memlog:** nine new entries: the direction (Carl's answer), a constraint that "supersedes entries 12 and 32", two decisions, the new question, a re-render event, both validate passes, and a stories check. The memlog **still has no record of the two-tag change**, so the drift from 5b is unchanged. [V-lab]
- **Attribution is correct here** ("Carl answered ..."), unlike 5b: the person answering really was Carl. [V-lab]
- **It found a stale phrase in `stories.yaml` and left it alone:** story 1's "the open case question in SPEC.md still applies" is now out of date, so it said so, kept the file as-is "per the update-never-rewrites-stories rule", and asked whether to re-run Story Breakdown. This matches [spec-skill.md](spec-skill.md) exactly. [V-lab; V, P19]
- It did not touch the hand-edits or mention them. [V-lab]

**Conclusion across 5b and 5c:** in two updates the skill edited `SPEC.md` surgically, keeping everything it was not asked to change, whether or not that content was in the memlog. So the documented rule ("re-derived on every run ... a hand-edit is overwritten") is not how it behaves in practice for these updates. What breaks is the record: the memlog stays incomplete, so anyone who relies on it (a resume, an audit, a future full re-derive) will not see the two-tag change. The change proposal's direct-edit route is therefore workable but leaves the memlog behind. [V-lab; I]

**Still untested:** a run from a nearly empty `SPEC.md` (a true re-derive), which is what the docs promise the memlog enables; and whether a new-session `bmad-spec` run with no `SPEC.md` at all rebuilds the two-tag content (it would not, the memlog lacks it). [?] → Later: both answered by 5d.


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

**Practical consequence for the change-proposal route:** editing `SPEC.md` by hand (as the proposal prescribes) works day to day but is fragile: the change survives only as long as `SPEC.md` is never regenerated. Routing the change through `bmad-spec` (so it lands in the memlog) is the durable path, and it is what the requirement-change path in the docs describes (update the PRD, re-run `bmad-spec`, re-run Story Breakdown; [flow.md](flow.md)). [I]


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

**Not tested:** regenerating `SPEC.md` from this memlog (which should keep the two-tag content); re-running Story Breakdown after the change; the Developer agent (`bmad-agent-dev`) actually performing the handoff instead of a script or a `bmad-spec` run. [?] → Later: Story Breakdown re-run done (5f). Regenerating from this memlog and the agent-persona handoff are still untested.


### Experiment 5f — Story Breakdown re-run after the change (2026-09-20, Carl answered, done)

**Purpose:** close the loop from 5e: `stories.yaml` in `lab5-route` was stale after the spec change. Story Breakdown was re-run on the spec folder (saved copy of the old file: `labs\lab5-route-stories.before-rebreakdown.yaml`). Prediction written beforehand: it proposes the same four stories with only story 3 changed, and asks about checkpoints again. [V-lab setup]

**Step 1 (101 s): it proposed and asked, writing nothing.** It proposed the same four stories with only story 3's description changed (adds "or carrying both of two given tags", AND, three or more rejected, the open API-shape question applies), noted that no `stories/` spec files exist so no ids are pinned, and offered a **five-story alternative** that would split story 3 into single-tag and two-tag filters. It asked two questions: which list, and whether to carry the old checkpoint values and story-4 dispatch note forward "rather than my defaulting them". Prediction confirmed, plus the alternative I had not predicted. [V-lab]

**Carl's answer (verbatim):** "4 stories, carry the checkpoints forward".

**Step 2 (138 s): written and verified.** [V-lab]
- `stories.yaml` differs from the old file in one hunk: story 3's description. Stories 1, 2 and 4, and every checkpoint value including story 4's `spec_checkpoint: true` and its "removeNote doesn't exist yet, add it first" note, are byte-identical. It checked this by diffing and logged the check.
- Schema check PASS (four quoted ids, unique and prefix-free, no `status` field). Three memlog events: re-derived, schema check, byte-identity check.
- It said `git diff` could not verify the file because my lab setup excludes `_bmad-output/` from git, so it diffed against the previous content instead. That is an artifact of my setup, and it reported it honestly. [V-lab]
- It stated that one open question gates the next story: whether the two-tag filter is a separate function or one parameter taking one or two tags. The approved proposal had said it must be answered before story 3 starts; it does not block story 2. [V-lab]

**The whole change loop, as observed (Experiments 5, 5e, 5f):** spec and stories (Experiment 5) then requirement change, then correct-course proposal (Experiment 5), then `bmad-spec` update using the proposal (5e), then Story Breakdown re-run (5f). Each step asked the human only what it needed, changed only what the previous step made stale, and flagged what it left alone. This matches the docs' requirement-change path (update the spec, re-run Story Breakdown; [flow.md](flow.md)) and the "Learn and adjust" stage. [V-lab; V, P3, P7]

**Human effort for the loop:** 13 answers from Carl in total across Experiments 5 to 5f (slug; express; leave questions open; story shape; checkpoints; scope placement (a); change picked (1); batch mode; Continue; approve; the normalize answer; 4 stories; carry checkpoints). About 20 to 30 minutes of skill runtime in the interactive paths, excluding the true re-derive.

**Not tested:** building any of the stories. The loop from spec to code after a change is Experiment 2's territory, not repeated here. [?] → Later: all four built in 5h.


## Follow-ups with Carl's answers (2026-09-21)

Carl answered the questions the earlier headless runs had left open, through the relay method (each question quoted to him, his answer passed back verbatim). **A tooling mistake of mine:** in these runs I passed the tool allow-list through an unquoted shell variable, which split it and produced "Ignoring --allowedTools rule" warnings; `uv run` was then blocked in the session that hit it (a run reported "`uv run` is blocked in this session; `python` runs the same scripts fine") while the runs still completed. Results were not affected as far as I can tell, but a later run used a quoted array. [V-lab]

### Experiment 3, patch menu ("apply all") (Carl chose option 1)

Both flawed-commit labs (`lab3-quick`, `lab3-thorough`) resumed at the menu "apply every patch, or walk through each". **Apply all worked in both**, in 63 s and 49 s. [V-lab]

| | Quick lab | Thorough lab |
|---|---|---|
| Patches applied | 7 | 6 |
| Tests after | 10 pass, 0 fail (was 3 pass, 1 fail) | 8 pass, 0 fail (was 3 pass, 1 fail) |
| `qty` guard, coupon-lookup guard, non-mutating discount | Fixed | Fixed |
| Per-item rounding | **Patched** (rounds once per line; `333 x 10` with SAVE10 gives 2997) | **Deferred**, untouched |
| `applyDiscount` exported without validation | Left exported, **deferred** to the human | **Removed from the exports** (patch 5) |
| The assert-free "coupon works" test | Replaced by 7 real cases | Now asserts 900, plus SAVE25, unknown coupon, omitted coupon, non-mutation |

- The two runs made different calls on the same underlying findings (rounding: patch versus defer; the exported function: defer versus unexport). Consistent with the triage variance seen before. [V-lab; I]
- Nothing was committed. Each run then reached a **new menu**: "Start the next story, Re-run code review, or Done". I did not answer it. [V-lab]
- The runs applied patches without a spec file, so they skipped the spec status and sprint sync steps ("no spec file"). [V-lab]

### Experiment 4, project context, answered (Carl's answers: none; don't know; current; don't know; don't know)

Answers were mapped in the order asked: rules regardless of the repo (none), outside documents (don't know), Node version (current), where planning documents and tickets live (don't know), whether an agent has gotten something wrong here (don't know). [V-lab]

- **The skill proposed a block and asked for approval before writing (118 s).** It said the interview "returned nothing new". The block: a one-paragraph orientation, plus two convention lines: throw `NoteError` with an `E_*` code and never a bare `Error`, and the store is injected so `src/notes.js` never touches the filesystem. [V-lab]
- **What it left out, with reasons:** policy (none brought), a file map ("a map costs every session and saves no search"), the test command (`package.json` already states it), and pitfalls. On pitfalls it said it had found that a `node --test` glob matching nothing reports "0 tests" with no failure, but that it "manufactured that by running a deliberately non-matching glob; a constructed trap isn't evidence, so it stays out". That is the docs' rule that a pitfall needs evidence, applied to its own finding. [V-lab; V, P24]
- **It asked one more question:** whether to also create a `CLAUDE.md` containing `@AGENTS.md`, since it could not verify the harness reads `AGENTS.md` natively. Carl approved the block and said yes to the `CLAUDE.md`. [V-lab]
- **Written (17 s):** `AGENTS.md` (exactly the approved block) and `CLAUDE.md` (`@AGENTS.md`), both untracked and not committed. It said committing is the human's to run. It noted that rules repeating across projects belong in global config, and that Carl's `~/.claude/CLAUDE.md` already carries those, so it had read the global file. [V-lab]
- **Compared with the planted conventions:** the block records 2 of the 5 (`NoteError` codes, injected store); the other three (tests in `tests/*.spec.js` with `node:test`, `nN` ids, exports at the bottom) are discoverable from the code, and the skill judged them not worth a line. Its docs-stated rule is to include only what is expensive to rediscover. [V-lab; V, P24]
- **Not yet tested:** whether a later build in this repo behaves differently with `AGENTS.md` present. Experiment 4's build without it followed 5 of 5 conventions and asked nothing, so a difference would be small. [?] → Later: Experiment 4b. The code was the same; review escalated a finding it had previously deferred.

### Experiment 5g, open questions answered and applied to the change-loop spec

In `lab5-route` (the spec after the requirement change, routed through `bmad-spec`), Carl answered three of the open questions. [V-lab]

- **API shape ("single parameter", 293 s):** one constraint was added ("filtering is a single operation that takes its one or two tags in one parameter; there is no separate two-tag function"), the question was dropped, and the other sections were left untouched. It flagged story 3's closing sentence ("the open API-shape question applies") as now false and offered a Story Breakdown re-run. Open questions: 8. [V-lab]
- **Lowercase = normalize, and removing a tag the note lacks = no-op (76 s):** CAP-1's success now includes uppercase input being lowercased and stored; a new constraint and CAP-2's success state the no-op; and the first answer opened a new question ("if someone removes or filters by `Work`, does it match a stored `work`?"). Story 1's "the open case question still applies" and story 3's API-shape sentence are both stale; the skill left `stories.yaml` alone and offered a re-run. Open questions: 7. [V-lab]
- Each answer changed the spec surgically and left the memlog with a record, as in 5c and 5e. [V-lab]

**A correction to something I told Carl:** I said building story 2 needed only open questions #2 and #4. That was wrong. Story 2 (remove a tag) depends on story 1 (tag storage and add), which does not exist in the code yet, and the stories run in order. Story 1 needs #3 (adding a tag the note already carries), #5 (which `E_*` codes), and #6 (which characters are legal), on top of #2 already answered. [V-lab; my error]


## Experiment 5h — all four stories built interactively (2026-09-21 to 2026-09-23, done)

**Purpose:** finish the loop Experiments 5 to 5g left at "spec, stories, requirement change, correct-course, spec update, stories re-run": build every story of the tags epic (`lab5-route`) through `bmad-build`, with Carl answering every open question and checkpoint through the relay method. Also resolved several open questions the earlier experiments had left standing. [V-lab]

**Method note:** each story ran as multiple headless `claude -p --continue` calls per story (plan, question round, approval, implement/review/present), same relay discipline as before — every BMAD question relayed to Carl verbatim, every answer passed back verbatim, nothing chosen on his behalf. A run I killed with too short a timeout during story 3's review step left implementation and tests fully done (61/61 later, 47/47 then) with only the review step interrupted; resuming with no timeout cap picked up cleanly at `status: in-review`, confirming the build spec's status field is safe to interrupt against. [V-lab]

**Open questions Carl answered along the way, applied through `bmad-spec` before building (not by hand-edit, learning Experiment 5b to 5e's lesson):**

| # | Question | Answer |
|---|---|---|
| — | Two-tag filter: separate function or one parameter | single parameter |
| — | Tags are lowercase: reject or normalize | normalize |
| — | Removing a tag the note doesn't carry | no-op |
| — | Adding a tag the note already carries | idempotent no-op |
| — | New `E_*` codes: new or reuse | new, one per failure |
| — | Characters beyond lowercase+length | exactly lowercase letters, digits, hyphens (ASCII) |
| — | Filtering by the same tag twice | single-tag case |
| — | (Story 3) function name/signature | `listNotesByTag(store, tags)`, bare string or array |
| — | (Story 3) does filter lowercase `Work`→`work` | yes, symmetric with add/remove |
| — | (Story 3) duplicates collapsing to 1–2 distinct tags, and `[]` | collapse first, check distinct count; `[]` rejected |
| — | (Story 3) third error code name | `E_FILTER_ARITY` (also covers the `[]` case) |
| — | (Story 4) unknown note id on remove | `E_NOT_FOUND` (not idempotent) |
| — | (Story 4) what a successful `removeNote` returns | `undefined` |

Each answer went through `bmad-spec`'s update path and landed in the memlog, matching Experiment 5e, not 5b's hand-edit route. Two of Carl's answers ("new codes", "digits, hyphens") were incomplete on their own terms, and the skill would not fill the gap itself — it opened a follow-on question each time (naming the codes; whether non-ASCII letters count) rather than guessing. [V-lab]

**Story Breakdown was re-run twice** as the spec changed (once after the API-shape/case/no-op answers, once more not needed — the token-code and character answers didn't touch story descriptions). Each re-run asked to confirm the story list (it proposed the same stories with only the stale sentence fixed) and whether to carry the checkpoints forward; Carl said yes both times, and the diff really was single-hunk each time, verified. [V-lab]

**All four stories, committed to the lab repo in order (`72dce13`, `2248ecf`, `ce33364`, `7ab412b`):**

| Story | Route | Human decisions before implementation | Findings (patch/false-or-rejected/deferred) | Tests after |
|---|---|---|---|---|
| 1 Tag storage and add | dispatch | Code names (2), checkpoint carry-forward | 3 patched / rest rejected | 18/18 |
| 2 Remove a tag | dispatch | Case symmetry, malformed-input handling (2) | 2 real gaps patched / 11 rejected | 28/28 |
| 3 List notes by tag | dispatch | Signature, case, duplicate/arity, code name (4) | 3 patched / 10 rejected | 47/47 |
| 4 Remove a note, tags with it | dispatch | Token-count accept, unknown-id behavior, return value (3) | 2 patched / 4 rejected / 2 deferred | 61/61 |

All [V-lab]. Every story took the `dispatch` route (none was small enough for `oneshot`), matching the release's route gate ([build-step-by-step.md](build-step-by-step.md)).

**Findings across the four builds**

- **Every checkpoint fired as documented, every time.** Dirty-tree checks (story 2's build halted immediately when story 1's work was uncommitted, and asked how to proceed — not scripted wording, the model's own judgment call at an unscripted checkpoint), subagent-permission asks (once per workflow run, as `SKILL.md` prescribes), approval checkpoints (all three options offered every time), token-count gates (story 4, over 1600, Carl chose to accept). None were skipped. [V-lab; V, P18r]
- **The commit step is the one place "confirm before committing" bites on every single story.** Each story's presentation step said it would normally commit locally and then didn't, correctly attributing this to Carl's standing rule rather than to a workflow default. Commits were made by me, as a person, after Carl approved each message — not by the skill. [V-lab]
- **Cross-story consistency held without being asked to.** Story 2 and 3 both independently proposed lowercasing input to match `addTag`, framing it as "symmetric with add/remove" before Carl answered. Story 3's implementation reused `addTag`'s validation regex rather than reinventing one. [V-lab]
- **The same finding was raised three separate times by three separate review runs and rejected each time on the same grounds** (a note with a non-array `tags` field would substring-match a filter) — and the build itself flagged this pattern to Carl unprompted, naming it as the most likely place its own reasoning could be wrong. This is a review behavior not observed in Experiments 2 or 3: a system noticing its own repeated dismissal of a finding and surfacing that as a signal, rather than just repeating the dismissal. [V-lab]
- **The deferred finding across stories (`nextId` reissuing a deleted note's id) was verified empirically before being filed**, with a concrete repro in `deferred-work.md`: create n1/n2/n3, remove n3, add a new note, and the new note gets id `n3` — then `getNote(s,'n3')` silently resolves to the new note. This is the planning-stage prediction from stories 1 and 2 made concrete once `removeNote` existed to trigger it. It was correctly barred from being fixed inside story 4 by the frozen spec's Never clause. [V-lab]
- **Design Notes and Deferred Work as a paper trail:** the id-reuse issue is recorded in three places by the end (spec Design Notes from story 1 onward, the story 4 spec, and `deferred-work.md`) with increasing precision each time, never resolved and never silently dropped. [V-lab]

**What the finished epic demonstrates, end to end:** idea and constraints (Experiment 5) → express spec + Story Breakdown → requirement change mid-epic → correct-course proposal → change routed through `bmad-spec`, not hand-edited (Experiment 5e) → Story Breakdown re-run → four stories built one at a time, each gated by real human decisions, each reviewed by independent subagent layers, each committed only on explicit confirmation → one real bug found and left properly documented rather than smoothed over. This is the "one toy idea through the flow" success criterion (criterion 3) met at full scale rather than the wordfreq-CLI scale of Experiment 2. [V-lab]

**Not tested:** `bmad-retrospective` on the finished epic (a natural next unit; → Later: Experiment 5i); `bmad-walkthrough`, which was offered at every story's end and never taken.


## Experiment 4b — does `AGENTS.md` change a build, once it exists? (2026-09-23, Carl answered, done)

**Purpose:** the follow-up Experiment 4 left open. `labs\lab4-context` already had `AGENTS.md`/`CLAUDE.md` approved and written in Experiment 4 but never committed; `labs\lab4-build` had already built the same request without any context file. Ran the identical request in `lab4-context` — "Add `removeNote(store, id)` ... An unknown id must fail" — to compare against the un-primed build. [V-lab]

**Setup wrinkle, itself a finding:** the run halted at step 1's version-control check before doing anything, because two *untracked* files (`AGENTS.md`, `CLAUDE.md`, sitting there since Experiment 4's approval) were enough to fail the "is the working tree clean?" gate — no tracked file needed to be modified. This is the first observed case of the dirty-tree checkpoint firing on untracked-only state; every prior instance (Experiment 5h story 2) was modified tracked files. [V-lab] Carl chose to commit the context files first, which was done (`9e3303f`), and the build restarted clean.

**Result: the code came out the same; review's judgment did not.** [V-lab]

| | `lab4-build` (no context, Experiment 4) | `lab4-context` (with `AGENTS.md`, this experiment) |
|---|---|---|
| Route | oneshot | oneshot |
| Reviewer | Blind Hunter | Blind Hunter |
| Tests after | 7/7 | 7/7 |
| Id-reuse finding | Logged to `deferred-work.md` as a pre-existing-adjacent low/medium note, no human asked | **Routed to HALT** — build stopped and asked Carl to decide |

- The underlying bug is identical in both runs: `nextId` takes `max` of currently stored ids, so removing a note and adding a new one can reissue the freed id, and a stale reference then silently resolves to the wrong record. Both reviewers found and verified it the same way (traced through code, reproduced by running it). [V-lab]
- **What changed is the reviewer's own reasoning for why it's non-trivial.** The triage log in this run states the reason explicitly: "a monotonic counter needs somewhere to persist, and `AGENTS.md` pins the store to `{ load(): Note[], save(Note[]) }` with no slot for one." Because a documented contract now existed to weigh the fix against, the smallest-fix test that routes findings to `patch` vs `HALT` ([build-step-by-step.md](build-step-by-step.md)'s triage categories) came out differently: fixing it would mean either violating the pinned contract or changing it, and step-oneshot's own classify rule sends exactly that case to HALT rather than patch. Without `AGENTS.md`, there was no documented contract to violate, so the same underlying tradeoff read as a lower-stakes, deferrable note. [V-lab; V, [build-step-by-step.md](build-step-by-step.md) triage categories]
- **Carl's decision — accept id reuse, document it — was applied as: a comment above `nextId` plus a new test pinning the reissue and the stale-reference resolution**, not a code fix. This is `patch`-shaped work (a test and a comment) that only became visible as a distinct step because the finding was elevated to a human decision first. [V-lab]
- Six other findings in this run's triage: two low patches (weak assertions strengthened), two low rejects (missing arg validation on `removeNote`, matching `getNote`'s existing behavior; three lines of duplicated find-and-throw logic, rejected as matching the file's own idiom), and the stale `AGENTS.md` summary line (still says `addNote`/`getNote`/`listNotes`, omits `removeNote`) correctly deferred rather than fixed inline — `AGENTS.md`, being project context rather than the changed contract, wasn't the target of this build. [V-lab]

**Reading:** project context did not change what got built, and it did not change what review found. It changed which findings become the human's decision to make versus a note left for later — by giving review something concrete to check a fix against. This is a different mechanism than Experiment 5h's repeated-finding self-flag (that was the model noticing a pattern in its own verdicts across separate builds); here a single artifact changed a single verdict, once, by supplying context the reviewer didn't have before. [I]

**Not tested:** whether a stricter or more detailed `AGENTS.md` (naming the id-reuse risk explicitly, or committing to "ids are never reused") would route the finding differently again; whether the same effect holds for findings unrelated to anything `AGENTS.md` states.


## Experiment 5i — `bmad-retrospective` on the finished tags epic (2026-09-23/24, Carl answered, done)

**Purpose:** close the loop on the built epic (Experiment 5h) with `bmad-retrospective`, run interactively via the relay method: opening question, Phase 4 acceptance verdict, and B1's open contract question all answered by Carl. [V-lab]

**Setup:** `labs\lab5-route`'s spec folder, stories mode (`SPEC.md`, `stories.yaml`, `stories/<id>-*.md`, no `sprint-status.yaml`). All four stories `status: done`, committed `72dce13`..`7ab412b`, 61/61 tests green, tree clean. Skipped Phase 3 (team discussion, opt-in and never runs headless) per instruction.

**Opening question, Carl's answer:** weighted the `nextId` id-reuse issue and the token-count gate accepted on story 4.

**Phase 1/2 (gather, analyze): 435-line `RETROSPECTIVE.md`, nothing else touched.** [V-lab]
- Verified epic-wide evidence: each story maps 1:1 to one commit, zero merges, test file append-only (0 deletions across four commits — the four baseline tests are provably untouched), churn reconciles exactly against `git show` at baseline.
- Explicitly recorded what evidence was **missing**, not silently skipped: no per-story session logs exist (`.memlog.md` stops at spec finalization, before story 1 dispatched), no previous retrospective, no PRD/architecture doc, and the untracked spec folder (`.git/info/exclude`) means its history is readable only from the memlog, not diffs.
- Ran `bmad-review`'s three code lenses over the whole `846e9dc..7ab412b` diff, weighted at story boundaries — the first review pass in this project that saw all four stories at once. Its unverified claims were each re-checked against source before being recorded; five that did not survive verification are listed (B8) rather than dropped silently, each with the specific reachability argument that refutes it.

**Findings, in outline (14 total: A1-A7, B1-B7, plus B8's refuted claims):**

- **A1 — the `nextId` propagation history is the finding, not just the bug.** Story 1 verdicted a duplicate-id concern `false` ("no path creates duplicates" — true at the time). Story 2 re-cited that verdict *by reference* without re-deriving it. Story 4 reproduced it empirically. Nothing in the process re-examines a `false` verdict when a later story invalidates the condition it depended on. Also sharper than `deferred-work.md` recorded: reuse is specific to deleting the *highest-numbered* note (a middle delete is safe, verified); emptying the store restarts the sequence at `n1`; and the harm reaches further than a stale read — a stale id lets `addTag` **write** a tag onto an unrelated note, silently.
- **A2/A3/B2/B5 — SPEC.md has drifted out of date in four separate spots**, all traceable to triage decisions in the story artifacts that never wrote back: all five Open Questions were answered in code and never closed in the spec; the character-check order (`SPEC.md` says checked-after-lowercasing, code checks raw input, deliberately, to reject Unicode confusables like the Kelvin sign) is wrong in the spec, in story 1's own frozen bullet, *and* in story 1's commit message — three of four places a reader would look, only the source comment and the triage row are correct; and `SPEC.md`'s "three or more tags is rejected" is literally false for duplicate entries (100 copies of `'work'` is accepted, since arity checks the *distinct* set).
- **A4 — the same duplication finding was rejected three times, each time correctly**, because each story's frozen Never bars touching a previous story's code — a structural gap in the "never touch prior stories" rule, not a reviewer failure. (Corroborates the pattern already logged from Experiments 5h and 4b: the same finding recurring across builds is itself informative.)
- **A6 — every Patch-verdicted fix from all four review passes actually landed** (checked against the real commits, not self-reported) — but the *Implementation Notes* sections describing them went stale twice (story 3 said "28→45 tests", the commit has 47; story 4 said "47→60", the commit has 61), while every commit *message* had the correct counts the whole time. The artifact meant for the next story to read is the one that didn't get updated after review.
- **A7 — the deferred `nextId` bug was pinned by a test as if it were intended behavior**, with no marker distinguishing "this documents a known defect" from "this is the spec." Whoever eventually fixes it must find and invert that test.
- **B1 — the epic's most serious finding, found independently by two review lenses, reachable through the public API, silent.** `listNotesByTag` and two no-op paths return live store objects; a caller can mutate a note's tags directly through the returned reference, bypassing the character rule and the 5-tag ceiling with no error and no `save()` call. Traced to five exits total, not the three the new stories added — `getNote` and `listNotes` (the widest, returning the live array itself) are pre-existing and were already aliasing before the epic began. **What changed the risk, not the code:** before this epic a note held only scalar fields, so aliasing leaked one field; story 1 added a mutable array, and story 3 then handed that array out by reference from a fourth entry point. Neither story was locally wrong; neither saw the compound effect. Also asymmetric within one function: `addTag`/`removeTag` return a fresh copy on their success paths but the live object on their no-op paths.
- **B4 — the two remove functions disagree on idempotence** (`removeTag` on an absent tag is a silent no-op per an explicit spec constraint; `removeNote` on an absent id throws, matching `getNote`) — both individually correct, never reconciled because the decisions were two stories apart.
- **B6 — proved by mutation testing, run live during the retrospective itself.** Rewriting `addTag`'s copy-on-write save to mutate in place: 61/61 tests still passed. The same rewrite on `removeNote` (which already has the guard story 4 added) failed exactly one assertion. Only one assertion in 515 lines of tests checks that the pre-call array itself wasn't touched, and it exists only because story 4's reviewer happened to invent that test shape — nothing revisited stories 1 and 2 once a better test existed.
- **B7 — a stated, testable spec line ("three distinct new error codes") is asserted nowhere.** The three codes appear 25 times across the test file, always as an individual expected value, never compared to each other. A refactor that collapsed two of them would pass all 61 tests.

**Machine verdict: `accepted-with-open-items`.** All CAP success criteria met and independently verified by direct execution (not just the test suite), the approved two-tag change is exercised, zero test deletions across the epic. Two findings could reasonably argue for `rejected` instead (B1, A1), both stated plainly with the argument each way; both are barred from this epic's own scope by a frozen Never clause. Carl rendered `accepted-with-open-items`, matching the machine verdict — no override. [V-lab]

**Action items: 16 proposed, none applied** (remediation R1-R5, spec reconciliation S1-S4, process P1-P6), each with a source finding and "Carl (proposed)" as owner. Stories mode forbids the retrospective from editing `SPEC.md`, `stories.yaml`, or story files itself — the whole list is a *proposal* document, same non-tinkering discipline as `bmad-spec`. [V-lab]

**Carl's decision on B1's open question, after the retrospective run:** "that is a defect to fix." The retrospective had explicitly left this as a contract question it could not settle itself ("is B1 a defect or the contract?" — story 3's AC-3 currently *requires* the aliasing). This decision authorizes R1 (copy on return at the three new-story exit points) and implicitly puts R1b on the table too: R1b's honest note is that R1 alone "does not close B1" — `getNote` and `listNotes` are still open, and closing them means renegotiating story 1's frozen Never clause, not just adding code. **Not yet acted on** — recorded as Carl's decision here, in our own wiki record, rather than by hand-editing the finalized `RETROSPECTIVE.md` (same non-hand-edit discipline as `bmad-spec`'s artifacts). Implementing R1/R1b would be a natural next unit, and would need Carl to explicitly renegotiate story 1's Never rule before R1b could proceed under BMAD's own process, not just under this record.

## R1/R1b — fixing retrospective finding B1 (2026-09-24/25, Carl answered, done)

**Purpose:** act on Carl's decision after Experiment 5i ("that is a defect to fix") and implement R1/R1b — the only retrospective action item taken from proposal to committed code. Run in `labs\lab5-route`, relay method throughout. [V-lab]

**Renegotiating the frozen Never clause.** R1b required overriding story 1's frozen "Never change `addNote`/`getNote`/`listNotes`" and reversing story 3's AC-3 identity assertion (`tests/notes.spec.js:354`) — both explicitly named in the intent as Carl's decision, not the build's judgment, per the "no escape hatch in a frozen Never" gap Experiment 5i's process findings (P4/P5) had already flagged as unresolved. [V-lab]

**Step-02's route gate found two more leaking exits than the human-authored intent named.** The intent (mine, from Carl's B1 read) listed five exits, matching the retrospective's count. During design, step-02 found `addTag` and `removeTag` also return the live store object on their *success* paths (`const updated = { ...note, ... }` saved into the store and then returned) — a sixth and seventh leak, not counted in B1 and not caught by either of Experiment 5i's two review lenses. Relayed to Carl verbatim; his answer, "split and fix all seven," resolved into two parts: *split* narrowed this build's own spec to the five originally-named exits (a token-count-adjacent scope decision), *fix all seven* committed to a follow-up build for the other two — both stated back to Carl before proceeding, unqueried. [V-lab]

**Build 1 (`spec-b1-defensive-copy-on-return.md`, commit `d3c526c`):** one `copyNote` helper, applied at the five named exits (`getNote`, `listNotes`, `listNotesByTag`, `addTag`/`removeTag` no-op paths). 70/70 tests pass (12 new). Clean at every checkpoint (dirty-tree, approval, no token-count split needed after the intent narrowed). [V-lab]

**An eighth exit, found by all three review layers independently, not by any human or by me.** `addNote` itself does `store.save([...notes, note]); return note;` — the same defect, pre-existing, present before the epic even started. None of B1's five named exits, the step-02 gate's two, Experiment 5i's two review lenses, or my own read of the retrospective had counted it. The build correctly left it unfixed (Carl's override named only `getNote`/`listNotes`) and logged it to `deferred-work.md` with a reproduction, rather than silently patching or silently dropping it. [V-lab] **This is the third instance in this project of a scope statement (human- or machine-authored) undercounting the actual defect surface, each caught by a different mechanism** — Experiment 5i's B1 undercounted at the retrospective stage (two review lenses missed the pre-existing `getNote`/`listNotes` aliasing until asked to look epic-wide), the step-02 gate undercounted again on the same finding at build time, and now review undercounts a third time on the same finding during implementation. Three independent looks at the "same" defect, three different exit counts, before the real number (eight) surfaced. [I]

**Follow-up (`spec-b2-defensive-copy-remaining-three-exits.md`, commit `ed2c9c0`):** Carl chose to fix all three deferred exits (`addTag`/`removeTag` success paths plus `addNote`) in one build. Hit the dirty-tree checkpoint on its own not-yet-flushed output-redirect file (`b2-followup.out`, 0 bytes, created by the very process running the check) — it reasoned aloud that the file matched the shape of a stray from a prior attempt but that "I didn't create it, so I won't delete it silently," and asked. Carl: leave it in place. 76/76 tests pass (6 new). All seven of B1's originally-enumerated exits, plus the eighth, are now closed across the two commits. [V-lab]

**A ninth defect found and deferred, out of scope, during B2's review:** `addTag`/`removeTag`'s *write* path mishandles a non-array `tags` value — a stored string spreads into individual characters, and the duplicate check substring-matches instead of exact-matches. Pre-existing from story 1, unrelated to copy-on-return, reproduced and logged rather than fixed. Two review lenses (edge-case, verification-gap) caught it on B2's first pass. [V-lab]

**Reading:** a defect that looks fully enumerated after a careful human read, a retrospective with two independent review lenses, and a scope-negotiation gate can still be undercounted — each additional look (build-time design, then implementation-time review, twice) found something the previous look missed, and every miss was caught by a different mechanism rather than the same one working harder. Nothing here contradicts [systemic-findings.md](systemic-findings.md)'s "context changes escalation not detection" pattern; this is closer to it, but the mechanism differs — the misses here are actual exit-count omissions, not a documented-vs-undocumented triage split. [I]

**My own process error, corrected in the moment:** after the first build (B1) completed, I checked its output file's existence from the wrong working directory (a `cd` chained before a backgrounded `&` command backgrounds the whole compound statement, not just the tail command, so my own shell's `pwd` never moved) and concluded, wrongly, that the build hadn't started. I sent a redundant second `--continue` call, which is what actually surfaced the "commit or follow-up build?" question relayed to Carl — the real build had already finished cleanly underneath. No data was lost; the mistake was in my own bash-scripting, not in BMAD. [V-lab]

**Process observations of note for the wiki itself:**
- The retrospective ran a genuine cross-story `bmad-review` pass and found a defect (B1) that no single story's review — each scoped to one diff — could have surfaced. This is a different mechanism than Experiment 4b's context-driven triage shift or Experiment 5h's self-flagged repeated-rejection pattern: here the artifact itself (all four stories' combined diff) is what a single-story review structurally cannot see.
- The retrospective caught its own limits and said so: Carl's second going-in concern (the token-count gate) had no artifact trail anywhere in the project, so it was recorded as "a user-reported process observation, not a sourced finding" rather than invented evidence to satisfy the concern. This matches the skill's stated rule: "a claim you cannot point at ... is not a finding. Drop it." [V-lab; V, retrospective SKILL.md]
- Six of the sixteen action items are pure process lessons about the workflow's own mechanics (P1-P6) — a checkpoint with no completion condition, a `false` verdict with no expiry condition, no backfill mechanism for a newly discovered test shape, no write-back from review to Implementation Notes, no escape hatch in "never touch a prior story," no requirement to log a triage decision that changes stated mechanism even when behavior matches intent. None of these are about the code; all are about gaps in BMAD's own process as currently specified, discovered by running it for real across a full epic.

## Experiment 8 — add-on setup + TEA (2026-09-26, done)

**Purpose:** NGA runs core/BMM plus three add-on modules (TEA 1.26.0, BMB 2.2.2, CIS 0.3.2 — `STATE.md`, Carl's manifest read). Install the same three into a fresh copy of `lab5-route` (`labs\lab8-tea`, `lab5-route` itself untouched) and read TEA's own files, since none of it lives in the core `BMAD-METHOD` repo already pinned. Then ask whether TEA would have caught retrospective finding B1 and how it sits next to `bmad-build`/`bmad-code-review`. [V-lab]

**Add-on modules are not in the core repo; `docs/customize/add-modules.md` (P27, read at the pinned tag) names them as separately versioned, separately released packages** — BMB (`bmad-builder`), CIS (`bmad-creative-intelligence-suite`), TEA (`bmad-method-test-architecture-enterprise`), each with its own npm package and GitHub repo. [V, P27]

**A real version-pin surprise, resolved.** Checking npm's published version lists for the three packages before installing found TEA topping out at 1.27.2 (1.26.0 does exist further back in the list — fine), but BMB (`bmad-builder`) topping out at only **1.1.0** and CIS (`bmad-creative-intelligence-suite`) at only **0.1.9** — nowhere near NGA's reported 2.2.2 and 0.3.2. Before concluding NGA's manifest was wrong, tried the installer's own `--pin CODE=TAG` flag (`docs/customize/add-modules.md`, P27) against exactly those versions: `npx bmad-method install --action update --modules bmm,tea,bmb,cis --pin tea=v1.26.0 --pin bmb=v2.2.2 --pin cis=v0.3.2`. **All three installed clean, no error, no fallback.** The generated `manifest.yaml` shows why: each external module carries `source: external`, `channel: pinned`, and a git `sha` — `--pin` resolves against **GitHub tags on the module's own repo**, not against the npm registry entry `add-modules.md` links to. npm's published copy of `bmad-builder` and `bmad-creative-intelligence-suite` is far behind their GitHub tags; TEA's happens to track closer. **Lesson for the wiki and for anyone else checking an add-on module's currency: check the module's GitHub tags (or `manifest.yaml` after an install), not its npm page — the two can disagree by a major version.** [V-lab]

**A second installer wrinkle, caught before it produced a false negative:** running the install without `--action update` against an already-initialized `_bmad/` (the copied `lab5-route` state) silently defaulted to **quick-update** under `--yes` non-interactive mode, per `add-modules.md`'s own documented behavior ("Refreshes installed modules from their recorded sources" — it does not add new ones). That first attempt reported success and touched only `core`/`bmm`; TEA/BMB/CIS were never installed. Re-run with an explicit `--action update` (full update, re-runs module selection) succeeded. A non-interactive add-on install onto an existing project needs `--action update` stated explicitly — the default action is a plausible trap. [V-lab]

**What TEA actually is, once installed: one persona-first skill (`bmad-tea`, "Murat"), not nine standalone workflow skills.** `add-modules.md`'s marketing copy ("an agent and nine workflows") undersells the shape: `bmad-tea/SKILL.md` is an agent activation sequence (resolve persona → greet → present menu) structurally close to `bmm`'s five thin agent personas (P22), but here the *whole module* is one agent whose menu dispatches to eight separate `bmad-testarch-*` skill directories (TD/TF/CI/AT/TA/RV/NR/TR) plus a ninth, `bmad-teach-me-testing` (TMT), with its own multi-session curriculum. `GATE` is a tenth menu code that is a routing *prompt*, not a skill — it tells the agent which of RV/NR/TR to sequence, never merging them. 54 skills total after install (29 core+bmm, 8 testarch workflows + `bmad-tea` + `bmad-teach-me-testing` = 10 tea, and BMB/CIS accounting for the rest). [V, P28]

**Test Review's (`RV`) criteria registry is deterministic and severity-pinned, unlike anything else read in this project.** `steps-c/criteria-registry.md` fixes a severity per criterion in a table (never chosen by the reviewer), gates each row as Absolute / Applicability / Convention, and states explicitly that a repo-wide bad habit earns the *same* violation on every file rather than a waiver — the opposite of `bmad-build`'s and `bmad-code-review`'s LLM-judgment triage (patch/reject/HALT, no fixed severity table observed anywhere in [build-step-by-step.md](build-step-by-step.md)). **Every one of its ~35 rows is about the test file's own construction** — disabled/focused tests, tautological or unreachable assertions, hard waits, shared-state leakage, shape-only assertions, Playwright/Pact convention adoption, Maestro mobile-flow patterns. **None inspect the production code under test.** [V, P28]

**Would TEA have caught B1? No — not through any workflow read.** B1 (functions returning live store objects, letting a caller mutate a note past validation through the public API) is a production-code encapsulation defect, not a test-file defect, and none of the three workflows examined operate on that axis:
- **`RV`'s registry has no row for reference aliasing, mutation-through-return, or defensive copying** — confirmed by grepping `bmad-testarch-test-review` and `bmad-tea`'s knowledge base for "alias", "mutat", "shared reference", "defensive copy", "encapsulat": every hit was GraphQL "mutations" or unrelated. The registry's closest row, H10 (shape-only assertion — an assertion checks type/presence but not value), is about a *wrong value* passing unnoticed, not about a *live reference* passing unnoticed; B6 in the retrospective (only one assertion in 515 lines pins that the pre-call array wasn't the same reference) is exactly the gap H10 does not reach, because reference identity is never a value in the sense H10 means. [V-lab]
- **`TR`'s gate decision (`step-05-gate-decision.md`) is arithmetic over a requirements-coverage matrix** (P0 must be 100%, P1 ≥90% for PASS, overall ≥80%), deliberately deterministic ("severity is read from a table, never chosen" has a direct analogue here: "gate decision MUST be deterministic"). It can only report a gap for a **named requirement**. B1 was never a named requirement anywhere in the tags epic's `SPEC.md` — "returned notes must be immutable" was never a capability, so there was nothing for Trace to mark uncovered. A coverage gate cannot find a gap in a list that was never written. [V, P28]
- **Test Design's (`TD`) knowledge base**, which runs earliest (risk-based planning, before code), was grepped for the same terms with the same null result — its risk vocabulary is web/API/mobile testing risk (network flakiness, auth negative paths, contract drift, CI parallelism), not backend encapsulation risk. Not read in full; a skim of the knowledge index and a targeted grep, not a claim that no fragment anywhere mentions it. [V-lab, partial]

**How TEA fits next to what this project already knows about the build/review loop:** `bmad-build`'s own review layers and `bmad-code-review` examine the diff for correctness defects (this is where B1 was actually found, twice — Experiment 5i's cross-epic `bmad-review` pass, and originally by "two review lenses" per the retrospective). TEA's RV/TR examine a different pair of things entirely: whether the *tests themselves* are trustworthy (RV) and whether *documented requirements* have test coverage (TR) — not whether the code has the defect a good test would have to specifically be written to catch. The three are complementary, not overlapping: none of them would have substituted for either of the other two on this project's own evidence so far. A B1-shaped defect only becomes visible to TEA the moment "returned notes are immutable" is written down as a requirement — which, per [spec-skill.md](spec-skill.md)'s own Spec Law rule 5 ("success signal concrete enough to test or demo"), is a `bmad-spec` gap upstream of TEA, not a TEA gap. [I]

**Not tested:** actually running any TEA workflow interactively (TD, TF, RV, or TR) against `lab8-tea`'s real code and tests — this unit stayed at "read the files and reason about what the criteria/gate logic covers," a static read like Experiments 1's skill-load check rather than a live run like Experiment 2 onward. A live `RV` run against `notes.spec.js` would confirm or correct the "no row fires" reading empirically. BMB and CIS were installed and pinned successfully but not read or exercised at all — reserved for Experiments 13 and 14 per the queue. `bmad-teach-me-testing`'s curriculum, and six of TEA's eight workflow skill bodies (TD, TF, CI, AT, TA, NR), were not opened.

## Experiment 9 — cross-epic frozen test (2026-09-27 to 09-29, done, interactive with Carl)

**Question:** within one epic, a story's frozen Never clause protects earlier stories' code (Experiments 5h, 5i). Across epics, does it? A second epic's story must change a function the first (tags) epic built and froze. Does the new spec or story freeze the old code, does `bmad-build` refuse, ask, or just edit it, and does anything flag the conflict with the first epic's `SPEC.md`?

**Setup:** `labs\lab9-crossepic`, a copy of `lab5-route` at `ed2c9c0` (tags epic finished, B1 fixed; `lab5-route` untouched). Second-epic intent: rename a tag across all notes (`renameTag`), and let tags contain underscores (`q3_2026`). The underscore half directly contradicts a tags-epic constraint (underscore explicitly rejected, story 1's frozen `addTag` rules, `TAG_PATTERN`). Relay method: Carl answers every BMAD question.

**Predictions (written before the first run):**
1. `bmad-spec` opens a new spec folder rather than updating `spec-note-tag`, and asks for a slug. [prediction]
2. It notices the underscore rule contradicts `spec-note-tag/SPEC.md` only if it reads that spec; I expect it to mention it (it found an existing change proposal unprompted in 5e), maybe as an open question. [prediction]
3. Nothing in BMAD enforces a frozen block from another epic's story file: `bmad-build` for the new story edits `addTag`'s validation without refusing, though its review or investigation may flag the old story's frozen text or the old `SPEC.md` as stale. [prediction]
4. The old `spec-note-tag/SPEC.md` is left saying underscores are rejected; no skill updates it. [prediction]

**Spec and story stage (relay method; Carl's answers verbatim):**

| Step | BMAD asked | Carl | Time |
|---|---|---|---|
| 1 | Update `spec-note-tag` (recommended) or new folder; rename vs "renaming or merging" non-goal; underscore everywhere or rename-only; uncarried `from`; express/guided | go with recommendation; drop both; everywhere; raise an error; express | 161 s |
| 2 | (CAP-5 written) which error code; return value; re-run Story Breakdown?; story 1's frozen lines now false, flagged not edited | existing; return the note | 337 s |
| 3 | which existing code; "the note" has no referent for a multi-note rename; Story Breakdown?; edit the frozen story-1 lines or leave flagged? | E_NOT_FOUND; array of every changed note; yes; edit as needed | 104 s |
| 4 | (edited frozen story 1 and 3 lines, left both Review Triage Logs untouched as history; fixed two SPEC.md wording errors unasked) two stories or one?; checkpoints per story | two stories; carry the checkpoints forward | 257 s |
| 5 | "carry forward" has nothing to carry for new stories: A (1–3 shape) or B (gate story 6 like story 4)? | A | 39 s |
| 6 | (wrote stories 5, 6) disclosed it went past confirmed scope: edited two shipped stories' descriptions | — | 117 s |

**Findings so far:** [V-lab]
- Prediction 1 wrong: `bmad-spec` recommended updating the existing epic's spec, not opening a new one, because a second spec would disagree on what a legal tag is. Carl accepted, so this became an in-epic change to a finished epic rather than a true cross-epic test. The cross-epic question itself (does another epic's freeze apply?) remains untested.
- Prediction 2 confirmed, more strongly than expected: it read the shipped spec, named the exact contradicting constraint and non-goal lines, and mapped the blast radius of the shared `TAG_PATTERN` to three shipped entry points before writing anything.
- **Frozen block handling:** it flagged story 1's falsified frozen lines twice and would not edit them until Carl explicitly said to. Once authorized, it edited the contract lines but refused to touch the Review Triage Logs ("rewriting them falsifies history rather than fixing a contract").
- It refused to invent a value from an ambiguous answer three times ("existing" named no code; "the note" had no referent; "carry forward" had nothing to carry for new stories).
- It overstepped once and disclosed it: edited two shipped stories' descriptions after three prior runs had left them byte-identical, and offered to revert.
- Carl: keep the two description edits. Stories 5–6 left unbuilt in `lab9-crossepic`. Re-running the true cross-epic version as **Experiment 9b** in a fresh copy, with Carl's instruction that the second epic gets its own new spec folder.

### Experiment 9b — same intent, forced into a new spec folder (2026-09-28)

**Setup:** `labs\lab9b-crossepic`, fresh copy of `lab5-route` at `ed2c9c0`. Same two-item intent as 9; Carl's up-front instruction: new epic, its own spec folder. Predictions 3 and 4 from Experiment 9 carry over unchanged.

| Step | BMAD asked | Answer | Time |
|---|---|---|---|
| 1 | slug; express/guided; conflict with spec-note-tag: (a) supersede + adopt as companion, (b) stand alone, (c) other; listed 10 gaps | Carl asked for suggestions; Claude drafted answers reusing Experiment 9's (slug `tag-rename`, express, (a), dedupe merge, `E_NOT_FOUND`, array of changed notes, underscore everywhere, all-or-nothing, no new codes); Carl: "Go with suggestions" | 32 s |
| 2 | (my first relay was truncated to "Go" by a PowerShell quoting bug) it refused to treat "Go" as answers and re-asked | resent in full | 11 s |
| 3 | (wrote `spec-tag-rename`, 2 capabilities, spec-note-tag untouched, supersession stated, verified the 2-test regression claim by running the suite on a scratch copy) 4 open questions: tag position after rename/collapse, error order, return order, non-array stored `tags`; split into stories? | — | 236 s |

**Findings:** [V-lab]
- With a new folder, `bmad-spec` never edits the other epic's files: spec-note-tag is untouched and the override is stated only in the new spec (supersedes two lines, adopted as companion).
- **Contrast with Experiment 9:** there, updating the same spec, it flagged story 1's falsified frozen lines immediately and would not edit them unauthorized. Here, the new spec has **no mention of story 1's frozen block at all** (grep for frozen / story 1 / `1-tag-storage`: no hits). The contradiction with the first epic's frozen story is invisible from the new epic's side. Whether `bmad-build` notices it is the next step.
- It checked a regression claim empirically (ran the suite with the pattern widened on a scratch copy: exactly 2 of 76 fail) instead of asserting it.
- It self-corrected twice before finishing: removed two non-goals it had invented, and cut a false clause from the Why.

**Build, story 1 (Underscore tags):** [V-lab]
- Setup error of mine first: the initial run halted in 11 s because the allowlist covered `Bash(uv run:*)` but the session invoked `render_skill.py` through PowerShell; adding `PowerShell(...)` equivalents fixed it. Not a BMAD finding.
- Checkpoints fired as in 5h: dirty tree (my untracked `.out` transcripts) and subagent permission. Carl approved Claude's suggestions: (a) leave them untracked, yes to subagents. Later transcripts saved to `labs\lab9b-out` instead.
- Route **oneshot**, 190 s. It widened `TAG_PATTERN`, flipped the two shipped tests at `:93` and `:365` to acceptance, and reworded the error message. Review raised 9 points: 6 patched (the message plus 5 missing edge tests), 3 rejected. 82/82 tests pass. It stopped before committing, as instructed.
- **The cross-epic answer: nothing froze and nothing asked.** `bmad-build` changed code that spec-note-tag's story 1 frozen block pins (`^[a-z0-9-]{1,20}$`, `a_b` illegal), and flipped two tests that story's work shipped, without mentioning that frozen block anywhere. Neither did the review. The new story's intent line cites the supersession ("supersedes spec-note-tag's underscore rejection"), inherited from the new SPEC.md, so the override is recorded, but only in the new epic. spec-note-tag's SPEC.md and story 1 file still say underscore is rejected. Prediction 3 confirmed; prediction 4 confirmed for 9b (in 9, the in-place update did fix them, on Carl's authorization).
- Contrast: in Experiment 9 (same spec), `bmad-spec` refused to edit story 1's frozen lines without authorization. Across epics, the frozen block is simply not consulted: **frozen-after-approval protects a story's intent within its own spec's workflow, not the code it produced.** [I, from 9 vs 9b]
- Carl: "please commit." Committed `b29066a` in `lab9b-crossepic` (lab repo only; `src/notes.js`, `tests/notes.spec.js`). Story 2 (`renameTag`) left unbuilt: the experiment's question is answered.

**Experiment 9 result (9 + 9b):** within one spec, a frozen story block is guarded (flagged, edited only on explicit human authorization, review history preserved). From a second epic, it is not consulted at all: `bmad-spec` records the override only in the new spec, and `bmad-build` plus review change the frozen story's code and shipped tests without mention. The first epic's spec and story files are left stating the old rule. [V-lab; I on the generalization]

## Experiment 10 — `bmad-code-review` over the whole tags epic (2026-09-29/30, done, interactive with Carl)

**Question:** each story's own review missed B1 (live store objects returned through the public API); only the retrospective's `bmad-review` pass over the combined diff found it (Experiment 5i). Does `bmad-code-review`, pointed at the whole epic's commit range with the spec, find it mid-epic, without waiting for a retrospective?

**Setup:** `labs\lab10-epicreview`, copy of `lab5-route`, checked out at `7ab412b` (end of story 4, before the B1 fixes) on branch `epic-review`. Removed from the gitignored `_bmad-output/` because they postdate the epic and name B1: `RETROSPECTIVE.md`, the two B1/B2 fix specs, and the B1/B2 entries in `deferred-work.md` (the story-4 `nextId` entry kept). **Residual contamination, accepted:** `SPEC.md` and `.memlog.md` were reconciled after the retrospective, so the memlog mentions that a retrospective and "remediation items R1-R5" exist, without describing B1. Story 1's triage log (row 11, "duplicate path returns the live stored object", rated `false`) is genuine epic history and stays. Range: `846e9dc..7ab412b`.

**Predictions (written before the run):**
1. It finds B1 or a close variant: the retrospective's `bmad-review` found it over the same combined diff, and two lenses found it independently there. [prediction]
2. If found, it ties it to the tags field added in story 1 plus the live returns, not just "getNote returns a live object" (a pre-existing convention it may dismiss as out of scope). [prediction]
3. It halts at least once for a human: the spec question or subagent permission, then the patch-handling menu (as in Experiment 3). [prediction]

| Step | BMAD asked | Answer | Time |
|---|---|---|---|
| 1 | Confirm target (4 commits, +556/−1, mode `full` against SPEC.md); launch subagents for four reviewers (Blind Hunter, Edge Case Hunter, Verification Gap, Acceptance Auditor)? | Claude suggested yes/yes; Carl: "Go with suggestions" | 27 s |
| 2 | (review done) 3 patch, 2 defer, 11 reject, 0 decision-needed; patch menu: apply all, or walk through | — | 149 s |

**Findings:** [V-lab]
- **B1 was found and rejected.** A reviewer raised it ("`listNotesByTag` returns the stored note objects rather than copies"), and triage rated it `false`: "Story 3 requires this, and it matches `listNotes`." The same defect the retrospective called the epic's most serious was dismissed on exactly the grounds each story's own review used: a spec acceptance criterion (story 3's AC-3) and the pre-existing convention. Prediction 1 half right (found), prediction 2 wrong (not tied to story 1's mutable `tags` field; judged against convention instead).
- **B6 was found and patched:** Verification Gap mutated `addTag`/`removeTag` to edit in place and all 61 tests still passed, and triage named the cross-story inconsistency (story 1 declined this test; story 4 added it for `removeNote`). This is a genuinely cross-story finding the per-story reviews could not make.
- `nextId` id reuse (A1) raised by three reviewers, deferred again, flagged as the epic's most significant known defect.
- Nothing written to SPEC.md: the workflow only records findings into a spec with a Tasks/Subtasks section, and an epic `SPEC.md` has none. Findings live only in chat plus two `deferred-work.md` entries.
- Prediction 3 confirmed: halted for confirm + subagents, then at the patch menu.
- **Reading:** a range review sees the whole epic's diff, so it can find the pieces of a cross-story defect, but its triage weighs each finding against the spec and existing conventions. Where the spec itself blesses the behavior (AC-3), the finding is rejected. The retrospective's pass differed in weighing the compound effect (a new mutable field plus live returns from a new entry point) rather than each piece's local justification. [I]
- Carl: stop here. Patch menu left unanswered; no patches applied, nothing committed in `lab10-epicreview`.

## Experiment 11 — `bmad-architecture` brownfield on a legacy-shaped toy (2026-09-30 to 10-01, done, interactive with Carl)

**Question:** `bmad-architecture` says to read the code first and "ratify existing conventions" on a brownfield codebase, and that an altitude sweep must leave no structural dimension silent (P21, [architecture-skill.md](architecture-skill.md)). On a legacy app whose business rules live only in UI event handlers, and whose database is declared off-limits: does the spine capture those rules, or ratify the handler layer's *structure* and miss the rules in it? Is the unchanged data layer recorded as decided, deferred, or left silent?

**Toy (generic, built for this experiment):** `labs\lab11-legacy`, "Order Desk", a small JS port of a desktop forms app (commit `67d948f`, BMAD 6.12.0 installed and committed on top). One module per screen exporting event handlers (`onLoad`, `onCustomerChange`, `beforeSave`...), a thin data module, one report, and `db/schema.sql`. README: being rewritten as a web front end plus service layer across several epics by different people; "the database stays exactly as it is... nothing in `db/` may change" because other systems read it. The README does not say where the rules are.

**Planted rules (answer key, kept out of the lab folder):**

| # | Rule | Where it lives |
|---|---|---|
| R1 | Customers on `hold` cannot place orders (Save disabled) | `orderForm.onCustomerChange` |
| R2 | Discount capped at 15%, 20% for gold; floored to whole percent | `orderForm.onDiscountChange` |
| R3 | $5 handling fee when subtotal under $50 | `orderForm.onFormatTotal` (a "formatting" handler) |
| R4 | Shipped orders cannot be reopened or cancelled | `orderForm.onStatusChange` |
| R5 | Open orders + this order over credit limit needs manager override | `orderForm.beforeSave` |
| R6 | Order region defaults from customer | `orderForm.onCustomerChange` |
| R7 | Gold tier needs credit limit ≥ 10,000; lowering the limit demotes gold | `customerForm.onTierChange` / `onCreditLimitChange` |
| R8 | Credit limit rounded to whole, never negative | `customerForm.onCreditLimitChange` |
| R9 | Month-end excludes cancelled, splits override sales, excludes handling fee | `reports/monthEnd.js` |
| R10 | `created_at` stamped at form load, not at save | `orderForm.onLoad` |
| D1 | DB `CHECK (discount_pct BETWEEN 0 AND 25)` disagrees with the UI caps (15/20) | `db/schema.sql` |

**Predictions (written before the run):**
1. It asks purpose/audience/altitude and paradigm questions before drafting (coaching path default). [prediction]
2. It records the database as a decided, binding constraint (an `[ADOPTED]` AD or equivalent), since the README states it plainly. [prediction]
3. It ratifies structure (screen → handlers → data module) and proposes a paradigm for the rewrite, but lists few of R1–R10 as invariants: the spine is for cross-unit consistency, not business rules. At most it names "where business rules live" as a boundary decision. I expect R3 (fee hidden in a formatter) and R10 to be missed entirely. [prediction]
4. D1 (DB check vs UI caps) is not noticed. [prediction]

**Run (coaching path, relay method; every answer was Claude's suggestion, approved by Carl with "Go with suggestions"):**

| Round | BMAD asked | Answer | Time |
|---|---|---|---|
| 1 | (read the code) mode; purpose/audience; DB engine; other writers. Opened by naming the core risk: "every business rule lives in the form event handlers", DB enforces almost none, and the 0–25 CHECK is looser than the form's 15/20 caps (D1) | coaching; spine only, build contract; SQLite; Order Desk sole writer | 83 s |
| 2 | Faithful port or fix? Listed 7 behaviors from the code, incl. R2/R3/R4/R5/R7/R9 and real quirks not planted (cap not re-applied on customer change, hold only via disabled Save, override unaudited, Cancelled→Open allowed, float money, UTC month grouping) | faithful port, quirks included; assume billing/warehouse may rely on any stored value | 45 s |
| 3 | Where do rules run once there is an API? A browser-only / B validate-on-save (breaks parity) / C service owns the draft, per-field round-trips (its lean) | C | 41 s |
| 4 | DB location and readers, journal mode (switching to WAL would be a DB change by another route), sign-in and override, web search permission | one Windows server, readers local read-only, journal mode untouched; Windows login, anyone may override; web allowed | 42 s |
| 5 | Stack: server OS; Node+TS vs ASP.NET Core (C# decimal breaks float parity); htmx vs SPA | Windows; Node 24 + TS, IIS gate; htmx 2.x | 58 s |
| 6 | Concurrent edits (one transaction for credit check + write), unsaved drafts in memory, identity gate-only, cutover overlap, **old code as frozen parity oracle**, four epics | all accepted; single cutover | 44 s |
| 7 | (drafted spine, 3 reviewer subagents: adversary, rubric, versions; applied fixes) 8 open questions + sign-off on 6 derived ADs | — (Carl stopped here) | 893 s |

**Spine (`ARCHITECTURE-SPINE.md`, 285 lines, `status: draft`, paradigm "functional core / imperative shell, server-held drafts, htmx"):** 12 ADs. [V-lab]
- **Rules are captured by reference to the code, not by listing them.** AD-1 (faithful port): "for the same starting data and the same sequence of user edits, the rewrite produces exactly the field values, messages, save outcomes and stored rows that `src/` produces, quirks included. `src/` is the authority." AD-2 freezes `src/` as an oracle and gates every port story on side-by-side parity tests. AD-1 names eight behaviors as "examples, not a complete list".
- **Answer-key coverage.** Named in the spine: R1 (hold via `saveEnabled`), R4 (status rules), R5 (credit check incl. fees), R6 (region copy), R7 (gold demotion), R9 (UTC month grouping), plus float money/`round2`. Named during questioning but not in the spine: R2 caps, R3 handling fee. R10 (`created_at` stamped by `onLoad`) surfaces as OQ-2 (does `onLoad` run when an existing order is opened?). Not mentioned: R8 (credit-limit rounding). D1 named in round 1, not carried into the spine as such (UI caps are stricter than the CHECK, so it never trips; OQ-5 covers the general stub-vs-real-schema case). Under AD-1/AD-2 every rule, listed or not, is bound by the parity gate.
- **The data layer is decided, not silent:** AD-7 "The database file is never changed": no DDL, no persistent PRAGMAs, explicit `foreign_keys = OFF` because the chosen driver defaults it on (a reviewer catch), writes only full legacy-shaped rows.
- **The gap it found that I did not plant (OQ-1):** the desktop form definitions (which fields are editable, which event fires which handler, what type each control passes) are not in the repository, and the faithful port depends on them. Rules that live in the UI include the event wiring itself, which isn't in the code at all.
- Reviewer gate changed two approved decisions and said so: FK default of the driver, IIS overlapping recycle and idle shutdown (would split or lose in-memory drafts).

**Predictions:** 1 confirmed (questions first, coaching). 2 confirmed (AD-7). 3 wrong in its main claim: the spine did not ratify the handler structure and stop there; it made "rules live in UI handlers" the central risk, moved rule ownership to the service (AD-3), and bound every rule through the oracle and parity gate. Half right that it lists few rules as invariants, by design. 4 wrong: D1 was the first thing it named.

**Reading:** "ratify existing conventions" here meant ratifying *behavior* (the legacy code as executable spec), not *structure* (the handler layer moved server-side). The remaining risk is the one the spine itself names: what isn't in the code (form wiring, OQ-1) can't be in the oracle. [I]
- Carl: stop here (2026-10-02). Open questions and AD sign-off left unanswered; spine stays `draft`. Lab repo holds only the baseline and BMAD install commits.

## Experiment 12 — `bmad-prd` Update mode on a hand-written PRD (2026-10-02, done, interactive with Carl)

**Question:** `bmad-prd` Update mode says that if the memlog is missing, "a bootstrap subagent reverse-engineers a thin one from the PRD", and that "conflicts with prior decisions are surfaced before applying" (P20, [prd-skill.md](prd-skill.md)). This is the "bring what you have" path: does it surface conflicts before editing, and is the bootstrapped memlog sensible?

**Toy (generic):** `labs\lab12-prd`, a hand-written one-page PRD for a community library's room-booking system (`docs/prd.md`, no memlog, never touched by BMAD; commit `3ee7da8`, BMAD 6.12.0 installed on top as `ad168a5`).

**Change request given to Update mode:** community groups want weekly recurring bookings of the Oak Room, up to 4 hours a session, for a whole season (for example September to December).

**Planted (answer key, kept out of the lab folder):**

| # | What | Where | Kind |
|---|---|---|---|
| K1 | 2-hour maximum, "decided by the board in March 2026" with a reason | Rules + FR3 | explicit conflict with a recorded decision |
| K2 | Recurring bookings listed as a non-goal | Non-goals | explicit conflict |
| K3 | A member holds at most 2 future bookings | FR4 | implicit conflict (a season series is many future bookings) |
| K4 | Free slots shown for the next 14 days | FR2 | implicit conflict (a season runs months ahead) |
| K5 | "Community groups" are not a user type; only members (cardholders) and staff exist | Users | implicit gap |
| C1 | Walk-ins without a card can book via staff, but Users and FR7 say only members book | Rules vs Users/FR7 | pre-existing internal contradiction, unrelated to the change |

**Predictions (written before the run):**
1. It bootstraps a memlog before editing, and records K1 as a decision (it has a date and a reason) and K2 as a non-goal. [prediction]
2. It surfaces K1 and K2 before applying anything and asks how to resolve them. [prediction]
3. It catches K3 and K4 (implicit), probably K4 less reliably than K3. K5 maybe. [prediction]
4. C1 is not mentioned; it's unrelated to the change. [prediction]

| Round | BMAD asked / did | Answer (Claude-suggested, Carl-approved) | Time |
|---|---|---|---|
| 1 | **Wrote nothing.** Listed conflicts with recorded decisions: K1 (quoting the board's reason), K2, K3 and K4 together ("a September–December series breaks both"), plus the PRD's "approved by the board" status line. 10 questions, K5 among them ("who can book a series... how is a group identified?") | proposed, pending board; staff-only for a named contact member; 4 h for Oak Room series only; fixed seasons; reject whole series on clash; 1 series per group, max 2 Oak evenings/week; series exempt from FR4/FR2; cancel one or all, 1 h cutoff; one series email; counter-measure ≥50% Oak evenings free | 23 s |
| 2 | Applied: new "Proposed change" section (FR9–FR17) marked pending board approval in header, section and Rules; the March 2026 rule and non-goal kept and pointed at it, not overwritten. Bootstrapped `docs/.memlog.md`. 3 new gaps opened by the answers | evening = starts at/after 17:00; one series per contact member; single email on whole-series cancel; then run reviewer + finalize, ask before commit | 59 s |
| 3 | Reviewer pass (rubric + adversarial subagents, reports in `docs/`): 2 critical, 4 high, 9 medium, 6 low. Stopped for decisions | — | 206 s |

**Findings:** [V-lab]
- **Conflicts surfaced before applying, as documented (P20).** Round 1 changed no file. All four K-conflicts were named, including both implicit ones (K3, K4), and K5 became a question. Predictions 2 and 3 confirmed; K4 was not harder than K3.
- **The bootstrap memlog was written with the first edit, not before the conflict check** (prediction 1 half right). It is thin, as documented: two `Recovered (Mar 2026)` decision entries (the 2 h cap with its board reason; FR4, FR2 and the non-goal), then the change and the answers. It credits every answer to "Carl" though Claude drafted them (same attribution gap as Experiments 5b/5e, `systemic-findings.md`).
- **The proposal was kept separate from the approved baseline:** "Until the board approves it, the March 2026 rules and non-goals above stand." The recorded decision was annotated, not rewritten.
- **The reviewer gate caught a hole in an answer I drafted and Carl approved:** defining "evening" by start time (≥17:00) lets a 16:00–20:00 series take a whole evening without counting, so six contacts could hold every evening, "exactly what the board's 2-hour rule was meant to stop". It also found the counter-measure can never fail under FR14's cap, an FR16 vs FR6 cutoff conflict, and that the "one series per contact" control is easy to get around.
- **C1 (walk-ins without a card vs members-only Users/FR7):** both reviewers noticed the walk-in rule, but only in relation to series (rubric: low, "not a conflict"; adversarial: M6). Neither named the pre-existing contradiction. Prediction 4 essentially confirmed.
- Carl: stop here (2026-10-02). Review findings left unanswered; PRD not finalized; nothing committed in the lab beyond the baseline and BMAD install.

## Experiment 13 — BMB build + what survives a reinstall (2026-10-03, done, interactive with Carl)

**Question:** what does a BMAD update overwrite and what survives? Feeds the queued `wiki/updating-bmad.md`. No release newer than 6.12.0 exists, so a same-version reinstall stands in for an update. Also: one small build with BMB (Builder module), to see where a custom skill lands and whether it survives.

**Setup:** `labs\lab13-bmb`, a copy of `lab8-tea` (core/BMM 6.12.0 + TEA v1.26.0, BMB v2.2.2, CIS v0.3.2, pinned). `_bmad/` and `.claude/` are excluded from git there (`.git/info/exclude`), so before/after are compared by snapshot copies, not git.

**Docs read first** (`docs/customize/customize-bmad.md` at the v6.12.0 tag, new ledger entry P30; BMB `bmad-workflow-builder/SKILL.md` + `customize.toml`):
- `_bmad/custom/` override files: "Updates do not touch your files." [V, P30]
- A skill's own `customize.toml`: "Never edit it; updates overwrite it." The installed file's header agrees: "DO NOT EDIT -- overwritten on every update." [V, P30; V-lab]
- `_bmad/config.toml` and `config.user.toml` are installer-owned, "regenerated on every install"; `_bmad/custom/config.toml` is "never touched by the installer". [V, P30]
- BMB's workflow builder writes new skills to `{bmad_builder_output_folder}`, default `{project-root}/skills`, not `.claude/skills`. [V, BMB SKILL.md]
- Not documented: what a reinstall does to an unknown skill folder a user added under `.claude/skills/`.

**Planted customizations (before the reinstall):**

| # | Change | Where | Docs say |
|---|---|---|---|
| U1 | Direct edit: `icon` changed + a marker comment | `.claude/skills/bmad-agent-pm/customize.toml` | overwritten |
| U2 | Team override: `icon` + one `persistent_facts` line | `_bmad/custom/bmad-agent-pm.toml` | survives |
| U3 | Central override: PM descriptor `description` | `_bmad/custom/config.toml` | survives |
| U4 | Direct edit: marker comment | `_bmad/config.toml` (installer-owned) | regenerated |
| U5 | Hand-added skill folder `lab-marker-skill` | `.claude/skills/` | undocumented |
| U6 | The skill BMB builds | `skills/` (BMB default) | undocumented |

**Predictions (written before any change):**
1. U1 and U4 are reverted; U2 and U3 survive byte-identical. [prediction]
2. U5 survives: the installer writes its own skills and leaves unknown folders alone. Low confidence. [prediction]
3. U6 survives (outside `_bmad/` and `.claude/`), but BMAD doesn't install it as a usable skill; it sits in `skills/` until someone moves it. [prediction]
4. A quick-update (the non-interactive default) moves `lastUpdated` for every module even though nothing changed; `installDate` stays. [prediction]

**BMB build (relay method, answers Claude-suggested, Carl-approved):** [V-lab]
- `/bmad-workflow-builder --headless` returned the documented headless shape, a JSON object with `"status": "blocked"` and a `reason`, even under `claude -p`. Three rounds: word rule and report shape and evals (whitespace like `wc -w`; "N words in <file>"; no evals); then a lint decision; then `"status": "complete"`. 107 s + 83 s + 13 s.
- Output landed in `skills/lab-word-count/` as documented: a 12-line `SKILL.md`, `scripts/count_words.py`, 6 passing tests; it matched `wc -w` on a real file (119 words). It was **not** installed into `.claude/skills/`, so Claude Code would not load it until someone moves it.
- **BMB contradicts itself on the memlog:** its own path-standards scan rated `.memlog.md` at the skill root a high-severity finding, while its own build rules put the memlog exactly there. It asked rather than choosing; Carl kept it.

**Customizations planted, then a snapshot.** Two errors of mine first: PowerShell 5.1's `Set-Content -Encoding utf8` wrote a BOM that broke TOML parsing (`Invalid statement (at line 1, column 1)`), and reading then rewriting `_bmad/config.toml` mangled its box-drawing characters. Fixed by rewriting without BOM; the reinstall then restored the file anyway. Not BMAD findings. Before reinstalling, the resolver returned `icon = "U2"`: the team override beats a direct edit to the shipped file, as documented. [V-lab]

**Quick-update (the non-interactive default, `install --yes` with no `--action`), 42 s:** "Updated 5 modules with preserved settings". Diff of `_bmad/`, `.claude/`, `skills/` before vs after: [V-lab]

| # | Result |
|---|---|
| U1 direct edit to a skill's `customize.toml` | **Overwritten, no backup.** Icon and marker gone; no `.bak` written. |
| U2 `_bmad/custom/bmad-agent-pm.toml` | Survived byte-identical. |
| U3 `_bmad/custom/config.toml` | Survived byte-identical. |
| U4 direct edit to `_bmad/config.toml` | **Regenerated, but backed up:** new `_bmad/config.toml.bak`, byte-identical to the edited file. |
| U5 hand-added `.claude/skills/lab-marker-skill/` | Survived; the installer still reports "54 skills" and leaves the extra folder alone. |
| U6 BMB-built `skills/lab-word-count/` | Survived (outside the installed folders). |
| Manifest | `lastUpdated` moved for all 6 entries; `installDate` unchanged. Module `config.yaml` files regenerated (new date, keys reordered); `files-manifest.csv` updated. |

**Full update (`--action update` with module list and pins):**
- **First attempt failed, and a failed update is not atomic.** PowerShell split my unquoted `--modules bmm,tea,bmb,cis` into separate words, and the installer failed in 4 s: "Source for module 'bmm tea bmb cis' is not available." The trigger was my quoting, but the failure still **deleted** every module's `config.yaml` and `module-help.csv` (10 files), **added** 66 copies of core skill files under `_bmad/core/bmad-*`, and rewrote the manifest, then reported failure. Customization overrides and the resolver survived it. [V-lab]
- **Re-run with quoted arguments, 10 s: repaired cleanly.** Versus the post-quick-update state, nothing removed, nothing added; only regenerated config/manifest files changed. U2, U3, U5, U6 and `config.toml.bak` all still present. U1/U4 were not re-planted before this run, so the full-update path's own treatment of direct edits is inferred to match quick-update, not observed. [V-lab; I]

**Predictions:** 1 confirmed (U1, U4 reverted; U2, U3 byte-identical), with a detail the docs don't give: the installer-owned config gets a `.bak`, a skill's `customize.toml` does not. 2 confirmed (unknown skill folder left alone). 3 confirmed (BMB output survives, not installed as a usable skill). 4 confirmed (`lastUpdated` moves on every module, `installDate` stays), so `lastUpdated` records the last install run, not the last real change.

- Carl's instruction was to run it; experiment complete 2026-10-03. Lab not committed (`_bmad/`, `.claude/` excluded there).

## Experiment 14 — CIS: Carson vs `bmad-brainstorming` directly (2026-10-03, done, interactive with Carl)

**What CIS is, read first** (installed CIS v0.3.2, `_bmad/cis/module-help.csv` and `bmad-cis-agent-brainstorming-coach/SKILL.md` + `customize.toml`): five workflows (innovation strategy, problem solving, design thinking, storytelling, and brainstorming) plus six agent personas. **CIS has no brainstorming skill of its own:** its Brainstorming menu row and Carson's only menu item (`BS`) both dispatch to the core `bmad-brainstorming`. Carson ("Elite Brainstorming Specialist") is a persona (role, identity, "enthusiastic improv coach" style, three principles) plus that one-item menu; Step 8 skips the menu and dispatches directly when the opening message names the intent. [V-lab, installed files]

**So the question becomes the queued persona test (STATE Next item 0):** does running the same skill through a persona change the session, or only its voice? Every earlier lab run invoked skills directly.

**Setup:** two copies of `lab8-tea` (separate folders so `claude -p --continue` sessions don't cross): `labs\lab14-direct` runs `/bmad-brainstorming`, `labs\lab14-cis` opens with "Hey Carson, let's brainstorm". Same generic topic and goal in both; same relayed answers in both.

**Predictions (written before the run):**
1. Carson dispatches straight to `bmad-brainstorming` without showing a menu (intent is named). [prediction]
2. Both halt at the same stance/technique choice (Experiments 6 and 7: a present human message means interactive). [prediction]
3. Same artifact shapes and similar idea counts; the persona changes chat voice (icon prefix, enthusiasm), not the session's structure or the ideas. [prediction]

**Round 1 (opening), both in parallel:** direct 18 s, Carson 31 s. Carson skipped his menu and went straight to `bmad-brainstorming` (prediction 1 confirmed), adding the 🧠 icon, a warmer opener and a `bmad-help` reminder. Otherwise the same session: the same stance question (Facilitator / Creative Partner / Ideate for me), the same technique-picker choice (composer page or in chat), the same ask for context, and the same blocked attempt to open the composer page. Prediction 2 confirmed. [V-lab]

**Round 2:** identical answers to both (Claude-suggested, Carl-approved): Ideate for me; the coach chooses techniques; context (rooms seat 12 and 4, open Mon–Sat 9:00–20:00, $500 a year, nothing tried). [V-lab]

| | Direct `/bmad-brainstorming` | Through Carson |
|---|---|---|
| Time | 377 s | 467 s |
| Techniques | 8 (Job to Be Done, Persona Journey, Worst Possible Idea, $0 Mandate, Ecosystem Thinking, Crank the Dial, SCAMPER, Parallel Universe) | 6 (Job to Be Done, Persona Journey, Anti-Solution, $0 Mandate, SCAMPER, Pirate Code + Alien Anthropologist) |
| Ideas | 102 | 105 |
| Memlog | 121 entries | 120 entries |
| `brainstorm.html` | 655 lines | 217 lines |
| Shortlist | 9 candidates, explicitly unchosen: "I haven't chosen any of them" | 7 picks in a costed table summing to ~$475, "my suggestion for you to accept or change", plus "free fixes that come first" |
| Extras | a cross-idea pattern ("friction and tone matter more than programming"); offers to summarize, plan or go deeper | a timing warning (college-essay workshops before ~Nov 1), flagged its own unverified FAFSA date; offers to switch stance |

**Findings:** [V-lab]
- **The session's structure didn't change.** Same skill, same checkpoints, same artifact types, near-identical idea and memlog counts, four of the opening techniques shared.
- **The output's stance did.** The direct run left the shortlist to the human; the Carson run made a costed, prioritized recommendation and added urgency. Carson's configured style is "enthusiastic improv coach... YES AND everything", so a more prescriptive close is not what the persona text describes. Prediction 3 half wrong: the persona changed more than voice, but not in the direction its own description suggests.
- **One run each.** Experiment 3 showed two runs of the same skill on the same input can make different judgment calls (`systemic-findings.md`, "Triage verdicts are one sample"). So the shortlist difference may be run-to-run variance rather than the persona. The structural sameness is solid; the stance difference is a single draw. [I]
- Answers the persona-layer question (STATE Next item 0) for this skill: an agent persona wraps the same workflow and does not alter its mechanics. Whether it changes judgment needs repeated runs. [I]
- Ideation quality was not judged, as in Experiments 6 and 7.

- Experiment complete 2026-10-03; both sessions left waiting at their "what next" question. No lab commits (`_bmad-output/` and `_bmad/` excluded).

### Experiment 14b — repeat runs (2026-10-03, done)

**Why:** Experiment 14's one difference (Carson's shortlist was costed and prescriptive; the direct run left it unchosen) rested on one run each. Two more runs per arm, each in a fresh copy of `lab8-tea` (`lab14-direct-2/3`, `lab14-cis-2/3`), same two-step protocol, same opening and the same Carl-approved answers reused verbatim. Scored on: whether the shortlist is chosen or left to the human, whether it is costed, idea and technique counts, time.

**Prediction:** if the persona drives the stance, all three Carson runs are prescriptive and all three direct runs leave the choice open. If it's variance, the stances mix within each arm. I expect a mix. [prediction]

**Results, all six runs** (runs 1 are Experiment 14's): [V-lab]

| Run | Time (step 2) | Techniques | Ideas | Shortlist | Costed? | Who decides |
|---|---|---|---|---|---|---|
| Direct 1 | 377 s | 8 | 102 | 9 candidates | No | Explicitly left to the human, "I haven't chosen any" |
| Direct 2 | 391 s | 7 | 104 | 7, "a recommendation, not a decision" | Yes, full $500 table | Human keeps/drops; asks if the split is right |
| Direct 3 | 511 s | 9 | 97 | 6, "for you to accept, cut or change" | One item only (~$150) | Asks the human how to split the $500 |
| Carson 1 | 467 s | 6 | 105 | 7, "my suggestion" | Yes, ~$475 | Human accepts or changes |
| Carson 2 | 406 s | 8 | 101 | 8, "draft shortlist", "your call" | Yes, $500 | Human keeps/adds |
| Carson 3 | 310 s | 5 | 104 | 7, sequenced by month | Yes, ~$385, rest left for the teen board | Plus six library-policy questions it won't decide |

**Findings:**
- **Mechanics: no persona effect.** Across six runs, ideas 97–105, techniques 5–9, times 5–9 minutes, the same checkpoints and artifacts, with no pattern by arm. [V-lab]
- **No run made the final decision.** All six handed the shortlist back to the human, whatever the framing. [V-lab]
- **Costing leans toward Carson, weakly.** All three Carson runs returned a fully costed shortlist; the direct runs were mixed (one full, one partial, one none). Experiment 14's single-pair contrast was partly variance: direct run 2 was as costed as any Carson run. With three per arm, this is a lean, not a result. [V-lab; I on the cause]
- Prediction (a mix within each arm): right for the direct arm, wrong for Carson, which was consistent on costing.
- Carson runs also tended to add concrete next-step framing (a timing warning, month-by-month sequencing, policy questions); direct run 3 asked policy questions too, so this isn't exclusive to the persona. [V-lab]
- **Answer to the persona question for this skill:** the persona wraps the same workflow and leaves its mechanics and its "human decides" checkpoint intact. It may nudge the close toward a costed recommendation; three runs can't separate that from chance. [I]

- Experiment 14b complete 2026-10-03. Labs `lab14-direct-2/3`, `lab14-cis-2/3`, sessions left at their closing question.

## Experiment 16 — does a central config override reach `bmad-code-review`, 6.12.0 vs 6.12.1? (2026-10-07, Carl-approved)

*Numbered 16 because the skill's queue reserves 15 for `bmad-prd` create-then-validate.*

**Question:** the v6.12.1 CHANGELOG (#3019) says 23 bmm skills at 6.12.0 read `_bmad/bmm/config.yaml` directly, so overrides in `_bmad/custom/config.toml` did not reach them. Does that show in a real run, and does a real 6.12.0 → 6.12.1 update fix it? Also the first real version-to-version update for [updating-bmad.md](updating-bmad.md).

**Setup:** two copies of `lab3-review` (Experiment 3's flawed coupon commit `92c1ace`, BMAD 6.12.0): `labs\lab16-v0` (left at 6.12.0) and `labs\lab16-v1` (updated). Both got the same override appended to `_bmad/custom/config.toml`: `[core] communication_language = "French"`. Pre-update snapshot: `labs\lab16-v1-presnap`.

**Deterministic checks (before any review run):**
- `uv run _bmad/scripts/resolve_config.py --project-root .` returns `"communication_language": "French"` **at 6.12.0** (lab16-v0). The resolver already honored the override; what 6.12.1 changes is whether skills call it. [V-lab]
- Installed `bmad-code-review/SKILL.md` Step 4 at 6.12.0: "Load config from `{project-root}/_bmad/bmm/config.yaml`", which says `communication_language: English`. At 6.12.1: "Run `uv run {project-root}/_bmad/scripts/resolve_config.py ...`". [V-lab]
- **The update:** `npx -y bmad-method@6.12.1 install --directory . --modules bmm --tools claude-code --yes` (a quick-update, no `--action`) took core and bmm 6.12.0 → 6.12.1 ("Custom files preserved: 2"). Unlike Experiment 8's case of adding modules, a version bump of installed modules needed no `--action update`. Manifest shows 6.12.1 for both; `lastUpdated` moved. [V-lab]
- After the update: `_bmad/custom/config.toml` byte-identical (hash match); no `.bak` (no direct edit planted); 235 files under `_bmad/` + `.claude/` before and after; lab git status clean. [V-lab]
- **#3016 confirmed:** `_bmad/config.toml` now carries user-scope keys it lacked at 6.12.0: `user_name = "BMad"` (the module default, not the install answer), `communication_language`, `user_skill_level`. The resolver still returns `user_name: "Carl"`, because `config.user.toml` outranks it. Someone reading `config.toml` alone would see the wrong name. [V-lab; I on the risk]

**Predictions (written before the review runs; source CHANGELOG v6.12.1 #3019):**
1. v0 (6.12.0): the trace shows `_bmad/bmm/config.yaml` read and no `resolve_config.py` call; the review is presented in English.
2. v1 (6.12.1): the trace shows `uv run ... resolve_config.py`; the review is presented in French.
3. Risk: a French result could come from the model reading `custom/config.toml` itself, and an English one from the English prompt pulling it back. So the trace decides; language is supporting evidence only. If v1 can't run the script (Experiment 4 saw headless approval failures), the result is inconclusive, not negative.

**Run:** same prompt in both arms (no-spec mode declared, step-1 checkpoint pre-approved, stop at the patch-handling menu without choosing), `claude -p ... --permission-mode acceptEdits --allowedTools "Bash(uv run:*)" "Bash(git:*)" "Bash(node:*)" "Bash(npm test:*)"`, `--output-format stream-json --verbose` saved to `labs\lab16-out\`.

**Result: both predictions confirmed, by trace and by language.** [V-lab]

| | v0 (6.12.0) | v1 (6.12.1) |
|---|---|---|
| Config load (trace) | `cat _bmad/bmm/config.yaml` (English); no `resolve_config.py` call | `uv run _bmad/scripts/resolve_config.py --project-root .` (French) |
| Read `_bmad/custom/config.toml` itself? | No (grep of the full trace) | No |
| Language of the presented review | **English** | **French**, throughout, including the patch menu |
| Time / turns | 117 s / 15 | 138 s / 20 |
| Findings | 7 patch, 1 defer, 4 rejected | 8 patch, 0 defer, 3 rejected |
| Stopped at | patch-handling menu, unanswered | patch-handling menu, unanswered |

- **So on 6.12.0, a team override in `_bmad/custom/config.toml` survives every update and is still ignored by `bmad-code-review`.** The resolver honored it all along; the skill never asked the resolver. After the 6.12.1 update, the same file, untouched, took effect with no other change. [V-lab] By the changelog, the same holds for the other 22 skills on the #3019 list (not each tested). [V, CHANGELOG; I for the untested 22]
- The English prompt and Carl's English global instructions did not pull v1 back to English: a resolved config value beat the prompt language. [V-lab]
- Neither arm hit the headless approval problem Experiment 4 saw, because `Bash(uv run:*)` was pre-allowed. Without that allowlist, a 6.12.1 skill may not be able to run the resolver headless. [V-lab; I on the no-allowlist case]
- Both caught planted flaws A to F again. The per-item rounding finding was **defer** in v0 and **patch** (low) in v1: the same split Experiment 3's two runs showed, now across a third pair. Not attributable to the version (no triage files changed in 6.12.1); two non-version candidates are run variance and the node refusal in v1 (below). [V-lab; I]
- Side note: v1 reported "node was refused" for its own direct check, though `Bash(node:*)` was allowed; its Verification Gap subagent did run the code. Likely a compound command not matching the allowlist pattern. Not investigated. [V-lab; ? on cause]

- Experiment 16 complete 2026-10-07. Labs `lab16-v0` (6.12.0), `lab16-v1` (6.12.1), `lab16-v1-presnap`; traces in `lab16-out/`. Both sessions left at the patch menu.

## Experiment 15 — `bmad-prd` Create, finalize, then Validate (2026-10-07, interactive with Carl, relay method)

**Question:** the untested half of `bmad-prd` (Experiment 12 ran Update only). Does Create elicit rather than author? Does Finalize reach `status: final`? Does a separate Validate run, against a PRD that already passed its own reviewer gate, still find things, and does it catch an internal contradiction planted by hand after finalize (Experiment 12's uncaught gap was a pre-existing contradiction)?

**Docs read first** (at the v6.12.0 tag, folded into the ledger as an extension of P20): `references/validate.md` (Validate is critique-only, no Finalize; rubric-walker subagent plus `finalize_reviewers`, default adversarial-general; synthesis into `validation-report.html` + `.md`, grade Excellent/Good/Fair/Poor by fixed rules; opens the HTML with `start ""` on Windows, skipped headless; always offers to roll findings into an Update) and `assets/prd-validation-checklist.md` (seven dimensions: decision-readiness, substance over theater, strategic coherence, done-ness clarity, scope honesty, downstream usability, shape fit; mechanical notes tail covers glossary drift, ID continuity, Assumptions Index roundtrip).

**Setup:** `labs\lab15-prd`, a copy of `lab6-base` (empty repo, BMAD 6.12.0, no PRD). Toy (generic): a neighborhood tool-lending shelf. Every discovery answer is Carl's, relayed verbatim.

**Plan:** (1) Create, relaying questions. (2) Finalize to `status: final`. (3) By hand, plant one internal contradiction unrelated to any change: a Non-Goal (or rule) that directly contradicts an existing FR. Exact text recorded here after planting, before Validate. (4) Validate in a fresh session.

**Predictions (before any run):**
1. Create opens with a brain-dump request and the stakes question (hobby / internal / launch), not a drafted PRD. [P20]
2. On a hobby-stakes answer, the PRD is short (~2 pages) and drops or downscales user journeys. [P20]
3. Finalize runs the reviewer gate and reaches `status: final` only after a human decision on open items.
4. Validate grades the finalized PRD *Good* or better on the unplanted content (it already passed a gate), but **does catch the planted contradiction**, because unlike Update, Validate reviews the whole PRD rather than a change against it; the rubric's mechanical notes and decision-readiness both point at it. Moderate confidence.
5. Headless, Validate writes both report files and does not open the browser.

**Create and finalize (session `188ab3e5`, resumed per turn with `claude -p --resume`; a change from earlier labs' fresh-session-per-turn relay, which keeps the skill's in-context state; Carl's answers relayed verbatim):**

| Turn | Time | What happened |
|---|---|---|
| 1 | 27 s | Workspace + memlog created, empty `prd.md`; asked brain dump + stakes. Prediction 1 right. |
| 2 | 16 s | Carl: "fast path" (no brain dump, no stakes). Logged it, then asked **10 batched questions**; said skipped ones become open questions, not inventions. |
| 3 | 64 s | Carl's ten one-word answers (hobby, shared, web app, invite+approve, owner approves, deposits ×2, on-time returns, no selling / non-tools). Drafted a ~2-page PRD, FR-1 to FR-9, no user journeys ("hobby", prediction 2 right). Asked 7 yes/no readings (a–g) + 7 open questions. **Proposed a counter-metric itself** (loans per month), flagged `[CONFIRM]`. |
| 4 | 47 s | Carl answered the 7 open questions, not a–g. On "4 You decide" (deposit rules) it **declined to decide**: "I'd rather the choice be yours", offered A/B options per sub-decision. |
| 5 | 35 s | Carl: 1B 2B 3A. Applied; noted 3A settled (e). In-app deposits opened **4 new questions** (D1–D4): open count rose. Offered "finalize and carry them as open items with you as owner". |
| 6 | 99 s | Carl: "finalize, leave the rest open". `status: final`; two items marked **blocker** (garage access/confirmation, deposit disputes/timing) and surfaced at the top of the PRD; memlog audit ("everything in the decision log made it into the PRD"); **reviewer pass skipped** ("hobby project"); polish pass, 12 wording fixes in `review-polish.md`; offered to commit, didn't. |

- **Elicits, doesn't author, even on the fast path and even when told "you decide".** [V-lab; V, P20 stance] The docs' "two or three turns" became six; "one or two consolidated questions" became four rounds, because each answer opened new gaps. [V-lab vs V, P20]
- **Tag convention departed from the template, and my relay prompt caused it:** the skill and template say inline `[ASSUMPTION: …]` plus a §9 Assumptions Index; the PRD used `[CONFIRM: …]` tags folded into Open Question OQ-5, no §9. The memlog records why: "Unanswered items go in Open Questions, not ASSUMPTION tags, per user directive that all decisions come from the human". That directive was my standing relay line, not Carl's. So the fast path's assume-and-tag behavior was suppressed by the experiment's own harness; a fast-path run without that line would likely use `[ASSUMPTION]` as documented. [V-lab; I on the counterfactual] Validate's rubric walker accepted the substitute as consistent with the logged directive. [V-lab]
- **Skipping the reviewer pass is allowed:** "Stakes-calibrated — hobby/solo may run quietly or skip" (SKILL.md:75). So a hobby PRD can reach `status: final` with no review at all; `prd-skill.md`'s "gates finalizing behind a reviewer pass" is true only above hobby stakes. [V, SKILL.md:75; V-lab]
- Finalize *did* run the triage step as documented: blockers surfaced, non-blockers deferred with an owner (Carl) and a revisit condition ("before UX or architecture"). [V-lab; V, SKILL.md:90]

**Planted after finalize, by hand (answer key, before Validate):** appended to §5 Non-Goals: "Email notifications. Members coordinate pickups and returns by text message between themselves." Contradicts FR-6 ("The requester is notified of the decision by email"), §6 MVP Scope ("as a web app with email notifications"), and Carl's answer 6 ("email") in the memlog. Not logged in the memlog. Validate passes if it names the contradiction (or the PRD/memlog mismatch).

**Validate (fresh session `406541a9`, not resumed, 276 s):** prompt asked for all reviewers, no PRD changes, no browser. Four reviewer subagents ran in parallel: rubric walker, adversarial-general, edge-case hunter, verification gap (it chose the last two as ad-hoc reviewers; it skipped structure/prose because the finalize polish had run them). It wrote `review-rubric.md`, three `review-*.md`, `validation-report.html` and `.md`; it did not open a browser; it left `prd.md` and `.memlog.md` untouched (timestamps unchanged). [V-lab]

- **Grade Poor, from one critical finding: the planted contradiction, found by all four reviewers.** The rubric walker quoted the planted line, listed all three things it contradicts plus OQ-2 (four in total, one more than the answer key), checked it against the memlog ("Nothing in the memlog supports the text-message line"), and fixed it with "delete the bullet". The synthesis also noticed that `prd.md`'s modified time (03:30) came after the "PRD finalized" memlog entry, with no logged edit. It said where the line came from "cannot be confirmed from the artifacts" instead of guessing. **Prediction 4's key part right; the planted contradiction was caught.** Unlike Experiment 12 (Update), Validate reads the whole PRD against itself and its memlog. [V-lab]
- **Prediction 4's other part wrong:** the unplanted content was not *Good*; it drew 8 high findings, which alone would grade *Fair*. The PRD had never been reviewed (the finalize gate was skipped at hobby stakes), so Validate was its first review. Real gaps it found: the Request/Loan lifecycle (concurrent requests, never-answered or never-picked-up approvals, no "reserved" state) is undefined and missing from the Open Questions; SM-1 counts only closed Loans, so lost tools improve the on-time rate; nothing in the MVP actually pushes on-time returns (the Deposit returns "even if late", reminders are open) though SM-1 claims to validate FR-9; `status: final` alongside two blockers misleads anyone reading the frontmatter; in-app deposit holds can expire in about the Loan length. Plus 15 medium, 10 low. [V-lab]
- **It caught the finalize step's own error:** finalize's memlog audit said "all 30 prior entries reflected"; there were 26 (verified by count). Validate flagged the miscount and that the audit would not have seen a post-finalize edit anyway. [V-lab]
- **Finalize vs Validate on reviewers:** finalize logged "Rubric reviewer gate skipped: hobby stakes, no finalize_reviewers configured", while Validate ran adversarial-general, which `validate.md` calls the default `finalize_reviewers` entry. Resolved: the installed `customize.toml` at 6.12.0 has `finalize_reviewers = []`, so finalize reported correctly and Validate added adversarial-general ad hoc. `validate.md`'s "(adversarial-general by default)" does not match the shipped default. [V-lab, installed `customize.toml`:148; V, validate.md]
- Closed by offering, not doing: three decisions handed back (fix/discuss/defer/ignore the critical one; same per high finding; roll into an Update or stop), matching `validate.md`'s "Always offer to roll findings into an Update". Left unanswered. [V-lab; V, validate.md]
- Prediction 5 right (both report files, no browser).

**Takeaways:**
1. A hobby-stakes `status: final` PRD may never have been reviewed. The skill allows that by design (SKILL.md:75), and here the first review graded it Poor/Fair. "Final" means "the human stopped answering", not "it passed a gate". [V-lab; V, SKILL.md:75; I on the reading]
2. Validate is the mode that catches internal contradictions; Update (Experiment 12) did not. Use Validate on a PRD you inherit, before you Update it. [V-lab across Experiments 12 and 15; I on the advice]
3. The skill held its "elicit, don't author" line even on the fast path and when told "you decide". The cost is turns: six rounds for a two-page hobby PRD. [V-lab]

- Experiment 15 complete 2026-10-08. Lab `lab15-prd`, outputs and traces in `lab15-out/`. Validate session left at its decision questions; PRD not updated.

## Experiment 17 — `bmad-walkthrough` through an agent persona (Amelia) (2026-10-08, interactive with Carl, relay method)

**Questions:** (1) Persona routing: `bmad-walkthrough` is on **no** agent's menu at 6.12.0 (Amelia's is BD, QA, CR, SP, ER; grep of all five `customize.toml`). Her activation rule: dispatch a clear menu match, otherwise "just continue the conversation". Asked for a walkthrough through Amelia, does she invoke the walkthrough skill, route to code review (CR), or do it in her own words? (2) The walkthrough itself, never run in the lab: does it find the spec, generate its own review trail, and stop for a human decision at wrap-up? (3) Does the persona change anything about the walkthrough (Experiment 14 found brainstorming's mechanics unchanged under a persona)?

**Docs read first (at the v6.12.0 tag; extends P31):** `SKILL.md`, `step-01-orientation.md`, `step-02-walkthrough.md`, `step-04-testing.md` in full (03, 05, `generate-trail.md` read 2026-10-03). Orientation finds the change by a five-step cascade (explicit argument, conversation, sprint status, current git HEAD with a confirm question, ask); ENRICH looks for a spec whose `baseline_commit` is an ancestor of the commit; `review_mode` is `full-trail` / `spec-only` / `bare-commit`; non-full-trail generates a trail. Step 2 groups by concern, ends "say **next**". Step 4 is manual-observation suggestions, ends waiting for a decision. Global rule "front-load then shut up": one message per step, no mid-step questions.

**Setup:** `labs\lab17-walk`, copy of `lab5-route` at `ed2c9c0` (the B2 fix, 2 files, +79/−12). Two specs in `implementation-artifacts` have a `baseline_commit` that is an ancestor of HEAD: `spec-b2-...` (baseline `d3c526c`, the right one) and `spec-b1-...` (baseline `7ab412b`, an older change). Neither has `## Suggested Review Order`; B2 has a Spec Change Log and Review Triage Log.

**Predictions (before the run):**
1. Routing: Amelia invokes `bmad-walkthrough` anyway. The request matches its description ("walk me through this change"), and nothing in her rules forbids invoking a skill off the menu. Moderate confidence; the alternative is CR as a fuzzy match.
2. Orientation stops to confirm the change ("I see HEAD is `ed2c9c0` ... is this the change?"), since the prompt names no commit.
3. ENRICH picks `spec-b2` (newest baseline), sets `spec-only`, and generates a trail. It may not notice that `spec-b1` also qualifies.
4. It walks one step per human turn (needs "next"), and never gives an approve/rework verdict itself.
5. Persona effect: the Amelia icon prefix and voice only; no change to the steps.

**Run (session `0829702e`, resumed per turn, Carl's answers relayed verbatim; traces `lab17-out/w1..w7.jsonl`):**

| Turn | Carl | Time | What happened |
|---|---|---|---|
| 1 | (request) | 20 s | Amelia greeted, **invoked `bmad-walkthrough` via the Skill tool** (not on her menu), no sprint status found, asked "HEAD is `ed2c9c0` on `master` ... is this the change you want to review?" |
| 2 | "Yes" | 41 s | Picked `spec-b2` by `baseline_commit`; `spec-only`, so it generated a trail; Orientation (intent verbatim from spec, stats: 2 files, ~60 logic lines, 0 new public interfaces) **and** the Walkthrough in one message: 4 concerns (close the leak at three exits; comment now claims a module-wide guarantee; six tests, one per I/O-matrix row; bookkeeping outside git in untracked `_bmad-output/`). Ended "say **next**". |
| 3 | "Proceed" | 16 s | Treated as "next". Detail pass: 3 risk spots: `[public API]` `addNote` identity change (noted it overrides story 1's frozen Never "on your earlier decision"), `[public API]` same on `addTag`/`removeTag`, `[security]` copy depth (nested fields would leak; only a comment guards it). "The spec's Spec Change Log is empty." |
| 4 | "deep dive on the 3 noted areas to come up with a better pattern and design" | 129 s | Copied src/tests to its scratchpad, confirmed the nested-field leak empirically, tested `structuredClone` in `copyNote` (76/76), proposed Option A (tested) / B (store-boundary clone, untested) + a cross-export identity test, **named which frozen-spec clauses each option overrides**, asked two decisions. Repo untouched (git status clean). |
| 5 | "neither, no doc" | 8 s | "Recorded", but no file written; back to the detail-pass menu. |
| 6 | "next" | 20 s | Testing: two `node -e` one-liners with expected output; **it ran the first on HEAD itself** ("I just ran it on HEAD and got exactly that"). |
| 7 | "approve" | 9 s | Wrap-up: confirmed approval of `ed2c9c0` as committed, "no completion step configured", asked if anything else. Nothing written. |

**Scored against predictions:**
1. Routing: **right.** Amelia called the skill though it isn't on her menu. [V-lab, trace]
2. Confirm-HEAD question: **right.** [V-lab]
3. `spec-b2` picked, `spec-only`, trail generated, `spec-b1` not mentioned: **right on all four.** [V-lab]
4. One step per human turn, no verdict of its own: **mostly.** Orientation and Walkthrough came in one message (step 1 has no halt, so that follows the files). It never judged the change; approval was Carl's. [V-lab; V, step-01/02]
5. Persona effect icon/voice only: **right.** The 💻 prefix carried through every step, and no step changed. [V-lab]

**Findings:**
- **A persona reaches skills that aren't on its menu.** The menu is a shortcut, not a boundary. [V-lab]
- **The Spec Change Log was empty after a real dispatch-route `bmad-build`.** The hardening history lived in the Review Triage Log, which the walkthrough isn't told to read; it cited those IDs anyway from reading the spec. The 2026-10-03 reading ("`## Spec Change Log` does come from `bmad-build`") is true of the template, but this build left it empty. [V-lab; I on how often]
- **The walkthrough flagged out-of-git changes:** edits under untracked `_bmad-output/` don't appear in the diff, and it said so. [V-lab]
- **"Dig into" goes beyond a correctness re-review when asked to design:** it ran prototypes and tests in its scratchpad, proposed designs, and stopped at the frozen-spec boundary. It wrote nothing to the repo and gave no verdict. [V-lab]
- **Its decisions don't persist.** "Neither, no doc" and "approve" were both acknowledged and neither was written to any file (spec, memlog, `sprint-status.yaml`). Wrap-up has a configurable completion step (empty by default). A resumed session or a teammate would find no record. [V-lab; V, step-05 "no completion step configured"]
- Template boilerplate leaked: the walkthrough's closing suggestion "party mode on whether this schema migration is safe" is the step file's example text, unrelated to this change. [V-lab; V, step-02 PRESENT block]
- Testing step: it pre-ran its own suggestion on HEAD. Honest about it, but the step is framed as the human's observation. [V-lab]

- Experiment 17 complete 2026-10-09. Lab `lab17-walk` (unchanged at `ed2c9c0`), traces `lab17-out/`.

## Experiment 18 — the same build through Amelia (`BD`) vs `bmad-build` directly (2026-10-09, Carl-approved)

**Question:** does loading the Developer persona change a build? Experiments 14 and 17 found persona mechanics unchanged for brainstorming and the walkthrough, but neither persona has principles about *how* to build. Amelia's do (`customize.toml` at the tag): "No task complete without passing tests", "Red, green, refactor — in that order", "Code comments explain why, not what", "production-ready ... free of AI-generated noise", communication style "Ultra-succinct. Speaks in file paths and AC IDs".

**Setup:** two fresh copies of `lab4-base` (Experiment 4's `notes-lib`, baseline `846e9dc`, BMAD 6.12.0, no `AGENTS.md`): `labs\lab18-direct` and `labs\lab18-amelia`. Both run at once, headless, same allowlist, same request: "Add `removeNote(store, id)` to the notes library. It returns the removed note. An unknown id must fail. Do not commit." Direct arm: `/bmad-build <request>`. Amelia arm: `/bmad-agent-dev BD <request>`. A same-day direct arm controls for model drift since Experiment 4 (2026-09-19); Experiment 4's exact prompt wasn't saved, so this one is reconstructed from its spec. Traces: `labs\lab18-out\`.

**Scoring:** Experiment 4's five conventions (`NoteError`/`E_*`; injected store, no filesystem; `tests/*.spec.js` with `node:test` + `memoryStore`; `nN` ids untouched; export at the bottom), route, questions asked, review counts, the `nextId` id-reuse finding, time, and from the trace: **the order of the first edit to `tests/` vs `src/`, and whether a failing test run comes before the first `src/` edit.**

**Predictions:**
1. Both arms: `oneshot` route, no questions, 5/5 conventions, the id-reuse finding deferred, no commit. Same as Experiment 4.
2. **Amelia dispatches `BD` straight to `bmad-build`** (clear intent, no menu shown).
3. **Test-first: no difference.** Once `bmad-build` loads, its own step files drive the implementation order, and the persona's principles are context, not instructions the build follows. Both arms edit `src/` first or both test first; neither runs a deliberate red test. Low-to-moderate confidence; this is the prediction most likely to be wrong.
4. Final message: Amelia's shorter and more path-dense; the direct arm's more narrative.
5. One run per arm, so any difference smaller than Experiment 3's triage variance (a finding patch-vs-defer) is noise.

**Result (both arms 2026-10-09; traces `lab18-out/direct.jsonl`, `amelia.jsonl`; analysis script `lab18-out/analyze.py`):**

| | Direct `/bmad-build` | Amelia `/bmad-agent-dev BD` |
|---|---|---|
| Dispatch | slash command loads the skill | Amelia called `bmad-build` via the Skill tool, no menu shown |
| Route | `oneshot` | `oneshot` |
| **Order** | spec → **`src/` edit** → tests → green (6/0) | spec → **tests (two edits) → run: 4 pass / 2 fail (red)** → `src/` edit → green (6/0) |
| Review | Blind Hunter subagent | Blind Hunter subagent |
| After review | 1 test tightened, 6/0 | 2 tests added, 7/0 |
| `src/` code | `removeNote` 9 lines, `filter(n => n.id !== id)` | same 9 lines, `filter(n => n !== note)` |
| Conventions | 5/5 | 5/5 |
| Id-reuse finding | **halted for a decision** (3 options: accept, counter in the store, random ids; recommends accept) | **halted for a decision** (2 options: accept and pin with a test, or back to planning) |
| Spec status | `in-progress` | `in-progress` |
| Time / turns | 88 s / 18 | 134 s / 31 |
| Commit | none | none |

**Scored against predictions:**
1. Same route, conventions and no commit: **right.** "No questions": **wrong for both arms.** Both halted on the id-reuse finding instead of deferring it (see below).
2. Amelia dispatched `BD` straight to `bmad-build`: **right.** [V-lab]
3. **Test-first, no difference: wrong.** Amelia's arm wrote the tests first, ran them red (2 failing), then wrote `src/`; the direct arm wrote `src/` first. `bmad-build`'s step files have no test-first instruction (grep for test-order wording across the installed skill), so the order came from the persona's "Red, green, refactor — in that order". **The persona's principles carry into the skill it dispatches.** One run per arm. [V-lab; I on the cause]
4. Amelia's final message shorter: **wrong / no difference.** Similar length; Amelia's had the 💻 prefix and framed the choice as two options instead of three. [V-lab]
5. Noise caveat stands: the 1-test vs 2-test patch difference and 3 vs 2 options are within Experiment 3's variance.

**Findings:**
- **First observed persona effect on behavior, not just voice.** Brainstorming (Experiment 14) and the walkthrough (Experiment 17) ran unchanged under a persona; a build under Amelia followed her TDD principle. The difference: those personas' principles didn't speak to the skill's work, and Amelia's do. It cost 46 s and 13 turns more here. [V-lab, one run per arm; I on the generalization]
- **Both arms escalated the id-reuse bug to a human decision. Experiment 4 (2026-09-19, same repo, no `AGENTS.md`) deferred it silently, and Experiment 4b found that only the context-primed run escalated.** Today both arms escalated with no context file. So 4b's "context changes escalation" is confounded: either model behavior changed since 2026-09-19 or escalation varies run to run. Experiment 4b's result is now `[?] re-check`; one more pair of runs would be needed to separate the two. [V-lab; ? on the cause]
- Both returned the stored `note` object from `removeNote`, the same live-reference pattern as retrospective finding B1. Neither review flagged it. Same in both arms, so not a persona effect. [V-lab]
- Both runs took a third of Experiment 4's 389 s (88 s and 134 s). [V-lab]
- Both left at the id-reuse decision, unanswered (no need to answer for the research).

- Experiment 18 complete 2026-10-09. Labs `lab18-direct`, `lab18-amelia` (uncommitted changes, specs `in-progress`).
