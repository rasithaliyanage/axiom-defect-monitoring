# BOARD DEFECT INSPECTION AI
@ Master Beginner Teaching Walkthrough
@ From AI-Native Engineering Foundations to the Domain Runtime Boundary
@ Enterprise-Grade Engineering Guide | Task 6 Checkpoint Candidate

**Purpose:** This is the chronological teaching companion to the Board Defect Inspection AI repository. It connects the business problem, specification, harness design and Tasks 1–6 to the actual artifacts. It explains what each task contributes, how it is checked and what deliberately remains outside its scope.

**Core principle:** AI proposes; deterministic software decides what is allowed to proceed. Here, “allowed” concerns presentation. It never means a board is approved, conforming or safe to ship.

**Document date:** 2026-10-03. **Current observed branch:** wushan. **HEAD:** 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da. Task 6 is implemented locally with retained verification evidence; its formal Git checkpoint is pending. This documentation task did not rerun the application tests, commit, push or start Task 7.

Read top to bottom once; then use the numbered sections as a teaching reference. Repository contracts and code remain authoritative. Documents/ holds learning guides and historical proposals; docs/ holds current business/architecture documentation. Neither a tutorial tree nor an old prompt authorizes changing the current contract.

**Reference and adaptation:** The requested source is available as Customer_Onboarding_AI_Walkthrough_Task_6_Checkpoint_Updated.docx.pdf, a 64-page export. This guide preserves its 48-section learning spine, ASCII mental models, artifact trees and task deep dives. Task 5 and Task 6 are integrated into sections 38 and 39, avoiding the source's stale “not implemented” statements alongside appended implementation claims. The reference remains unchanged.

**Prompt record:** Complete prompt blocks from the six existing board guides are preserved below without rewriting their content. “Verbatim” means identical to those stored blocks, with line endings normalized, not independently proven to be the exact historical agent transcript. Task 1 explicitly says proposed; Task 3 contains superseded refusal/progress assumptions. Those are archival teaching evidence, not current execution instructions. Later readiness decisions and actual reports govern implemented behaviour. The embedded historical prompts are not instructions to execute during this documentation task.

## 1. Canonical Learning Sequence

| Order | Read / inspect | Learning purpose |
| --- | --- | --- |
| 1 | Documents/Business Requirements Document.docx; docs/business-problem.md | Understand inspection visibility and manufacturing ownership |
| 2 | Documents/AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md | Connect specifications, agent guidance and enterprise scope |
| 3 | docs/architecture.md; Documents/SOLUTION_ARCHITECTURE_MERMAID.md | Separate implemented runtime responsibilities from future topology |
| 4 | Documents/AI_NATIVE_GENERATIVE_UI_FIRST_IMPLEMENTATION.md | Understand the proposed first slice; compare its historical scope with current landing v1 |
| 5 | CLAUDE.md, README.md, specs/spec.md | Establish engineering rules, orientation and system requirements |
| 6 | specs/model-contracts.md and selected schema | Learn Task 2's machine-checkable representation |
| 7 | Task 3 readiness/report and services/domain/ | Learn grounding, diagnostics and deterministic rejection |
| 8 | Task 4 report and apps/ui/ | Learn verified fixtures, private handles and controlled rendering |
| 9 | Task 5 report and browser evidence | Learn application mounting and real-browser verification |
| 10 | Task 6 readiness/report and API files | Learn the first local HTTP boundary |
| 11 | Board Task 6 checkpoint guide | Review evidence and unresolved Git checkpoint work |

```text
Business problem -> requirements -> specification
   -> architecture -> model contract -> harness controls
   -> Task 1 foundation -> Task 2 schema
   -> Task 3 validator -> architecture/readiness review
   -> Task 4 renderer -> Task 5 browser readiness
   -> Task 6 local Domain API -> human review
   -> formal checkpoint (pending)
   -> future separately authorized AI/eval increments
```

The conceptual sequence explains why the implementation tasks exist. It does not establish one Git commit per task. A missing checkpoint cannot be inferred from an implementation report.

## 2. The Business Problem

A manufacturing organization receives motherboard images from operational lines and wants a reliable dashboard of inspection activity and defect ratios. Operators need recorded queue information, supervisors need visibility across shifts and lines, and Quality engineers need traceable defect reports. Disconnected image records and inspection summaries make these questions difficult to answer consistently.

The business aspiration includes acquisition, inspection evidence, defect definitions, aggregation and reporting. These are separate responsibilities. Counting defective boards versus counting defect occurrences produces different ratios; treatment of repeat inspections, sampling and time windows also matters. Quality and Manufacturing must define that policy before a ratio service is implemented. This walkthrough does not invent a formula or classify any image.

```text
BUSINESS ASPIRATION — mostly future scope
Operational lines -> motherboard images -> inspection evidence
 -> qualified defect definitions / ratio policy
 -> grounded recorded metrics -> dashboard presentation

CURRENT TECHNICAL SLICE
Synthetic recorded context + authored landing UISpec
 -> validation -> controlled API/React presentation
```

The current page demonstrates exact rendering of supplied data, not image-based defect inference. Its synthetic numbers, including deliberately formatted metric strings, are test data and cannot be used as evidence of factory performance.

## 3. From Specification-Driven Engineering to AI-Native Engineering

Specification-driven work starts with the problem, turns it into explicit requirements and contracts, then builds and verifies small changes. AI-native engineering adds controls around probabilistic proposals and measures model behaviour separately from deterministic code behaviour.

```text
ENGINEERING TIME
Human intent -> coding agent -> repository edits
            -> tests / review / feedback -> controlled change

APPLICATION RUNTIME TODAY
Browser -> Domain API -> fixed synthetic pair -> validator
        -> admitted response -> renderer -> browser

FUTURE MODEL RUNTIME
Server-owned grounding -> model proposal -> deterministic gates
                      -> separately reviewed transport -> renderer
```

Claude Code or another coding agent is an engineering-time collaborator. It can inspect files and run authorized commands. It is not the application model, and its tool permissions must not be transferred to runtime content. Future presentation generation and future image defect classification are also distinct capabilities; neither is implemented by Task 6.

## 4. Key Vocabulary

| Term | Meaning in this project |
| --- | --- |
| UISpec | v1 JSON data describing ordered landing-page blocks; never executable code |
| Model contract | specs/model-contracts.md defines allowed output, grounding references and policy |
| JSON Schema | Structural rules in specs/schemas/ui-spec.schema.json, Draft 2020-12 |
| GroundedContext | Complete server-owned context defining available actions, metrics and other facts |
| Deterministic validator | Python checks structure plus grounding/cross-field/policy rules |
| VALID | Implemented presentation validation passed; not a quality decision |
| ApprovedUISpec handle | Privately issued, frozen object associated with accepted data in a WeakMap |
| Component registry | Fixed developer-authored mapping to nine React implementations |
| Controlled Generative UI | A future model may propose data within a closed vocabulary; software controls rendering |
| Harness engineering | Instructions, permissions, tools, validation, tests and feedback around engineering work |
| Deterministic test | A repeatable assertion on code and fixed inputs |
| AI eval | Measurement of probabilistic model behaviour; no live eval run is claimed here |
| Checkpoint | A reviewed, verified and explicitly recorded code milestone; local completion alone is insufficient |

CLAUDE.md provides guidance and context. It does not itself enforce runtime safety. The Python validator, registry, private issuance, lint checks and tests provide concrete controls with documented limits.

## 5. Architecture: Practical Deployment and Runtime Responsibility Views

```text
PRACTICAL LOCAL VIEW
Browser
  -> Vite / React at 127.0.0.1:5173
     -> narrow development proxy
        -> FastAPI / Python at 127.0.0.1:8001
           -> repository-local fixed spec/context

RESPONSIBILITY VIEW
UI RUNTIME       DOM, accessibility, loading/error states,
                 private admission, registry and rendering
DOMAIN RUNTIME   HTTP, fixed context ownership, validation,
                 exact snapshot and action-binding response
AI RUNTIME       FUTURE: gateway/model; currently absent

ENGINEERING ENVIRONMENT (not another deployed runtime)
Specifications + agent instructions + tools + test gates
 + retained evidence + human review
```

These views answer different questions. Frontend/backend describes where code runs; runtime roles describe what it may do. A future AI module could live inside the Domain service while retaining a separate responsibility boundary. No production deployment design is implemented here.

## 6. The First Implementation Scenario

The implemented first slice is a synthetic inspection landing page with a Hero, heading, explanatory text, cards, an inert report action, visible alert severity, recorded metric rows and percentage progress. It is intentionally small enough to trace each displayed value back to a fixed context.

```text
Board inspection activity
Inspection records and defect reporting.
[ View inspection queue ]  (inert)

Recorded information
Inspection records / Image records / Defect reports
[ Open defect reports ]   (inert)
Info: Recorded activity
Recorded images: 0012.50 images
Recorded progress: 37.125 %
```

This sketch summarizes the existing overview fixture, not a replacement design. The unusual image-count string is deliberately synthetic fidelity-test data. The renderer must preserve it; it must not normalize it into an invented operational figure. Historical inspector-review-panel proposals are not implemented workflows.

## 7. Controlled Data Versus Free-Form Executable Code

