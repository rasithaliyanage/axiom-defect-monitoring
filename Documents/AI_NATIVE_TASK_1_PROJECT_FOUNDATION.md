# Board Defect Inspection AI

## Task 1 — Establishing the Project Foundation

Beginner-friendly guide to starting an AI-native project with Claude Code.

**Companion documents:** `AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md` (architecture, repository structure, open items) and `AI_NATIVE_GENERATIVE_UI_FIRST_IMPLEMENTATION.md` (the first slice this foundation prepares for).

**Status:** Proposed Task 1 — not yet executed. Section 7 describes what this task *should* produce, not a record of what an agent already created.

**Version:** 1.0

---

## 1. What This Task Is About

We are starting the Board Defect Inspection application from an empty repository. Task 1 is deliberately **not** about building the application. It is about creating the project foundation that will guide both the development team and Claude Code.

The first implementation scenario is intentionally small: an **inspector review panel** using controlled Generative UI, rendered over a recorded inspection fixture. The runtime AI model will produce a structured UI specification, while the application controls what can actually be rendered.

---

## 2. Starting Point: An Empty Repository

The application starts in a new, empty repository — separate from the analysis repository that holds the BRD, the architecture diagram and these guides. Those documents are **inputs** to Task 1, not part of the application codebase.

```
git clone <application-repository-url>
cd board-defect-inspection
git status
```

Then start Claude Code from the repository root:

```
claude
```

> The repository URL is not recorded here because it has not been supplied. Fill it in before running the task.

---

## 3. Why We Do Not Start by Building the Application

A conventional project might begin immediately with a frontend framework, an API, a database and a model integration. Here we deliberately establish the engineering foundation first, in order to:

- Clarify the business problem before implementation
- Define what the system should do
- Define what the runtime AI model may and may not do
- Record which decisions are **not ours to make** and who owns them
- Give Claude Code persistent project context and engineering instructions
- Separate deterministic software tests from probabilistic AI evaluations
- Keep the first implementation small enough to understand and review

The fourth item is specific to this project and is the one most easily skipped. Our source BRD is a discovery document: the defect taxonomy, severity classifications, thresholds and recall targets are explicitly owned by the Quality and Manufacturing teams and are not yet decided. A coding agent given no instruction on this point will fill those gaps with reasonable-looking values, and a plausible invented threshold is far more dangerous than an obviously empty one.

---

## 4. The Information Layers Created in Task 1

| Layer | File | Beginner meaning | Owner |
|---|---|---|---|
| Business | `docs/business-problem.md` | Why are we building this? | Business / BA |
| **Policy** | `policies/` | What counts as a defect, and at what threshold? | **Quality / Manufacturing** |
| System | `specs/spec.md` | What should the system do? | Engineering |
| Model | `specs/model-contracts.md` | What may the runtime AI model do? | Engineering |
| Schema | `contracts/` | What shapes cross between runtimes? | Engineering |
| Engineering | `CLAUDE.md`, `.claude/` | How should Claude Code work here? | Engineering |

The key lesson is to avoid putting all project knowledge into one large prompt or document.

The `policies/` layer is the addition this domain forces, and it is not merely a different folder — it has a **different owner**. Engineering does not get to decide what counts as a critical defect. Keeping that knowledge in its own versioned location means a threshold change is a reviewable business action rather than a code edit buried in a commit.

---

## 5. The Exact Task 1 Prompt

This is the complete instruction for establishing the project foundation:

