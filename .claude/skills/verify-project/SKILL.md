---
name: verify-project
description: Run this repository's existing verification suites and report what actually happened. Use when asked to verify the project, check that everything still passes, run the tests, confirm a change is safe, or produce test evidence before a checkpoint.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# verify-project

Run the verification this repository already has, and report the real result.

This skill adds no test framework, writes no test, and changes no code. Its entire value is that the
numbers it reports were observed rather than remembered.

## Governed by

`.claude/rules/testing.md` says how to behave while doing this — above all, never report a result
that was not executed. `.claude/rules/security.md` covers the security checks. `tests/README.md` and
`apps/ui/README.md` describe the suites themselves. Read those; this file does not restate them.

## Procedure

**1. Establish where you are.** `git status --short` and `git branch --show-current`. A verification
report is about a specific working tree, so say which one.

**2. Pick the suites the change touched.** Run everything before a checkpoint; for a narrow change,
run what is relevant and say what you skipped and why. Running an unrelated suite proves nothing.

| Area changed | Suite |
|---|---|
| validator, schema, text policy, Domain Runtime, API | Python |
| renderer, registry, components, API client | React |
| anything under `apps/ui/src` | typecheck + safety lint |
| a specification or schema | Python, plus the schema checks below |

**3. Run them.** From the repository root unless noted:

```bash
.venv/Scripts/python.exe -m pytest -q          # Python suite
.venv/Scripts/python.exe -m pip check          # dependency consistency

cd apps/ui
npm test                                        # React suite (runs the fixture gate first)
npm run typecheck                               # tsc --noEmit, strict
npm run lint                                    # safety scan of the render path
npm run build                                   # prepare, typecheck, production build
```

Return to the repository root afterwards.

**4. Schema checks.** `tests/validator/test_task4_fixtures.py` and `test_fallback_spec.py` validate
the fixture pairs and the fallback against the loaded schema. Separately confirm the schema parses
and meta-validates as Draft 2020-12. Keep those two results distinct: parsing is not validation, and
neither is grounding.

**5. Security checks.** `npm run lint` is the render-path scan; `apps/ui/test/safety.test.tsx` holds
the injection and execution probes. Also confirm no secret, key or credential entered the diff.

**6. Report.** One row per check, with the actual number:

```
Python          282 passed, 2 warnings
React            93 passed (6 files)
typecheck        clean
safety lint      clean (10 files, 9 rules)
build            PASS (674ms)
schema           15 passed; parses and meta-validates as Draft 2020-12
```

## Reporting rules

Four distinct outcomes. Do not collapse them:

- **passed** — executed, and it passed
- **failed** — executed, and it failed. Quote the failure
- **skipped** — deliberately not run. Say why
- **unavailable** — could not run. Say what blocked it

"Unverified" is a usable answer. A fabricated pass is not, and it is the same failure this project
prohibits in the product, applied to our own evidence.

Report the counts you saw. Do not reconcile them against a number from a document, a previous run or
a task prompt — if they differ, the suite is right and the document is stale, and that gap is itself
worth reporting.

## Known environment issue

Under a sandboxed shell, six `tmp_path` tests can error with `PermissionError` on the system temp
directory. That is environmental, not a code failure. Re-run with `--basetemp` pointed at a writable
directory and report the clean result, noting the workaround.

## Out of scope

Do not modify a test, weaken an assertion or delete a case to produce a passing run. Do not commit or
push. Do not add a dependency, a runner or a framework. If a check genuinely cannot run, report it as
unavailable and stop — that is the correct output, not a problem to engineer around.
