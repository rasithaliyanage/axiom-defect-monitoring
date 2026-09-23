# Task 3 local implementation report

## Outcome

Implemented the deterministic UISpec validator and tests against the updated version 1.0 model contract and the task-selected `specs/schemas/ui-spec.schema.json`. The user confirmed that this contract supersedes the old refusal and reference-based ProgressIndicator requirements. No model, renderer, API, repair orchestration, authentication or later inspection capability was built. Nothing was committed or pushed.

## Files created

- `services/__init__.py` and `services/domain/__init__.py`: minimal import packages.
- `services/domain/validator.py`: schema-backed validation, grounding, aggregate text checks, diagnostics and non-mutation.
- `services/domain/validation_models.py`: strict Pydantic context and result types.
- `services/domain/text_policy.py`: explicit deterministic text patterns.
- `services/domain/README.md`: usage, result contract, interpretations and limitations.
- `tests/validator/conftest.py`: fixed context fixtures and disabled networking.
- `tests/validator/test_validator.py`: parameterized deterministic tests and schema checks.
- `requirements.txt`: jsonschema 4.26.0 and pydantic 2.13.5.
- `requirements-dev.txt`: pytest 9.1.1 plus runtime requirements.
- `pytest.ini`: focused test discovery and import configuration.
- This implementation report.

A local `.venv` was created for installation and verification and is ignored by Git. No global Python packages were installed.

## Files modified

- `.gitignore`: ignore the virtual environment and Python/test caches.
- `tests/README.md`: current Task 3 run instructions and distinction from future application tests.
- `specs/schemas/ui-spec.schema-notes.md`: current v1 guidance; old partial-schema discussion retained as explicitly historical.
- `specs/TASK-3-READINESS.md`: record the user confirmation and subsequent implementation.

The normative model contract and both JSON schema files were preserved.

## Rules implemented

Uses Draft 2020-12 schema validation for all nine components, closed props, required fields, enums, string bounds and block/item/row limits. Runtime checks cover contextId equality; approved and available actions/categories; metric, alert and capability references; exact InfoPanel value/unit matching; percentage units and exact numeric progress; 4000 total rendered string characters; and documented deterministic text patterns.

All inspectable violations are collected, deduplicated and sorted in gate/path/code/rule/message order. Required and extra properties receive exact escaped JSON Pointer paths. Invalid JSON returns structured E_SCHEMA diagnostics. Invalid domain context raises a sanitized caller error. The validator does not mutate inputs or return a repaired specification.

The legacy refusal and progress shapes are explicitly rejected. No replacement refusal, 30-node rule, 8 KiB limit, steps/current relationship or generated_for structure was added.

## Verification results

Environment: Python 3.14.7, project-local virtual environment.

Commands actually run:

```text
.venv/Scripts/python.exe -m pytest -q
163 passed in 13.02s

.venv/Scripts/python.exe -m pip check
No broken requirements found.
```

An earlier run passed 162 tests. Review then improved missing/extra-field diagnostics and added a regression case, producing the final 163-test result above.

Coverage includes all nine components and five actions; valid minimal/composed pages; local array/string bounds; exact 4000-character limits; nested card rules; unknown types/props; grounding and numeric precision; malformed/cyclic inputs; deterministic ordering; non-mutation; no validation-time file reads; no external schema retrieval; and networking disabled for every test.

Task 2 checks are executed within the suite: the selected schema is checked against the Draft 2020-12 meta-schema, component/action coverage is asserted, and the updated model contract's valid example passes structural and runtime validation using fixed context. This is actual execution evidence, not a reused result from the schema report or onboarding tutorial.

## Interpretations and remaining limits

`services/domain/README.md` records the implementation choices needed where prose was underspecified: the local result structure; code-point counting of displayed string fields; JSON-number grammar for progress metrics; malformed context as a caller error; and existing E_PROP_INVALID for unavailable alertId. No new rejection codes were invented.

Text checks are deterministic patterns, not a proof of arbitrary natural-language meaning. They cannot guarantee all implied verdicts, capability honesty, locale compliance or injection detection; false positives and false negatives remain possible. VALID means the implemented deterministic rules passed. Semantic evaluation is still needed before an integrated approval/rendering path can be claimed complete.

The alternative `specs/ui-spec.schema.json` has different bounds and remains unused. The selected schema's InfoPanelRow.value description contradicts its maxLength keyword; the keyword is enforced. These pre-existing discrepancies remain recorded without silently changing contract files.

## Git state and proposed checkpoint

Branch: `wushan`. HEAD text: `443221d7d7905a16e542884ec5a8f7fe4f7e56be`.

`git status --short` fails with `fatal: bad object HEAD`. Final `git diff --stat` and `git diff` fail with `fatal: unable to read 12422d3a056648bc1aac7574633c51e44b136b4b`. Consequently no reliable clean/dirty status or Git diff can be claimed. Local source files and the change list above were inspected directly. Git data was not repaired or modified.

Proposed next checkpoint: review these local Task 3 changes and interpretation choices, reconcile the remaining schema/documentation discrepancies, and restore readable repository objects before considering a commit. No Task 4 work was started.
