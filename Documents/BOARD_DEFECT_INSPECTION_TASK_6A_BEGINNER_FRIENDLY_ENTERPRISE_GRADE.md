# BOARD DEFECT INSPECTION AI
@ Task 6A — ContextPayload Request Seam
@ Beginner-Friendly Enterprise-Grade Implementation Guide
@ Proposed increment: explicit presentation request propagation

**Status: proposal only — no Task 6A implementation or verification performed.**
**Document date:** 2026-10-03. Task 6 is implemented locally with retained verification evidence; its formal Git checkpoint is pending. Observed branch: wushan. HEAD: 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da. The dirty working tree contains previous and unrelated work.

**Reference:** Customer_Onboarding_Task_6A_Beginner_Friendly_Enterprise_Grade.docx.pdf, the available 19-page export in Documents. Its 27-section sequence is preserved here. Its completed-status claims, query parameters, generated_for metadata, test counts and commits are not transferred to this project.

**Readiness decision:** This guide recommends the smallest wire-compatible seam: explicitly carry the already-supported page/locale request into the domain service. It does not authorize new board/line/shift fields. If Task 6A is intended to introduce multiple business-context variants, stop before implementation and agree their contracts, server-owned context mapping and browser admission strategy. Document creation is not approval of an API redesign.

## 1. Purpose of Task 6A

The proposed increment makes presentation request data explicit in the application and domain service while preserving deterministic fixture output. Task 6 already validates {"page":"landing","locale":"en-US"} at HTTP ingress. However, the route currently discards the parsed request object and calls get_landing_ui_spec() without parameters; the browser loader constructs those values internally.

Task 6A would name and carry that existing request as an immutable ContextPayload from the developer-authored frontend setting through HTTP validation into the service. The service would check that its independently owned complete GroundedContext matches the request's supported page and locale, then validate and return the unchanged fixture.

Key lesson: request intent becomes explicit and testable across layers; it does not become grounding truth. No probabilistic generation, new production facts or new dashboard functionality is introduced.

## 2. Where Task 6A Fits

```text
Task 1   Foundation and business scope
   |
Task 2   v1 model contract and selected JSON Schema
   |
Task 3   Deterministic Python validation
   |
Task 4   Fixed React registry / controlled renderer
   |
Task 5   Browser-ready synthetic demonstration
   |
Task 6   Local Domain API and approved-response admission
         Implementation exists; formal checkpoint pending
   |
Task 6A  PROPOSED explicit page/locale request seam
   |
Human review -> checkpoint only if explicitly authorized
   |
Future   Separately reviewed AI input/transport design
```

Task 6A is a proposed internal propagation improvement, not the first contextual HTTP request. Do not claim Task 6 lacked a presentation request, or that this document completed a new milestone.

## 3. What Would Change from Task 6 to Task 6A

```text
CURRENT TASK 6
App -> fetchLandingPage(signal)
    -> loader hard-codes page + locale
    -> fixed POST -> strict LandingRequest validation
    -> get_landing_ui_spec() (no request argument)
    -> fixed pair -> Python validation -> exact response
    -> full fixed-response admission -> private handle -> renderer

PROPOSED TASK 6A
App INITIAL_CONTEXT: page + locale
    -> fetchLandingPage(request, signal)
    -> snapshot supported request -> same fixed POST/body
    -> strict HTTP validation -> immutable ContextPayload
    -> get_landing_ui_spec(request_context)
    -> fixed server GroundedContext matches page + locale
    -> same Python validation and exact unchanged response
    -> full admission + request/page association
    -> private handle -> same renderer
```

Successful wire output, component order, metrics, action bindings and browser appearance remain unchanged. Traceability is established through explicit arguments and tests, not a new telemetry system, request echo envelope or client-supplied context identifier.

## 4. What Is ContextPayload in the Board Project?

ContextPayload is proposed terminology for the small presentation request, distinct from the existing full GroundedContext. It must not be passed to the UISpec validator in place of complete grounding.

| Field | Exact supported value/type | Role | HTTP requirement |
| --- | --- | --- | --- |
| page | String enum: landing only | Requested presentation page | Required |
| locale | String enum: en-US only | Requested supported presentation locale | Required; no default |
| Dormant fields | None defined | No unused fields invented | Reject extras |

