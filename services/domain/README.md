# Domain Runtime

Task 3 implements `UISpecValidator` in `validator.py`, typed context/results in `validation_models.py`, and explicit deterministic text checks in `text_policy.py`.

Task 6 adds the HTTP boundary in `api/` and fixture orchestration in `landing_service.py`. **This is the Domain Runtime, not the AI Runtime** — there is no model gateway, no model call and no generation anywhere in this package. The specification it serves is developer-authored and synthetic.

## HTTP boundary (Task 6)

Run from the repository root:

```
.venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8000
```

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Returns exactly `{"status": "ok"}`. Process liveness only — **not** inspection or manufacturing readiness |
| `/api/v1/ui/landing-page` | POST | Returns the validated synthetic landing presentation |

**Request** is presentation-only. Every field is **required, with no defaults** — the request states what it asks for rather than relying on the server to fill gaps. `extra="forbid"` means a request supplying grounding (`context`, `metrics`, `alerts`, `actions`, `blocks`, `contextId`) is **rejected**, not ignored — the browser cannot supply grounding truth.

```json
{ "page": "landing", "view": "overview", "locale": "en-US" }
```

| Field | Values | Notes |
|---|---|---|
| `page` | `landing` | |
| `view` | `overview`, `minimal` | Selects from a fixed catalogue; can never name a path |
| `locale` | `en-US` | Compared against the server context's locale; not echoed in the response |

`locale` carries one member today. The value is not invented — it is the locale already present in every server-owned context. Further locales are a business decision and are added only when that decision is made.

**Success — HTTP 200:**

```json
{ "spec":     { "specVersion": "1.0", "page": "landing", "contextId": "...", "blocks": [...] },
  "bindings": { "actionLabels": { "view-defect-reports": "Open defect reports" } },
  "meta":     { "contextId": "...", "source": "fixture", "validation": "VALID" } }
```

`bindings` exists because `Hero.primaryAction` is an identifier and the UI specification carries no label for it — a bare spec provably cannot supply this. `meta` is informational; `validation` is **not** the client's proof and the browser adapter does not trust it.

**Errors** use one sanitized envelope. Validator rejection codes are logged server-side and never serialized:

```json
{ "error": { "code": "BAD_REQUEST" | "VALIDATION_FAILED", "message": "..." } }
```

| Status | `error.code` | Cause |
|---|---|---|
| `400` | `BAD_REQUEST` | Unsupported request shape, or supplied grounding |
| `404` | `NOT_FOUND` | Unknown route |
| `405` | `METHOD_NOT_ALLOWED` | Wrong method |
| `500` | `VALIDATION_FAILED` | A fixture failed validation. A server defect; the spec is never returned |

The handler is registered against **Starlette's** `HTTPException`, not FastAPI's. FastAPI's subclasses
it, so the parent catches both the errors our routes raise and the routing errors (404, 405) that
Starlette raises. Registering against FastAPI's would miss routing errors and leak Starlette's
default `{"detail": ...}` shape — which it did until it was caught by the Task 6 checkpoint review.

## The presentation request (Task 6A)

The route validates the transport model, then constructs an immutable domain value and passes it to
the service explicitly:

```python
payload = ContextPayload(page=Page.LANDING, view=View.OVERVIEW)   # frozen, enum-typed
presentation = service.presentation(payload)                      # was presentation(view: str)
```

`ContextPayload` (`request_context.py`) is the **presentation request** — what the caller asked to
see. It is **not** the `GroundedContext`, which is server-owned and never supplied by a caller. It
carries no metrics, alerts, actions or contextId.

The domain value is constructed only *after* transport validation, so a malformed request cannot
reach the service. The service compares the request's page against the server-owned context and
spec; a mismatch is an internal failure (`PageMismatch` → sanitized 500) and neither the fixture nor
the context is ever rewritten to satisfy a request.

More request dimensions (line, shift, board type, locale) are expected. They are deliberately absent:
their value sets are business-owned and undecided. When decided they become additional fields and
enum members — the seam does not need redesigning.

