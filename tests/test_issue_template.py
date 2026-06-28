from nightly_agent_lab.issue_template import render_task

EXPECTED_SECTIONS = [
    "## Goal",
    "## Scope",
    "## Out of Scope",
    "## Target Repository",
    "## Base Branch",
    "## Risk Level",
    "## Acceptance Criteria",
    "## Commands to Run",
    "## Safety Rules",
    "## Expected Deliverables",
    "## Notes for Claude",
]


def test_render_task_contains_all_sections():
    md = render_task(title="My Task", repo="owner/name")
    for section in EXPECTED_SECTIONS:
        assert section in md


def test_render_task_includes_metadata():
    md = render_task(
        title="My Task",
        repo="owner/name",
        base_branch="develop",
        risk_level="medium",
    )
    assert "# Nightly Task: My Task" in md
    assert "owner/name" in md
    assert "develop" in md
    assert "medium" in md
