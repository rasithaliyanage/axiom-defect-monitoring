# Board Defect Inspection AI
# Task 3 — Deterministic UISpec Validator & Tests
@ Beginner-Friendly Editable Guide

This guide explains what Task 3 will build, why it matters, how validation works, how it will be tested, and where it fits in the AI-native engineering journey.

**Board-project status:** documentation and implementation brief only. Task 2 has a partial schema; Task 3 has not been implemented. The original guide's format is retained without borrowing its completion claims.

## 1. Where We Were After Task 2
Task 1 established the engineering foundation. Task 2 began converting the written UISpec model contract into a machine-checkable JSON Schema. Component props, CTA actions and several limits remain undefined.
```text
Written Model Contract
        ↓
JSON Schema — currently partial
        ↓
Software can check the defined structural rules
```
JSON Schema checks structural rules such as component types, required properties, enums and array limits. A complete contract must come before complete validation.

## 2. What Task 3 Does
Task 3 is intended to build a deterministic Python UISpec validator and an automated test suite, using pytest if selected during implementation.
```text
AI Model → Raw UISpec → Deterministic Validator
                              ↓
                       Approved UISpec
                              ↓
                 Controlled UI Renderer → React UI
```
The validator does not generate UI, call a model, render React or make board-quality decisions. A valid UISpec does not mean that a board passes inspection.
<!-- PAGE -->
## 3. What Does “Deterministic” Mean?
AI models are probabilistic. The same request can produce different outputs. For the same UISpec, supplied domain context and schema version, the validator should produce the same result.
```text
Same valid input + same context   → VALID
Same valid input + same context   → VALID
Same invalid input + same context → INVALID
Same invalid input + same context → INVALID
```
**Key principle:** the validator does not make AI deterministic. It makes the validation boundary deterministic.

## 4. Two Layers of Validation
| Layer | Purpose | Examples |
|---|---|---|
| JSON Schema | Structural rules | Types, required fields, enums, closed envelopes |
| Runtime validator | Approved additional checks | Reference membership and cross-field rules once defined |
Think of JSON Schema as checking the shape of the parts, while runtime validation checks relationships requiring supplied context or additional logic.

## 5. Rule #1 — Component-Count Limits
The board contract permits **1–12 top-level components** in a normal page. Its refusal shape contains an empty components array. It does not define a total-tree limit of 30 nodes.
```text
components
├── Hero                   ← top-level entry 1
├── Heading                ← top-level entry 2
└── FeatureGrid            ← top-level entry 3
    └── props.items        ← children shown in the example;
                              formal rules remain undefined
```
- A top-level array limit is not a count of all descendants.
- A total-node limit needs an approved maximum and child traversal rules.
- Do not import Hero or InfoPanel containers from onboarding examples.
- The original guide's 30-node rule is not an approved board rule.
<!-- PAGE -->
**Why?** A bounded interface helps keep model output reviewable. Engineering must define bounds explicitly rather than inherit another project's numbers.

## 6. Rule #2 — Serialized UISpec Size
The original guide defines 8 KiB (8,192 bytes). The board contract currently has no serialized-size limit. Record the missing decision; do not silently adopt 8 KiB.
| Rule | What it limits | Board status |
|---|---|---|
| Top-level component count | Normal-page list size | 1–12 entries |
| Total component-node count | Tree complexity | Not defined |
| Serialized size | Entire JSON payload | Not defined |
If a size limit is adopted, define UTF-8 encoding, raw bytes versus reserialization and exact boundary behaviour. Character length is not byte length.

## 7. Rule #3 — ProgressIndicator
The board contract uses a data reference, not onboarding steps and current position:
```json
{"type": "ProgressIndicator", "ref": "metrics.shift_progress"}
```
The Domain Runtime resolves the value under the current model contract. The example key is not evidence of a live metric. No `current < len(steps)` rule may be invented when those fields do not exist.

## 8. Rule #4 — Context and Reference Consistency
The model receives available metric/alert keys and viewer context. Exact context shape, role echo rules and missing-reference handling need clarification.
```text
Supplied available keys + UISpec references
                    ↓
       Apply the approved grounding policy
```
The onboarding fields `meta.generated_for`, segment, product interest and region are not board UISpec fields. Do not rename and import them.
<!-- PAGE -->
## 9. Rejection — Not Repair
```text
INVALID MODEL OUTPUT
        ↓
      REJECT

Not: INVALID → silently change it → accept
```
- No truncating text or removing unknown properties.
- No replacing component types or CTA actions.
- No deleting excess components or rewriting context.
- No changing data references to hide validation failures.
The validator reports the problem without mutating the input. A separate model repair attempt is an orchestration concern: architecture permits one, while FR-03 prohibits repair. Resolve that conflict before integration.

