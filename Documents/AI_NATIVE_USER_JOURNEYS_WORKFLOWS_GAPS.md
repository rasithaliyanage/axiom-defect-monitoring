# Enterprise AI-Native PCB Defect Inspection — User Journeys, Workflows & Process Gaps

## Architecture Review: Actors, End-to-End Journeys, Core Workflows and Open Questions

**Source artifact:** AI_NATIVE_SOLUTION_ARCHITECTURE_INFOGRAPHIC.png — "Enterprise AI-Native PCB Defect Inspection Architecture" (Model-Driven | Probabilistic | Adaptive | Human in the Loop). Diagram status: *Proposed design — validation required.*

**Prepared for:** Solution Architecture Review / SRS & Proposal input
**Prepared by:** AI-Native Solution Architecture function
**Document owner:** info@capricon.lk
**Version:** 1.0
**Status:** Draft for stakeholder / BA validation

---

## 0. Purpose and Method

This document decomposes the reference architecture into (1) the actors and their end-to-end journeys through the system, (2) the core business and system workflows implied by the eleven architectural layers and six Quality Gates (QG-1–QG-6), and (3) the process, ownership and control gaps that cannot be resolved from the diagram alone.

**Method and constraints applied:**
- Every journey and workflow step below is traced to a specific labelled element in the source diagram (layer name, gate, or panel).
- No industry-standard defaults have been assumed where the diagram is silent (e.g., SLAs, retry limits, retention periods). Such items are listed as open questions in Section 3, not resolved by assumption.
- Vendor-delivered platform capabilities (Layers 1–11, Quality Gates, Failure Handling, Observability) are kept distinct from client-owned business decisions (policy thresholds, BRD review authority, compliance sign-off), consistent with the diagram's Edge (factory/on-prem) vs. Enterprise (central platform) separation.

---

## 1. User Journeys

### 1.1 Actor Inventory

The diagram depicts or clearly implies the following distinct actors. Each is classified by type (human role vs. automated/system actor) and by home layer.

| # | Actor | Type | Primary Layer(s) | Evidence in Diagram |
|---|---|---|---|---|
| A1 | Line / Factory Operator | Human | 1 – Data Capture & Ingestion (Edge) | Cameras, Board ID scanner/PLC, Line adapter interactions, "bounded re-capture" on QG-1 failure |
| A2 | Edge AI System | Automated | 2 – Edge AI Processing | Preprocess, Edge Inference, QG-2, local decision (layers 5–6 only) |
| A3 | Enterprise AI Model Orchestration | Automated | 4 – AI Model Layer | Approved model orchestration, vision pipeline, specialized models |
| A4 | Probabilistic Risk Engine | Automated | 5 – Probabilistic Reasoning & Risk | Evidence aggregation, calibration, uncertainty, risk assessment |
| A5 | Decision Engine | Automated (policy-driven) | 6 – Decision Layer | Product-specific rules/thresholds, QG-4, PASS/HOLD/REJECT |
| A6 | Human Reviewer / Inspector | Human | 7 – Human-in-the-Loop | Review queue, annotation + review, QG-5, second reviewer path |
| A7 | BRD Reviewer / Business Approver | Human | 6 – Decision Layer (HOLD → BRD REVIEW, REJECT → BRD FAIL) | "Physical action approved" gate distinct from QG-5 labeling |
| A8 | ML Engineer / Data Scientist (MLOps) | Human | 8 – Model Lifecycle & MLOps | Train & experiment, QG-6, "AI-assisted engineering → Human review → CI/evaluation" |
| A9 | Platform Owner | Human | 9 – Observability, Operations & AI-Native Hosting | "approve exceptions / suspend," incident response |
| A10 | Compliance / Governance Administrator | Human | 10 – Governance, Security & Compliance | RBAC/access control, model governance approvals, compliance evidence |
| A11 | Operator / Inspector / Manager (UI consumer) | Human | 11 – Adaptive UI Layer | Explicitly named: "operators, inspectors and managers" |
| A12 | Edge–Enterprise Synchronization Service | Automated | Layer 3 (shared) + Edge-Enterprise Collaboration panel | Factory-initiated uploads & polling, offline approved cache, mTLS sync |

> Note: A6 (label/annotation reviewer) and A7 (BRD reviewer) are shown as separate gates in the diagram (QG-5 vs. BRD Review/Fail) but their organizational relationship is **not defined** — see Gap 1.

