# Judge reproduction — clone to one Switch run in nine steps

The local CLI/tests need Python 3.11+ and IANA timezone data. The Switch path
additionally needs a Mac with Docker, Switch Console and your own signed-in
Codex provider. The historical smoke used Console v0.40.1, bundled Mattermost
11.9.0 and Codex v0.163.0 on 3 November 2026; these are observed versions, not
claims about the latest releases. Clean installation time has not been measured.

1. **Clone the public repository.**

   ```sh
   git clone https://github.com/Ovarixia/switch-keepkill-desk.git
   cd switch-keepkill-desk
   ```

2. **Create a virtual environment and install.** Run from the clone root:

   ```sh
   python3 -m venv .venv
   .venv/bin/python -m pip install -e '.[dev]'
   ```

3. **Run the offline checks yourself.** Neither tests nor CLI fetch URLs:

   ```sh
   .venv/bin/ruff check .
   .venv/bin/pytest -q
   ```

   Expect ruff success and at least 57 passing tests. Tests cover UTC elapsed
   hours across DST, rejected ambiguous/nonexistent times and a pending human gate.

4. **Replay the business case without Switch first.**

   ```sh
   .venv/bin/keepkill check fixtures/operations-rfp.json
   .venv/bin/keepkill brief fixtures/operations-rfp.json -o BRIEF.md --to America/Toronto --now '2026-11-03 16:10'
   ```

   Inspect `BRIEF.md`: Paris `17:00` → Toronto `11:00`, `66.83` hours,
   `Gate: PENDING HUMAN KEEP/KILL`, and blank `Decision:`. This is an explicitly
   fixed-clock replay. [Expected output](../evidence/sample-brief/BRIEF.md).

5. **Prepare Switch.** Start Docker and a local Switch Console server with
   bundled Mattermost; confirm it is healthy. Configure the Codex provider with
   your account. Import `templates/keepkill-desk.template.yaml` in **Templates**,
   then create a Group with `team=ovx`, provider `codex`, location `local`, the
   bundled bridge (`$first`) and the default separate sibling agent directories.
   The creator joins intake and review. Exactly two agents are needed.

6. **Inspect the rendered agent setup before sending.** Auto mode ON, Bypass
   permissions OFF, agent management OFF. The scout writes only its own
   `facts.json`; the checker reads `../ovx-scout/facts.json` and writes only its
   own `BRIEF.md`. All `{team}` placeholders must resolve. For non-sibling
   directories configure the actual read path first. Make the installed tool
   executable available in the checker's environment: from the clone root,
   `pwd` plus `/.venv/bin/keepkill` gives your machine's full executable path;
   set that actual path in the checker instructions if PATH lacks `keepkill`.
   Do not paste a literal shell variable that the agent cannot resolve. Keep
   the default sandbox; file-name limits are instructions, not file-level ACLs.

7. **Send one intake.** Paste `fixtures/operations-rfp-source.txt` into
   `ovx-intake`. Change `RFP-DEMO-1103` to a unique marker if repeated. It supplies
   source `Europe/Paris` and team `America/Toronto`. For a live opportunity,
   use the current clock: do not pass the replay's `--now`. If this fictional
   deadline has passed, the correct result is negative hours and `EXPIRED`.
   Observe the scout's actual write tool result before its addressed handoff
   to `@ovx-checker` in `ovx-review`. A chat claim alone is insufficient.

8. **Inspect the checker run.** It must verify the current marker and URL in
   `../ovx-scout/facts.json`, run `check`, `deadline` and `brief`, and show
   source/team IANA timezones, reference time, hours remaining and cautions in
   its real `BRIEF.md`. Missing or stale files block the handoff. No human or
   orchestration deposits the JSON. Missing facts remain unknown; source
   silence about AI is not permission. `check` exit 2 is a visible validation
   result, not an approval. Failed scout write means FAIL; login blocks must
   be reported honestly.

9. **Stop at the human gate.** Agents leave the generated `Decision:` blank,
   publish `PENDING HUMAN KEEP/KILL` and wait. A human reviews the source,
   capacity, deliverables and payment terms and explicitly records KEEP or
   KILL in the review room's **Decisions**. Do not infer KEEP from positive
   hours. The historical smoke and supplied artefacts stop before this human
   action; they do not prove it was performed. No bid, account, registration,
   message outside the two rooms or submission is authorized by this demo.

Public [historical evidence](../evidence/README.md) and the
[150-second montage](demo/keepkill-desk-demo.mp4) are available without a local
Switch installation. The montage is silent, uses historical screenshots plus
an enhanced CLI replay, and is not a live screen recording. This workflow
processes one opportunity at a time: a single `facts.json` can be overwritten
by the next intake. No repeated/concurrent-run guarantee is claimed.
