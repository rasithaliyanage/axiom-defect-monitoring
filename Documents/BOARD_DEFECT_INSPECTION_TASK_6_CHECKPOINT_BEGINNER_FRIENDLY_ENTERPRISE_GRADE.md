# BOARD DEFECT INSPECTION AI

Task 6 Checkpoint

Beginner-Friendly Enterprise-Grade Engineering Guide

FastAPI Domain Runtime and API-Backed UI

Checkpoint: PENDING — local implementation, not a committed milestone

Observed HEAD: 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da

HEAD commit message: update 2026-09-22

Proposed checkpoint message, not executed: Task 6: Implement FastAPI domain runtime and API-backed UI

Branch: wushan | Document review date: 2026-10-06 (corrected)

> **Correction, 2026-10-06.** This document previously existed only as a DOCX with no Markdown source
> or generator, so it drifted out of step with the code while its siblings were kept current. The
> text was extracted to this file, a generator was added, and the following were corrected against
> verified state: backend port 8001 → **8000**; request `{page, locale}` → **`{page, view, locale}`**;
> rejection `422 invalid_request` → **`400 BAD_REQUEST`** with the `{"error":{code,message}}`
> envelope; success body `{spec, source, rejections, contextId, actions}` → **`{spec, bindings, meta}`**;
> canonical fixtures `apps/ui/fixtures/` → **`tests/fixtures/ui-spec/`**; and test counts
> 197 Python / 63 UI → **240 / 93**. Section 3.1 was added for the payload contract, and the
> inspection queue endpoint recorded. Nothing in the architecture or scope boundaries changed.

Audience: Engineering leads, system auditors and technical stakeholders.

Reference: Customer_Onboarding_Task_6_Checkpoint_Beginner_Friendly_Enterprise_Grade.docx.pdf in Documents. The requested DOCX is present as a PDF export. This adaptation follows the user's 13-section outline. It consolidates the reference's enterprise lessons, mental model and final status into sections 5, 11 and 12. The source is unchanged. Application results are retained Task 6 implementation evidence; only document/Git inspection was performed for this report. No new application test or live smoke run is claimed.

## 1. What This Checkpoint Means

Task 6 was implemented previously. It connects the existing synthetic board-inspection landing page to a small FastAPI Domain Runtime while preserving Python validation and the controlled renderer. Readiness decisions were approved; a formal implementation review and Git checkpoint are not assumed.

A completed checkpoint would verify the reviewed implementation, commit the agreed files, push to the agreed branch and record synchronization. This document prepares that checkpoint; it does not perform those actions. The working tree contains earlier Task 4/5 assets, Task 6 implementation and unrelated documents. It is not clean. No Task 6 commit hash or push range can truthfully be supplied yet.

The business objective is a trustworthy view of motherboard inspection and defect activity across operational lines. Task 6 proves the presentation boundary with synthetic data. Image-based defect detection, line-level defect-ratio calculation and operational dashboards remain future business capabilities. Quality and Manufacturing own defect definitions and ratio policy.

## 2. Task 6 in the Overall Incremental Journey

Task 1  Project foundation and business context

|

v

Task 2  Machine-checkable v1 UISpec contract

|

v

Task 3  Deterministic Python UISpec validator

|

v

Task 4  Controlled React registry and renderer

|

v

Task 5  Minimal runnable synthetic React UI

|

v

Task 6  FastAPI Domain Runtime + API-backed UI

<-- CHECKPOINT CANDIDATE; Git checkpoint pending

|

v

Future  Separately reviewed AI Runtime / model seam

Task 7 NOT STARTED

This is an implementation journey, not a fabricated sequence of milestone commits. Task 6A from the onboarding tutorial is not an approved board-project task.

## 3. The Architecture at Checkpoint

UI RUNTIME: apps/ui/

Browser -> React / TypeScript -> fixed API client

|

| POST /api/v1/ui/landing-page

| {"page":"landing","view":"overview","locale":"en-US"}

v

Vite same-origin proxy -> 127.0.0.1:8000

|

v

DOMAIN RUNTIME: services/domain/

FastAPI route -> landing_service.py

|

v

Fixed overview UISpec + complete server-owned context

|

v

Task 3 UISpecValidator.validate(spec, context)

|

| require status VALID