```
We are building an AI-Based Automated Board Defect Inspection System.
This repository is currently empty.

Do NOT build the application yet.

First, establish the project engineering foundation for an AI-native,
model-driven application.

The first implementation scenario is intentionally small and READ-ONLY:
an inspector review panel using controlled Generative UI, rendered over a
RECORDED inspection fixture. No camera, no PLC, no live inference.
Nothing in this first slice may change the state of a board.

The runtime AI model will generate a structured UI specification, not
executable code. The application will validate that output and render it
only through an approved component vocabulary.

SOURCE DOCUMENTS — read before proposing anything:
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
Not required for this slice because it is read-only. Do not build a login
subsystem. Record in docs/adr/ that this deferral expires the moment a
disposition can be submitted.

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

---

## 6. Understanding the Prompt

**"Do NOT build the application yet."** Prevents Claude Code from jumping into a frontend, an API, a model integration or a database.

**"Establish the project engineering foundation."** Makes documentation, conventions and boundaries the first deliverable.

**"Intentionally small and READ-ONLY."** Limits the first slice to a review panel that cannot change anything, instead of attempting the inspection platform.

**"Rendered over a RECORDED inspection fixture."** Removes the apparent dependency on the whole pipeline. A review panel looks like it needs a camera, edge inference and a decision path; over a fixture it needs none of them.

**"Not executable code."** Creates the critical boundary: model output is data, not instructions.

**"Do NOT fill in plausible values."** The instruction most specific to this project. The BRD leaves taxonomy and thresholds to Quality; an agent that helpfully supplies them has converted an open business question into an apparent requirement, and nobody downstream will know it happened.

**"Different owner."** Tells the agent that `policies/` is not just another docs folder — the knowledge in it belongs to a team that has not answered yet.

**"Supply evidence VALUES instead of references."** Keeps the model out of the data path. A model that can pass through a confidence value can pass through the wrong one.

**"Must not state, imply or recommend a disposition."** The model composes the screen on which a disposition will eventually be made. A layout can editorialize without ever naming a verdict.

**"DispositionControl is deliberately EXCLUDED."** The v1 catalogue is a governance decision, not a backlog of unfinished components.

**"Deferral expires the moment a disposition can be submitted."** Records *why* authentication is absent, so a later reader does not mistake a scoped decision for an oversight.

**"OPEN DECISION" (stack).** Two source documents disagree. The agent is told to leave it open rather than silently pick one.

**"Create ONLY the directories the first slice needs."** Our full structure has around twenty top-level directories. Scaffolding all of them on day one produces empty folders that imply commitments nobody has made.

**"List every open question you encountered."** Turns the agent's uncertainty into a review artifact instead of leaving it to be resolved by guesswork.

**"Do not proceed to the next task automatically."** Controls scope and lets a human review each increment.

---

## 7. What Task 1 Should Produce

| Item | Purpose |
|---|---|
| `CLAUDE.md` | Persistent engineering instructions: scope, architecture, approved components, hard boundaries, information ownership |
| `README.md` | Human-facing project overview |
| `.claude/settings.json` | Minimal project settings; no unnecessary hooks or permissions yet |
| `docs/business-problem.md` | The business "why": requirements, success indicators, explicit non-goals |
| `docs/architecture.md` | The "how": UI/Domain/AI runtimes, trust boundaries, controlled Generative UI |
| `docs/quality-gates.md` | QG-1 to QG-6 and their failure actions, documented ahead of implementation |
| `docs/adr/0001-…` | Decision-record format, seeded with the authentication deferral and the open stack decision |
| `specs/spec.md` | The system "what": functional requirements, boundary behaviour, out-of-scope items |
| `specs/model-contracts.md` | Runtime AI contract: context, UI specification, vocabulary, refusal shape, restrictions |
| `specs/ui-contract.md` | The UI specification schema |
| `policies/` | Placeholder files naming the owning team and source question for taxonomy, thresholds, decision rules and UI layout policy |
| `contracts/ui/` | Shared UI specification schema, owned by neither runtime |
| `simulators/capture/` | Location for the recorded inspection fixture the first slice renders |
| `tests/README.md` | The purpose of deterministic software tests |
| `evals/README.md` | The purpose of AI evaluations |

A useful review question when the task completes: **does any file in `policies/` contain a number?** If it does, the agent invented it, and that is the first thing to remove.

---

## 8. The Three Runtime View

Task 1 establishes three logical runtime areas. They describe responsibilities; they do not require three separate applications.

```
        Inspector (browser)
                |
                v
          UI Runtime
   Approved component catalogue
   Generative UI renderer
   Standard fallback UI
                |
                v
        Domain Runtime
   Review API surface
   Evidence reference resolution
   Owns all state
                |
                v
          AI Runtime
   Model gateway (version pinned)
   UI specification generation
                |
                v
     simulators/capture/
   Recorded inspection fixture
