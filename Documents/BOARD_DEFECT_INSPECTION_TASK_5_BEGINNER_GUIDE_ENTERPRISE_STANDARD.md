# Board Defect Inspection AI
# Task 5 - Minimal Runnable React UI
@ Beginner-Friendly Enterprise Standard Guide
@ Browser Readiness and Verification of the Existing Task 4 Demonstration

**Status:** Proposed Task 5 guide and implementation prompt. Documentation adaptation only; Task 5 has not been executed or accepted by this work.

**Prepared:** 30 September 2026. Adapted from `Customer_Onboarding_Task_5_Beginner_Guide_Enterprise_Standard.docx`. The source remains unchanged.

## 1. Purpose of Task 5

The manufacturing organization wants to inspect motherboard images from each operational line, identify defects, calculate agreed line-level defect ratios and provide a dashboard with traceable evidence. This task advances only the browser presentation foundation for that larger goal.

The onboarding tutorial calls Task 5 the first runnable browser milestone. In this repository, Task 4 already created a Vite application shell, React entry point, developer-authored styling and five Python-verified fixture pairs. Our Task 5 therefore verifies that existing application in a real browser and closes only demonstrated application-readiness gaps. It must not recreate the renderer or scaffold a second UI project.

The deliverable is a reproducible synthetic inspection landing-page demonstration with recorded browser evidence. It is not a working image-inspection system, a live defect-ratio dashboard, or runtime AI integration.

## 2. Position in the Incremental Architecture

```text
Task 1 - Project foundation and specifications
Task 2 - Machine-checkable UISpec contract
Task 3 - Deterministic Python UISpec validator
Task 4 - Controlled renderer, verified fixtures and Vite shell
Task 5 - Browser readiness, focused gaps and verification
Later  - Separately scoped domain services, model integration,
         evaluations and governed manufacturing workflows
```

Do not inherit the onboarding tutorial's Task 6-9 numbering as an approved board-project roadmap. The broader architecture documents are proposals; this guide does not authorize their implementation.

## 3. Task 5 Architectural Boundary

```text
Developer-authored UISpec JSON + complete synthetic context
                         |
                         v
Existing Task 3 Python validator, run during preparation
                         |
                         v
Generated static fixture data + retained verification evidence
                         |
                         v
Private ApprovedUISpec handle issuance in approved.ts
                         |
                         v
ControlledRenderer -> explicit registry -> React -> browser
```

Developer authorship alone is not approval. The existing preparation script must actually validate each fixture against its matching GroundedContext. TypeScript compatibility, a cast, a brand or an `approved=true` field does not establish validation.

There is an offline Python preparation step, but no live validation API or browser-to-Python transport. The renderer accepts only privately issued handles. VALID refers to presentation validation, never board PASS/FAIL or quality approval.

## 4. Adapted Task 5 Implementation Prompt

The following future implementation prompt follows the source guide's opening scope statement, architectural decision block, divider lines and 21 numbered sections, adapted for this repository. It is not a record of executed work, and including it here does not start Task 5.

