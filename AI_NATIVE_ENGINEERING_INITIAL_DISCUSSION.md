# AI-Native Engineering with Claude Code

## From Business Specification to a Model-Driven Board Defect Inspection System — Initial Engineering Foundation

Claude Code | CLAUDE.md | spec.md | Project Harness

This document captures the initial engineering discussion for building an enterprise AI-Based Automated Board Defect Inspection System using Claude Code from the terminal.

The first part deliberately starts with specification-driven software engineering: business problem → specification → project instructions → architecture → plan → tasks → implementation. The later sections show why this foundation must evolve when the application itself becomes model-driven and probabilistic.

**Source inputs:** `Business Requirements Document.docx` (BRD v1.0, Discovery / Business Requirements) and `AI_NATIVE_SOLUTION_ARCHITECTURE_INFOGRAPHIC.png` (proposed 11-layer edge/enterprise architecture — *proposed design, validation required*).

**Status:** Initial engineering discussion | **Version:** 1.0 | **Audience:** Solution Architecture, AI/ML, Software Engineering, Quality and Data teams

---

## 1. Key Terms Used in This Document

- **CLAUDE.md** — persistent project guidance and context for Claude Code, such as architecture, conventions, workflows and commands. It is guidance/context, not a hard enforcement mechanism.
- **spec.md** — the project's functional and non-functional specification. It is an engineering convention, not a special Claude Code filename.
- **Claude Code** — Anthropic's coding agent used from the terminal to inspect, modify, test and reason over the repository.
- **Project harness** — the surrounding repository structure, instructions, rules, tools, state and verification mechanisms that make agentic development more reliable.
- **AI-native engineering** — engineering software in which probabilistic models are first-class components, requiring model contracts, evaluation, uncertainty handling and human escalation.
- **Harness engineering** — the broader practice of designing the environment and feedback mechanisms around an agent so it can perform complex, iterative, long-running work reliably.

---

## 2. The Business Scenario Used Throughout

The running example is the board defect inspection process described in the BRD. Boards are produced on a manufacturing line and inspected at defined inspection points. The organization must capture images, analyse them, determine whether a board meets quality criteria, identify and locate defects, express confidence, route uncertain cases to human review, and retain auditable evidence.

### 2.1 The board's journey (BRD Section 7.1)

```
Board enters production
   ↓
Manufacturing processes
   ↓
Inspection point
   ↓
Image capture and inspection
   ↓
PASS / FAIL / REVIEW
   ↓
Rework / Scrap / Next stage
```

### 2.2 Capabilities in scope

- Board image capture at designated inspection points (FR-001)
- Board identification and result association (FR-002)
- Defect detection across predefined categories (FR-003)
- Board classification — PASS / FAIL / REVIEW (FR-004)
- Defect classification and localization (FR-005, FR-006)
- Confidence information for predictions (FR-007)
- Multiple defects on the same board (FR-008)
- Human review and authorized override (FR-009, FR-010)
- Inspection evidence retention and history (FR-011, FR-012)
- Model versioning, validation and governance (AI-006, AI-007, BR-004)

### 2.3 Outcome vocabulary

The BRD uses **PASS / FAIL / REVIEW**. The proposed architecture diagram uses **PASS / HOLD / REJECT** as presentation vocabulary. These are the same three dispositions:

| Architecture term | BRD / API term | Meaning |
|---|---|---|
| PASS | PASS | Approved acceptance conditions met |
| HOLD | REVIEW | Await review or exception resolution; physical hold/manual action separately approved |
| REJECT | FAIL | Defect rejection under approved quality rules |
| Gate rejection / quarantine | INVALID or UNAVAILABLE status, normally routed to REVIEW | Invalid data does not prove the board is defective |

The engineering team must pick one vocabulary for storage and API values and document the mapping. A rename after implementation requires schema migration.

---

## 3. Why the Work Starts with a Specification

Before asking Claude Code to write application code, the engineering team should establish what is being built, why it is being built, what constraints apply and how success will be verified.

This matters more than usual on this project, because the BRD is deliberately a *discovery* document. It contains 25 open questions (Q01–Q25), TBD values in every KPI row, and an explicit instruction that defect taxonomy, thresholds and ground truth are owned by the Quality and Manufacturing teams — not by the technology team. A coding agent given only "build AI board inspection" will invent exactly those missing business rules.

```
Business Problem → Specification → Project Instructions → Architecture
      → Implementation Plan → Tasks → Claude Code → Code → Tests
```

The specification prevents the coding agent from inventing business requirements and creates a durable context layer reusable across many coding sessions.

---

## 4. CLAUDE.md — Project Instructions for the Agent

