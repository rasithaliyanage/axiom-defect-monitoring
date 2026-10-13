# Rule: testing

**Scope:** engineering-time guidance for Claude Code. Enforces nothing at runtime — see
[`README.md`](README.md).

**Authority:** `tests/README.md` describes the deterministic suites; `evals/README.md` describes AI
evaluations. The distinction between them is explained in both and in the root `README.md`.

## Read the tests before changing the code

Existing tests are the clearest statement of what the current behaviour is *supposed* to be. Before
modifying implementation code, find the tests that cover it and read them. A surprising assertion is
usually a recorded decision, not an oversight.

## Run what the change touched

| Changed | Run | Command |
|---|---|---|
| Validator, schema, text policy | Python suite | `.venv/Scripts/python.exe -m pytest -q` |
| Domain Runtime, API, services | Python suite | same |
| Renderer, registry, components, client | UI suite | `cd apps/ui && npm test` |
| Render-path safety | Safety lint | `cd apps/ui && npm run lint` |
| TypeScript types | Typecheck | `cd apps/ui && npm run typecheck` |

`pytest.ini` sets `testpaths = tests/validator tests/api`. A new Python test outside those trees is
not collected, so confirm collection rather than assuming it — read the collected count.

Run the full suite before calling a change complete, not just the file you touched. Do not run
unrelated suites for their own sake; a UI-only change does not need a Python regression argument.

## Add tests for deterministic behaviour

Anything with a repeatable right answer gets a deterministic test: a validation outcome, a rejection
code, a status code, an error shape, a render decision. Measuring model behaviour across a case set
belongs in `evals/`, is scored rather than pass/fail, and is not a substitute for a test.

A contract change is wide. Per `CLAUDE.md`, a change to the component vocabulary, component props,
the grounded context shape or the UI specification schema requires all four of
`specs/model-contracts.md`, `specs/schemas/ui-spec.schema.json`, `tests/` and `evals/` in the same
change. The acceptance criteria those tests exist to satisfy are listed in `specs/spec.md`.

## Do not soften a test to make a change pass

A failing test is information. The order of response is: understand why it fails, then decide whether
the code or the expectation is wrong.

Never delete a test to get to green. Never weaken an assertion — widen a range, drop a field,
loosen an exact match to a substring, add a skip — without saying in the change description what
property is no longer covered and why that is acceptable. If the old expectation was genuinely
wrong, replace it with one that is right and says so; do not quietly narrow it.

A test that is awkward to satisfy is sometimes pointing at a real boundary. That has already happened
in this repository more than once.

## Report what actually ran

Never state that a test passed unless you executed it in that session and read the result. Never
present a prior run as a current one. Never report a count you did not see.

If a check could not run — tooling missing, environment refusing, a sandbox permission error — say
that it did not run and why. "Unverified" is a usable answer; a fabricated pass is not, and it is
exactly the failure mode `business-data-integrity.md` prohibits in the product, applied to our own
evidence.

Partial results get reported partially: which suites ran, which did not, and what remains unknown.
