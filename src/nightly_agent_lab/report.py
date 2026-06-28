"""Generate Markdown summaries of nightly run results."""

from __future__ import annotations

# Allowed run statuses.
STATUSES = ("success", "failure", "partial", "skipped")


def render_report(
    *,
    status: str,
    summary: str,
    run_url: str,
    pr_url: str | None = None,
) -> str:
    """Return a Markdown summary of a nightly run.

    ``pr_url`` is optional; when omitted a placeholder line is rendered so the
    section is still present and easy to fill in during review.
    """
    pr_line = pr_url if pr_url else "_No pull request was opened._"

    return f"""# Nightly Run Report

## Status

{status}

## Summary

{summary}

## GitHub Actions Run

{run_url}

## Pull Request

{pr_line}

## Changed Files

<!-- List of files changed in this run. -->

## Tests

<!-- Test command(s) run and their results. -->

## Blockers

<!-- Anything that stopped the run from completing, or "None". -->

## Next Actions

<!-- Follow-up tasks for the next nightly run or for human review. -->
"""
