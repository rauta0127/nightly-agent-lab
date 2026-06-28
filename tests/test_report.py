from nightly_agent_lab.report import render_report

EXPECTED_SECTIONS = [
    "## Status",
    "## Summary",
    "## GitHub Actions Run",
    "## Pull Request",
    "## Changed Files",
    "## Tests",
    "## Blockers",
    "## Next Actions",
]


def test_render_report_contains_all_sections():
    md = render_report(
        status="success",
        summary="Implemented scaffold",
        run_url="https://example.com/run/1",
    )
    for section in EXPECTED_SECTIONS:
        assert section in md


def test_render_report_without_pr_url():
    md = render_report(
        status="success",
        summary="No PR opened",
        run_url="https://example.com/run/1",
    )
    assert "No pull request was opened" in md


def test_render_report_with_pr_url():
    md = render_report(
        status="success",
        summary="PR opened",
        run_url="https://example.com/run/1",
        pr_url="https://example.com/pull/42",
    )
    assert "https://example.com/pull/42" in md
