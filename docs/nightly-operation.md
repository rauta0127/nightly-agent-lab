# Nightly Operation Guide

How to run and review unattended nightly tasks in this lab. The goal early on is
to build confidence with **small, low-risk tasks** before scaling up.

## 1. Write a nightly task

A good nightly task is small, well-scoped, and has verifiable acceptance
criteria. Open an issue using the **Nightly Task** issue template, or generate a
task body locally:

```bash
nal new-task \
  --title "Add risk-level option to task generator" \
  --repo "rauta0127/nightly-agent-lab" \
  --base-branch "develop" \
  --risk-level "low"
```

Paste the output into a GitHub issue (or a file under `examples/tasks/`). See
`examples/tasks/001-small-refactor.md` for a complete example.

Tips:

- Keep the scope to a single change.
- Always fill in **Out of Scope** and **Acceptance Criteria**.
- Start with `risk-level: low`.

## 2. Run the nightly workflow

The Claude Nightly workflow is a **manual-only template** today
(`workflow_dispatch`) and will **skip** unless `ENABLE_CLAUDE_NIGHTLY` is set to
`true` in repository variables.

Intended flow once Bedrock access is configured (see
`docs/bedrock-github-actions-setup.md`):

1. Go to **Actions → Claude Nightly (template) → Run workflow**.
2. Provide inputs:
   - `task` — the task instructions.
   - `base_branch` — usually `develop` (the default).
   - `max_turns` — keep this small at first (e.g. `10`–`15`).
3. Start the run.

Automatic scheduling is intentionally **not** enabled yet.

## 3. Morning review

After a nightly run:

1. Open the run from the **Actions** tab and read the job summary.
2. Review the pull request (if one was opened) as you would any human PR.
3. Confirm acceptance criteria are met.
4. Check that CI (lint + tests) is green.
5. Confirm no secrets or sensitive data appear in the diff or logs.
6. Generate a report for your records:

   ```bash
   nal report \
     --status success \
     --run-url "https://github.com/<owner>/<repo>/actions/runs/<id>" \
     --summary "Implemented initial CLI scaffold" \
     --pr-url "https://github.com/<owner>/<repo>/pull/<n>"
   ```

## 4. When a run fails

Check, in order:

- The Actions logs for the failing step.
- Whether `ENABLE_CLAUDE_NIGHTLY` and `AWS_REGION` variables are set.
- Whether the `AWS_ROLE_TO_ASSUME` secret is present and the IAM trust policy
  allows this repository via OIDC.
- Whether the task exceeded `max_turns` or strayed outside its scope.
- Whether lint or tests failed — fix the task definition and re-run.

## 5. Scaling up

Only increase task size, `max_turns`, or eventually add scheduling once small
tasks run reliably and reviews are consistently clean.