v

Exact validated snapshot + matching action bindings

{spec, source:"fixture", rejections:[], contextId, actions}

|

v

UI RUNTIME

Unknown response JSON

-> exact match to independently prepared overview

-> private ApprovedUISpec handle issuance

-> ControlledRenderer -> explicit nine-entry registry

-> developer-authored React components -> browser

INDEPENDENT PREPARATION GATE

Fixed pairs -> Python validator -> generated catalogue

+ retained verification evidence

|

+-> fixed response admission reference

AI RUNTIME: NOT IMPLEMENTED

Future gateway/model requires a separately reviewed design.

FastAPI is Domain Runtime, not AI Runtime. The browser cannot supply grounding. The service validates the same request-local snapshot it returns. Its validator returns status/rejections, not an approved payload. Private browser issuance follows the reviewed fixed-fixture admission check; an HTTP 200, cast, brand or approved=true flag is insufficient.

The sole canonical pair remains tests/fixtures/ui-spec/full-catalogue.spec.json and overview.context.json. Hero labels come from matching context actions; CTA retains its supplied label. All actions are inert. The browser must fetch successfully; the prepared catalogue is never a failure fallback. This deliberately fixed transport cannot admit arbitrary future model-generated UISpecs. Changing the fixture requires matching frontend preparation/build.

### 3.1 Payload Contract as Implemented

`POST /api/v1/ui/landing-page` is the only endpoint that takes a payload.

```text
POST /api/v1/ui/landing-page
Content-Type: application/json

{ "page": "landing", "view": "overview", "locale": "en-US" }
```

| Field | Allowed values | Introduced |
| --- | --- | --- |
| page | landing | Task 6 |
| view | overview, minimal | Task 6 |
| locale | en-US | Task 6A |

All three are required with **no defaults**; an omitted field is rejected rather than silently
supplied. `extra="forbid"` on the transport model rejects any unknown field, which is the mechanism
that refuses supplied grounding — `context`, `metrics`, `alerts`, `actions`, `blocks` or `contextId`.
The browser cannot assert grounding truth.

`locale` is compared against the server-owned context's own locale and is **not echoed** in the
response, so no locale echo may be claimed.

Success returns `{spec, bindings, meta}`. `bindings` carries server-owned action labels, which a bare
UISpec provably cannot supply because `Hero.primaryAction` is an identifier with no label in the
contract. `meta.validation` is informational and the browser adapter does not treat it as proof.

Every failure returns one sanitized envelope `{"error": {"code", "message"}}` — `400 BAD_REQUEST`,
`404 NOT_FOUND`, `405 METHOD_NOT_ALLOWED`, `500 VALIDATION_FAILED` or
`500 INSPECTION_DATA_UNAVAILABLE`. Validator rejection codes are logged server-side and never
serialized.

#### Read-only endpoints taking no request body

```text
GET /health                                  -> {"status":"ok"}   liveness only
GET /api/v1/inspection/queue?line=&limit=    -> {records, meta}   synthetic board records
GET /api/v1/inspection/board/{boardId}       -> {record, meta}    single board lookup
```

These satisfy part of `specs/spec.md` FR-9. Records carry board identity and capture metadata only:
there is deliberately no status, disposition, verdict, score or defect-ratio field, because whether a
board passes inspection is a quality determination owned by Quality and Manufacturing and nothing in
this phase determines one.

Unimplemented from FR-9: `/inspection/summary`, `/ingest/images`, `/defects/categories`,
`/defects/alerts`, `/defects/summary`.

#### Parameter policy

Parameters exist on the inspection reads and nowhere else.

| Endpoint | Accepts | Rejects |
| --- | --- | --- |
| `GET /api/v1/inspection/queue` | `line` (optional, 1-64 chars), `limit` (optional, 1-50) | Unrecognised line value, out-of-bounds or non-numeric limit, any unknown parameter — all `400 BAD_REQUEST` |
| `GET /api/v1/inspection/board/{boardId}` | the path identifier | Any query parameter — `400`. Unknown identifier — `404 BOARD_NOT_FOUND` |
| `POST /api/v1/ui/landing-page` | nothing beyond the JSON body | A query string is **ignored, never honoured**: the response is byte-identical with and without one |

