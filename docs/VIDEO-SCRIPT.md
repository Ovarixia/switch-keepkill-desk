# Demo script — 2 minutes 30 seconds

Artefact: [docs/demo/keepkill-desk-demo.mp4](demo/keepkill-desk-demo.mp4).
**Silent slide montage, not a live Switch screen recording.** Titles and captions
carry the explanation; optional narration below is a script, not recorded audio.
No human decision, live new template import, upload or submission is claimed.

| Time | Shot / source | On-screen action / optional narration |
| --- | --- | --- |
| 0:00–0:15 | Business context title | A small supplier must decide whether to spend six hours on a fictional EUR 8400 bid. Paris closes the call; the owner works in Toronto. Agents prepare; a human commits. |
| 0:15–0:30 | `evidence/run2108/01-intake.png` | Paste once. Historical RUN 2108 uses a fictional challenge with Asia/Kolkata source and Europe/Paris team time. This is the measured Switch smoke, distinct from the new RFP example. |
| 0:30–0:45 | `02-scout-write.png` | Scout validates the ten fields and writes `./facts.json` in its own directory before relaying. No human saves the JSON. |
| 0:45–1:00 | `03-facts-file.png` | Show the actual scout file. The sanitized smoke report records the write tool result, timestamp and hash; a chat claim alone is insufficient. |
| 1:00–1:15 | `04-checker.png`, handoff explanation | Addressed handoff to the checker in review. It reads `../ovx-scout/facts.json` and checks the current marker and URL; absent or stale input blocks. |
| 1:15–1:30 | `04-checker.png`, command outputs | `keepkill check`, `deadline`, `brief`: three exit codes 0. The historical conversion is Kolkata 23:59 → Paris 19:29, with 94.25 hours at that run's clock. |
| 1:30–1:45 | Newly generated `evidence/sample-brief/BRIEF.md`, deadline excerpt | Explicit switch to the enhanced CLI RFP replay. Source Paris 17:00 → Toronto 11:00. Reference Toronto 3 November 16:10, **66.83 elapsed hours**, both IANA zones and OPEN status visible in BRIEF. This was not rerun inside Switch. |
| 1:45–2:00 | Same generated brief, human gate excerpt | `Gate: PENDING HUMAN KEEP/KILL` and blank `Decision:`. Complete facts do not mean KEEP. Review the six-hour bid effort, twelve-hour capacity, delivery scope and payment terms. |
| 2:00–2:15 | `05-brief-file.png` | Historical brief also leaves the decision blank. The agents must stop until the human records KEEP or KILL in review-room Decisions. This montage demonstrates the pending gate, not a completed human action. |
| 2:15–2:30 | Repository / reproduction title | Public repo, nine-step judge guide, red→green tests, two-version CI and sanitized evidence. One historical run; sequential processing only. Public hosting and registration/submission remain with Melwin. |

The montage uses five sanitized screenshots, not the absent PNGs under the
original temporary directory. Their provenance, crops and masks are in
[evidence/run2108/manifest.json](../evidence/run2108/manifest.json). Screenshots
are held as slides, with titles and explanations added outside their content.
[Build script and instructions](demo/README.md), [captions](demo/captions.srt)
and [shot manifest](demo/manifest.json) are included.

For a future live recording, follow [JUDGES.md](JUDGES.md), capture the actual
scout write and checker tools, open the real new brief, then let the human
choose explicitly. Do not present this existing montage as that recording.
