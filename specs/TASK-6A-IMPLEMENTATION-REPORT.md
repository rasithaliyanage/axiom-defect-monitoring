# Task 6A implementation report — presentation request seam

- **Date:** 2026-10-06
- **Branch:** `wushan` · **HEAD:** `3810dc0` · Git readable, no failures
- **Committed:** no. Tasks 4, 5, 6, the structure work and this increment are all uncommitted.
- **Readiness:** `specs/TASK-6A-READINESS.md` — readiness was blocked; scope narrowed by user decision.

## Scope implemented

The seam only: the presentation request becomes an explicit immutable domain value that the route
constructs after validation and hands to the service. **No wire change, no response change, no
contract change, no fixture move.** The five blockers in the readiness note remain deferred.

## Files created

| File | Purpose |
|---|---|
| `services/domain/request_context.py` | `Page` / `View` string enums and the frozen `ContextPayload` |
| `tests/api/test_request_context.py` | 23 tests for the seam |
| `specs/TASK-6A-READINESS.md` | Readiness, blockers, decisions |
| `specs/TASK-6A-IMPLEMENTATION-REPORT.md` | This report |

## Files modified

`services/domain/landing_service.py` — `presentation(view: str)` → `presentation(request: ContextPayload)`;
`VIEWS` keyed by `View`; new `PageMismatch`; request/context page association.
`services/domain/api/routes.py` — constructs `ContextPayload` after validation, handles `PageMismatch`.
`tests/api/test_landing_api.py` — three call sites updated to the new signature; the unknown-view test
rewritten, because an unknown view is now unrepresentable.

**Unchanged:** `specs/model-contracts.md`, both schemas, `validator.py`, `validation_models.py`,
`text_policy.py`, the renderer, `UISpec` types, and every fixture.

## Request type and immutability

```python
class Page(StrEnum):  LANDING = "landing"
class View(StrEnum):  OVERVIEW = "overview";  MINIMAL = "minimal"

@dataclass(frozen=True, slots=True)
class ContextPayload:
    page: Page
    view: View
```

Frozen and slotted, so assignment raises `FrozenInstanceError` and no attribute can be added.
`__post_init__` rejects non-enum values, because the type is also constructed in tests and could
later be constructed by a non-HTTP caller.

It carries **no grounding** — a test asserts its field set is exactly `{page, view}` and contains no
`metrics`, `alerts`, `actions`, `capabilities` or `contextId`. `ContextPayload` is the *presentation
request*; `GroundedContext` remains server-owned and is never supplied by a caller.

## Propagation and rejection

```
POST {page, view}  →  Pydantic transport model (extra="forbid")
                   →  ContextPayload(page=Page(...), view=View(...))     ← constructed only here
                   →  service.presentation(payload)
                   →  validator.validate(spec, COMPLETE server context)
                   →  {spec, bindings, meta}                              ← unchanged
```

The domain value is constructed **after** transport validation, so a malformed request cannot reach
the service. Five rejection cases are tested with the service replaced by a spy that records calls;
each asserts HTTP 400 **and** that the spy was never invoked. A query string is tested too: it is
ignored, not honoured.

## Server context ownership and validator integration

The service compares the request's `page` against both the server-owned context and the spec. A
mismatch raises `PageMismatch` → sanitized HTTP 500. **Neither the fixture nor the context is ever
rewritten to satisfy a request** — a test confirms the file on disk is unchanged after a mismatch.

A spy on the validator asserts it receives a plain `dict` carrying all ten `GroundedContext` fields,
and explicitly **not** a `ContextPayload`.

## Unchanged output

A test asserts the response keys are exactly `{spec, bindings, meta}`, that `meta` is exactly
`{contextId, source, validation}`, and that `generated_for` appears nowhere. Live verification
confirmed exact spec equality and ordered action-binding equality against the canonical pair.

## Verification — commands run

| Command | Result |
|---|---|
| `pytest --collect-only -q` | **217 collected** — 163 validator + 7 fixture + 24 API + 23 request-context |
| `pytest -q` | **217 passed**, 1 warning |
| `pip check` | No broken requirements found |
| `npm test` | **88 passed** (6 files) |
| `npm run typecheck` | clean, strict |
| `npm run lint` | `safety lint: clean (10 files, 9 rules)` |
| `npm run build` | built in 658ms |

### Schema checks, separated

| Check | Result |
|---|---|
| JSON parsing | PASS — selected schema |
| Draft 2020-12 **meta**-validation | PASS — selected schema |
| **Instance** validation (structure only) | PASS — both fixtures |
| **Full runtime** validation (structure + grounding + text policy) | VALID, 0 rejections — both fixtures |

The alternative `specs/ui-spec.schema.json` is **not** meta-validated by the current suite. Not claimed.

### Live API

```
GET  /health                              200  {"status":"ok"}
GET  /health  (via Vite proxy)            200  {"status":"ok"}
POST /api/v1/ui/landing-page              200  {spec, bindings, meta}
POST … + {"locale":"en-US"}               400  BAD_REQUEST     ← extra field rejected
POST /api/v1/ui/landing-page (via proxy)  200
```

Live response revalidated with the complete canonical context: **VALID**, exact spec equality,
action bindings equal, no `generated_for`.

### Browser

`POST http://localhost:5173/api/v1/ui/landing-page → 200` in the network log — page data comes from
FastAPI. Page text confirmed rendered fixture content, so React genuinely rendered rather than
serving a shell.

Backend stopped → page text showed the synthetic notice retained plus "The landing page could not be
loaded / Nothing was substituted in its place", with **no fixture content present**. No silent
fallback.

**Unverified:** screenshots. `Page.captureScreenshot` timed out repeatedly against the extension on
2026-10-06; evidence is page text and the network log instead. Narrow viewport and
cross-browser/assistive technology also remain unverified, as recorded for Task 6.

## Architectural invariants

- `ContextPayload` is the presentation request, never the `GroundedContext` — asserted by field set.
- Python retains schema, grounding and text-policy authority; nothing was duplicated in TypeScript.
- The renderer is unchanged; `UISpecRenderer` remains the only render path.
- Nine components and five context-bound inert actions preserved.
- `VALID` refers to a UI specification, never board approval or classification.
- No `eval`, `Function`, `dangerouslySetInnerHTML`, dynamic import or data-driven component lookup.

## Excluded scope — confirmed

No model, gateway, Agent SDK, database, authentication, physical integration, classification, ratio
calculation, quality approval or production infrastructure. No Task 7. No new dependency: the seam
uses stdlib `dataclasses` and `enum` only.

## Limitations

Screenshots unverified this session (extension timeout). Narrow viewport still unverified.

The five deferred blockers stand: `locale` as a request field, required-without-defaults, the
`422`/flat-body error contract, the canonical fixture relocation, and the alternative response
envelope. Each is a contract change needing the four-artefact update in `CLAUDE.md`.

`CLAUDE.md` rule 3 remains unsatisfied — no bounded repair, no deterministic fallback specification.

## Next smallest step

**TASK-005, the deterministic fallback specification.** Unchanged recommendation: it is the only
outstanding item a non-negotiable rule requires, and it adds no dependency.