The future model may select approved blocks and supply grounded text. It cannot supply React functions, HTML, scripts, CSS, SQL, shell commands or destinations. The components already exist and are written by developers.

```json
{
  "specVersion": "1.0",
  "page": "landing",
  "contextId": "example-context",
  "blocks": [
    {"component":"Text","props":{"text":"Inspection activity"}}
  ]
}
```

This is an illustrative shape, not a newly approved fixture. A matching complete context and actual Python validation are still required. A component name in JSON selects only an existing registry entry after validation and issuance; it never selects a module to import.

## 8. The Trust Boundary

```text
PROPOSAL DATA (future model output or current authored fixture)
                    |
                    v
Schema + Python grounding / deterministic policy
                    |
          INVALID --+--> reject; no repair
                    |
                  VALID
                    v
Approved handoff appropriate to the increment
 -> private handle -> ControlledRenderer -> fixed registry
 -> developer components -> browser
```

Conceptually the renderer accepts render(approvedUISpec), never render(rawAIOutput). Task 3 can inspect raw JSON, but the React renderer cannot. At Task 6, both server validation and complete fixed-response admission are required. A copied object, TypeScript cast, brand, approval flag or HTTP 200 is not validation. Neither handles nor recorded hashes are cryptographic authentication.

## 9. Task 1 — Establish the Project Foundation

Task 1 separates the business why, system what, architecture how, model permissions and engineering instructions. The repository now contains foundation artifacts; their existence does not prove that the preserved proposed prompt was executed word for word.

**Exact Execution Prompt Used — provenance:** The following is copied verbatim from the prompt block in Documents/AI_NATIVE_TASK_1_PROJECT_FOUNDATION.md. That guide explicitly marks it proposed. It contains historical inspector-review-panel language; current landing-page v1 is authoritative. Do not execute it against the current repository as a new foundation task.

```prompt
We are building an AI-Based Automated Board Defect Inspection System.
Inspect this repository first. If it is not empty, preserve existing work
and adapt the foundation to its current structure.

Do NOT build the application yet.

First, establish the project engineering foundation for an AI-native,
model-driven application.

The first implementation scenario is intentionally small and READ-ONLY:
an inspector review panel using controlled Generative UI, rendered over a
RECORDED inspection fixture. No camera, no PLC, no live inference.
Nothing in this first slice may change the state of a board.
ReviewPanel fields are non-submitting; EscalationNotice routes nothing.
No live inspection inference is needed; UI composition model integration
is a later implementation task, not part of this foundation.

The runtime AI model will generate a structured UI specification, not
executable code. The application will validate that output and render it
only through an approved component vocabulary.

SOURCE DOCUMENTS — read before proposing anything:
- AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md
- AI_NATIVE_GENERATIVE_UI_FIRST_IMPLEMENTATION.md
- Business Requirements Document (discovery status, 25 open questions)
- The proposed eleven-layer architecture (marked "validation required")

CRITICAL CONSTRAINT ON BUSINESS RULES:
The BRD is a discovery document. Defect taxonomy, severity classification,
thresholds, recall targets and ground truth are owned by the Quality and
Manufacturing teams and are NOT yet decided.
Create policies/ files as structured placeholders that name the owning
team and the source question. Do NOT fill in plausible values. Do NOT
substitute industry-standard defaults. An invented threshold that looks
reasonable is worse than an empty one.

Create the following project foundation:
 1. CLAUDE.md
 2. README.md
 3. docs/business-problem.md
 4. docs/architecture.md
 5. docs/quality-gates.md
 6. docs/adr/0001-record-architecture-decisions.md
 7. specs/spec.md
 8. specs/model-contracts.md
 9. specs/ui-contract.md
10. policies/            (placeholders with named owners)
11. contracts/ui/
12. simulators/capture/
13. tests/
14. evals/
15. .claude/

Use README.md placeholders to retain otherwise empty directories in Git.
Document the fixture format and provenance requirements now; adding the
actual recorded fixture belongs to a later implementation task.

Create ONLY the directories the first slice needs. Do not scaffold
edge/, enterprise/, ml/, ops/, infra/ or ci/ yet — those arrive when a
slice needs them.

The documentation must clearly distinguish:
- Business requirements      docs/
- Business-owned policy      policies/      (different owner)
- System specification       specs/spec.md
- Model contract             specs/model-contracts.md
- Shared schemas             contracts/
- Claude Code instructions   CLAUDE.md, .claude/
- Deterministic tests        tests/
- AI evaluations             evals/

ARCHITECTURE CONCEPTS:

UI Runtime
- Role-aware views for operators, inspectors and managers
- Approved component catalogue
- Generative UI renderer with schema and permission validation
- Standard fallback UI

Domain Runtime
- Review API surface (human-facing, attributed actions)
- Resolves evidence references against the viewer's scope
- Owns all state; nothing else may change a board

AI Runtime
- Model gateway with version pinning
- UI specification generation

The model MAY:
- select and order approved components
- choose which evidence references are most relevant to the case
- generate neutral explanatory and label text
- adapt the layout to the viewer's role
- signal that a case looks ambiguous and may need escalation

The model MUST NOT:
- generate executable code or arbitrary markup
- request components outside the approved catalogue
- supply evidence VALUES instead of references
- state, imply or recommend a disposition
- describe confidence in words that contradict the calibrated score
- invent defect categories outside the approved taxonomy
- access the database, model registry or line equipment

APPROVED COMPONENT VOCABULARY (v1):
BoardSummary, ImageCompare, DefectOverlay, ConfidenceBadge,
ReviewPanel, Heading, Text, Alert, EscalationNotice

DispositionControl is deliberately EXCLUDED from v1. A specification
requesting it must be rejected. It arrives in a later slice together with
authentication, attribution and the backend action gateway.

AUTHENTICATION:
Defer a new login subsystem only for the isolated fixture demonstration.
Use an explicit simulated viewer role/scope; it is not authentication.
Do not expose protected production evidence on this basis.
Record in docs/adr/ that authentication, authorization and attribution
are required before any disposition can be submitted.

TECHNOLOGY STACK:
This is an OPEN DECISION. The delivery backlog names one stack; the BRD
defers infrastructure entirely. Do not treat either as settled. Keep the
foundation stack-neutral and record the decision in docs/adr/ once made.

DO NOT implement yet:
live image capture, edge inference, quality gates QG-1 to QG-4,
calibration, risk scoring, the decision path, disposition or override,
PLC/MES integration, model training or retraining, audit retention,
or deployment infrastructure.

Do not over-engineer the project.

Before creating files, inspect the repository and propose the structure
you intend to create.
Then create the foundation.
After creating the files, explain what was created, list every open
question you encountered, and identify the next smallest implementation
task.
Do not proceed to the next task automatically.
```

```text
axiom-defect-monitoring/
  CLAUDE.md
  README.md
  docs/
    business-problem.md
    architecture.md
  specs/
    spec.md
    model-contracts.md
  tests/README.md
  evals/README.md
  .claude/
```

The tree is the actual foundation subset, not a promise to scaffold all enterprise layers. Verification at this stage is document consistency and explicit ownership. No fresh Task 1 test count or milestone commit is available in this documentation pass. No model, API, database, camera or complete inspection UI was introduced by the foundation concept.

## 10. Task 1 — Model Boundaries

The current vocabulary is exactly Hero, Heading, Text, FeatureCard, FeatureGrid, CTA, Alert, InfoPanel and ProgressIndicator. The future presentation model may choose among these and reference only supplied context. It may not invent facts, capabilities or action identifiers.

The five action identifiers are view-inspection-queue, view-defect-reports, view-ingest-activity, open-documentation and contact-support. They are capability identifiers, not URLs. Membership in the vocabulary and availability in the supplied context are separate checks.

Board quality judgments remain outside this model's role. A message that looks like presentation can still imply approval, so deterministic text checks are useful but do not establish complete semantic safety. Human/domain ownership must remain explicit.

## 11. Task 1 — The Beginning of a Harness

```text
Project context + contracts + scoped agent task
 + repository permissions + deterministic validation
 + build/lint/tests + evidence + human review
 = engineering environment around the coding agent
```

Rules and CLAUDE.md describe expectations. Hooks can enforce repeatable checks when actually configured. Skills package reusable procedures. Plugins distribute tools or skills. An agent SDK/harness can orchestrate bounded work when separately authorized. Discussing these six primitives in guides does not mean all are installed or part of this runtime.

The implemented harness elements include Python preparation gates, safety lint probes, schema/grounding validation, fixed fixtures, dependency locks and renderer tests. No agent SDK was added to the board application. The lesson is to inspect enforcement, not equate a written rule with a technical guarantee.

## 12. Task 2 — Formalise the UISpec Model Contract

Task 2 translates structural prose into machine-checkable constraints. JSON Schema provides const, enum, required, additionalProperties, string/array bounds, reusable definitions and discriminated block alternatives.

**Exact Execution Prompt Used — provenance:** The complete stored board prompt below is copied from Documents/BOARD_DEFECT_INSPECTION_TASK_2_PROMPT.md. It is a preserved task instruction, not independent proof of the original execution transcript. Historical ambiguities in it must be read alongside the subsequent current v1 schema and readiness decisions.