The project does not define segment, product_interest, region, campaign, operationalLineId, shift or boardType in the current request. It would be misleading to invent enums such as Line-A/Line-B without an agreed authoritative catalogue. locale is already active and required, not a dormant default.

The full GroundedContext remains server-owned: contextVersion, contextId, page, locale, generatedAt, capabilities, defectCategories, metrics, alerts and actions. Its synthetic values are not manufacturing evidence. Quality and Manufacturing continue to own taxonomy and ratio policy.

## 5. Python ContextPayload Design

A candidate module is services/domain/request_context.py, beside the service. This keeps the domain type independent of the HTTP package; the tutorial's top-level api/context.py would not fit this repository. No second API tree should be created.

```python
# Proposed design only; not installed application code.
from dataclasses import dataclass
from enum import Enum

class Page(str, Enum):
    LANDING = "landing"

class Locale(str, Enum):
    EN_US = "en-US"

@dataclass(frozen=True)
class ContextPayload:
    page: Page
    locale: Locale

    def __post_init__(self) -> None:
        if not isinstance(self.page, Page):
            raise ValueError("Unsupported presentation request")
        if not isinstance(self.locale, Locale):
            raise ValueError("Unsupported presentation request")
```

Frozen prevents ordinary attribute reassignment; annotations alone do not enforce construction types, hence the explicit guard. This is not a security sandbox or a substitute for HTTP validation. Convert only values already accepted by the strict route model: Page(parsed.page), Locale(parsed.locale). Unknown or missing values must never become defaults.

A strict frozen Pydantic model is a viable smaller alternative if inspection justifies reusing one model instead of adding duplicate request types. Record that choice before implementation; do not introduce both abstractions unnecessarily. Keep existing Literal validation semantics, extra-field rejection and duplicate-key checks. Do not add an as_grounded_context() or generated_for helper: the presentation request is not the validator's full context.

## 6. HTTP API Contract

Retain the already-reviewed board endpoint and request, not the source's GET query API:

```text
POST /api/v1/ui/landing-page
Content-Type: application/json
{"page":"landing","locale":"en-US"}

HTTP 200:
{spec, source:"fixture", rejections:[], contextId, actions}
```

Keep the response fields exactly as agreed in Task 6. The bare UISpec used by the onboarding tutorial cannot carry our context action bindings and reviewed metadata. GET /health remains 200 {"status":"ok"}, liveness only. Do not change methods, add an alias, allow query context or introduce a request echo field.

If additional presentation values or business selectors are required, record and obtain review of the request and admission amendments before implementation. A schema-preserving transport change is still an API contract change.

## 7. FastAPI Boundary Validation

```text
Incoming POST
 -> require application/json; reject query parameters
 -> parse JSON with duplicate-key rejection
 -> strict LandingRequest: required fields, no extras
      |
      +-> invalid -> 422 {"error":"invalid_request"}
      |             service not called
      v
Construct immutable ContextPayload from validated fields
 -> domain service(request_context)
```

Preserve existing sanitization: no input echo, exception detail or path leaks. Tests must prove a rejected request cannot reach the fixture loader/service. A rejected schema value is not silently coerced. Do not replace the existing parser with a convenient framework default that loses duplicate-key rejection.

Query validation from the tutorial is intentionally not added. In this board API any nonempty query is invalid. URL encoding alone would not establish enum membership, grounding or safety anyway.

## 8. Domain Service Flow

```text
Immutable presentation request
       |
       v
Load fixed overview raw spec + complete server context once
       |
       v
Require server page == request.page.value
Require server locale == request.locale.value
       |
       v
UISpecValidator.validate(raw_spec, complete_server_context)
       |
       +-> INVALID -> existing LandingUnavailable / HTTP 500
       v
Return exact accepted spec and same-context action bindings
```

The current service already creates request-local data by reading the fixed pair. Reuse this snapshot discipline rather than adding a second fixture store or unnecessary deep-copy layer. Preserve no post-validation reread and caller/source non-mutation tests. If shared cached objects are ever proposed, that is a new ownership decision requiring review.

Do not retarget meta.generated_for: that field does not exist in v1. Do not rewrite spec.contextId or server context fields from browser input. A mismatch between a valid request and an internally inconsistent fixture is a server failure, not permission to repair the fixture. Keep existing sanitized 500 behaviour and original validator codes.

