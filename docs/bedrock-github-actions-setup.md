# Running Claude Code from GitHub Actions on Amazon Bedrock

This document describes how a future nightly run will authenticate from GitHub
Actions to Amazon Bedrock. **No real credentials, account IDs, or ARNs are
stored in this repository** — only the names of the settings you will need.

## Authentication model

GitHub Actions authenticates to AWS using **OIDC + an IAM role**, not long-lived
access keys:

1. GitHub issues a short-lived OIDC token to the workflow job.
2. The job exchanges that token for temporary AWS credentials by assuming an
   IAM role (`AWS_ROLE_TO_ASSUME`) configured to trust GitHub's OIDC provider.
3. Those temporary credentials are used to call Bedrock.

This keeps secrets out of the repository and avoids storing AWS keys.

## What you must configure (names only)

Set these in **Settings → Secrets and variables → Actions**. Do **not** put any
of the real values in this repo.

### Repository Variables

| Name                    | Purpose                                                    |
| ----------------------- | ---------------------------------------------------------- |
| `ENABLE_CLAUDE_NIGHTLY` | Set to `true` to allow the Claude job to run.              |
| `AWS_REGION`            | AWS region hosting Bedrock, e.g. `us-east-1`.              |
| `BEDROCK_MODEL_ID`      | Bedrock model id, used via `${{ vars.BEDROCK_MODEL_ID }}`. |

The model id is referenced as a variable (not hard-coded) so it can change
without editing the workflow. See "Bedrock model" below for what to confirm.

### Repository Secrets

| Name                 | Purpose                                                       |
| -------------------- | ------------------------------------------------------------- |
| `AWS_ROLE_TO_ASSUME` | IAM role ARN trusted via GitHub OIDC (placeholder ARN below). |
| `SLACK_WEBHOOK_URL`  | Optional Slack incoming webhook for run notifications.        |

Placeholder values (illustrative only — replace in repo settings, never commit):

```text
AWS_ROLE_TO_ASSUME = arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>
AWS_REGION         = <REGION>
```

## Bedrock model

Set `BEDROCK_MODEL_ID` to the exact Bedrock model id you intend to use, and
confirm:

- account-level **model access** is granted for that model in `AWS_REGION`, and
- whether the model is served via a **cross-region inference profile** (this
  affects which resource ARNs the IAM policy must allow — see below).

The workflow uses `${{ vars.BEDROCK_MODEL_ID }}`; do not hard-code a model id in
the YAML.

## Dispatching from `develop`

The OIDC trust policy is scoped to the `develop` ref (see below). The OIDC `sub`
claim reflects the **ref the workflow runs on**, not the `base_branch` input.
Therefore any run that needs AWS **must be dispatched with `develop` selected as
the workflow ref** in the Actions UI. Do not run it from a `feature/*` or
`experiment/*` branch — merge the workflow change into `develop` first, then
dispatch from `develop`.

## Runners

For the initial proof of concept, use **GitHub-hosted runners**
(`ubuntu-latest`). Self-hosted runners are out of scope until the workflow is
proven.

## Public repository safety

This is a **public** repository. Therefore:

- Never commit secrets, tokens, webhook URLs, AWS account IDs, or role ARNs.
- Never `echo` secret values into logs or the job summary.
- Reference secrets only via `${{ secrets.* }}` / `${{ vars.* }}` in workflows.
- Pull requests from forks do not receive secrets by design — keep it that way.
- Review the Actions logs after a run to confirm no sensitive data leaked.
- The AWS **account ID is not treated as a secret** by
  `aws-actions/configure-aws-credentials`, so it can otherwise surface in logs.
  The workflow sets `mask-aws-account-id: true` on the credentials step to keep it
  out of the logs of this public repo.

## IAM role requirements (high level)

The assumed role needs a **trust policy** for the GitHub OIDC provider and a
least-privilege **permissions policy**. The concrete documents live in your AWS
account and are intentionally not stored here (placeholders only).

### Trust policy (scoped to repo + `develop`)

Condition the trust on:

- `token.actions.githubusercontent.com:aud` = `sts.amazonaws.com`
- `token.actions.githubusercontent.com:sub` =
  `repo:rauta0127/nightly-agent-lab:ref:refs/heads/develop`

This blocks other repositories, branches, and forks from assuming the role.
(If a GitHub Environment is adopted later, the `sub` becomes
`repo:rauta0127/nightly-agent-lab:environment:<ENV>` and the trust policy must be
updated accordingly.)

### Permissions policy (least privilege)

Allow only `bedrock:InvokeModel` (and `bedrock:InvokeModelWithResponseStream` if
streaming is used). Scope the **resource ARNs as narrowly as the selected
model/profile allows**:

- For a direct model, the single model ARN may suffice.
- For a **cross-region inference profile**, you must allow the profile ARN **plus
  the underlying foundation-model ARNs across the associated regions**, and model
  access must be enabled in each of those regions.

Start with the minimal ARN set the chosen model/profile actually needs. **Never**
use `bedrock:*` or resource `*` in steady state. If a broader scope is needed
briefly for diagnosis, revert it immediately afterward.