CLAUDE.md should describe the project context and working conventions Claude Code should follow: project purpose, architecture principles, technology choices, coding standards, testing commands, security expectations and development workflow.

### 4.1 Recommended content

- Project purpose and business context
- Technology stack and repository structure
- Architecture principles (including the edge/enterprise split)
- Coding and testing conventions
- Security and privacy expectations
- AI/agent principles
- Human oversight requirements
- Development workflow
- Quality gates and communication expectations

### 4.2 Example initial CLAUDE.md content

```
# Board Defect Inspection AI

## Purpose
Build an enterprise board defect inspection system that combines deterministic
software controls with AI-assisted image analysis, defect classification and
risk-based disposition.

## Engineering Principles
- Prefer small, incremental changes.
- Read the relevant specification before implementing.
- Do not invent business requirements, defect definitions or thresholds.
- Keep safety-critical and line-control paths deterministic.
- AI outputs must be structured, validated and auditable.
- High-risk or uncertain decisions require human review.
- Write tests for every implemented capability.

## Domain Rules That Must Not Be Weakened
- A board containing a critical defect is never automatically PASS (BR-001).
- Low-confidence predictions route to human review (BR-002).
- Human overrides are recorded with actor and reason (BR-003).
- Only approved model versions run in production inspection (BR-004).
- Quality gates QG-1 through QG-6 are mandatory, not advisory.

## Development Workflow
1. Read CLAUDE.md.
2. Read the relevant specification.
3. Inspect the existing repository.
4. Plan the smallest complete change.
5. Implement.
6. Run deterministic tests.
7. Evaluate model-driven behaviour where applicable.
8. Report changes, tests and remaining risks.
```

> **Important:** CLAUDE.md is not itself a security boundary. If a behaviour must be technically enforced — for example, that an unapproved model cannot reach the production inference path — use permissions, hooks, application controls or platform enforcement rather than relying only on instructions.

---

## 5. spec.md — The Central Specification

`spec.md` is the central product and engineering specification. It should explain the business objective, users, workflow, functional requirements, non-functional requirements, AI requirements, acceptance criteria and scope boundaries.

### 5.1 Suggested specification contents

1. Purpose and business objective
2. Users and stakeholders
3. End-to-end inspection workflow
4. Functional requirements
5. Non-functional requirements
6. Security and privacy requirements
7. AI/model requirements
8. Human-in-the-loop requirements
9. Auditability and observability
10. Acceptance criteria
11. Out of scope

### 5.2 Example requirement, written AI-natively

A deterministic-style requirement taken straight from the BRD reads:

```
FR-003 — Defect Detection
The system shall identify predefined defect categories within the supported
inspection scope.
```

The AI-native version defines the behaviour around uncertainty, evidence and escalation:

```
FR-003 — Defect Detection

The Detection capability shall identify in-scope defect categories on a
captured board image, return a defect class, a localization region where
required, a raw score per class, and an explicit uncertainty representation.

The capability shall not convert raw scores into probabilities unless
calibration has been validated for the relevant board type, line and
operating scope.

The capability shall escalate to human review when evidence is insufficient,
contradictory, out-of-distribution, or below the approved confidence
threshold for the defect category.

The behaviour shall be evaluated against the approved evaluation dataset
using the documented per-defect recall and escalation thresholds.
```

The second version can be tested. The first cannot.

---

## 6. The Repository Structure

The repository structure should reflect the architecture. Four delivery tiers matter here, and they are not the same axis: **where code runs** (edge vs. central) and **what kind of code it is** (deterministic application vs. probabilistic model). Splitting only by location hides the application tier; splitting only by kind hides the latency boundary. The structure below keeps both visible.

```
board-defect-inspection-ai/
├── CLAUDE.md
├── README.md
├── docs/
│   ├── business-problem.md
│   ├── architecture.md
│   ├── security.md
│   └── decisions.md
├── specs/
│   ├── spec.md
│   ├── defect-taxonomy.md
│   ├── quality-gates.md
│   ├── model-contracts.md
│   ├── backend-contracts.md
│   └── decision-policy.md
├── plans/
│   └── implementation-plan.md
├── tasks/
│   └── tasks.md
├── edge/
├── backend/
├── ml/
├── frontend/
└── evals/
    ├── datasets/
    ├── scenarios/
    └── evaluation-rubric.md
```

| Directory | Owns | Layers |
|---|---|---|
| `edge/` | On-line capture, preprocessing, edge inference runtime, line adapter, local evidence and outbox | 1–2, local part of 3 |
| `backend/` | API, workflow state machine, disposition policy engine, persistence, evidence and audit store, RBAC, integration adapters (PLC / MES / Quality), action gateway | Central part of 3, plus 6, 7, 10 |
| `ml/` | Vision pipeline, specialized defect models, calibration, training, evaluation harness, model registry integration | 4–5, 8 |
| `frontend/` | Operator, inspector and manager interfaces, including the adaptive UI composition client | 11 |

