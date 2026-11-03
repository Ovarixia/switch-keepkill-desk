"""Rebuild a silent 150-second screenshot montage with Pillow and ffmpeg."""

import argparse
import hashlib
import json
import shutil
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHOTS = ROOT / "evidence/run2108"
SIZE = (1920, 1080)
SECONDS = 15


def font(size, supplied):
    candidates = (
        [supplied]
        if supplied
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    raise SystemExit("Supply a TrueType font with --font PATH")


def slides():
    brief = (ROOT / "evidence/sample-brief/BRIEF.md").read_text()
    deadline = brief.split("## Deadline\n", 1)[1].split("\n##", 1)[0].strip()
    gate = brief.split("## Human decision\n", 1)[1].strip()
    return [
        (
            "01 / The business decision",
            None,
            [
                "Fictional supplier-intake pilot: EUR 8400 fixed fee.",
                "Bid effort: 6 hours. Available team capacity: 12 hours.",
                "Paris deadline. Toronto bid owner. One human decision.",
                "Scout extracts. Checker calculates. Human chooses KEEP or KILL.",
            ],
            "Two agents reduce preparation work. The human owns the commitment.",
        ),
        (
            "02 / Paste once in intake",
            "01-intake.png",
            [],
            "Historical RUN 2108: pasted synthetic opportunity, source zone + team zone.",
        ),
        (
            "03 / Scout validates and writes",
            "02-scout-write.png",
            [],
            "The scout writes facts.json in its own directory before announcing the handoff.",
        ),
        (
            "04 / Inspect the real facts file",
            "03-facts-file.png",
            [],
            "Historical file capture; the run report also records the scout's write tool result.",
        ),
        (
            "05 / Address the checker in review",
            "04-checker.png",
            [],
            "Checker reads ../ovx-scout/facts.json; it verifies the current run marker and URL.",
        ),
        (
            "06 / Run keepkill: check, deadline, brief",
            "04-checker.png",
            [],
            "RUN 2108: all three commands exit 0. Its historical checker output shows 94.25 hours.",
        ),
        (
            "07 / New business brief: hours are visible",
            None,
            deadline.splitlines(),
            "Enhanced CLI example at a fixed clock. "
            "This output is not from the historical Switch run.",
        ),
        (
            "08 / A brief is not approval",
            None,
            gate.splitlines()[:2]
            + [
                "",
                "Complete facts and an open deadline are not approval.",
                "Review scope, capacity, delivery risk and payment terms.",
                "Only the human records KEEP or KILL in Decisions.",
            ],
            "Generated gate from the same business brief. No decision has been entered.",
        ),
        (
            "09 / Stop at the human gate",
            "05-brief-file.png",
            [],
            "Historical brief: Decision stayed blank. "
            "Human decision recording is not demonstrated.",
        ),
        (
            "10 / Reproduce and inspect the evidence",
            None,
            [
                "github.com/Ovarixia/switch-keepkill-desk",
                "Clone -> venv -> install .[dev] -> ruff -> pytest",
                "Import template -> paste source -> inspect brief -> human gate",
                "docs/JUDGES.md: nine steps. evidence/: sanitized report + five screenshots.",
                "One historical Switch run; enhanced CLI example; sequential processing only.",
                "Public video hosting, registration and submission remain with Melwin.",
            ],
            "Track 01 Best Business Workflow | No live screen recording or human voiceover.",
        ),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", help="TrueType font path; macOS/Linux defaults are detected")
    args = parser.parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required; no automatic package-manager install is performed")
    output = HERE / "slides"
    output.mkdir(exist_ok=True)
    titles = font(54, args.font)
    body = font(36, args.font)
    captions = font(29, args.font)
    foot = font(23, args.font)
    all_slides = slides()
    subtitle_lines = []
    concat_lines = []
    for index, (title, screenshot, lines, caption) in enumerate(all_slides):
        canvas = Image.new("RGB", SIZE, "#101923")
        draw = ImageDraw.Draw(canvas)
        draw.text((80, 54), title, font=titles, fill="#ffffff")
        draw.line((80, 145, 1840, 145), fill="#67d6bb", width=4)
        if screenshot:
            with Image.open(SHOTS / screenshot) as shot:
                fitted = ImageOps.contain(shot.convert("RGB"), (1740, 710))
            canvas.paste(fitted, ((SIZE[0] - fitted.width) // 2, 175 + (710 - fitted.height) // 2))
        else:
            y = 215
            for line in lines:
                for wrapped in textwrap.wrap(line, width=86) or [""]:
                    draw.text((100, y), wrapped, font=body, fill="#e6edf6")
                    y += 57
                y += 12
        y = 921
        for line in textwrap.wrap(caption, width=112):
            draw.text((80, y), line, font=captions, fill="#67d6bb")
            y += 38
        draw.text(
            (80, 1035),
            "SILENT SLIDE MONTAGE | RUN 2108 historical evidence + fixed-clock CLI replay",
            font=foot,
            fill="#b9c5d2",
        )
        name = f"slide-{index + 1:02}.png"
        canvas.save(output / name)
        concat_lines.extend([f"file 'slides/{name}'", f"duration {SECONDS}"])
        start, end = index * SECONDS, (index + 1) * SECONDS

        def timestamp(seconds):
            return f"00:{seconds // 60:02}:{seconds % 60:02},000"

        subtitle_lines.extend(
            [str(index + 1), f"{timestamp(start)} --> {timestamp(end)}", title, caption, ""]
        )
    concat_lines.append(f"file 'slides/slide-{len(all_slides):02}.png'")
    (HERE / "slides.txt").write_text("\n".join(concat_lines) + "\n")
    (HERE / "captions.srt").write_text("\n".join(subtitle_lines))
    video = HERE / "keepkill-desk-demo.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            "slides.txt",
            "-vf",
            "fps=12",
            "-t",
            str(SECONDS * len(all_slides)),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            video.name,
        ],
        cwd=HERE,
        check=True,
    )
    manifest = {
        "type": "silent screenshot slide montage, not live footage",
        "duration_seconds": SECONDS * len(all_slides),
        "resolution": list(SIZE),
        "frames_per_second": 12,
        "video_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
        "video_bytes": video.stat().st_size,
        "sources": ["evidence/run2108/manifest.json", "evidence/sample-brief/BRIEF.md"],
        "shots": [
            {
                "start_seconds": i * SECONDS,
                "end_seconds": (i + 1) * SECONDS,
                "title": slide[0],
                "screenshot": slide[1],
            }
            for i, slide in enumerate(all_slides)
        ],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Created {video.name}: {manifest['duration_seconds']}s, {video.stat().st_size} bytes")


if __name__ == "__main__":
    main()
