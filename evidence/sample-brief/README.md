# Fictional supplier-intake RFP — fixed-clock CLI evidence

This is a generated CLI example, not a second Switch smoke. Every organisation,
commercial term and URL is synthetic. The source is
[operations-rfp-source.txt](../../fixtures/operations-rfp-source.txt); the expected
extraction is [operations-rfp.json](../../fixtures/operations-rfp.json).

An EU supplier is deciding whether to spend six hours bidding for a fictional
EUR 8400 pilot, with twelve available team hours before the deadline. The source
closes at **17:00 Europe/Paris**; the bid owner works in **America/Toronto**, where
it is **11:00**. At the fixed replay time 3 November 2026, 16:10 Toronto (22:10
Paris), **66.83 elapsed hours** remain. Capacity is a separate source fact, not
66.83 working hours. Delivery in ten business days, scope and payment terms
still require human judgement; the tool does not estimate margin or recommend KEEP.

From the clone root after installation:

```sh
.venv/bin/keepkill check fixtures/operations-rfp.json
.venv/bin/keepkill deadline --at '2026-11-06 17:00' --tz Europe/Paris --to America/Toronto --now '2026-11-03 16:10'
.venv/bin/keepkill brief fixtures/operations-rfp.json -o evidence/sample-brief/BRIEF.md --to America/Toronto --now '2026-11-03 16:10'
```

Outputs: `Complete: all required facts are present.`, deadline `2026-11-06 11:00`,
`Hours remaining: 66.83`, then `Brief written: evidence/sample-brief/BRIEF.md`.
All commands exit 0. Repeating these commands reproduces the checked-in brief.
For a real-time evaluation omit `--now`; the sample deadline will eventually expire.

The generated brief always leaves `Decision:` blank and the gate pending.
A reviewer may record KEEP or KILL in Switch Decisions; no such decision or
actual bid has been made here. Missing/invalid facts are surfaced, not repaired
by guessing; an open deadline never constitutes approval.