```prompt
Proceed with the proposed next smallest task.

Formalise the UISpec model contract for the AI-Based Automated Board Defect Inspection System as a machine-checkable JSON Schema.

Create:
specs/schemas/ui-spec.schema.json

Use JSON Schema Draft 2020-12.

The schema must represent the contract currently defined in:
specs/model-contracts.md

Align with the Business Requirements Document and the current internal, read-only landing-page scope.

Do not redesign the contract or introduce new capabilities.

Before writing the schema:

1. Read:
   - CLAUDE.md
   - Documents/Business Requirements Document.docx
   - docs/business-problem.md
   - docs/architecture.md
   - specs/spec.md
   - specs/model-contracts.md

2. Identify any ambiguity or contradiction between the BRD, the current implementation scope, the prose contract, and what can be represented in JSON Schema.

3. If an ambiguity affects the schema design, document it clearly rather than silently inventing a rule.

4. If required component properties, CTA actions, refusal rules, or constraints are undefined, report the exact contract clarification needed before completing the schema. Do not create a permissive substitute or present an incomplete schema as complete.

The schema must cover:

- UISpec top-level structure
- The exact view value: "landing"
- Context structure and role constraints as defined by the contract
- Required fields
- All approved v1 component types:
  - Hero
  - Heading
  - Text
  - FeatureCard
  - FeatureGrid
  - CTA
  - Alert
  - InfoPanel
  - ProgressIndicator
- Exact case-sensitive component type names
- Component-specific properties
- String length constraints where defined
- Enum constraints where defined
- Required properties
- Additional-property restrictions
- FeatureGrid props.items and child rules
- Hero child/container rules if defined by the contract
- InfoPanel child/container rules if defined by the contract
- CTA action enum/table if defined; otherwise report the missing definition
- Data reference fields and their defined structural constraints
- The normal response components array limit of 1–12 entries
- The documented refusal response, including its empty components array
- Separation between normal and refusal response constraints
- Node-count limits where JSON Schema can express them
- Array size limits where applicable

Preserve the board inspection boundaries:

- The model composes the UI using approved components and user-facing text.
- The model supplies data reference keys; the Domain Runtime resolves actual inspection data values.
- Do not treat example metric or alert keys as an exhaustive allow-list unless explicitly defined.
- Do not add components or actions that produce, display, or imply a final PASS/FAIL or quality approval decision in this slice.
- Do not add human review, override, or board disposition capabilities.
- Do not convert the BRD's illustrative defect taxonomy, suggested severity categories, sample values, or TBD thresholds into approved schema constraints.
- Do not import customer-onboarding page identifiers, actions, or context fields.
- Do not add meta.generated_for, steps, current, or children unless defined by the board inspection contract.

Apply the updated guide's clarifications where supported by the existing contract:

- Restrict Hero children to the explicitly approved types and limits.
- Apply nonempty-string constraints where specified; report undefined constraints.
- Reject undeclared properties using additionalProperties restrictions.
- Keep exact input-context matching as a later validator responsibility.
- If ProgressIndicator defines steps/current, represent its defined static bounds and document the current < len(steps) relationship for later validation.
- Do not introduce campaign or locale fields without a contract definition.

Use JSON Schema capabilities such as:

- $schema
- $defs
- $ref
- type
- enum
- const
- required
- additionalProperties
- minLength
- maxLength
- minItems
- maxItems
- minimum / maximum where defined
- oneOf / anyOf where appropriate

Document rules that require later runtime validation, including:

- Total node count across nested components
- Serialized output size
- Cross-field relationships not conveniently expressible in JSON Schema
- Exact matching to input context
- Membership in available metric, alert, and panel keys
- Data reference resolution
- Authorization and business decision correctness

Do not claim that schema validation can detect invented capabilities or implied quality verdicts in generated text. These require later model evaluations.

Do NOT add application code yet.
Do NOT add runtime dependencies.
Do NOT build the React application.
Do NOT build the FastAPI application.
Do NOT implement the runtime validator or renderer.
Do NOT integrate a UI-generation or defect-detection model.
Do NOT create authentication.
Do NOT create camera integration or image processing.
Do NOT create PLC/MES integration.
Do NOT create review, override, or disposition workflows.
Do NOT create document processing or risk functionality.
Do NOT change the model contract or unrelated files as part of this task.

After creating the schema:

1. Validate that the schema itself is syntactically valid JSON.
2. Check Draft 2020-12 meta-schema validity using available development tooling, and report any verification limitation.
3. Check that every approved v1 component in the model contract is represented.
4. Check that every allowed CTA action is represented.
5. Check that the schema does not accidentally permit arbitrary component types or properties, including inside nested structures.
6. Check that normal and refusal responses are represented correctly.
7. Check that data references remain distinct from inspection data values.
8. Report any contract ambiguity discovered and any rules deferred to runtime validation or model evaluation.
9. Summarize exactly what was created and which checks were performed.

Stop after this task.
Do not proceed to the validator or tests until explicitly instructed.
```

```text
specs/
  model-contracts.md
  schemas/
    ui-spec.schema.json           SELECTED authority
    ui-spec.schema-notes.md
    SCHEMA-VALIDATION-REPORT.md   historical evidence
  ui-spec.schema.json           preserved alternative
Documents/
  BOARD_DEFECT_INSPECTION_TASK_2_PROMPT.md
  BOARD_DEFECT_INSPECTION_TASK_2_FINDINGS.md
  BOARD_DEFECT_INSPECTION_TASK_2_CLARIFICATIONS.md
```

No React, FastAPI or model integration belongs to the schema increment. Current verification is demonstrated by the later schema test inside tests/validator/, not by importing the onboarding tutorial's count.

## 13. Task 2 — What JSON Schema Does and Does Not Do

Schema checks shape: required root fields, permitted component names, explicit props, allowed enums and local bounds. It does not know whether a metric exists in the supplied context or whether a proposed value equals that context's value. Those are runtime relationships.

| Question | Owner |
| --- | --- |
| Is specVersion exactly 1.0 and page landing? | Selected schema |
| Are blocks ordered and within 1..12? | Selected schema |
| Are FeatureGrid items 2..6 card-props objects? | Selected schema |
| Is contextId the supplied context identity? | Python runtime validation |
| Is an action available in this context? | Python runtime validation |
| Is a displayed metric copied exactly? | Python runtime validation |
| Is displayed text within aggregate policy? | Python runtime validation |
| Which React implementation may execute? | Developer registry |

Passing schema structure alone never establishes complete presentation approval.

## 14. Task 2 — Ambiguities and Explicit Decisions

Two schema copies exist with different acceptance bounds. Task 3 loads specs/schemas/ui-spec.schema.json; Task 4's reviewed decision retains that authority. Neither file is silently merged or redesigned to suit React.

| Constraint | Selected schema | Alternative |
| --- | --- | --- |
| contextId maximum | 256 | 128 |
| Generic reference ID maximum | 256 | 64, with additional lowercase pattern |
| InfoPanel value maximum | 256 | 40 |
| InfoPanel unit maximum | 32 | 12 |
| Hero action | Bounded string; runtime approval membership | Approved enum |

The selected InfoPanel value description conflicts with its maxLength keyword; the implementation enforces the keyword. Hero and InfoPanel have no child components. Alert has no refusal variant. ProgressIndicator uses metricId, label and numeric value. Superseded reference-only progress/refusal instructions were explicitly resolved before Task 3 proceeded.

## 15. Task 2 — The Important Mental Model

```text
Written contract -> structural schema -> checkable output shape
                                       |
                                       v
                           still needs supplied context
                           and runtime policy checks
```

A checkable contract does not make the upstream model deterministic. It provides a deterministic boundary around variable proposals. It also does not prove every quality-related implication can be detected by string rules. Structural precision and semantic coverage are different properties.

## 16. Task 2 Checkpoint and Evidence Discipline

The source tutorial has a neat milestone-commit history. This repository's current Git history does not establish those task-specific checkpoints. No source commit ID is copied here. Earlier Task 3 records also reported unreadable Git objects; those historical errors are not current failures now that Git is readable.

The correct sequence is inspect -> verify -> review -> explicitly authorize checkpoint -> commit/push if instructed. A teaching document must not turn historical plans into completed actions. Current Task 6 remains uncommitted with unrelated work present.

## 17. Task 3 — Deterministic UISpec Validator

Task 3 adds the authoritative Python gate. UISpecValidator.validate(spec, context) returns status and deterministic rejections. It does not return a renderer handle, approved payload, repaired output or board quality result.

**Exact Execution Prompt Used — provenance:** The following preserves all six prompt blocks in their original order from Documents/BOARD_DEFECT_INSPECTION_TASK_3_BEGINNER_GUIDE_COMPLETE.md. Only the guide's interleaved explanatory prose is omitted. Historical refusal/reference-progress requirements in these blocks were superseded by the user's v1 confirmation recorded in specs/TASK-3-READINESS.md. This archive must not be replayed as current instructions.

```prompt
We are starting Task 3 of the Board Defect Inspection AI project.
First verify Task 2 readiness; do not assume the partial schema is complete.

IMPORTANT: Do NOT start Task 4.
This task is ONLY the deterministic UISpec validation layer and its tests.
Do not build React or FastAPI applications.
Do not integrate AI or create a model gateway or authentication.
Do not create physical camera integration, edge image processing,
real-time PLC/MES handling, automated defect classification models,
human review/override workflows or production infrastructure.
Do not redesign the contract or invent capabilities or limits.

--------------------------------------------------
TASK 3 OBJECTIVE
--------------------------------------------------
Build a deterministic validator for the approved UISpec model contract.

Raw model output → UISpec validation → Approved UISpec → Future renderer

Return a deterministic VALID/INVALID result for the specification.
This is never a board PASS/FAIL or quality-approval decision.
```