```

The frontend/backend view remains useful and is not being replaced. The runtime view explains the logical responsibilities across interface, business control and probabilistic intelligence.

---

## 9. What Controlled Generative UI Means

Instead of asking the runtime model to write a screen as code, we ask it to describe the screen using a controlled structure.

```
{
  "view": "inspection_review",
  "context": { "board_ref": "attempt-2f91c4", "role": "inspector" },
  "components": [
    { "type": "BoardSummary",    "source": "attempt.metadata" },
    { "type": "ImageCompare",    "mode": "reference_vs_captured" },
    { "type": "DefectOverlay",   "source": "attempt.detections" },
    { "type": "ConfidenceBadge", "source": "attempt.calibrated_score" },
    { "type": "ReviewPanel",     "fields": ["defect_class", "reason_code"] }
  ]
}
```

The intended boundary is:

```
AI model
   ↓
Structured output
   ↓
Schema validation
   ↓
Approved component vocabulary
   ↓
Evidence references resolved by the backend
   ↓
Known components
   ↓
Rendered UI
```

The model is probabilistic; the surrounding software provides deterministic controls. Note the extra step this domain adds over a generic Generative UI flow: **the backend resolves evidence references**, so the values an inspector reads never travel through the model.

---

## 10. Initial Approved UI Components

```
BoardSummary      ImageCompare       DefectOverlay
ConfidenceBadge   ReviewPanel        Heading
Text              Alert              EscalationNotice
```

The vocabulary is intentionally small. Two kinds of output fall outside the contract and must be rejected rather than interpreted:

```
{ "type": "execute_query" }          ← never in the catalogue
{ "type": "DispositionControl" }     ← in the eventual catalogue, not in v1
```

The second is the more interesting case. It is a legitimate component of the finished system that this slice has not yet earned.

---

## 11. Understanding the Model Contract

A model contract defines the boundary around runtime AI behaviour. The mindset shifts from *"give the model a prompt"* to *"engineer a contract around model behaviour."*

**The model may:** select and order approved components; choose which evidence references are most relevant; generate neutral text; adapt layout to role; signal ambiguity.

**The model must not:** generate executable code or arbitrary markup; request components outside the catalogue; supply evidence values instead of references; state or imply a disposition; contradict the calibrated score; invent defect categories; access the database, registry or line equipment.

Each prohibition should name how it is enforced. Some are structural — catalogue membership and schema validity are enforced by the renderer, and evidence scope by the backend. Others can only be measured: no validator can detect a layout that implies a verdict, so that one is enforced by evaluation cases.

Knowing which prohibitions are structural and which are measurable tells you where you need evals rather than tests.

---

## 12. Tests Versus AI Evals

| Area | Question | Example |
|---|---|---|
| Deterministic tests | Does the software behave correctly? | A valid UI specification renders through approved components; one requesting `DispositionControl` is rejected |
| AI evals | Does the AI behave acceptably? | A marginal-confidence result is not composed so that it reads as conclusive |

Task 1 establishes the separation. It does not implement the test suite or the evaluation harness.

---

## 13. What Was Deliberately NOT Built

No application code yet — no frontend, no API, no model gateway. No authentication subsystem. No database. No CI/CD, containers or deployment infrastructure. No live image capture, edge inference or quality-gate enforcement. No calibration, risk scoring or decision path. No disposition or override. No PLC or MES integration. No model training, registry or retraining loop. No `edge/`, `enterprise/`, `ml/`, `ops/`, `infra/` or `ci/` directories.

These omissions are intentional. The first increment should demonstrate the engineering method, not bury it in infrastructure.

---

## 14. What the Harness Means at This Stage

At this stage we have a Claude Code project foundation rather than a fully enforced runtime harness. `CLAUDE.md` supplies persistent guidance; the repository structure gives each kind of project truth a clear home.

An important distinction: **CLAUDE.md is guidance and context, not a security guarantee.** Stronger enforcement comes later from `.claude/` permissions and hooks, from schema validation, and from tests. Task 1 creates `.claude/` with minimal settings precisely so the location exists before anything needs to be enforced there.

`simulators/capture/` also belongs to the harness. It is created in Task 1 — even though it holds only a fixture — because an agent with no way to exercise degraded or unusual inputs will write confident happy-path code.

---

## 15. Why Task 1 Is Important for AI-Native Engineering

Traditional software rests on deterministic logic written by developers. AI-native systems introduce probabilistic model behaviour, so the engineering environment must define responsibilities and boundaries around that behaviour:

- Define what the model is responsible for
- Define what the model is not allowed to do
- Keep model output structured
- Validate model output before using it
- Keep deterministic software boundaries around probabilistic behaviour
- Separate software correctness from AI behaviour quality
- Record which questions belong to the business and remain unanswered
- Make feedback and improvement part of the engineering lifecycle

---

## 16. The Engineering Flow Being Established

```
Business Problem
       ↓
