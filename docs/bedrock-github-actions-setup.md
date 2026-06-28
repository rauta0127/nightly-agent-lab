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

| Name                    | Purpose                                              |
| ----------------------- | ---------------------------------------------------- |
| `ENABLE_CLAUDE_NIGHTLY` | Set to `true` to allow the Claude job to run.        |
| `AWS_REGION`            | AWS region hosting Bedrock, e.g. `us-east-1`.        |

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

## IAM role requirements (high level)

The assumed role needs a trust policy for the GitHub OIDC provider (scoped to
this repository) and a permissions policy allowing the relevant
`bedrock:InvokeModel*` actions for the model(s) you intend to use. The concrete
policy documents are configured in your AWS account and are intentionally not
stored here.