## 10. Structured Validation Results
A useful error identifies what failed, where it failed and why. This is illustrative; the result API and stable code catalogue still need definition.
```text
INVALID
path:    /components/0/type
rule:    enum
message: Component type is outside the approved vocabulary
```
Validation outcomes concern the UISpec, never the board's PASS/FAIL disposition.

## 11. What Will Be Implemented
No files below have been implemented by this guide. These are proposed locations consistent with the planned Domain Runtime.
| File | Purpose |
|---|---|
| services/domain/validator.py | Pure validation logic and structured results |
| tests/validator/test_validator.py | Contract-focused deterministic tests |
| Test/dependency configuration | Minimal chosen tooling; no app scaffolding |
| tests/README.md | Instructions and scope for the implemented tests |
<!-- PAGE -->
## 12. The Test Suite
The future suite should cover:
- Valid cases: minimal page, all approved types, defined grid children, documented refusal and reference-based ProgressIndicator.
- Invalid cases: unknown types, extra envelope fields, wrong types, missing required fields and 0/13 normal-page entries.
- Contract-dependent cases: unknown props, CTA actions, nested children, string/size/tree limits and context rules after they are defined.
- Determinism: repeat the same valid and invalid inputs with fixed context.
- Non-mutation: UISpec and supplied context remain unchanged.
- Result shape: agreed diagnostics rather than stack traces.
**Result: not run.** The source tutorial's 24 passing tests do not describe this repository.

## 13. Task 2 Regression Check
After implementation, recheck Draft 2020-12 schema validity, all nine component types, approved examples, refusal handling and every defined property/action/child restriction.
The existing work checked JSON syntax and component-enum coverage. It did not establish a complete schema or the source tutorial's 12 passing regression checks.

## 14. What Task 3 Does NOT Build
- React application or controlled renderer.
- FastAPI application, model integration or model gateway.
- Authentication or production infrastructure.
- Physical cameras, edge image processing or real-time PLC/MES handling.
- Automated defect classification or human review/override workflows.
The BRD describes these broader business needs; this increment establishes a UI validation boundary only.

## 15. Where Task 3 Fits
```text
Probabilistic AI → Structured output → Deterministic validation
                                      ↓
                              Approved UISpec
                                      ↓
                         Controlled components → UI
```
<!-- PAGE -->
```text
Task 1 → Project Engineering Foundation
   ↓
Task 2 → Complete Machine-Checkable Model Contract
   ↓
Task 3 → Deterministic Validation Boundary
   ↓
Future → Controlled Generative UI Renderer
```
AI may propose presentation, while deterministic software controls what can proceed. The current project must first complete the missing contract definitions.

## 16. Why This Matters for AI-Native Engineering
The BRD seeks more consistent inspection, fewer escaped defects and traceable evidence (BO-01–BO-08). A presentation model must not become an ungoverned source of quality judgements or manufactured figures.
```text
Business requirements set the purpose
                 ↓
Contract defines what the model may return
                 ↓
Schema checks structure
                 ↓
Validator checks approved runtime rules
                 ↓
Renderer controls what can appear
```
UISpec validation does not establish defect-detection accuracy. Quality owns the taxonomy, severity and acceptable error rates; Manufacturing owns throughput and operational failure procedures.

## 17. Git Checkpoint
No Task 3 implementation checkpoint is claimed. Inspect the actual branch, commit and working tree during the authorised implementation. Record verification evidence before proposing a checkpoint.
```text
Implement → Verify → Review → Authorised checkpoint
```
Do not copy commit hashes or remote-synchronization claims from the onboarding guide. This document request does not authorise a commit or push.
<!-- PAGE -->
## 18. Task 3 in One Sentence
Task 3 creates the deterministic gate that checks whether an AI-generated UISpec complies with the approved board-project contract before it proceeds toward rendering.

## 19. Task 2 vs Task 3
```text
Task 2 asks:
"Is the structure correct?"

Task 3 asks:
"Does the complete UISpec obey the approved runtime rules?"
```
Both depend on a complete contract. Passing a partial schema is insufficient to approve arbitrary props or nested content.

