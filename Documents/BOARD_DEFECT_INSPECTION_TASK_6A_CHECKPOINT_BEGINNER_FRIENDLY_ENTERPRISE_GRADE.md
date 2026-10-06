# BOARD DEFECT INSPECTION AI
@ Task 6A Checkpoint
@ Explicit Presentation Request Context Propagation
@ Beginner-Friendly Enterprise-Grade Checkpoint Guide

**Checkpoint status: VERIFIED — Task 6A is implemented locally; the Git checkpoint remains pending.**
**Inspection date:** 2026-10-06 (corrected). **Branch:** wushan. **HEAD:** 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da.

> **Correction, 2026-10-06.** This document was first issued as BLOCKED on the finding that Task 6A
> was absent. That finding was wrong. It described the Customer Onboarding tutorial's codebase, not
> this repository: it reported `get_landing_ui_spec`, `LandingRequest` and `INITIAL_CONTEXT`, none of
> which have ever existed here, and declared four files missing that were present — two of them
> created on 2026-10-03, three days before the inspection. Sections 5, 6 and 15 have been rewritten
> against verified state. The genuine divergences, which are deferred contract decisions rather than
> missing work, are retained and listed in section 15.

This document adapts Customer_Onboarding_Task_6A_Checkpoint_Beginner_Friendly_Enterprise_Grade.docx using the supplied board-specific checkpoint prompt. The source's 23-section teaching sequence is retained. Its completed checkpoint, counts, commit hashes and synchronization claims are not copied as project results. The source document remains unchanged.

The supplied prompt ends at the Phase 13 heading. Section 22 provides a clearly labeled, completed adaptation using the source's final review/commit/push/report sequence. That completion is authored guidance, not a verbatim record of missing user text. Only initial repository/source inspection was executed; the checkpoint stopped before tests, staging, commit or push because the prerequisite failed.

## 1. What Is a Checkpoint?

A checkpoint verifies an already implemented increment, reviews its exact file scope, records it in Git and, when all conditions and target-branch requirements are satisfied, synchronizes the intended remote branch. It does not implement missing functionality or make previous work appear to be a new milestone.

```text
Existing implementation -> inspect -> verify -> review
 -> commit agreed files -> push agreed target -> verify synchronization

Missing implementation -> STOP before checkpoint
```

The user's commit/push instruction is conditional on successful verification. That condition has not been met. This document reports the failed prerequisite rather than claiming an executed checkpoint.

## 2. Why Task 6A Would Need Its Own Checkpoint

The proposed board Task 6A would carry the existing presentation request explicitly into the domain service without adding new HTTP fields or an AI model. Its value is traceability and ownership, not new generated UI.

```text
Task 1  Foundation
Task 2  v1 contract / selected schema
Task 3  Python validator
Task 4  Controlled renderer / private handles
Task 5  Browser-ready synthetic UI
Task 6  Local Domain API (implemented locally)
Task 6A Explicit request propagation (proposal, NOT implemented)
        |
        v
Checkpoint blocked -> resolve prerequisite -> separate review
Future tasks require their own scope and authorization
```

Do not import the reference's Task 7–16 numbering for Rules, Skills, Hooks, Plugins, Agent SDK or model integration. No such work is authorized by this checkpoint.

## 3. Current and Intended Runtime Baselines

```text
OBSERVED TASK 6
React -> fetchLandingPage(signal)
 -> loader constructs fixed page/locale JSON
 -> strict POST validation -> get_landing_ui_spec()
 -> server-owned fixture/context -> Python validator
 -> exact response admission -> private handle -> renderer

TASK 6A TARGET, NOT OBSERVED
React INITIAL_CONTEXT
 -> fetchLandingPage(requestContext, signal)
 -> same POST JSON -> strict validation -> immutable ContextPayload
 -> get_landing_ui_spec(request_context)
 -> server context association -> existing Python validator
 -> full response admission + request page association
 -> private handle -> ControlledRenderer -> browser
```

Runtime AI remains absent in both flows. The target cannot be declared complete merely because the existing Task 6 API returns a valid fixture.

