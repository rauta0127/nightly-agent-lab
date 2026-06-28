"""Command-line interface for nightly-agent-lab.

Provides two subcommands:

* ``nal new-task``  - generate a Markdown issue body for a nightly task.
* ``nal report``    - generate a Markdown summary of a nightly run.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from .issue_template import RISK_LEVELS, render_task
from .report import STATUSES, render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nal",
        description="Helpers for unattended nightly AI coding workflows.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    new_task = subparsers.add_parser(
        "new-task",
        help="Generate a Markdown issue body for a nightly task.",
    )
    new_task.add_argument("--title", required=True, help="Short task title.")
    new_task.add_argument("--repo", required=True, help="Target repository, e.g. owner/name.")
    new_task.add_argument("--base-branch", default="main", help="Base branch (default: main).")
    new_task.add_argument(
        "--risk-level",
        default="low",
        choices=RISK_LEVELS,
        help="Risk level for the task (default: low).",
    )
    new_task.set_defaults(func=_cmd_new_task)

    report = subparsers.add_parser(
        "report",
        help="Generate a Markdown summary of a nightly run.",
    )
    report.add_argument(
        "--status",
        required=True,
        choices=STATUSES,
        help="Outcome of the run.",
    )
    report.add_argument("--summary", required=True, help="One-line summary of what happened.")
    report.add_argument("--run-url", required=True, help="URL of the GitHub Actions run.")
    report.add_argument("--pr-url", default=None, help="URL of the pull request (optional).")
    report.add_argument(
        "--output",
        default=None,
        help="Write the report to this file instead of stdout (optional).",
    )
    report.set_defaults(func=_cmd_report)

    return parser


def _cmd_new_task(args: argparse.Namespace) -> str:
    return render_task(
        title=args.title,
        repo=args.repo,
        base_branch=args.base_branch,
        risk_level=args.risk_level,
    )


def _cmd_report(args: argparse.Namespace) -> str:
    return render_report(
        status=args.status,
        summary=args.summary,
        run_url=args.run_url,
        pr_url=args.pr_url,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    text = args.func(args)

    # Only `report` defines --output; other subcommands always print to stdout.
    output_path = getattr(args, "output", None)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