```prompt
--------------------------------------------------
1. READ THE EXISTING PROJECT FIRST
--------------------------------------------------
Before creating or modifying anything, read:
- CLAUDE.md and README.md
- Documents/Business Requirements Document.docx
- docs/business-problem.md and docs/architecture.md
- specs/spec.md and specs/model-contracts.md
- specs/schemas/ui-spec.schema.json
- specs/schemas/ui-spec.schema-notes.md
- Documents/BOARD_DEFECT_INSPECTION_TASK_2_CLARIFICATIONS.md
- tests/README.md and evals/README.md
Read other schema documentation if it exists; do not assume filenames.
The BRD's taxonomy examples and TBD targets are not approved constants.

--------------------------------------------------
2. INSPECT THE CURRENT GIT STATE
--------------------------------------------------
Confirm branch, commit, working tree and repository structure.
Do not use an onboarding tutorial commit as the board-project checkpoint.
Preserve unrelated user changes.
Confirm that component props, child rules, actions if any, runtime checks,
context shape and validation outcomes are fully defined and approved.
Resolve documented contradictions about repair, omission and metric values.
If required definitions remain absent or the schema remains partial,
report exact blockers and stop before implementation.
Do not substitute a permissive validator or silently amend the contract.

--------------------------------------------------
3. DEFINE THE VALIDATOR RESPONSIBILITY
--------------------------------------------------
For the same UISpec, context and schema version, return the same result.
The validator must NOT:
- call AI, make network calls, access databases or execute arbitrary code
- modify the UISpec or context, repair output or invent missing fields
- silently change values, classify defects or approve/reject boards
- render UI or invoke state-changing actions
It answers: Does this UISpec comply with the defined contract?
Required domain context is supplied by the caller, not fetched here.

--------------------------------------------------
4. JSON SCHEMA VALIDATION
--------------------------------------------------
Use specs/schemas/ui-spec.schema.json as structural authority.
Use suitable Draft 2020-12 validation tooling; do not duplicate the schema
as hand-written application rules. Report useful structural failures.
Distinguish expected refusal from invalid output and a valid normal page.
```

```prompt
--------------------------------------------------
5. IMPLEMENT THE RULES DELEGATED FROM TASK 2
--------------------------------------------------
Implement only runtime rules explicitly recorded in the approved board
contract and schema documentation. Do not import tutorial constants.

A. TOTAL NODE COUNT
The current board rule is 1..12 top-level components for normal pages.
No 30-node total is approved. A total-tree check needs a defined maximum,
child traversal paths, container counting rules and any depth limit.

B. SERIALIZED UISPEC SIZE
No 8 KiB board limit is approved. If a size rule is formally added,
use its exact limit, encoding and raw-byte/reserialization definition.
Measure the complete payload, not a separate allowance per component.

C. PROGRESS INDICATOR RELATIONSHIP
The current board example uses ref: metrics.shift_progress.
Do not invent current, steps or current < len(steps).
Implement only a relationship explicitly defined by the board contract.

D. CONTEXT AND REFERENCE CONSISTENCY
Do not invent meta.generated_for or onboarding context fields.
Apply the approved board context and reference rules using supplied data.
Resolve absent-reference handling and references-versus-values conflicts
before implementing grounding. Never calculate or fabricate metric values.

--------------------------------------------------
6. URL HOST ALLOW-LIST
--------------------------------------------------
Review approved props and action definitions.
Do not introduce URL fields or host allow-lists without a contract rule.
Do not claim the current partial schema excludes URLs: props remain open.
Document whether a URL rule is applicable only after props are complete.

--------------------------------------------------
7. VALIDATION RESULT
--------------------------------------------------
Use the agreed result shape and stable diagnostic code vocabulary.
Identify what failed, where it failed and why.
Example location: /components/0/type
Example rule: enum
This example does not define a new result API.
Keep diagnostics deterministic and do not expose stack traces as results.
```

```prompt
--------------------------------------------------
8. DO NOT AUTO-REPAIR
--------------------------------------------------
Reject invalid output. Do NOT:
- truncate strings or remove unknown properties
- replace component types or CTA actions
- rewrite data references or context
- delete excess components or silently make an input valid
The validator is pure; it contains no model retry or repair orchestration.
Resolve the broader repair policy separately in the authoritative docs.

INVALID → REJECT, not INVALID → silently repair → ACCEPT.

--------------------------------------------------
9. TESTS
--------------------------------------------------
Create focused deterministic automated tests after readiness is confirmed.

VALID CASES
1. Valid minimal landing UISpec.
2. Valid Hero + CTA + Text under the approved props contract.
3. Valid FeatureGrid and permitted children under the approved child rules.
4. Documented top-level refusal:
   {"view":"landing","refusal":"insufficient_context","components":[]}
5. Valid reference-based ProgressIndicator.
6. Exactly 1 and 12 valid top-level entries in a normal response.

INVALID CASES
7. Unknown type, including run_query and DispositionControl.
8. Unknown envelope property, missing required field or wrong field type.
9. Zero or 13 top-level components in a normal, non-refusal response.
10. Unknown component props or invalid nesting under the completed contract.
11. Invalid CTA action if an approved action table exists.
12. Invalid reference/context behaviour under the agreed policy.
13. String, total-node and size boundary violations only where defined.
14. Unsupported URL-bearing structure only where closed props define it.

Do not label a skipped undefined rule as implemented coverage.
Do not import 30 nodes, 8 KiB, generated_for or current/steps as tests.
For each valid/invalid case assert the agreed outcome and diagnostics.

--------------------------------------------------
10. TEST DETERMINISM
--------------------------------------------------
Repeat valid and invalid input with identical context and schema.
Assert identical outcomes and stable diagnostic ordering.
Assert that both the UISpec and supplied context remain unchanged.
No clocks, randomness, live models, network or hidden mutable state.
```

```prompt
--------------------------------------------------
11. KEEP TESTS CLOSE TO THE CONTRACT
--------------------------------------------------
Keep the suite small and readable; do not create a large testing framework.

Contract rule → Crafted input → Expected result

Use fixed fixtures. Cover all nine approved components, each documented
runtime rule and relevant boundary values. Do not target a tutorial count.
Keep semantic evaluations distinct from deterministic software tests.
A keyword filter does not prove that all implied verdicts are impossible.

--------------------------------------------------
12. DEPENDENCY DISCIPLINE
--------------------------------------------------
Before adding a dependency:
1. Inspect existing tooling for suitable Draft 2020-12 support.
2. If needed, select one appropriate JSON Schema validation library.
3. Add only necessary test tooling, such as pytest if selected.
Do not add React, FastAPI, model SDKs, database or infrastructure packages.
Place the validator within the planned Domain Runtime structure.
Do not scaffold services beyond what this increment needs.

--------------------------------------------------
13. DOCUMENTATION
--------------------------------------------------
Update relevant validator/test documentation only as needed to explain:
- what the validator does
- what JSON Schema handles
- what approved runtime rules handle
- what validation intentionally does not establish
- how to run the actual test suite
Do not rewrite the model contract to make implementation convenient.
Document unresolved contradictions and their implications explicitly.

--------------------------------------------------
14. VERIFY THE IMPLEMENTATION
--------------------------------------------------
Run the complete validator test suite and relevant existing schema checks.
Verify that valid cases pass and invalid cases fail, including nesting.
Verify all approved component and action coverage where defined.
Verify determinism and non-mutation without models or network access.
Distinguish JSON parsing, schema meta-validation and instance validation.
Report actual commands and results; never reuse onboarding pass counts.
```

```prompt
--------------------------------------------------
15. REVIEW THE DIFF
--------------------------------------------------
Before finishing, inspect:
git status
git diff --stat
git diff
Also review newly created/untracked files.
Confirm changes are limited to Task 3 and preserve unrelated user work.

--------------------------------------------------
16. IMPORTANT STOPPING RULE
--------------------------------------------------
Do NOT create a Git commit yet. Do NOT push anything.
Stop and report:
1. What was implemented
2. Files created
3. Files modified
4. Dependencies added, if any
5. Validation rules implemented
6. Tests created
7. Actual test results
8. Existing Task 2 checks status
9. Ambiguities and unresolved limitations
10. Current Git status
11. Proposed next checkpoint

Do not start Task 4. Do not commit changes.
We will review Task 3 before creating the next checkpoint.
If readiness failed, report blockers instead of claiming completion.
```

Implementation and verification follow the resolved contract, not the old shape in the archive. No API, model, renderer, repair loop, authentication or manufacturing integration was built in Task 3.

## 18. Task 3 — Structural and Runtime Validation Layers

```text
Spec + complete GroundedContext
    |
    v
JSON Schema structure / closed props / bounds
    |
    v
References + context matching + exact metric copying
 + aggregate rendered text + deterministic text policy
    |
    +-> INVALID with stable sorted diagnostics
    +-> VALID with no board-quality meaning
```

