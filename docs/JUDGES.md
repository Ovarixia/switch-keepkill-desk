# Judge reproduction — autonomous local hand-off

Prerequisites: a Mac, Docker, Switch Console v0.40.1, a signed-in Codex provider,
Python 3.11+ with timezone data, and the local repository. Approximate 15-minute
walkthrough; clean installation time has not been measured.

1. Follow README installation; run ruff and pytest (41 tests).
2. Import the YAML Group with `team=ovx`, local sibling agent directories and
   bundled Mattermost. Keep exactly two agents, Auto ON and Bypass OFF. Inspect
   rendered instructions: scout writes only its own facts.json; checker reads
   ../ovx-scout/facts.json and writes only its own BRIEF.md. Install keepkill in
   the checker environment. Do not widen permissions.
3. Verify Docker and Mattermost healthy. Paste one synthetic opportunity in
   intake with a unique run marker, source timezone and Europe/Paris team time.
   Observe the scout's validated JSON, its actual file write, and addressed
   hand-off to review. No human saves the facts file.
4. Observe checker check, deadline conversion and BRIEF.md. It must read the
   current scout file; absent or stale input blocks processing. It asks only
   for the team IANA timezone if that has not already been supplied.
5. Read the real brief and its blank Decision field. The human can then choose
   KEEP or KILL and record it in Decisions. The smoke stops before that choice.

Measured Smoke 2 outcome and screenshots: ../../logs/2026-11-03T2108/RAPPORT.md.
No URL verification, scraping, automatic decision or submission. Unknowns stay
unknown; silence about AI is not permission. The write limits are instructions,
not file-level ACLs. Login blocks the smoke; missing scout write means FAIL.