## Validation happens before any success response

`landing_service.py` deep-copies the spec and its complete context, calls the **existing** `UISpecValidator.validate(spec, context)` unchanged, requires `VALID`, and returns exactly the object that was validated. Nothing is repaired, substituted or omitted, and no rejection code was added.

Copies isolate requests from each other. **Copying is isolation, not validation** — the validator call is what makes the response safe to return.

## Canonical fixtures

`tests/fixtures/ui-spec/` — the same pair the offline preparation gate validates. This package owns no second copy.

## CORS

None. The Vite dev server proxies `/api` to port 8000, so the browser sees one origin.

The current version 1.0 contract supersedes the old `view/components/type/ref` model, as confirmed for this task. The old refusal object is invalid; version 1.0 defines no refusal variant. ProgressIndicator uses `metricId`, `label` and numeric `value` matched to a context metric with unit `%`. No onboarding `steps`, `current`, `generated_for`, 30-node rule or 8 KiB limit is implemented.

## Usage

From the repository root, after installing the requirements:

```python
from services.domain.validator import UISpecValidator

validator = UISpecValidator()  # Loads and meta-validates the local schema once.
context = {
    "contextVersion": "1.0",
    "contextId": "example-context",
    "page": "landing",
    "locale": "en-US",
    "generatedAt": "2026-09-22T06:00:00Z",
    "capabilities": [],
    "defectCategories": [],
    "metrics": [],
    "alerts": [],
    "actions": [],
}
spec = {
    "specVersion": "1.0",
    "page": "landing",
    "contextId": "example-context",
    "blocks": [{"component": "Text", "props": {"text": "Inspection activity"}}],
}
result = validator.validate(spec, context)
print(result.model_dump_json())
```

`validate` accepts raw JSON text or an already decoded JSON value. The context is a dictionary or a `GroundedContext` model. Validation performs no file access, network access, database access, model call, time lookup or rendering. Constructor file access is limited to the explicitly selected local schema. External schema references are refused; no remote resolver is used.

Raw JSON rejects duplicate keys and non-JSON numbers. Decoded inputs must contain only finite JSON-compatible values (Decimal is also supported for exact numeric inputs); cyclic structures, non-string object keys and lone Unicode surrogates are rejected. The function copies input data for inspection and never repairs or mutates caller data.

## Structural authority

The task-selected file is `specs/schemas/ui-spec.schema.json`. Its Draft 2020-12 schema implements component/property types, required fields, enums, local bounds and structural nesting. JSON Schema is used directly rather than duplicating these rules in Pydantic output models.

The other file, `specs/ui-spec.schema.json`, is not loaded. Its differing limits are documented in `specs/TASK-3-READINESS.md`; neither schema was changed for Task 3. Construction freezes which schema is used for subsequent calls. Identifier enum sets are obtained from that schema, including the action set used to check Hero.primaryAction at runtime.

Pydantic provides the strict typed context and immutable result envelope required by the repository conventions. It does not coerce metric values, generate timestamps, fetch data or populate missing required context fields. Duplicate identifiers within a collection and dangling context alert categories are caller errors. Context timestamps are retained as strings, as defined by the input interfaces; validating domain timestamp formats is not part of UISpec validation.

## Result interface and deterministic diagnostics

The local validator interface is an implementation choice because the version 1.0 prose defines rejection codes but not a Python return type:

```json
{
  "status": "INVALID",
  "rejections": [
    {
      "gate": 3,
      "code": "E_CONTEXT_MISMATCH",
      "path": "/contextId",
      "rule": "context_id",
      "message": "Context identifier differs from the request"
    }
  ]
}
```

Paths are escaped JSON Pointers; the root is an empty string. Results use only the existing contract rejection codes. Diagnostics are deduplicated and sorted by `(gate, path, code, rule, message)`, using lexical path ordering. Invalid fields may produce several applicable codes: a bad prop can produce both E_SCHEMA and E_PROP_INVALID, for example. Messages do not contain raw model payloads or stack traces.