Observability and hosting (Layer 9) cut across all four and are configured per environment rather than owned by one directory.

---

## 7. Starting from a Clean Project Structure

A practical terminal starting point:

```
mkdir board-defect-inspection-ai
cd board-defect-inspection-ai
git init

mkdir -p docs specs plans tasks
mkdir -p evals/datasets evals/scenarios
mkdir -p edge backend ml frontend
mkdir -p .claude

claude
```

The purpose of this first session is not to build the application. The objective is to establish the engineering foundation before implementation.

---

## 8. PROMPT 01 — Establish the Engineering Foundation

```
We are building an enterprise AI-native board defect inspection application.

The application will be model-driven. Its behaviour will therefore be
probabilistic rather than fully deterministic.

Do not write application code yet.

First help me establish the engineering foundation.

Create:
1. docs/business-problem.md
2. CLAUDE.md
3. specs/spec.md

The system must support:
- board image capture at defined inspection points
- defect detection and classification
- defect localization where required
- PASS / FAIL / REVIEW board disposition
- confidence and uncertainty reporting
- human review and authorized override
- inspection evidence, history and auditability
- controlled model versioning and deployment

Important:
This is an AI-native system.
The specification must explicitly address:
- probabilistic model behaviour
- uncertainty and calibration
- confidence thresholds
- false negatives on critical defects
- out-of-distribution boards and unknown defects
- model failure and inspection-system unavailability
- evaluation datasets
- quality thresholds
- human escalation
- model/prompt/config versioning

Constraints:
- The source BRD is a discovery document. Do not invent defect definitions,
  severity classifications, thresholds or KPI targets that it marks as TBD
  or as owned by the Quality team. Record them as open questions instead.
- Keep vendor responsibilities and client responsibilities distinct.

After creating the files, explain the decisions you made.
Do not implement the application yet.
```

---

## 9. PROMPT 02 — Hostile Architecture Review of the Specification

```
Review specs/spec.md as a hostile architecture reviewer.

Do not modify the file.

Identify:
1. Ambiguous requirements
2. Requirements that assume deterministic model behaviour
3. Requirements that cannot be verified
4. Missing AI evaluation criteria
5. Requirements that silently invent business rules the BRD left open
6. Unsafe automatic dispositions (especially automatic PASS)
7. Missing human escalation conditions
8. Missing model/config versioning
9. Missing behaviour for inspection-system unavailability
10. Requirements that need measurable acceptance criteria

For each issue explain:
- The problem
- Why it matters
- Recommended change

Do not implement anything.
```

This review is where the BRD's open questions should resurface as engineering blockers rather than quietly disappear. Expect it to flag, at minimum: undefined per-defect thresholds (Q19, Q20), undefined ground-truth ownership (Q11), undefined behaviour when AI is uncertain or unavailable (Q12, Q13), and undefined override authority (Q18).

---

## 10. PROMPT 03 — Refine the Specification for Probabilistic Behaviour

```
Based on your review, update specs/spec.md.

Convert vague AI requirements into measurable probabilistic quality
requirements where possible.

For every model-driven capability define:
- Input
- Output
- Expected behaviour
- Uncertainty behaviour
- Failure behaviour
- Evaluation metric
- Target threshold
- Human escalation condition

Where the BRD does not supply a target threshold, insert an explicit
placeholder marked as an open question with a named owner. Do not
substitute an industry default.

Do not introduce requirements that cannot realistically be evaluated.

After updating the specification, provide a summary of the changes.
```

### 10.1 Supplied recall targets — handle with care

The architecture diagram supplies per-defect recall targets. They are explicitly labelled *"Pending Quality confirmation — not measured results."* They must enter the specification as **supplied design targets**, not as validated performance or contractual acceptance criteria:

| Defect type | Supplied minimum recall | Status |
|---|---|---|
| Missing component | 99.5% | Supplied — pending Quality confirmation |
| Wrong component | 99.0% | Supplied — pending Quality confirmation |
| Misaligned component | 98.5% | Supplied — pending Quality confirmation |
| Solder bridge | 99.5% | Supplied — pending Quality confirmation |
| Damaged component | 98.0% | Supplied — pending Quality confirmation |
| Scratch | 95.0% | Supplied — pending Quality confirmation |

The corresponding BRD defect taxonomy (D001–D006) is also explicitly marked "examples only — the manufacturing/quality team must define the actual taxonomy."