The last row is the boundary that matters. This endpoint feeds the controlled renderer, so
caller-steered input is exactly what the approved-input rule exists to prevent; filtering a read-only
list is a different risk class, with no model and no renderer downstream of it.

Allowed `line` values are **derived from the fixture at load**, in first-seen order, not declared as
an enum in code — line identifiers are owned by Manufacturing, and a second copy here would go stale
silently. An unrecognised value is a `400`, not an empty list: a typo must be visible, and an empty
list would read as "no boards". Queue `meta` reports `count`, the unfiltered `total` and the
`filters` applied, so a narrow filter is always distinguishable from an empty dataset. Caller text is
never echoed into an error message — the unknown-parameter error names the allowed set, not the
supplied name — and the board identifier is matched in memory against
already-loaded records — no path is constructed from it and no file is opened in the request path.

## 4. Verification Summary Table

| Checkpoint Item | Result | Evidence |
| --- | --- | --- |
| Task 6 Git commit | PENDING | No milestone commit created; observed HEAD 3810dc0 |
| Push / shared checkpoint | NOT PERFORMED | No push range or live remote synchronization claim |
| Current Git state | DIRTY | Fresh status inspection on wushan; prior and current work retained |
| Local tracking comparison | 0 ahead / 0 behind | HEAD...origin/wushan; cached local reference only, no fetch |
| Python suite | PASS | 282 passed, 2 warnings (2026-10-06) |
| Python discovery | PASS | 163 validator + 8 fallback + 7 fixture + 24 landing API + 24 request-context + 14 inspection queue + 42 inspection parameters |
| React suite | PASS | 93 passed across 6 files |
| Schema checks | PASS | Selected-schema JSON parsing, Draft 2020-12 meta-validation, instance validation and full runtime validation reported separately. The alternative schema is not meta-validated by the suite |
| Full runtime validation | PASS | Complete matching context; existing UISpecValidator; VALID with 0 rejections |
| TypeScript / safety lint / build | PASS | Strict compile clean; safety lint clean (10 files, 9 rules); Vite build |
| GET /health | PASS | HTTP 200, exactly `{"status":"ok"}`; direct and through the Vite proxy |
| POST landing endpoint | PASS | HTTP 200; VALID on revalidation; exact spec and ordered action-binding equality |
| Supplied grounding | REJECTED | HTTP **400** `BAD_REQUEST`, direct and proxy |
| GET /api/v1/inspection/queue | PASS | HTTP 200; synthetic board records; no quality determination |
| Inspection queue filters | PASS | `line=line-a` 200, `limit=2` 200, both combined 200; `count`/`total`/`filters` reported |
| Rejected parameters | PASS | Unknown line **400**, `limit=99` **400**, unknown parameter **400** |
| GET /api/v1/inspection/board/{id} | PASS | Known board 200; unknown board **404** `BOARD_NOT_FOUND` |
| UI endpoint parameter boundary | PASS | Query string on the landing POST returns an identical specification |
| Real Chrome rendering | PASS | `POST …/landing-page → 200` in the network log; nine components rendered. Narrow viewport and screenshots unverified |
| Backend unavailable | PRIOR PASS | Controlled error; no static fallback; notice remains |
| Dependencies | PRIOR PASS | pip check clean; pinned requirements and constraints |
| AI / Task 7 | NOT IMPLEMENTED | No model gateway or runtime model request |
| Production inspection | OUT OF SCOPE | No classifier, ratio service or quality decision |

Evidence: specs/TASK-6-IMPLEMENTATION-REPORT.md and specs/task6-browser-evidence/{api-smoke.json,observations.json,unavailable.json,wide.png,narrow.png,unavailable.png}. The unused alternative schema is not meta-validated by the current suite. Do not substitute tutorial test counts or treat parsing as full validation.

## 5. Beginner Explanation: Why a Checkpoint Matters

Finishing code and recording a reproducible milestone are separate steps. A commit identifies exact file content. Test and browser evidence show what was exercised. A verified push makes the reviewed commit available to colleagues. A clean working tree means there are no remaining local edits; it does not by itself establish correctness.

Our tests describe a working local Task 6 slice, but those files have not yet been packaged into a reviewed commit. Committing every current file would also capture unrelated work. The checkpoint must first establish an explicit file list and include any required earlier UI assets that are still untracked. Preserve unrelated files rather than deleting or staging them to manufacture a clean status.

