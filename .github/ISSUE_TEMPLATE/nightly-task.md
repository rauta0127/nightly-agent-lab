---
name: Nightly Task
about: A small, well-scoped task for an unattended nightly Claude Code run.
title: "Nightly Task: "
labels: ["nightly-task"]
---

## Goal

<!-- What should be accomplished? Keep it to a single, well-scoped change. -->

## Scope

<!-- Files, modules, or behaviors that are in scope. -->

## Out of Scope

<!-- Explicitly list what must NOT be touched. -->

## Risk Level

<!-- low | medium | high -->

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