## 9. Why the Fixture Does Not Dynamically Generate UI

There is exactly one supported page/locale combination. Repeated requests yield the same overview and bindings; there is no second valid context to invent merely to imitate the tutorial's matrix.

```text
landing + en-US -> unchanged canonical overview pair
unsupported input -> reject
```

The fixed data still includes all nine component types and supplied synthetic strings/percentages. No context-driven component selection, new fixtures, personalized copy, timestamps, random IDs or ratio calculations. Existing canonical ownership stays in apps/ui/fixtures/overview.spec.json and overview.context.json.

For future multiple contexts, agree server-side catalogue ownership, complete paired contexts, mapping and browser admission first. Request values must not become arbitrary file paths or grounding facts.

## 10. Deterministic Validator Integration

The validator receives the unchanged UISpec snapshot and complete server-owned GroundedContext. It does not receive only the two-field ContextPayload. Request page/locale matching belongs to the service's association check; schema, grounding and text policy stay in the existing validator.

Retain specVersion "1.0", page "landing", contextId and ordered blocks. Selected authority remains specs/schemas/ui-spec.schema.json; the alternative copy remains preserved and unused. No generated_for, root/children, refusal or steps/current shapes are added.

The validator returns status/rejections, not a browser trust token. VALID means presentation validation. It never indicates a board passes inspection, a line meets a quality threshold or shipment is approved.

## 11. React API Client Changes

Proposed developer-facing call: fetchLandingPage(requestContext, signal). Keep the endpoint fixed and serialize only the explicit accepted page and locale into the JSON body. Do not accept an arbitrary URL, path, Response, UISpec or fetch implementation as production inputs.

```typescript
// Proposed transport type; keep existing UISpec types unchanged.
type ContextPayload = Readonly<{
  page: 'landing';
  locale: 'en-US';
}>;
```

A TypeScript type cannot validate runtime values. The loader should reject unsupported/extra request fields and snapshot the two accepted scalar values before asynchronous work, preventing caller mutation from changing the outgoing request or later association check. This is validation of the transport request, not duplicated UISpec/grounding logic.

No URLSearchParams is needed for a JSON POST. Adding query strings would violate the current contract. Continue unknown response JSON handling, exact full-envelope/spec/action equality with the independently Python-prepared overview, and private issuance from the admitted response itself. Do not issue a local fallback handle.

**Request/response association instead of assertContextEcho:** After existing full admission, compare response.spec.page to the captured request.page. contextId and action bindings must still match the prepared pair. Locale is not carried in UISpec or the response envelope; do not claim a locale echo. For the singleton en-US contract, the accepted request value and server-side context comparison establish the limited association. Multiple locales would require a separately reviewed transport/admission design, not an invented response field or a superficial guard.

Keep private issuance inside approved.ts. api/client.ts currently re-exports the fixed loader; do not move issuance into a general public approve(payload) factory just to match tutorial file names.

## 12. React Application Changes

Proposed INITIAL_CONTEXT is a developer-controlled immutable constant with page landing and locale en-US. Pass it to the fixed loader through the existing LandingApplication effect. No query-string reader, form, upload, line filter, context picker or user-generated JSON input is introduced.

```text
INITIAL_CONTEXT -> fixed API loader -> approved handle
                -> existing App -> ControlledRenderer
```

Keep the error boundary and synthetic/inert notice outside supplied content. App must not import the registry to bypass ControlledRenderer or turn response names into React elements directly. All five actions remain inert and context-bound; Hero labels and CTA labels remain unchanged.

## 13. Loading and Error Behaviour

| State | Required proposed behaviour |
| --- | --- |
| Loading | Existing visible status and synthetic notice |
| Ready | Accepted response handle through existing App/ControlledRenderer |
| Invalid local request | Controlled error, no fetch or issuance |
| HTTP/network/JSON/admission error | Controlled error, no fixture fallback |
| Unmount or stale response | Abort/ignore completion; no late update |

Preserve existing AbortController and active-request handling. Capture the request values before fetch. No retry loop, inferred context correction or stateful inspection action belongs in this increment.

## 14. Why No Silent Fallback?

A page that silently returns to static data can conceal a broken API or mismatched context. Task 6 already made these failures visible; Task 6A must retain that behaviour. Prepared fixtures are admission references and test inputs, not recovery content.

