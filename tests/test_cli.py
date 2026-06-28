import pytest

from nightly_agent_lab.cli import main


def test_help_succeeds(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "new-task" in out
    assert "report" in out


def test_new_task_via_main(capsys):
    rc = main(
        [
            "new-task",
            "--title",
            "Example",
            "--repo",
            "owner/name",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "# Nightly Task: Example" in out


def test_report_via_main(capsys):
    rc = main(
        [
            "report",
            "--status",
            "success",
            "--summary",
            "Did the thing",
            "--run-url",
            "https://example.com/run/1",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "# Nightly Run Report" in out


def test_report_writes_to_output_file(tmp_path, capsys):
    out_file = tmp_path / "report.md"
    rc = main(
        [
            "report",
            "--status",
            "success",
            "--summary",
            "Wrote to file",
            "--run-url",
            "https://example.com/run/1",
            "--output",
            str(out_file),
        ]
    )
    assert rc == 0
    # Nothing is printed to stdout when --output is given.
    assert capsys.readouterr().out == ""
    contents = out_file.read_text(encoding="utf-8")
    assert "# Nightly Run Report" in contents
    assert "Wrote to file" in contents


def test_report_prints_to_stdout_without_output(capsys):
    rc = main(
        [
            "report",
            "--status",
            "success",
            "--summary",
            "Printed to stdout",
            "--run-url",
            "https://example.com/run/1",
        ]
    )
    assert rc == 0
    assert "# Nightly Run Report" in capsys.readouterr().out


def test_no_command_errors():
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code != 0
