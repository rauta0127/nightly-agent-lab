# CLAUDE.md

## Project Purpose

This repository is a small lab for evaluating and improving unattended nightly
AI coding workflows using Claude Code GitHub Actions (with Amazon Bedrock and,
later, Slack notifications). It is **public**, so treat everything committed
here as world-readable.

## Development Rules

- Prefer small, reviewable changes.
- Do not add external services unless explicitly requested.
- Do not add databases in the MVP.
- Do not implement a Slack bot until the CLI and reporting workflow are stable.
- Do not commit secrets, tokens, webhook URLs, AWS account IDs, or role ARNs.
- Every behavior change should include tests.
- Update README when user-facing behavior changes.
- Keep dependencies minimal; the CLI uses the standard library (`argparse`).
- Use a `src/` layout; the package is `nightly_agent_lab` and the command is `nal`.

## Test Commands

- Run tests: `python -m pytest`
- Lint: `python -m ruff check .`

(If `python` is unavailable, use `python3`.)

## Completion Criteria

Before finishing a task:
1. Run relevant tests.
2. Run lint.
3. Summarize changed files.
4. Summarize test results.
5. List remaining blockers and follow-up tasks.
