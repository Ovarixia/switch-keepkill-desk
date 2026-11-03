# KEEP/KILL Desk

Teams waste time comparing opportunities with unclear deadlines and missing
rules. This local desk turns pasted source text into checked facts and a brief
for a human decision. Tranche 1 contains the template, file-only Python tool,
tests and reproduction documentation. The autonomous scout-to-checker contract
is described below; RUN 2108 evidence and its measured result are recorded in
`../logs/2026-11-03T2108/RAPPORT.md`.

## Workflow

1. A human pastes an opportunity in `{team}-intake`. The Codex scout extracts
   fixed facts, marks missing facts `INCONNU/UNKNOWN`, validates the JSON syntax
   and types, and writes only `facts.json` in its own directory. It then carries
   the facts, source text and path to review, addressing the checker.
2. In `{team}-review`, the Codex checker runs `keepkill` to check facts, convert
   the deadline, calculate hours left, and write `BRIEF.md` in its own directory.
   It reads `../{team}-scout/facts.json` without changing it, checks the current
   run marker and URL, and uses the supplied IANA team timezone or asks for it.
3. The human decides KEEP or KILL and records it in the room Decisions.

```text
Human: paste opportunity
        |
        v
{team}-intake [scout / Codex]
        | scout writes ./facts.json, then facts + source text + path
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

## Switch setup — local installation verified

Verified locally on 3 November 2026 with Switch Console v0.40.1, Docker
Desktop and the bundled Mattermost 11.9.0. Codex v0.163.0 was already signed
in; no new login or account was created during this smoke. The imported Group
template and both `ovx` rooms were inspected in Console. Both agents showed
Auto mode ON, Bypass permissions OFF and agent management OFF.

Reproduction steps:

1. Install Docker and Switch Console v0.40.1 on the local Mac. Open Console.
2. Choose **Add server** and create a local server using the bundled Mattermost.
3. Configure the **Codex** provider and sign in using your own account.
4. Open **Templates** and import `templates/keepkill-desk.template.yaml`.
   Create the Group with `team=ovx`, provider `codex`, location `local`,
   separate agent directories and the bundled Mattermost bridge (`$first`).
5. Set both agents to **Auto mode ON**, **Bypass permissions OFF**. Agents remain
   read-only by default except the scout’s `facts.json` and the checker’s
   `BRIEF.md`, each in its own directory. Keep separate sibling directories
   with their default agent names. Do not expand sandbox permissions.
6. Install `keepkill` on the agents' local machine and make its executable
   available in the checker's environment. Open the bundled Mattermost and the
   `ovx-intake` and `ovx-review` rooms. Use the creator's linked identity.
   The checker instructions call the executable by absolute path, e.g.
   `$REPO_ROOT/.venv/bin/keepkill` (where `$REPO_ROOT` is your clone of this
   repo); replace it with your own installation path. The checker's working
   directory is created by Switch, typically
   `~/.switch/agents/<server-id>/ovx-checker`, with the scout as its sibling
   `~/.switch/agents/<server-id>/ovx-scout`.
7. Paste one synthetic opportunity in intake with a unique run marker, URL,
   source deadline and source IANA timezone, plus team timezone Europe/Paris.
   The scout writes `./facts.json` before posting the addressed hand-off.
   The checker reads `../ovx-scout/facts.json`, then runs check, deadline and
   brief. Unknown facts stay unknown. No human file deposit is needed.
8. Read the real `BRIEF.md`. The human records KEEP or KILL in Decisions after
   reviewing it; agents always leave `Decision:` blank.

The relative path is option B: `workspace-write` allows a scout to write in its
own cwd without requesting access to the checker's directory. The checker only
reads its sibling's file. With custom non-sibling directories, configure the
actual scout read path in the checker instructions before starting. `{team}`
is a Switch template parameter, rendered to `ovx` for the local agents; inspect
the rendered instructions after import. No unresolved placeholder should remain.
The file-write restrictions are agent instructions, not a file-level OS ACL.

For Smoke 2, first save `docker info` and verify the existing Mattermost container
is healthy. Preserve stale checker artefacts separately before sending. Observe
the scout's actual write tool activity and the file's timestamp, hash and run
marker. Read check/deadline/brief outputs from the checker's tool results and
verify the new brief timestamp and blank decision. If the scout does not write,
report FAIL; do not manufacture the hand-off. Stop with screenshots and a partial
FAIL if login blocks. Capture the new settings and each key step.
Evidence: `../logs/2026-11-03T2108/`; consult its report for the actual outcome.
The earlier run 2032 does not prove an autonomous file hand-off.

Smoke 2 RUN 2108 passed on 3 November 2026: the scout wrote its own facts.json
at 21:13:07 CET, then the checker read that file and wrote BRIEF.md at 21:13:44.
All three checker commands returned 0. The decision stayed blank. No human or
orchestration deposited the new JSON; the scout's tool log proves the write.
This verifies one run using the existing live agents, not a clean installation
or repeated/concurrent opportunities.

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

- Smoke 2 result and real screenshots: `../logs/2026-11-03T2108/RAPPORT.md`.
- Video script only; no recording, upload or submission performed.
- Judge walkthrough: [docs/JUDGES.md](docs/JUDGES.md).
- Video script only: [docs/VIDEO-SCRIPT.md](docs/VIDEO-SCRIPT.md).
- Human-filled delivery fields: [docs/SUBMISSION.md](docs/SUBMISSION.md).

The repository stays local with no remote. Publication requires Melwin's
approval and the later code audit. Registration and submission belong to Melwin.
