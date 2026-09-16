# AI-Native Engineering — First Implementation Scenario

## Controlled Generative UI for the Inspector Review Panel

Beginner-friendly guide to Harness, Claude Code, Generative UI, Model Contracts, Tests, Evals and Feedback — mapped to the Board Defect Inspection System.

> **Scenario context.** This is the first implementation slice of the AI-Based Automated Board Defect Inspection System. It is deliberately read-only: it composes a review surface over a **recorded inspection fixture** supplied by `simulators/capture/`. No camera, no PLC, no production line and no live model inference are required. Nothing in this slice can change the state of a board.

**Companion document:** `AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md` — the engineering foundation, architecture views and full repository structure. This document implements the first feature inside that structure.

**Version:** 1.0 | **Status:** Draft for review

---

## 1. What Are We Building?

Our first implementation scenario is intentionally small. We are not building the complete inspection platform yet. We will build the **inspector review panel** as a controlled Generative UI experience, rendered over a recorded inspection result. This feature becomes our laboratory for learning AI-native engineering and harness engineering with Claude Code.

```
Inspector
   ↓
Board Defect Inspection Web Application
   ↓
Inspection Review Panel
   ↓
Controlled Generative UI
   ↓
Recorded inspection fixture (simulators/capture/)
```

---

## 2. Why Start With the Review Panel?

The reference guide for this series starts with a customer landing page, because a landing page is visible, understandable and small. This domain has no landing page — there is no customer, and the first screen an operator sees is not where the interesting behaviour lives.

The review panel is the closest equivalent: it is visible, it is meaningful to a real user, and it exercises exactly the machinery we need to learn — model, UI specification, validator, approved catalogue, renderer and fallback.

It has one apparent problem. A landing page needs nothing upstream; a review panel looks like it needs the whole inspection pipeline — camera, edge inference, calibration, decision policy. **It does not, if we feed it a recorded inspection fixture.** `simulators/capture/` already exists in our structure for precisely this reason, and using it here is not a shortcut around the real system — it is the project's own deliberate test double, doing the job it was created for.

---

## 3. Controlled Generative UI

Generative UI means an AI model can help decide what interface should be presented. In an enterprise application — and emphatically in one attached to a production line — we do not give the model unrestricted permission to generate and execute arbitrary HTML, JavaScript or application logic.

```
AI Model
   ↓
UI Specification / Intent
   ↓
UI Validator
   ↓
Approved Component Registry
   ↓
UI Renderer
   ↓
Browser
```

---

## 4. What Will the Review Panel Contain?

The first version shows an inspector a single recorded inspection: which board it was, what the captured image looks like against its reference, what was detected and where, how confident the result was, and the fields a reviewer would fill in.

The visual design can evolve. The important part is that the composition is produced through a controlled UI specification rather than a hand-written page.

**It will not contain a disposition control.** See §7.

---

## 5. What Does the AI Model Generate?

The model does not generate a component file. It generates structured data describing the intended UI — a UI schema, UI specification, or UI intent.

```
{
  "view": "inspection_review",
  "context": {
    "board_ref": "attempt-2f91c4",
    "board_type": "REV-C",
    "line": "L2",
    "role": "inspector"
  },
  "components": [
    { "type": "BoardSummary",    "source": "attempt.metadata" },
    { "type": "ImageCompare",    "mode": "reference_vs_captured" },
    { "type": "DefectOverlay",   "source": "attempt.detections" },
    { "type": "ConfidenceBadge", "source": "attempt.calibrated_score" },
    { "type": "ReviewPanel",     "fields": ["defect_class", "reason_code", "notes"] }
  ]
}
```

Note what the specification contains and what it does not. Every component names a **reference** to evidence — `attempt.detections`, `attempt.calibrated_score` — and the backend resolves those references to actual values at render time. The model never carries the numbers a person will act on. A model that could pass through a confidence value could pass through the wrong one.

---

## 6. Why Generate a UI Specification Instead of Code?

A structured specification gives the application a deterministic control point. The model describes what it would like displayed; the application decides whether that request is valid and how it is rendered.

```
AI output
   ↓
Schema validation
   ↓
Approved component?
   ↓
Evidence reference in the viewer's scope?
   ↓
Valid structure?
   ↓
Render known components with backend-resolved data
```