Do not turn an unsupported locale into en-US, an invalid page into landing or a mismatched response into the local overview. Observability here means a controlled visible error and testable outcome, not a new logging/telemetry platform.

## 15. Security and Control Properties

- Only the existing page/locale values enter the presentation seam.
- HTTP rejection occurs before service access; no silent default or coercion.
- Complete GroundedContext remains server-owned; browser metrics/actions/contextId reject.
- Context values remain data, never component names, paths, URLs or executable strings.
- Both schemas, validator API, UISpec types, registry and renderer remain unchanged.
- Full response admission remains mandatory; page association alone cannot issue a handle.
- No eval, Function, raw HTML, dynamic imports, prop spreading or arbitrary component lookup.
- Unknown/inherited component names still reject the entire render.
- Inert actions preserve exact labels and data without navigation or manufacturing side effects.
- Fixed timestamps/identity and non-mutation remain tested; no random/time-driven content.
- No new validator codes, authentication claims or cryptographic trust claims.

These are acceptance criteria for proposed work, not freshly verified Task 6A results. The existing Task 6 evidence does not prove a not-yet-written seam.

## 16. What Task 6A Does NOT Build

No runtime AI, Model Gateway, AiClient, Agent SDK, model SDK or AI eval execution. No new business-context enums, line/shift filters, metric source or personalization engine. No camera/edge/PLC/MES, image processing, classifier, live defect ratio, quality approval/override or human workflow. No database, persistence, authentication, uploads, onboarding, document processing, risk scoring or production infrastructure.

No GET-query replacement, generated_for retargeting, bare-UISpec response redesign, dynamic transport, second application or fixture duplication. No Task 7 implementation. No commit or push is authorized by this document.

## 17. Test Coverage to Add and Retain

Baseline evidence from Task 6: 197 Python tests and 63 UI tests passed, with one Starlette/HTTPX deprecation warning; TypeScript, safety lint, build and pip check passed. These are prior results, not a promised Task 6A test count. No Task 6A tests were run for this guide.

| Area | New or adapted assertions |
| --- | --- |
| Context construction | Exact Page/Locale members, required fields, frozen state, reject raw/unsupported values |
| Route propagation | Accepted values become the explicit service argument; rejected request never calls service |
| Domain association | Request page/locale match server context; mismatch fails without editing source |
| Full validation | Validator receives raw spec plus complete same server context before success |
| Fixture ownership | Same exact response, repeatability and unchanged canonical files/inputs |
| Client request | Fixed POST URL, exact body/headers, no query, unsupported request rejection, captured values |
| Admission | Retain full equality and private issuance; mismatched page/spec/bindings reject |
| UI | INITIAL_CONTEXT reaches client; unchanged notice/renderer path and inert actions |
| Async lifecycle | Mutation after invocation cannot alter captured request; stale completion ignored |
| Regressions | All nine components/five actions, unissued/copied handles, DOM safety and preparation cleanup |

Use isolated test mechanisms for mismatched internal fixtures and malformed responses. Do not add production switches, arbitrary paths or bypass factories. Do not duplicate old tests solely to increase counts.

## 18. Task 6A API Smoke Test Matrix

**All rows are proposed expectations; result is NOT RUN for Task 6A.**

| Request / condition | Expected status | Expected behaviour | Result |
| --- | --- | --- | --- |
| GET /health | 200 | Exact status ok, liveness only | Not run |
| POST exact landing/en-US body | 200 | Existing envelope, unchanged overview and bindings | Not run |
| Repeat same valid body | 200 | Equal deterministic content | Not run |
| POST empty object or missing page/locale | 422 | invalid_request, service not called | Not run |
| POST unsupported page | 422 | No defaulting | Not run |
| POST locale fr-FR or wrong type | 422 | No coercion/localization fallback | Not run |
| POST supplied contextId/metrics/actions/lineId | 422 | Client grounding/extra fields rejected | Not run |
| POST with query parameters | 422 | Queries remain unsupported | Not run |
| Duplicate JSON keys or malformed JSON | 422 | Existing parser protection retained | Not run |
| GET landing endpoint | 405 | method_not_allowed | Not run |
| Isolated invalid server fixture/context test | 500 | landing_unavailable; no internal detail | Not run |