## 4. ContextPayload in Simple Terms

| Field | Exact supported value | Meaning |
| --- | --- | --- |
| page | landing | Requested presentation page |
| locale | en-US | Required supported presentation locale |

Both are required JSON POST body fields. There are no dormant defaults, onboarding enums, manufacturing line/shift/board-type fields or client grounding. ContextPayload is a small presentation request, not the full GroundedContext.

The server retains the complete context with identity, fixed synthetic timestamps, capabilities, metrics, alerts, categories and actions. Python validation still receives that complete server-owned context. VALID never means board quality approval.

## 5. What Task 6A Was Intended to Change

Task 6 already accepts and validates page/locale. The proposed increment would retain the parsed request, construct an immutable domain value and pass it explicitly to the service. The service would check page/locale association before validating the unchanged fixed pair. React would supply a fixed INITIAL_CONTEXT and snapshot it through asynchronous loading.

Verified inspection, 2026-10-06, found the increment present:

| Artifact | State |
| --- | --- |
| services/domain/request_context.py | Present — `Page` / `View` StrEnums and a frozen, slotted `ContextPayload` |
| tests/api/test_request_context.py | Present — 23 tests |
| specs/TASK-6A-READINESS.md | Present — records five blockers and the decisions taken |
| specs/TASK-6A-IMPLEMENTATION-REPORT.md | Present |
| routes.py | Constructs `ContextPayload` after transport validation, then calls `_service.presentation(payload)` |
| landing_service.py | `presentation(request: ContextPayload)`; `VIEWS` keyed by `View`; `PageMismatch` on request/context disagreement |
| apps/ui/src/App.tsx | `fetchLandingPage({ view, signal })` |

The earlier claim rested on three symbols — `get_landing_ui_spec`, `LandingRequest` and
`INITIAL_CONTEXT` — that return zero matches across `services/`, `apps/ui/src/` and `tests/`. They
are the reference tutorial's names. The scope implemented here is narrower than this guide proposes,
by explicit decision recorded in the readiness note; see section 15 for what was deferred and why.

## 6. What This Checkpoint Actually Verified

| Checkpoint item | Status | Evidence |
| --- | --- | --- |
| Branch and HEAD | Observed | wushan; 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da |
| Working tree | Dirty | Prior modified/deleted/untracked work retained; unrelated edits preserved |
| Task 6A code and reports | **Present** | `request_context.py`, `test_request_context.py`, both specs; file timestamps predate this inspection |
| Python suite (§7) | **PASS** | 217 passed, 1 warning — 163 validator + 7 fixture + 24 API + 23 request-context |
| Python discovery (§7) | **PASS** | 217 collected, matching 217 passed |
| `pip check` (§7, §14) | **PASS** | No broken requirements found |
| React suite (§8) | **PASS** | 88 passed across 6 files |
| TypeScript / safety lint (§8) | **PASS** | Strict compile clean; safety lint clean, 10 files, 9 rules |
| Production build (§9) | **PASS** | Vite build 670ms |
| Schema checks (§9) | **PASS** | JSON parsing, Draft 2020-12 meta-validation, instance validation and full runtime validation reported separately; alternative schema not meta-validated, and not claimed |
| Execution safety (§12) | **PASS** | No `eval`, `Function`, raw-HTML sink or dynamic import in `apps/ui/src` with comments stripped |
| Private issuance (§12) | **PASS** | 2 mint sites, both inside `renderer/approved.ts`; 0 elsewhere in `src` |
| Locale echo (§12) | **PASS** | Zero `locale` occurrences in transport models; no echo claimed |
| Contract protection (§13) | **PASS** | `model-contracts.md`, both schemas, `spec.md`, renderer, registry, types, components and canonical fixtures all last modified before Task 6A |
| `approved.ts` unchanged (§13) | **No conflict here** | The transport adapter has lived inside `approved.ts` since Task 6; Task 6A did not modify it |
| Dependencies (§14) | **PASS** | Zero added by Task 6A. The only additions against HEAD are `fastapi`, `uvicorn`, `httpx` from Task 6 |
| Staging / commit / push | Not performed | Deliberate — this remains a verification pass |
| Remote synchronization | Not established | No fetch or push performed; no synchronization claimed |