• Stable boundaries separate UI, Domain and future AI responsibilities.

• Validation precedes transport success and rendering admission.

• The registry remains the only component rendering path.

• Dependency failure stays visible instead of displaying a static fallback.

• Small increments make failures and review decisions easier to explain.

## 6. API Smoke Tests

The following summarizes retained observations, not a new command transcript. URLs and results come from specs/task6-browser-evidence/api-smoke.json.

GET http://127.0.0.1:8000/health

-> HTTP 200

-> {"status":"ok"}

POST http://127.0.0.1:8000/api/v1/ui/landing-page

Content-Type: application/json

{"page":"landing","view":"overview","locale":"en-US"}

-> HTTP 200

-> source: fixture; contextId: task4-catalogue

-> runtimeValidation: VALID; actionsMatch: true

POST same endpoint with supplied grounding

-> HTTP 400

-> {"error":{"code":"BAD_REQUEST","message":"..."}}

GET http://127.0.0.1:8000/api/v1/inspection/queue

-> HTTP 200  (no parameters)

?line=line-a -> HTTP 200    ?limit=2 -> HTTP 200    ?line=line-b&limit=1 -> HTTP 200

-> {"records":[{"boardId":"BRD-2026-000150","line":"line-b",
                "inspectionPoint":"pre-conformal","recordedAt":"2026-09-22T06:13:05Z"}],
    "meta":{"source":"fixture","count":1,"total":4,
            "filters":{"line":"line-b","limit":1}}}

?line=line-z -> HTTP 400 {"error":{"code":"BAD_REQUEST","message":"Unknown line"}}

?limit=99 -> HTTP 400  "Query parameter is missing, out of range or of the wrong type"

?unexpected=x -> HTTP 400  "Unsupported query parameter. This endpoint accepts: limit, line"

The last two messages name the request part and the allowed set. Neither reflects what the caller
sent: the `limit` message used to read "Request is not a supported presentation request", inherited
from the landing-page handler, and the unknown-parameter message used to echo the supplied parameter
name. Both are now pinned by tests.

GET http://127.0.0.1:8000/api/v1/inspection/board/BRD-2026-000148

-> HTTP 200; unknown identifier -> HTTP 404 {"error":{"code":"BOARD_NOT_FOUND",...}}

Success contains exactly spec, bindings and meta. Invalid server fixtures produce 500 VALIDATION_FAILED; wrong methods produce 405 METHOD_NOT_ALLOWED; unknown routes produce 404 NOT_FOUND. These are sanitized HTTP errors, not new validator rejection codes. Health indicates process liveness only.

Reproduction commands, to run during the separately authorized checkpoint:

.venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8000

curl.exe -i http://127.0.0.1:8000/health

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/ui/landing-page -ContentType application/json -Body '{"page":"landing","view":"overview","locale":"en-US"}'

Feed response.spec, not the entire envelope, into UISpecValidator.validate with the complete canonical context. Require result.status == "VALID", exact fixture equality and exact ordered action-binding equality. Never use the onboarding validator.valid API.

## 7. Browser and System Smoke Tests

Vite: http://127.0.0.1:5173/

POST /api/v1/ui/landing-page via Vite -> HTTP 200

GET /health via Vite -> HTTP 200 {"status":"ok"}

Supplied grounding via Vite -> HTTP 400 BAD_REQUEST

Chrome 154.0.8037.93, retained implementation evidence:

1440x1000 and 375x812 -> nine blocks; no horizontal overflow

Keyboard focus -> visible outlines; controls remain inert

Clicks/reload -> unchanged values and deterministic DOM

Success -> no console errors or unexpected external/model traffic

Backend stopped -> expected proxy error; controlled visible UI error

-> notice retained; no main content or buttons

In a second terminal, start npm run dev from apps/ui and use its printed URL. The existing developer-owned browser script requires dedicated Chrome remote debugging on port 9225; setup is in apps/ui/README.md.

node apps/ui/scripts/check-browser.mjs http://127.0.0.1:5173/

node apps/ui/scripts/check-browser.mjs http://127.0.0.1:5173/ --expect-unavailable