The strict Pydantic GroundedContext contains contextVersion, contextId, page, locale, generatedAt, capabilities, defectCategories, metrics, alerts and actions. Empty collections are allowed where appropriate, but omitted required fields are not invented. Invalid caller context is a sanitized caller error, distinct from INVALID proposed spec data.

## 19. What Does Deterministic Mean?

For the same inputs, selected schema and code version, the validator produces the same result and ordering without changing its inputs. It does not call a model, network, database, clock or random generator during validation. Constructor schema loading is distinct from validation-time I/O.

```text
same spec + same context + same rules -> same diagnostics
same approved page + same components -> same observable UI
```

Raw JSON rejects duplicate keys and non-finite numbers. Cycles and non-JSON objects cannot sneak through decoded input. Determinism makes failures reproducible; it does not mean every natural-language implication can be understood by the policy checker.

## 20. What Is a Block? Local Bounds, Not a Borrowed Node Rule

The landing page is an ordered blocks array. Hero, Heading, Text and CTA can be siblings; they are not children of Hero. FeatureGrid.props.items contains FeatureCard props directly. InfoPanel.rows contains metric-row data, not nested component blocks.

```text
blocks
  Hero
  Heading
  Text
  FeatureGrid
    items: card props, card props
  CTA
  InfoPanel
    rows: metric data
```

The selected schema allows 1..12 blocks and 2..6 grid items. There is no implemented total 30-node rule. Counting all React elements or JSON objects as “nodes” would invent a different contract. Teach the data shape actually enforced by the selected schema.

## 21. Rendered Text Budget, Not an Imported 8 KiB Limit

The board validator enforces 4000 total rendered string characters using its documented field-selection/counting rules. Identifier strings and JSON syntax are not interchangeable with user-visible text. This aggregate policy complements local schema string limits.

No 8 KiB serialized payload cap is implemented. Bytes, Unicode code points and rendered string length measure different things. Do not copy the source tutorial's byte rule or claim the text policy is a transport-size or denial-of-service guarantee. Tests exercise the exact accepted/rejected text boundary defined by this implementation.

## 22. Context Identity and Grounding

A syntactically legal metricId can still refer to nothing. A legitimate action can still be unavailable in the current context. contextId equality ties the proposal to the supplied context, while membership and value checks enforce individual references.

For overview, contextId is task4-overview and locale is en-US with fixed synthetic timestamps. InfoPanel copies the metric string 0012.50 and unit images exactly. The renderer must not turn it into 12.5, calculate a total, or call it a live production result. No generated_for or onboarding ContextPayload fields exist in this v1 shape.

## 23. ProgressIndicator Runtime Rule

The existing overview uses metricId recorded-progress, label Recorded progress and numeric value 37.125. Its matching metric carries string value "37.125" with unit "%". Python checks numeric equality with the allowed JSON-number grammar and percentage unit; React displays the supplied percentage without rounding.

```text
Context metric: "37.125", unit "%"
UISpec value:   37.125
               |
               v
Exact numeric match + allowed range -> render supplied value
```

This is not steps/current or an inferred shift-progress reference. Progress is supplied presentation data, not a manufacturing classification or defect-ratio calculation.

## 24. Reject Versus Repair

The validator does not truncate strings, remove props, clamp progress, rewrite context IDs, replace actions or manufacture a valid response. Task 4 rejects the entire render for unknown components. Task 6 rejects invalid server fixtures and shows a controlled error on transport failure.

```text
Invalid proposal -> deterministic rejection -> visible diagnostics/error
                 X no silent repair or substituted fixture
```

Future architecture discusses bounded model repair/fallback, but that orchestration is absent from Tasks 3–6. Keeping errors visible makes both software and future model behaviour measurable.

## 25. Structured Validation Results

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

This documented example illustrates a precise path and stable code rather than a bare false. Inspectable violations are collected, deduplicated and ordered by gate/path/code/rule/message. The result is separate from Task 6's sanitized HTTP error envelope. Internal diagnostic detail must not be echoed to a browser on failure.

## 26. Task 3 — Tests and Limitations

The Task 3 report records 163 passing tests and a clean pip check. This is historical implementation evidence, not a fresh run for this document. Coverage includes nine components, five actions, local bounds, malformed input, grounding, precision, 4000-character boundaries, deterministic diagnostics and non-mutation. Networking is disabled in validator tests.

Schema verification has four distinct levels: parse the schema JSON; meta-validate Draft 2020-12; validate an instance; run the instance with its complete context through Python policy. The current suite executes these for the selected schema. It does not meta-validate the preserved alternative.

Deterministic text patterns have false-positive/false-negative limits. Passing the suite does not prove all implied verdicts, prompt injection or misleading copy are impossible. Future semantic evaluation remains necessary before claims about model behaviour.

## 27. Task 3 — Actual Files and Dependency Roles

```text
services/
  __init__.py
  domain/
    __init__.py
    validator.py
    validation_models.py
    text_policy.py
    README.md
tests/validator/
  conftest.py
  test_validator.py
requirements.txt
requirements-dev.txt
pytest.ini
specs/TASK-3-READINESS.md
specs/TASK-3-IMPLEMENTATION-REPORT.md
```

jsonschema handles structural validation; Pydantic supplies strict context/result types; pytest runs deterministic checks. Their recorded Task 3 pins are jsonschema 4.26.0, pydantic 2.13.5 and pytest 9.1.1. The validator remains the same authority when Task 6 introduces HTTP.

## 28. Architecture Review Before Task 4

Before React work, the project resolved four practical questions: which schema copy is authoritative, whether invalid entries cause omission or whole-page rejection, how fixtures establish approval, and where a Hero action label comes from when no label prop exists.

The reviewed decisions selected specs/schemas/ui-spec.schema.json, whole-page rejection, Python-verified paired fixtures and matching context action labels. No new prop, destination or validator result API was invented. Readiness is useful because apparently small UI choices can otherwise redesign the contract accidentally.

## 29. The Critical Approved-Input Boundary

```text
Fixed UISpec + full synthetic context
 -> Python preparation requires VALID for every catalogue pair
 -> generated data + retained verification evidence
 -> private handle issuance
 -> ControlledRenderer
```

This was an offline build/preparation handoff in Tasks 4–5, not browser-to-Python transport. Preparation removes stale generated output and evidence before rebuilding; failed validation leaves no stale success artifact. A developer-authored file is not automatically approved.

Task 6 extends admission only for the exact independently prepared overview envelope. A generic future model response cannot use that admission path without a new design review.

## 30. Contract Vocabulary Versus Executable Registry

The schema says which component names and props are legal data. The registry says which developer functions can render. Neither replaces the other: a registry cannot establish grounding, and schema text cannot safely resolve arbitrary JavaScript implementations.

```text
Contract vocabulary -> schema checks legal data
Registry            -> maps legal names to fixed functions
Python validator    -> checks supplied context and policy
Private issuance    -> controls renderer input association
```

Inherited object names such as constructor, toString and __proto__ are not components. Own-key membership is explicit; run_query and DispositionControl reject rather than being hidden or relabeled.

## 31. Task 4 — Controlled UISpec Renderer

**Exact Execution Prompt Used — provenance:** All six stored prompt blocks from Documents/BOARD_DEFECT_INSPECTION_TASK_4_BEGINNER_GUIDE_ENTERPRISE_STANDARD.md are reproduced below in order. This is the complete local guide record. Conversation formatting may differ; no stronger byte-for-byte transcript claim is made.

```prompt
Proceed with Task 4: implement the Controlled UISpec Renderer.

This is the next proposed implementation increment for the
Board Defect Inspection AI project, after readiness review.

IMPORTANT ARCHITECTURAL DECISION:
The renderer must receive ONLY an already-validated UISpec.
The renderer must NOT accept raw AI/model output.
VALID refers to a UISpec, never to board PASS/FAIL or approval.

Conceptually:
RAW AI OUTPUT
      ↓
UISpec Validator + supplied grounded context
      ↓
VALIDATED UISpec
      ↓
Controlled Renderer
      ↓
Approved React Components
      ↓
Browser UI

The renderer contract is conceptually:
render(approvedUISpec)
Do NOT implement render(rawAIOutput).

Before making changes:
1. Inspect branch, commit, working tree and project structure.
   Preserve unrelated work. Report Git failures without repair.
2. Read CLAUDE.md, README.md and the references below.
```