There is no second valid page/locale combination in this contract. Demonstrating two different valid contexts would require an approved expansion; do not invent one for a screenshot. Revalidate successful response.spec with the complete canonical context, compare exact spec/action equality, and repeat through the Vite proxy.

## 19. Browser Smoke Test Plan

Start the backend from root using .venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8001. Start npm run dev from apps/ui and use the printed URL. Inspect current listeners first; preserve unrelated processes. Keep Windows helper windows hidden.

Confirm the real browser sends the exact POST body from INITIAL_CONTEXT and receives the existing envelope. Observe rendered DOM, external synthetic notice, exact values, context-derived Hero label, inert controls, keyboard focus and narrow/wide layouts. Only local Vite assets/HMR and the agreed Domain API traffic are expected. No query-string debug display belongs in the product UI.

Stop the task-owned backend and verify controlled error without fallback; restore only if needed and record cleanup. Use the existing check-browser.mjs setup, adapting only demonstrated gaps. Record browser/version/URL/screenshots, console and network. HTTP 200 or an HTML shell alone is not rendering evidence. Mark inaccessible browser checks unverified; no smoke results are claimed by this proposal.

## 20. Architectural Invariants to Confirm

| Review question | Required answer after implementation | Evidence to collect |
| --- | --- | --- |
| Is HTTP context new? | No; existing POST fields are now propagated | Before/after diff |
| Are accepted values unchanged? | Yes, landing and en-US only | Request negative tests |
| Does the service receive the request explicitly? | Yes | Route/service argument assertion |
| Is the request immutable? | Yes, supported scalar fields only | Construction/mutation tests |
| Does browser context become grounding? | No | Full context ownership tests |
| What does Python validate? | Exact spec plus complete server GroundedContext | Validator spy/assertion |
| Is generated_for added or retargeted? | No; absent from v1 | Schema/source diff |
| Is contextId rewritten? | No | Exact fixture equality |
| Is locale echoed by the response? | No; association is server-checked, not an echo claim | Transport review |
| Is the response envelope retained? | Yes, spec/source/rejections/contextId/actions | Exact response test |
| Can page matching alone approve data? | No, full existing admission required | Negative transport tests |
| Does private issuance remain restricted? | Yes | Copied/flagged/unissued rejection |
| Does App bypass the registry path? | No, ControlledRenderer remains the entry | Application test/source review |
| Are schema/validator/renderer unchanged? | Yes | Diff and regression checks |
| Do arbitrary request values select code/files? | No | Closed-input tests and source review |
| Is AI or a quality decision introduced? | No | Dependency/scope review |
| Are failures hidden by fixtures? | No | Backend-unavailable browser check |

These answers are target invariants, not a completed confirmation table. The final report must replace expectations with actual evidence or explicit failures.

## 21. Engineering-Time Versus Runtime Perspective

```text
ENGINEERING TIME                     RUNTIME (proposed)
Human task/review                     React INITIAL_CONTEXT
  -> coding agent                       -> JSON POST
  -> CLAUDE.md/rules/specs               -> HTTP validation
  -> tools/permissions                  -> immutable request
  -> skills/hooks when configured       -> server GroundedContext
  -> tests and evidence                 -> Python validator
  -> reviewed repository change         -> private handle
                                        -> controlled renderer

Plugins/Agent SDK in a teaching diagram do not mean
those capabilities are installed in this application.
```

The coding agent helps engineers modify the repository. It is not a deployed model serving board inspection users. This task adds no runtime agent framework and grants no new execution capability to context data.

## 22. The Future AI Insertion Point

```text
PROPOSED TASK 6A
Presentation request -> server association with fixed grounding
 -> authored spec -> validator -> fixed-response admission -> UI

FUTURE, SEPARATE DESIGN
Approved presentation request -> server-owned grounding assembly
 -> model gateway -> raw UISpec proposal
 -> same structural/grounding validation principles
 -> separately reviewed dynamic response admission
 -> private handle -> existing controlled renderer -> UI
```

The controlled-rendering principle can remain stable, but the present exact-overview browser adapter cannot accept arbitrary future valid model output. Do not promise a seamless model replacement without revisiting transport admission, context binding, semantic evaluation and failure policy. No model interface is required merely to make this diagram concrete.