## 20. Current Project State
| Checkpoint | Status |
|---|---|
| Task 1 — Project foundation | Documentation present |
| Task 2 — UISpec JSON Schema | Partial; gaps recorded |
| Task 3 — Validator + tests | Guide prepared; implementation not performed |
| Task 4 — Renderer increment | Not started by this work |

## 21. Beginner Takeaway
```text
Business Need → Specification → Model Contract
                                  ↓
                             JSON Schema
                                  ↓
                      Deterministic Validator
                                  ↓
                       Tests → Renderer → UI
```
We establish a controlled presentation boundary before allowing generated specifications to reach a real UI. For the Board Defect Inspection project, it must preserve domain-owned data and avoid implying a quality verdict.
<!-- PAGE -->
@ Task 3 guide adapted — ready for document review.
@ Implementation remains pending a complete, consistent contract.

**Reading this edition**
The original guide's three-part structure is preserved: beginner explanation, validator-location clarification, then the complete prompt and implementation/checkpoint discussion.

This edition follows the board BRD and the repository's currently directed read-only landing-page slice. It is not a retrospective implementation report.

The original onboarding rules of 30 nodes, 8 KiB, progress steps and generated_for are discussed in the same places, but are not promoted into board requirements without a contract decision.

The following prompt is documentation for a future task. It has not been executed as part of this request.
<!-- PAGE -->
## Documentation Clarification — Where the Python Validator Lives
The planned Task 3 increment introduces a Python validator. It is useful to identify its intended location separately from the schema and future renderer.

### The Python validator
`services/domain/validator.py` — proposed, not created.
This module belongs near the Domain Runtime and applies the approved schema and runtime rules. The original tutorial's `domain/validator.py` path is adapted to the repository's planned layout.

### The JSON Schema and Python validator work together
```text
specs/schemas/ui-spec.schema.json
                ↓
services/domain/validator.py   [planned]
                ↓
          VALID / INVALID
```
### The validator's tests
`tests/validator/test_validator.py` — proposed, not created. The suite will exercise fixed UISpec/context fixtures without calling a model or network.

### What the Python validator does not do
- It does not call AI, generate UI or render React.
- It does not replace the schema or fetch domain data.
- It does not silently repair output or decide board quality.

### How Task 2, Task 3 and Task 4 connect
| Task | Artifact or proposed location | Purpose |
|---|---|---|
| Task 2 | specs/schemas/ui-spec.schema.json | Structural contract |
| Task 3 | services/domain/validator.py | Deterministic validation |
| Task 3 | tests/validator/test_validator.py | Validation checks |
| Task 4 | apps/ui/ registry and renderer | Map approved types to known React components |
<!-- PAGE -->
### The conceptual flow
```text
AI Model
   ↓
Raw UISpec + supplied domain context
   ↓
services/domain/validator.py   [planned]
   ├── Invalid → STOP; caller handles fallback
   └── Valid
        ├── Expected refusal → fallback
        └── Normal page
              ↓
        Approved UISpec
              ↓
        Future React Renderer
```
**Architectural clarification:** a Python validator and a TypeScript renderer are not physically connected just because both are shown in a diagram. API transport and runtime wiring are later work.

The current schema cannot yet establish approval for the full component tree. Its props remain open, and the context/result policies are incomplete. The flow above represents the intended boundary after those gaps are resolved.

Under the current model contract, the Domain Runtime resolves referenced values. Architecture AD-7 instead describes model-copied metric values; this contradiction must be resolved before implementing grounding or integrating the renderer.
<!-- PAGE -->
## Complete Task 3 Record — Prompt, Implementation and Checkpoint Context
This section preserves the original guide's full prompt format and detailed follow-up record. For the board project, it is a future implementation brief rather than a claim of completed work.

## 1. Where Task 3 Starts
Task 3 requires a complete, reviewed Task 2 contract and schema. The current partial schema is not that checkpoint. Inspect actual repository state rather than assuming a tutorial commit or remote synchronization.
```text
Complete Task 2 → Implement validation → Review → Checkpoint
                                                     ↓
                                                   Task 4
```
## 2. Complete Claude Code Prompt for Task 3
The prompt below keeps the original objective, 16 numbered instructions and stopping rule, adapted to board inspection. Copy it only when authorising that future task.
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
<!-- PAGE -->
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
<!-- PAGE -->
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
<!-- PAGE -->
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
<!-- PAGE -->
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
<!-- PAGE -->
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