### 1.2 End-to-End Journeys

| Actor | Entry Point | Key Interactions | Decision Points | Exit / Outcome | Layers Touched |
|---|---|---|---|---|---|
| **A1 — Line/Factory Operator** | Physical PCB placed at camera station | Camera/Board ID scanner/sensor capture; acknowledges Line adapter commands and PLC state | QG-1 (input completeness, focus, metadata, source health, sequence validity) | Pass → forwarded to Edge AI; Fail → **Quarantine or bounded re-capture** | 1 (Presentation/Edge) |
| **A2 — Edge AI System** | QG-1-passed capture | Preprocess (denoise/normalize/crop/ROI) → Edge Inference against approved model version → optional local decision (only for layers 5–6 products) → persist trusted evidence | QG-2 (model version, inference latency, deadline, output format) | Pass → evidence persisted, forwarded to context/model layers; Fail → **HOLD / bounded re-process** | 2 (Application/Edge) |
| **A12 — Sync Service** | Scheduled poll or factory-initiated upload | Synchronizes approved models/context, inspection results; maintains offline approved cache; secure/encrypted mTLS channel; fleet management of edge devices | Sync success vs. degraded/offline state | Edge continues on last-known-good cache when disconnected | Layer 3 shared, Edge–Enterprise Collaboration panel |
| **A3 — Enterprise Model Orchestration** | Validated evidence + validated context (QG-3 passed) | Routes to approved, product-specific model/ensemble; runs vision pipeline (Understand → Detect → Classify → Localize); invokes specialized models | Model/ensemble selection per product | Model evidence (classes, bounding boxes, raw per-class scores) passed downstream; central re-analysis preserves the original edge outcome | 4 (Enterprise + Edge deployment) |
| **A4 — Risk Engine** | Model evidence received | Evidence aggregation → validated calibration (temperature scaling/Platt/isotonic) → uncertainty estimation (aleatoric/epistemic) → risk assessment (severity, criticality, business impact) | Calibration validity (raw scores explicitly **not** treated as probabilities until validated) | Calibrated risk output passed to Decision Layer | 5 |
| **A5 — Decision Engine** | Calibrated risk output | Applies product-specific rules/thresholds and approved decision logic | QG-4 (valid evidence, complete context, policy/risk checks) | **PASS** (release) / **HOLD** (→ BRD Review) / **REJECT** (→ BRD Fail); decision record with evidence, reasoning, model/policy versions, audit trail created | 6 |
| **A7 — BRD Reviewer** | Decision Layer outputs HOLD or REJECT | Reviews decision record (evidence, reasoning, versions) | BRD REVIEW (HOLD) vs. BRD FAIL (REJECT) | Physical action on the board approved only after this review | 6 |
| **A6 — Human Reviewer/Inspector** | Uncertain results, high-risk cases, or unknown/anomaly items enter Review Queue | Annotation + review (bounding boxes, component IDs, reason codes); second reviewer where required; model override recorded separately from training-label approval | QG-5 (guideline agreement, label completeness, critical checks e.g. safety) | Pass → validated feedback stored, linked to original case, used for training/evaluation; Fail → **Escalate** | 7 |
| **A8 — ML Engineer (MLOps)** | Versioned, PASS-audited, leakage-controlled training data | Train & experiment; experiment tracking; evaluation on held-out sets | QG-6 (independent recall/FN, calibration, regression/performance slices, hardware validation) | Pass → quality approval + model registry entry → shadow/staged deployment (canary, monitoring, rollback if needed); Fail → **Iterate**. Explicit control: *"No self-approved model deployment."* | 8 |
| **A9 — Platform Owner** | Alert from Observability (drift, anomaly, threshold breach, SLA breach) | Diagnoses/mitigates incident; approves exceptions or suspends operation; reviews forecasts and capacity plans; enforces policy gate limits | Approve exception vs. suspend; execute & verify remediation | Feedback loop improves platform reliability and forecasting | 9 |
| **A10 — Governance/Compliance Admin** | Access request, model/policy change request, or scheduled audit | RBAC provisioning (least privilege); reviews audit & lineage (immutable, end-to-end); approves model/policy governance changes | Approve/deny access; approve/deny model or policy change | Compliance evidence produced against applicable obligations | 10 (cross-cutting) |
| **A11 — Operator/Inspector/Manager (UI)** | Opens Adaptive UI with authorized role/task context | Views AI-composed, role-aware, permission-scoped interface; takes an explicit action | UI validation (schema/permissions) pass vs. fail | Explicit user action triggers backend authorization into existing workflows; on failure → **Standard UI fallback** (invalid output/timeout/user choice) | 11 (reads Layers 6–7 data, hosted by 9, governed by 10) |

