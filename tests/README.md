# Deterministic tests

## Task 3 implementation

The UISpec 1.0 validator suite now lives in `tests/validator/`. Run it from the
repository root with `.venv/Scripts/python.exe -m pytest -q` after installing
`requirements-dev.txt` into the local virtual environment. See
`services/domain/README.md` for setup, the result interface, interpretation
choices and deterministic text-policy limitations.

For this increment, `specs/schemas/ui-spec.schema.json` is the selected structural
authority. The superseded `view/components` refusal and `ref`-based progress
format are invalid under v1 and are tested as rejections. No renderer, API,
model gateway, repair or fallback orchestration tests are claimed here.

The strategy below includes future application-level checks. Its statement that
all implied decision language is caught is an aspiration, not a property proven
by the current pattern checks. Semantic evaluation remains necessary.

## Purpose

This directory holds deterministic software tests. They call no AI model, depend on no network, and
produce identical results on every run. They gate every change to the repository.

Non-deterministic measurement of model behaviour belongs in `evals/`, not here. If a check's result can
vary between two runs of the same code, it is an evaluation and it is in the wrong directory.

## What these tests must establish

The validation pipeline rejects what the contract says it rejects. For every rejection code in
`specs/model-contracts.md` there is at least one test supplying a crafted specification that triggers it
and asserting the exact code. Crafted fixtures stand in for model output; no model is invoked.

The renderer cannot render an unapproved component. A block naming an unregistered component is omitted
and recorded. There is no fallback resolution path, and a test asserts that no dynamic execution
mechanism — `eval`, `new Function`, `dangerouslySetInnerHTML`, model-driven dynamic import — exists in
the renderer or the registry.

Registry completeness matches the specification. The registry contains exactly the nine components in
FR-2, no more and no fewer.

Grounding is exact. A metric value differing from the grounded context in any character, including
rounding and thousands separators, is rejected. A unit mismatch is rejected.

Decision language is caught. Text asserting a pass, fail, approval, rejection, or fitness outcome is
rejected with `E_DECISION_LANGUAGE`, including phrasings that imply the outcome without using the exact
word.

The fallback specification is valid. It passes the schema and all four gates, and it references no
metric, alert, or defect category. This is asserted, not assumed.

Rejection reporting is complete. An output with several distinct violations reports all of their codes,
per VR-11.

Repair is bounded. Exactly one repair attempt occurs, and the second failure yields the fallback. A
test with a stub gateway that always fails asserts the call count.

Failure paths resolve to the fallback. Model unavailability, timeout, and transport error each produce
the fallback specification and a recorded outcome, with no repair attempt for transport failures.

Domain API contracts hold. Each endpoint in the specification's API surface returns its declared shape,
and the defect endpoints expose only approved categories.

Generation records are complete. A generation writes the context identifier, raw output, outcome,
rejection codes, source, and latency, and writes no image content.

## Planned layout

Created alongside the code they cover, not in advance.

```
tests/
  validator/        one file per validation gate, plus rejection-code coverage
  renderer/         registry mapping, unapproved component handling, no-execution assertions
  domain/           API contract tests for inspection, ingest metadata, defect reporting
  fallback/         fallback specification validity and failure-path behaviour
  fixtures/         crafted valid and invalid specifications, and grounded context samples
```

Fixtures are shared with `evals/` where the same case is useful to both. A fixture is a static file; it
never contains live model output captured without review.

## Conventions

One behaviour per test, named for the behaviour rather than the function under test.

Assert on rejection codes, never on human-readable messages. Codes are contract; messages are not.

No sleeps, no real clocks, no random values, no network. Inject time and identifiers.

Every contract change lands with its test change in the same commit, per `CLAUDE.md`.

## Runner

Not yet chosen. The runner is selected in the increment that introduces the first executable code, so
that the choice follows the code rather than constraining it. Expect Python tooling for the Domain and
AI Runtimes and TypeScript tooling for the UI Runtime.
