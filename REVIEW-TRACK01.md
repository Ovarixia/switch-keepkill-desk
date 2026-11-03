# Track 01 judge review — KEEP/KILL Desk

Reviewed commit: `be7aee6` (`main`), public repo `Ovarixia/switch-keepkill-desk`.
Review date: 3 November 2026. Contest deadline: **7 November 2026, 19:29 Europe/Paris**.
Scope: significant chances of winning Track 01 Best Business Workflow. No product changes in this review.

GitHub Actions run `41720698496` on this commit is success (ruff + pytest, Python 3.11 and 3.12). `evidence/verification/pytest-green.txt` records 57 passed. The repository is public and MIT.

## Verdict

A Track 01 judge who clones the repo gets a careful, honest, offline deadline desk and a two-room Switch template. A judge who scores the **workflow** gets a contest-triage form (track, prize, AI-tools flag), one historical Switch smoke of an **older** brief, and a silent slide film. The business story the README sells — Paris 17:00 is Toronto 11:00, six hours of bid effort against twelve hours of capacity, a human who then commits — has never been executed by the agents, and no human has recorded KEEP or KILL.

That gap is the score. Honesty in the README is already good enough. Another documentation pass will not move the prize. One fresh Switch session of the shipped workflow, ending in a real human decision, plus a short live recording of that session, will.

If the fictional RFP is still the demo, record it **before 6 November 2026, 17:00 Europe/Paris** (11:00 America/Toronto). After that clock the current fixture is `EXPIRED`. An expired brief with a human KILL is a valid demo only if the submission says so. Passing `--now` in a live run to keep `66.83` / `OPEN` would falsify the evidence.

## What is already strong — leave it alone

- **The human gate in the CLI.** `Decision:` stays blank. An unexpected `decision` field is reported and cannot become `Decision: KEEP`. Complete facts and an open deadline do not approve anything. Do not add a scorer, a recommendation, or a `keepkill decide` that picks the outcome.
- **Deadline arithmetic.** IANA conversion, UTC elapsed hours across the October and March transitions, and rejection of ambiguous or nonexistent local times are tested and are the right behaviour. Do not replace elapsed hours with a business-day engine.
- **The two-agent shape.** Scout writes only `./facts.json`, checker reads `../{team}-scout/facts.json`, checker writes only `BRIEF.md`, scout is `anyone`, checker is `owner-agents`, one intake→review link, exactly two Codex agents. RUN 2108 proved this handoff. Do not add a third agent, a queue, or a web UI.
- **Offline, file-only CLI.** No URL fetch, no bid submission, PyYAML as the only runtime dependency. Keep it that way.
- **The honesty already written** in `README.md`, `docs/JUDGES.md`, `docs/SUBMISSION.md`, `docs/VIDEO-SCRIPT.md`, and `evidence/README.md`. Those limits match the artefacts. Update them only after a new live run exists. Do not soften them in advance.
- **CI, sanitization, and the French RUN 2108 report.** The workflow is green. Paths and runtime ids are redacted. `evidence/run2108/RAPPORT.md` can stay the historical record in French. Do not translate it as a project.
- **Synthetic `.invalid` URLs.** Do not point the demo at a real buyer.

## Ranked findings

### 1. The only Switch proof is an older product, on a contest fixture

**Impact: High. Effort: one Switch session on the current template. Kind: live Switch evidence.**

RUN 2108 (3 November 2026, ~21:12–21:13 Europe/Paris) is a real autonomous handoff. The scout’s write tool returned exit 0 at `21:13:07.419529+01:00` (`facts.json`, 552 bytes). The checker’s `BRIEF.md` landed at `21:13:44.347572+01:00` (804 bytes). Chat shows `keepkill check`, `deadline`, and `brief` all exit 0. Hours `94.25` and `2026-11-07 19:29 (Europe/Paris)` appear in the **deadline command output**, which is visible in `evidence/run2108/04-checker.png`.

The brief the human would have opened does not contain them. The checker’s own brief text in `evidence/run2108/handoff-receipt.json`, and `evidence/run2108/05-brief-file.png`, stop at:

- Source `2026-11-07 23:59` `Asia/Kolkata`
- Team time `(Europe/Paris): 2026-11-07 19:29`
- `Decision:` blank

There is no reference clock, no hours line, no deadline status, and no `Gate: PENDING HUMAN KEEP/KILL`. Those lines exist only in the current renderer (`src/keepkill_desk/cli.py`), shipped in `be7aee6` **after** this smoke. `evidence/sample-brief/BRIEF.md` is that renderer at a fixed clock (`--now 2026-11-03 16:10`, `66.83` hours, Toronto). The RAPPORT states the template was patched onto existing agents and was not freshly imported.

The intake in `01-intake.png` is “Atlas Local Ops Challenge”, prize USD 2000, deliverables Repository / demo video / README. It is the hackathon describing itself. It is not the EUR 8400 supplier RFP.

**Do this:** import `templates/keepkill-desk.template.yaml` into a group (fresh import, not a settings patch of the 2108 agents). Paste `fixtures/operations-rfp-source.txt` with a unique marker. Keep Auto ON, Bypass OFF. Omit `--now`. Collect the scout write-tool result, the checker’s three command results, and the on-disk `BRIEF.md`. That brief has to show both IANA names, the reference timestamp, hours remaining, and a blank `Decision:`.

### 2. The business decision is prose in `notes`, and the team zone is not a fact

**Impact: High. Effort: schema, brief renderer, template instructions, fixtures, tests — then the same live run as finding 1. Kind: code, and it counts only if that run uses it.**

The decision a Track 01 judge is scoring is whether a supplier should spend six hours of a twelve-hour window on a fictional EUR 8400 bid, paid 50/50, while the buyer’s clock is Paris and the owner’s clock is Toronto. In `fixtures/operations-rfp.json` the effort, the capacity, and `America/Toronto` sit inside `notes`. The checked fields are still a contest form: `track`, `prize`, `ai_tools_allowed`. `66.83` is elapsed UTC time, including the night. A judge who reads only the Deadline section will treat it as slack.

The checker chooses `--to` from instructions, not from a validated field. The template says to use the team zone “already supplied in the room; otherwise ask only for that timezone (demo: Europe/Paris)”. The judge script’s team zone is `America/Toronto`, written as a preamble line in `fixtures/operations-rfp-source.txt`. One agent that follows the parenthetical writes a Paris brief for a Toronto owner, and the dual-zone story is gone. RUN 2108 did not catch this: that intake already said “Team timezone confirmed: Europe/Paris”.

**Do this, before the live run, and do not ship it unless that run includes it:**

- Add `team_tz` as a required IANA field. The checker passes it as `--to`. Delete the Europe/Paris demo default from the instructions.
- Add numeric `bid_effort_hours` and `capacity_hours`.
- In the brief, print three labelled numbers: elapsed hours, bid effort, stated capacity. A comparison such as “stated effort is within stated capacity” is a fact check. It must not print KEEP or KILL.
- Leave payment terms as text. Do not estimate margin.

If this cannot be finished and replayed, skip it and run finding 1 on the current code. An unrehearsed schema bump repeats the mistake `be7aee6` already made.

### 3. No human has kept or killed anything

**Impact: High. Effort: the last minute of the same Switch session. Kind: live Switch evidence.**

Every artefact leaves `Decision:` blank, on purpose, and then stops. The instructions tell the human to record KEEP or KILL in review-room Decisions. Nothing in the public evidence shows that recording. For this track the gate is the product. A blank line proves the agents can halt. It does not prove a person used the brief.

**Do this in the same session, after the agents stop:** the human writes one Decisions entry. Cite bid effort, stated capacity, the 50/50 payment, and the team clock. Do not cite “hours remaining are positive” as the reason. Publish the decision text next to the brief. The CLI still does not store or choose it.

### 4. The submission film is a silent montage of the old smoke

**Impact: High. Effort: capture the session in finding 1; hosting is separate. Kind: docs/demo, then human submit.**