The second command requires the backend to be stopped. An HTML-shell HTTP 200 is not React-rendering evidence. Prior verification stopped its own backend, Vite and dedicated browser. This document did not start services or freshly prove ports free. Ports were confirmed free before starting and released afterwards. No CORS middleware is needed for the narrow local proxy. Cross-browser and assistive-technology checks remain unverified.

## 8. Security and Control Verification

The implementation report and existing tests record these controls:

• No eval(), Function(), dangerouslySetInnerHTML or data-driven dynamic imports.

• No arbitrary component resolution or model-prop spreading onto DOM.

• ControlledRenderer receives only privately issued handles; copied/unissued objects fail.

• Unknown and inherited component names reject the entire page; no skip or repair.

• Fixed nine-component vocabulary; all five actions remain context-bound and inert.

• App uses ControlledRenderer, not a direct registry bypass.

• Strings render as React text; no executable API strings or JavaScript URLs.

• Python owns schema, grounding and text policy; TypeScript only admits the exact fixed response.

• Request fields are presentation-only; client grounding is rejected.

• Loading/error states, cancellation and no-fallback handling remain explicit.

• VALID means presentation validation, never board pass/fail or approval.

Schema authority remains specs/schemas/ui-spec.schema.json. The competing specs/ui-spec.schema.json is preserved with different bounds, not merged. These controls are not cryptographic authentication or proof against modified application source.

## 9. Dependency Review

Existing runtime: jsonschema==4.26.0, pydantic==2.13.5

Existing tests:   pytest==9.1.1

Task 6 runtime:  fastapi==0.142.1, uvicorn==0.54.0

Task 6 tests:    httpx==0.28.1

Resolved constraints: requirements-lock.txt, 28 packages

Observed environment: Python 3.14.7 / Node 24.20.0 / npm 11.19.0

React package.json and package-lock.json: unchanged by Task 6

No AI SDK, agent framework, ORM, authentication framework, cloud AI SDK or document-processing library was added. Mandatory framework transitives are recorded in the constraints; no telemetry exporter/instrumentation was configured. The retained Starlette TestClient warning recommends its newer HTTPX2 path; tests and pip check passed. The warning remains disclosed, not suppressed. Constraints describe the tested Windows environment, not a universal platform guarantee.

## 10. What Was NOT Started

• No tutorial ContextPayload parameters, onboarding segments, product interest or region seam.

• No Task 6A or Task 7 implementation, model gateway, AiClient or live generation.

• No authentication, database, persistence, uploads, document processing or risk scoring.

• No camera capture, image/edge processing, PLC/MES or physical integration.

• No defect classifier, live defect-ratio calculation, charts, line filters or image overlays.

• No board quality approval, override or human review workflow.

• No production infrastructure, deployment, model repair, retry or fallback orchestration.

• No schema redesign, duplicate grounding validator or second UI/API project.

Manufacturing inspection remains the business context, not a claim that this synthetic landing page detects defects from images.

## 11. Git History and the Core Mental Model

Fresh inspection on 2026-10-03 found this actual history, newest first:

3810dc0 update 2026-09-22

f5caf99 repo folder changes

f0e3f27 Update 2 initial discussion document

7345e6d Updated initial discussion document

4893869 Updated push

c7fef5e pdated files

Branch: wushan

HEAD: 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da

HEAD...origin/wushan: 0 ahead, 0 behind (cached ref)

Working tree: modified, deleted and untracked files

Task 6 commit: absent / pending

Task 6 push: not performed

Previous official Task 5 commit: not established

Local tracking equality does not prove the remote is current; no fetch or push was performed. Existing deletions under docs/ and untracked earlier UI/guide work are preserved. Do not import source-example commits or claim a clean checkpoint.

CURRENT, DETERMINISTIC

Fixed spec + complete context -> Python validation

-> agreed response + action bindings

-> exact prepared-fixture admission -> private handle

-> controlled registry -> known React components -> UI

FUTURE, NOT IMPLEMENTED

Model proposes UISpec -> Python validation with grounding

-> separately reviewed transport/admission -> renderer

VALID presentation != board PASS/FAIL or approval

The future model must never be allowed to create executable application behaviour. The current fixed-response adapter is deliberately not a general model-output adapter.

## 12. Recommended Next Steps

