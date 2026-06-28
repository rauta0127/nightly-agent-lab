# nightly-agent-lab

A small lab for evaluating and improving **unattended nightly AI coding
workflows** built on Claude Code GitHub Actions + Amazon Bedrock (with Slack
notifications planned later).

## Purpose

The aim is to learn — in the open — how practical it is to let an AI coding
agent pick up a well-scoped task overnight, open a pull request, and report back,
while keeping a human firmly in the review loop. This repo is the minimal
substrate for those experiments:

- a tiny Python CLI (`nal`) to help author tasks and run reports,
- a `CLAUDE.md` describing the rules the agent must follow,
- an issue template for nightly tasks,
- and a (not-yet-enabled) GitHub Actions workflow scaffold for nightly runs.

## What this validates

- Can a nightly run reliably handle small, low-risk tasks end to end?
- Is the task/issue format clear enough to keep the agent in scope?
- Is the morning review workflow (PR + report) fast and trustworthy?
- Can Bedrock be wired up from GitHub Actions safely, without committing secrets?

## Initial setup

Requires Python 3.11+.

```bash
python -m pip install -e ".[dev]"
```

(If `python` is unavailable, use `python3`.)

## `nal new-task`

Generate a Markdown issue body for a nightly task:

```bash
nal new-task \
  --title "Add risk-level option to task generator" \
  --repo "rauta0127/nightly-agent-lab" \
  --base-branch "main" \
  --risk-level "low"
```

Prints a structured Markdown body to stdout. Redirect it to a file or paste it
into a GitHub issue (see the **Nightly Task** issue template).

## `nal report`

Generate a Markdown summary of a nightly run:

```bash
nal report \
  --status success \
  --run-url "https://github.com/example/repo/actions/runs/123" \
  --summary "Implemented initial CLI scaffold"
```

`--pr-url` is optional:

```bash
nal report \
  --status success \
  --run-url "https://github.com/example/repo/actions/runs/123" \
  --summary "Implemented initial CLI scaffold" \
  --pr-url "https://github.com/example/repo/pull/42"
```

By default the report is printed to stdout. Use `--output` to write it to a
file instead:

```bash
nal report \
  --status success \
  --run-url "https://github.com/example/repo/actions/runs/123" \
  --summary "Implemented initial CLI scaffold" \
  --output report.md
```

## Running CI

CI runs on every pull request and on pushes to `main` (see
`.github/workflows/ci.yml`). To run the same checks locally:

```bash
python -m ruff check .
python -m pytest
```

## Roadmap

1. **Now** — CLI scaffold (`new-task`, `report`), tests, CI, docs.
2. **Next** — enable the Claude Nightly workflow against Bedrock via GitHub OIDC,
   starting with small manual (`workflow_dispatch`) runs.
3. **Later** — Slack notifications for run results.
4. **Eventually** — scheduled nightly runs and richer reporting, once small tasks
   run reliably.

See `docs/bedrock-github-actions-setup.md` and `docs/nightly-operation.md`.

## Security note

This is a **public** repository. **Never commit** secrets, tokens, webhook URLs,
AWS account IDs, or role ARNs. Required settings are referenced **by name only**;
their values live in GitHub repository Secrets/Variables, not in the code.
