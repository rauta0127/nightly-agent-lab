"""Generate Markdown issue bodies for nightly tasks."""

from __future__ import annotations

# Allowed risk levels, ordered from least to most risky.
RISK_LEVELS = ("low", "medium", "high")


def render_task(
    *,
    title: str,
    repo: str,
    base_branch: str = "main",
    risk_level: str = "low",
) -> str:
    """Return a Markdown issue body for a nightly task.

    The output is intended to be pasted into a GitHub issue (or fed to a
    Claude Code GitHub Actions run) describing a single, small, reviewable task.
    """
    return f"""# Nightly Task: {title}

## Goal

<!-- What should be accomplished? Keep it to a single, well-scoped change. -->

## Scope

<!-- Files, modules, or behaviors that are in scope. -->

## Out of Scope

<!-- Explicitly list what must NOT be touched. -->

## Target Repository

{repo}

## Base Branch

{base_branch}

## Risk Level

{risk_level}

## Acceptance Criteria

<!-- Checklist describing "done". Each item should be verifiable. -->

## Commands to Run

```bash
python -m ruff check .
python -m pytest
```

## Safety Rules

- Do not commit secrets, tokens, webhook URLs, AWS account IDs, or role ARNs.
- Prefer small, reviewable changes.
- Do not add external services or databases unless explicitly requested.
- Stop and report if a change would exceed the stated scope.

## Expected Deliverables

<!-- Branch, pull request, updated tests, updated docs, etc. -->

## Notes for Claude

<!-- Extra context, gotchas, or links. -->
"""
