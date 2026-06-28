# Nightly Task: Add --output option to nal report

## Goal
Add an optional `--output` argument to `nal report` so the generated report can be
written to a file instead of only being printed to stdout.

## Scope
- `src/nightly_agent_lab/cli.py`
- `tests/test_cli.py`
- `README.md`

## Out of Scope
- Any change to `nal new-task`.
- Adding new dependencies.

## Risk Level
low

## Acceptance Criteria
- `nal report` prints to stdout when `--output` is omitted.
- `nal report --output path/to/report.md` writes the report to the given file.
- Unit tests are added covering both cases.
- README is updated to document the new option.

## Commands to Run
```bash
python -m ruff check .
python -m pytest
```

## Safety Rules
- Do not commit secrets, tokens, or URLs containing credentials.
- Keep the change small and reviewable.
- Do not modify unrelated files.

## Expected Deliverables
- A branch off `develop` and a pull request targeting `develop`.
- Passing tests and lint.
- Updated README.

## Notes for Claude
This is a deliberately small task intended to validate the nightly workflow
end-to-end. Prefer clarity over cleverness. Use `develop` as the base branch;
`main` is reserved for stable releases.
