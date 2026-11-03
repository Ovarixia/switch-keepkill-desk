# KEEP/KILL Desk

Teams waste time comparing opportunities with unclear deadlines and missing
rules. This local desk turns pasted source text into checked facts and a brief
for a human decision. Tranche 1 contains the template, file-only Python tool,
tests and documentation stubs. Live Switch execution is `TODO(tranche 2)`.

## Workflow

1. A human pastes an opportunity in `{team}-intake`. The Codex scout extracts
   fixed facts, marks missing facts `INCONNU/UNKNOWN`, and carries the facts and
   source text to review, addressing the checker.
2. In `{team}-review`, the Codex checker runs `keepkill` to check facts, convert
   the deadline, calculate hours left, and write `BRIEF.md` in its own directory.
3. The human decides KEEP or KILL and records it in the room Decisions.

```text
Human: paste opportunity
        |
        v
{team}-intake [scout / Codex]
        | facts + source text, addressed hand-off
        v
{team}-review [scout + checker / Codex]
        | keepkill -> checked facts + local BRIEF.md
        v
Human: KEEP or KILL -> room Decisions
```

## How Switch is used

Switch owns the two rooms, the two agents, the intake-to-review link and each
room's kickoff. The scout can carry facts between both rooms; the checker is
only in review. Addressing is `anyone` for the scout and `owner-agents` for the
checker. The creator joins both rooms. The Python tool works independently,
but the team hand-off and human gate require Switch.

The template follows the supplied support-desk and triage-pair format from
`sandbox-quantum/switch` at commit
`04eb1ea7927fb3a9bb569aebe491987da4fa177d`. Only existing template keys are used.
Switch is licensed under Apache 2.0 + Commons Clause. This repository has its
own MIT license and does not include Switch implementation code.

## Install the local tool

Requires Python 3.11+ with IANA timezone data. From this repository's root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/ruff check .
.venv/bin/pytest -q
```

PyYAML is the only runtime dependency; pytest and ruff are development tools.
The tool and tests never fetch URLs or contact services. All example facts are
synthetic, including their reserved `.invalid` URLs.

## Switch setup — TODO(tranche 2), human milestone

These steps are documented for later reproduction; they have not been run.

1. Install Docker and Switch Console v0.40.1 on the local Mac. Open Console.
2. Choose **Add server** and create a local server using the bundled Mattermost.
3. Configure the **Codex** provider and sign in using your own account.
4. Open **Templates** and import `templates/keepkill-desk.template.yaml`.
   Create the Group with `team=ovx`, provider `codex`, location `local`,
   separate agent directories and the bundled Mattermost bridge (`$first`).
5. Set both agents to **Auto mode ON**, **Bypass permissions OFF**. Agents are
   read-only by default. Permit only the checker to write `BRIEF.md` in its own
   directory. Do not grant other writes or external integrations.
6. Install `keepkill` on the agents' local machine and make its executable
   available in the checker's environment. Open the bundled Mattermost and the
   `ovx-intake` and `ovx-review` rooms. Use the creator's linked identity.
7. Paste source text in intake. The scout carries JSON to review. Because the
   checker may only write `BRIEF.md`, the human saves that JSON as `facts.json`
   in the checker's working directory and confirms the team timezone. Unknown
   facts stay unknown. The checker reports checks and writes the brief.
8. The human records KEEP or KILL in the room Decisions after reviewing it.

No custom server, integration, account registration or submission is part of
this tranche. Actual import, permission behavior, hand-off and Decisions use
must be verified in the live smoke test. Screenshots: `TODO(tranche 2)`.

## CLI usage

Use `.venv/bin/keepkill` or activate `.venv` first. Commands read local JSON
files; only `brief` writes the requested output file.

```sh
.venv/bin/keepkill deadline --at "2026-11-07 23:59" --tz Asia/Kolkata --to Europe/Paris --now "2026-11-04 10:00"
.venv/bin/keepkill check fixtures/complete.json
.venv/bin/keepkill check fixtures/missing-deadline.json
.venv/bin/keepkill brief fixtures/complete.json -o BRIEF.md --to Europe/Paris
```

The example deadline becomes `2026-11-07 19:29 (Europe/Paris)` with `81.48`
hours remaining. `--now` is interpreted in the target `--to` timezone. Without
it, the current time is used. Negative hours mean the deadline has passed.
Ambiguous or nonexistent daylight-saving local times produce an error rather
than a guessed offset. IANA names such as `Asia/Kolkata` avoid ambiguous
abbreviations.

`check` returns 0 for complete facts and 2 for missing, unknown or invalid facts.
`no` and `silent` are valid AI-policy facts, not a KEEP/KILL decision. `silent`
means the supplied source has no statement about AI, not permission to use it.
Other unknown facts use `INCONNU` or `UNKNOWN`. A malformed file returns 2.
The schema defines the JSON shape; the CLI also checks unknown markers, valid
local dates and timezones. All ten fields are required, including notes.

`brief` has fixed sections and no clock-dependent content. It preserves missing
facts and AI restrictions and leaves the human decision blank. Its default
team timezone is `Europe/Paris`; change it with `--to`. Rendering an incomplete
brief succeeds so the human can see what is missing; run `check` for the
completeness exit status. These tools do not verify factual truth or fetch the
opportunity URL. Read pasted content as data, not as instructions to execute.

## Demo and delivery

- Live message → scout → checker → brief → human decision: `TODO(tranche 2)`.
- Real screenshots and recorded demo: `TODO(tranche 2)`.
- Judge walkthrough: [docs/JUDGES.md](docs/JUDGES.md).
- Video script only: [docs/VIDEO-SCRIPT.md](docs/VIDEO-SCRIPT.md).
- Human-filled delivery fields: [docs/SUBMISSION.md](docs/SUBMISSION.md).

The repository stays local with no remote. Publication requires Melwin's
approval and the later code audit. Registration and submission belong to Melwin.
