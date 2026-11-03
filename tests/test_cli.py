import json
from datetime import timezone
from pathlib import Path

import pytest

from keepkill_desk.cli import check_facts, local_time, main, render_brief

ROOT = Path(__file__).resolve().parents[1]
OPTIONAL_FACTS = {"team_tz", "bid_effort_hours", "capacity_hours"}
HOUR_FACTS = {"bid_effort_hours", "capacity_hours"}


@pytest.fixture
def facts():
    return json.loads((ROOT / "fixtures/complete.json").read_text())


def test_ist_to_paris():
    from zoneinfo import ZoneInfo

    result = local_time("2026-11-07 23:59", "Asia/Kolkata").astimezone(ZoneInfo("Europe/Paris"))
    assert result.strftime("%Y-%m-%d %H:%M %z") == "2026-11-07 19:29 +0100"


def test_deadline_hours(capsys):
    assert (
        main(
            [
                "deadline",
                "--at",
                "2026-11-07 23:59",
                "--tz",
                "Asia/Kolkata",
                "--to",
                "Europe/Paris",
                "--now",
                "2026-11-04 10:00",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out == (
        "Deadline: 2026-11-07 19:29 (Europe/Paris)\nHours remaining: 81.48\n"
    )


def test_expired_deadline(capsys):
    assert (
        main(
            [
                "deadline",
                "--at",
                "2026-11-07 10:00",
                "--tz",
                "Europe/Paris",
                "--to",
                "Europe/Paris",
                "--now",
                "2026-11-07 12:00",
            ]
        )
        == 0
    )
    assert "Hours remaining: -2.00" in capsys.readouterr().out


def test_elapsed_hours_across_dst(capsys):
    assert (
        main(
            [
                "deadline",
                "--at",
                "2026-10-25 04:00",
                "--tz",
                "Europe/Paris",
                "--to",
                "Europe/Paris",
                "--now",
                "2026-10-25 01:00",
            ]
        )
        == 0
    )
    assert "Hours remaining: 4.00" in capsys.readouterr().out


@pytest.mark.parametrize("value", ["2026-02-30 12:00", "2026-11-07", "2026-1-1 1:00"])
def test_invalid_dates(value):
    with pytest.raises(ValueError):
        local_time(value, "Europe/Paris")


@pytest.mark.parametrize(
    "value, message",
    [
        ("2026-03-29 02:30", "Nonexistent"),
        ("2026-10-25 02:30", "Ambiguous"),
    ],
)
def test_dst_requires_clarification(value, message):
    with pytest.raises(ValueError, match=message):
        local_time(value, "Europe/Paris")


def test_utc_time():
    assert local_time("2026-11-07 12:00", "UTC").utcoffset() == timezone.utc.utcoffset(None)


@pytest.mark.parametrize(
    "fixture, code",
    [
        ("complete.json", 0),
        ("missing-deadline.json", 2),
        ("ai-forbidden.json", 0),
    ],
)
def test_check_exit_status(fixture, code, capsys):
    assert main(["check", str(ROOT / "fixtures" / fixture)]) == code
    output = capsys.readouterr().out
    if code == 2:
        assert "deadline_local:" in output
        assert "deadline_tz:" in output
    else:
        assert output.startswith("Complete:")


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", "UNKNOWN"),
        ("url", "  "),
        ("prize", None),
        ("notes", 42),
        ("deliverables", []),
        ("deliverables", ["UNKNOWN"]),
        ("deliverables", "README"),
        ("ai_tools_allowed", "maybe"),
        ("deadline_tz", "Invalid/Zone"),
        ("deadline_local", "2026-02-30 12:00"),
    ],
)
def test_invalid_fact_report(facts, field, value):
    facts[field] = value
    assert any(
        issue.startswith(field) or issue.startswith("deadline_local/deadline_tz")
        for issue in check_facts(facts)
    )


def test_absent_field(facts):
    del facts["eligibility"]
    assert check_facts(facts) == ["eligibility: missing or INCONNU/UNKNOWN"]


def test_unexpected_field(facts):
    facts["decision"] = "KEEP"
    assert check_facts(facts) == ["decision: unexpected field"]


@pytest.mark.parametrize("content", ["[]", "{broken"])
def test_invalid_json(tmp_path, capsys, content):
    path = tmp_path / "facts.json"
    path.write_text(content)
    assert main(["check", str(path)]) == 2
    assert capsys.readouterr().err.startswith("Error:")


def test_missing_file(tmp_path, capsys):
    assert main(["check", str(tmp_path / "absent.json")]) == 2
    assert capsys.readouterr().err.startswith("Error:")


def test_brief_snapshot(facts, tmp_path):
    expected = (ROOT / "tests/snapshots/complete.md").read_text()
    assert render_brief(facts, now="2026-11-04 10:00") == expected
    output = tmp_path / "BRIEF.md"
    assert (
        main(
            [
                "brief",
                str(ROOT / "fixtures/complete.json"),
                "-o",
                str(output),
                "--now",
                "2026-11-04 10:00",
            ]
        )
        == 0
    )
    assert output.read_text() == expected


def test_incomplete_brief(tmp_path):
    output = tmp_path / "BRIEF.md"
    assert (
        main(
            [
                "brief",
                str(ROOT / "fixtures/missing-deadline.json"),
                "-o",
                str(output),
            ]
        )
        == 0
    )
    result = output.read_text()
    assert "Team time (Europe/Paris): INCONNU" in result
    assert "deadline_local: missing" in result
    assert "silence is not permission" in result
    assert "Decision:\n" in result


def test_ai_forbidden_brief():
    facts = json.loads((ROOT / "fixtures/ai-forbidden.json").read_text())
    result = render_brief(facts)
    assert "AI tools are forbidden" in result
    assert "Decision:\n" in result
    assert "Decision: KEEP" not in result
    assert "Decision: KILL" not in result


def test_brief_target_and_no_input_mutation(facts):
    before = json.dumps(facts)
    assert "Team time (UTC): 2026-11-07 18:29" in render_brief(facts, "UTC")
    assert json.dumps(facts) == before


def test_invalid_output_path(tmp_path, capsys):
    assert (
        main(
            [
                "brief",
                str(ROOT / "fixtures/complete.json"),
                "-o",
                str(tmp_path),
            ]
        )
        == 2
    )
    assert capsys.readouterr().err.startswith("Error:")


def test_invalid_target(capsys):
    assert (
        main(
            [
                "deadline",
                "--at",
                "2026-11-07 23:59",
                "--tz",
                "Asia/Kolkata",
                "--to",
                "Invalid/Zone",
            ]
        )
        == 2
    )
    assert capsys.readouterr().err.startswith("Error:")


def test_schema_and_fixtures(facts):
    schema = json.loads((ROOT / "schema/facts.schema.json").read_text())
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(facts)
    assert set(schema["properties"]) == set(schema["required"]) | OPTIONAL_FACTS
    assert schema["properties"]["ai_tools_allowed"]["enum"] == ["yes", "no", "silent"]
    for path in (ROOT / "fixtures").glob("*.json"):
        example = json.loads(path.read_text())
        assert set(schema["required"]) <= set(example) <= set(schema["properties"])
        for field, value in example.items():
            if field == "deliverables":
                assert isinstance(value, list)
            elif field in HOUR_FACTS:
                assert type(value) in (int, float)
                assert value >= 0
            else:
                assert isinstance(value, str)


@pytest.mark.parametrize(
    "at, source, target, now, hours, status",
    [
        ("2026-11-07 23:59", "Asia/Kolkata", "Europe/Paris", "2026-11-04 10:00", "81.48", "OPEN"),
        (
            "2026-11-06 17:00",
            "Europe/Paris",
            "America/Toronto",
            "2026-11-03 16:10",
            "66.83",
            "OPEN",
        ),
        ("2026-10-25 04:00", "Europe/Paris", "Europe/Paris", "2026-10-25 01:00", "4.00", "OPEN"),
        ("2026-03-29 04:00", "Europe/Paris", "Europe/Paris", "2026-03-29 01:00", "2.00", "OPEN"),
        (
            "2026-11-07 10:00",
            "Europe/Paris",
            "Europe/Paris",
            "2026-11-07 12:00",
            "-2.00",
            "EXPIRED",
        ),
        ("2026-11-07 10:00", "Europe/Paris", "Europe/Paris", "2026-11-07 10:00", "0.00", "DUE NOW"),
    ],
)
def test_brief_elapsed_hours_and_pending_gate(facts, at, source, target, now, hours, status):
    facts.update(deadline_local=at, deadline_tz=source)
    before = json.dumps(facts)
    result = render_brief(facts, target, now=now)
    assert f"Hours remaining: {hours}" in result
    assert f"Deadline status: {status}" in result
    assert f"Reference time ({target}): {now}" in result
    assert "Gate: PENDING HUMAN KEEP/KILL" in result
    assert "Decision:\n\n" in result
    assert "Stop here until the human records KEEP or KILL in Decisions." in result
    assert json.dumps(facts) == before


@pytest.mark.parametrize("value", ["UNKNOWN", "2026-10-25 02:30", "2026-03-29 02:30"])
def test_unknown_or_ambiguous_brief_never_invents_hours(facts, value):
    facts.update(deadline_local=value, deadline_tz="Europe/Paris")
    result = render_brief(facts, now="2026-11-03 22:10")
    assert "Hours remaining: INCONNU" in result
    assert "Deadline status: INCONNU" in result
    assert "Gate: PENDING HUMAN KEEP/KILL" in result


def test_cli_brief_fixed_clock_and_repeatability(tmp_path):
    output = tmp_path / "BRIEF.md"
    command = [
        "brief",
        str(ROOT / "fixtures/complete.json"),
        "-o",
        str(output),
        "--to",
        "Europe/Paris",
        "--now",
        "2026-11-04 10:00",
    ]
    assert main(command) == 0
    first = output.read_bytes()
    assert b"Hours remaining: 81.48" in first
    assert main(command) == 0
    assert output.read_bytes() == first


@pytest.mark.parametrize("now", ["2026-10-25 02:30", "2026-03-29 02:30", "bad"])
def test_invalid_brief_clock_does_not_overwrite_output(tmp_path, now, capsys):
    output = tmp_path / "BRIEF.md"
    output.write_text("Preserve previous brief")
    assert (
        main(["brief", str(ROOT / "fixtures/complete.json"), "-o", str(output), "--now", now]) == 2
    )
    assert output.read_text() == "Preserve previous brief"
    assert capsys.readouterr().err.startswith("Error:")


def test_brief_default_clock_is_current(facts):
    from datetime import datetime
    from zoneinfo import ZoneInfo

    before = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M")
    result = render_brief(facts)
    after = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M")
    assert any(f"Reference time (Europe/Paris): {time}" in result for time in (before, after))
    assert "Hours remaining: INCONNU" not in result


def test_complete_facts_cannot_supply_human_decision(facts):
    facts["decision"] = "KEEP"
    result = render_brief(facts, now="2026-11-04 10:00")
    assert "decision: unexpected field" in result
    assert "Decision: KEEP" not in result
    assert "Decision: KILL" not in result
    assert "Gate: PENDING HUMAN KEEP/KILL" in result


def _decision_is_blank(result: str) -> None:
    assert "Gate: PENDING HUMAN KEEP/KILL" in result
    assert "Decision:\n\n" in result
    assert "Decision: KEEP" not in result
    assert "Decision: KILL" not in result
    for line in result.splitlines():
        if line.startswith("Decision:"):
            assert line == "Decision:"


def test_schema_exposes_optional_team_and_capacity_facts(facts):
    schema = json.loads((ROOT / "schema/facts.schema.json").read_text())
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(facts)
    assert set(schema["properties"]) == set(schema["required"]) | OPTIONAL_FACTS
    assert schema["properties"]["team_tz"]["type"] == "string"
    assert schema["properties"]["bid_effort_hours"]["type"] == "number"
    assert schema["properties"]["bid_effort_hours"]["minimum"] == 0
    assert schema["properties"]["capacity_hours"]["type"] == "number"
    assert schema["properties"]["capacity_hours"]["minimum"] == 0
    for field in OPTIONAL_FACTS:
        assert field not in schema["required"]


def test_operations_source_names_the_capacity_facts():
    source = (ROOT / "fixtures/operations-rfp-source.txt").read_text()
    assert "Deadline timezone: Europe/Paris" in source
    assert "Team timezone (team_tz): America/Toronto" in source
    assert "Bid effort hours (bid_effort_hours): 6" in source
    assert "Capacity hours (capacity_hours): 12" in source


def test_operations_rfp_labels_capacity_and_leaves_decision_blank(tmp_path, capsys):
    facts_path = ROOT / "fixtures/operations-rfp.json"
    facts = json.loads(facts_path.read_text())
    assert facts["deadline_tz"] == "Europe/Paris"
    assert facts["team_tz"] == "America/Toronto"
    assert facts["bid_effort_hours"] == 6
    assert facts["capacity_hours"] == 12
    assert main(["check", str(facts_path)]) == 0
    check_out = capsys.readouterr().out
    assert check_out.startswith("Complete:")
    assert "KEEP" not in check_out
    assert "KILL" not in check_out
    output = tmp_path / "BRIEF.md"
    assert (
        main(
            [
                "brief",
                str(facts_path),
                "-o",
                str(output),
                "--to",
                "America/Toronto",
                "--now",
                "2026-11-03 16:10",
            ]
        )
        == 0
    )
    result = output.read_text()
    assert "Team time (America/Toronto): 2026-11-06 11:00" in result
    assert "Hours remaining: 66.83" in result
    assert "Deadline status: OPEN" in result
    section = result.split("## Team and capacity\n", 1)[1].split("\n##", 1)[0]
    assert "- Team timezone: America/Toronto" in section
    assert "- Bid effort (hours): 6" in section
    assert "- Capacity (hours): 12" in section
    assert "Elapsed hours remaining include nights and are not bid effort or capacity." in section
    assert "this brief's clock uses" not in result
    _decision_is_blank(result)
    assert capsys.readouterr().out.startswith("Brief written:")


def test_sample_brief_matches_operations_replay():
    facts = json.loads((ROOT / "fixtures/operations-rfp.json").read_text())
    expected = render_brief(facts, "America/Toronto", now="2026-11-03 16:10")
    checked = (ROOT / "evidence/sample-brief/BRIEF.md").read_text()
    assert checked == expected


def test_omitted_clock_zone_uses_stated_team_tz():
    facts = json.loads((ROOT / "fixtures/operations-rfp.json").read_text())
    result = render_brief(facts, now="2026-11-03 16:10")
    assert "Team time (America/Toronto): 2026-11-06 11:00" in result
    assert "Team time (Europe/Paris)" not in result
    assert "Hours remaining: 66.83" in result
    assert "- Team timezone: America/Toronto" in result
    _decision_is_blank(result)


def test_explicit_clock_zone_still_shows_toronto_facts():
    facts = json.loads((ROOT / "fixtures/operations-rfp.json").read_text())
    result = render_brief(facts, "Europe/Paris", now="2026-11-03 22:10")
    assert "Team time (Europe/Paris): 2026-11-06 17:00" in result
    assert "Hours remaining: 66.83" in result
    assert "- Team timezone: America/Toronto" in result
    assert "- Bid effort (hours): 6" in result
    assert "- Capacity (hours): 12" in result
    assert (
        "Team timezone in the facts is America/Toronto; this brief's clock uses Europe/Paris."
        in result
    )
    _decision_is_blank(result)


def test_capacity_facts_absent_omit_the_section(facts):
    result = render_brief(facts, now="2026-11-04 10:00")
    assert "## Team and capacity" not in result
    assert "Bid effort" not in result
    assert "Capacity (hours)" not in result
    assert "Hours remaining: 81.48" in result
    _decision_is_blank(result)


def test_fractional_and_zero_hours_are_labelled_facts(facts):
    facts.update(team_tz="America/Toronto", bid_effort_hours=6.25, capacity_hours=0)
    assert check_facts(facts) == []
    result = render_brief(facts, "Europe/Paris", now="2026-11-04 10:00")
    assert "- Team timezone: America/Toronto" in result
    assert "- Bid effort (hours): 6.25" in result
    assert "- Capacity (hours): 0" in result
    _decision_is_blank(result)


@pytest.mark.parametrize(
    "field, value",
    [
        ("team_tz", "Not/AZone"),
        ("team_tz", "INCONNU"),
        ("team_tz", 12),
        ("bid_effort_hours", -1),
        ("bid_effort_hours", True),
        ("bid_effort_hours", "6"),
        ("bid_effort_hours", float("nan")),
        ("capacity_hours", float("inf")),
        ("capacity_hours", "UNKNOWN"),
    ],
)
def test_invalid_capacity_facts_are_reported(facts, field, value):
    facts[field] = value
    issues = check_facts(facts)
    assert any(issue.startswith(f"{field}:") for issue in issues)
    assert f"{field}: unexpected field" not in issues


def test_unknown_capacity_is_labelled_without_a_decision(facts):
    facts.update(team_tz="INCONNU", bid_effort_hours="UNKNOWN", capacity_hours="INCONNU")
    result = render_brief(facts, now="2026-11-04 10:00")
    assert "- Team timezone: INCONNU" in result
    assert "- Bid effort (hours): INCONNU" in result
    assert "- Capacity (hours): INCONNU" in result
    assert "team_tz: missing or INCONNU/UNKNOWN" in result
    assert "bid_effort_hours: missing or INCONNU/UNKNOWN" in result
    assert "capacity_hours: missing or INCONNU/UNKNOWN" in result
    _decision_is_blank(result)


def test_effort_above_capacity_is_not_a_verdict():
    facts = json.loads((ROOT / "fixtures/operations-rfp.json").read_text())
    facts["bid_effort_hours"] = 20
    facts["capacity_hours"] = 12
    result = render_brief(facts, "America/Toronto", now="2026-11-03 16:10")
    assert "- Bid effort (hours): 20" in result
    assert "- Capacity (hours): 12" in result
    assert "KEEP" not in result.split("## Human decision", 1)[0]
    _decision_is_blank(result)