---

## 2. Workflows

Each workflow below states its trigger, sequence, participating components, data exchanged, decision/approval points, execution mode, and success/failure paths, exactly as evidenced in the diagram.

### 2.1 Ingestion & Edge Inference
- **Trigger:** New PCB presented at the capture station.
- **Sequence:** Capture (camera/Board ID/sensor/metadata) → QG-1 validation → Preprocess → Edge Inference → QG-2 validation → optional local decision (layers 5–6 only) → persist evidence.
- **Components:** Cameras, Board ID scanner/PLC, sensors, Edge AI, Line adapter.
- **Data exchanged:** High-resolution image, board metadata, machine state, model output/confidence, timestamp/sequence.
- **Decision/approval points:** QG-1 (input validity), QG-2 (inference reliability).
- **Execution mode:** Synchronous, in-line with production; automated with operator-triggered re-capture on failure.
- **Success/failure:** Success → forwarded for context enrichment. Failure → Quarantine / bounded re-capture / HOLD.

### 2.2 Context Enrichment
- **Trigger:** Validated inference, or a scheduled context sync.
- **Sequence:** Local cache lookup → Context sync with Central context store → QG-3 validation (product/revision validity, spec/component references, line context).
- **Components:** Local cache, Context sync service, Central context store.
- **Data exchanged:** Board specifications, BOM, product variants, machine/process context, version/expiry metadata.
- **Decision/approval points:** QG-3 (context completeness/validity); on failure, last-known-good is used only within approved validity policy.
- **Execution mode:** Asynchronous sync; synchronous validation gate before inference is trusted; fully automated.
- **Success/failure:** Pass → validated context available for decisioning. Fail → HOLD / exception.

### 2.3 Model Orchestration & Vision Pipeline
- **Trigger:** Validated evidence and validated context both available.
- **Sequence:** Approved model routing/product-specific selection → vision pipeline (Understand → Detect → Classify → Localize) → specialized models produce model evidence.
- **Components:** AI Model Layer (Enterprise + Edge deployment), specialized defect models.
- **Data exchanged:** Defect classes, bounding-box locations, raw per-class scores.
- **Decision/approval points:** Model/ensemble selection is policy-driven, not case-by-case approved.
- **Execution mode:** Synchronous per item; central re-analysis runs asynchronously and explicitly preserves the original edge outcome (does not silently overwrite it). Fully automated.
- **Success/failure:** Model evidence is always passed forward to the Risk Layer; no explicit failure branch is shown at this stage.

### 2.4 Probabilistic Risk Assessment
- **Trigger:** Model evidence produced.
- **Sequence:** Evidence aggregation → validated calibration (temperature scaling / Platt / isotonic) → uncertainty estimation (aleatoric / epistemic, where validated) → risk assessment (severity, criticality, business impact).
- **Components:** Probabilistic Reasoning & Risk Layer.
- **Data exchanged:** Calibrated probabilities, uncertainty bounds, risk scores.
- **Decision/approval points:** Calibration must be validated before scores are treated as probabilistic (explicit diagram note: "Raw scores are not automatically probabilistic").
- **Execution mode:** Synchronous; fully automated.
- **Success/failure:** Output feeds Decision Layer; no explicit failure branch shown at this stage.

### 2.5 Decisioning
- **Trigger:** Calibrated risk output ready.
- **Sequence:** Apply product-specific rules/thresholds and approved decision logic → QG-4 validation → outcome determination → decision record creation.
- **Components:** Decision Layer.
- **Data exchanged:** Decision outcome, evidence and reasoning, model/policy version references, audit trail entry.
- **Decision/approval points:** QG-4 (valid evidence, complete context, policy/risk checks); outcome branches to PASS, HOLD (→ BRD Review), or REJECT (→ BRD Fail).
- **Execution mode:** Synchronous decisioning; **manual approval gate required before physical action** on HOLD/REJECT outcomes.
- **Success/failure:** PASS → released. HOLD/REJECT → routed to BRD review before any physical action is taken.