Prior Task 6 evidence remains in `specs/TASK-6-IMPLEMENTATION-REPORT.md` and
`specs/task6-browser-evidence/`. It is not relabelled as Task 6A verification; the results above were
run fresh on 2026-10-06.

## 7. Cold-State Python Verification

Run only after the implementation prerequisite and comparison baseline are resolved:

```powershell
.venv/Scripts/python.exe -m pytest --collect-only -q
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check
```

Report actual count, duration, discovery and warnings. Include validator, fixture-handoff, API and new request-propagation cases. Prior Task 6 recorded 197 passing Python tests and one Starlette/HTTPX deprecation warning; no fresh Task 6A result exists. Do not alter tests to match a target count or silently suppress warnings.

## 8. React Verification

From apps/ui, the future checkpoint must run npm test, npm run typecheck and npm run lint. Preserve Task 4 renderer/registry/DOM controls, Task 5 application coverage and Task 6 admission tests. Task 6A tests must actually demonstrate request propagation, immutable snapshots and response page association.

Prior Task 6 recorded 63 passing UI tests. That baseline cannot prove new code that is absent. Report warnings honestly rather than interpreting “strict checking without warnings” as permission to hide tooling diagnostics.

## 9. Schema and Production Build Verification

Distinguish JSON parsing, Draft 2020-12 meta-validation, instance validation and full Python grounding/policy validation. The selected authority is specs/schemas/ui-spec.schema.json; the alternative remains preserved and unused. Current tests do not meta-validate that alternative.

After readiness, run npm run build from apps/ui. Keep Python fixture preparation and stale-output cleanup gates. Do not manually edit generated fixtures.ts. Ensure dist, node_modules and caches remain ignored; do not recursively delete unrelated output to manufacture a clean tree. No build was run for this blocked checkpoint.

## 10. API Smoke Tests

Target backend is 127.0.0.1:8001; preserve unrelated listeners. Tests below remain expectations, not executed results.

| Request | Expected | Actual this checkpoint |
| --- | --- | --- |
| GET /health | 200, status ok | Not run |
| POST landing route with {} | 422 invalid_request | Not run |
| POST exact landing/en-US | 200 complete existing envelope | Not run |
| POST extra lineId | 422 invalid_request | Not run |
| POST locale fr-FR or unsupported page | 422 invalid_request | Not run |
| POST with query parameters | 422 invalid_request | Not run |
| GET landing route | 405 method_not_allowed | Not run |

Success must retain {spec, source, rejections, contextId, actions}, source fixture, empty rejections and exact canonical spec/bindings. Revalidate response.spec against the complete canonical server context. Prove rejected requests never reach the service with isolated route tests; HTTP status alone does not demonstrate that internal property.

## 11. Browser Smoke Test

After a real implementation, start npm run dev, use its printed URL and observe actual React rendering. Confirm exact JSON POST body, full admission, external notice, nine overview blocks, unchanged metric strings/units/progress, focus, responsive layouts and inert controls. Stop the task-owned backend and reload to prove a controlled error without static fallback.

The overview displays only its supplied controls; all five approved actions are covered by dedicated fixtures/tests. Do not claim five visible buttons on the overview page or modify it to create them. Local Vite assets/HMR and the agreed Domain API are expected; external/model traffic is not.

Record browser/version/screenshots, console and network, or mark checks unavailable. A shell HTTP 200 is insufficient. No browser was started during this blocked checkpoint.

## 12. Security and Admission Verification

The future checkpoint must preserve no eval, Function, raw HTML sink, data-driven imports, arbitrary component lookup or model-prop spreading. The explicit registry remains the only component mapping and rejects inherited/unknown names for the whole page.

Private issuance remains inside approved.ts. Request page association is supplementary to full response equality; it cannot replace complete admission or server validation. No locale echo field exists in the response, so do not claim one. The server must compare requested locale to its own context.

