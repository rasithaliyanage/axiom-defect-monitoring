# Board Defect Inspection AI — Task 6
@ Domain Runtime / FastAPI Boundary — Beginner-Friendly Enterprise Guide

Status: proposed implementation guide; documentation only. Task 6 has not been implemented or verified. Task 5 has local implementation and browser evidence, but human approval, commit and checkpoint status must be inspected rather than assumed.

Source adapted: Customer_Onboarding_Task_6_Beginner_Guide_Enterprise_Grade.docx.pdf. This guide preserves its 25-section teaching structure and divider-based prompt while replacing onboarding assumptions with the board project's actual paths, v1 contract and approved-input boundary.

## 1. Where Task 6 Fits

Manufacturing stakeholders ultimately need inspection records and trustworthy defect reporting by operational line. Images, defect definitions and ratio policies belong to the relevant domain systems and Quality/Manufacturing owners. Task 6 would prove a small HTTP boundary using synthetic records; it would not inspect images, classify boards or calculate a defect ratio.

Tasks 3–5 already provide Python validation, controlled React rendering, paired synthetic fixtures and a browser-runnable Vite application. The proposed next increment is a Domain Runtime API with no model integration.

## 2. Task 6 Objective

Serve a fixed developer-authored landing UISpec only after the existing Python validator accepts it against a complete matching synthetic GroundedContext. React would consume the agreed API response through a reviewed transport adapter and pass a privately issued handle to the existing renderer.

Before implementation, resolve the endpoint/request/response contract and the transition from static fixture issuance to runtime response issuance. Those decisions are prerequisites, not implementation details that can be guessed.

## 3. The Core Architectural Rule

Current, implemented flow:

```text
Fixed UISpec + synthetic GroundedContext
  -> Python validation during preparation
  -> generated catalogue and verification evidence
  -> privately issued ApprovedUISpec handle
  -> ControlledRenderer -> explicit registry -> React -> browser
```

Proposed Task 6 flow, pending transport review:

```text
React request -> Domain API -> fixed server-owned spec/context snapshot
  -> existing Python validator
  -> agreed response containing the validated presentation and required bindings
  -> reviewed client transport adapter -> private ApprovedUISpec issuance
  -> ControlledRenderer -> registry -> browser
```

A Python object or WeakMap handle cannot be serialized into a browser trust token. HTTP 200, a cast, a brand, an outer shape check or approved=true is not proof of validation. The server validation path and restricted client issuance path must be reviewed together. VALID refers only to presentation validation, never a board quality decision.

## 4. What Is the Domain Service?

A small service would obtain the fixed spec and context, create an isolated request snapshot, invoke UISpecValidator.validate(spec, context), reject an INVALID result and return the exact validated snapshot with the bindings required by the agreed transport contract. Routes handle HTTP; the service handles orchestration; the existing validator owns schema, grounding and deterministic policy.

The validator currently returns status/rejections, not an approved payload. Preserve that API. Do not claim validate() returns an ApprovedUISpec or introduce a new validator rejection code for HTTP failures.

## 5. FastAPI Structure

The following is a candidate layout, not created files or a mandatory new framework:

```text
services/domain/
  validator.py                  existing
  validation_models.py          existing
  text_policy.py                existing
  api/
    main.py                     proposed FastAPI construction
    routes.py                   proposed health and landing routes
    errors.py                   only if a separate module is justified
  landing_service.py            proposed fixed-fixture orchestration
apps/ui/
  src/App.tsx                   existing notice and renderer boundary
  src/main.tsx                  existing browser entry
  src/approved.ts               existing private issuance; integration review required
  src/api/client.ts             proposed transport client
  fixtures/                     existing paired synthetic sources
  scripts/                      existing preparation and verification gates
tests/domain_api/               proposed API/service checks
```

Use __init__.py only where package/import conventions require it. Do not scaffold a second top-level api/, frontend/, backend/ or ui/ project. Fixture ownership/location must be decided before moving files; no duplicate mutable sources of truth.

## 6. API Contract and Readiness Decisions

