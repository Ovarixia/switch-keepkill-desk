# Judge reproduction — stub

TODO(tranche 2): verify this walkthrough on a clean local setup and add real
screenshots. The approximate 15-minute target assumes prerequisites installed.

Prerequisites: a Mac, Docker, Switch Console v0.40.1, a Codex account signed in,
Python 3.11+ with timezone data, and the repository available locally.

1. Minutes 0–3: follow README installation; run ruff and pytest.
2. Minutes 3–7: Console → Add server local → Codex → Templates → import YAML;
   use `team=ovx` and bundled Mattermost. Set Auto ON and Bypass OFF.
3. Minutes 7–10: open Mattermost; paste a synthetic opportunity in intake.
   Observe the scout's facts and addressed hand-off to review.
4. Minutes 10–13: human saves facts.json in the checker's own directory and
   confirms Europe/Paris. Observe check, deadline conversion and BRIEF.md.
5. Minutes 13–15: human reviews the brief, chooses KEEP or KILL, and records
   the decision in the room Decisions. Repeat with a missing deadline if time.

Known limits: no live Switch run verified in tranche 1; no URL verification,
scraping, automatic fact-file write, automatic decision or submission. The
human file hand-off is intentional because the checker's only allowed write
is BRIEF.md. Provider access and local permissions require human setup.
The 15-minute estimate is TODO(tranche 2), not a measured result.
