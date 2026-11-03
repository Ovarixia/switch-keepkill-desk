import json
from datetime import timezone
from pathlib import Path

import pytest

from keepkill_desk.cli import check_facts, local_time, main, render_brief

ROOT = Path(__file__).resolve().parents[1]


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
    assert render_brief(facts) == expected
    output = tmp_path / "BRIEF.md"
    assert main(["brief", str(ROOT / "fixtures/complete.json"), "-o", str(output)]) == 0
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
    assert set(schema["required"]) == set(schema["properties"]) == set(facts)
    assert schema["properties"]["ai_tools_allowed"]["enum"] == ["yes", "no", "silent"]
    for path in (ROOT / "fixtures").glob("*.json"):
        example = json.loads(path.read_text())
        assert set(example) == set(schema["required"])
        for field, value in example.items():
            assert isinstance(value, list if field == "deliverables" else str)