| Decision | Current evidence | Required resolution |
| --- | --- | --- |
| Endpoint and method | Board architecture/specification proposes POST /api/v1/ui/landing-page; onboarding uses GET /api/onboarding/ui | Retain the board route direction unless explicitly amended; define the exact presentation-only request before coding |
| Success body | Board architecture describes source/rejection metadata; tutorial prefers bare UISpec | Agree the minimal transport envelope and source semantics; do not invent new fields silently |
| Hero action labels | UISpec has an action ID but no label; current renderer reads matching context bindings | Specify server-owned bindings and their association with the validated context; never invent labels, URLs or destinations |
| Approved-input issuance | approved.ts only issues fixed generated catalogue handles | Review a restricted runtime transport adapter; never expose a general approve(rawJSON) factory |
| Errors | Validator returns status/rejections; no HTTP error contract is implemented | Agree HTTP status and sanitized error body separately from validator codes |
| Fixture location | Five retained spec/context pairs are under apps/ui/fixtures | Select a single canonical source and a safe local packaging/loading strategy; retain preparation and regression coverage |

GET /health returning a small fixed status is a proposal for liveness only. It must not imply manufacturing availability or quality readiness. No endpoint in this section is claimed to exist.

## 7. Developer-Authored UISpec Fixture

Prefer the existing overview pair for the integrated page and minimal pair for focused tests. Keep specVersion "1.0", page "landing", contextId and ordered blocks. Preserve complete context fields: contextVersion, contextId, page, locale, generatedAt, capabilities, defectCategories, metrics, alerts and actions.

Overview retains synthetic values such as 0012.50 images and 37.125 percent. These are deliberately supplied values, not real line performance. Hero and InfoPanel contain no child components; FeatureGrid contains 2..6 FeatureCard props objects; ProgressIndicator uses metricId, label and numeric value. Alert has no refusal variant.

## 8. Validator Integration

Use services/domain/validator.py and the selected specs/schemas/ui-spec.schema.json without duplicating their rules. Validate the same snapshot that is serialized. Never validate one object and return a different or subsequently mutated object.

Both schemas remain distinct. The selected schema allows context/reference limits of 256 and InfoPanel value/unit limits of 256/32; the alternative uses 128/64/40/12 and different identifier constraints. Hero action and Alert category constraints also differ. Preserve the selected keyword bounds and documented interpretation of its conflicting value description.

Reject malformed or ungrounded fixtures deterministically. Do not repair, skip, relabel, substitute or call a model. Keep internal diagnostics distinct from the agreed sanitized HTTP failure response.

## 9. Why the Fixture Is Copied

An isolated snapshot prevents a response caller or one request from mutating the shared source for another request. Copy the spec and its complete context consistently; derive action bindings from that same context. Test returned-object mutation, repeated requests, unchanged source files and identical supplied values. Copying is isolation, not validation.

## 10. Testable Fixture Access

The source tutorial describes a previous import-reference bug; that is not a board-project incident. For this project, use a small explicit fixture provider or call-time module reference if needed for tests. Substitute it only inside isolated tests to exercise rejection. Do not ship an arbitrary file-path parameter, upload endpoint or invalid-fixture switch.

## 11. React API Integration

Keep the nine-entry registry and ControlledRenderer unchanged unless the reviewed boundary requires a narrowly justified integration change. The API client treats decoded JSON as unknown and checks the agreed transport shape. It does not reimplement schema, metric matching or text policy in TypeScript.

The reviewed adapter must obtain data only through the intended server-owned response path and preserve context/action binding before private issuance. Document the trust assumptions and test that raw objects, copied handles and approval flags still cannot reach the renderer. Do not weaken issuance simply to make fetch response types compile.

Keep the offline catalogue for existing deterministic tests. An API error must not silently fall back to the static Task 5 page. Changing the browser's runtime source does not authorize deleting fixtures or removing preparation gates.

## 12. Loading, Success and Error States

A proposed API-backed wrapper would show developer-owned loading text, render only after successful transport handling, and show a controlled error for network failure, non-success HTTP status, invalid JSON or unusable response. Preserve the rendering error boundary and synthetic/inert notice outside supplied content. Cancel or ignore obsolete responses when the component unmounts. Do not add polling, retries or fallback orchestration.