---

## 11. PROMPT 04 — Create the Evaluation Rubric

```
Read:
  CLAUDE.md
  specs/spec.md

Create:
  evals/evaluation-rubric.md

Define the evaluation strategy for:
1. Image/capture quality assessment
2. Defect detection and classification
3. Defect localization
4. Calibration and uncertainty
5. Board-level disposition (PASS / FAIL / REVIEW)

For each capability define:
- Evaluation objective
- Test scenarios
- Metrics
- Thresholds
- Critical failures
- Human escalation requirements

Separate:
A. Deterministic tests
B. Semantic/model evaluations
C. Safety evaluations
D. Workflow/trajectory evaluations

Treat a false negative on a critical defect as a distinct, separately
reported critical failure — not as one error among many.
```

---

## 12. PROMPT 05 — Create the Golden Evaluation Dataset

```
Using specs/spec.md and evals/evaluation-rubric.md,
create an initial golden evaluation dataset definition.

Create:
  evals/datasets/board_inspection_cases.json

Include representative scenarios for:
- clean board, no defect
- single critical defect (missing component)
- single critical defect (solder bridge)
- major defect (misaligned component)
- minor defect (surface scratch)
- multiple defects on one board
- rare defect with very few training examples
- board variant or revision not seen in training
- poor image quality (blur, occlusion, reflection)
- incorrect or missing board identifier
- lighting variation outside the normal range
- ambiguous case where inspectors historically disagreed

For each case define:
- input
- relevant context (board type, revision, line, inspection point)
- expected behaviour
- expected escalation
- evaluation criteria

Do not invent real defect tolerances or quality rules.
Keep the dataset clearly marked as synthetic development/test data until
the Quality team supplies the authoritative ground truth.
```

The BRD is explicit that ground truth is a business asset: *"The AI team should not be expected to determine business definitions of defects."* The golden dataset is scaffolding until Quality signs it off.

---

## 13. PROMPT 06 — Define Model and Service Contracts

```
Read the specifications and evaluation rubric.

Create:
  specs/model-contracts.md
  specs/backend-contracts.md

In model-contracts.md define contracts for:
1. Image Quality model (ingestion gate)
2. Detection and Classification model (vision pipeline)
3. Localization output
4. Calibration and Uncertainty component
5. Review Prioritisation model (if used)
6. Adaptive UI composition model (if used)

For every model component specify:
- Purpose
- Inputs
- Outputs
- Allowed tools/actions
- Forbidden actions
- Uncertainty representation
- Failure behaviour
- Escalation behaviour
- Evaluation criteria

In backend-contracts.md define the deterministic services that enforce
those contracts:
1. Inspection API and workflow state machine
2. Disposition policy engine
3. Action gateway (authorization and execution boundary)
4. Evidence, decision-record and audit persistence
5. Integration adapters (PLC, MES, Quality system)

For every backend service specify:
- Purpose
- Interface and callers
- Authorization rules
- State transitions owned
- Invariants it must enforce
- Failure behaviour and idempotency
- Audit obligations

Note explicitly which components are models and which are deterministic
services. The decision/disposition engine is a deterministic policy
component, not a model. Every "forbidden action" in model-contracts.md
must name the backend service that enforces it; a forbidden action with
no named enforcer is an open issue, not a control.
```

A model contract that says a component "must not issue the final disposition" is a statement of intent. It becomes a control only when a named service refuses to accept a disposition from that component. That mapping is the point of writing the two contract files together.

### 13.1 Example — Detection model contract

- **Purpose:** identify in-scope defect categories on a captured board image and localize them where required.
- **Inputs:** validated board image, board identifier, board type/revision context, inspection point metadata.
- **Outputs:** defect classes, localization regions, raw per-class scores, uncertainty representation, model and preprocessing version.
- **Allowed:** analyse the supplied image, report detected defects, report low confidence, report out-of-distribution input.
- **Forbidden:** issue the final board disposition, signal the PLC directly, suppress a detection to meet a throughput target, or invent a defect category outside the approved taxonomy.

### 13.2 Example — Decision engine (deterministic, not a model)

- **Purpose:** convert calibrated risk into PASS / FAIL / REVIEW under approved, versioned business policy.
- **Inputs:** calibrated detection evidence, validated board context, product-specific policy and thresholds.
- **Outputs:** disposition, decision record with evidence, reasoning, policy version and model version.
- **Forbidden:** automatically PASS a board carrying a critical defect (BR-001); act on unvalidated context; run an unapproved model version (BR-004).

### 13.3 Example — Backend action gateway (deterministic service)