```prompt
Proceed with Task 5: verify and complete the Minimal Runnable React UI.

This is the next smallest browser-readiness increment for the
Board Defect Inspection AI application.

IMPORTANT:
Task 4 already includes a Vite shell and synthetic demonstration.
Inspect its actual state; do not assume it is reviewed or checkpointed.
The current architecture described by the board guide contains:
- the v1 model contract and selected JSON Schema
- the deterministic Python UISpec validator
- the controlled React component registry and renderer
- paired synthetic UISpec/context fixtures and preparation checks
- the existing Vite application shell and renderer tests

Reuse that implementation and close only demonstrated Task 5 gaps.
Do NOT start Task 6 or introduce runtime AI, a model gateway,
FastAPI integration, authentication, persistence or infrastructure.
Do NOT add camera capture, defect inference, live defect-ratio
calculation, image overlays or manufacturing approval workflows.
Do NOT redesign the model contract, recreate or bypass the renderer,
or scaffold a second UI project.

--------------------------------------------------
IMPORTANT ARCHITECTURAL DECISION
--------------------------------------------------
The browser must use a developer-authored APPROVED UISpec fixture
with a complete matching synthetic GroundedContext.
Developer authorship alone does not establish approval.
The existing Python preparation step must validate every fixture
before the application loads its generated fixture catalogue.

The Task 5 flow is:
Developer-authored UISpec + matching synthetic context
                ↓
Existing Task 3 Python validator during preparation
                ↓
Generated fixture data + retained verification evidence
                ↓
Privately issued ApprovedUISpec handle
                ↓
ControlledRenderer → explicit registry → React → browser

There is no live browser-to-Python validation transport.
Do NOT pass raw JSON or raw model output directly to the renderer.
A TypeScript cast, brand or approved=true flag is not validation.
VALID means presentation validation, never board quality approval.

--------------------------------------------------
1. INSPECT THE CURRENT REPOSITORY
--------------------------------------------------
Inspect branch, HEAD, git status and existing changes. Read the
Task 4 report and actual files. Do not assume Task 4 is reviewed,
committed or checkpointed. Preserve unrelated work. Report Git
failures without repair. Do not copy the tutorial's commit ID.

--------------------------------------------------
2. READ THE EXISTING PROJECT DOCUMENTATION
--------------------------------------------------
Read CLAUDE.md, README.md, docs/business-problem.md,
docs/architecture.md, specs/spec.md and specs/model-contracts.md.
Read specs/schemas/ui-spec.schema.json and its schema notes.
Compare the preserved alternative specs/ui-spec.schema.json.
Read specs/TASK-3-READINESS.md, TASK-3-IMPLEMENTATION-REPORT.md
and TASK-4-IMPLEMENTATION-REPORT.md under specs/.
Read apps/ui/README.md, source, fixtures, scripts and tests;
services/domain/ validator files and README; tests/README.md;
tests/validator/ and tests/renderer_fixtures/; evals/README.md.
Consult Documents/Business Requirements Document.docx and the
board architecture/guides for business context, not new UI props.
Do not assume docs/walkthrough.md or schemas/README.md exists.

--------------------------------------------------
3. TASK 5 OBJECTIVE
--------------------------------------------------
Make the existing controlled renderer verifiably runnable in a
real browser using the synthetic board-inspection landing page.
The application must load a verified catalogue fixture, obtain its
approvedFixture handle, pass it to ControlledRenderer and display
the resulting React UI. This is a technical rendering demonstration.
It is not a complete inspection product.

Describe the current browser entry point, approved-input path,
verification gaps and any proposed file changes before editing.
If the current UI already meets a requirement, verify and reuse it.
Stop on a required unresolved contract decision; do not invent one.

--------------------------------------------------
4. APPROVED UISPEC FIXTURE
--------------------------------------------------
Use specVersion "1.0", page "landing", contextId and blocks.
Keep specs/schemas/ui-spec.schema.json as the selected authority.
Do not change either schema, merge their bounds or import v0 shapes.
The vocabulary is exactly Hero, Heading, Text, FeatureCard,
FeatureGrid, CTA, Alert, InfoPanel and ProgressIndicator.
Hero and InfoPanel do not contain child components. FeatureGrid
has 2..6 FeatureCard props objects. Alert is an ordinary component;
v1 defines no refusal variant. ProgressIndicator uses metricId,
label and numeric value, not steps/current or a reference-only shape.

Prefer the existing overview fixture for the browser and minimal
fixture for a focused application test. Retain complete matching
contexts. If a real gap needs a new fixture, add a paired context
and include it in the existing fixed preparation catalogue.
Do not relabel synthetic values as live production results.

--------------------------------------------------
5. FIXTURE VALIDATION
--------------------------------------------------
Reuse apps/ui/scripts/prepare_fixtures.py and existing command gates.
Preparation must pass before dev, test and build load application
data. Preserve failure cleanup and verification evidence.
Do not duplicate JSON Schema or grounding logic in React.
Do not manually edit src/generated/fixtures.ts.

--------------------------------------------------
6. REACT APPLICATION STRUCTURE
--------------------------------------------------
Work inside apps/ui/. Reuse index.html, vite.config.ts, src/main.tsx,
src/style.css, package.json and the dependency lockfile.
Create or extract App.tsx only if a demonstrated testability need
justifies it; no file split is required merely to match a tutorial.

--------------------------------------------------
7. APPLICATION ROOT
--------------------------------------------------
Mount the existing ControlledRenderer with an approvedFixture
handle and developer-owned callback. Keep raw JSON, arbitrary paths,
query-string payloads, uploads and model output out of the entry.
Keep the error boundary and the notice outside fixture-authored text.
Do not bypass the registry with hard-coded inspection components.

The existing integration is conceptually:
<ControlledRenderer
  page={approvedFixture('overview')}
  onAction={() => { /* Inert synthetic demonstration. */ }}
/>

Use the actual existing imports and API; do not create another path.

--------------------------------------------------
8. BOARD DEFECT INSPECTION LANDING PAGE
--------------------------------------------------
Show the synthetic inspection landing page. Preserve sibling order,
text, metric strings, units and supplied progress values.
Use semantic headings, visible severity and accessible controls.
Apply only necessary developer-authored CSS corrections.
Do not add charts, line filters, image overlays or new components.

--------------------------------------------------
9. STYLING
--------------------------------------------------
Keep styling minimal, readable and developer-authored.
Reuse src/style.css. Correct only demonstrated readability,
spacing, grid layout, severity visibility, focus or responsive gaps.
Make headings and actions easy to identify. Preserve supplied text,
metric strings, units and progress values.
Do not add a design system or unnecessary styling dependencies.

--------------------------------------------------
10. CTA BEHAVIOUR
--------------------------------------------------
Use only the existing five action IDs available in context:
view-inspection-queue, view-defect-reports, view-ingest-activity,
open-documentation and contact-support.
Hero labels come from matching context action bindings; CTA uses
its supplied label. Tests may record identifiers. Demo clicks must
not navigate, call APIs or change inspection data.

--------------------------------------------------
11. DETERMINISTIC APPLICATION BEHAVIOUR
--------------------------------------------------
Keep fixed fixture identity, locale and timestamps. Do not introduce
randomness, time-driven copy, external data or generated code.
Confirm repeated rendering and clicks leave input data unchanged.

--------------------------------------------------
12. TESTING
--------------------------------------------------
Inspect existing coverage before adding tests. Verify application
mounting, use of ControlledRenderer, the synthetic/inert notice,
expected fixture content and harmless actions. Test error handling
only through an isolated test mechanism, never a production bypass.
Retain existing unknown/inherited-name, DOM safety, determinism
and non-mutation coverage. Do not chase a tutorial test count.

--------------------------------------------------
13. BROWSER RUNNABILITY
--------------------------------------------------
Start npm run dev from apps/ui and use the printed local URL.
Observe the rendered page, console and network activity. Confirm
the notice, expected components, inert controls, keyboard focus
and basic narrow/wide viewport usability. Record browser, URL,
observations and a screenshot when available.
An HTTP 200 or HTML shell alone is not proof React rendered.
If browser access is unavailable, report that check as unverified.

Reuse the existing dev and build scripts. Install locked dependencies
with npm ci only when necessary. Report the actual run commands.
Do not claim npm run preview exists without inspecting package.json.
Keep background helper windows hidden on Windows.

--------------------------------------------------
14. DEPENDENCY DISCIPLINE
--------------------------------------------------
Inspect available runtimes and the existing lockfile. Prefer npm ci
when installation is necessary. Do not copy old tutorial versions.
Add no new library unless a demonstrated Task 5 need requires it.
No AI SDK, backend, database, auth or large UI framework belongs here.

--------------------------------------------------
15. SECURITY BOUNDARY
--------------------------------------------------
Preserve Task 4's approved-handle and fixed-registry boundary.
Keep explicit DOM props, React text rendering and developer-owned
callbacks. Reject unsupported entries for the whole page.
Inherited names such as constructor, toString and __proto__ must
not resolve through the registry.
Do not use eval(), Function(), arbitrary HTML injection, generated
JavaScript, fixture-driven dynamic imports or component lookup.
Preserve existing safety lint checks and runtime coverage.
The error boundary is not a model-repair or fallback UISpec loop.
No dangerouslySetInnerHTML or model-prop spreading onto DOM.
Do not skip, substitute, relabel or repair unsupported components.
Do not introduce new validator rejection codes.

--------------------------------------------------
16. DO NOT CHANGE THE MODEL CONTRACT
--------------------------------------------------
Preserve specs/model-contracts.md, the selected
specs/schemas/ui-spec.schema.json, the alternative schema and
the existing TypeScript UISpec types and validator API.
Do not merge schema bounds or import the onboarding v0 contract.
If a genuine inconsistency blocks Task 5, STOP and report:
1. The inconsistency.
2. The files and contract rules involved.
3. Why Task 5 cannot safely proceed until it is resolved.
Do not silently change the contract.
Quality and Manufacturing own defect definitions and ratio policy.
Do not calculate a new defect ratio or infer missing production data.
Any new metric must originate in supplied context. Keep future
architecture separate from implemented scope.

--------------------------------------------------
17. DOCUMENTATION
--------------------------------------------------
Update documentation only as needed to explain browser readiness,
the synthetic fixture/context pair, offline Python preparation,
approved-handle issuance, controlled rendering and local commands.
Record Task 5 work in specs/TASK-5-IMPLEMENTATION-REPORT.md.
Clearly distinguish fresh results from historical Task 4 evidence.
Do not assume docs/walkthrough.md exists or rewrite earlier guides.
Do not present this proposed prompt as completed implementation.
Record what already existed, what changed and how to reproduce it.
Update apps/ui/README.md only where behaviour or commands changed.

--------------------------------------------------
18. VERIFICATION
--------------------------------------------------
After implementation, run and record exact commands and results:
1. Focused Task 5 application checks.
2. Existing Task 4 renderer regression checks.
3. Task 3 Python validator and fixture-handoff regression checks.
4. Existing Task 2 schema verification checks.
5. Strict TypeScript, safety lint and production build checks.
6. Real-browser rendering, interaction, console and network checks.

From apps/ui, use the existing commands:
npm test
npm run typecheck
npm run lint
npm run build
npm run dev

From the repository root, use the available project environment:
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check

Report schema parsing, meta-validation and instance checks separately.
Distinguish JSON parsing, Draft 2020-12 meta-validation, schema
instance validation and full runtime validation.
Report failures and unavailable checks honestly. Historical test
counts are not fresh results or targets. HTTP 200 alone is not
evidence of successful React rendering.

--------------------------------------------------
19. ARCHITECTURAL VERIFICATION
--------------------------------------------------
Confirm explicitly that:
- The existing Task 4 ControlledRenderer and registry are used.
- Fixtures and matching contexts pass Python preparation.
- Only privately issued approved handles reach the renderer.
- Raw JSON and raw model output are not accepted at the entry point.
- Synthetic values and inert controls remain clearly identified.
- No runtime AI, FastAPI, authentication or persistence was added.
- No defect inference, live ratio service or approval workflow was added.
- No production infrastructure or alternative rendering path was added.
- No arbitrary component or generated-code execution was introduced.

The future model flow remains a separately scoped proposal:
AI model → raw UISpec → deterministic validation → approved input
→ controlled renderer → approved React components → browser.
Do not implement that future integration in Task 5.
No domain-data access, camera/edge/PLC/MES integration, classifier,
review/override workflow, retry/repair or fallback UISpec integration.
No onboarding, registration, document upload or risk scoring.
Local Vite asset/HMR traffic is expected; external/domain/model
requests and live validator transport are outside this task.

--------------------------------------------------
20. REVIEW THE DIFF
--------------------------------------------------
Before finishing, run:
git status
git diff --stat
git diff

Review every changed file and any new untracked Task 5 files.
Confirm changes are limited to Task 5. Preserve unrelated work.
Do not clean up historical code or repair Git failures implicitly.
Report exact Git errors. Separate existing changes from Task 5
changes and generated artifacts.

--------------------------------------------------
21. IMPORTANT STOPPING RULE
--------------------------------------------------
Do NOT commit. Do NOT push. Do NOT start Task 6.
Do NOT integrate the AI model, FastAPI or a model gateway.
Stop after Task 5 implementation and verification.

Report:
1. What was implemented
2. Files created
3. Files modified
4. Approved UISpec fixture and matching context design
5. Application structure
6. Renderer integration
7. Browser run instructions
8. Tests added
9. Task 5 test results
10. Task 4 regression results
11. Task 3 regression results
12. Task 2 schema verification results
13. Build and real-browser verification results
14. Dependencies added
15. Security and control verification
16. Architectural issues and unverified checks
17. Current Git status
18. Recommended next smallest task

Wait for human review before proceeding further.
```