The five action IDs remain context-bound and inert: view-inspection-queue, view-defect-reports, view-ingest-activity, open-documentation and contact-support. Hero labels come from matching context bindings; CTA preserves its supplied label.

## 13. Local Development Boundary

Choose one minimal local connection strategy during readiness: preferably a relative API request through a narrowly scoped Vite development proxy, or explicitly allowed development origins if direct cross-origin requests are required. A same-origin proxy does not require browser-facing CORS merely because the backend listens on another port.

Use the actual printed Vite URL. A proposed backend port is a local convention, not infrastructure. If CORS is needed, allow only the agreed origins/methods/headers, no wildcard or credentials by default. Do not copy the tutorial's GET-only policy onto the board's proposed POST route. Do not claim npm run preview exists; inspect package.json. Local-development configuration is not production security.

## 14. Security and Control Boundary

No eval(), Function(), dangerouslySetInnerHTML, model/API-driven imports, arbitrary component lookup, raw HTML or model-prop spreading. Unsupported components reject the entire render. Keep the current safety lint probes and runtime tests. Fixed developer-authored browser test expressions are tooling, never model input or application execution paths.

The browser must not supply grounding truth, fixture filenames or component definitions to the service. Presentation selectors are distinct from server-owned GroundedContext. No claim of cryptographic transport authentication follows from hashes or private JavaScript handles.

## 15. Why There Is Still No AI Runtime

FastAPI would be the Domain Runtime, not the AI Runtime. The task would establish a deterministic HTTP boundary using fixed synthetic input. Model gateway, prompts, model credentials, repair and model evaluation execution remain future, separately authorized work. The product's broader manufacturing goals do not expand this increment.

## 16. Testing Strategy

Backend checks should cover agreed health and landing responses, exact fixture/context association, runtime validation before success, invalid fixture rejection, sanitized failure, non-mutation, repeatability, unsupported request inputs and absence of model/domain-data calls. Test the wire payload against the selected schema and existing validator using the matching context.

UI checks should cover loading/success/error, invalid JSON and response shape, binding/context mismatch, rejected unissued inputs, successful controlled rendering, no stale-response update, inert actions and no silent static fallback. Keep all existing registry, DOM safety, exact-metric, determinism and Python preparation tests.

Root pytest.ini currently discovers only tests/validator and tests/renderer_fixtures. If tests/domain_api is added, explicitly include it in test discovery and verify collection. Do not claim new API tests ran merely because root pytest passed.

## 17. Task 6 Verification Status

| Check | Task 6 status |
| --- | --- |
| Readiness and transport contract agreement | Pending human review |
| FastAPI/service implementation | Not implemented |
| API/client integration tests | Not executed |
| API/browser success and failure checks | Not executed |
| Task 6 dependency compatibility and build | Not executed |

Task 5's report records 33 UI tests, 167 Python tests, typecheck/lint/build and headless Chrome checks. Those are historical Task 5 results, not Task 6 results or target counts. No onboarding success numbers or commit identifiers apply to this project.

## 18. Dependencies

No project dependency is added by this document. At future implementation time inspect the actual Python/Node runtimes, installed versions and lockfiles. Select compatible FastAPI, a minimal development server and HTTP test support only if needed. Record resolved versions then; do not copy the tutorial's old lower bounds or install optional server extras by default. Reuse React tooling and preserve existing requirement pins unless a demonstrated compatibility change is approved and verified.

## 19. What Task 6 Does Not Build

No model gateway or runtime AI, database/persistence, authentication subsystem, camera/edge/PLC/MES integration, image upload/processing, automated classifier, defect-ratio calculation, quality verdict, human approval/override, onboarding/registration/risk scoring, charts/filters, production infrastructure, retry/repair or fallback orchestration. No UISpec vocabulary or schema redesign.

## 20. Adapted Task 6 Implementation Prompt

This is a proposed future prompt. It retains the source's opening and divider-based organization, but adds the readiness gate required by the actual board implementation. It is not an executed instruction or a completion record.