- **Purpose:** the single boundary through which any state change or physical effect is authorized and executed.
- **Interface and callers:** the adaptive UI, the edge line adapter and internal workflow services. No model component is a permitted caller.
- **Authorization rules:** re-authorize the acting user against role and line scope at the moment of submission; never trust authorization implied by what the UI rendered.
- **Invariants enforced:** the record version and board state are still current and the action has not expired; the disposition came from the policy engine, not from a model output; a critical-defect board cannot be released as PASS; the acting model version is on the approved list.
- **Failure behaviour and idempotency:** commands carry a command ID and are delivered once logically; a retry reconciles state rather than repeating a physical action; an unacknowledged command resolves to an explicit UNKNOWN outcome requiring reconciliation, never a blind repeat.
- **Audit obligations:** persist actor, role, timestamp, prior and new state, reason, policy version and model version before the effect is considered complete.

This is the service that makes §13.1's *"Forbidden: issue the final board disposition, signal the PLC directly"* real. Without it, that line is documentation.

---

## 14. PROMPT 07 — Design the Enterprise Architecture

```
Read:
  CLAUDE.md
  docs/business-problem.md
  specs/spec.md
  specs/model-contracts.md
  specs/backend-contracts.md
  evals/evaluation-rubric.md

Create:
  docs/architecture.md

Design an enterprise architecture for the system.

Explicitly separate:
1. Deterministic application components (the backend tier)
2. Probabilistic model components
3. Edge (on-line, low-latency) versus central execution
4. Evaluation
5. Human decision points
6. Security controls
7. Observability

Specify the backend tier concretely, not as an implied middle:
- API surface and the workflow state machine that owns disposition state
- Where the policy engine runs and how policy versions are pinned
- Persistence model for inspection records, evidence and the audit trail
- Authorization model (user, role, line/site scope) and where it is enforced
- The action gateway and its idempotency and reconciliation behaviour
- Integration adapters for PLC, MES and the Quality system
- Messaging and the outbox pattern for edge-to-central delivery

Identify which decisions must remain deterministic and which can be
model-driven.

Address explicitly:
- what happens when the inspection system is unavailable
- what happens when the edge is disconnected from the central platform
- whether a local disposition may be issued, and under what preconditions
- how a central re-analysis relates to a disposition already acted upon

Implementation stack is already selected in PRODUCT_BACKLOG.md
(Angular/TypeScript, Java/Spring Boot, Python/ONNX Runtime, PostgreSQL,
S3-compatible object storage, RabbitMQ, NGINX, enterprise OIDC, managed
Linux VMs). Design within it; do not re-litigate the stack, and do not
introduce new infrastructure without recording the reason in
docs/decisions.md.

Do not implement code.
```

> **Note on the stack.** The technology choices above are cited because the delivery backlog has already committed to them, not because this discussion selects them. The BRD is explicit that the BA team should not prescribe technology (BRD §46); that boundary is respected by treating the stack as an existing organizational constraint rather than a fresh architectural decision.

### 14.1 The layered reference architecture

The proposed design organizes the system into eleven logical layers with six mandatory quality gates. Layers 1–2 execute at the edge; layer 3 spans edge and enterprise; layers 4–8 are principally enterprise with edge-deployed models; layers 9–11 are cross-cutting.

| # | Layer | Gate |
|---|---|---|
| 1 | Data Capture & Ingestion (edge) | QG-1 Ingestion Quality |
| 2 | Edge AI Processing (on-site, low-latency) | QG-2 Edge Quality |
| 3 | Context & Reference (edge + enterprise) | QG-3 Context Quality |
| 4 | AI Model Layer (orchestration, vision pipeline) | — |
| 5 | Probabilistic Reasoning & Risk | — |
| 6 | Decision Layer (policy-based disposition) | QG-4 Decision Quality |
| 7 | Human-in-the-Loop (review, annotation) | QG-5 Label Quality |
| 8 | Model Lifecycle & MLOps | QG-6 Evaluation Quality |
| 9 | Observability, Operations & Hosting | — |
| 10 | Governance, Security & Compliance | — |
| 11 | Adaptive UI (AI-rendered interface) | — |

The six gates answer six questions: Is the input valid? Is the inference reliable? Is the context complete? Is the decision justified? Are the labels verified? Is the model ready for release?

---

## 15. PROMPT 08 — Build an Incremental Implementation Plan

```
Read all current project documentation.

Create:
  plans/implementation-plan.md

Break implementation into incremental vertical slices.

Each slice must:
- deliver usable functionality
- have deterministic tests
- have AI evaluations where applicable
- have acceptance criteria
- identify model dependencies
- identify security risks
- identify which quality gates it implements

Sequence the slices so that the deterministic evidence, audit and disposition
path exists before any automatic physical action is enabled.

Do not create one giant implementation phase.
```