No context values become grounding, file paths, executable code or URLs. No raw spec or approval flag reaches ControlledRenderer. Existing Task 6 controls are recorded historically; new Task 6A assertions have not been executed here.

## 13. Contract and Renderer Protection

Compare against a reviewed Task 6 baseline, not blindly against the current old HEAD. Preserve model-contracts.md, both schemas, specs/spec.md, canonical overview pair, render.tsx, registry.ts, types.ts and components.tsx. The repository uses components.tsx, not a components/ directory.

**Blocking inconsistency:** The supplied prompt also requires approved.ts unchanged. The existing restricted loader and private issuer live in that file, and the Task 6A proposal extends that loader with request capture/admission association. The policy needs explicit reconciliation before implementation or checkpointing. Possible reviewed designs must preserve private issuance and full response admission; moving logic merely to evade the unchanged-file check is not acceptable.

This checkpoint does not resolve the conflict by editing code or relaxing the rule. An agreed before/after baseline must distinguish expected earlier Task 6 modifications from unexpected Task 6A changes. Existing dirty contract files relative to HEAD are not automatically evidence that Task 6A changed them.

## 14. Dependency Verification

Task 6A is expected to add zero third-party packages. Compare requirements.txt, requirements-dev.txt, requirements-lock.txt, apps/ui/package.json and package-lock.json against the agreed baseline. Retain existing FastAPI/Pydantic and React tooling.

Do not import source tutorial dependency versions or install new tooling merely for a checkpoint. No packages were installed in this document task. Full dependency regression remains not run because the implementation prerequisite failed.

## 15. Proposed Change Set Versus Actual State

| Expected area | Observed state |
| --- | --- |
| Domain context module | **Present** — `services/domain/request_context.py` |
| Task 6A readiness/report | **Present** — both specs |
| routes.py / landing_service.py | Explicit domain request implemented; service takes `ContextPayload` |
| App.tsx / API client | `fetchLandingPage({ view, signal })` |
| API tests | Actual path `tests/api/` — `test_landing_api.py` and `test_request_context.py` |
| UI tests | Actual files `api-integration.test.tsx`, `app.test.tsx`, `proxy-config.test.ts` |
| approved.ts | Transport adapter and private issuance both inside it, since Task 6; untouched by 6A |
| Prior work | Mixed modified/untracked files; not a Task 6A-only diff |

### Divergences from this guide — deferred by decision, not missing work

Four of these were raised as blockers in `specs/TASK-6A-READINESS.md` and deferred by explicit user
decision in favour of a seam-only scope with no wire change.

| This guide expects | This repository | Status |
| --- | --- | --- |
| `ContextPayload{page, locale}` | `{page, view}` | Deferred contract decision |
| Rejection `422` + `{"error":"invalid_request"}` | `400` + `{"error":{code,message}}` | Deferred. Adopting the flat body would reverse the Task 6 fix that made every error share one envelope |
| Response `{spec, source, rejections, contextId, actions}` | `{spec, bindings, meta}` | Deferred wire change |
| Backend port 8001 | 8000, matching the Vite proxy | Runtime flag, not a defect |
| "nine overview blocks" | 12 blocks covering all 9 component types and all 5 actions | Guide conflates component types with block instances |
| `components.tsx`, `render.tsx`, `registry.ts`, `types.ts` at `src/` | `src/components/approved.tsx`, `src/renderer/*` | Our layout, settled in `docs/adr/0001-repository-layout.md` |

This documentation task updates only this checkpoint guide and its generated DOCX. It does not change
runtime code, historical BRDs or any earlier guide.

## 16. The Checkpoint Commit

No checkpoint commit was created. No files were staged. The instruction to commit after successful verification cannot be fulfilled while the requested implementation is missing.

A possible future message is “Task 6A: Propagate explicit presentation request context”, subject to the completed checkpoint procedure. Do not use the source's commit hash, amend older milestones, squash unrelated work or stage all current files. Any required untracked Task 4–6 dependencies need an explicit staging decision.

