"""File-only CLI. No agent or service is started here."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

FIELDS = (
    "name",
    "url",
    "track",
    "prize",
    "deadline_local",
    "deadline_tz",
    "eligibility",
    "deliverables",
    "ai_tools_allowed",
    "notes",
)
UNKNOWN = {"INCONNU", "UNKNOWN"}


def local_time(value: str, tz: str) -> datetime:
    """Reject ambiguous or nonexistent wall times rather than guessing."""
    naive = datetime.strptime(value, "%Y-%m-%d %H:%M")
    if naive.strftime("%Y-%m-%d %H:%M") != value:
        raise ValueError("Use YYYY-MM-DD HH:MM for local times")
    zone = ZoneInfo(tz)
    candidates = []
    for fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=fold)
        if aware.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None) == naive:
            candidates.append(aware)
    if not candidates:
        raise ValueError(f"Nonexistent local time: {value} ({tz})")
    if len({item.utcoffset() for item in candidates}) > 1:
        raise ValueError(f"Ambiguous local time: {value} ({tz}); clarify the source")
    return candidates[0]


def missing(value: object) -> bool:
    return value is None or (
        isinstance(value, str) and (not value.strip() or value.strip().upper() in UNKNOWN)
    )


def check_facts(facts: dict) -> list[str]:
    """Check the simple facts schema without a second runtime dependency."""
    issues = []
    for field in FIELDS:
        value = facts.get(field)
        if missing(value):
            issues.append(f"{field}: missing or INCONNU/UNKNOWN")
        elif field == "deliverables":
            if not isinstance(value, list) or not value:
                issues.append("deliverables: expected a nonempty list of strings")
            else:
                for index, item in enumerate(value):
                    if not isinstance(item, str) or missing(item):
                        issues.append(f"deliverables[{index}]: missing or invalid string")
        elif not isinstance(value, str):
            issues.append(f"{field}: expected a string")
        elif field == "ai_tools_allowed" and value not in {"yes", "no", "silent"}:
            issues.append("ai_tools_allowed: expected yes, no or silent")
    for field in sorted(set(facts) - set(FIELDS)):
        issues.append(f"{field}: unexpected field")
    if not any(issue.startswith(("deadline_local:", "deadline_tz:")) for issue in issues):
        try:
            local_time(facts["deadline_local"], facts["deadline_tz"])
        except (ValueError, ZoneInfoNotFoundError) as exc:
            issues.append(f"deadline_local/deadline_tz: {exc}")
    return issues


def load_facts(path: str) -> dict:
    facts = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(facts, dict):
        raise ValueError("Facts must be a JSON object")
    return facts


def render_brief(facts: dict, target: str = "Europe/Paris") -> str:
    issues = check_facts(facts)
    zone = ZoneInfo(target)

    def display(field: str) -> str:
        value = facts.get(field)
        if missing(value):
            return "INCONNU"
        if isinstance(value, str):
            return value.replace("\r", " ").replace("\n", " ")
        return "INCONNU"

    converted = "INCONNU"
    if not any(issue.startswith("deadline_") for issue in issues):
        converted = (
            local_time(facts["deadline_local"], facts["deadline_tz"])
            .astimezone(zone)
            .strftime("%Y-%m-%d %H:%M")
        )
    deliverables = facts.get("deliverables")
    items = ["- INCONNU"]
    if isinstance(deliverables, list) and deliverables:
        items = [
            "- "
            + (
                item.replace("\r", " ").replace("\n", " ")
                if isinstance(item, str) and not missing(item)
                else "INCONNU"
            )
            for item in deliverables
        ]
    validation = [f"- {issue}" for issue in issues] or ["- All required facts are present."]
    ai = display("ai_tools_allowed")
    if ai == "no":
        validation.append("- AI tools are forbidden by the supplied facts; human review required.")
    elif ai == "silent":
        validation.append("- Source is silent about AI tools; silence is not permission.")
    return "\n".join(
        [
            f"# Opportunity brief: {display('name')}",
            "",
            "## Facts",
            f"- Name: {display('name')}",
            f"- URL: {display('url')}",
            f"- Track: {display('track')}",
            f"- Prize: {display('prize')}",
            f"- Eligibility: {display('eligibility')}",
            f"- AI tools allowed: {ai}",
            "",
            "## Deadline",
            f"- Source local time: {display('deadline_local')}",
            f"- Source timezone: {display('deadline_tz')}",
            f"- Team time ({target}): {converted}",
            "",
            "## Required deliverables",
            *items,
            "",
            "## Missing facts and cautions",
            *validation,
            "",
            "## Notes",
            display("notes"),
            "",
            "## Human decision",
            "Decision:",
            "",
            "The human decides KEEP or KILL and records it in the room Decisions.",
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="keepkill")
    commands = parser.add_subparsers(dest="command", required=True)
    deadline = commands.add_parser("deadline", help="Convert a deadline and calculate hours left")
    deadline.add_argument("--at", required=True)
    deadline.add_argument("--tz", required=True)
    deadline.add_argument("--to", required=True)
    deadline.add_argument("--now", help="Reference local time in the --to timezone")
    check = commands.add_parser("check", help="List missing or invalid facts")
    check.add_argument("facts")
    brief = commands.add_parser("brief", help="Write a Markdown brief; leave the decision blank")
    brief.add_argument("facts")
    brief.add_argument("-o", "--output", required=True)
    brief.add_argument("--to", default="Europe/Paris", help="Team timezone (default Europe/Paris)")
    args = parser.parse_args(argv)
    try:
        if args.command == "deadline":
            target = ZoneInfo(args.to)
            at = local_time(args.at, args.tz).astimezone(target)
            now = local_time(args.now, args.to) if args.now else datetime.now(target)
            elapsed = at.astimezone(timezone.utc) - now.astimezone(timezone.utc)
            hours = elapsed.total_seconds() / 3600
            print(f"Deadline: {at:%Y-%m-%d %H:%M} ({args.to})")
            print(f"Hours remaining: {hours:.2f}")
            return 0
        facts = load_facts(args.facts)
        if args.command == "check":
            issues = check_facts(facts)
            print("\n".join(issues) if issues else "Complete: all required facts are present.")
            return 2 if issues else 0
        Path(args.output).write_text(render_brief(facts, args.to), encoding="utf-8")
        print(f"Brief written: {args.output}")
        return 0
    except (OSError, ValueError, ZoneInfoNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