```prompt
Proceed with Task 6: implement the Domain Runtime / FastAPI Boundary.

This is the next smallest implementation increment for the
Board Defect Inspection AI application.

IMPORTANT:
Begin with readiness. Implement only after the required transport
decisions below are resolved and recorded.

Task 5 has local implementation and browser verification evidence.
Inspect review, branch, HEAD and working tree; do not assume approval,
a commit or a checkpoint. Preserve unrelated changes and report Git
failures without repairing the repository.

The current architecture contains:
- Business problem and system specification
- v1 model contract and selected JSON Schema
- Deterministic Python UISpec validator
- Controlled React component registry and renderer
- Minimal runnable React UI and browser-runnable Vite application
- Paired developer-authored synthetic UISpec/context fixtures
- Python preparation gates and retained verification evidence
- Privately issued ApprovedUISpec handles
- Deterministic renderer, application and validator tests

Reuse apps/ui/, services/domain/ and the v1 contract.
Task 6 must establish the first runtime/API boundary only after readiness.

Do NOT start Task 7.
Do NOT implement a model gateway or call an AI/model API.
Do NOT implement runtime AI generation.
Do NOT introduce authentication, a database or persistence.
Do NOT introduce camera/edge/PLC/MES integration or image processing.
Do NOT introduce defect classification or defect-ratio calculation.
Do NOT introduce quality decisions or human approval/override workflows.
Do NOT introduce onboarding, registration, uploads, document processing
or risk scoring.
Do NOT introduce production infrastructure.
Do NOT redesign the UISpec model contract or controlled renderer.
Do NOT duplicate Python schema or grounding validation in TypeScript.

==================================================
ARCHITECTURAL OBJECTIVE
==================================================
Establish a small HTTP boundary for the existing synthetic landing page.
The Domain Runtime must validate a fixed UISpec with its complete
server-owned GroundedContext before any success response.
A reviewed transport adapter must preserve the approved-input boundary:
server validation -> agreed response/bindings -> private handle issuance
-> ControlledRenderer -> explicit registry -> React -> browser.
A cast, brand, approved=true, HTTP 200 or outer shape check is not validation.
VALID never means a board passes inspection or is approved.

Move from the existing prepared static catalogue -> approved handle ->
renderer -> browser to React -> API client -> agreed board endpoint ->
FastAPI -> fixed spec/context -> Python validator -> reviewed response
and bindings -> private handle -> ControlledRenderer -> browser.
The service must return the developer-authored presentation only after
validation. There must still be NO AI/model call.

==================================================
BEFORE IMPLEMENTATION
==================================================
Read CLAUDE.md, README.md, docs/business-problem.md, docs/architecture.md,
docs/repository-structure.md, specs/spec.md, specs/model-contracts.md,
both UISpec schemas, selected schema notes and Task 3–5 reports.
Read apps/ui/ source, scripts, fixtures, tests and README; services/domain/
validator, validation_models, text_policy and README; tests/README.md,
tests/validator/, tests/renderer_fixtures/, pytest.ini and evals/README.md.
Consult the BRD and board guides as context, not new contract definitions.

Before writing files, explain:
1. The smallest FastAPI application structure and proposed file changes.
2. Where the domain service will live.
3. The canonical UISpec fixture and complete matching context location.
4. How the existing Python validator will be reused.
5. The exact request, success response and error transport contract.
6. How React will consume the API and privately issue approved handles.
7. How ControlledRenderer remains the only component rendering path.
8. What is intentionally not being implemented.

Do not proceed until this design and the decisions below are resolved.
Resolve and record these required decisions:
1. Board POST /api/v1/ui/landing-page versus the tutorial GET route;
   define the exact presentation-only request and reject supplied grounding.
2. Exact success/error transport contract and metadata semantics.
3. Matching context action bindings for Hero labels and dispatch.
4. Restricted runtime response adapter and private handle issuance.
5. Canonical fixture ownership without unreviewed moves or duplicate sources.
6. Minimal proxy/CORS strategy and local request method/origin policy.
If a required decision remains unresolved, report blockers and STOP.
Do not silently invent a response API or weaken the existing handle boundary.

Explicitly review actual Task 1-5 artifacts before writing files.
The reference list above includes these concrete implementation files:
- apps/ui/src/types.ts, registry.ts, render.tsx, approved.ts, components.tsx
- apps/ui/src/App.tsx, main.tsx, style.css and apps/ui/index.html
- apps/ui/package.json, package-lock.json, vite.config.ts and README.md
- apps/ui/fixtures/ spec/context pairs and verification.json
- apps/ui/scripts/prepare_fixtures.py, prepare.mjs and verification scripts
- services/domain/validator.py, validation_models.py and text_policy.py
- requirements.txt and requirements-dev.txt
Do not substitute historical implementation claims for inspection.

==================================================
FASTAPI APPLICATION
==================================================
After readiness, create only the minimal application under services/domain/.
Keep HTTP routing separate from fixed-fixture orchestration and validation.
Reuse existing import conventions; no second top-level API or UI project.

A candidate layout, subject to the readiness decisions, is:
services/domain/
  validator.py                  existing authoritative validator
  validation_models.py          existing context/result types
  text_policy.py                existing deterministic policy
  api/
    __init__.py
    main.py                     FastAPI construction and router wiring
    routes.py                   health and landing HTTP concerns
  landing_service.py            fixture/validation orchestration
apps/ui/src/api/client.ts       proposed restricted HTTP client

Adjust the layout if the existing repository supports a simpler design.
Record the canonical fixture location before adding or moving files.
Do not over-engineer or introduce empty layers.

==================================================
HEALTH ENDPOINT
==================================================
Agree GET /health with a small deterministic liveness response.
Do not disclose environment secrets or imply inspection/quality readiness.

After agreement, implement GET /health returning HTTP 200 and a small
fixed body, proposed as { "status": "ok" }. Test the agreed body exactly.
This indicates process liveness only, not manufacturing readiness.

==================================================
BOARD LANDING UI ENDPOINT
==================================================
Use the reviewed board endpoint/method/request, not /api/onboarding/ui.
Keep specVersion "1.0", page "landing", contextId and ordered blocks.
Use specs/schemas/ui-spec.schema.json; preserve the unused alternative.
No root/children, generated_for, refusal or reference-only progress shapes.

The agreed endpoint must return HTTP 200 for a valid supported request,
containing the validated UISpec in the reviewed transport format.
Use specs/model-contracts.md together with the selected schema as the
existing authorities. Do not invent a new UI contract.

==================================================
DOMAIN SERVICE
==================================================
Obtain a fixed spec and complete context; snapshot them consistently.
Reuse overview/minimal fixtures where appropriate. Keep synthetic labels,
values, units, IDs, locale and timestamps unchanged. No domain-data access.
Derive action bindings only from the same server-owned context.
Keep the service small; do not add a repository or orchestration framework.

Keep orchestration out of the HTTP route. Create a small landing service:
route -> service -> spec/context snapshot -> Python validator -> exact
validated presentation and agreed bindings.
Do not add repositories, dependency-injection frameworks, databases or
other abstractions without a demonstrated need.

==================================================
PYTHON VALIDATION BOUNDARY
==================================================
Reuse UISpecValidator.validate(spec, context) without changing its API.
It returns status/rejections, not an approved payload.
Validate the exact snapshot to be returned; never return an INVALID spec.
Do not repair, substitute, omit or invoke a model. Keep original rejection
codes and separate sanitized HTTP errors from validation diagnostics.
Retain existing offline fixture preparation, cleanup and evidence checks.

Before any success response:
1. Validate JSON-schema structure through the existing Python validator.
2. Validate existing grounding, runtime/cross-field and policy rules.
3. Require status VALID for the complete matching spec/context snapshot.
4. Return that exact validated snapshot in the agreed transport format.
An invalid fixture must fail deterministically, not be silently modified.

==================================================
API CONTRACT
==================================================
Implement only the reviewed transport contract. The source tutorial's
bare UISpec cannot by itself supply our context action bindings or handle.
Do not add arbitrary envelopes, approval flags or authentication claims.
Retain exact values and context identity through serialization and issuance.

Preserve the source's minimal-response principle: use the smallest
response that satisfies the reviewed board contract. Do not add generic
{ "data": ... } or { "ui": ... } wrappers without a recorded reason.
The board's metadata and action-binding needs require an explicit decision;
they do not authorize arbitrary new fields or changes to the UISpec.

==================================================
CORS / LOCAL DEVELOPMENT
==================================================
Use the agreed minimal proxy or explicit local-origin configuration.
Do not add unnecessary CORS for a same-origin development proxy.
If direct CORS is required, test allowed and disallowed origins and the
actual method/headers. No wildcard origins or production configuration.
Record actual URLs and ports; do not assume a preview script exists.

==================================================
REACT INTEGRATION
==================================================
Reuse App, main, existing error boundary, CSS and ControlledRenderer.
Treat response JSON as unknown until the reviewed transport adapter accepts
it; do not pass it to the renderer or cast it into ApprovedUISpec.
Keep private issuance restricted and covered by negative tests.
No direct registry use from the app, generated components or dynamic imports.
Preserve all nine components, five approved actions and context Hero labels.
Keep actions inert and the synthetic notice outside supplied content.

After readiness, replace the browser's direct static-fixture runtime
source with the agreed Domain API. Retain static fixtures for tests.
A static page alone does not demonstrate the new runtime boundary.
Keep the renderer unchanged unless a genuine integration issue requires
a minimal, explained and reviewed change.

The application must NOT:
- Import the Python validator into the browser.
- Import the registry to bypass ControlledRenderer.
- Create React elements directly from API component names.
- Interpret API data as executable code or raw HTML.
- Dynamically import components from API/model data.
- Use eval(), Function() or arbitrary DOM props.

==================================================
CLIENT-SIDE RESPONSE HANDLING
==================================================
Handle loading, successful transport, HTTP/network failure, invalid JSON
and unexpected response shape. Validate transport metadata only as agreed;
do not recreate schema, grounding or text-policy validation in TypeScript.
Ignore/cancel stale requests. On failure show a controlled developer-owned
error; never silently return to the Task 5 fixture. Retain fixtures for tests.

The minimum client states/checks are:
1. Loading.
2. Successful response.
3. HTTP/API and network failure.
4. Invalid JSON or unexpected/unusable response shape.
A failed runtime dependency must remain visible as an application error,
not be hidden by reverting to hard-coded content.

==================================================
UI BEHAVIOUR
==================================================
Keep the existing landing presentation and exact ordered content.
Add only necessary loading/error states. No charts, workflows or new props.
Unknown components reject the whole render; no skip, repair or substitution.

Demonstrate loading -> successful API response -> rendered UI, and
API failure -> controlled error message. Do not build a full design system,
redesign the board landing page or add other product functionality.

==================================================
TESTING
==================================================
Add deterministic FastAPI/domain tests. At minimum test:
1. GET /health returns HTTP 200.
2. Health returns the exact agreed deterministic status body.
3. The agreed board landing endpoint returns HTTP 200 for a valid request.
4. Its UISpec has specVersion "1.0", page "landing" and matching contextId.
5. The returned spec passes the existing Python validator with its context.
6. The successful response contains the exact developer-authored fixture.
7. An invalid fixture cannot be returned as an approved success response.
8. Service and returned-object mutation leave the source spec/context intact.
9. The same supported request produces the same response.
10. No AI/model/external-domain call is made; the intended local API is allowed.

Add React tests for:
11. Loading state.
12. Successful API response.
13. HTTP/API/network failure state.
14. The accepted response reaches ControlledRenderer through private issuance.
15. The application does not bypass the controlled renderer.

Also cover the board-specific boundaries:
- Validation-before-success and exact context/action-binding association.
- Rejected supplied grounding and unsupported request fields/values.
- Sanitized failures without leaked internal exception details.
- Invalid JSON/shape, mismatched bindings and unissued/copied/flagged objects.
- Inert actions, stale-response handling and no silent static fallback.
Preserve registry, DOM safety, determinism and fixture-cleanup regressions.
Update pytest.ini if a new test directory is added; verify actual collection.
No production invalid-fixture switches or arbitrary path inputs.
Keep tests small, readable and beginner-friendly.

==================================================
DEPENDENCIES
==================================================
Inspect installed runtimes, pins and locks first. Add only compatible
FastAPI/server/test dependencies justified by the implementation.
Record selected versions; do not copy tutorial pins. Reuse React tooling.
No AI SDK, ORM, authentication, cloud SDK, broker or agent framework.

Do not add database frameworks, model SDKs, LangChain or document-processing
libraries. Add the minimal development server and HTTP test support only
when needed. Reuse installed tooling and retain locks; ignore build outputs.

==================================================
SECURITY / CONTROL REQUIREMENTS
==================================================
No eval(), Function(), dangerouslySetInnerHTML, model-prop spreading,
API-driven component resolution, executable strings or arbitrary URLs.
The browser cannot provide grounding truth. Keep schema and grounding
in Python. Preserve safety lint and fail-closed registry checks.
No new validator rejection codes or changed UISpec types to suit HTTP.

The API must not become an arbitrary component execution mechanism.
Do not execute JavaScript, shell commands, HTML or JavaScript URLs from
API/model data. Preserve the future model -> contract/schema -> Python
validation -> reviewed transport -> controlled-renderer boundary without
implementing the model path in this task.

==================================================
IMPORTANT ARCHITECTURAL DISTINCTION
==================================================
FastAPI is Domain Runtime. React is UI Runtime. AI Runtime remains absent.
Quality and Manufacturing own taxonomy and ratio policy. Do not calculate
or infer production figures, classify boards or make quality decisions.

UI Runtime: React, TypeScript and ControlledRenderer.
Domain Runtime: FastAPI, Python, application/API orchestration and validation.
AI Runtime: future model gateway and UI generation model; NOT implemented.
Do not describe the FastAPI service as the AI Runtime.

==================================================
DOCUMENTATION
==================================================
Record actual decisions, file changes, installation/run commands and limits
in relevant READMEs and specs/TASK-6-IMPLEMENTATION-REPORT.md.
Separate proposed architecture, existing Task 5 assets and implemented work.
Any necessary API contract amendment must be explicit and reviewed first;
do not redesign UISpec or silently rewrite normative documentation.
Do not assume docs/walkthrough.md exists or rewrite historical tutorials.

Update apps/ui/README.md and services/domain/README.md for changed behaviour.
Update root README.md and tests/README.md where commands/discovery change.
Make only a small, explicit architecture update where required to distinguish
implemented Domain Runtime behaviour from future model topology.
Document:
- How to install selected FastAPI/server/test dependencies.
- How to start the backend and React development server.
- Actual local ports, URLs and proxy/CORS configuration.
- GET /health and the agreed landing method/request/response/errors.
- Runtime flow including validation, bindings and handle issuance.
- That the API supplies a developer-authored synthetic UISpec.
- That AI/model integration is intentionally absent.
Do not update a walkthrough unless separately required.

==================================================
VERIFICATION
==================================================
After implementation, perform and record each check:
1. FastAPI/domain tests, with actual discovery confirmed.
2. React application/client tests.
3. Existing Task 4 renderer tests and Task 5 application regressions.
4. Existing Task 3 validator and fixture-preparation tests.
5. Task 2 schema checks actually executed by the current suite.
6. TypeScript, safety lint and React production build.
7. Start FastAPI locally with the documented command.
8. Verify GET /health, HTTP status and exact response body.
9. Verify the agreed landing endpoint, response and Python validation.
10. Start the existing React/Vite development server.
11. Verify in a real browser that page data comes from FastAPI.
12. Verify backend-unavailable behaviour without static fallback.
13. Review git status, git diff --stat, git diff and all new files.

From apps/ui run npm test, npm run typecheck, npm run lint, npm run build.
From root run .venv/Scripts/python.exe -m pytest -q and
.venv/Scripts/python.exe -m pip check. Confirm new API tests are collected.
Distinguish schema JSON parsing, Draft 2020-12 meta-validation, instance
validation and full runtime validation. Record exact commands/results.
Start the actual backend and npm run dev; use printed local URLs.
Verify health, agreed landing response, proxy/CORS as applicable, real
React rendering, visible synthetic notice, keyboard focus, inert actions,
wide/narrow layouts, console/network and backend-unavailable behaviour.
Record browser/screenshots or explicitly mark unavailable checks unverified.
HTTP 200 or an HTML shell alone is not browser rendering evidence.
Update the Task 5 browser-check network expectations only for the agreed
local Domain API; continue rejecting unexpected external/model traffic.

Confirm explicitly in the final report:
- No AI/model integration or model gateway.
- No authentication, database, document processing or risk functionality.
- No approval/override workflow or production infrastructure.
- No camera/edge/PLC/MES, classifier or defect-ratio implementation.
- No renderer bypass, duplicate Python validator or arbitrary execution.
- No contract, schema or grounding changes hidden in HTTP integration.

==================================================
GIT DISCIPLINE
==================================================
Review git status, git diff --stat, git diff and every new file.
Separate prior changes, Task 6 changes and generated artifacts.
Do NOT commit.
Do NOT push.
Do NOT start Task 7.

After implementation and verification, report:
1. Files created
2. Files modified
3. FastAPI architecture and recorded readiness decisions
4. API endpoints and exact request/response/error contract
5. Domain service design
6. Canonical UISpec fixture and matching context location
7. Validator integration and unchanged schema authority
8. React API integration and restricted approved-handle issuance
9. Loading/error behaviour, stale responses and no silent fallback
10. Tests added and actual test discovery
11. Full test results, including Task 3-5 regressions
12. Schema parsing, meta-validation, instance and runtime check results
13. TypeScript, safety lint and production build results
14. Real-browser/API success and failure checks, URLs and screenshots
15. Dependencies added and exact selected versions
16. Security/control checks and excluded scope confirmation
17. Documentation changes
18. Architectural issues, remaining limitations or incomplete checks
19. Git status/diff summary, prior work and generated artifacts
20. Recommended next smallest task

If readiness is blocked, report the unresolved decisions and STOP
before implementation; do not present unexecuted checks as results.

STOP after the report.
Wait for human review before proceeding to Task 7.
```

