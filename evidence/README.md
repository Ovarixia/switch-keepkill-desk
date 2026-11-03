# Public evidence

| Evidence | What it demonstrates | Limits |
| --- | --- | --- |
| [RUN 2108 report](run2108/RAPPORT.md) | Existing Switch scout wrote facts; checker read the sibling file and generated a brief on 3 November 2026 | One historical run; template was updated directly in existing agents, not freshly imported |
| [Selected tool receipt](run2108/handoff-receipt.json) | Scout's actual write call/result and checker outputs, with source hashes | Selected historical records; paths redacted and runtime identifiers omitted |
| [01 intake](run2108/01-intake.png), [02 scout write](run2108/02-scout-write.png), [03 actual facts](run2108/03-facts-file.png), [04 checker](run2108/04-checker.png), [05 actual brief](run2108/05-brief-file.png) | Five selected screenshots of that run | Cropped and path-redacted; no human KEEP/KILL was entered |
| [Sample business brief](sample-brief/BRIEF.md) and [replay commands](sample-brief/README.md) | Hours in the brief, Paris to Toronto conversion, labelled team timezone, bid effort and capacity, and an explicit pending human gate | Synthetic CLI replay at a fixed clock, not new Switch footage |
| [Red test receipt](verification/pytest-red.txt) | New behaviour absent before implementation: 16 failed, 41 passed | Development evidence, not a live workflow |
| [Green tests](verification/pytest-green.txt), [ruff](verification/ruff.txt), [YAML check](verification/ci-yaml.txt) | Final local validation | GitHub Actions status is linked separately in the delivery report |
| [Demo montage](../docs/demo/keepkill-desk-demo.mp4) | 150-second illustrated walkthrough of historical screenshots and current CLI output | Silent slide montage, not a live Switch recording |

The original PNGs requested under `/tmp/switch-p2-20261103/` were absent at
preparation time. The five images here come from the retained RUN 2108 logs.
[manifest.json](run2108/manifest.json) records original and public SHA-256 hashes,
crops and redaction coordinates. No raw Mattermost export, session credentials,
local permalinks or runtime logs are bundled. The report copy removes private
home paths and runtime identifiers. Original source trace labels remain for
provenance, but are not public clickable links.

To rebuild the sanitized copy with access to your private source logs:

```sh
.venv/bin/python -m pip install -e '.[demo]'
.venv/bin/python evidence/sanitize_run2108.py PATH_TO_PRIVATE_RUN2108_LOGS
```

Do not confuse the historical `94.25` hours shown by the checker with the new
fixed-clock business example's `66.83`. The historical BRIEF lacks an hours line;
the enhanced version is independently tested and shown in the generated sample.
No independent truth checking of the opportunity, clean-install timing,
concurrency safety or human-decision execution is claimed.

Verification transcripts have terminal colour escapes and trailing whitespace
removed; assertions, errors and command outcomes are preserved.