`docs/demo/keepkill-desk-demo.mp4` is 150.0 seconds, 1920×1080, H.264, silent. `docs/demo/manifest.json` and `docs/demo/captions.srt` describe ten 15-second slides. Five slides are cropped RUN 2108 screenshots. Two slides quote the fixed-clock sample brief and say that output is not from Switch. The captions are accurate. A judge who presses play still sees slides, a hover-tooltip crop on `04-checker.png`, and a Quick Look window of a brief that has no hours line.

**Do this:** a 60–90 second screen recording of the new session: intake paste, scout write result, checker brief with both zones and hours, human typing the Decisions line. Burned-in captions are enough if there is no narration. That file replaces the montage as the **submission** video. Keep the montage in the repo as a labelled fallback; do not upload it as the entry video.

Public hosting of that file is still a human action (`docs/SUBMISSION.md` marks the URL as TODO).

### 5. The entry is not submitted

**Impact: High. Effort: portal fields. Kind: human submit.**

`docs/SUBMISSION.md` still has three TODOs: public video URL, registration, contest submission. Without them the rest of this list cannot win. Copy has to describe the new run. It must not say RUN 2108 or the montage demonstrated the RFP brief, the hours line inside `BRIEF.md`, or a completed human decision.

Deadline for that human submit: **7 November 2026, 19:29 Europe/Paris**.

## Must-do before submit

Do them in this order. Stop after 5.

1. **Code, only if the live run will use it.** `team_tz`, `bid_effort_hours`, `capacity_hours`, and three labelled numbers in the brief. Checker instructions take `--to` from `team_tz`. No Europe/Paris demo default. No KEEP/KILL text. If this slips, skip it.
2. **Live Switch.** Fresh import of the YAML you will actually submit. Paste the RFP source. Omit `--now`. Prove scout write, checker `BRIEF.md` (both zones, reference time, hours, blank decision), and — if step 1 landed — effort and capacity. Do this before **6 November 2026, 17:00 Europe/Paris** if the story is an open window.
3. **Human decision** in review-room Decisions, with a reason that uses capacity and payment terms. Agents stay stopped.
4. **60–90s live recording** of steps 2 and 3. That is the submission video.
5. **Human submit** before **7 November 2026, 19:29 Europe/Paris**: public URL, registration, portal text that matches step 2.

## Nice-to-have

- A ten-line English header on `evidence/run2108/RAPPORT.md` that points judges at the new run and states that the 2108 brief has no hours line. Do not translate the report.
- Scout runs `keepkill check` on its own `facts.json` before the handoff, so the agent’s inline Python in the 2108 receipt is not a second schema. Low impact once the checker already validates.
- Blank lines under the gate for the human’s capacity note and commercial note. Useful only after finding 2 is visible.
- Replacing `04-checker.png` because a tooltip covers the French sentence. Irrelevant once finding 4’s recording is the thing judges watch.

## Do not build

A multi-opportunity queue, a margin or profit score, URL verification, a third agent, a web app, a business-day calendar, or a CLI command that writes KEEP or KILL. Any of those spends the session that should be the live run.

## Claims checked against the tree

| Claim in the review brief | What the repo shows |
| --- | --- |
| Scout writes `./facts.json`; checker reads `../{team}-scout/facts.json` | Template instructions and kickoff. RUN 2108 used `../ovx-scout/facts.json`. |
| Current brief has both IANA zones, a reference timestamp, hours, and a pending gate | `render_brief` and `evidence/sample-brief/BRIEF.md`. |
| CLI never chooses KEEP/KILL | `Decision:` is a fixed blank line. `test_complete_facts_cannot_supply_human_decision`. |
| USP after the five-gap commit was not replayed in Switch | `be7aee6` adds hours-in-brief, the RFP fixture, DST cases, and the montage. RAPPORT and the 2108 brief predate those lines. |
| Demo is a silent 150s montage | `video-probe.json`, manifest, captions, and the MP4 duration `150.000000`. |
| CI green, 57 tests, 3.11 and 3.12 | Actions run `41720698496` success. Local receipt: `57 passed`. |
| Full ~$10k pool is not a credible claim | README already limits itself to a practical Track 01 entry. Keep that sentence. |