## 3. What This Prompt Is Intended to Build
The original guide reported completed files. For the board project these are planned artifacts, not implementation evidence.
| Artifact | Purpose | Role |
|---|---|---|
| services/domain/validator.py | Pure validation logic | Task 3 boundary |
| Package setup if needed | Minimal import/package support | Implementation detail |
| tests/validator/test_validator.py | Automated tests | Behavioural evidence |
| Test/dependency configuration | Selected validation and test tooling | Reproducibility |
| tests/README.md | Actual run instructions | Documentation |
<!-- PAGE -->
## 4. The Most Important File: services/domain/validator.py
This proposed Python module is the gatekeeper. It must not call AI, render React or make quality decisions.
```text
specs/schemas/ui-spec.schema.json
                ↓
services/domain/validator.py   [planned]
   ├── JSON Schema checks
   ├── Approved runtime limits, if defined
   └── Approved supplied-context/reference checks
                ↓
          VALID / INVALID
```
## 5. JSON Schema vs Python Validator
| Layer | Main question | Board example |
|---|---|---|
| JSON Schema | Is structure allowed? | Is type in the nine-name enum? |
| Python validator | Do approved contextual rules hold? | Is a reference allowed by supplied context, under the agreed policy? |
The runtime checker should not become a second, drifting copy of the schema.

## 6. What “Deterministic” Means Here
```text
Same UISpec + same context + same schema version
                       ↓
              Same result every time
```
No model, network, live data lookup or hidden clock belongs inside that decision.

## 7. The Node-Count Rule — Clarified
One node normally means one component instance; a complete board contract must define exactly which nested locations contain nodes. The envelope, ordinary properties and metadata are not automatically component instances.
The approved 1–12 limit is on top-level normal-page entries. The onboarding total of 30 is not adopted. Hero/InfoPanel child rules and FeatureGrid's exhaustive child restrictions remain undefined.
<!-- PAGE -->
## 8. The Serialized-Size Rule — Clarified
**Important:** 8 KiB is an onboarding-project constraint, not a universal Generative UI rule or an approved board limit.

### Relationship to Task 2 and Task 3
JSON Schema can express local string and array limits. A chosen serialized-byte rule needs an operational definition outside ordinary structural validation.
```text
JSON Schema → Structural validity
Python validator → Approved runtime and cross-field checks
```
### How size would be measured
Engineering must decide whether to measure original incoming bytes or a specified JSON serialization. If reserializing, encoding, separators and escaping affect byte count and must be consistent.
```text
UISpec
  ↓
Approved serialization/measurement policy
  ↓
Byte length compared with approved maximum
```
No board maximum or serialization policy is defined yet. Do not implement a guessed value or claim such a check exists.

### Why this matters in an AI-native system
A model can produce unexpectedly large text even with few components. Resource limits must be explicit, reviewable and tested at their boundaries. They are engineering limits, not manufacturing throughput or defect-detection thresholds.

The BRD leaves business KPIs and production constraints to stakeholder agreement. The UI validator must not substitute tutorial numbers for those decisions either.
<!-- PAGE -->
### Why both rules are useful when approved
Node count measures structure; serialized size measures the whole payload. They protect different boundaries. Neither replaces the other.
### Examples — symbolic, not approved board limits
| Total nodes | Serialized size | Outcome under a future policy |
|---|---|---|
| At or below approved N | At or below approved B | These two checks pass; other checks still apply |
| Above approved N | At or below approved B | Reject for node count |
| At or below approved N | Above approved B | Reject for size |
| Above approved N | Above approved B | Both limits violated |
N and B are explanatory placeholders, not schema fields or newly approved constants. A complete-payload limit is not a separate allowance for every node.

## 9. Context Equality
The board contract contains context with a role example but no `meta.generated_for` structure or exact echo rule. Do not import segment, product_interest or region.
Define context requiredness, role vocabulary and reference semantics first. Missing-key behaviour currently conflicts: the system specification permits omission of a missing metric component, whereas newer architecture treats ungrounded identifiers as validation failures.

## 10. URL Allow-List: Why It Is Not Added
The model contract defines no URL-bearing property or CTA action table. Do not invent fields or allow-list hosts. However, the partial schema leaves props open, so the project cannot claim URLs are structurally excluded.
Closing props and defining actions are prerequisites to a reliable statement about URL-rule applicability.
<!-- PAGE -->
## 11. Validation Means Reject — Not Repair
```text
INVALID UISpec → REJECT
                 X
No truncation, property removal or action replacement
No node deletion, reference substitution or context rewriting
```
Keep the pure validator separate from orchestration. Resolve the architecture's model-repair rule against FR-03 before any runtime integration.