---

## 16. PROMPT 09 — Convert the Plan into Executable Tasks

```
Create tasks/tasks.md from the implementation plan.

Every task must contain:
- Task ID
- Objective
- Specification reference
- Dependencies
- Acceptance criteria
- Tests
- AI evaluation requirements
- Security considerations
- Quality gate affected
```

---

## 17. PROMPT 10 — Implement One Vertical Slice

```
Implement TASK-001.

Before writing code:
1. Read CLAUDE.md.
2. Read the referenced specification.
3. Read docs/architecture.md.
4. Inspect the existing repository.
5. Identify dependencies.

Then:
1. Implement the smallest complete vertical slice.
2. Write deterministic tests.
3. Run the tests.
4. Validate against the acceptance criteria.

Do not modify unrelated files.

After implementation report:
- Files changed
- Requirements satisfied
- Tests executed
- Test results
- Remaining risks
```

---

## 18. What Changes When the Application Becomes Model-Driven?

The first ten prompts establish a strong conventional engineering workflow. However, an AI application cannot be engineered as though every function returns a predictable result. Model outputs vary with model version, preprocessing, camera and lighting conditions, board variant, context and input characteristics.

```
Traditional deterministic function:
  input → function → expected output

Model-driven component:
  image + context + model + preprocessing
      → probabilistic output
      → validation / evaluation
      → accept / re-capture / escalate
```

The engineering equation becomes:

```
Application behaviour = Code + Model + Preprocessing + Context + Calibration + Data
```

This is why the BRD's instruction to report precision, recall, F1, false-positive rate, false-negative rate and per-defect performance — rather than a single "accuracy" figure — is an engineering requirement, not a reporting preference.

---

## 19. Deterministic vs Probabilistic Boundaries

A central architecture principle is to keep critical controls and state transitions deterministic while allowing models to handle bounded probabilistic tasks.

```
Board → Camera → Edge Capture → Workflow Controller
   │
   ├── Deterministic:
   │     authentication
   │     RBAC
   │     workflow state
   │     board identity association
   │     disposition policy and thresholds
   │     PLC signalling and interlocks
   │     evidence persistence
   │     audit trail
   │
   └── Probabilistic:
         image quality assessment
         defect detection
         defect classification
         localization
         uncertainty estimation
         review prioritisation
   │
   ▼
Evaluation
   ├── acceptable   → continue
   └── uncertain    → human review
```

On this project the boundary has a physical consequence: a probabilistic component must never actuate the line directly. The proposed design states this explicitly — *"no direct inference-to-PLC shortcut"* and *"persist before action."* Evidence is durably recorded before any physical action, and a disposition is mapped to an approved physical procedure rather than dispatched straight from an inference result.

Everything in the left-hand column above belongs to one component. It has a name, and the next section gives it one.

---

## 20. The Backend — Deterministic Spine and Action Gateway

In a model-driven architecture it is easy to describe the system as layers of models and lose the application tier entirely. That would be a serious error here. The backend is not the part left over once the interesting AI work is removed; it is the component that makes every constraint in this document enforceable.

### 20.1 What the backend owns

| Responsibility | Why it cannot live in a model | Layer |
|---|---|---|
| Authentication, RBAC, line/site scoping | Permission is not a prediction | 10 |
| Inspection workflow state machine | A board is in exactly one state; state is not probabilistic | 6 |
| Disposition policy engine and thresholds | Policy is approved, versioned business rule, not learned behaviour | 6 |
| Board identity association | An inspection result bound to the wrong board is worse than no result | 1, 6 |
| Evidence, decision-record and audit persistence | Auditability requires durability guarantees a model cannot offer | 10 |
| Action gateway to PLC / line control | Physical effect requires authorization, idempotency and reconciliation | 6, edge |
| Integration adapters (MES, Quality system) | Contracts with external systems are fixed, not inferred | Integration |
| Review queue and assignment | Who reviews what is an operational rule | 7 |

### 20.2 The enforcement relationship

Model contracts (§13) list forbidden actions. The backend is what refuses them. Read the two together:

```
Model contract says                    Backend service enforces
─────────────────────────────────────  ──────────────────────────────────────
Detection must not issue the           Only the policy engine may write a
final disposition                      disposition to the state machine

Detection must not signal the PLC      Only the action gateway may emit a
directly                               line command, and only from a
                                       persisted disposition

UI model must not grant permission     Action gateway re-authorizes the user
                                       at submission, ignoring what was
                                       rendered

No unapproved model in production      Inference path checks the registry's
                                       approved-version list before use

Critical defect is never auto-PASS     Policy engine rejects the disposition;
(BR-001)                               gateway rejects the release command
```