## 17. Final Repository Synchronization

```text
Observed branch: wushan
Observed HEAD: 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da
Message: update 2026-09-22
Working tree: DIRTY, preserved
Task 6A commit: NONE
Push to origin/main: NOT PERFORMED
HEAD == live origin/main: NOT VERIFIED
```

The requested target is origin/main, but the working branch is wushan. Do not silently switch, merge, rename or run a push that updates an unrelated local main. Resolve the intended integration path and verify remote state before any future push. No force push or implicit history repair.

## 18. What Was NOT Introduced

No functionality, runtime AI, Model Gateway, Agent SDK, model evaluation, feedback loop, Rules, Skills, Hooks or Plugins. No manufacturing line/shift/board-type inputs, classifier, ratio calculation or quality decision. No authentication, persistence, production infrastructure or new dependencies. Task 7 was not started.

No missing Task 6A code was written during checkpointing. Preserving that distinction is the central stop condition in the user's request.

## 19. Why This Is an Important Architectural Boundary

```text
ENGINEERING TIME                  APPLICATION RUNTIME
Instructions / tools / review     Request -> server-owned context
Tests and evidence               -> validator -> private admission
                                 -> renderer -> browser

Future probabilistic model is separate from both the coding agent
and the currently deterministic fixture pipeline.
```

A checkpoint can freeze a verified runtime foundation only when that foundation exists in the reviewed files. A polished report cannot replace missing implementation evidence. Context intent, grounding authority and executable UI control remain distinct responsibilities.

## 20. Transition Beyond Task 6A

The next action is to locate an existing implementation if it resides in another checkout, or separately authorize implementation after resolving the approved.ts constraint. Do not search or modify unrelated branches implicitly, and do not begin Task 7.

The reference's future curriculum is informative, not an agreed project roadmap. New engineering-time controls or model integration require their own scoped instructions after the current milestone is actually reviewed.

## 21. Beginner Mental Model

```text
A guide describes a change.
Source files demonstrate the change exists.
Fresh tests demonstrate what was verified.
A reviewed commit identifies exact content.
A successful verified push establishes shared history.

Missing source change -> checkpoint stops at the first gate.
```

AI may propose; deterministic software controls allowed presentation. VALID is not board approval. This document records a blocked checkpoint honestly rather than turning a proposed request seam into a completed manufacturing capability.

## 22. Completed Board Checkpoint Prompt — Adapted, Not Executed

This is a normalized complete adaptation of the supplied phases and the source's final checkpoint sequence. The user's text ended at Phase 13; phases 13–16 and the closing report below are reconstructed guidance. Conflicting prerequisites are explicit stop gates. This prompt is not a claim that the steps were run, nor authorization to implement missing features.