1. Review Task 6 implementation, its fixed-fixture transport limitation and the file inventory; resolve which earlier untracked UI assets belong in the checkpoint.

2. Run a separate verification-only checkpoint pass using section 13. Record fresh results and an exact staging plan. Obtain explicit commit/push authorization before those actions.

3. After checkpoint review, separately decide the next smallest board-specific increment. Do not copy onboarding Task 6A parameters or begin a model interface automatically.

Final status: TASK 6 IMPLEMENTED LOCALLY; FORMAL GIT CHECKPOINT PENDING. This document adds no runtime functionality and makes no commit, push, clean-tree or live-remote synchronization claim.

## 13. Exact Checkpoint Prompt Used

Provenance correction: no board-specific checkpoint execution has occurred. The following is the exact adapted prompt supplied for a future run, not a historical prompt claimed to have been executed. The source's unconditional commit/push instructions are replaced by the project's current review boundary. This preserves verification discipline without fabricating authorization or milestone history.

Proceed with Board Defect Inspection Task 6 checkpoint readiness only.

IMPORTANT

Implementation exists locally. Do not assume review, a commit or a checkpoint.

Do NOT implement functionality or start Task 6A or Task 7.

Do NOT add ContextPayload parameters, AI, a gateway or a model interface.

Do NOT change architecture, UISpec, either schema, validator or renderer.

This pass is VERIFY -> REVIEWABLE CHECKPOINT PLAN -> STOP.

Do NOT commit.

Do NOT push.

Commit/push requires a separately explicit instruction after review.

==================================================

CURRENT CHECKPOINT AND INSPECTION

==================================================

Read CLAUDE.md, README.md, docs/architecture.md,

docs/repository-structure.md, specs/spec.md, model-contracts.md,

Task 3-6 reports, Task 6 readiness, both schemas and selected notes.

Read apps/ui/README.md, services/domain/README.md and tests/README.md.

Inspect actual implementation, fixtures, preparation, locks and tests.

Run git branch --show-current, git rev-parse HEAD, git status,

git diff --stat, git diff and git log --oneline -6.

Inspect all untracked files relevant to the proposed checkpoint.

Recorded baseline was wushan at 3810dc0; verify, do not assume unchanged.

There is no established Task 5 milestone commit in this report.

Preserve unrelated edits and deletions. Report Git failures without repair.

Do not reset, clean, stash, move files or stage everything for convenience.

Confirm no Task 6A/7 or out-of-scope integration slipped into the increment.

Stop on a required unresolved contract or scope decision.

==================================================

COLD-STATE VERIFICATION

==================================================

Do not manufacture a clean working tree. Start from stopped task-owned

servers and record the actual dirty state. Use existing environments.

From root run:

.venv/Scripts/python.exe -m pytest --collect-only -q

.venv/Scripts/python.exe -m pytest -q

.venv/Scripts/python.exe -m pip check

From apps/ui run:

npm test

npm run typecheck

npm run lint

npm run build

Preserve fixture preparation gates, cleanup and verification evidence.

Do not manually edit src/generated/fixtures.ts.

Historical baseline: 197 Python and 63 UI tests; report actual discovery

and results instead of forcing a count or copying tutorial counts.

Distinguish schema JSON parsing, Draft 2020-12 meta-validation,

instance validation and complete runtime validation with context.

The suite does not meta-validate the alternative schema; say so.

Record the retained Starlette/HTTPX warning and any new failures.

If a check fails, report it; do not expand implementation scope silently.

==================================================

API SMOKE TEST

==================================================

Start the existing backend with:

.venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8000

Do not terminate unrelated listeners. Record actual port and URL.

GET /health must return 200 and exactly {"status":"ok"}.

POST /api/v1/ui/landing-page with application/json and exactly

{"page":"landing","view":"overview","locale":"en-US"} must return HTTP 200.

Expect exactly {spec, source, rejections, contextId, actions}:

source="fixture", rejections=[], matching task4-catalogue contextId.

Read canonical tests/fixtures/ui-spec/full-catalogue.spec.json and its full context.

Validate live response.spec with UISpecValidator.validate(spec, context).

Require status VALID, exact spec equality and ordered action equality.

Reject client grounding and unknown fields/values on the UI endpoint, and

confirm a query string there is ignored rather than honoured. Exercise the