A forbidden action with no named enforcing service is an open issue, not a control. This is the single most useful review question to ask of the architecture document produced by PROMPT 07.

### 20.3 Why this gets stronger, not weaker, as the AI gets better

A common assumption is that a more capable model needs less deterministic scaffolding. The opposite holds for this system. As the model takes on more of the inspection judgement, the consequences of an unbounded action grow, and the value of a narrow, auditable execution boundary grows with it. The backend is what allows the model to be improved, replaced, rolled back or run in shadow mode without renegotiating who is allowed to reject a board.

This is also what makes the Layer 11 principle — *"the UI model composes presentation; users authorize actions"* — implementable rather than aspirational. The adaptive UI can render anything it likes; nothing happens until an authenticated user submits an action that the gateway independently re-authorizes.

---

## 21. Evaluation Becomes a First-Class Engineering Layer

- **Deterministic tests** verify code, schemas, APIs, state transitions and PLC message contracts.
- **Semantic/model evaluations** assess whether detection, classification and localization outputs meet quality expectations.
- **Safety evaluations** test critical-defect false negatives, out-of-distribution boards, unknown defects, degraded images and unsafe automatic dispositions.
- **Workflow/trajectory evaluations** assess whether the system follows the intended gate sequence and escalates correctly.
- **Golden datasets** provide repeatable scenarios against which model, preprocessing and threshold changes can be compared.

Example evaluation repository:

```
evals/
├── datasets/
│   ├── board_inspection_cases.json
│   ├── critical_defect_cases.json
│   └── calibration_cases.json
├── expected/
│   └── expected_behaviour.json
├── scenarios/
│   ├── degraded-image.md
│   ├── unseen-board-revision.md
│   ├── rare-defect.md
│   ├── multiple-defects.md
│   └── inspection-system-unavailable.md
└── evaluation-rubric.md
```

---

## 22. Why the Specification Must Evolve

A deterministic requirement might say:

```
The system shall detect a missing component.
```

An AI-native requirement defines the behaviour around uncertainty:

```
The Detection capability shall detect a missing component on a supported
board type and revision, return a localization region, retain an evidence
reference, represent uncertainty explicitly, and escalate when the evidence
is insufficient, contradictory or out-of-distribution.

The behaviour shall be evaluated against the approved evaluation dataset
using the documented per-defect recall and escalation thresholds, and a
false negative on a critical defect shall be reported as a critical failure.
```

---

## 23. The Three-Layer Model

```
Layer 1 — Claude / Model
  Probabilistic reasoning engine

Layer 2 — Claude Code
  Development agent that reads the repository, edits files,
  runs tools/tests and iterates on the software

Layer 3 — Runtime System
  Probabilistic: Image Quality model, Detection model, Calibration component
  Deterministic: backend workflow state machine, policy engine and action
  gateway, which own every state change and physical effect
```

Layer 2 builds the system. Layer 3 runs it. Conflating them is a common and expensive mistake: the coding agent's autonomy in the repository says nothing about how much autonomy a runtime model should have over a production line.

---

## 24. Harness Engineering — Where It Fits

The initial project foundation should not be confused with a commercial product called Harness. In this context, harness engineering means deliberately designing the environment around the coding/agent system so that it can work iteratively and reliably.

```
        CLAUDE CODE / AGENT
                │
   ┌────────────┼────────────┐
   │            │            │
Context       Tools        State
CLAUDE.md     Terminal     Progress
specs         Filesystem   Artifacts
architecture  Tests        Evaluations
   │            │            │
   └────────────┼────────────┘
                │
            IMPLEMENT
                │
             VERIFY
                │
            EVALUATE
                │
   Continue / Correct / Escalate
```

CLAUDE.md and the specification remain valid and important. They form part of the project context and engineering foundation, while the broader harness includes the mechanisms that provide context, tools, state, verification, feedback and controlled iteration.

---

## 25. Recommended End-to-End AI-Native Engineering Lifecycle

```
Business Problem
   → Specification
   → Model Contracts
   → Golden Dataset
   → Architecture
   → Implementation Plan
   → Tasks
   → Claude Code
   → Implement
   → Deterministic Tests
   → AI Evaluations
   → Quality Gate
   → Deploy (shadow → staged → production)
   → Observe
   → Production Failure / New Case
   → New Evaluation Case
   → Claude Code
   → Improve
```

This mirrors the model lifecycle the BRD already requires — development, validation, business/quality approval, deployment, monitoring, performance review, retraining, revalidation, new version — with the evaluation dataset as the artifact that connects a production failure back to an engineering change.

