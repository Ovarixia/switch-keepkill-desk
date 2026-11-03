# Switch KEEP/KILL Desk

A small business team must decide which opportunities deserve its limited bid
time. KEEP/KILL Desk turns pasted source text into a scout-owned facts file,
a checker-generated brief with **source and team IANA timezones, timestamped
hours remaining**, and a **mandatory human KEEP/KILL gate**. Switch coordinates
the two Codex agents; the local Python tool does deterministic checks. The human
owns the decision. [Public repository](https://github.com/Ovarixia/switch-keepkill-desk).

## Why this wins Track 01

This targets Track 01 Best Business Workflow by giving people and agents distinct,
reviewable responsibilities: a scout extracts evidence, a checker makes the
cross-timezone deadline and missing facts visible, and a human decides whether
to commit scarce business time. The fictional EUR 8400 supplier-intake RFP shows
why this matters: **17:00 Europe/Paris is 11:00 America/Toronto**, with **66.83
elapsed hours** left at the replay clock, six hours of bid effort and twelve
available team hours. The brief labels team timezone, bid effort and capacity
beside those elapsed hours. These are inputs to a human decision, not an automated
profitability judgement. One historical Switch run proves the file handoff;
tests and a generated brief prove the enhanced hours display. This is a practical
Track 01 entry, not a claim of a contest win or measured commercial ROI.

## Workflow and human gate

```text
Human pastes opportunity in {team}-intake
    -> scout (Codex) validates and writes ./facts.json in its own directory
    -> addressed handoff: facts + exact source + path to {team}-review
    -> checker reads ../{team}-scout/facts.json and checks marker + URL
    -> keepkill check / deadline / brief -> checker-owned ./BRIEF.md
    -> PENDING HUMAN KEEP/KILL: stop and wait
    -> human reviews and records KEEP or KILL in review-room Decisions
```

Switch owns the rooms, agents, intake-to-review link and kickoffs. The scout
belongs to both rooms (`anyone` addressing); the checker belongs only to review
(`owner-agents`). The creator joins both rooms. Exactly two Codex agents are used.
The CLI never chooses KEEP or KILL, never contacts a URL, and has no command to
submit a bid or register. Every generated brief leaves `Decision:` blank, even
when all facts are complete or the deadline is open. Source text is data, never
an authority to execute instructions or override the human gate.

The gate is mandatory in the agent workflow and visible in every brief. The
CLI does not implement approval storage or a Switch-wide authorization lock.
File-write limits are agent instructions, not file-name OS ACLs. A human can
bypass instructions manually; the project does not claim to prevent that.

## Judge quick start — nine steps

The [complete nine-step walkthrough](docs/JUDGES.md) includes exact setup and
failure criteria. All repository paths are relative to the clone root.

1. Clone `https://github.com/Ovarixia/switch-keepkill-desk.git` and `cd switch-keepkill-desk`.
2. Create `.venv`: `python3 -m venv .venv`, then `.venv/bin/python -m pip install -e '.[dev]'`.
3. Run `.venv/bin/ruff check .` and `.venv/bin/pytest -q` (at least 57 tests).
4. Replay: `.venv/bin/keepkill brief fixtures/operations-rfp.json -o BRIEF.md --to America/Toronto --now '2026-11-03 16:10'`.
5. Open a healthy local Switch/Docker server, sign in to Codex and import `templates/keepkill-desk.template.yaml`; create the Group with `team=ovx`.
6. Keep separate sibling agent directories, Auto ON and Bypass OFF; make your clone's `.venv/bin/keepkill` available to the checker and inspect rendered instructions.
7. Paste `fixtures/operations-rfp-source.txt` in intake with a unique marker; observe the scout's actual `facts.json` write and addressed handoff.
8. Inspect the checker's three commands and real brief: both IANA zones, clock, hours, labelled team timezone, bid effort and capacity when the source states them, missing facts and pending gate. Live runs use the current clock.
9. Agents stop. The human reviews and records KEEP or KILL in Decisions. No automatic external action follows.

Requirements: Python 3.11+ with IANA timezone data; PyYAML is the sole runtime
dependency. Tests and CLI are offline. Switch reproduction additionally needs
a Mac, Docker, Console and your own Codex account. The historical smoke used
Console v0.40.1, Mattermost 11.9.0 and Codex v0.163.0; clean installation and the
latest template's fresh import have not been revalidated here.

## CLI and deadline semantics

```sh
.venv/bin/keepkill check fixtures/operations-rfp.json
.venv/bin/keepkill deadline --at '2026-11-06 17:00' --tz Europe/Paris --to America/Toronto --now '2026-11-03 16:10'
.venv/bin/keepkill brief fixtures/operations-rfp.json -o BRIEF.md --to America/Toronto --now '2026-11-03 16:10'
```

Expected deadline: `2026-11-06 11:00 (America/Toronto)`; hours: `66.83`.
[`evidence/sample-brief/BRIEF.md`](evidence/sample-brief/BRIEF.md) is generated
with those exact arguments. `--now` is a local wall time in the target `--to`
IANA timezone and is for labelled replay only. Omit it for the current clock.
The brief includes its reference timestamp and UTC offset, both timezone names,
elapsed UTC hours, and `OPEN`, `DUE NOW`, `EXPIRED` or `INCONNU` deadline status.
Hours are rounded to two decimals; status uses the unrounded duration.
Negative hours mean expired, not KILL. Elapsed hours include nights/weekends;
they are not available working capacity. Recompute before making a real decision.
When the facts include them, the brief adds **Team and capacity** with the team
IANA zone, bid effort hours and capacity hours. If `--to` is omitted and
`team_tz` is a valid IANA zone, that zone is the brief clock; otherwise the
clock falls back to Europe/Paris. An explicit `--to` still overrides it, and a
difference is reported without filling `Decision:`.

DST-ambiguous and nonexistent local times are rejected rather than guessed.
Invalid or missing deadline facts render `INCONNU` hours in the brief. `check`
returns 0 for complete facts, 2 for invalid/missing facts or malformed files.
`brief` can render incomplete facts so the human can see cautions; rendering
success is not completeness or approval. A bad reference clock or timezone
returns 2 without overwriting the output. Briefs are identical for the same
facts, target timezone and explicit `--now`.

The [schema](schema/facts.schema.json) requires ten fields, including notes;
`deliverables` is a nonempty list. Optional `team_tz`, `bid_effort_hours` and
`capacity_hours` are checked when present and printed as labelled brief facts.
Omit them when the source does not state them; do not guess a number. The CLI
also checks unknown markers, dates and zones. `ai_tools_allowed` is `yes`, `no` or `silent`; `silent` never means
permission. Other missing facts use `INCONNU/UNKNOWN`. The tool checks supplied
facts, not their external truth; all fixtures and `.invalid` URLs are synthetic.

## Evidence, demo and CI

- [Public evidence index](evidence/README.md): sanitized RUN 2108 report and five screenshots. The scout wrote its file at 21:13:07 CET; the checker wrote its brief at 21:13:44, all three commands exit 0, decision blank. This proves one run with existing agents, not repeated/concurrent operation.
- [Business case and replay](evidence/sample-brief/README.md): new hours-in-BRIEF behaviour, independent of the historical smoke.
- [150-second demo MP4](docs/demo/keepkill-desk-demo.mp4), [shot-by-shot script](docs/VIDEO-SCRIPT.md), [rebuild instructions](docs/demo/README.md). Silent screenshot montage plus CLI replay; no live Switch recording is claimed.
- [CI workflow](.github/workflows/ci.yml): ruff and pytest on Python 3.11 and 3.12 for pushes and pull requests to `main`. [Actual Actions runs](https://github.com/Ovarixia/switch-keepkill-desk/actions/workflows/ci.yml) are the status authority; no unverified green badge is displayed.
- [Submission fields](docs/SUBMISSION.md): public repository and README filled; public video URL, registration and contest submission remain Melwin's actions. Nothing is uploaded or submitted by this project.

Only sequential processing is demonstrated: the next intake can replace the
single scout file. Marker/URL checks reduce stale input risk but do not provide
concurrency control. Human decision recording was deliberately not performed
in the smoke. No speed, revenue, or security-isolation benchmark is claimed.

The template follows the supplied support-desk/triage-pair key format from
`sandbox-quantum/switch` commit `04eb1ea7927fb3a9bb569aebe491987da4fa177d`.
Switch uses Apache 2.0 + Commons Clause. This repository is MIT licensed and
contains no Switch implementation code.