```prompt
Task 6A Checkpoint — Explicit Presentation Request Context Propagation

Checkpoint an already implemented and reviewed Task 6A only.
Do NOT implement new functionality. Do NOT start Task 7.
Objective: verify -> review -> conditionally commit/push -> synchronize.
The assertion that Task 6A is complete must be verified from actual files.
If implementation is absent, STOP before tests/staging/commit/push and report.

Required target flow:
React INITIAL_CONTEXT -> fetchLandingPage(requestContext, signal)
 -> POST /api/v1/ui/landing-page with page landing and locale en-US
 -> strict request validation -> immutable ContextPayload
 -> explicit service argument -> server GroundedContext association
 -> UISpecValidator.validate(raw_spec, complete_server_context)
 -> exact envelope/action bindings -> full response admission
 -> request page association -> private handle -> ControlledRenderer.

No AI/model, gateway, Agent SDK, evals, feedback, Skills, Hooks, Plugins,
Rules, manufacturing context fields or other runtime functionality.

==================================================
PHASE 1 — VERIFY REPOSITORY STATE
==================================================
Run git status, git branch --show-current, git log --oneline -8.
Confirm actual Task 6A source and reports exist; do not trust a guide alone.
Record HEAD, review state and unrelated changes. Do not modify anything yet.
Expected working branch must be agreed; do not assume main from the tutorial.
If Task 6A is missing, STOP and report actual signatures/absent files.

==================================================
PHASE 2 — REVIEW THE DIFF AND BASELINE
==================================================
Review git diff, git diff --stat, git diff --name-only, git status --short
and relevant untracked files. Preserve unrelated modifications/deletions.
Read the Task 6/6A reports, readiness decisions, actual source and tests.
Expected scope includes request_context.py (or agreed module), routes.py,
landing_service.py, client/App, propagation tests, reports and READMEs.
Use actual test paths, not tutorial file names.
Identify a reviewed Task 6 baseline for comparison. Old HEAD is not enough
if Task 6 itself remains uncommitted. Stop if scope/baseline is unresolved.
No implementation fixes, test weakening, cleanup, reset or implicit repair.

==================================================
PHASE 3 — PROTECT CONTRACTS AND RENDERER
==================================================
Compare model-contracts.md, both schema files, specs/spec.md and canonical
overview spec/context against the agreed Task 6 baseline.
Compare render.tsx, registry.ts, types.ts and actual components.tsx.
The supplied requirement also protects approved.ts. If request propagation
required editing its loader, STOP for an explicit reviewed exception/design
decision. Do not waive the requirement or move issuance to bypass it.
Unexpected protected-file changes block commit.

==================================================
PHASE 4 — VERIFY CONTEXT CONTRACT
==================================================
Exactly page='landing' and locale='en-US'; both required JSON body fields.
Missing/invalid/extra/non-JSON/query input rejects with sanitized 422;
GET on landing rejects 405. No silent coercion or defaults.
ContextPayload reaches get_landing_ui_spec(request_context) explicitly.
Server context page/locale association happens before spec validation.
Full GroundedContext remains server-owned. No generated_for or fake echo.
Retain {spec, source, rejections, contextId, actions} exactly.

==================================================
PHASE 5 — COLD-STATE PYTHON VERIFICATION
==================================================
From root run:
.venv/Scripts/python.exe -m pytest --collect-only -q
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check
Record exact counts, duration, discovery, warnings and failures.
Include validator, fixture handoff, API and request propagation tests.
Do not reuse prior counts or modify tests simply to make them pass.

==================================================
PHASE 6 — REACT VERIFICATION
==================================================
From apps/ui run npm test, npm run typecheck, npm run lint.
Verify renderer/registry/safety, application, full admission and new page
association/request tests. Report actual warnings; do not suppress them.
Confirm immutable snapshots and cancelled/stale responses remain safe.

==================================================
PHASE 7 — SCHEMA REGRESSION
==================================================
Report JSON parsing, Draft 2020-12 meta-validation, instance validation
and full runtime validation separately. Validate canonical pairs through
existing preparation gates; preserve cleanup/evidence.
Do not claim the alternative schema was meta-validated by the current suite.
No schema changes, new validator codes or duplicate TypeScript grounding.

==================================================
PHASE 8 — PRODUCTION BUILD
==================================================
From apps/ui run npm run build. Require strict TypeScript and Vite success.
Verify build/generated/cache outputs are ignored and excluded from staging.
Do not delete unrelated artifacts. Return to repository root.

==================================================
PHASE 9 — API SMOKE TEST
==================================================
Start the existing backend on 127.0.0.1:8001; preserve other listeners.
GET /health -> 200 {"status":"ok"}.
POST /api/v1/ui/landing-page:
{} -> 422 invalid_request.
{"page":"landing","locale":"en-US"} -> 200 exact envelope.
Extra lineId, missing fields, unsupported locale/page -> 422.
Any query parameters -> 422; GET landing -> 405.
Verify response.spec with complete canonical context and exact bindings.
Use route tests to prove invalid input never reaches the domain service.
Do not add production test switches or arbitrary fixture/path inputs.

==================================================
PHASE 10 — REAL BROWSER / VITE
==================================================
Run npm run dev in apps/ui and use its printed URL.
Observe exact POST body, real rendered nine blocks, external notice,
exact data, focus, wide/narrow layouts, console and network.
Overview controls are inert; all five actions are covered across fixtures/tests,
not necessarily visible on this one page. Do not change content for this check.
Stop backend and reload: controlled error, no static fallback.
Record screenshots/browser/URLs or explicitly mark unavailable checks.
Only expected local assets/HMR/API traffic. Stop task-owned processes afterward.

==================================================
PHASE 11 — SECURITY AND ADMISSION
==================================================
Run existing lint/runtime safety assertions. No eval, Function, dynamic import,
raw HTML, arbitrary prop spreading or data-driven component/module resolution.
No model SDK/external domain call. Preserve fixed registry and private issuer.
Full response equality is mandatory before request page association/issuance.
No locale echo claim: locale is not a response field.
App renders only through ControlledRenderer; no raw JSON handle cast.

==================================================
PHASE 12 — DEPENDENCIES
==================================================
Compare Python requirements/constraints and UI manifests/lock with baseline.
Task 6A should add no third-party dependencies. Report unexplained drift.
Do not upgrade packages during a checkpoint or hide known warnings.

==================================================
PHASE 13 — FINAL DIFF REVIEW (COMPLETED ADAPTATION)
==================================================
Run git status --short, git diff --stat, git diff and git diff --check.
Review every candidate new file and exact staged-file plan.
Exclude secrets, environment files, node_modules, dist, caches and generated
fixture source. Retain deliberate verification evidence and canonical pairs.
Separate unrelated local work and any required untracked prior dependencies.
If an isolated, self-contained checkpoint cannot be established, STOP.

==================================================
PHASE 14 — CONDITIONAL CHECKPOINT COMMIT
==================================================
Only proceed when implementation exists, all required checks pass and baseline,
protected-file policy, exact staging scope and branch strategy are resolved.
Stage only the reviewed files/hunks; never git add everything.
Inspect git diff --cached and --cached --check before commit.
Suggested board message:
Task 6A: Propagate explicit presentation request context
Do not amend, squash or rewrite previous history.
Do not commit Task 6 work under a false Task 6A label.

==================================================
PHASE 15 — PUSH TO THE AGREED TARGET
==================================================
User-requested target is origin/main. Verify remote and branch integration
strategy first. If still on wushan, STOP for the intended merge/push path;
do not switch/merge/rename implicitly or push unrelated local main.
Once resolved and checks pass, push the intended checkpoint without force.
Record exact command/result. Failed push is not synchronization.

==================================================
PHASE 16 — FINAL SYNCHRONIZATION
==================================================
Inspect git status, git log --oneline -8, git rev-parse HEAD and the verified
remote main tip. Confirm the intended committed content is present remotely.
Do not infer live remote state from stale cached refs.
Report remaining unrelated dirty files honestly; do not delete them to claim
clean status. If a clean-tree checkpoint is required, leave it unmet and report.
Record actual hash, message, push range and synchronization result only.

FINAL REPORT
Report initial state, baseline, reviewed scope, contract/renderer comparisons,
all commands/results/counts/durations, schema checks, build, API/browser evidence,
security, dependencies, final files, warnings and incomplete checks.
Report commit/push as NOT PERFORMED if blocked; never invent a hash.
State final branch/HEAD/remote result and remaining dirty work accurately.
Confirm no new functionality, Rules, Skills, Hooks, Plugins, SDK, AI, new
manufacturing fields or Task 7 work. STOP and wait for human review.
```

## 23. Final Checkpoint State and Required Next Action

```text
Task 6A completion asserted by prompt
 -> repository inspection
 -> implementation absent + protection/branch questions
 -> CHECKPOINT BLOCKED
 -> no tests falsely relabeled
 -> no staging / commit / push
 -> STOP; document findings
```

To resume checkpointing, identify the checkout/branch containing the completed Task 6A work, or separately authorize its implementation after the approved.ts policy is resolved. Establish the Task 6 comparison baseline and intended wushan-to-origin/main integration path. This document does not perform those steps or start the next task.