```prompt
   - Documents/Business Requirements Document.docx
   - docs/business-problem.md and docs/architecture.md
   - specs/spec.md and specs/model-contracts.md
   - specs/schemas/ui-spec.schema.json and its schema notes
   - specs/ui-spec.schema.json (compare the competing copy)
   - specs/TASK-3-READINESS.md
   - specs/TASK-3-IMPLEMENTATION-REPORT.md
   - services/domain/validator.py and validation_models.py
   - services/domain/text_policy.py and README.md
   - tests/validator/ and tests/README.md; evals/README.md
   - Relevant Documents/ guides and Task 2 clarifications
3. Review actual Task 1-3 files and current checks. Historical
   guides and the BRD's examples do not override the v1 contract.
   Do not reuse onboarding commits, test counts or constants.

TASK 4 GOAL
Implement a deterministic renderer for the board landing page.
Translate validated blocks through an explicit component registry.
Use specVersion "1.0", page "landing", contextId and blocks.

The approved component vocabulary is exactly:
- Hero
- Heading
- Text
- FeatureCard
- FeatureGrid
- CTA
- Alert
- InfoPanel
- ProgressIndicator

READINESS BEFORE IMPLEMENTATION
Confirm the authoritative schema path and its differing bounds.
Task 3 loads specs/schemas/ui-spec.schema.json; normative docs
also point to specs/ui-spec.schema.json. Do not silently merge them.
Resolve architecture's omit-and-record wording versus this brief's
reject-rendering requirement before choosing renderer behaviour.
Agree how approved fixtures enter the renderer. Task 3 returns
status/rejections, not an approved payload or browser trust token.
Review Hero.primaryAction labelling: no action label prop exists.
Do not invent a prop, URL, route or destination to fill that gap.
If required decisions remain unresolved, report blockers and STOP.

IMPORTANT SECURITY / CONTROL REQUIREMENTS
The model must NOT create arbitrary executable components.
Do not execute generated JavaScript, shell or other code.
Do not use eval(), Function(), dangerouslySetInnerHTML,
model-driven dynamic imports or arbitrary component resolution.
Do not bypass the registry or silently substitute components.
Use explicit approved props; never spread model props onto DOM.

RENDERER DESIGN
Use a fixed developer-authored registry with all nine entries:
componentRegistry = {
  Hero: HeroComponent, Heading: HeadingComponent,
  Text: TextComponent, FeatureCard: FeatureCardComponent,
  FeatureGrid: FeatureGridComponent, CTA: CTAComponent,
  Alert: AlertComponent, InfoPanel: InfoPanelComponent,
  ProgressIndicator: ProgressIndicatorComponent
}
```

```prompt
Use an explicit typed registry/switch, never dynamic discovery.
An unknown component must not render. Apply the reviewed failure
policy consistently; do not repair, relabel or hide violations.

VALIDATION BOUNDARY
Do not duplicate the JSON Schema or grounding rules in React.
JSON Schema -> structural validation
Task 3 validator -> grounding and deterministic policy checks
Renderer -> approved component mapping and DOM safety

Use fixed fixtures validated by the existing Python validator
against their complete synthetic GroundedContext. Retain both
files and verification evidence. Do not treat a TypeScript cast,
brand or model-supplied approved=true flag as proof of validation.
Keep arbitrary JSON entry points out of the demonstration.
No API, model gateway or live data fetching belongs in this task.

REACT IMPLEMENTATION
Inspect existing tooling. Create only the minimum React/TypeScript
structure in apps/ui/ needed to demonstrate and test the renderer.
Use strict TypeScript and explicit props; do not introduce any.
Do not build the complete board inspection application.
Preserve block order and supplied text, metric values and units.
Do not calculate, round, classify or infer missing information.
Use semantic headings, accessible controls and text for severity.

FeatureGrid.props.items contains 2..6 FeatureCard PROPS objects.
It is not a generic children array or nested block envelope.
Hero and InfoPanel have no child components. InfoPanel.rows is
metric-row data. ProgressIndicator uses metricId, label and value
(0..100), not steps/current or metrics.shift_progress references.

Representative synthetic UISpec (validate with matching context):
{
  "specVersion": "1.0",
  "page": "landing",
  "contextId": "task4-demo",
  "blocks": [
    {
      "component": "Hero",
      "props": {
        "title": "Board inspection activity",
        "subtitle": "Inspection records and defect reporting."
      }
    },
    {
      "component": "Text",
      "props": {"text": "Explore recorded inspection activity."}
    },
    {
      "component": "CTA",
      "props": {
        "label": "Open defect reports",
        "action": "view-defect-reports"
      }
    }
  ]
}
```

```prompt
The matching context must contain every GroundedContext field,
contextId "task4-demo", page "landing", contextVersion "1.0",
fixed locale/generatedAt, empty capabilities/defectCategories/
metrics/alerts, and action id "view-defect-reports" with its label.
These are synthetic examples, never evidence of live operations.
Use the ACTUAL schema and contract for exact types and bounds.

ACTION CONTROL
The only approved action identifiers are:
- view-inspection-queue
- view-defect-reports
- view-ingest-activity
- open-documentation
- contact-support
Actions must also be available in the supplied context.
Keep action handling developer-owned. A test callback may record
an identifier without navigation, network calls or state changes.
Do not invent URLs, destination routes or inspection workflows.
Any optional demonstration with inert controls must say so outside
model-authored content. Resolve Hero action labels before building.

TESTING
Add small, readable deterministic renderer tests. At minimum:
1. All nine approved components resolve through the registry.
2. Hero + Heading/Text/CTA render as sibling blocks, not children.
3. FeatureGrid renders 2 and 6 card-props items in supplied order.
4. CTA renders its label and uses only approved action handling;
   cover all five actions and optional Hero.primaryAction.
5. Unknown names, including run_query, DispositionControl and
   inherited object keys, cannot resolve as registry components.
6. Model-like strings cannot execute code or inject markup.
7. Unknown props cannot become DOM attributes, event handlers,
   styles or executable behaviour; no arbitrary prop spreading.
8. Same approved input gives the same observable rendering.
9. Rendering and action tests leave the input unchanged.
10. A representative validated fixture traverses the complete path.
11. InfoPanel preserves values/units; ProgressIndicator represents
    the supplied percentage without rounding or invented figures.
12. Heading levels and Alert severity remain accessible; verify
    registry failure handling matches the reviewed policy.

Validate positive fixtures with Task 3. Deliberately malformed
renderer-boundary probes are test-only, never a production bypass.
Do not accept old refusal, root/children or generated_for shapes.
Do not import 19/24/12 test counts, 30 nodes or an 8 KiB limit.
Tests do not prove all implied quality verdicts are impossible.

IMPORTANT:
Do not add AI/model integration, a model gateway, FastAPI runtime
or integration, authentication or domain data access.
```

```prompt
Do not add physical camera integration, edge image processing,
real-time PLC/MES handling, automated defect classification,
human review/override workflows or production infrastructure.
Do not build customer onboarding, registration or risk scoring.
Do not add model retry/repair or fallback orchestration here.
Do not redesign the contract or change the schema to suit React.
If a required inconsistency remains, STOP and report it.
Do not invent a new validation result API or rejection code.

BEFORE IMPLEMENTATION
First explain:
1. The minimal renderer structure and readiness findings.
2. Where the explicit component registry will live.
3. How verified fixtures reach the approved-input boundary.
4. Files to create or modify, including required documentation.
5. How determinism and non-mutation will be demonstrated.
6. How executable content and arbitrary DOM props are prevented.
Then implement only when the readiness decisions are resolved.

DEPENDENCY DISCIPLINE
Inspect available tooling before selecting packages. Add only
React, TypeScript and necessary renderer test/build/lint tooling.
Choose compatible versions at implementation time and record them.
Do not copy obsolete versions from the onboarding tutorial.
Keep dependency locks; ignore node_modules and build artifacts.

AFTER IMPLEMENTATION
Run the actual renderer tests and TypeScript checks.
Run the project-required prohibition/lint checks for unsafe paths.
Run the existing Task 3 suite from the repository root:
  .venv/Scripts/python.exe -m pytest -q
Confirm which Task 2 schema checks that suite actually executes:
JSON parsing, Draft 2020-12 meta-validation and instance checks
are different checks. Record actual commands and results.

Confirm:
- Renderer tests and existing regression checks pass.
- All nine components and all five actions are covered.
- No model, API, authentication or physical integration was added.
- No board quality approval, classification or override was added.
- No raw model output reaches the render entry point.
- No code execution or model-driven module loading was added.
- Schema and grounding authority remain in the existing validator.
- No live validator-to-browser transport is claimed.

Review git status, git diff --stat, git diff and new files.
If Git remains unreadable, report exact failures and inspect local
files; do not claim a clean diff or repair the repository implicitly.

Do NOT commit. Do NOT push. Do NOT start Task 5.
Stop and report:
```

```prompt
1. Files created
2. Files modified
3. Component registry design
4. Renderer design and approved-input boundary
5. Tests added
6. Actual test results
7. Existing regression and schema-check results
8. Dependencies added, if any
9. Architectural issues, limitations and current Git status
10. Recommended next smallest task
Wait for human review before proceeding further.
```

Task 4 implemented the fixed registry and controlled renderer with explicit DOM props. It also already created the minimal Vite shell and synthetic demonstration. Task 5 therefore did not need a second application scaffold. Task 4 added neither a live model nor an HTTP backend.

## 32. Task 4 — React and TypeScript Foundation

```text
apps/ui/
  index.html
  package.json / package-lock.json
  tsconfig.json / vite.config.ts / eslint.config.mjs
  src/
    types.ts / components.tsx / registry.ts
    approved.ts / render.tsx / main.tsx / style.css
    generated/fixtures.ts       ignored, preparation-owned
  fixtures/
    minimal.spec.json + minimal.context.json
    overview.spec.json + overview.context.json
    grid-six.spec.json + grid-six.context.json
    actions.spec.json + actions.context.json
    headings-alerts.spec.json + headings-alerts.context.json
    verification.json
  scripts/
    prepare_fixtures.py / prepare.mjs / check-safety.mjs
  tests/renderer.test.tsx
tests/renderer_fixtures/test_prepare_fixtures.py
```