## 23. Task 6A Implementation Prompt — Proposed Exact Instructions

The following is the complete proposed board prompt, ready for a future coding-agent session. It is not an “exact prompt previously used” claim. It begins with readiness, because the user must agree that Task 6A means the minimal page/locale propagation seam rather than additional manufacturing context values.

```prompt
Proceed with Task 6A readiness: explicit presentation ContextPayload seam
for Board Defect Inspection AI. Implement only once the scope below is
confirmed in the session and recorded; do not silently redesign transport.

Task 6 is implemented locally. Do not assume review, a commit or checkpoint.
This task carries the existing page/locale request explicitly through the
application and domain layers. It adds no business-context variants.
No model, gateway, Agent SDK, database, authentication, physical integration,
classification, ratio calculation, quality approval or production infrastructure.
Do NOT commit. Do NOT push. Do NOT start Task 7.

==================================================
1. INSPECT AND READ BEFORE EDITING
==================================================
Inspect branch, HEAD, git status, diff/stat, relevant new files and runtime
tooling. Preserve unrelated work. Report Git failures without repair.
Do not copy tutorial commit IDs or assume origin/main.
Read CLAUDE.md, README.md, docs/business-problem.md, docs/architecture.md,
docs/repository-structure.md, specs/spec.md, specs/model-contracts.md,
both schemas, selected notes, Task 3-6 readiness/reports and runtime READMEs.
Read services/domain/api/main.py and routes.py, landing_service.py,
validator.py, validation_models.py and text_policy.py.
Read apps/ui/src/approved.ts, api/client.ts, App.tsx, main.tsx,
types.ts, registry.ts, render.tsx, fixture pairs and preparation scripts.
Read tests/domain_api, tests/validator, tests/renderer_fixtures,
apps/ui/tests, pytest.ini, manifests/locks and evals/README.md.
Use BRD/guides for context, not new prop or request definitions.

==================================================
2. READINESS AND SMALLEST DESIGN
==================================================
Explain current behaviour: the strict POST request already has page/locale;
the route validates then discards the parsed object; the service has no
request argument; the loader internally supplies fixed values.
Propose explicit request propagation with no wire/output change.
Record decisions before implementation:
- ContextPayload means presentation request, not GroundedContext.
- Exactly page='landing' and locale='en-US', both required, no defaults.
- Retain POST JSON; queries remain rejected. No new fields or enum values.
- Retain exact Task 6 envelope, canonical pair and private admission.
- No generated_for, contextId retargeting or new response echo metadata.
- Choose one minimal immutable domain request representation.
- Page association is checkable; locale is not echoed on the wire.
List exact candidate files and why each change is needed.
If the user expects multiple lines/shifts/board types/locales, STOP and
request contract decisions. Do not invent value sets or weaken admission.
Readiness approval for Task 6 does not automatically approve new contracts.

==================================================
3. CONTEXT MODEL AND HTTP BOUNDARY
==================================================
After agreement, add only the minimal domain request type, preferably
services/domain/request_context.py; no second top-level api project.
Candidate: string enums Page.LANDING and Locale.EN_US plus a frozen
ContextPayload dataclass with required fields and runtime type checks.
A strict frozen Pydantic representation may be simpler; explain the choice.
Do not create unnecessary conversion/validation layers.
Retain strict Literal-equivalent HTTP semantics, required fields, extra
field rejection, malformed/duplicate JSON detection, media-type and query
checks. Construct the domain value only after request validation.
Reject invalid/missing input with 422 {"error":"invalid_request"}.
Prove the service is not called on rejection. No silent coercion/default.
Preserve GET /health and existing sanitized 404/405/500 contracts.
Do not change POST /api/v1/ui/landing-page to GET or add aliases.

==================================================
4. DOMAIN SERVICE AND VALIDATION
==================================================
Make get_landing_ui_spec receive the immutable request explicitly.
Keep sole canonical apps/ui/fixtures/overview.spec.json and its complete
overview.context.json. Preserve snapshot/no-reread/non-mutation behaviour.
Compare request page and locale to the server-owned context values.
Mismatch is an internal failure; never overwrite fixture/context fields.
Pass the exact raw spec snapshot and COMPLETE server context to existing
UISpecValidator.validate. Require status VALID before success.
Never pass only ContextPayload to that validator.
Return unchanged spec, source='fixture', rejections=[], contextId and
ordered context actions. No generated_for or new response fields.
Keep original validator API/codes, both schemas and UISpec types unchanged.
No new fixture copy, arbitrary path input, repository framework or cache.
No repair, inference, model call or silent substitution.

==================================================
5. REACT REQUEST AND APPROVED HANDLE
==================================================
Introduce a small readonly transport request type separate from UISpec.
Pass a developer-owned INITIAL_CONTEXT {page:'landing',locale:'en-US'}
to fetchLandingPage(requestContext, signal) in the existing app effect.
No form, URL/query input, upload, selector, filter or debug UI.
Reject unsupported/extra runtime request fields; TypeScript alone is not
validation. Snapshot accepted scalar values before asynchronous work.
Keep fixed relative POST URL, explicit JSON fields and existing headers,
credentials/redirect/cache rules and AbortSignal handling.
No URLSearchParams for this JSON POST; do not add query transport.
Keep response JSON unknown until complete exact-overview admission.
Retain independent Python preparation gates and verification evidence.
After full admission, associate response.spec.page with captured request.page.
Preserve contextId/binding equality checks through full admission.
Do not claim locale echo: it is not a response field. Keep server locale
association and the singleton supported locale; stop if expansion is needed.
Only private issuance may create a handle from the actual admitted response.
Do not export approve(raw), accept arbitrary URLs/Responses or return a
local fixture handle after failure. Echo matching alone never approves data.
App ready state still uses existing App/ControlledRenderer with inert callback.
No direct registry bypass, API-driven React creation or changed component props.

==================================================
6. ERRORS, DETERMINISM AND SECURITY
==================================================
Preserve loading, success, HTTP/network/JSON/admission error states,
external synthetic notice, render error boundary and cancellation/stale guards.
No retries or silent fallback. No input mutation or time/random fields.
Retain all nine components and five context-bound inert actions.
No eval, Function, dangerouslySetInnerHTML, arbitrary DOM prop spreading,
dynamic imports, executable strings or component/module/path lookup from data.
Unknown/inherited components reject the whole page without skip or repair.
VALID means presentation only, never board approval or classification.
Quality and Manufacturing own defect/ratio policy; no figures are inferred.

==================================================
7. DETERMINISTIC TESTS
==================================================
Inspect coverage and add only meaningful missing tests.
Python: context construction/immutability; valid route argument propagation;
invalid/missing/extra/query/duplicate/wrong-type input rejects before service;
request-to-server page/locale association; complete context at validator;
validation-before-success; unchanged exact response; mismatched/invalid server
fixture failure; repeatability/non-mutation and no outbound model/domain calls.
Use isolated tests for invalid fixture injection, never a production switch.
React: initial request reaches client, exact fixed POST/body, runtime invalid
request rejection, no query/path injection, snapshot unaffected by later caller
mutation, full response admission and page association, all error states,
private issuance, controlled renderer use, inert actions and stale completion.
Retain registry/DOM safety, copied/unissued handle and fixture-cleanup coverage.
There is only one valid request combination; do not invent a second for tests.
Do not chase tutorial counts. Verify actual pytest discovery if files change.

==================================================
8. DEPENDENCIES AND DOCUMENTATION
==================================================
Reuse installed FastAPI/Pydantic, standard-library dataclasses/Enum and
existing React tooling. No new dependency expected; justify any real need.
Retain locks and existing preparation gates; never manually edit generated
fixtures.ts. Do not suppress the existing Starlette/HTTPX warning silently.
Update relevant runtime READMEs and tests/README.md only for actual changes.
Record readiness and implementation evidence in specs/TASK-6A-READINESS.md
and specs/TASK-6A-IMPLEMENTATION-REPORT.md as appropriate to work performed.
Use a small explicit architecture update if needed; no historical guide rewrite.
Do not assume docs/walkthrough.md exists. Do not change model-contracts.md,
schemas, grounding API or renderer to accommodate this seam.

==================================================
9. VERIFICATION AND BROWSER
==================================================
From root run:
.venv/Scripts/python.exe -m pytest --collect-only -q
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check
From apps/ui run npm test, npm run typecheck, npm run lint, npm run build.
Report JSON parsing, Draft 2020-12 meta-validation, instance validation and
full runtime checks separately. Alternative-schema meta-validation is not
part of the current suite; do not claim it ran.
Baseline 197 Python/63 UI results are historical, not new test results.
Start actual backend and npm run dev using documented commands/printed URLs.
Verify exact health, landing success, rejected requests and Vite proxy.
Revalidate live response.spec with full canonical context and compare exact
spec/action values. Observe real browser POST body, rendered page, notice,
focus, inert actions, wide/narrow layout, console and allowed local traffic.
Stop the task-owned backend and verify visible error with no fallback.
Use existing browser-check script where possible; record screenshots/browser
and mark unavailable checks unverified. A shell HTTP 200 is insufficient.
Preserve unrelated listeners; stop only task-owned processes afterward.

==================================================
10. REVIEW AND FINAL REPORT
==================================================
Review git status, git diff --stat, git diff, git diff --check and new files.
Separate prior work, Task 6A changes and ignored generated artifacts.
No cleaning/stashing/repairing unrelated work. Report exact Git failures.
Do NOT commit. Do NOT push. Do NOT start Task 7.
Report:
1. Created/modified files and agreed readiness decisions.
2. Exact request type/values, immutability and unchanged API contract.
3. HTTP rejection and explicit service propagation.
4. Server GroundedContext ownership and validator integration.
5. Unchanged fixture/output and no generated_for/identity retargeting.
6. Client snapshot, full admission, association limits and private issuance.
7. App states, stale handling, inert actions and no fallback.
8. New tests, actual collection and all fresh results/warnings.
9. Schema/typecheck/lint/build/pip checks, API/browser evidence and URLs.
10. Dependencies/docs changed and preserved control boundaries.
11. Answers to the architectural invariant questions in this guide.
12. Excluded scope, incomplete checks, Git state and next smallest review step.
If readiness is blocked, report decisions needed without implementation claims.
STOP after the report and wait for human review.
```

