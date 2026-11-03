"""Build a public, cropped evidence copy; never modify original smoke logs."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

DEST = Path(__file__).resolve().parent / "run2108"
SHOTS = [
    ("03-intake-sent-w1170.png", "01-intake.png", (630, 440, 1440, 797), []),
    (
        "04-scout-json-and-path-w1170.png",
        "02-scout-write.png",
        (630, 307, 1440, 797),
        [(705, 381, 1415, 401)],
    ),
    ("08-scout-facts-real-w1359.png", "03-facts-file.png", None, []),
    (
        "07-checker-run2108-result-w1170.png",
        "04-checker.png",
        (630, 437, 1442, 796),
        [(705, 751, 1415, 773)],
    ),
    ("06-brief-real-readable-w1359.png", "05-brief-file.png", None, []),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scrub(text):
    text = re.sub(r"/Users/[^/\s`]+", "<HOME>", text)
    return re.sub(r"localhost-\d+", "<server-id>", text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Private RUN 2108 log directory")
    args = parser.parse_args()
    DEST.mkdir(exist_ok=True)
    manifest = {"source_run": "2026-11-03T2108", "screenshots": []}
    for source, name, crop, masks in SHOTS:
        original = args.source / source
        with Image.open(original) as opened:
            picture = opened.convert("RGB")
        draw = ImageDraw.Draw(picture)
        for box in masks:
            draw.rectangle(box, fill="#242424")
            draw.text((box[0] + 2, box[1] + 2), "[local filesystem path redacted]", fill="white")
        if crop:
            picture = picture.crop(crop)
        picture.save(DEST / name)
        manifest["screenshots"].append(
            {
                "source_filename": source,
                "source_sha256": sha(original),
                "public_filename": name,
                "public_sha256": sha(DEST / name),
                "crop_xyxy": crop,
                "redaction_boxes_xyxy_in_source": masks,
            }
        )
    source_report = args.source / "RAPPORT.md"
    text = source_report.read_text()
    manifest["source_report_sha256"] = sha(source_report)
    scout_path = args.source / "scout-write-activity.json"
    checker_path = args.source / "checker-command-outputs.json"
    scout = json.loads(scout_path.read_text())
    receipt = {
        "description": "Selected historical tool records; paths redacted, runtime IDs omitted",
        "author": scout["author"],
        "source_sha256": {
            scout_path.name: sha(scout_path),
            checker_path.name: sha(checker_path),
        },
        "scout": [],
        "checker": [],
    }
    for record in scout["records"]:
        payload = record["payload"]
        if payload["type"] == "custom_tool_call":
            receipt["scout"].append(
                {
                    "timestamp_utc": record["timestamp"],
                    "tool": payload["name"],
                    "input": scrub(payload["input"]),
                }
            )
        elif payload["type"] == "custom_tool_call_output":
            for item in payload["output"]:
                try:
                    result = json.loads(item["text"])
                except (KeyError, ValueError):
                    continue
                if "exit_code" in result:
                    receipt["scout"].append(
                        {
                            "timestamp_utc": record["timestamp"],
                            "exit_code": result["exit_code"],
                            "output": scrub(result["output"]),
                        }
                    )
    for record in json.loads(checker_path.read_text()):
        receipt["checker"].append(
            {
                "timestamp_utc": record["timestamp"],
                "exit_code": record["exit_code"],
                "output": scrub(record["output"]),
            }
        )
    receipt_path = DEST / "handoff-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    manifest["public_receipt_sha256"] = sha(receipt_path)
    # Remove private host/account paths, local permalinks and runtime identifiers.
    text = scrub(text)
    text = re.sub(r"thread `[^`]+`", "thread `[runtime id redacted]`", text)
    text = re.sub(r"`call_[^`]+`", "`[tool call id redacted]`", text)
    text = re.sub(
        r"Liens Mattermost locaux observés :.*?## Chronologie",
        "## Chronologie",
        text,
        flags=re.DOTALL,
    )
    mapped = {source: name for source, name, _, _ in SHOTS}
    mapped.update({scout_path.name: receipt_path.name, checker_path.name: receipt_path.name})

    def link(match):
        label, target = match.groups()
        if target in mapped:
            return f"[{label}]({mapped[target]})"
        return f"{label} (`{target}`, private source retained outside this public copy)"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    lines = text.splitlines()
    lines[1:1] = [
        "",
        "> Historical report, sanitized copy. Original run: 3 November 2026, RUN 2108.",
        "> Crops and path masks are documented in manifest.json; local permalinks and runtime IDs",
        "> were removed. Unbundled trace links are rendered as source labels, not public links.",
        "> Historical statements about no remote/no publication describe that run only.",
        "> This is not a new Switch run and does not prove the later hours-in-BRIEF change.",
    ]
    (DEST / "RAPPORT.md").write_text("\n".join(lines) + "\n")
    manifest["public_report_sha256"] = sha(DEST / "RAPPORT.md")
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Sanitized report and {len(SHOTS)} screenshots: evidence/run2108/")


if __name__ == "__main__":
    main()