## 5. Expected Implementation Result

Task 5 should establish reproducible real-browser evidence for the existing synthetic landing page and close only demonstrated readiness gaps. Reuse the Task 4 application, renderer, paired fixtures and Python preparation. This is an expected outcome; implementation and browser verification have not been performed by this document edit.

## 6. Existing Files and Possible Additions

Reuse the existing application structure:

```text
apps/ui/
  index.html
  vite.config.ts
  package.json
  package-lock.json
  src/
    main.tsx
    style.css
    approved.ts
    render.tsx
    registry.ts
    components/
    generated/fixtures.ts        ignored preparation output
  fixtures/
    *.spec.json / *.context.json retained paired inputs
    verification.json            retained validation evidence
  scripts/                       existing preparation and lint checks
  tests/renderer.test.tsx        existing deterministic coverage
```

A focused `apps/ui/tests/app.test.tsx` and a future `specs/TASK-5-IMPLEMENTATION-REPORT.md` are possible additions if Task 5 is authorized. A new `App.tsx` is conditional, not a required artifact. Do not create another top-level `ui/` or `domain/` directory.

## 7. Files That May Need Modification

The future change list depends on observed gaps. Likely candidates are application tests, minimal presentation corrections and run documentation. Package scripts or dependencies should change only when existing tooling cannot support a required check.