### 2.6 Human-in-the-Loop Review & Labeling
- **Trigger:** HOLD outcome, low-confidence inference, or flagged unknown/anomaly.
- **Sequence:** Item enters review queue → annotation + review (bounding boxes, component IDs, reason codes) → second reviewer for required cases → QG-5 validation → validated feedback stored and linked to originating case.
- **Components:** Human-in-the-Loop Layer.
- **Data exchanged:** Approved labels, review comments, case linkage, override rationale.
- **Decision/approval points:** QG-5 (guideline agreement, label completeness, critical/safety checks). Model override and training-label approval are kept as separate approval tracks.
- **Execution mode:** Asynchronous; fully manual (expert human).
- **Success/failure:** Pass → validated feedback used for training/evaluation. Fail → Escalate.

### 2.7 Model Lifecycle / MLOps
- **Trigger:** New/updated verified training data, scheduled retraining, or drift-triggered retraining need.
- **Sequence:** Versioned data (representative PASS audits, verified labels, data leakage control) → train & experiment (with experiment tracking, evaluation on held-out sets) → QG-6 evaluation → quality approval + model registry entry → shadow/staged deployment (canary, monitoring, rollback if needed).
- **Components:** Model Lifecycle & MLOps Layer, CI/evaluation pipeline.
- **Data exchanged:** Training datasets, experiment metrics, model artifacts, model metadata, release notes.
- **Decision/approval points:** QG-6 (independent recall/false-negative rate, calibration, regression/performance slices, hardware validation). Explicit control: **no self-approved model deployment** — pipeline requires AI-assisted engineering → human review → CI/evaluation → authorized release.
- **Execution mode:** Predominantly asynchronous/batch; hybrid automated-assisted + mandatory human authorization.
- **Success/failure:** Pass → shadow/staged deployment with monitoring and rollback capability. Fail → Iterate.

### 2.8 Observability & Incident Response
- **Trigger:** Continuous monitoring signal — drift/anomaly detection, threshold breach, or capacity forecast issue.
- **Sequence:** Monitor (performance, quality trends, system health) → Alert (thresholds, anomalies, SLA breaches) → incident response (diagnose, mitigate, rollback if needed) → Observe (telemetry/logs) → Forecast (demand/risk models, prediction intervals) → Plan (outages, cooldowns) → Policy gate (check capacity, enforce limits) → Execute & verify → feedback to improve.
- **Components:** Observability, Operations & AI-Native Hosting Layer; Platform Owner.
- **Data exchanged:** Telemetry, logs, drift/anomaly metrics, alerts, capacity forecasts, policy constraints.
- **Decision/approval points:** Platform Owner approves exceptions or suspends operation; policy gate enforces reserved-edge and bounded-enterprise-scaling limits; isolated training pools are explicitly segregated from production capacity, and "uncertain forecasts → static reserve" (i.e., the system never consumes edge reservations under uncertainty).
- **Execution mode:** Continuous/asynchronous monitoring; manual incident response for exceptions.
- **Success/failure:** Verified remediation feeds back into forecasting and planning; no explicit terminal failure state shown beyond suspend/rollback.

### 2.9 Governance & Compliance
- **Trigger:** Access request, model/policy change request, or scheduled audit.
- **Sequence:** Access control (RBAC, least privilege) → data protection (encryption, retention, anonymization) → audit & lineage capture (immutable history, end-to-end traceability) → model governance (approvals, risk management, change control) → compliance evidence compiled against applicable obligations.
- **Components:** Governance, Security & Compliance Layer (cross-cutting across Edge and Enterprise).
- **Data exchanged:** Access logs, lineage records, approval records, compliance artifacts.
- **Decision/approval points:** Approvals required for access grants, model promotion, and policy/change control.
- **Execution mode:** Asynchronous, continuous, cross-cutting; manual approvals with automated logging/evidence capture.
- **Success/failure:** Produces auditable, end-to-end compliance evidence across every layer; no explicit failure path (governance is a control layer, not a pass/fail gate in the diagram).

