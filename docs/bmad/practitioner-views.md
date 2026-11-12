# Practitioner Views: Secondary Sources Checked Against the Lab

!!! tip "TL;DR"
    The first source (S1, January 2026) is a critique of BMAD as it stood at a 6.0 alpha, eight months and two restructurings before the release this wiki describes. About half its complaints don't fit 6.12: the roster, document sharding, and "too heavy for small work" have all changed. The other half match what the lab saw: artifacts that fall out of sync, runs that report done when they aren't fully done, and output that varies between runs. Token cost, the learning curve, and dependence on strong models were never measured here. The second source (S2, October 2026) compares installing v6.12 and v7. It is right where it copies BMAD's current install page and wrong in three places: it attributes v6 installer changes to v7, puts a v7 setup step into v6.12, and points to a plugin marketplace that BMAD itself calls stale. The third (S3, BMAD's author on YouTube) matches the v7 docs on epic folders and stories planned at build time. Its specific numbers and bmad-loop's internals are unverified, and the captions are poor.

## S1: "Limitations of BMAD Method" (asantos2000, 2026-01-10)

**What it is.** A literature-style critique on a personal blog ([asantos2000.github.io/blog/post-3](https://asantos2000.github.io/blog/post-3/)). It mostly aggregates others: three Medium comparisons, one practitioner blog (J. Cochran, 2025), two Reddit threads, a LinkedIn post, and a Medium piece on v6 token savings. All ten references are dated 2025. The author's own experience isn't reported. Evidence types below come from how the article itself attributes each point.

**Which BMAD it describes.** The article says "as of v6" and describes step files and document sharding. On its publication date, the current release was a 6.0 alpha (`6.0.0-alpha.23` shipped 2026-01-11) [V, CHANGELOG at tag `v6.12.1`]. Since then:

- The Scrum Master and QA agents were removed (6.3.0, 2026-04-09). [V, CHANGELOG v6.3.0]
- `bmad-shard-doc` was retired with no replacement (6.11.0). [V, CHANGELOG v6.11.0]
- `bmad-spec` and `bmad-build` became the center of the method. [V, P1/P2; Finding 1 in STATE]

Read it as a description of an earlier BMAD, not of 6.12. [I]

| # | S1 claims (its evidence) | Against 6.12 and the lab |
|---|---|---|
| 1 | **Rigid, over-structured, "excessive" for small projects.** "Rigid until you understand when to streamline" (Cochran). (Practitioner quote, opinion.) | **Mostly superseded.** 6.12 sizes the work: a small change can go straight to `bmad-build` with no spec, and the official tutorial does exactly that. [V, P3, P38] In the lab, a small change in an existing repo took ~6.5 min with no questions asked. [V-lab, Experiment 4] Ceremony still shows up as halts for human decisions (review triage menus, the dirty-tree checkpoint). [V-lab, Experiments 3, 5h] |
| 2 | **"Rigid" also means changing requirements force costly re-sharding.** (Author's analysis.) | **Doesn't apply.** Sharding is gone (above). A requirement change in 6.12 goes through `bmad-spec` and `bmad-correct-course`. The lab ran that loop end to end, and the cost was mainly human questions, not reprocessing. [V-lab, Experiments 5 to 5f] |
| 3 | **Agents assumed reliable.** One user spent "9+ hours" and got an auth system the pipeline marked complete while broken; another was told bugs were fixed when they weren't. (Two Reddit anecdotes.) | **Agrees in kind, not identical.** The nearest lab analogue: a true headless `bmad-spec` call returned `complete` with three open questions, and an unapproved assumption written into the contract. [V-lab, Experiment 21] Related but different: a latent defect (B1) passed every story-level review and a whole-epic review, and only the retrospective caught it. [V-lab, Experiments 5i, 10; [systemic-findings.md](systemic-findings.md)] That is a missed defect, not a false "done". No lab run produced broken code reported as passing: test suites were green and were checked independently. [V-lab, Experiments 5h, 20] |
| 4 | **Steep learning curve,** ~two months to master (Cochran); "50+ commands" overwhelm newcomers. (Practitioner estimate, cited comparison.) | **Untested.** The lab measures behavior, not learning time. 6.12's own answer is the shortest path plus `bmad-help`, which recommended spec → build for a tiny idea. [V-lab, Experiment 1; V, P38] |
| 5 | **Agents fail to update all artifacts.** (User report.) | **Agrees.** It's this wiki's most repeated pattern: memlog vs `SPEC.md`, stale `stories.yaml`, Implementation Notes, a first epic's spec contradicted by a second epic's code, the epic-context cache. [V-lab, Experiments 5b to 5i, 9b; [systemic-findings.md](systemic-findings.md) "the record for the next reader drifts"] |
| 6 | **Web planning vs IDE switching.** (Cochran, practitioner description.) | **Agrees, and sharper at 6.12.** Web bundles are a separate product line, and a web-planned PRD carries no memlog into the IDE flow. [V, P37, P42] v7 removes bundles. [V, P34] |
| 7 | **High token cost.** ~31,667 tokens per workflow run before v6's step files vs ~8,333 after, "74%"; one project's monthly API cost ~$847 to ~$220; one developer "~230 million tokens in a week". (A secondary Medium analysis of one project; one Reddit anecdote.) | **Untested; not verified.** The lab recorded wall-clock time (6.5 to 32 min per build), not tokens. Time is not a proxy for tokens. [V-lab] The 6.12 changelog makes its own performance claims, also without published data. [V, P42] |
| 8 | **Depends on advanced models with large context.** (Cited; one anecdote from a "free big model" user.) | **Untested.** Every lab run used Claude Code with a frontier model. [V-lab] |
| 9 | **Scale and time.** "6–15 minutes of upfront planning before any code, even for a modest feature" (Cochran); one project took ~8 h vs minutes with OpenSpec (cited, flagged by the author as possibly extreme). | **Roughly consistent on time.** Small builds took ~6.5 min end to end; a three-reviewer build took ~32 min; a full brainstorm took 25 min. [V-lab, Experiments 2, 4, 7] No comparison against another framework was run. |
| 10 | **Reproducibility:** non-deterministic output. (Author's analysis plus one report.) | **Agrees.** Triage verdicts on the same finding varied between runs, and repeated brainstorming runs differed. [V-lab, [systemic-findings.md](systemic-findings.md) "triage verdicts are one sample"; Experiment 14b] |
| 11 | **Mirrors Product Owner / Scrum Master roles;** agents Analyst, PM, Architect, Dev, QA. | **Disagrees with 6.12.** There are five agents: Mary, John, Winston, Sally, Amelia. No Scrum Master or QA agent; QA work sits in skills and the separate TEA module. [V, P2, CHANGELOG v6.3.0; V-lab, Experiment 8] |
| 12 | **Guardrails:** sandboxed commands and an experimental LLM "judge" consensus mechanism. (Cited from a Medium piece.) | **Not found as described.** 6.12's equivalent is independent review subagents with triage. No "judge consensus" feature appears in the docs read. [?] Not searched for exhaustively. |

**Net.** The critique still holds where it concerns how LLM workflows behave: drift, false completion, variance. Where it concerns BMAD's structure, it describes an earlier version. [I] Someone reading S1 today should take items 3, 5, 6 and 10 seriously and discount items 1, 2 and 11 for version. [I]

## S2: "BMAD Method v6.12 vs v7" (Hakky Handbook, last updated 2026-10-24)

**What it is.** A Japanese install-and-setup comparison on Hakky Inc.'s handbook site, bylined "Hakky AI." There's no claim of hands-on use: it cites the official install docs, the add-modules page, and two `CHANGELOG.md` permalinks, `1cbcfa27` (2026-09-28) and `abe4eb1b` (2026-09-05). It covers install, prerequisites, updates, and module handling only. It says nothing on review defaults, ticketing, or the workflow skills. Checked against tag `v6.12.1` and against BMAD's `main` branch at `e734d3a` (2026-11-06, read 2026-11-07). [V-lab for the commit lookup]

| # | S2 claims | Against the release, current `main`, and the lab |
|---|---|---|
| 1 | **v6.12 is the stable line, "frozen except for bug fixes"; v7 is a preview alpha whose spec changes often.** | **Agrees.** Main's README says v6.12 is "frozen aside from bug fixes" and v7 is "in preview alpha". [V, main `README.md`] |
| 2 | **v6.12 installs with `npx bmad-method install`, an interactive installer that also picks modules.** | **Agrees.** [V, P38, P27; V-lab, Experiments 1, 8] |
| 3 | **v6.12 needs Node 20.12+, Python 3.10+, and `uv`.** | **Partly.** Main's install page says exactly this for v6.12. [V, main `docs/start/install-bmad.md`] But the v6.12.1 tag's own install page lists Node 20.12+ and `uv` and never names a Python version. `uv` only warns when missing; it doesn't block the install. [V, P38] Main's changelog also says Python "leaves the prerequisites" once scripts move to `uv run`. [V, main `CHANGELOG.md`] The primary sources disagree with each other. Python 3.10 is not a v6.12 requirement anywhere in the v6.12 docs. [I] |
| 4 | **After a v6.12 install, open Claude Code and ask the `bmad` skill to run `bmad setup`.** | **Disagrees.** `bmad setup` is a v7-preview skill. Main's install page puts it after the line "The rest of this page does not apply to v6.12". [V, main `docs/start/install-bmad.md`; P34] The lab only met it in the v7 migration run. [V-lab, Experiment 19] |
| 5 | **v7 installs from the Claude Code plugin marketplace (`/plugin marketplace add bmad-code-org/bmad-plugins`), as `bmad-method` plus `bmad-core-tools`.** | **Out of date.** Main's install page leads with the Skills CLI (`npx skills add bmad-code-org/BMAD-METHOD ...`). It says the marketplace "was last built before v7 and still carries the earlier skills", so install with the Skills CLI until it is rebuilt. [V, main `docs/start/install-bmad.md`] The lab installed v7 with `npx skills add`. [V-lab, Experiment 19] The plugin names themselves match main. [V] |
| 6 | **v7 setup puts the runtime and module scripts under `_bmad/`; entry points are `bmad setup` and `bmad status`.** | **Agrees.** [V, main `docs/start/install-bmad.md`; V-lab, Experiment 19] |
| 7 | **v7's breaking changes:** custom-content install removed, the community-module picker removed (use `--custom-source`), `--tools none` refused, `--yes` needs an explicit `--tools <id>`. | **Wrong release.** These are all v6 changes, shipped months before the v7 draft. Custom content was removed in 6.3.0 (2026-04-09), `--tools none` in 6.6.0 (2026-04-28), and the picker in 6.7.0 (2026-05-17). [V, CHANGELOG at tag `v6.12.1`] Anyone on 6.12 already has them. They aren't news for v7. |
| 8 | **Scripts that call `python3` directly are deprecated; use `uv run`.** | **Agrees, with timing.** 6.x announced that v7 would standardize on `uv run`, and main has moved the remaining call sites. [V, main `CHANGELOG.md`] |
| 9 | **v7 updates can break an existing setup, need a migration check, and need `bmad setup` re-run afterward. v6.12 updates need no per-update migration check.** | **Agrees on v7.** Main's install page warns that "updates can break an existing setup". [V] The lab saw `bmad migrate method` and setup re-runs. [V-lab, Experiment 19] **On v6.12, "no migration check" isn't the whole story:** a 6.x update can still overwrite a skill's `customize.toml` and strand override files renamed in 6.11. [V-lab, Experiment 13; V, P42; [updating-bmad.md](updating-bmad.md)] |

**Net.** S2 is accurate where it copies main's current install page (status, the v7 entry points, `uv`). It goes wrong in three places. It carries a v7 step back into v6.12 (`bmad setup`). It recommends a marketplace that main itself says is stale. It files April–May 6.x installer changes under v7. [I] A reader moving to v7 should start from main's install page, not from S2. [I]

**Primary facts found while checking S2.** These came from reading main, not from S2, and are logged here so they aren't lost:
- Main's README gives a v7 release ETA of "mid-November 2026, and it might be sooner". [V, main `README.md` @ `e734d3a`]
- v6.12 source and docs now live on a `V6.12` branch. [V, main `README.md`]
- Main is now 61 commits past the `bda3c59` commit this wiki's v7 page describes. [V-lab, `git rev-list`] [v7-preview.md](v7-preview.md) may therefore be out of date. A refresh is its own unit.

## S3: BMad Code YouTube channel (BMAD's author)

**What it is.** Brian's own channel: demos, live sessions with community guests, and v7 previews. Two videos read so far, from auto-captioned transcripts (`data/fabric/bmadcode/`, gitignored). **The captions are poor:** the Live Ep 5 track reads like a machine translation of a translation ("Be Mad", "BDD" for BMAD), so nothing below is a quote, only paraphrase. Author statements are still secondary until a doc or lab backs them. Added 2026-11-10 on demand; not reviewed.

### S3a: "How Teams Run BMad at Scale", Live Ep 5 (2026-10-17, with Tim Dickey)

| # | S3a says | Against the docs and the lab |
|---|---|---|
| 1 | **In v7 each epic is its own folder whose epic file is the spec. The single sprint-planning file goes, and stories aren't written up front; each is planned as it's built.** | **Agrees.** `epics.md` and `sprint-status.yaml` become the ticket tree, and "an entry needs no file to be built". [V, P34 ticket-tree doc] The lab built a story with no story file. [V-lab, Experiment 20] |
| 2 | **The epic, not the story, is now one developer's unit of work. Aim for about 7 to 11 stories per epic.** | **First half agrees:** "An epic is one capability that one owner delivers to production." [V, P34 ticket-tree doc] **The 7 to 11 figure wasn't found** in the v7 skills and planning docs at `bda3c59` or `main` @ `e734d3a` (searched, not read in full). [?] Treat it as the author's guidance. |
| 3 | **Long planning documents become folders of small files with one main file; the old mechanical sharding is gone.** | **Partly.** v7 writes each document as `<type>-<slug>/<type>-<slug>.md`. [V, P34 CHANGELOG] `bmad-shard-doc` was retired with no replacement. [V, CHANGELOG] A split into several files inside the folder wasn't seen in the files read. [?] |
| 4 | **"Too heavy" is a misreading of old versions: one skill can build directly, and it runs review lenses and tests before calling the work done. The lenses can be configured.** | **Agrees.** Same as S1 row 1. [V, P3, P38; V-lab, Experiment 4] `bmad-build`'s `customize.toml` defines the review layers at 6.12.1 and quick/thorough lens sets in v7. [V, `customize.toml` at both versions] v7's default quick review ran one subagent in the lab. [V-lab, Experiment 20] |
| 5 | **A meeting transcript can go straight into planning and come out as an epic.** | **Docs agree on the input:** `bmad-ticket` accepts "a PRD alone, meeting notes, or a one-paragraph idea". [V, P34 ticket-tree doc] Not tried in the lab. |
| 6 | **The v7 `bmad` agent can suggest other installed skills, and steers trivial work away from the full method.** | **Not checked.** [?] |
| 7 | **Use the strongest model for planning and a cheaper one for coding; planning tokens pay for themselves.** | **Untested.** Every lab run used a frontier model. [V-lab] Same gap as S1 row 8. |
| 8 | **AI amplifies whatever practice a team already has: the bottleneck moves to pipelines, code review and requirements. Prefer continuous delivery from main, with feature flags.** | **Opinion, outside BMAD's docs.** It fits the docs' own premise that human attention is "the most expensive resource". [V, P8] [I] |
| 9 | **Output quality depends on the person steering: state your own view and ask the model to challenge it.** | **Consistent with the lab.** A headless `bmad-spec` run returned `complete` with open questions when nobody steered it. [V-lab, Experiment 21] [I] |

### S3b: "bmad-loop First Look" (2026-07-07, with Paul, "Pinky D")

| # | S3b says | Against the docs and the lab |
|---|---|---|
| 1 | **bmad-loop replaces the experimental "automator" and installs as an option in the BMAD installer.** | **Agrees.** 6.10.0 (2026-07-03) added `bmad-loop` as an opt-in module and deprecated `bmad-automator`. [V, CHANGELOG v6.10.0] Its registry entry points to its own repo, `github.com/bmad-code-org/bmad-loop`: "Builds, verifies, and retros a whole epic unattended", not selected by default. [V, `bmad-modules.yaml` @ v6.12.1] There is no separate `bmad-loop` npm package (404). [V-lab] |
| 2 | **It runs a whole epic, or chosen stories with a cap, and can pick up a project already half done.** | **Partly.** At 6.12 it walks a spec folder's `stories.yaml` in list order. It is a linear scheduler with no dependency graph, and selecting one story runs only that story. [V, P15] The video's demo read `sprint-status.yaml`, the 6.10 layout. [I] |
| 3 | **Each story is built by an unattended worker that follows spec status and escalates to a human when stuck.** | **Agrees.** The worker was `bmad-dev-auto` in 6.10, renamed `bmad-build-auto` in 6.11. [V, CHANGELOG; [updating-bmad.md](updating-bmad.md)] `blocked` is meant as a routing signal, not just a failure. [V, P15] Never run in the lab. |
| 4 | **Findings that aren't this story's problem go to deferred work, and a "sweep" works through them later, two passes by default.** | **Partly.** `bmad-build-auto` reports `deferred` findings as a machine-readable list, "intentionally not a backlog"; the orchestrator decides what to do. [V, P15] The changelog names "deferred-work sweeps" as a bmad-loop job. [V, CHANGELOG v6.10.0] The sweep's behavior and limit weren't checked. [?] |
| 5 | **It runs agents in visible tmux sessions (tmux 3.2+) rather than headless calls, partly because of how headless use is billed.** | **Not checked.** bmad-loop's own repo wasn't read, and the billing point is about vendor policy. [?] |
| 6 | **Works with Claude Code, Codex, Gemini CLI and GitHub Copilot CLI through hook adapters; it can run each story in a git worktree.** | **Not checked.** [?] Same reason. |
| 7 | **Parallel work means separate epics.** (Implied by the demo running one epic at a time.) | **Agrees.** The docs say bmad-loop doesn't coordinate across a project; parallel streams need separate epic owners or a higher layer. [V, P15] This matches S3a row 2. [I] |
| 8 | **There is no v5 because a publishing script pushed 5.x versions to npm by mistake.** | **The versions exist:** npm lists `5.0.0-beta.1` through `5.1.3`. [V-lab, `npm view`] The cause is the author's account. |

**Net.** On v7's direction (epic folders, stories planned at build time, one owner per epic) the author's talk matches the docs, which makes the channel a good early signal for what a release will change. [I] Specific numbers (7 to 11 stories per epic) and bmad-loop's internals (tmux, adapters, sweep limits) are author statements only. [I] The caption quality limits what can be cited. [V-lab]

## Not yet checked

- S3: more videos still to pull (`sources.md`). bmad-loop's own repo has since been read (P43); see [loops.md](loops.md). It confirms S3b rows 5 and 6: tmux 3.2+ by default, and profiles for Claude Code, Codex, Gemini CLI, Copilot CLI, OpenCode and Antigravity. [V, P43]
- S1's underlying sources (Cochran's blog, the Medium token analysis) haven't been read directly. The figures above are quoted as S1 reports them.
- S2's two `CHANGELOG.md` permalinks were looked up but not read in full.

---

??? info "About this page"

    *Outside write-ups about BMAD (blogs, talks, videos), each checked claim by claim against the pinned release (6.12.0, read at 6.12.1) and this project's lab runs. Per the spec, a secondary source never makes a claim [V] by itself. The left column is what the source says, attributed to it. Only the right column carries [V, Pxx] or [V-lab] tags, and those cite this wiki's own evidence. Disagreements are logged rather than smoothed over (spec, Method 4). Page started unattended 2026-11-07 with S1. S2 was added the same day, on demand. S3 was added 2026-11-10, on demand. None has been reviewed.*