read-only inspection reads unfiltered, filtered, over-bounded, with an

unknown filter value and with an unknown parameter; record every status.

Verify sanitized 400/404/405/500 contracts through existing tests;

do not introduce production invalid-fixture switches for smoke checks.

No bare-UISpec onboarding endpoint or validator.valid API substitution.

==================================================

BROWSER AND VITE SMOKE TEST

==================================================

Start npm run dev from apps/ui and use the printed URL.

Verify health and landing POST through the narrow same-origin proxy.

No CORS middleware is needed; do not add wildcard origins.

Use real Chrome/browser access with existing check-browser.mjs setup.

Confirm React actually renders all nine overview blocks and the notice.

Observe exact values/units/progress, severity, keyboard focus, inert

actions, wide/narrow layout, console and network behaviour.

Permit local Vite assets/HMR and the agreed local Domain API only.

Stop the task-owned backend and verify controlled error with no fallback.

Record screenshots/observations; mark unavailable checks unverified.

An HTTP 200 or HTML shell alone is insufficient rendering evidence.

Stop only the servers/browser started for this pass. Verify their

listeners are released; do not claim unrelated ports are free.

==================================================

SECURITY REGRESSION

==================================================

Run existing safety lint and registry/transport negative tests.

No eval, Function, raw HTML sink, model-prop spreading, executable

strings, data-driven import or arbitrary component resolution.

App must use ControlledRenderer with a privately issued handle.

No direct App registry bypass or API-name-driven React creation.

Unknown/inherited names reject the entire render without repair.

Response JSON stays unknown until complete fixed-response admission.

No cast, brand, approved flag or HTTP status is validation by itself.

Confirm actual accepted response data is issued, not a static fallback.

Keep all nine components/five actions and context-based Hero labels.

Keep cancellation, failure visibility, deterministic data and non-mutation.

Python retains schema/grounding authority; VALID is presentation only.

==================================================

DEPENDENCY AND DOCUMENTATION REVIEW

==================================================

Review requirements.txt, requirements-dev.txt, requirements-lock.txt,

apps/ui/package.json and package-lock.json.

Task 6 direct additions were FastAPI 0.142.1, uvicorn 0.54.0 and

HTTPX 0.28.1. Verify actual pins; do not upgrade during checkpointing.

No AI SDK, agent framework, ORM, auth, cloud or document-processing SDK.

Review README.md, docs/architecture.md, specs/spec.md, tests/README.md,

both runtime READMEs, readiness and implementation reports.

Retain explicit transport amendment and fixed-fixture limitations.

Do not assume docs/walkthrough.md exists or rewrite historical guides.

Record fresh results separately from prior implementation evidence.

==================================================

GIT HYGIENE AND PROPOSED COMMIT

==================================================

Run git diff --check and review full diff plus each relevant new file.

Separate prior work, Task 6 work and generated/ignored artifacts.

Exclude node_modules, dist, caches, .venv and generated fixture source.

Retain canonical pairs and intentional verification/browser evidence.

Identify required earlier UI files that are still untracked; a Task 6

commit must not omit its dependencies or absorb unrelated files.

Produce an exact proposed file list and explain unresolved scope.

Proposed message, subject to review:

Task 6: Implement FastAPI domain runtime and API-backed UI

Do not stage, commit or push in this pass. Do not copy origin/main.

Identify the actual intended remote/branch without claiming live sync

from cached tracking refs. Record any later authorization separately.

Only an authorized successful commit/push may establish a new hash,

push range and remote synchronization. Never invent those fields.

==================================================

FINAL REPORT AND SCOPE CONFIRMATION

==================================================

Report branch, HEAD, review state, dirty files and proposed commit scope.

Report actual Python/UI discovery/results, schema checks, typecheck,

safety lint, build, dependencies, API and real-browser evidence.

Include commands, URLs, screenshots, failures, warnings and limitations.

Confirm no new runtime functionality, Task 6A/7, model/gateway, auth,

database, uploads, document/risk features, manufacturing integration,

classifier, ratio calculation, quality approval/override or production

infrastructure. No hidden contract changes, fallback or renderer bypass.

State commit and push NOT PERFORMED unless separately authorized later.

Give the smallest next review step. STOP. Wait for human review.

