"""File-only CLI. No agent or service is started here."""

import argparse
import json
import math
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
OPTIONAL_FIELDS = ("team_tz", "bid_effort_hours", "capacity_hours")
HOUR_FIELDS = ("bid_effort_hours", "capacity_hours")
UNKNOWN = {"INCONNU", "UNKNOWN"}
FALLBACK_ZONE = "Europe/Paris"


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


def valid_hours(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value) and value >= 0


def format_hours(value: int | float) -> str:
    if float(value) == 0:
        return "0"
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


def stated_hours(facts: dict, field: str) -> str | None:
    if field not in facts:
        return None
    value = facts[field]
    if valid_hours(value):
        return format_hours(value)
    return "INCONNU"


def resolve_zone_name(facts: dict, target: str | None) -> str:
    """Prefer an explicit clock zone, then a valid team_tz, then Europe/Paris."""
    if target:
        return target
    stated = facts.get("team_tz")
    if isinstance(stated, str) and not missing(stated):
        try:
            ZoneInfo(stated)
        except ZoneInfoNotFoundError:
            return FALLBACK_ZONE
        return stated
    return FALLBACK_ZONE


def check_capacity(facts: dict, issues: list[str]) -> None:
    if "team_tz" in facts:
        value = facts["team_tz"]
        if not isinstance(value, str):
            issues.append("team_tz: expected an IANA timezone string")
        elif missing(value):
            issues.append("team_tz: missing or INCONNU/UNKNOWN")
        else:
            try:
                ZoneInfo(value)
            except ZoneInfoNotFoundError:
                issues.append(f"team_tz: unknown IANA timezone {value}")
    for field in HOUR_FIELDS:
        if field not in facts:
            continue
        value = facts[field]
        if isinstance(value, str) and missing(value):
            issues.append(f"{field}: missing or INCONNU/UNKNOWN")
        elif not valid_hours(value):
            issues.append(f"{field}: expected a non-negative number of hours")


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
    known = set(FIELDS) | set(OPTIONAL_FIELDS)
    for field in sorted(set(facts) - known):
        issues.append(f"{field}: unexpected field")
    check_capacity(facts, issues)
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


def hours_remaining(at: datetime, now: datetime) -> float:
    """Measure elapsed UTC hours, including daylight-saving transitions."""
    return (at.astimezone(timezone.utc) - now.astimezone(timezone.utc)).total_seconds() / 3600


def render_brief(facts: dict, target: str | None = None, now: str | None = None) -> str:
    issues = check_facts(facts)
    target = resolve_zone_name(facts, target)
    zone = ZoneInfo(target)
    reference = local_time(now, target) if now is not None else datetime.now(zone)

    def display(field: str) -> str:
        value = facts.get(field)
        if missing(value):
            return "INCONNU"
        if isinstance(value, str):
            return value.replace("\r", " ").replace("\n", " ")
        return "INCONNU"

    converted = "INCONNU"
    hours = "INCONNU"
    status = "INCONNU"
    if not any(issue.startswith("deadline_") for issue in issues):
        at = local_time(facts["deadline_local"], facts["deadline_tz"]).astimezone(zone)
        converted = at.strftime("%Y-%m-%d %H:%M")
        remaining = hours_remaining(at, reference)
        hours = f"{remaining:.2f}"
        status = "EXPIRED" if remaining < 0 else "DUE NOW" if remaining == 0 else "OPEN"
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
    if status == "EXPIRED":
        validation.append("- Deadline has passed; do not assume an extension.")
    stated_zone = facts.get("team_tz")
    if (
        isinstance(stated_zone, str)
        and not missing(stated_zone)
        and stated_zone != target
    ):
        try:
            ZoneInfo(stated_zone)
        except ZoneInfoNotFoundError:
            pass
        else:
            validation.append(
                f"- Team timezone in the facts is {stated_zone}; "
                f"this brief's clock uses {target}."
            )
    capacity = []
    if "team_tz" in facts:
        shown = display("team_tz") if isinstance(facts.get("team_tz"), str) else "INCONNU"
        capacity.append(f"- Team timezone: {shown}")
    for field, label in (
        ("bid_effort_hours", "Bid effort (hours)"),
        ("capacity_hours", "Capacity (hours)"),
    ):
        shown = stated_hours(facts, field)
        if shown is not None:
            capacity.append(f"- {label}: {shown}")
    if any(field in facts for field in HOUR_FIELDS):
        capacity.append(
            "- Elapsed hours remaining include nights and are not bid effort or capacity."
        )
    capacity_section = ["", "## Team and capacity", *capacity] if capacity else []
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
            f"- Reference time ({target}): {reference:%Y-%m-%d %H:%M:%S %z}",
            f"- Hours remaining: {hours}",
            f"- Deadline status: {status}",
            *capacity_section,
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
            "Gate: PENDING HUMAN KEEP/KILL",
            "Decision:",
            "",
            "The human decides KEEP or KILL and records it in the room Decisions.",
            "Stop here until the human records KEEP or KILL in Decisions.",
            "Complete facts and an open deadline are not approval. No automatic action follows.",
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
    brief.add_argument(
        "--to",
        default=None,
        help=(
            "IANA timezone for the brief clock. Default: facts team_tz when that "
            "is a valid zone, otherwise Europe/Paris"
        ),
    )
    brief.add_argument(
        "--now", help="Reference local time in the --to timezone; default: current time"
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "deadline":
            target = ZoneInfo(args.to)
            at = local_time(args.at, args.tz).astimezone(target)
            now = local_time(args.now, args.to) if args.now else datetime.now(target)
            hours = hours_remaining(at, now)
            print(f"Deadline: {at:%Y-%m-%d %H:%M} ({args.to})")
            print(f"Hours remaining: {hours:.2f}")
            return 0
        facts = load_facts(args.facts)
        if args.command == "check":
            issues = check_facts(facts)
            print("\n".join(issues) if issues else "Complete: all required facts are present.")
            return 2 if issues else 0
        Path(args.output).write_text(render_brief(facts, args.to, args.now), encoding="utf-8")
        print(f"Brief written: {args.output}")
        return 0
    except (OSError, ValueError, ZoneInfoNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