The selected schema, alternative schema, v1 props, validator API and original fixtures should remain unchanged unless an independently resolved inconsistency requires otherwise. Preserve all unrelated working-tree changes. This adaptation itself creates only the board guide, its editable Word version and its document generator.

## 8. Fixture Design

| Existing fixture | Purpose | Board-contract detail |
| --- | --- | --- |
| minimal | Small browser/application example | Hero, Text and CTA are sibling blocks; contextId is task4-demo. |
| overview | Existing browser demonstration | Exercises all nine component types, including normal Alert, metric rows and percentage progress. |
| grid-six | Upper grid boundary | Six FeatureCard props objects in supplied order. |
| actions | Action callback coverage | All five actions exercised by Hero and CTA. |
| headings-alerts | Semantic presentation | Heading levels 2/3 and visible info/warning/critical severity. |

Every fixture has a complete synthetic context: contextVersion, contextId, page, locale, generatedAt, capabilities, defectCategories, metrics, alerts and actions. Referenced identifiers and values must match that context. Use the actual checked-in files rather than copying an illustrative JSON example without its context.

The broader dashboard ambition includes per-line counts, defect ratios, trends and image evidence. These are future requirements. A fixed supplied metric can be displayed through InfoPanel; Task 5 does not introduce a ratio calculation, live line comparison or a chart component. Quality must settle counting, reinspection, pending review and denominator policies before a real ratio service is implemented.