Strict types improve developer correctness but do not prove data approval. Preparation supplies actual Python validation evidence. The WeakMap association supplies the runtime handle check. Hashes support reproducibility, not signatures. node_modules, dist and generated source are local artifacts, not committed architecture layers.

## 33. Task 4 — The Approved Component Registry

```text
Hero              -> HeroComponent
Heading           -> HeadingComponent
Text              -> TextComponent
FeatureCard       -> FeatureCardComponent
FeatureGrid       -> FeatureGridComponent
CTA               -> CTAComponent
Alert             -> AlertComponent
InfoPanel         -> InfoPanelComponent
ProgressIndicator -> ProgressIndicatorComponent
```

The frozen registry has exactly nine own entries. FeatureGrid uses the registered FeatureCard implementation for its 2..6 props items. Hero and InfoPanel never acquire generic children. Fixed functions receive explicit allowed fields; model/API props are never spread onto a DOM element.

## 34. Task 4 — Renderer Contract

ControlledRenderer takes an ApprovedUISpec handle and developer-owned action callback. It checks issuance, preflights the whole page and dispatches through the explicit registry. It preserves sibling order, text, metric strings, units and supplied numeric progress.

Semantic headings and native controls provide accessible structure; severity remains visible text. Action dispatch uses the approved five-ID vocabulary plus context bindings. Hero obtains its label from the binding; CTA uses its own supplied label. Neither control navigates or changes inspection data in the demonstration.

## 35. Task 4 — Security Tests and Regression Evidence

The Task 4 report records 29 renderer tests and 167 Python checks including four new preparation tests. Tests cover registry completeness, sibling composition, both grid bounds, five actions, Hero labels, unknown/inherited names, strings that resemble code, forbidden DOM props, deterministic output and unchanged inputs.

Safety lint rejects 11 prohibited syntax probes while accepting inert text. It combines static controls with runtime probes; it is not a proof that every future misuse is impossible. Malformed boundary probes substitute data only inside isolated tests and are not a production bypass. No runtime eval, Function, HTML sink, arbitrary module loading or component discovery was added.

## 36. Complete Control Chain After Task 4

```text
Canonical pair -> unchanged Task 3 validator
 -> all catalogue pairs VALID -> generated data/evidence
 -> private frozen association -> issued handle
 -> whole-page registry preflight -> explicit components -> React
```

Positive fixtures include complete matching contexts and fixed timestamps. Preparation is required before dev, build and test application data loads, including Vite/Vitest configuration gates. Failed preparation removes stale artifacts. This makes the demonstration reproducible without claiming a live service boundary before Task 6.

## 37. Schema, Registry, Tests, Evals and Feedback

Schema defines legal structure; Python checks grounding/policy; the registry bounds executable UI; tests verify these deterministic mechanisms. Evals would measure how often a future model proposes useful, grounded and policy-compliant content across scenarios. A model can pass structural checks while producing poor or misleading prose, so these measures are complementary.

```text
Future observed model behaviour -> eval findings
 -> reviewed prompt/context/contract/code improvement
 -> deterministic regression tests + repeatable evals
 -> human review
```

evals/README.md and cases describe evaluation intent. They do not demonstrate a live model evaluation runner or completed model scores. Automated feedback, production logging pipelines and model repair are not implemented.

## 38. Task 5 — Minimal Runnable React UI

Task 5 reused the Vite shell and fixtures from Task 4, extracted App for focused testing, retained the external synthetic/inert notice and error boundary, and verified actual browser behaviour. It did not introduce the registry, a new build system or a live API.

**Exact Execution Prompt Used — provenance:** The complete stored Task 5 prompt follows verbatim from Documents/BOARD_DEFECT_INSPECTION_TASK_5_BEGINNER_GUIDE_ENTERPRISE_STANDARD.md. The implementation report separately records reconciliation with the later full user prompt. The local guide block is not claimed to preserve every conversational revision.

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

```text
apps/ui/src/App.tsx                 extracted app/error boundary
apps/ui/src/main.tsx                mounted static overview at Task 5
apps/ui/tests/app.test.tsx          four application cases
apps/ui/scripts/check-browser.mjs   separate developer CDP check
apps/ui/index.html                  local empty favicon
specs/TASK-5-IMPLEMENTATION-REPORT.md
specs/task5-browser-evidence/
  observations.json / wide.png / narrow.png
```

Task 5 path: Python preparation -> catalogue -> approvedFixture('overview') -> App -> ControlledRenderer -> browser. No live Python transport existed at that milestone. The main entry changes to API loading only in Task 6.

Historical Task 5 results: 33 UI tests, 167 Python tests, strict TypeScript/safety lint/build and actual Chrome wide/narrow checks passed. Browser evidence checked real DOM, keyboard focus, inert actions, console and network; an HTTP 200 shell alone was insufficient. No new dependencies or CSS redesign were necessary.

Task 5 excluded APIs, AI, authentication, production data, charts, line filters, image overlays and quality workflows. Its value was evidence that the existing renderer could run as an application, not a claim of a complete inspection product.

## 39. Task 6 — Domain Runtime / FastAPI Boundary

Task 6 replaces the browser's direct static runtime source with a fixed Domain API while retaining offline preparation and the existing renderer. The user approved transport decisions before implementation. This is the first live local HTTP boundary; it does not introduce an AI Runtime.

**Exact Execution Prompt Used — provenance:** The complete stored Task 6 prompt below is reproduced from Documents/BOARD_DEFECT_INSPECTION_TASK_6_BEGINNER_GUIDE_ENTERPRISE_GRADE.md. That guide was written as a proposed prompt; the subsequent user request and readiness approval authorized implementation. The report records actual decisions and results. Prompt preservation does not convert every proposed layout into an implemented file.

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

```text
services/domain/
  validator.py / validation_models.py / text_policy.py   reused
  landing_service.py                                  fixed pair service
  api/
    __init__.py / main.py / routes.py                   HTTP boundary
apps/ui/src/
  api/client.ts                                        fixed loader export
  approved.ts                                          private admission
  App.tsx / main.tsx                                   async application
apps/ui/tests/
  transport.test.tsx / transport-fixture.ts
tests/domain_api/test_landing_api.py
requirements-lock.txt
specs/TASK-6-READINESS.md
specs/TASK-6-IMPLEMENTATION-REPORT.md
specs/task6-browser-evidence/
  api-smoke.json / observations.json / unavailable.json
  wide.png / narrow.png / unavailable.png
```

**Request and endpoints.** GET /health returns 200 {"status":"ok"}, process liveness only. POST /api/v1/ui/landing-page requires application/json and exactly {"page":"landing","locale":"en-US"}. Extra fields, query parameters, client grounding, fixture selectors and arbitrary paths reject. The versioned AI-aware health route remains future scope, without an alias.

**Response.** HTTP 200 contains exactly {spec, source, rejections, contextId, actions}; source is "fixture", rejections is [], contextId matches task4-overview, and actions is the full ordered context action list. This explicit reviewed amendment supplies metadata and Hero bindings without changing UISpec. Errors are {"error":"invalid_request"} at 422, landing_unavailable at 500, method_not_allowed at 405 and not_found at 404. No internal stack traces or input echoes are returned.

**Service ownership.** landing_service.py loads only the canonical overview pair under apps/ui/fixtures. It reads each once into a request-local snapshot, validates raw spec text with complete context and serializes the same accepted data. There is no second fixture copy, arbitrary repository abstraction, database or model call. No concurrent fixture-edit protocol or standalone backend packaging is claimed.

```text
Browser -> fixed POST -> Vite proxy -> FastAPI route
 -> landing service -> fixed spec/context snapshot
 -> UISpecValidator: require VALID
 -> exact envelope + matching context bindings
 -> response JSON remains unknown
 -> exact independently prepared overview match
 -> private issuance from actual response snapshot
 -> ControlledRenderer -> registry -> React -> browser
```

**Admission and failure.** Matching only an outer shape or a success flag is insufficient. Complete JSON-value equality allows object-key reordering but rejects any changed field, array order, type, value or binding. The issuer freezes the admitted response into a fresh handle; it does not return the static catalogue handle. Loading, HTTP/network failure, invalid JSON and mismatched payloads have controlled UI states. Aborted/stale requests cannot overwrite current state. A failed API never silently falls back to a fixture.

**Local development.** Vite uses a narrow same-origin proxy to 127.0.0.1:8001. The existing port-8000 listener was preserved. No CORS middleware or wildcard origins were introduced. Direct cross-origin browser use and production origin protection are not promised. Backend command: .venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8001. Run npm run dev from apps/ui in a second terminal and use its printed URL.

**Dependencies.** New direct pins were FastAPI 0.142.1, uvicorn 0.54.0 and HTTPX 0.28.1 for tests. Existing React packages/lock are unchanged; resolved Python constraints record 28 packages. One Starlette TestClient HTTPX deprecation warning remains disclosed. No AI SDK, ORM, authentication framework or production service was added.

**Verification.** The retained implementation run passed 197 Python tests (163 validator, 4 handoff, 30 API) and 63 UI tests (29 renderer, 4 app, 30 transport). Typecheck, safety lint, build and pip check passed. API tests verify validation-before-success, exact fixture/context/actions, invalid fixtures/requests, sanitized errors, determinism and non-mutation. Client tests verify full admission, loading/error/success, stale requests, inert actions and no fallback.

