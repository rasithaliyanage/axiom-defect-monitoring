# Task 5 implementation report — minimal runnable React UI

- **Date:** 2026-09-30
- **Branch:** `wushan` · **HEAD:** `3810dc0` · Git readable, no failures
- **Committed:** no. Task 4, the repository-structure work and this increment are all uncommitted.

## Correction to the task premise

The Task 5 prompt described an existing Vite shell and synthetic demonstration, and named
`apps/ui/scripts/prepare_fixtures.py`, `src/generated/fixtures.ts`, `index.html`, `src/main.tsx`,
`src/style.css`, `ControlledRenderer`, `approvedFixture()`, `tests/renderer_fixtures/`,
`specs/TASK-4-IMPLEMENTATION-REPORT.md`, `npm run dev` and `npm run lint`.

**None of those existed.** Task 4 in this repository produced a renderer *library* exercised in
jsdom. `vite.config.ts` carried only a Vitest `test:` block; there was no HTML entry, no dev script
and no browser path of any kind. The prompt appears to describe the Customer Onboarding tutorial's
Task 4, consistent with its own warnings not to copy tutorial commit IDs, versions or test counts.

Task 5 was therefore **build**, not **verify and complete**. Everything below is new work except
where marked as pre-existing.

## What already existed (Task 4, unchanged in substance)

`apps/ui/src/renderer/{types.ts,registry.ts,renderUISpec.tsx}`, `src/components/approved.tsx`, three
test files (56 tests), `tests/fixtures/ui-spec/*.{spec,context}.json`, and
`tests/validator/test_task4_fixtures.py`. The nine-component registry, the exhaustive switch, the
omit-and-record path and the DOM-safety rules are reused as they were.

## Files created

| File | Purpose |
|---|---|
| `apps/ui/scripts/prepare_fixtures.py` | Offline gate. Runs the Task 3 validator over every fixture pair, emits the catalogue, deletes output and exits non-zero on failure |
| `apps/ui/scripts/prepare.mjs` | Portable launcher — npm scripts run under cmd.exe on Windows, where a bare relative interpreter path fails |
| `apps/ui/scripts/safety-lint.mjs` | `npm run lint`. Node standard library only, no new dependency |
| `apps/ui/src/generated/fixtures.ts` | **Generated.** Validated specs, context-sourced action labels, verification hashes |
| `apps/ui/src/renderer/approved.ts` | The approved-input boundary; the only module that can mint the brand |
| `apps/ui/src/App.tsx` | Application root. Extracted so it can be mounted in tests without a DOM entry point |
| `apps/ui/src/main.tsx` | Browser entry. Accepts no input of any kind |
| `apps/ui/src/ErrorBoundary.tsx` | Fixed message on render failure. Not a repair or fallback loop |
| `apps/ui/src/style.css` | Developer-authored styling |
| `apps/ui/index.html` | HTML shell |
| `apps/ui/test/support/approve.ts` | Test-only minting, deliberately outside `src/` |
| `apps/ui/test/app.test.tsx` | 13 Task 5 tests |

## Files modified

`apps/ui/package.json` — added `prepare:fixtures`, `dev`, `lint`; `test` and `build` now run the gate
first. `apps/ui/src/renderer/renderUISpec.tsx` — the `spec` prop narrowed from `UISpec` to
`ApprovedUISpec`. The three existing test files — wrapped their specs in `approveForTest(...)`; no
assertion changed.

## The approved-input path

```
tests/fixtures/ui-spec/*.{spec,context}.json      developer-authored, synthetic
        ↓   scripts/prepare_fixtures.py  →  services/domain/validator.py
        ↓   any INVALID ⇒ output deleted, exit 1
src/generated/fixtures.ts                          + sha256 of every input
        ↓   src/renderer/approved.ts                the only minting point
ApprovedUISpec handle
        ↓
UISpecRenderer → registry → React → browser
```

**What the brand proves, and what it does not.** `ApprovedUISpec` is branded with a `unique symbol`
that is not exported, so no value of that type can be constructed outside `approved.ts`. That makes
"no raw JSON reaches the renderer" a compile-time property of **provenance**.

It is **not** validation. A cast, brand or `approved: true` flag is worthless as evidence on its own.
The evidence is the offline Python gate, recorded as content hashes in `VERIFICATION` and surfaced in
the page notice. There is no live browser-to-Python transport, and none is claimed.

**Naming.** The renderer is still `UISpecRenderer`, not `ControlledRenderer`. §7 says to use the
actual existing API and not to recreate the renderer; a rename would be churn with no behavioural
gain. Role mapping: `full-catalogue` is the prompt's "overview" fixture, `task4-demo` its "minimal".