Specification
       ↓
Model Contract
       ↓
Project Foundation
       ↓
Claude Code
       ↓
Incremental Implementation
       ↓
Tests
       ↓
AI Evals
       ↓
Feedback
       ↓
Claude Code
       ↓
Continuous Improvement
```

Task 1 establishes the foundation for this flow. The project intentionally stops after the foundation so each later increment can be reviewed.

---

## 17. Task 1 Completion Checklist

- [ ] Empty application repository cloned and opened from the project root
- [ ] Claude Code started from the repository
- [ ] Source documents (BRD, architecture) read before any file was proposed
- [ ] Project scope defined
- [ ] Business problem documented
- [ ] Architecture documented, including the three runtimes
- [ ] Quality gates QG-1 to QG-6 documented
- [ ] System specification documented
- [ ] Runtime model contract documented, each prohibition naming its enforcement point
- [ ] UI specification schema defined
- [ ] `policies/` created as placeholders with named owners and **no invented values**
- [ ] Claude Code project instructions created
- [ ] `.claude/` created with minimal settings
- [ ] `simulators/capture/` created for the recorded fixture
- [ ] Tests and evals separated conceptually
- [ ] Controlled Generative UI boundary defined
- [ ] Approved component vocabulary defined, with `DispositionControl` excluded
- [ ] Authentication deferral recorded as a decision with an expiry condition
- [ ] Technology stack recorded as an open decision
- [ ] Out-of-scope capabilities documented
- [ ] Open questions encountered during the task listed for review
- [ ] No unnecessary application implementation introduced

---

## 18. Key Beginner Lessons

**A prompt is not an engineering contract.** A prompt gives instructions; a contract defines expected behaviour and boundaries around model output.

**Do not let the model generate application code.** For controlled Generative UI, the model describes intent using structured data and the application renders known components.

**Keep the data path away from the model.** The model names evidence; the backend resolves it.

**Some knowledge is not engineering's to write down.** Taxonomy and thresholds belong to Quality. The correct output for an unanswered business question is a placeholder with a named owner, never a plausible value.

**Build in small increments.** Small tasks make failures easier to diagnose and changes easier to review.

**Tests and evals are different.** Tests check deterministic correctness; evals assess probabilistic behaviour. Some constraints can only be evaluated, never validated.

**The engineering environment matters.** Instructions, specifications, validation, tests and evaluation mechanisms help an AI coding agent work more reliably.

---

## 19. End of Task 1

At the end of Task 1 we have not built the inspector review panel. We have built the environment in which it can be built deliberately.

> **Key idea:** Before asking an AI agent to build the system, establish the rules, context, boundaries and structure in which it must work — and be explicit about which questions are still open and who owns them.

---

*Derived from `Customer_Onboarding_Task_1_Beginner_Guide` (reference sample, Customer Onboarding domain), mapped to the Board Defect Inspection System. Architecture and structure follow `AI_NATIVE_ENGINEERING_INITIAL_DISCUSSION.md`; the first slice follows `AI_NATIVE_GENERATIVE_UI_FIRST_IMPLEMENTATION.md`. Source inputs — the BRD and the eleven-layer architecture — are both provisional, and their open items remain open.*