## 21. Expected Task 6 Implementation Results

No Task 6 code, endpoint, transport adapter or API test has been created by this guide. A future report must record actual implementation and failures, not convert this proposal into a success claim. Completion requires both a working local API path and preserved renderer trust controls, including the agreed Hero action binding. An API-only HTTP 200 does not satisfy the browser objective.

## 22. Enterprise Engineering Lessons

Separate HTTP concerns, fixture orchestration, validation and rendering. Keep one schema authority and one source for grounding. Treat a transport boundary as an explicit architecture decision. Make failures visible and distinguish liveness from business readiness. Keep proposal, implementation and verification evidence separate. A safe static fixture demo does not automatically establish a safe runtime input path.

## 23. What Comes Next

The next smallest step is review of the readiness decisions in section 6, then an explicitly authorized implementation increment. Do not automatically introduce a browser-supplied GroundedContext as the tutorial suggests for its later ContextPayload task: our architecture assigns grounding to the server. Model integration remains a later independently reviewed increment, not an automatic Task 7 commitment.

## 24. The Control Model

```text
Business owns definitions and ratio policy
  -> server owns grounding
  -> schema defines structure
  -> Python validates structure, grounding and deterministic policy
  -> reviewed transport preserves the validated presentation and bindings
  -> private client issuance admits only the intended response path
  -> controlled registry renders text and approved components
```

Future AI may propose presentation only. It does not acquire data-access or quality-decision authority. Pattern-based text validation and tests cannot prove absence of every implied verdict; semantic evaluations remain a separate concern.

## 25. Task 6 Summary and Provenance

This document adapts the onboarding FastAPI teaching sequence to the existing Board Defect Inspection project. The source's v0 shape, nested Hero example, onboarding endpoints, API folder, success counts, dependency lower bounds and checkpoint are not project requirements. Its implementation-results sections become explicit pending verification sections.

References: source PDF; CLAUDE.md; docs/architecture.md and repository-structure.md; specs/spec.md and model-contracts.md; selected schema and preserved alternative; Task 3–5 reports; apps/ui and services/domain READMEs and source. The source PDF is preserved. The accompanying Markdown is the editable content source; Word is generated from it. Package/text integrity checks are not a visual Word pagination review or application verification.