## Fail-closed behaviour, demonstrated

An unapproved `DispositionControl` block was temporarily injected into `task4-demo.spec.json`:

```
  1 E_SCHEMA            /blocks/3            Schema constraint violated: oneOf
  2 E_UNKNOWN_COMPONENT /blocks/3/component  Component is not approved
FIXTURE PREPARATION FAILED: task4-demo: validator returned INVALID
Generated catalogue removed. The application cannot load stale data.
EXIT=1        fixtures.ts present? NO
```

Both gates reported, generated output removed, non-zero exit. The fixture was restored to its
original three blocks and the gate re-run clean. No new rejection code was introduced.

## Verification — commands actually run

All from `apps/ui` unless stated.

| # | Command | Result |
|---|---|---|
| 1 | `npm test` | **69 passed** (4 files) — 56 pre-existing + 13 new |
| 2 | `npm run typecheck` | clean, strict, no `any` |
| 3 | `npm run lint` | `safety lint: clean (9 files, 9 rules)` |
| 4 | `npm run build` | built in 1.20s — 36 modules, `dist/index.html` 0.45 kB, CSS 4.43 kB, JS 232.03 kB |
| 5 | `npm run prepare:fixtures` | both fixtures VALID |
| 6 | `.venv/Scripts/python.exe -m pytest -q` (root) | **170 passed** |
| 7 | `.venv/Scripts/python.exe -m pip check` (root) | No broken requirements found |

Pytest needs a writable `--basetemp` on this machine; without it one pre-existing test errors on a
Windows temp-directory permission fault unrelated to this work.

### Schema checks, reported separately

| Check | `specs/schemas/…` (authority) | `specs/ui-spec.schema.json` (deprecated) |
|---|---|---|
| JSON parsing | PASS | PASS |
| Draft 2020-12 **meta**-validation | PASS | PASS |
| **Instance** validation of both fixtures (structure only) | PASS | not used |
| **Full runtime** validation (structure + grounding + text policy) | VALID, 0 rejections | not used |

These are four distinct checks. Meta-validation asks whether the schema is itself a valid schema;
instance validation asks whether a document conforms to it; runtime validation adds grounding and
text policy, which JSON Schema cannot express.

### Browser check — **UNVERIFIED**

`npm run dev` started cleanly and served correctly:

- `GET /` → **200**, 608 bytes, with `<div id="root">` and the module script
- `GET /src/main.tsx` → **200**, transformed by Vite
- `GET /src/generated/fixtures.ts` → **200**

**This is not proof that React rendered**, and the task says so explicitly. The Chrome extension
reported "Browser extension is not connected", so the required observations — visible notice,
rendered components, inert controls, keyboard focus, console and network activity, narrow and wide
viewports, screenshot — **were not made**. The dev server was stopped afterwards.

The closest available evidence is indirect: `test/app.test.tsx` mounts `App` through real React DOM
in jsdom and asserts the notice, the block count, heading levels, action dispatch, determinism and
non-mutation. That is a genuine render, but it is not a browser.

## Scope boundaries held

No runtime AI, model gateway, FastAPI integration, authentication, persistence or infrastructure. No
camera capture, defect inference, defect-ratio calculation, image overlay or approval workflow. No
second UI project. The model contract, both schemas and the validator API are untouched — confirmed
by `git status`, which shows no modification to `specs/model-contracts.md`,
`specs/schemas/ui-spec.schema.json` or `services/domain/`.

No new dependency was added. `lint` is implemented with the Node standard library rather than
pulling in ESLint.

## Limitations

The browser check is unverified, as above — the single most significant gap in this increment.

`npm run typecheck` alone does not run the preparation gate, so a clean checkout must run
`npm run prepare:fixtures` (or `test`/`build`/`dev`, which do) before `src/generated/fixtures.ts`
exists. The generated file is committed so the repository typechecks on clone.

The safety lint is a textual scan of `src/**` with comments stripped. It is not a proof about the
dependency tree.

`CLAUDE.md` rule 3 requires a deterministic fallback specification after one bounded repair attempt.
Neither exists. The error boundary is **not** that fallback and does not stand in for it.

## Recommended next task

**TASK-005, the deterministic fallback specification** — as already recorded in `tasks/tasks.md`.
It is the smallest remaining increment, adds no dependency, and closes a non-negotiable rule the
codebase does not currently satisfy.

Separately, the browser verification should be repeated once extension access is available.