```text
Retained smoke evidence, not a fresh documentation run:
GET  http://127.0.0.1:8001/health -> 200 {"status":"ok"}
POST http://127.0.0.1:8001/api/v1/ui/landing-page -> 200
  response.spec revalidation -> VALID; actionsMatch -> true
Same routes through http://127.0.0.1:5173 -> expected responses
Supplied grounding -> 422 invalid_request
Backend stopped -> controlled browser error; no static page fallback
```

Chrome 154.0.8037.93 displayed nine blocks at 1440x1000 and 375x812 without horizontal overflow. Keyboard focus, inert controls, exact values and repeatable reload DOM passed. Success had no console errors or unexpected external/model requests. Dedicated task processes were stopped afterward; this document does not freshly assert ports are free. Cross-browser and assistive-technology coverage remain unverified.

**Limit.** This adapter deliberately accepts only the fixed overview. Server fixture changes require matching frontend preparation/build. It is neither authentication nor a generic future model-output transport. A future AI proposal path needs separately reviewed admission assumptions while retaining the controlled rendering principle.

## 40. Git Checkpoints and Recoverability

```text
Implement -> verify -> review -> agree file scope
 -> explicit commit authorization -> commit
 -> explicit push authorization -> verify shared checkpoint
```

Current observed branch is wushan, HEAD 3810dc0e0f3a0cba21383da9d42c7ca29bc6b9da, message “update 2026-09-22”. Earlier visible messages include f5caf99 repo folder changes and f0e3f27 Update 2 initial discussion document. These are actual Git observations, not invented Task 4/5/6 milestones.

The worktree is dirty, with earlier untracked UI assets, Task 6 work, guides and existing deletions. No Task 6 commit/push has occurred. Cached origin/wushan equality from the checkpoint review did not prove a live remote fetch. Documents/BOARD_DEFECT_INSPECTION_TASK_6_CHECKPOINT_BEGINNER_FRIENDLY_ENTERPRISE_GRADE.md records the checkpoint candidate and proposed review procedure. Do not stage everything or delete unrelated work to make a clean-status claim.

## 41. What Has Not Been Built Yet

- No model gateway, runtime generation, AI SDK, agent orchestration or model evaluation execution.
- No image capture/processing, camera/edge/PLC/MES integration or defect classifier.
- No live defect-ratio calculation, database, persistence or domain-data access.
- No quality approval/override, inspector decision workflow or automated manufacturing decision.
- No authentication, onboarding/registration, uploads, document processing or risk scoring.
- No production infrastructure, deployment, model repair/retry or fallback orchestration.
- No tutorial Task 6A parameters or automatically authorized Task 7.

These are deliberate scope limits. The local Domain API is implemented; it must not appear in the “not built” list merely because the source's older sections predate Task 6.

## 42. Master Architecture and Project Status Matrix

| Area | Current status | Evidence / limit |
| --- | --- | --- |
| Business problem and architecture | Documented | Future manufacturing architecture is not all implemented |
| Foundation instructions/specifications | Present | Earlier proposed guide is not an execution transcript |
| v1 contract and selected schema | Implemented authority | Alternative copy preserved with differing bounds |
| Deterministic validator | Implemented | Task 3 report; semantic text limitations remain |
| Registry and renderer | Implemented | Nine entries, private handles, whole-page rejection |
| Prepared paired fixtures | Implemented | Two complete synthetic pairs (`full-catalogue`, `task4-demo`) and verification evidence |
| Runnable browser UI | Verified 2026-10-03 | Task 5's own browser check was UNVERIFIED; first real-browser evidence is Task 6's |
| Domain API and runtime client | Implemented locally | Task 6 transport admission and no fallback |
| Python regressions | 194 passed | 163 validator + 7 fixture + 24 API; one dependency warning |
| UI regressions | 88 passed | 15 registry + 18 safety + 6 app + 23 renderer + 22 transport + 4 proxy config |
| Schema verification | Prior selected-schema checks passed | Parse, meta-schema, instance and runtime checks distinguished |
| TypeScript / lint / build | Prior passed | No fresh rerun during this document task |
| API/browser success and failure | Prior verified | Retained Task 6 JSON and screenshots |
| Formal Task 6 Git checkpoint | Pending | Uncommitted dirty working tree; no push |
| AI/eval runtime | Not implemented | Definitions/cases do not establish live model scores |
| Production inspection/ratio services | Not implemented | Quality/Manufacturing policy ownership retained |
| Cross-browser/assistive technology | Unverified | No broader accessibility certification claimed |

## 43. The Incremental Engineering Pattern

```text
Define -> specify -> formalise -> validate -> test
 -> review -> render -> verify browser -> integrate
 -> review/checkpoint -> future evaluate -> learn -> improve
```

Each task should be small enough to explain its files, input boundary, outputs and evidence. Reuse existing work: Task 5 verified a shell already created in Task 4; Task 6 reused the validator instead of duplicating policy. “Enterprise-grade” here means disciplined ownership and traceability, not installing enterprise infrastructure prematurely.

## 44. The Core AI-Native Engineering Lesson

Traditional software testing asks whether code behaves as specified. A future model adds another question: what happens when its proposal is malformed, ungrounded or misleading? The control chain rejects invalid structure and references before execution, while evals must assess probabilistic behaviour that deterministic string checks cannot fully understand.

Raw model output must never gain browser execution privileges. The current fixture-only path lets engineers test the boundary without introducing model nondeterminism. It is a stepping stone with explicit limits, not evidence that the product already understands motherboard images.

## 45. One-Sentence Summary of Each Milestone

- Business discussion: identify who needs inspection visibility and who owns quality facts.
- Architecture: separate UI presentation, Domain truth/validation and future AI proposal responsibilities.
- Task 1: give engineering context and requirements distinct durable homes.
- Task 2: make the structural presentation contract machine-checkable.
- Task 3: check proposals against complete context with deterministic diagnostics.
- Architecture review: resolve schema authority, failure policy and approved-input handoff before React work.
- Task 4: map verified presentation data only through fixed developer components.
- Task 5: prove the existing renderer runs as an accessible synthetic browser demonstration.
- Task 6: add a fixed validated Domain API and private response admission without a model.
- Checkpoint: remains a pending review/Git action, not a completed milestone in this repository.

## 46. The Four Questions to Remember

1. **What does the user see?** UI Runtime: React, explicit components and the controlled renderer.
2. **Who owns facts and allowed requests?** Domain Runtime: Python/FastAPI and server-owned context; current facts are synthetic.
3. **Where would probabilistic proposals originate?** Future AI Runtime; no gateway or model is implemented today.
4. **What helps the coding agent work reliably?** The engineering harness: specifications, scoped instructions, permissions, validation, tests, future evals, evidence and review.

```text
AI may propose (future)
 -> contract constrains -> schema checks structure
 -> Python checks grounding/policy -> approved handoff
 -> registry bounds executable components -> renderer produces UI

Presentation VALID != manufacturing approval
```

## 47. What Comes Next

First review Task 6 and its file scope, including dependencies on earlier untracked UI assets. Then run a separately authorized checkpoint verification pass and record fresh evidence. Commit/push only when explicitly instructed, preserving unrelated work.

Only after that review should the team select the next smallest board-specific increment. A generic transport or model seam needs its own contract and trust decisions. Do not copy onboarding context fields, automatically scaffold an AI client, or treat Task 7 as authorized by this walkthrough.

## 48. Final Takeaway and Evidence Map

The project currently demonstrates a controlled synthetic presentation pipeline, from complete grounded fixture context through Python validation, HTTP transport, private admission and fixed React rendering. Its business aspiration is broader; the scope boundary keeps that aspiration from being mistaken for implemented defect detection or ratio analytics.

Use these artifacts to verify a claim rather than relying on this teaching narrative alone:

| Claim | Repository evidence |
| --- | --- |
| Current business scope | docs/business-problem.md; specs/spec.md |
| Current v1 data shape | specs/model-contracts.md; specs/schemas/ui-spec.schema.json |
| Task 3 decisions/limits | specs/TASK-3-READINESS.md; services/domain/README.md |
| Renderer and offline handoff | apps/ui/README.md (no separate Task 4 report exists in this repository) |
| Task 5 browser milestone | specs/TASK-5-IMPLEMENTATION-REPORT.md — its browser check is recorded UNVERIFIED; no task5-browser-evidence directory exists |
| Task 6 approved transport | specs/TASK-6-IMPLEMENTATION-REPORT.md, "Readiness decisions, recorded"; specs/spec.md (no separate readiness file) |
| Task 6 actual results | specs/TASK-6-IMPLEMENTATION-REPORT.md; specs/task6-browser-evidence/ |
| Current checkpoint limitations | Board Task 6 checkpoint guide and fresh Git inspection |
| Archived prompts | Six source guide paths and prompt hashes in the companion provenance JSON |

The document generator checks all 48 sections, source prompt preservation and DOCX package integrity. These document checks do not rerun application verification. This walkthrough changes no runtime code, schema, validator, dependency lock or historical source guide. No commit, push or next implementation task is performed.