### 2.10 Adaptive UI Rendering
- **Trigger:** Authorized user opens a task-scoped interface.
- **Sequence:** Authorized context (role, task, permitted evidence) → UI composition model generates a structured UI spec → UI validation (schema/permissions) → component renderer builds approved widgets from authoritative data → adaptive, role-aware interface presented, with pinned active reviews → explicit user action triggers backend authorization into existing workflows.
- **Components:** Adaptive UI Layer; consumes data from Layers 6–7; hosted by Layer 9; governed by Layer 10.
- **Data exchanged:** UI specification/schema, permissions, rendered components, user actions.
- **Decision/approval points:** UI validation pass/fail. Design principle stated in diagram: *"UI model composes presentation; users authorize actions"* — i.e., the AI never executes backend actions directly.
- **Execution mode:** Synchronous per render; automated generation with manual, explicit user action for any backend effect.
- **Success/failure:** Pass → adaptive interface rendered. Fail (invalid output, timeout, or user choice) → Standard UI fallback.

### 2.11 Edge–Enterprise Synchronization
- **Trigger:** Factory-initiated upload or scheduled polling.
- **Sequence:** Approved model/context updates pushed to edge; inspection results synchronized to enterprise; offline approved cache maintained for continuity; fleet management of edge devices.
- **Components:** Edge–Enterprise Collaboration channel (secure, encrypted, mTLS, DMZ-crossing).
- **Data exchanged:** Approved models, context, inspection results, evidence, policies, logs, fleet status.
- **Decision/approval points:** Not explicit — synchronization appears policy-driven and continuous rather than approved case-by-case (see Gap 10).
- **Execution mode:** Asynchronous.
- **Success/failure:** Edge continues operating from last-known-good offline cache if disconnected; no explicit conflict-resolution or staleness cutoff is shown (see Gap 9).

---

## 3. Process Identification Challenges / Gaps

The following items are not resolvable from the diagram alone. Each states what is missing, why it matters at enterprise scale, and the specific question to raise with the client/BA team. No industry-default assumption has been substituted for any of these.

1. **Ownership overlap between the Layer 7 label/annotation reviewer (QG-5) and the Layer 6 BRD reviewer (BRD Review/BRD Fail).**
   *Why it matters:* These read as two distinct human gates with different purposes (label quality vs. release/physical-action approval), but the diagram does not state whether they are the same personnel, team, or queue, which affects staffing, SLA design, and system access provisioning.
   *Question:* Are the BRD reviewer and the label/annotation reviewer the same role? If not, what is the case hand-off mechanism between them?

2. **No SLA or timeout is defined for HOLD or Escalate states.**
   *Why it matters:* Boards can sit in HOLD (BRD review) or Escalated (expert review) indefinitely per the diagram, which directly affects line throughput, WIP inventory, and customer delivery commitments.
   *Question:* What is the maximum allowable dwell time in HOLD/Escalated before a board is force-failed, auto-released under a fallback policy, or flagged as a line bottleneck?

3. **"Bounded re-capture" (QG-1) and "bounded re-process" (QG-2) have no stated bound.**
   *Why it matters:* The retry ceiling and the terminal action once it is exhausted (permanent quarantine, scrap, forced escalation) are not shown, which is required to size quarantine capacity and operator workload.
   *Question:* What is the retry limit for re-capture/re-process, and what is the terminal disposition once that limit is exceeded?

4. **Authority and trigger conditions for the "Approved manual / hold — stop fallback" (Failure Handling panel) are undefined.**
   *Why it matters:* This is the most severe failure-handling action shown (a full production stop) with no stated authorization level, automatic vs. discretionary trigger, or resumption procedure — a material operational-risk gap.
   *Question:* Who is authorized to invoke the manual stop fallback, under what conditions is it automatic vs. discretionary, and what is the documented resumption procedure?

5. **The physical actuation mechanism for PASS/HOLD/REJECT is not specified.**
   *Why it matters:* The Decision Layer states "physical action approved," but nothing in the diagram indicates what device executes this (conveyor diverter, robotic sorter, manual operator instruction), or whether a secondary human confirmation is required at the point of action for REJECT outcomes.
   *Question:* What physical/mechanical system executes the PASS/HOLD/REJECT decision on the line, and is a secondary human confirmation required immediately before physical action on a REJECT?

6. **Conflict resolution between central re-analysis and the original edge decision is unclear.**
   *Why it matters:* Layer 4 states central re-analysis "preserves the original edge outcome," implying central inference can diverge from what already happened physically at the edge, but no corrective process is shown for that divergence.
   *Question:* If central re-analysis disagrees with an edge decision already acted on physically, what is the corrective process — recall, re-inspection, or record-only annotation?

