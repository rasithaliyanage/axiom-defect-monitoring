# Hooks

Shell commands the harness runs automatically on Claude Code events. Unlike `CLAUDE.md`, a hook is
executed rather than read, so this is where a constraint can actually be **enforced** rather than
stated.

**Status:** empty. No hooks are configured. `.claude/settings.json` carries empty permission lists.

## Candidates, none yet implemented

Each of these corresponds to a rule the repository currently relies on documentation or a test to
uphold:

| Hook | Would enforce |
|---|---|
| Pre-commit prohibition scan | `CLAUDE.md` rule 2 — reject `eval`, `new Function`, `dangerouslySetInnerHTML` or model-driven dynamic import reaching the render path |
| Pre-commit policy check | No invented value lands in `policies/` |
| Post-edit contract check | A change to the schema, vocabulary or props also touches model contract, tests and evals, per "Contract changes are wide changes" |
| Pre-commit test gate | Both suites pass before a commit is accepted |

The prohibition scan currently exists as a test in `apps/ui/test/safety.test.tsx`, which catches it
in CI rather than at the moment of writing. A hook would catch it earlier; the test should remain
either way.

## Caution

A hook runs with the user's permissions. Keep them narrow, fast and read-only where possible, and
never make one destructive.