---

## 26. Key Engineering Messages

1. Do not start an enterprise AI build by asking Claude Code to generate the whole application.
2. Start with the business problem and a specification.
3. CLAUDE.md tells Claude Code *how* the project should be approached; spec.md defines *what* should be built.
4. The project repository becomes part of the agent's working context.
5. Once models become first-class components, deterministic unit tests alone are insufficient.
6. AI behaviour must be specified in terms of uncertainty, evidence, evaluation and escalation.
7. Critical business controls — disposition policy, interlocks, audit, PLC signalling — should remain deterministic, and they belong to a named backend tier rather than being distributed across the model layers.
8. Models should operate inside explicit contracts and bounded workflows, with no direct path to physical action. A forbidden action in a model contract is only a control once a backend service is named as its enforcer.
9. Evaluation datasets and rubrics must become first-class engineering assets, owned jointly with the Quality team.
10. Harness engineering is the broader discipline of making agentic work reliable through context, tools, state, verification and feedback.
11. Where the BRD is silent, the correct engineering output is an open question with a named owner — not an assumed default.

---

## 27. Final Mental Model

```
Specification-Driven Engineering
   ↓
Claude Code Project Foundation
   ↓
Model-Driven Software
   ↓
AI-Native Engineering
   ↓
Harness Engineering
   ↓
Reliable Long-Running Agentic Work
```

---

## Appendix A — Suggested First Files to Create

- `CLAUDE.md`
- `README.md`
- `docs/business-problem.md`
- `docs/architecture.md`
- `docs/security.md`
- `docs/decisions.md`
- `specs/spec.md`
- `specs/defect-taxonomy.md`
- `specs/quality-gates.md`
- `specs/model-contracts.md`
- `specs/backend-contracts.md`
- `specs/decision-policy.md`
- `plans/implementation-plan.md`
- `tasks/tasks.md`
- `evals/evaluation-rubric.md`
- `evals/datasets/board_inspection_cases.json`

---

## Appendix B — Practical Rule for a Claude Code Session

```
Before implementation:
  READ → UNDERSTAND → PLAN → IMPLEMENT → TEST → EVALUATE → REPORT

Never:
  PROMPT → GENERATE EVERYTHING → ASSUME IT WORKS
```

---

## Appendix C — Open Items Carried Into Engineering

These are carried from the BRD and the proposed architecture. They are engineering blockers, not documentation gaps, because each one changes what gets built.

| # | Open item | Source | Owner |
|---|---|---|---|
| 1 | Authoritative defect taxonomy and severity classification | BRD §13, §14 (marked "examples only") | Quality |
| 2 | Acceptable false-negative and false-positive rates per defect | BRD Q19, Q20 | Quality |
| 3 | Confirmation of the supplied per-defect recall targets | Architecture diagram (marked pending) | Quality |
| 4 | Ground-truth ownership and inspector-disagreement resolution | BRD §19, Q11 | Quality |
| 5 | Behaviour when the AI result is uncertain | BRD Q12 | Quality |
| 6 | Behaviour when the inspection system is unavailable | BRD §23, Q13 | Manufacturing |
| 7 | Whether an immediate PASS/FAIL signal to the line is required | BRD Q14, Q15 | Automation |
| 8 | Production rate, inspection window and maximum latency | BRD §21, Q05, Q06 | Manufacturing |
| 9 | Board variants, revisions and whether both sides are inspected | BRD Q07, Q08 | Manufacturing |
| 10 | Volume, labelling status and quality of historical images | BRD §18, Q09, Q10 | Data |
| 11 | Image and result retention periods | BRD §26, Q17 | Quality / Compliance |
| 12 | Override authority and approval rights for models and thresholds | BRD §29, Q18 | Quality / Security |
| 13 | Retry/re-capture bounds and terminal action once exhausted | Architecture diagram (bound not stated) | Solution Architecture |
| 14 | Review/escalation SLA before a held board is force-dispositioned | Architecture diagram (no SLA stated) | Quality / Manufacturing |
| 15 | Conflict handling when central re-analysis disagrees with an edge disposition already acted upon | Architecture diagram | Solution Architecture |

---

*End of initial discussion document.*

*Derived from `Business Requirements Document.docx` (v1.0, discovery status) and `AI_NATIVE_SOLUTION_ARCHITECTURE_INFOGRAPHIC.png` (proposed design, validation required). Related engineering artifacts in this repository: `AI_NATIVE_USER_JOURNEYS_WORKFLOWS_GAPS.md`, `AI_NATIVE_END_TO_END_WORKFLOW.md`, `AI_NATIVE_GAP_ANALYSIS.md`.*