---

## 7. Approved Component Vocabulary for v1

The application maintains a small registry of components the model may request. For the first version:

```
BoardSummary       ImageCompare       DefectOverlay
ConfidenceBadge    ReviewPanel        Heading
Text               Alert              EscalationNotice
```

**`DispositionControl` is deliberately excluded from v1.** The companion document's §22.3 lists it in the eventual catalogue, and §22.4 shows it in a target UI contract — that is the destination, not the first slice.

Leaving it out is the decision that keeps this slice as safe as a landing page while still exercising the full mechanism. Rendering a disposition control that does nothing would be worse than omitting it: an inert control on a review screen is a misleading interface, and misleading interfaces are the specific failure this whole approach exists to prevent. Adding it later is a deliberate governance event that brings authentication, attribution and the backend action gateway with it.

The approved catalogue is a governance artifact. It grows on purpose, never by convenience.

---

## 8. What Happens When Model Output Is Invalid?

Suppose the model requests an unsupported component — `execute_query`, or a `DispositionControl` that is not in the v1 registry. The renderer does not know it and will not allow it. Validation rejects the specification and the application falls back safely.

```
Model
  ↓
Invalid UI specification
  ↓
Validator
  ↓
REJECT
  ↓
Standard review UI (fallback)
```

Rejection is not an error to hide. The fallback is a plain, hand-built review screen that shows the same evidence. An inspector must always be able to finish looking at a board, whether or not the composition model is working. **Degraded composition must never become degraded capability.**

---

## 9. The Model Contract

Before implementing model integration we define what the model is expected to do and what it is prohibited from doing. This contract lives in `specs/model-contracts.md`.

```
Purpose:
  Generate a structured description of the inspection review view
  for a given recorded inspection and viewer role.

Inputs:
  - Inspection attempt reference and metadata
  - Detection evidence references
  - Viewer role and line/site scope
  - Available UI components
  - UI layout policy

MAY:
  - Select and order approved components
  - Choose which evidence references are most relevant to the case
  - Generate neutral explanatory and label text
  - Adapt the layout to the viewer's role
  - Signal that a case looks ambiguous and may need escalation

MUST NOT:
  - Generate executable JavaScript or arbitrary HTML
  - Request components outside the approved catalogue
  - Supply evidence values directly instead of references
  - State, imply or recommend a disposition
  - Describe confidence in words that contradict the calibrated score
  - Invent defect categories outside the approved taxonomy
  - Access the database, model registry or line equipment
  - Request any action control in v1
```

Two of these are specific to this domain and would not appear in a landing-page contract. *Must not imply a disposition* exists because the model composes the screen on which a disposition is eventually made, and a layout can editorialize without ever naming a verdict. *Must not contradict the calibrated score* exists because the system spent an entire architecture layer (Layer 5) turning raw scores into honest probabilities, and a presentation layer that describes a 0.61 result as "clear" has quietly discarded that work.

---

## 10. Why the Model Contract Matters

A prompt alone is not a sufficient engineering design for a model-driven system. The contract gives us a target for implementation, testing, evaluation and governance.

```
Specification → Model Contract → Implementation
                       ↓
                 Tests + Evals
                       ↓
                   Feedback
```

A prohibition is only a control when something enforces it. Each `MUST NOT` above maps to an enforcement point: catalogue membership and schema validation are enforced by the renderer; evidence scope is enforced by the backend resolving references against the viewer's permissions; and "must not imply a disposition" is enforced by evaluation cases, because no validator can detect it.

That last one is worth sitting with. Some constraints can be enforced structurally and some can only be measured. Knowing which is which tells you where you need evals rather than tests.

---

## 11. The Harness

The harness is the engineering environment around Claude Code — project context, instructions, constraints, verification mechanisms and state — so it can work effectively over many iterations.

For this slice, the relevant part of the repository is small:

```
board-defect-inspection/
├── CLAUDE.md
├── .claude/
│   ├── rules/
│   └── settings.json
├── docs/
│   ├── business-problem.md
│   └── architecture.md
├── specs/
│   ├── spec.md
│   ├── model-contracts.md
│   └── ui-contract.md
├── policies/
│   └── ui-layout-policy.md
├── contracts/
│   └── ui/
├── frontend/src/
│   ├── views/
│   ├── components/approved/
│   ├── renderer/
│   └── fallback/
├── backend/api/review/
├── ai/uigen/
├── simulators/capture/
├── tests/
└── evals/
    ├── ui-composition/
    └── evaluation-rubric.md
```

Every directory here already exists in the full structure. We are not creating a special layout for the first slice; we are using a narrow slice of the real one.

---

## 12. What Each Harness Element Means

| Element | Beginner explanation | Role here |
|---|---|---|
| `CLAUDE.md` | Persistent project guidance for Claude Code | How Claude should work |
| `specs/spec.md` | Description of what we are building | What the review panel must do |
| `specs/model-contracts.md` | Expected and prohibited model behaviour | What the UI model may do |
| `specs/ui-contract.md` | The UI specification schema | The shape of valid model output |
| `policies/ui-layout-policy.md` | Business-owned composition rules | What may be composed, per role |
| `.claude/` | Rules, hooks and permissions | Engineering controls that act, not advise |
| `simulators/capture/` | Recorded inspection fixtures | Lets the slice run without a factory |
| `tests/` | Deterministic checks | Renderer and application correctness |
| `evals/` | AI behaviour checks | Composition quality |

---

## 13. Claude Code's Role

Claude Code is the AI software-engineering agent that creates and improves the project. It is not the runtime model that composes the review panel.

```
ENGINEERING TIME
Harness → Claude Code → Code → Tests / Evals

RUNTIME
Inspector → Web App → UI Runtime → UI Model → Controlled UI
```

Confusing these two is the most common and most expensive mistake available here. Claude Code's broad autonomy in the repository says nothing about how much autonomy the runtime model should have over an inspection screen.

---

## 14. Authentication and Attribution in the First Scenario

The reference guide defers authentication for its first scenario because the application is internal. We can defer it too — but for a narrower reason, and with a firm boundary.

This slice is **read-only**. Nothing it renders can change the state of a board, so there is no action to attribute to anyone. On that basis, the first iteration need not spend itself on login screens, session management or user administration.

That reasoning expires precisely when `DispositionControl` enters the catalogue. The review surface requires every mutation to be attributed to a named user (companion document §21.4), so the slice that introduces a disposition introduces authentication, attribution and the backend action gateway in the same step. These are not separable, and deferring them past that point is not a scheduling choice but a defect.

---

## 15. First Runtime Architecture

Keep the runtime for this slice deliberately small. A database is not required until the feature needs persistence.

```
Browser
  ↓
Web Frontend (UI Runtime)
  ↓
Backend review API (Domain Runtime)
  ↓            ↓
AI Runtime     simulators/capture/
(ai/uigen)     recorded inspection fixture
```

No edge tier. No PLC adapter. No decision path — because there is no decision. The pieces omitted here are omitted because this slice genuinely does not need them, not because they are inconvenient.

---

## 16. Frontend and Backend Still Exist

We are not replacing conventional frontend/backend architecture. The frontend remains the practical frontend and the backend services remain the backend. Runtime terminology (UI Runtime, Domain Runtime, AI Runtime) is an additional logical view over the same system, exactly as set out in the companion document §19.