## 9. Renderer Integration

The existing application concept is:

```tsx
<ControlledRenderer
  page={approvedFixture('overview')}
  onAction={() => { /* Inert synthetic demonstration. */ }}
/>
```

`main.tsx` mounts this through React's existing root. `approved.ts` supplies a handle for a verified catalogue item. `render.tsx` performs whole-page preflight and uses `registry.ts` to resolve the components. FeatureGrid cards use the same registry entry. Application-shell notices and the error message are developer-owned; they do not bypass the renderer for inspection content.

The generated fixture module is not a place to author fixtures. Preparation recreates it from validated inputs and retains hashes of the selected schema, validator sources, UISpec and context. Hashes document provenance, not authentication or a browser trust protocol.

## 10. Architectural Observation: Ordered V1 Blocks

Our v1 contract supports an ordered `blocks` array, so Hero, Heading, Text, FeatureGrid and InfoPanel can already be siblings in one page. The tutorial's workaround of stacking several single-root v0 specifications is unnecessary and must not be imported.

Hero and InfoPanel have no child components. InfoPanel rows are data; FeatureGrid items are card props. Alert is a normal component, not a refusal response. ProgressIndicator represents a supplied 0-100 value grounded in a context metric with unit `%`. No root/children, generated_for, steps/current or legacy refusal shape is accepted.