Discriminator-based schema failures report errors from the named component's branch, not hypothetical errors for the other eight branches. After structural failures, the validator continues every check that can safely inspect the available data. Unparseable input cannot undergo later gates and returns E_SCHEMA. Malformed/inconsistent domain context raises a sanitized `InvalidContextError`; it is a caller failure, not a model rejection with an invented code.

The model contract lacks a dedicated missing-alert code. This implementation uses the existing E_PROP_INVALID (Gate 2: prop value outside its allowed set) with `rule: reference` for unavailable `alertId`. It does not introduce or rename a rejection code. This mapping is a documented interpretation for review.

## Runtime rules and interpretations

- **Context identity:** exact equality of UISpec.contextId and the supplied contextId.
- **Identifiers:** actions and categories must be in the schema's approved enum and the supplied context. Metrics, alerts and capabilities must exist in their corresponding context collection. FeatureGrid card capability references are checked too.
- **InfoPanel:** values are compared character-for-character with Metric.value. If the output includes a unit it must match the context unit exactly; omission is allowed because the contract makes the output unit optional. No formatting, rounding or conversion occurs.
- **ProgressIndicator:** the context metric must use `%`. Its value must be a finite JSON-number-form string: optional minus, decimal fraction and exponent, without whitespace, leading plus, separators or percent suffix. Decimal comparison preserves precision and accepts equivalent forms such as `2.40` and `2.4`. Raw JSON numeric tokens use Decimal parsing. For decoded float input, comparison uses the supplied float's string representation; use raw JSON or Decimal when exact decimal precision matters. No tolerance or rounding is introduced.
- **4000-character total:** sum Unicode code points in the rendered string fields only. Count Hero eyebrow/title/subtitle; Heading/Text text; FeatureCard title/body including every grid item; CTA label; Alert title/body; InfoPanel title and each row's label/value/unit; ProgressIndicator label/caption. Count repeated occurrences separately. Exclude keys, IDs, component names, enums and envelope metadata. Exclude numeric ProgressIndicator.value because no renderer formatting is defined. This counting interpretation resolves the prose's unspecified field selection and is explicit here, not an added size limit.
- **Nesting:** FeatureGrid items are card props, not nested block envelopes. Generic children and nested component envelopes receive E_DEPTH_LIMIT in addition to applicable schema errors. Other invalid nested values are rejected by schema conformance.
- **URLs:** no host allow-list or URL property is added. Closed props reject unknown URL-bearing fields, and rendered text is checked for URL/email/path patterns.

## Text-policy coverage and limitations

`text_policy.py` exposes the actual deterministic patterns. Code-like strings are checked everywhere in output values, including identifiers. Recognized markup, Markdown formatting, locations, emoji ranges, generation self-reference and quality-decision wording are checked in rendered strings. Cases include the contract's script, quality-verdict and URL examples. Word boundaries avoid rejecting unrelated words such as `compass` merely because they contain `pass`.

These are deterministic pattern checks with potential false positives and false negatives. They do not understand every locale, Markdown form, programming language, URL form, capability claim, instruction, or implied verdict. In particular they do not certify general capability honesty or semantic absence of quality judgements. Context text is never executed or followed, but detecting and recording an injection attempt by the generation model belongs to model orchestration/evaluations.

**VALID means the schema, implemented grounding rules and documented deterministic policy checks passed.** It is not proof that unrestricted prose satisfies every semantic prohibition. The contract's exhaustive natural-language requirements cannot be guaranteed by these tests or a keyword filter. No renderer or production approval path is built in Task 3; later integration must account for these limitations and model evaluations.

## Verification

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe -m pytest -q
```

Tests use fixed synthetic context and specifications. Networking is disabled by an autouse fixture. Coverage includes all nine components/five actions, local bounds, closed and nested props, supplied-context checks, percentage precision, text patterns, 4000-character boundaries, non-mutation and repeatability, malformed input, the updated contract's valid example and Draft 2020-12 meta-schema validation.

Installation needs package access; validation and tests do not. Git repair, model repair, renderer omission behaviour, fallback rendering and application integration remain outside this change.