## 24. Human Review Checklist Before Checkpoint

- Confirm Task 6 review/checkpoint state rather than assuming completion from the tutorial.
- Confirm the agreed increment is page/locale propagation, not a hidden business-context expansion.
- Compare wire contracts, canonical files, schemas, validator and renderer against the pre-task snapshot.
- Verify request data is explicit, immutable and never promoted to grounding.
- Review the absence of generated_for retargeting and the honest locale-association limitation.
- Confirm full private admission, no raw renderer input and no static fallback.
- Inspect actual tests/smoke evidence and the invariant matrix; distinguish expected from executed results.
- Preserve source fixtures and intentional evidence; keep build/cache/generated artifacts ignored.
- Separate prior untracked work from the increment before discussing a commit.
- Confirm no commit, push or Task 7 occurred during the implementation task.

## 25. Recommended Checkpoint

After implementation, verification and human review, a separately authorized checkpoint may use the proposed message: Task 6A: Propagate explicit presentation request context. That message describes the minimal board increment more accurately than claiming new query context or business variants.

No hash or push destination is promised. Inspect the actual branch and remote at checkpoint time; do not copy origin/main. Earlier untracked dependencies and unrelated work require an explicit staging plan. Do not manufacture a clean working tree by deleting or absorbing unrelated files.

## 26. What Comes Next

First agree whether this minimal explicit-request seam provides the intended learning value. If the real goal is context-varying board dashboards, the next work is a contract/readiness discussion covering fields, authoritative values, complete server grounding and response admission — not immediate coding of invented enums.

After a reviewed Task 6A, choose one separately scoped increment. An AI interface or generalized transport may be considered, but neither is automatically authorized. The present exact-fixture adapter cannot simply be replaced with a model response without new trust decisions.

## 27. Final Beginner Mental Model

```text
Task 6:  We built a controlled local API route.
Task 6A: We propose carrying its existing request explicitly
         through each layer, with no new business facts.
Future:  A model may propose presentation behind reviewed gates.

Request intent != server grounding
Server validation != browser approval flag
Context association != complete response admission
Presentation VALID != manufacturing approval
```

The useful enterprise lesson is traceable intent with stable boundaries. This proposed seam makes responsibility visible without pretending that typed request data, an echo guard or a developer-authored fixture is sufficient validation. The guide and prompt are documentation only; no Task 6A code, fresh application tests, commit or push were performed.