## 12. Task 3 Test Result
```text
Board-project validator tests:    NOT IMPLEMENTED / NOT RUN
Complete Task 2 regression suite: NOT ESTABLISHED
Implementation checkpoint:       NOT CLAIMED
```
The original guide's 24 passing tests and 12 checks are not board-project evidence. Its listed category counts also do not add to 24; use actual future execution results.

## 13. Observations Discovered During Document Review
- Props and nested content remain open in the partial schema.
- Component properties, CTA actions and string bounds remain incomplete.
- Architecture uses component/block terminology; the contract uses type/components.
- Architecture AD-7 describes model-copied values; FR-04 and the contract require references.
- Repair, block omission and missing-reference policies conflict across files.
- Stable rejection codes are referenced but absent from the model contract.
- General implied-verdict detection is not guaranteed by a keyword test.

## 14. Architecture at the End of Task 3 — Intended
```text
PROBABILISTIC AI WORLD → Raw Model Output
                              ↓
              Deterministic Python boundary
              JSON Schema + approved runtime checks
                              ↓
                       Approved UISpec
```
<!-- PAGE -->
```text
Approved normal UISpec → Future UI Renderer
Valid refusal         → Caller selects fallback
Invalid output        → No rendering; agreed failure policy
```
This is a planned architectural boundary. Python/API/React wiring is a later increment, not something this document establishes.

## 15. What Task 3 Does NOT Build
- React application or controlled React renderer.
- FastAPI application, AI integration or model gateway.
- Authentication or production infrastructure.
- Physical camera integration or edge image processing.
- Real-time PLC/MES signals or automated defect classification.
- Human review, override or board-disposition workflows.

## 16. When Task 4 Can Begin
Task 4 can be considered only after the complete contract, implemented validator and deterministic tests have been reviewed. It is not ready merely because this guide exists.
```text
Task 2: Complete machine-checkable contract
                     ↓
Task 3: Verified deterministic validation
                     ↓
             Approved UISpec
                     ↓
Task 4: Controlled registry and renderer
```
## 17. Pre-Task-4 Checkpoint Status
The board project has no Task 3 completion evidence from this work. A later report must record actual files, commands, test outcomes, limitations and Git state. Checkpoint only after review and authorisation.
The renderer must receive a validated specification, not raw output or output accepted only by the current partial schema.
<!-- PAGE -->
## 18. Beginner Takeaway
Task 3 turns a complete written UISpec contract into executable deterministic validation. The schema defines structure, Python applies approved runtime checks, and tests demonstrate repeatable behaviour. Evaluations remain necessary for misleading composition and unsupported model claims.

For board inspection, this protects presentation without authorising the model to decide quality, invent defect categories or fabricate data. The BRD's broader inspection, evidence and human-review requirements remain distinct future work.

### Supporting documents used for this adaptation
- **Original format:** Customer_Onboarding_Task_3_Beginner_Guide_Complete.docx.pdf, pages 1–22. The supplied source is PDF, not an editable DOCX.
- **Business source:** Documents/Business Requirements Document.docx, especially BO-01–BO-08; sections 13–17 on taxonomy/performance; sections 19, 21–26 and 41 on ownership and open questions. The docs/ copy was identical at review.
- **Current slice:** docs/business-problem.md; specs/spec.md, especially FR-02–FR-06 and deferred scope; specs/model-contracts.md, sections 2–8.
- **Architecture and guidance:** CLAUDE.md and docs/architecture.md, including the documented conflicts about repair and metric values.
- **Actual schema:** specs/schemas/ui-spec.schema.json and ui-spec.schema-notes.md.
- **Supporting review:** Documents/BOARD_DEFECT_INSPECTION_TASK_2_CLARIFICATIONS.md is an unapplied proposal, not an approved amendment.
- **Alternative slice:** Documents/AI_NATIVE_GENERATIVE_UI_FIRST_IMPLEMENTATION.md proposes a review-panel registry; it does not replace the currently directed landing-page vocabulary.
- **Verification strategy:** tests/README.md and evals/README.md; their conflicting semantic, repair and value-copy assumptions need reconciliation.

**Business ownership remains unchanged.** Quality defines taxonomy, severity, ground truth and acceptable detection errors. Manufacturing defines throughput and operational response to failure. UI-generation evaluation targets are not manufacturing acceptance thresholds.

**Document status:** board-specific guide and full 16-step implementation prompt, adapted in the original three-part format. No validator, test suite, runtime dependency or application has been created by this document work.