Task 3 and Task 4 selected `specs/schemas/ui-spec.schema.json`. The alternative `specs/ui-spec.schema.json` remains unused. The selected copy permits contextId/reference bounds of 256, InfoPanel value 256 and unit 32; the alternative has 128/64/40/12 and different identifier restrictions. Hero-action and Alert-category structural checks also differ. The selected value description contradicts its maxLength; the actual keyword is enforced. Task 5 preserves this explicit selection rather than reconciling the files silently.

## 11. Tests and Verification Evidence

| Verification | Required Task 5 evidence | Status in this adaptation |
| --- | --- | --- |
| Application path | Mount, expected page content, notice and inert controls | Not executed |
| Renderer regression | Actual current UI test output | Not rerun |
| Python regression | Validator and fixture-handoff results from root | Not rerun |
| Schema checks | Parsing, meta-validation and instance checks identified separately | Source inspected only |
| Safety and typing | ESLint/prohibition probes and strict TypeScript | Not rerun |
| Build | Successful current static application build | Not rerun |
| Real browser | Browser/version, URL, rendered-page observation, console/network checks | Not performed |

Historical evidence is available in the Task 4 report: 29 renderer tests, 167 Python tests including the original 163 validator tests and four handoff checks, build/typecheck success and safety lint probes. These are historical results, not fresh Task 5 results or a required test-count target.

The existing schema test parses the selected JSON, calls Draft202012Validator.check_schema, checks vocabulary coverage, validates the contract example against the schema and passes it through the runtime validator with fixed context. The alternative schema is not automatically covered. An HTTP response only proves resource delivery; browser execution, component rendering and interaction require separate observation.

## 12. Browser Run Instructions

These commands describe the existing workflow. They were not executed as part of this document conversion. Inspect available environments before creating or installing anything.