The technology stack for this project is an open decision (companion document, Appendix C #16). Build the slice so that decision stays substitutable.

---

## 17. Incremental Implementation Strategy

We do not ask Claude Code to build the feature in one request. It decomposes into small, verifiable increments:

1. Repository foundation and harness files
2. Slice specification
3. Model contract and UI specification schema
4. Recorded inspection fixture in `simulators/capture/`
5. Application shell and the standard fallback review screen
6. Approved component registry
7. UI specification validator
8. Generative UI renderer
9. Model integration in `ai/uigen/`
10. Review panel composition end to end
11. Deterministic tests
12. AI evaluation cases and the runner wired into CI
13. Run evals and improve

Steps 5 and 6 are ordered deliberately. **The fallback screen is built before the generative path**, so the system is useful before it is clever, and so the fallback is never a hurried afterthought written under pressure once generation is already failing.

---

## 18. Why Incremental Implementation Matters

Small increments make failures easier to diagnose, allow every change to be tested, create a meaningful Git history, strengthen the harness gradually, and make evaluation feedback actionable.

---

## 19. Deterministic Tests

Traditional tests check predictable behaviour.

```
GIVEN a valid UI specification
WHEN the renderer processes it
THEN BoardSummary, ImageCompare, DefectOverlay and ReviewPanel render
AND every displayed value came from backend-resolved evidence
AND unsupported component types cannot render
AND a specification requesting DispositionControl is rejected in v1
```

---

## 20. AI Evals

Models are probabilistic, so unit tests alone are not enough. We also need evaluation cases that judge whether the model's *composition decisions* are acceptable — not whether a component renders, but whether composing it that way, for that case, for that viewer, was sound.

---

## 21. Tests vs Evals

Tests ask: *does the software behave correctly?* Evals ask: *does the AI behave acceptably?*

Both are required. A perfect renderer can faithfully display a poor composition decision, and a good composition can still fail because the application code is broken. In this domain the asymmetry matters: a renderer bug is visible and loud, while a subtly misleading composition is quiet and may only surface as an inspector's misplaced confidence.

---

## 22. Feedback Loop

Failures are engineering inputs. A problematic evaluation or production case becomes a new evaluation scenario, and leads to improvements in the contract, prompt, context, renderer or application code.

```
AI Output → Evaluation → Failure
       ↓
Feedback → Claude Code
       ↓
Tests → Evals → Improved Output
```

---

## 23. Example Feedback Scenario

Suppose, for a board whose calibrated confidence is 0.61, the model composes a view led by a large heading reading **"No significant defects found"**, with the confidence badge placed below the fold.

Nothing here is invalid. Every component is approved, the schema is correct, the evidence references are in scope, and no disposition is named. A validator cannot catch it. But an inspector scanning that screen has been told something the evidence does not support, on exactly the screen where they will later be asked to decide.

```
Failure
   ↓
Add evaluation case: marginal confidence must not read as conclusive
   ↓
Strengthen contract: confidence badge adjacent to any summary heading
   ↓
Strengthen ui-layout-policy.md
   ↓
Claude Code
   ↓
Tests → Evals → Improved version
```

This is the domain's version of the reference guide's over-claiming landing page — and it is the clearest argument for why this surface needs evaluations of its own.

---

## 24. Complete First-Scenario Flow

```
Business Problem
   ↓
Specification
   ↓
Model Contract
   ↓
Harness
   ↓
Claude Code
   ↓
Incremental Implementation
   ↓
Controlled Generative UI
   ↓
Tests
   ↓
Evals
   ↓
Feedback
   ↓
Claude Code
   ↓
Improvement
```

---

## 25. What We Are NOT Building Yet

Deliberately postponed: authentication and attribution, live image capture, edge inference, quality gates QG-1 to QG-4, calibration and risk scoring, the decision path, disposition and override, PLC/MES integration, the label store and retraining loop, evidence retention and audit, and production deployment infrastructure.

Every one of these is in the architecture. None is in this slice.

---

## 26. What Comes After the Review Panel?

Once the engineering pattern is understood, the same discipline expands along the real inspection path:

```
Review panel over a recorded fixture
   ↓
Live capture + QG-1 enforcement
   ↓
Edge inference + QG-2
   ↓
Context and QG-3
   ↓
Calibration and risk
   ↓
Decision path and QG-4
   ↓
DispositionControl + action gateway + attribution
   ↓
PLC signalling
   ↓
Human review loop, labels and QG-5
   ↓
Model lifecycle and QG-6
```

The order is not arbitrary. Each step earns the next, and the disposition control does not appear until the evidence, decision and audit path beneath it exists.

---

## 27. Mental Model

- **Frontend / UI Runtime** — what the inspector sees.
- **Backend / Domain Runtime** — what controls the process and decides what is allowed.
- **AI Runtime** — where probabilistic intelligence is used.
- **Generative UI** — the model helps determine interface composition.
- **Model Contract** — expected and prohibited model behaviour.
- **Harness** — context, constraints, tools and verification around Claude Code.
- **Simulators** — how the system runs without a factory.
- **Tests** — deterministic software checks.
- **Evals** — AI behaviour checks.
- **Feedback** — failures converted into the next engineering iteration.

---

## 28. Definition of Done

The first scenario is complete when:

- The web application opens and the review panel renders over a recorded inspection fixture
- The model produces a structured UI specification rather than executable code
- Only approved components render, and `DispositionControl` is rejected in v1
- Every displayed value is resolved by the backend from evidence references, never passed through by the model
- Invalid or out-of-scope output is rejected and the standard fallback screen takes over
- The fallback screen alone is sufficient for an inspector to review a board
- The model contract exists and each prohibition names its enforcement point
- Deterministic tests pass
- UI-composition evaluation cases exist and the runner is wired into CI
- An evaluation failure can drive a Claude Code improvement

---

## 29. Final Takeaway

We are not simply asking Claude Code to build a review screen. We are using one small, safe feature to demonstrate a complete AI-native engineering discipline: define the business need, specify the behaviour, establish a harness and a model contract, implement incrementally, control model output through deterministic boundaries, test the software, evaluate the AI, learn from feedback, and improve the system.

The slice is read-only by design. That is what lets us learn the mechanism on a surface where being wrong costs nothing — before applying it to one where being wrong rejects a good board or passes a defective one.

---

## Appendix A — Approved Components for v1

| Component | Shows | Notes |
|---|---|---|
| `BoardSummary` | Board identity, type, revision, line, inspection point | Metadata only |
| `ImageCompare` | Captured image against its reference | Backend-resolved image refs |
| `DefectOverlay` | Detection regions on the captured image | From detection evidence |
| `ConfidenceBadge` | Calibrated confidence and uncertainty | Never model-authored text |
| `ReviewPanel` | Reviewer input fields | Inert in v1; no submission |
| `Heading` `Text` | Structure and neutral labels | Subject to the no-editorializing rule |
| `Alert` | Degraded evidence or missing data notices | |
| `EscalationNotice` | Flags a case as ambiguous | Signals only; routes nothing |

Excluded in v1: `DispositionControl`, `QueueList`, `TrendChart`, `StatCard`, `ProgressIndicator`.

---

## Appendix B — First-Scenario Evaluation Cases

| # | Case | Checks |
|---|---|---|
| 1 | Clear single defect | Relevance — overlay and confidence both surfaced |
| 2 | Marginal confidence | Representation fidelity — must not read as conclusive |
| 3 | Multiple defects on one board | Completeness — all surfaced, not only the first |
| 4 | Missing or degraded evidence | Safe defaults — honest degraded view, not a gap |
| 5 | Unknown component type requested | Constraint compliance — rejected |
| 6 | Invented defect category | Taxonomy compliance |
| 7 | Prompt injection inside an operator note | Robustness |
| 8 | Manager vs inspector, same board | Permission conformance |
| 9 | Invalid JSON or schema violation | Validation and fallback |
| 10 | Editorializing or excessive text | Usability; no disposition implied |

---

## Appendix C — Where This Differs from the Reference Guide

Four translation decisions were made deliberately and are open to challenge.

| # | Reference guide | This document | Reason |
|---|---|---|---|
| 1 | Landing page as first feature | Inspector review panel over a recorded fixture | No customer or landing page exists in this domain; the review panel is the smallest visible surface that exercises the same machinery |
| 2 | First slice needs no upstream system | First slice needs a recorded inspection | An inspection view has inputs a landing page does not; `simulators/capture/` supplies them, which is the purpose it exists for |
| 3 | CTA included in the first catalogue | `DispositionControl` excluded from v1 | The reference CTA is harmless; a disposition control is the action this whole architecture governs. It arrives with authentication, attribution and the action gateway, or not at all |
| 4 | Authentication deferred (internal app) | Deferred *only while read-only* | The review surface requires attributed actions; deferral expires the moment a disposition can be submitted |

---

*Derived from `03 - Customer_Onboarding_Generative_UI_First_Implementation_Beginner_Guide` (reference sample, Customer Onboarding domain), mapped to the Board Defect Inspection System. Architecture, repository structure and section references follow `AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md`. This is a proposed first slice against a design that is itself marked as requiring validation; the open items in that document's Appendix C remain open.*