7. **Supplied recall targets are explicitly marked as unvalidated ("Pending Quality confirmation — not measured results").**
   *Why it matters:* These are the only quantitative acceptance criteria in the diagram (e.g., 99.5% recall for missing component) and are foundational to any SRS/contract, yet the source diagram itself flags them as unconfirmed.
   *Question:* Who owns sign-off on these recall targets (client Quality function, vendor, or joint), and what validation dataset and methodology will be used before they become binding acceptance criteria?

8. **Data retention period, anonymization scope, and data-residency constraints are unspecified.**
   *Why it matters:* Layer 10 lists "Data protection: Encryption, retention, anonymization" as a category label only — no retention period, no definition of what must be anonymized (e.g., customer board designs, proprietary component layouts), and no residency/sovereignty constraint is given, all of which are required for a compliance-ready SRS.
   *Question:* What are the specific retention periods, anonymization scope, and data residency/sovereignty requirements for captured PCB images and inspection metadata?

9. **Offline edge cache staleness policy is not defined.**
   *Why it matters:* "Offline approved cache (models & context)" allows continued edge operation during disconnection, but no expiry or maximum staleness is given before the edge must halt or flag reduced confidence — a gap that risks inspecting against outdated specifications.
   *Question:* How long may an edge site operate on cached models/context before it must halt, or degrade to a flagged/reduced-confidence mode, due to staleness?

10. **Model promotion/rollback approval authority is ambiguous between MLOps (Layer 8, QG-6) and Governance (Layer 10, model governance).**
    *Why it matters:* "Quality approval + registry" and "rollback if needed" appear under MLOps, while "Model governance: Approvals, risk management, Change control" appears separately under Governance — it is unclear whether this is one approval event described twice, or two sequential, independently owned approvals.
    *Question:* Is model promotion to production a single approval event, or does it require separate, sequential sign-off from both the MLOps quality gate (QG-6) and the Governance layer's model governance function?

11. **Adaptive UI fallback triggers ("Invalid output, Timeout, User choice") have no defined thresholds or degraded-mode scope.**
    *Why it matters:* The UI can fall back to a "Standard UI," but the timeout duration and whether the fallback exposes full or reduced functionality are not shown, which is required to define degraded-mode UX and support requirements.
    *Question:* What is the timeout threshold that triggers Standard UI fallback, and does the fallback expose full functionality or a reduced feature set?

12. **Quarantined evidence has no defined review or disposition workflow.**
    *Why it matters:* "Quarantine invalid evidence" appears in Failure Handling with no stated reviewer, retention period, or reprocessing/disposal path — a traceability gap for audit purposes.
    *Question:* What is the review cadence and disposition process (reprocess, discard, archive for audit) for evidence sent to quarantine, and who owns that review?

13. **Edge–Enterprise synchronization has no explicit conflict-resolution or case-level approval.**
    *Why it matters:* Synchronization (models, context, inspection results) is described as continuous/policy-driven with no stated mechanism for resolving conflicting updates (e.g., two sites receiving different context versions simultaneously) or for approving individual sync events.
    *Question:* Is synchronization fully automated and policy-driven with no case-level approval, and what is the conflict-resolution rule if concurrent updates disagree (e.g., version precedence, central override)?

14. **Isolated training pool segregation boundary is not defined.**
    *Why it matters:* Layer 9 states training pools are "isolated" and "segregated" from production capacity, but the diagram does not specify whether this is a logical (access-control) or physical (separate infrastructure) segregation — material for a security architecture review.
    *Question:* Is training-pool isolation enforced logically (network/access segmentation) or physically (separate infrastructure), and what compliance requirement, if any, drives that choice?

---

## 4. Summary for Evaluators

- **11 architectural layers**, **6 mandatory Quality Gates**, and **12 distinct actors** (7 human roles, 5 automated/system actors) were identified directly from the diagram.
- **11 core workflows** were derived, spanning synchronous edge inspection, asynchronous enterprise decisioning/MLOps, and continuous cross-cutting observability/governance.
- **14 open questions** are raised for BA/client validation before this architecture can move from "proposed design" to an approved baseline for SRS or contractual commitment. None of these gaps have been resolved by assumption; all require explicit client input.

*This document is derived solely from the referenced architecture diagram. It supersedes no existing Business Requirements Document or prior gap analysis and should be read alongside `AI_NATIVE_GAP_ANALYSIS.md` for any overlapping findings.*