From the repository root, only if the virtual environment/dependencies are missing:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
```

From `apps/ui`, install locked dependencies when necessary and start the demonstration:

```powershell
npm ci
npm run dev
```

Open the URL Vite actually prints; the script binds to 127.0.0.1. Do not claim a particular port was verified before observing it. Retain the synthetic/inert-control notice and confirm no unexpected console error or domain/model request. Restart the dev server after fixture changes so preparation runs again. Local asset requests and development HMR are expected.

Verification commands from `apps/ui`:

```powershell
npm test
npm run typecheck
npm run lint
npm run build
```

Verification commands from the repository root:

```powershell
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check
```

The current package has no `preview` script. Do not copy `npm run preview` from the tutorial as if it already exists. If a future Task 5 needs one, justify and document the minimal addition. When launching any background helper on Windows, keep its window hidden; leave a visible browser only when needed for interactive inspection.

## 13. Dependency Discipline

This documentation adaptation adds no application dependency. The repository already pins React/react-dom 19.3.0, TypeScript 6.0.3, Vite 8.3.0, Vitest 5.0.1, JSDOM 30.1.1, ESLint 10.11.0 and typescript-eslint 8.70.1, with supporting type packages and a lockfile. These are observed repository pins, not a recommendation to upgrade or a claim they are the latest releases.

Reuse the installed compatible tooling. Do not import the onboarding tutorial's Vite 5, React plugin or Node type versions. Do not add an Agent SDK, model client, state-management framework, database library or authentication dependency for this browser milestone.

## 14. Security and Control Verification

Verify that the application uses issued handles, retains fresh Python fixture preparation, resolves all content through the fixed registry and rejects a whole page with unsupported entries. Inherited names such as constructor, toString and __proto__ must not resolve.

Keep explicit DOM props, React text rendering and developer-owned action callbacks. Preserve lint prohibitions and runtime tests against executable strings, arbitrary HTML and module selection. A rendered VALID fixture is not a proof of unrestricted natural-language semantics or a manufacturing quality certification.

The demo's error boundary is an application error display. It is not the future validated fallback UISpec or a model-repair loop. Hooks, skills, plugins and agent harnesses from the broader project discussion are not automatically configured or introduced by Task 5.

## 15. Why This Milestone Matters

Browser verification establishes that the existing offline-approved data path works as a visible application, not just as a component test or a generated HTML shell. It allows UI problems to be investigated before adding probabilistic model behaviour or live services.

For the manufacturing organization, this is a controlled demonstration of presenting inspection information. It does not establish image-model accuracy, throughput, line coverage, approved defect-ratio definitions or production readiness. Those need their own data, specifications, acceptance evidence and Quality/Manufacturing decisions.

## 16. What Task 5 Does Not Build

- Runtime AI generation, model gateway, Agent SDK integration or model evaluations.
- FastAPI runtime, domain API, live data access or a live validator-to-browser transport.
- Camera capture, edge inference, defect classification, PLC/MES integration or physical actuation.
- Defect-ratio aggregation, new chart components, live line filters or image evidence viewers.
- Board approval, disposition, human override or manufacturing review workflows.
- Authentication, persistence, production deployment or infrastructure.
- Model retries, repair, fallback orchestration or a feedback/training loop.
- Customer onboarding, registration, document processing or risk scoring.

## 17. Documentation, Adaptation and Checkpoint Status

This guide retains the source's 18-section learning structure and a 21-part implementation prompt, while replacing the onboarding assumptions with board-project scope. The main corrections are the existing browser shell, v1 ordered blocks, actual directory paths, normal Alert semantics, context-backed fixtures and real runtime handle boundary.

Source: `Documents/Customer_Onboarding_Task_5_Beginner_Guide_Enterprise_Standard.docx`. Board references: the BRD, initial engineering discussion, end-to-end workflow, Task 3/4 guides, rules guide, current specifications, `apps/ui/README.md` and `specs/TASK-4-IMPLEMENTATION-REPORT.md`. Broad architecture proposals do not override the current contract.

No onboarding commit, checkpoint, success count or dependency version is presented as board-project evidence. The source guide is preserved. The companion Markdown is the editable content source; the Word document uses a clean US Letter layout with source-equivalent margins. Exact source pagination is not claimed. Document package/content checks are separate from application tests and browser verification.

When Task 5 is separately authorized, report these 18 items: implemented work; files created; files modified; fixture/context design; application structure; renderer integration; run instructions; tests added; Task 5 results; Task 4 regression; Task 3 regression; schema checks; build/browser evidence; dependencies; control verification; unresolved issues; current Git state; and the smallest next step. Do not commit, push or begin the next task without that later instruction.

## 18. One-Sentence Summary

Task 5 verifies and completes the existing board-inspection browser demonstration using Python-validated synthetic fixtures and the Task 4 controlled renderer, without introducing live models, backend integration or manufacturing decisions.
