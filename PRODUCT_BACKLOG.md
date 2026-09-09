# Board Defect Inspection - Product Backlog

Version: 2.0 | Prepared: 2026-09-08 | Status: Development specification; business decision gates remain open

## 1. Scope and source of truth

Primary visual source: [Solution architecture.png](<Solution architecture.png>). Detailed behavior and component boundaries: [SOLUTION_ARCHITECTURE_MERMAID.md](SOLUTION_ARCHITECTURE_MERMAID.md). Business traceability follows the discovery BRD referenced by that document.

Deliver a conventional enterprise application with Angular/TypeScript, Java/Spring Boot, Python/ONNX Runtime, PostgreSQL, S3-compatible storage, RabbitMQ, NGINX, enterprise OIDC identity, Git/Jenkins and managed Linux VMs. The image groups components for presentation; the written architecture resolves arrow ambiguity: database outbox events reach RabbitMQ through a publisher, workers deliver external integrations, and original images are stored in object storage.

The scope includes camera acquisition, board identification, vision inference, versioned QC decisions, local durability, optional PLC control, OT/IT synchronization, human review, history/reporting, model governance and production operations. Hardware purchases, factory modifications and stakeholder approvals are external dependencies tracked below. Autonomous manufacturing changes, physical repair, generative AI, predictive maintenance, fixed YOLO selection and automatic unapproved model deployment are excluded.

No inspection accuracy, confidence threshold, latency, availability or delivery date is invented here. Stories contain executable behavior and test expectations; live hardware and production acceptance remain gated by the named decisions. All stories are initially **Not started**. This backlog is a specification, not evidence of implementation or approval.

## 2. Planning conventions

- **P0:** essential for reliable inspection, traceability, access control or production acceptance. **P1:** required enterprise capability that can follow the first controlled pilot. Optional integrations become release requirements only when selected.
- **R0 Foundation:** decisions, contracts, simulators and development platform. **R1 Controlled pilot:** one line/board scope, reviewed model and end-to-end review/evidence; live actuation disabled until approved. **R2 Enterprise rollout:** selected integrations, expanded reporting, redundancy and multi-line acceptance. **R3 Improvement:** governed additional model releases.
- **Open:** work can enter refinement immediately; listed prerequisites must still finish before integration. **Gated Dxx:** simulator/framework work can start, but production completion requires the named decision. **Conditional Dxx:** build live integration only if selected.
- Dependencies are story IDs; decision gates are separate. Owner labels designate accountable disciplines, not assigned individuals. Team estimates and capacity-based sprint commitments are set in refinement after decision gates and representative workloads are available.
- Feature groups are the epics below. Acceptance criteria are mandatory, uniquely addressable as `<story ID>-AC1`, etc. Development tasks are checklist items `<story ID>-T1`, etc.

## 3. Decision register and acceptance parameters

| ID | Decision and required artifact | Accountable owner | Blocks |
| --- | --- | --- | --- |
| D01 | Supported boards/revisions, defect catalogue, severities, tolerances, required views and identity policy; signed recipe examples | Quality + Manufacturing | Live capture, QC rules, model scope |
| D02 | Per-defect and board-level metrics, minimum critical recall, false-positive/negative limits, calibration criteria and review thresholds; approved evaluation matrix | Quality + ML | Model release and automatic PASS/FAIL |
| D03 | Peak/steady boards per minute, end-to-end maximum latency, inspection timeout and image sizes; workload profile | Manufacturing + Automation | Hardware sizing and performance acceptance |
| D04 | REVIEW/unavailable/missing-ID behavior, hold/manual/stop actions, reviewer SLA and authorized overrides; signed state/action matrix | Manufacturing + Quality | Live fallback, review release and actuation |
| D05 | Camera SDK, trigger protocol, board identity mapping, equipment access and camera/lighting acceptance sample | Automation | Hardware adapter acceptance |
| D06 | Whether PLC and MES/QMS are required; protocol/schema, command expiry, acknowledgement and reconciliation rules; interface contracts | Automation + Enterprise IT | Live external integrations |
| D07 | Operating hours, availability SLO, maximum offline time, RTO/RPO, standby strategy and failure domains; capacity/recovery plan | Manufacturing + IT Operations | Production topology and recovery acceptance |
| D08 | Retention by data class, legal holds, archive/deletion policy, expected volume and access/export restrictions | Quality + Compliance + Security | Lifecycle jobs and storage sizing |
| D09 | Representative images, ground-truth owner, label adjudication rules, independent dataset split and permitted data use | Quality + Data + ML | Validated model feasibility |
| D10 | Enterprise identity provider, line/site access matrix, MFA policy, certificate issuer and approval/deployment separation | Security + Enterprise IT | Production authentication and deployment roles |

Parameter contract: store approved values in versioned configuration with units and owner: `peakBoardsPerMinute`, `inspectionDeadlineMs`, `reviewSlaMinutes`, `commandExpiryMs`, `maxOfflineHours`, `availabilityTarget`, `rtoMinutes`, `rpoMinutes`, retention periods and per-defect metric thresholds. Sample fixtures must be marked TEST ONLY. Production startup rejects missing required configuration instead of silently adopting test defaults.

## 4. Shared implementation contracts

These are proposed development contracts to implement and version in PB-003; changes require migration and compatibility review.

### 4.1 Domain records

| Record | Minimum fields and invariants |
| --- | --- |
| InspectionAttempt | Globally unique inspectionId; optional boardId; board type/revision, batch, site, line, station; recipe/model/preprocessing versions; UTC capture/completion timestamps; processingStatus; initialDisposition; authoritativeDisposition; recordVersion; optional parentInspectionId. Never reuse boardId as an attempt key. |
| Evidence | evidenceId, inspectionId, viewId, capture timestamp, pixel dimensions, content type, byte length, SHA-256, storage key, synchronization status and retention class. Image bytes remain outside broker messages. |
| Prediction | predictionId, inspectionId, evidenceId, defect code, severity reference, confidence and score semantics, original-image coordinates when localization applies, model version. |
| ReviewDecision | reviewId, inspectionId, reviewer subject, prior recordVersion, decision, reason, timestamp and optional corrected annotations. Append changes; retain original AI outcome. |
| Command | commandId, inspectionId, expected board/state, disposition/action, issuer, creation/expiry timestamps, commandVersion, delivery/acknowledgement status and reason. |
| ReleasePackage | releaseId, model/recipe/preprocessing versions, supported board revisions, artifact checksums, approval identity/time, compatible runtime and previous release. |
| Event / AuditEvent | eventId, schemaVersion, eventType, aggregateId/version, occurredAt, correlationId, producer; audit adds actor, action, prior/new state reference and reason. |

Use foreign keys and uniqueness constraints, UTC timestamps, explicit schema migrations, and indexes supporting line/time/status queries. Record missing board identity explicitly and apply D01/D04 policy. Never fabricate a board ID. Model confidence is a score with documented semantics, not automatically a probability.

### 4.2 State and consistency rules

Processing state: `CAPTURED -> VALIDATING -> INFERENCING -> COMPLETED`; invalid images, unsupported configuration and timeout terminate as `UNAVAILABLE` with a reason. Incomplete/unavailable processing is not PASS. A completed attempt has initial disposition PASS, FAIL or REVIEW. REVIEW assignment state is separate: `OPEN -> CLAIMED -> RESOLVED`, with audited reassignment. Human decisions append revisions and update authoritativeDisposition transactionally.

Physical command state is separate: `PENDING -> SENT -> ACKNOWLEDGED`; failures can become `UNKNOWN`, `EXPIRED` or `FAILED`. UNKNOWN triggers reconciliation; it is not permission to repeat physical action. An ACK confirms the agreed protocol state, not proof of product quality.

Persist evidence durably, then commit the inspection, pending command and outbox event locally before dispatch. Synchronize centrally with at-least-once delivery and idempotent effects. Confirm image checksums before evidence becomes AVAILABLE; metadata can be RECEIVED while images remain PENDING. Reinspection is a new linked attempt. At review resolution, lock/check recordVersion; persist disposition, audit and outbox atomically. Validate current board state and command expiry at the edge before acting.

### 4.3 API and event surface

All enterprise APIs use `/api/v1`, versioned OpenAPI, JSON validation, correlation IDs, bounded pagination and standardized errors. User requests use OIDC; factory requests use line-scoped machine identities over mutual TLS. Never expose PostgreSQL or PLC access to browsers.

| Interface | Required behavior |
| --- | --- |
| POST /inspections | Idempotency-Key = inspectionId; identical retry returns the recorded response; reused ID with different immutable data returns 409. |
| PUT /inspections/{id}/evidence/{evidenceId} | Bounded streamed upload through the approved gateway; verify declared size/type/hash; retries do not create duplicate evidence. |
| GET /inspections and GET /inspections/{id} | Authorized filters, cursor pagination, complete history and evidence availability. |
| GET /inspections/{id}/evidence/{evidenceId} | Authorized evidence streaming; no unrestricted object-store URL. |
| GET /reviews; POST /reviews/{id}/claim; POST /reviews/{id}/decisions | Assignment and If-Match/recordVersion checks; 409 on stale edits; reasons mandatory. |
| GET /edge/commands; POST /edge/commands/{id}/ack | Poll by authenticated line with durable cursor; command expiry, state and acknowledgement identity validated. |
| GET /edge/releases/current; GET /edge/releases/{id}/artifact | Only compatible approved release manifests/artifacts for the authenticated line. |
| POST /recipes; POST /recipes/{id}/approve; POST /releases/{id}/approve | Versioned changes, server-side role checks and audit. Approval is separate from deployment. |
| GET /reports/quality; POST /reports/exports | Approved metric definitions, access-scoped filters, asynchronous bounded exports and freshness indication. |
| Events | InspectionRecorded.v1, EvidenceAvailable.v1, ReviewRequested.v1, ReviewResolved.v1, ReleaseApproved.v1, CommandStatusChanged.v1, AuditRecorded.v1. Stable eventId; consumers track duplicates and aggregate versions. |

Recommended HTTP errors: 400 invalid fields, 401 missing/invalid identity, 403 insufficient scope, 404 inaccessible/missing resource per agreed disclosure policy, 409 conflict, 413 oversize upload, 429 throttled, 503 dependency unavailable. Never put tokens, image bytes or sensitive review text in routine logs.

### 4.4 Initial permission matrix

D10 confirms this proposed matrix. All permissions are line/site-scoped and enforced by the backend.

| Role | Permissions |
| --- | --- |
| Operator | View assigned-line status/evidence and record operational acknowledgement; no quality override by default. |
| Inspector | Claim/review assigned cases; resolve only permitted dispositions under D04. |
| Quality approver | Approve rules/models and authorized overrides; cannot silently rewrite historical results. |
| Manager/analyst | Read scoped dashboards/history and approved exports; no deployment or override. |
| ML engineer | Access approved datasets; submit model candidates and evaluation; no self-approval. |
| Deployment administrator | Deploy approved software/model packages; no model self-approval or quality override. |
| Factory service | Upload own-line inspections, poll own-line releases/commands and acknowledge own commands only. |

## 5. Epic and release map

| Epic | Capability | Stories | Primary milestone |
| --- | --- | --- | --- |
| E01 | Decisions, contracts and engineering foundation | PB-001 to PB-005 | R0 |
| E02 | Camera acquisition and local inference | PB-006 to PB-010 | R1 |
| E03 | QC decisions, persistence and physical control | PB-011 to PB-015 | R1 |
| E04 | OT/IT gateway, synchronization and messaging | PB-016 to PB-020 | R1 |
| E05 | Identity, operator experience and human review | PB-021 to PB-025 | R1 |
| E06 | History, reporting and external integrations | PB-026 to PB-029 | R1/R2 |
| E07 | Dataset, model validation and controlled releases | PB-030 to PB-033 | R1/R3 |
| E08 | Audit, retention and security hardening | PB-034 to PB-037 | R1/R2 |
| E09 | Observability, deployment and resilience | PB-038 to PB-042 | R1/R2 |
| E10 | Integrated verification and operational acceptance | PB-043 to PB-046 | R1/R2 |

## 6. Detailed development backlog

### E01

#### PB-001 - Resolve quality and operational decisions

**Priority:** P0 | **Milestone:** R0 | **Owner:** BA / Quality / Manufacturing

**Readiness:** Open | **Dependencies:** None

**Traceability:** BO-01 to BO-08; BRD sections 12-25, 40-41

As a product owner, I need approved inspection rules and measurable acceptance targets so development can distinguish configurable behavior from unresolved business choices.

**Acceptance criteria**

1. **PB-001-AC1:** D01-D06 each have an owner, a signed artifact or explicit unresolved status, and linked examples for supported boards.
2. **PB-001-AC2:** D02/D03 define metric units, sample population and pass/fail evaluation method; illustrative BRD values are not adopted silently.
3. **PB-001-AC3:** D04 maps REVIEW, timeout, missing identity and lost acknowledgement to authorized operational actions.

**Development tasks**

- [ ] **PB-001-T1:** Run workshops and record D01-D06 decisions and interface availability.
- [ ] **PB-001-T2:** Produce a versioned recipe fixture and state/action table covering normal and failure cases.
- [ ] **PB-001-T3:** Publish acceptance parameter schema and tag unresolved stories with their decision gates.

#### PB-002 - Approve data, security and service objectives

**Priority:** P0 | **Milestone:** R0 | **Owner:** Security / Operations / Data

**Readiness:** Open | **Dependencies:** None

**Traceability:** BRD sections 18-19, 22, 26, 29-31

As an operations owner, I need explicit service and data obligations so infrastructure and controls can be sized and verified.

**Acceptance criteria**

1. **PB-002-AC1:** D07-D10 identify approvers, required artifacts and unresolved assumptions.
2. **PB-002-AC2:** Recovery and retention policies distinguish databases, images, model datasets and audit evidence.
3. **PB-002-AC3:** The role matrix includes approval/deployment separation and line-scoped service access.

**Development tasks**

- [ ] **PB-002-T1:** Document failure domains, SLO/RTO/RPO and offline capacity inputs.
- [ ] **PB-002-T2:** Create data classification, permitted-use and retention matrix.
- [ ] **PB-002-T3:** Map enterprise identity/certificate integrations and access test accounts.

#### PB-003 - Version domain, API and event contracts

**Priority:** P0 | **Milestone:** R0 | **Owner:** Backend / Edge / QA

**Readiness:** Open | **Dependencies:** None

**Traceability:** FR-002, FR-011, FR-012; BRD 25, 28

As an engineer, I need executable shared contracts so edge, UI and enterprise components integrate consistently.

**Acceptance criteria**

1. **PB-003-AC1:** OpenAPI and event schemas implement section 4, including validation, errors, identity and version fields.
2. **PB-003-AC2:** Contract fixtures cover duplicate/conflicting IDs, missing board ID, stale reviews and out-of-order events.
3. **PB-003-AC3:** Compatibility checks reject breaking schema changes without a version/migration plan.

**Development tasks**

- [ ] **PB-003-T1:** Define JSON schemas, OpenAPI and database ownership boundaries.
- [ ] **PB-003-T2:** Implement schema validation and shared fixtures for Java, Python and Angular clients.
- [ ] **PB-003-T3:** Add consumer/provider contract checks and document evolution rules.

#### PB-004 - Bootstrap application and developer environment

**Priority:** P0 | **Milestone:** R0 | **Owner:** Backend / Frontend / DevOps

**Readiness:** Open | **Dependencies:** PB-003

**Traceability:** Architecture: conventional application stack

As a developer, I need a reproducible local stack so I can run a complete synthetic inspection without factory access.

**Acceptance criteria**

1. **PB-004-AC1:** A clean checkout builds Angular, Spring Boot and the Python inference interface using pinned dependencies and documented commands.
2. **PB-004-AC2:** Development PostgreSQL, object storage, RabbitMQ and test identity services start with non-production credentials.
3. **PB-004-AC3:** Health checks distinguish liveness from dependency readiness; sample data is clearly test-only.

**Development tasks**

- [ ] **PB-004-T1:** Create application modules, edge service skeleton and Python package.
- [ ] **PB-004-T2:** Add database migrations and local service orchestration with seeded test data.
- [ ] **PB-004-T3:** Document setup, configuration injection, troubleshooting and teardown.

#### PB-005 - Provide simulators and automated engineering checks

**Priority:** P0 | **Milestone:** R0 | **Owner:** QA / Automation / DevOps

**Readiness:** Open | **Dependencies:** PB-003, PB-004

**Traceability:** AC-004 to AC-007; architecture: Git/Jenkins

As an engineer, I need deterministic equipment and dependency simulators so failure behavior is testable before hardware is available.

**Acceptance criteria**

1. **PB-005-AC1:** Simulators reproduce camera disconnects, missing views, delayed inference, duplicate triggers and lost PLC acknowledgements.
2. **PB-005-AC2:** CI builds and runs contract/unit/integration checks and produces identifiable artifacts without embedded secrets.
3. **PB-005-AC3:** A synthetic inspection traverses capture, persistence and a stub central endpoint with a stable correlation ID.

**Development tasks**

- [ ] **PB-005-T1:** Implement camera/board/PLC and inference simulators behind production adapter interfaces.
- [ ] **PB-005-T2:** Create versioned normal, invalid and adversarial fixtures.
- [ ] **PB-005-T3:** Configure Jenkins stages, artifact provenance and test reports.

### E02

#### PB-006 - Capture and correlate board identity

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / Automation

**Readiness:** Gated D01, D05 | **Dependencies:** PB-003, PB-005

**Traceability:** FR-001, FR-002

As a production operator, I need every capture assigned to the correct inspection attempt so evidence cannot be attributed to another board.

**Acceptance criteria**

1. **PB-006-AC1:** Each accepted trigger creates a unique inspectionId and captures available board/type/revision/line metadata.
2. **PB-006-AC2:** Duplicate triggers are deduplicated within the agreed hardware contract; reinspection creates a linked new attempt.
3. **PB-006-AC3:** Missing or conflicting identity is recorded and follows approved policy rather than guessing a board ID.

**Development tasks**

- [ ] **PB-006-T1:** Implement identity-source adapter and trigger correlation state machine.
- [ ] **PB-006-T2:** Persist trigger identity and lineage; isolate simultaneous line/station contexts.
- [ ] **PB-006-T3:** Exercise duplicate, reordered, missing and conflicting identity scenarios with simulator and D05 equipment.

#### PB-007 - Acquire and validate all required views

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / Automation / QA

**Readiness:** Gated D01, D03, D05 | **Dependencies:** PB-006

**Traceability:** FR-001; BRD 20-21

As an inspector, I need complete usable images so inspection never treats a missing view as a clean board.

**Acceptance criteria**

1. **PB-007-AC1:** The pinned recipe defines required views and capture deadline; missing/late views produce an explicit incomplete outcome.
2. **PB-007-AC2:** Image format, dimensions and configured quality checks are applied before inference; failures include view and reason.
3. **PB-007-AC3:** Original images are durably written with checksum and view metadata before the attempt can become complete.

**Development tasks**

- [ ] **PB-007-T1:** Implement camera SDK adapter, timeout handling and reconnect policy.
- [ ] **PB-007-T2:** Add recipe-driven multi-view collection and image validation.
- [ ] **PB-007-T3:** Verify wrong resolution, corrupt image, missing side, disconnected camera and lighting test samples.

#### PB-008 - Implement validated local inference service

**Priority:** P0 | **Milestone:** R1 | **Owner:** ML / Edge

**Readiness:** Open | **Dependencies:** PB-003, PB-004

**Traceability:** FR-003, FR-005 to FR-008; AI-006

As the inspection coordinator, I need structured predictions and explicit failures so QC decisions use a dependable model interface.

**Acceptance criteria**

1. **PB-008-AC1:** A request returns defect codes, scores, evidence/view identity, model version and original-image coordinates where applicable.
2. **PB-008-AC2:** Multiple detections are retained; malformed outputs, NaN scores, unknown classes and runtime errors return typed failures.
3. **PB-008-AC3:** No approved/compatible model means not-ready; test stubs are unmistakably non-production and cannot satisfy release validation.

**Development tasks**

- [ ] **PB-008-T1:** Implement ONNX loading, preprocessing/postprocessing and versioned inference interface.
- [ ] **PB-008-T2:** Restore bounding-box coordinates after resizing and validate output schema.
- [ ] **PB-008-T3:** Test representative fixtures, empty detections, multiple defects and incompatible runtime/model packages.

#### PB-009 - Coordinate inspection deadlines and concurrency

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / QA

**Readiness:** Gated D03, D04 | **Dependencies:** PB-007, PB-008

**Traceability:** FR-004; AC-004, AC-005

As a manufacturing operator, I need each inspection completed within its approved deadline without mixing concurrent boards.

**Acceptance criteria**

1. **PB-009-AC1:** One pinned model/recipe/preprocessing version is used throughout each attempt even during release activation.
2. **PB-009-AC2:** Late inference is recorded as unavailable and cannot overwrite a terminal outcome or release a board.
3. **PB-009-AC3:** Bounded concurrency and backpressure follow the configured overload policy; restart does not silently abandon in-flight attempts.

**Development tasks**

- [ ] **PB-009-T1:** Implement attempt state machine, deadline budget and bounded work queues.
- [ ] **PB-009-T2:** Add cancellation/result fencing and startup reconciliation for interrupted attempts.
- [ ] **PB-009-T3:** Load-test concurrent boards, timeout races and package switches using synthetic workloads.

#### PB-010 - Benchmark camera and inference hardware

**Priority:** P0 | **Milestone:** R1 | **Owner:** ML / Automation / Performance QA

**Readiness:** Gated D01, D03, D05, D09 | **Dependencies:** PB-007, PB-008, PB-009

**Traceability:** AI-001 to AI-004; AC-004, AC-005

As a solution owner, I need measured target-hardware capacity so the selected computer and cameras support actual production.

**Acceptance criteria**

1. **PB-010-AC1:** The benchmark uses representative board variants, image sizes, required views and peak workloads from approved decisions.
2. **PB-010-AC2:** Results report end-to-end and stage latency, deadline misses, throughput, CPU/GPU, memory and disk pressure.
3. **PB-010-AC3:** The hardware recommendation includes capacity headroom and a reproducible pass/fail report against D03; an unmet target blocks pilot approval.

**Development tasks**

- [ ] **PB-010-T1:** Build replay harness and capture measurements on candidate CPU/GPU equipment.
- [ ] **PB-010-T2:** Profile capture, preprocessing, inference and local commit costs.
- [ ] **PB-010-T3:** Publish sizing, bottlenecks and camera/lighting feasibility findings.

### E03

#### PB-011 - Manage versioned defect catalogues and recipes

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Quality

**Readiness:** Gated D01, D02, D04 | **Dependencies:** PB-003, PB-004

**Traceability:** FR-004; AI-005; BRD 13-16, 32

As a Quality approver, I need reviewed versioned rules so each board is evaluated against the correct criteria.

**Acceptance criteria**

1. **PB-011-AC1:** Draft recipes validate supported revisions, required views, severities, tolerances and required parameters.
2. **PB-011-AC2:** An approved version is immutable; edits create a new version and preserve approver/time/reason.
3. **PB-011-AC3:** Production activation rejects missing decision parameters and unsupported model/recipe combinations.

**Development tasks**

- [ ] **PB-011-T1:** Implement catalogue/recipe schema, validation and draft/approval APIs.
- [ ] **PB-011-T2:** Add approval audit events and compatibility manifest generation.
- [ ] **PB-011-T3:** Create fixtures for severity conflicts, absent critical rules and invalid threshold combinations.

#### PB-012 - Calculate board-level PASS, FAIL or REVIEW

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / Quality / QA

**Readiness:** Gated D01, D02, D04 | **Dependencies:** PB-009, PB-011

**Traceability:** FR-004, FR-008; proposed BR-001, BR-002

As a Quality manager, I need deterministic board-level decisions so multiple defects and uncertainty follow approved policy.

**Acceptance criteria**

1. **PB-012-AC1:** Given a pinned rule fixture, outcomes and reason codes match its severity/tolerance/multiple-defect decision table.
2. **PB-012-AC2:** Incomplete inspection, invalid output or low confidence alone cannot produce PASS; unavailable processing remains distinct.
3. **PB-012-AC3:** Every outcome records contributing predictions and rule/model versions, making replay of the same inputs deterministic.

**Development tasks**

- [ ] **PB-012-T1:** Implement pure decision evaluator and structured explanation payload.
- [ ] **PB-012-T2:** Define precedence for conflicting defects and review conditions from D01/D04.
- [ ] **PB-012-T3:** Add boundary, multi-defect, critical-defect and missing-view decision-table tests.

#### PB-013 - Persist local evidence, outcomes and outbox atomically

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / Backend

**Readiness:** Open | **Dependencies:** PB-003, PB-004

**Traceability:** FR-011; architecture: persist before dispatch

As an operations engineer, I need durable local results so a crash does not lose evidence or dispatch an unrecorded decision.

**Acceptance criteria**

1. **PB-013-AC1:** Durable image write precedes metadata commit; outcome, command intent and outbox records commit in one database transaction.
2. **PB-013-AC2:** A crash before commit produces no dispatchable command; a crash after commit leaves a recoverable pending record.
3. **PB-013-AC3:** Startup reconciles orphan files and incomplete attempts without deleting unsynchronized evidence.

**Development tasks**

- [ ] **PB-013-T1:** Create local migrations, evidence write/checksum protocol and outbox tables.
- [ ] **PB-013-T2:** Implement transactional repository and dispatcher eligibility checks.
- [ ] **PB-013-T3:** Inject crash points around image write, transaction commit and dispatch; verify recovery.

#### PB-014 - Apply explicit unavailable and fallback policies

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / Automation / Quality

**Readiness:** Gated D04, D07 | **Dependencies:** PB-009, PB-012, PB-013

**Traceability:** BRD 23; AC-007

As a production operator, I need visible approved fallback behavior when inspection cannot run.

**Acceptance criteria**

1. **PB-014-AC1:** Camera/model failure, storage exhaustion, timeout and missing configuration produce distinct unavailable reasons.
2. **PB-014-AC2:** Configured manual/hold/stop requests are recorded and routed through the control interface only when authorized; no silent PASS occurs.
3. **PB-014-AC3:** An edge outage has a documented independent operator/PLC procedure because software on the failed computer cannot execute fallback.

**Development tasks**

- [ ] **PB-014-T1:** Implement policy mapping, unavailable events and local status indicators.
- [ ] **PB-014-T2:** Define recovery criteria and manual acknowledgement for restart of inspection.
- [ ] **PB-014-T3:** Test each failure type and document the edge-down procedure with Automation.

#### PB-015 - Deliver and reconcile PLC commands

**Priority:** P0 | **Milestone:** R1 | **Owner:** Automation / Edge

**Readiness:** Conditional D06; gated D04 | **Dependencies:** PB-013, PB-014

**Traceability:** BRD 25; architecture: line control adapter

As an automation engineer, I need acknowledged board-specific commands so a retry cannot act on the wrong board.

**Acceptance criteria**

1. **PB-015-AC1:** Commands contain inspection/board identity, expected state and expiry; stale or mismatched commands are rejected and escalated.
2. **PB-015-AC2:** Acknowledgement loss produces UNKNOWN and reconciliation using the agreed PLC contract, not blind repeat actuation.
3. **PB-015-AC3:** Restart and duplicate delivery preserve command history; simulator mode is available and real actuation defaults disabled.

**Development tasks**

- [ ] **PB-015-T1:** Implement PLC adapter from D06 protocol and durable command/acknowledgement state machine.
- [ ] **PB-015-T2:** Add board-position validation, expiry and manual reconciliation workflow.
- [ ] **PB-015-T3:** Run hardware-in-loop tests for duplicate commands, delayed ACK, changed board position and restart.

### E04

#### PB-016 - Establish the controlled OT/IT gateway

**Priority:** P0 | **Milestone:** R1 | **Owner:** Network / Security / DevOps

**Readiness:** Gated D10 | **Dependencies:** PB-003, PB-004

**Traceability:** BRD 25, 29; architecture: industrial DMZ

As a security engineer, I need authenticated allowlisted factory connections so enterprise synchronization does not expose control equipment.

**Acceptance criteria**

1. **PB-016-AC1:** Only approved upload/poll endpoints are reachable from factory identities; direct browser/database/PLC routes are denied.
2. **PB-016-AC2:** Wrong, expired or revoked certificates fail authentication; service identity maps to permitted site/line.
3. **PB-016-AC3:** Gateway enforces body size/time limits and logs correlation IDs without credentials or image bodies.

**Development tasks**

- [ ] **PB-016-T1:** Configure NGINX mutual TLS, routing, certificate trust and network rules as code.
- [ ] **PB-016-T2:** Implement line identity propagation with spoofed-header prevention.
- [ ] **PB-016-T3:** Test unauthorized endpoints, cross-line requests, certificate rotation and large uploads.

#### PB-017 - Ingest inspections and verify evidence

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Data

**Readiness:** Open | **Dependencies:** PB-003, PB-004

**Traceability:** FR-011, FR-012; architecture: ingestion API

As a Quality investigator, I need consistent central records and verified evidence so partial uploads are visible.

**Acceptance criteria**

1. **PB-017-AC1:** Identical inspection retries have one effect; conflicting immutable data under the same ID returns 409.
2. **PB-017-AC2:** Evidence becomes AVAILABLE only after size/hash verification; interrupted uploads remain retryable and visibly PENDING.
3. **PB-017-AC3:** Metadata, ingestion audit and outbox changes commit atomically; access is scoped to the authenticated producer.

**Development tasks**

- [ ] **PB-017-T1:** Implement idempotent inspection endpoint, relational constraints and evidence streaming.
- [ ] **PB-017-T2:** Create object keys, checksums and pending/available reconciliation jobs.
- [ ] **PB-017-T3:** Test partial upload, bad checksum, duplicate/conflicting payload and central database failure.

#### PB-018 - Synchronize offline data and poll factory updates

**Priority:** P0 | **Milestone:** R1 | **Owner:** Edge / Backend

**Readiness:** Gated D07 | **Dependencies:** PB-013, PB-016, PB-017

**Traceability:** BRD 22-23, 25; architecture: synchronization worker

As an operator, I need inspections buffered during network outages and safely synchronized after recovery.

**Acceptance criteria**

1. **PB-018-AC1:** A simulated outage retains local records/evidence and retries with bounded backoff; synchronized data is not duplicated.
2. **PB-018-AC2:** Checkpoints advance only after durable central acknowledgement; local cleanup requires verified upload and retention eligibility.
3. **PB-018-AC3:** Release/command polling uses durable cursors and line scope; a crash after receipt permits safe replay without skipping commands.

**Development tasks**

- [ ] **PB-018-T1:** Implement checkpointed upload/poll workers and jittered retry/backoff.
- [ ] **PB-018-T2:** Add bounded spool thresholds, oldest-unsynced metrics and backpressure integration.
- [ ] **PB-018-T3:** Test disconnect/reconnect, central 429/503 responses, clock skew and worker restart.

#### PB-019 - Publish and consume durable business events

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / DevOps

**Readiness:** Open | **Dependencies:** PB-003, PB-017

**Traceability:** Architecture: PostgreSQL outbox, RabbitMQ, workers

As an integration owner, I need reliable asynchronous events so broker outages do not lose committed business changes.

**Acceptance criteria**

1. **PB-019-AC1:** Committed outbox events publish with stable IDs and publisher confirmation; broker failure leaves them pending.
2. **PB-019-AC2:** A consumer acknowledges only after durable processing; repeated delivery has one business effect.
3. **PB-019-AC3:** Poison messages reach a dead-letter queue after configured attempts and replay retains original event identity.

**Development tasks**

- [ ] **PB-019-T1:** Provision durable exchanges/queues and implement outbox claiming/publication.
- [ ] **PB-019-T2:** Implement consumer inbox/deduplication and aggregate-version ordering checks.
- [ ] **PB-019-T3:** Test crashes before/after publish and acknowledgement, broker disconnect and malformed payload.

#### PB-020 - Return authorized review dispositions to the edge

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Edge

**Readiness:** Gated D04, D06 | **Dependencies:** PB-018, PB-025

**Traceability:** FR-010; architecture: command polling

As a reviewer, I need my authorized decision delivered to the correct board with visible execution status.

**Acceptance criteria**

1. **PB-020-AC1:** A resolved review creates a versioned command atomically with its decision; factory polling returns only its own commands.
2. **PB-020-AC2:** The edge validates signature/identity, expiry and expected board/attempt state; stale commands are escalated without actuation.
3. **PB-020-AC3:** UI distinguishes decision recorded, command pending and action acknowledged; duplicate commands cannot create duplicate execution effects.

**Development tasks**

- [ ] **PB-020-T1:** Implement command polling/ack APIs and edge disposition validation.
- [ ] **PB-020-T2:** Connect valid commands to simulator or selected PLC adapter and persist execution history.
- [ ] **PB-020-T3:** Test review after board movement, duplicate poll, expired command and lost acknowledgement.

### E05

#### PB-021 - Implement enterprise sign-in and backend authorization

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Frontend / Security

**Readiness:** Gated D10 | **Dependencies:** PB-003, PB-004

**Traceability:** BRD 29; architecture: OIDC/RBAC

As a security owner, I need scoped identities and server-side authorization for every sensitive action.

**Acceptance criteria**

1. **PB-021-AC1:** Valid OIDC sessions permit only mapped roles/lines; expired tokens and wrong issuer/audience are rejected.
2. **PB-021-AC2:** Inspector, analyst, ML and deployment roles cannot approve or modify resources outside their permissions.
3. **PB-021-AC3:** Evidence reads, exports and direct API requests receive the same checks as UI actions; denied actions are observable.

**Development tasks**

- [ ] **PB-021-T1:** Integrate Angular sign-in/session handling and backend token verification.
- [ ] **PB-021-T2:** Implement permission policies, site/line scope and privileged MFA requirements.
- [ ] **PB-021-T3:** Automate permission-matrix tests including object-ID tampering and cross-line requests.

#### PB-022 - Build live inspection and evidence screens

**Priority:** P0 | **Milestone:** R1 | **Owner:** Frontend / Backend

**Readiness:** Open | **Dependencies:** PB-017, PB-021

**Traceability:** FR-006, FR-007, FR-011

As an operator, I need an accurate view of inspection status and evidence so I can identify quality or equipment issues.

**Acceptance criteria**

1. **PB-022-AC1:** The screen shows line/board/attempt identity, processing status, disposition, timestamps and evidence availability.
2. **PB-022-AC2:** Original images and overlays remain aligned through zoom/rotation; all required views and multiple detections are accessible.
3. **PB-022-AC3:** Loading, empty, unavailable and disconnected states are explicit; color is not the sole status indicator and keyboard navigation works.

**Development tasks**

- [ ] **PB-022-T1:** Implement paginated line feed and bounded status refresh.
- [ ] **PB-022-T2:** Build accessible image viewer, overlay transforms and metadata panel.
- [ ] **PB-022-T3:** Test missing evidence, large images, multiple views and stale connections on supported operator displays.

#### PB-023 - Manage review assignment and escalation

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Frontend

**Readiness:** Gated D04 | **Dependencies:** PB-019, PB-021

**Traceability:** FR-009; BRD 24

As an inspector, I need an ordered review queue with ownership so cases are not lost or reviewed concurrently without control.

**Acceptance criteria**

1. **PB-023-AC1:** REVIEW outcomes create one case; queue filtering respects line access and configured priority/SLA.
2. **PB-023-AC2:** Concurrent claims allow one owner; reassignment is authorized and audited without discarding work history.
3. **PB-023-AC3:** Overdue cases generate deduplicated escalation events and remain visible until resolved.

**Development tasks**

- [ ] **PB-023-T1:** Implement review-case schema, claim/reassignment API and indexed queue queries.
- [ ] **PB-023-T2:** Build queue/assignment screens with age, priority and claimant information.
- [ ] **PB-023-T3:** Test duplicate review events, simultaneous claims, abandoned assignments and SLA timers.

#### PB-024 - Capture human evidence and corrected annotations

**Priority:** P0 | **Milestone:** R1 | **Owner:** Frontend / Backend / Quality

**Readiness:** Gated D04, D09 | **Dependencies:** PB-022, PB-023

**Traceability:** FR-009; BRD 18-19, 24

As a reviewer, I need to inspect original evidence and record corrections so uncertainty can be resolved with provenance.

**Acceptance criteria**

1. **PB-024-AC1:** Review displays original prediction, complete evidence and model/rule versions without altering the source image.
2. **PB-024-AC2:** Corrections use original-image coordinates and include reviewer identity, reason and timestamp.
3. **PB-024-AC3:** Unsure/disputed cases can be escalated; corrected labels are marked unverified until the ground-truth process approves them.

**Development tasks**

- [ ] **PB-024-T1:** Build annotation add/edit tools and review draft persistence.
- [ ] **PB-024-T2:** Implement correction validation and provenance schema.
- [ ] **PB-024-T3:** Test coordinate transforms, unavailable evidence, reload of drafts and disputed label handling.

#### PB-025 - Resolve reviews with concurrency-safe overrides

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Frontend / Quality

**Readiness:** Gated D04, D10 | **Dependencies:** PB-023, PB-024

**Traceability:** FR-010; proposed BR-003

As an authorized inspector, I need an auditable final decision that cannot silently overwrite another review.

**Acceptance criteria**

1. **PB-025-AC1:** Decision submission requires permitted disposition, reason and current recordVersion; a stale version returns 409.
2. **PB-025-AC2:** Original AI outcome remains immutable; human decision, authoritative disposition, audit and command intent commit together.
3. **PB-025-AC3:** A rejected/unauthorized request creates no disposition command, and UI explains conflicts without resubmitting blindly.

**Development tasks**

- [ ] **PB-025-T1:** Implement transactional resolution endpoint, concurrency checks and role/rule policy.
- [ ] **PB-025-T2:** Add decision confirmation/reason UI and conflict refresh workflow.
- [ ] **PB-025-T3:** Test simultaneous overrides, unauthorized transitions, duplicate submissions and transaction rollback.

### E06

#### PB-026 - Search complete inspection history

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Frontend

**Readiness:** Open | **Dependencies:** PB-017, PB-021, PB-025

**Traceability:** FR-012; AC-006

As a Quality investigator, I need to reconstruct why a board received its disposition.

**Acceptance criteria**

1. **PB-026-AC1:** Search filters board/attempt, line, date, defect and disposition with stable bounded pagination.
2. **PB-026-AC2:** Detail shows initial predictions, evidence, rule/model versions, all reviews, reinspection lineage and command states.
3. **PB-026-AC3:** Unavailable or expired evidence is labelled explicitly; access checks cover every linked record.

**Development tasks**

- [ ] **PB-026-T1:** Implement indexed history queries and authoritative detail endpoint.
- [ ] **PB-026-T2:** Build history filters, timeline and linked reinspection navigation.
- [ ] **PB-026-T3:** Verify reconstruction across overrides, missing board ID, pending upload and retained metadata after image expiry.

#### PB-027 - Provide quality dashboards and controlled exports

**Priority:** P1 | **Milestone:** R2 | **Owner:** Backend / Frontend / Data

**Readiness:** Gated D08 | **Dependencies:** PB-019, PB-026

**Traceability:** BRD 27; architecture: reporting replica

As a manager, I need consistent quality metrics and exports without slowing inspection or miscounting attempts.

**Acceptance criteria**

1. **PB-027-AC1:** Reports distinguish attempts from unique boards, unavailable inspections from completed outcomes and initial from authoritative dispositions.
2. **PB-027-AC2:** Totals reconcile to a fixed fixture; defect distribution declares whether its denominator is defects, boards or attempts.
3. **PB-027-AC3:** Replica freshness is visible; scoped asynchronous exports use bounded resources, audited downloads and expiry.

**Development tasks**

- [ ] **PB-027-T1:** Define report metric catalogue and reinspection/override/timezone semantics.
- [ ] **PB-027-T2:** Implement reporting replica queries, aggregates and asynchronous export jobs.
- [ ] **PB-027-T3:** Build dashboard filters; test totals, lag, access restrictions and spreadsheet-formula escaping.

#### PB-028 - Integrate selected MES and quality systems

**Priority:** P1 | **Milestone:** R2 | **Owner:** Integration / Enterprise IT

**Readiness:** Conditional D06 | **Dependencies:** PB-019, PB-025

**Traceability:** BRD 25

As a manufacturing systems owner, I need inspection and revised review outcomes delivered under the agreed external contract.

**Acceptance criteria**

1. **PB-028-AC1:** Selected interfaces map board/attempt, defects, evidence references and authoritative disposition without exposing unrestricted images.
2. **PB-028-AC2:** Retries use the external idempotency/correlation contract and prevent duplicate downstream effects where supported.
3. **PB-028-AC3:** Permanent rejection and unknown delivery state remain visible; replay and reconciliation are authorized and audited.

**Development tasks**

- [ ] **PB-028-T1:** Implement D06 mapping, protocol adapter and versioned contract fixtures.
- [ ] **PB-028-T2:** Persist per-destination delivery/acknowledgement state and reconcile uncertain outcomes.
- [ ] **PB-028-T3:** Run partner sandbox tests for outage, duplicate delivery, schema rejection and later human override.

#### PB-029 - Deliver operational and review notifications

**Priority:** P1 | **Milestone:** R2 | **Owner:** Backend / Operations

**Readiness:** Gated D04 | **Dependencies:** PB-019, PB-023

**Traceability:** BRD 24, 31; architecture: notifications

As a support owner, I need actionable alerts with controlled escalation so inspection failures receive attention.

**Acceptance criteria**

1. **PB-029-AC1:** Configured review/system events route to authorized recipients with line, severity and a protected application link.
2. **PB-029-AC2:** Repeated events are grouped/deduplicated; retries and failed delivery are recorded without blocking inspection.
3. **PB-029-AC3:** Notification content excludes raw images, tokens and unrestricted review text; acknowledgement/escalation follows configured policy.

**Development tasks**

- [ ] **PB-029-T1:** Implement notification adapter, templates and recipient configuration.
- [ ] **PB-029-T2:** Add deduplication, delivery tracking and escalation scheduler.
- [ ] **PB-029-T3:** Test channel outage, alert storms, recipient scope and resolution messages.

### E07

#### PB-030 - Curate versioned datasets and verified ground truth

**Priority:** P0 | **Milestone:** R1 | **Owner:** Data / Quality / ML

**Readiness:** Gated D01, D08, D09 | **Dependencies:** PB-003

**Traceability:** BRD 18-19; BO-08

As an ML engineer, I need representative verified datasets so evaluation reflects the supported manufacturing scope.

**Acceptance criteria**

1. **PB-030-AC1:** Dataset manifests record evidence hashes, label versions, board/revision, provenance and permitted use.
2. **PB-030-AC2:** Quality adjudication resolves disputed labels; reviewer corrections are not promoted automatically.
3. **PB-030-AC3:** Splits isolate related boards/batches/images to prevent leakage and report class/variant coverage, including rare defects.

**Development tasks**

- [ ] **PB-030-T1:** Import approved historical data and implement manifest/annotation validation.
- [ ] **PB-030-T2:** Define adjudication workflow and versioned train/validation/independent-test partitions.
- [ ] **PB-030-T3:** Produce data-quality, duplicate, representation and access/retention reports.

#### PB-031 - Train and independently evaluate candidate models

**Priority:** P0 | **Milestone:** R1 | **Owner:** ML / Quality

**Readiness:** Gated D01, D02, D03, D09 | **Dependencies:** PB-008, PB-030

**Traceability:** AI-001 to AI-007; AC-001 to AC-005

As a Quality approver, I need reproducible model evidence so only candidates meeting agreed quality and timing criteria can progress.

**Acceptance criteria**

1. **PB-031-AC1:** Evaluation reports per-defect and board-level precision/recall, false positives/negatives, confusion matrices, sample counts and target-hardware latency.
2. **PB-031-AC2:** Threshold/calibration tuning uses development/validation data; the independent test set is reserved for final evaluation.
3. **PB-031-AC3:** A candidate failing any mandatory D02/D03 criterion is ineligible for approval; unsupported/rare categories are declared, not hidden in overall accuracy.

**Development tasks**

- [ ] **PB-031-T1:** Implement reproducible training/configuration capture and ONNX export validation.
- [ ] **PB-031-T2:** Evaluate calibration where scores are used and document score semantics.
- [ ] **PB-031-T3:** Publish signed-off evaluation artifacts, dataset versions and model limitations for review.

#### PB-032 - Approve, distribute and roll back model packages

**Priority:** P0 | **Milestone:** R1 | **Owner:** ML / Backend / Edge / Quality

**Readiness:** Gated D02, D10 | **Dependencies:** PB-011, PB-018, PB-031

**Traceability:** AI-006, AI-007; AC-008; BRD 30

As a deployment administrator, I need verified approved packages so model changes are controlled and reversible.

**Acceptance criteria**

1. **PB-032-AC1:** Only Quality-approved compatible model/preprocessing/recipe bundles are offered to a line; checksums and approval provenance are verified at the edge.
2. **PB-032-AC2:** Activation occurs between attempts, preserves the prior package and pins running attempts to their original versions.
3. **PB-032-AC3:** Failed download/health check leaves the prior release active; rollback records history and cannot install an incompatible or unapproved package.

**Development tasks**

- [ ] **PB-032-T1:** Implement candidate/approved/deployed registry and separation of approval from deployment.
- [ ] **PB-032-T2:** Build resumable artifact transfer, integrity checks, atomic activation and rollback.
- [ ] **PB-032-T3:** Exercise corrupt download, approval denial, incompatible runtime, in-flight inspection and staged-line rollout.

#### PB-033 - Monitor model quality and govern improvement cycles

**Priority:** P1 | **Milestone:** R3 | **Owner:** ML / Data / Quality

**Readiness:** Gated D02, D09 | **Dependencies:** PB-024, PB-025, PB-030, PB-032

**Traceability:** BO-08; BRD 30-31

As a Quality manager, I need verified post-release metrics so degradation can trigger investigation and a controlled new release.

**Acceptance criteria**

1. **PB-033-AC1:** Quality metrics join predictions to verified labels and expose sample size, delay, scope and unlabelled coverage.
2. **PB-033-AC2:** Input/defect-rate shifts generate investigation signals rather than claims of measured accuracy loss.
3. **PB-033-AC3:** Retraining candidates follow the same curation, independent evaluation and approval gates; no automatic production replacement occurs.

**Development tasks**

- [ ] **PB-033-T1:** Ingest verified review labels into the controlled dataset workflow.
- [ ] **PB-033-T2:** Implement cohort metrics and configurable drift/investigation alerts.
- [ ] **PB-033-T3:** Create retraining request records linking trigger, dataset, experiment and eventual release.

### E08

#### PB-034 - Archive business audit events without gaps

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Security / Data

**Readiness:** Open | **Dependencies:** PB-019, PB-021

**Traceability:** BRD 28-29; FR-010

As an auditor, I need a protected record of decisions and privileged changes so their provenance can be demonstrated.

**Acceptance criteria**

1. **PB-034-AC1:** Business state changes and audit outbox entries commit together; archive delivery failure leaves retryable durable events.
2. **PB-034-AC2:** Archive records include actor, action, aggregate/version, timestamp, reason and correlation; ordinary application roles cannot update/delete them.
3. **PB-034-AC3:** Duplicate archive delivery is idempotent and audit gaps/backlogs are detected; authorized audit queries are themselves recorded.

**Development tasks**

- [ ] **PB-034-T1:** Implement shared audit emission for reviews, recipes, releases, exports and administration.
- [ ] **PB-034-T2:** Create restricted archive writer/read roles and retention-lock integration when selected.
- [ ] **PB-034-T3:** Test transaction rollback, archive outage, tampering attempts and replay reconciliation.

#### PB-035 - Apply retention, archival and legal-hold policies

**Priority:** P1 | **Milestone:** R2 | **Owner:** Data / Compliance / Backend

**Readiness:** Gated D08 | **Dependencies:** PB-017, PB-030, PB-034

**Traceability:** BRD 26, 28

As a data owner, I need controlled lifecycle management so evidence is retained and deleted according to approved obligations.

**Acceptance criteria**

1. **PB-035-AC1:** Policy dry-run reports affected images, results, labels, artifacts and audit records before destructive execution.
2. **PB-035-AC2:** Legal hold, active investigation, unsynchronized evidence and required deployed artifacts prevent ineligible deletion.
3. **PB-035-AC3:** Lifecycle jobs retain tombstones/provenance where permitted, update evidence availability and account for replicas/backups under D08.

**Development tasks**

- [ ] **PB-035-T1:** Implement per-class retention metadata, holds and idempotent archival/deletion jobs.
- [ ] **PB-035-T2:** Add policy administration, dry-run report and restricted execution audit.
- [ ] **PB-035-T3:** Test hold precedence, partial deletion recovery, object/metadata consistency and backup expiration rules.

#### PB-036 - Harden secrets, encryption and network access

**Priority:** P0 | **Milestone:** R1 | **Owner:** Security / DevOps

**Readiness:** Gated D10 | **Dependencies:** PB-016, PB-021

**Traceability:** BRD 29; architecture: security controls

As a security owner, I need protected service identities and data across the deployment.

**Acceptance criteria**

1. **PB-036-AC1:** Production secrets are injected from the approved store, excluded from repository/artifacts/logs and restricted by service.
2. **PB-036-AC2:** TLS and encryption-at-rest settings are verified for applicable databases, evidence and backups; rotated credentials/certificates work without unauthorized bypass.
3. **PB-036-AC3:** Network tests deny unapproved paths and browser-to-PLC/database access; privileged and service actions respect D10.

**Development tasks**

- [ ] **PB-036-T1:** Provision least-privilege accounts, secrets references and encryption keys.
- [ ] **PB-036-T2:** Implement rotation/expiry monitoring and documented recovery from expired credentials.
- [ ] **PB-036-T3:** Run negative access, transport, log-redaction and artifact-secret scans.

#### PB-037 - Verify application and supply-chain security

**Priority:** P0 | **Milestone:** R1 | **Owner:** Security / QA / DevOps

**Readiness:** Open | **Dependencies:** PB-005, PB-021

**Traceability:** BRD 29; architecture: build/test/scan

As a release owner, I need security verification that covers APIs, uploads and dependencies before pilot deployment.

**Acceptance criteria**

1. **PB-037-AC1:** CI generates dependency inventory and scans code/dependencies/artifacts under the agreed security policy.
2. **PB-037-AC2:** Tests cover broken object authorization, malicious uploads, injection, cross-site scripting, session handling and rate limits.
3. **PB-037-AC3:** Findings have reproducible evidence and remediation ownership; unresolved release-blocking findings prevent deployment.

**Development tasks**

- [ ] **PB-037-T1:** Add artifact inventory/provenance, dependency checks and secret scanning to Jenkins.
- [ ] **PB-037-T2:** Implement bounded file handling, output escaping and API abuse tests.
- [ ] **PB-037-T3:** Review threat model for OT/IT, review overrides, artifact delivery and external integrations.

### E09

#### PB-038 - Instrument inspection and enterprise operations

**Priority:** P0 | **Milestone:** R1 | **Owner:** Backend / Edge / Operations

**Readiness:** Open | **Dependencies:** PB-004, PB-013

**Traceability:** BRD 31; architecture: observability

As an on-call engineer, I need correlated metrics and logs to locate inspection failures quickly.

**Acceptance criteria**

1. **PB-038-AC1:** An inspection correlation ID connects capture, inference, persistence, synchronization, review and command records where those stages exist.
2. **PB-038-AC2:** Metrics expose latency, deadline misses, throughput, unavailable reasons, spool space, unsynced age, queue depth and review age.
3. **PB-038-AC3:** Metric labels avoid unbounded board/inspection IDs; telemetry failure cannot block local inspection and sensitive data is redacted.

**Development tasks**

- [ ] **PB-038-T1:** Add OpenTelemetry spans and structured logs at shared boundaries.
- [ ] **PB-038-T2:** Expose Prometheus metrics and Grafana operational dashboards.
- [ ] **PB-038-T3:** Create diagnostic fixtures proving correlation, cardinality limits and telemetry-outage behavior.

#### PB-039 - Define service alerts and support runbooks

**Priority:** P0 | **Milestone:** R1 | **Owner:** Operations / Quality

**Readiness:** Gated D03, D04, D07 | **Dependencies:** PB-038

**Traceability:** BRD 22-23, 31

As on-call support, I need actionable alarms and recovery procedures tied to approved service objectives.

**Acceptance criteria**

1. **PB-039-AC1:** Alerts cover stalled inspection, no camera input, storage pressure, synchronization age, broker/DB failure and certificate expiry with configured severities.
2. **PB-039-AC2:** Each alarm links to a runbook with diagnosis, authorized action, escalation and recovery verification.
3. **PB-039-AC3:** SLO dashboards show measurement window and exclusions from D07; drills demonstrate alarm triggering and clearing without alert floods.

**Development tasks**

- [ ] **PB-039-T1:** Define alert rules, routing and operational dashboards from approved parameters.
- [ ] **PB-039-T2:** Write runbooks for edge down, camera failure, central outage, storage full and UNKNOWN commands.
- [ ] **PB-039-T3:** Exercise alerts through the approved monitoring channel and retain drill evidence.

#### PB-040 - Deploy controlled VM environments and releases

**Priority:** P0 | **Milestone:** R1 | **Owner:** DevOps / Security

**Readiness:** Gated D07, D10 | **Dependencies:** PB-005, PB-036, PB-037

**Traceability:** Architecture: managed Linux VMs, Git/Jenkins

As a deployment administrator, I need reproducible isolated environments and reversible releases.

**Acceptance criteria**

1. **PB-040-AC1:** Development/test/production use separated credentials and data; one identifiable tested artifact is promoted with recorded authorization.
2. **PB-040-AC2:** Central software deployment uses health checks and rollback; edge upgrades occur in approved windows without mixing attempt versions.
3. **PB-040-AC3:** Database migration checks document compatibility and forward recovery; rollback never assumes irreversible migrations can be undone. Before pilot use, encrypted database/object backups and a matching-evidence restore are demonstrated; PB-041 extends this to enterprise failover.

**Development tasks**

- [ ] **PB-040-T1:** Create VM/service provisioning and environment-specific configuration templates.
- [ ] **PB-040-T2:** Implement Jenkins promotion, artifact verification and application rollback.
- [ ] **PB-040-T3:** Rehearse migration compatibility, failed startup, edge maintenance recovery and baseline pilot backup/restore.

#### PB-041 - Implement failover and disaster recovery

**Priority:** P0 | **Milestone:** R2 | **Owner:** Operations / Data / QA

**Readiness:** Gated D07, D08 | **Dependencies:** PB-040

**Traceability:** BRD 22, 31; architecture: data platform/resilience

As a manufacturing owner, I need proven recovery of inspections and evidence within agreed objectives.

**Acceptance criteria**

1. **PB-041-AC1:** Chosen topology includes redundant application/gateway endpoints, PostgreSQL standby and replicated RabbitMQ queues across approved failure domains.
2. **PB-041-AC2:** Database failover avoids two writable primaries; evidence backup/restore includes matching metadata and verified checksums.
3. **PB-041-AC3:** Restore/failover drills measure actual RTO/RPO against D07 and identify lost/unreconciled data; unmet objectives block enterprise rollout.

**Development tasks**

- [ ] **PB-041-T1:** Provision replication, failover fencing, backups and recovery access.
- [ ] **PB-041-T2:** Implement coordinated database/object restore and queue/outbox reconciliation procedures.
- [ ] **PB-041-T3:** Run isolated restore, node failure, gateway outage and failback drills with evidence.

#### PB-042 - Onboard additional lines and enforce isolation

**Priority:** P1 | **Milestone:** R2 | **Owner:** Edge / Backend / Operations

**Readiness:** Gated D01, D03, D07 | **Dependencies:** PB-032, PB-040, PB-041

**Traceability:** BRD 31; architecture: repeat per production line

As a manufacturing manager, I need new lines onboarded without leaking data or exhausting existing inspection capacity.

**Acceptance criteria**

1. **PB-042-AC1:** Each line has its own identity, compatible approved recipe/model and independently bounded edge resources.
2. **PB-042-AC2:** Central load from one line cannot cross authorization boundaries; capacity tests exercise planned concurrent lines.
3. **PB-042-AC3:** Onboarding verifies camera, clock synchronization, package, connectivity, fallback and support ownership before activation.

**Development tasks**

- [ ] **PB-042-T1:** Create line registration and configuration/deployment checklist.
- [ ] **PB-042-T2:** Add per-line quotas, access tests and capacity dashboards.
- [ ] **PB-042-T3:** Rehearse line onboarding, removal and high-load neighbor scenarios.

### E10

#### PB-043 - Verify the complete pilot inspection workflow

**Priority:** P0 | **Milestone:** R1 | **Owner:** QA / Quality / Automation

**Readiness:** Gated D01-D06, D09, D10 | **Dependencies:** PB-010, PB-012, PB-014, PB-020, PB-026, PB-032, PB-034, PB-036, PB-037, PB-040

**Traceability:** AC-001 to AC-008

As a product owner, I need demonstrated end-to-end behavior before the controlled pilot.

**Acceptance criteria**

1. **PB-043-AC1:** A supported board traverses capture, inference, decision, durable evidence, central history and applicable review with one traceable attempt.
2. **PB-043-AC2:** Scenarios include PASS, FAIL, REVIEW, unavailable, multiple defects, reinspection and human override, using approved fixtures and model evidence.
3. **PB-043-AC3:** All AC-001 through AC-008 have linked reports and owner disposition; selected PLC integration additionally requires PB-015 hardware acceptance.

**Development tasks**

- [ ] **PB-043-T1:** Assemble requirement-to-test matrix and representative end-to-end fixtures.
- [ ] **PB-043-T2:** Run integrated pilot tests including role/line access and package/version traceability.
- [ ] **PB-043-T3:** Record defects, repeat failed cases after fixes and publish pilot acceptance evidence.

#### PB-044 - Verify peak load, disconnection and crash recovery

**Priority:** P0 | **Milestone:** R1 | **Owner:** Performance QA / Edge / Operations

**Readiness:** Gated D03, D04, D07 | **Dependencies:** PB-018, PB-019, PB-038, PB-040

**Traceability:** AC-004, AC-005; BRD 22-23, 31

As an operations owner, I need fault and load evidence that inspection remains controlled during expected failures.

**Acceptance criteria**

1. **PB-044-AC1:** Peak-load and endurance tests meet approved throughput/deadline limits and expose resource headroom and unavailable outcomes.
2. **PB-044-AC2:** Network/broker outages, partial uploads, disk exhaustion and crashes around commits cause no silent evidence loss or unrecorded physical command.
3. **PB-044-AC3:** Replay reconciles duplicates and pending records; duration/capacity tests use D07 offline limits and verify fallback when limits are exceeded.

**Development tasks**

- [ ] **PB-044-T1:** Build workload and fault-injection scenarios around transaction/acknowledgement boundaries.
- [ ] **PB-044-T2:** Measure end-to-end latency, spool growth, retry behavior and recovery convergence.
- [ ] **PB-044-T3:** Publish pass/fail report and remediate bottlenecks before release approval.

#### PB-045 - Conduct operational handover and pilot go-live

**Priority:** P0 | **Milestone:** R1 | **Owner:** Product / Quality / Manufacturing / Operations

**Readiness:** Gated D01-D10 | **Dependencies:** PB-039, PB-043, PB-044

**Traceability:** BRD 40; AC-001 to AC-008

As a manufacturing owner, I need trained operators and an approved rollback/fallback plan before live use.

**Acceptance criteria**

1. **PB-045-AC1:** Quality and Manufacturing approve pilot scope, model/rules, fallback, review staffing and go/no-go criteria; unresolved mandatory gates prevent live automatic control.
2. **PB-045-AC2:** Operators demonstrate review, escalation and edge-down procedures; support can locate evidence and execute authorized recovery.
3. **PB-045-AC3:** Deployment, smoke checks, observation period and rollback responsibilities are recorded; pilot limitations versus enterprise HA are explicit.

**Development tasks**

- [ ] **PB-045-T1:** Prepare operator/support guides and run scenario-based training.
- [ ] **PB-045-T2:** Complete production readiness checklist and scoped pilot approvals.
- [ ] **PB-045-T3:** Execute controlled deployment, record observed results and track follow-up defects.

#### PB-046 - Accept enterprise rollout and selected integrations

**Priority:** P0 | **Milestone:** R2 | **Owner:** Product / Quality / Operations

**Readiness:** Gated D06-D08 | **Dependencies:** PB-027, PB-029, PB-035, PB-041, PB-042, PB-045

**Traceability:** BRD 25-31, 40

As the business sponsor, I need enterprise acceptance evidence across selected lines and integrations.

**Acceptance criteria**

1. **PB-046-AC1:** Selected PLC/MES/QMS interfaces pass partner/hardware acceptance; unselected integrations are explicitly marked not applicable with D06 approval.
2. **PB-046-AC2:** Multi-line capacity, recovery objectives, retention/hold behavior and security controls pass the approved acceptance matrix.
3. **PB-046-AC3:** Release evidence includes restore/failback drills, outstanding risks, ownership and business/operational sign-off; no planned control is represented as tested.

**Development tasks**

- [ ] **PB-046-T1:** Run PB-015/PB-028 acceptance when their integrations are selected.
- [ ] **PB-046-T2:** Complete enterprise UAT, retention/hold rehearsal and multi-line/recovery evidence review.
- [ ] **PB-046-T3:** Publish release record, support ownership and scheduled post-release review.

## 7. Delivery sequence and dependency handling

These are dependency waves, not date or effort commitments. Prerequisite IDs in each story take precedence over release labels. Implementing framework code with fixtures does not close a production decision gate.

| Wave | Work package | Exit evidence |
| --- | --- | --- |
| A | PB-001/PB-002 decision workshops; PB-003 contracts; PB-004 scaffold; PB-005 simulators/CI | Executable contracts, clean local build, tracked decision artifacts and fault-capable simulators |
| B | PB-006/PB-007 capture, PB-008 inference interface, PB-011 recipes, PB-013 persistence; PB-016/PB-017 gateway/ingestion; PB-021 identity; PB-030 dataset | Synthetic durable inspection synchronized through authenticated interfaces; approved live-data scope tracked |
| C | PB-009/PB-010 coordination/benchmark, PB-012/PB-014 QC/fallback; PB-018/PB-019 synchronization/events; PB-022 to PB-025 UI/review; PB-031 evaluation | Complete simulated decision/review path, independent model report and fault evidence |
| D | PB-020 review commands, selected PB-015 PLC, PB-026 history, PB-032 releases, PB-034/PB-036/PB-037 controls, PB-038 to PB-040 operations | Approved package, access/audit evidence, operational dashboards and repeatable deployment |
| E | PB-043/PB-044 integrated and fault/load tests; PB-045 pilot | AC-001 to AC-008 evidence and scoped go-live approval |
| F | PB-027 to PB-029 enterprise reporting/integrations, PB-035 lifecycle, PB-041/PB-042 resilience/scale; PB-046 rollout | Selected integrations, recovery and multi-line UAT accepted |
| G | PB-033 governed improvement | Verified production feedback and subsequent release through existing approval gates |

Security, identity, audit, baseline backup/restore procedures and tested fallback are pilot requirements. R2 expands recovery to the approved enterprise failover topology; it does not authorize an unprotected pilot. If D07 requires full redundancy for the first production line, PB-041 moves into the R1 gate.

**First refinement package:** PB-001 through PB-005. Refine PB-003's schemas before parallel component implementation. Then choose a vertical slice: synthetic board -> local evidence/outbox -> authenticated central ingestion -> authorized history view. Assign individual owners and estimate after the team reviews fixtures, hardware access and shared contracts.

For each conditional story, record SELECTED or NOT APPLICABLE with D06 evidence. If SELECTED, PB-015 is a hard prerequisite to live PLC actuation, and PB-028 is a hard prerequisite to the relevant enterprise integration acceptance. A conditional dependency cannot be bypassed merely because its story is P1.

## 8. Verification and requirement coverage

| Source requirement/component | Delivery stories | Required verification |
| --- | --- | --- |
| FR-001 image capture; cameras/lighting | PB-006, PB-007, PB-010 | Trigger correlation, required views, corrupt/late images and hardware sample acceptance |
| FR-002 board identification | PB-003, PB-006, PB-026 | Missing ID policy, duplicate trigger and reinspection lineage |
| FR-003, FR-005 to FR-008 defect detection/classification/localization/confidence | PB-008, PB-010, PB-012, PB-030, PB-031 | Per-defect metrics, multiple detections, coordinate mapping and score semantics |
| FR-004 board classification | PB-009, PB-011, PB-012, PB-014 | Approved decision tables; incomplete or low-confidence-only input never implies PASS |
| FR-009/FR-010 human review/override | PB-020, PB-023, PB-024, PB-025 | Claim races, stale edits, authorized outcomes and command expiry |
| FR-011/FR-012 evidence/history | PB-013, PB-017, PB-018, PB-026, PB-035 | Checksums, interrupted upload, history reconstruction and retention |
| AI-001 to AI-005, AI-007 | PB-010, PB-030, PB-031, PB-033 | Independent test evidence, critical recall, false positives/negatives and calibration where applicable |
| AI-006; approved model/version | PB-008, PB-011, PB-032 | Recorded compatible versions, approval, failed rollout and rollback |
| Local coordinator/QC/PLC | PB-009, PB-012 to PB-015, PB-020 | Deadline fencing, commit-before-dispatch, acknowledgement loss and stale board state |
| DMZ gateway/synchronization | PB-016 to PB-018, PB-036 | Mutual TLS, network denial, offline recovery and checkpoint replay |
| Angular/SSO/Spring Boot | PB-003, PB-004, PB-021 to PB-027 | API contracts, access matrix, evidence UI, concurrency and report reconciliation |
| PostgreSQL/object storage/reporting replica/backups | PB-013, PB-017, PB-027, PB-035, PB-041 | Transaction invariants, evidence consistency, visible lag and restore |
| RabbitMQ/workers/MES/notifications | PB-019, PB-028, PB-029 | Idempotency, dead-letter replay, partner contract and escalation |
| Model governance/Git/Jenkins | PB-005, PB-030 to PB-033, PB-037, PB-040 | Dataset provenance, independent evaluation, approval separation and artifact promotion |
| Security/audit/traceability | PB-021, PB-026, PB-034 to PB-037 | Cross-line denial, tamper resistance, encryption and audit completeness |
| Observability/resilience/multi-line operations | PB-038 to PB-042, PB-044 | Fault alarms, SLO measurements, failover, RTO/RPO and isolation |
| AC-001 defect detection | PB-031, PB-043 | Approved performance for every in-scope defect |
| AC-002 critical defects | PB-012, PB-031, PB-043 | Approved critical recall and critical-rule cases |
| AC-003 false positives | PB-031, PB-043 | Agreed false-positive metric on independent data |
| AC-004 throughput / AC-005 latency | PB-010, PB-043, PB-044 | End-to-end target-hardware peak-load measurements |
| AC-006 traceability | PB-026, PB-034, PB-043 | Reconstruct board/attempt, evidence, versions, review and command history |
| AC-007 human review | PB-023 to PB-025, PB-043 | Approved uncertain-case handling, role checks and review escalation |
| AC-008 approved model use | PB-032, PB-043 | Reject unapproved/incompatible packages and retain previous approved release |

Test implementation choices: Java unit/integration tests for transactions and rules; Python tests for inference contracts and coordinate transforms; Angular component and browser workflow tests for review/accessibility; simulator and hardware-in-loop tests for acquisition/control; workload/fault harnesses for offline/load/recovery. Use real PostgreSQL/RabbitMQ/object-store test instances for delivery and persistence semantics rather than claiming mocks prove durability.

## 9. Definition of Ready

A story is Ready for sprint commitment when:

- Its accountable team and individual assignee are recorded and the team has estimated/split it into a deliverable increment.
- Referenced schemas and fixtures exist; acceptance criteria identify positive, negative and failure cases.
- Prerequisites are delivered or a documented contract-compatible stub is agreed for the intended increment.
- Named decision gates are resolved for the intended scope, or the increment is explicitly limited to simulator/framework work with live acceptance still open.
- Required equipment, data, accounts and test environment are accessible.
- API/data migration, authorization, operational and test impacts are understood.

Do not label an entire gated story Done because its simulator path works. Track remaining live acceptance explicitly. Do not substitute invented targets for missing D02/D03/D07 inputs.

## 10. Definition of Done

A development story is Done when:

- All numbered acceptance criteria pass with linked test evidence and required decision artifacts.
- Implementation is reviewed, builds reproducibly, and passes relevant contract, integration, security and workflow checks.
- Persistent changes include verified migrations and recovery/compatibility notes.
- Sensitive actions enforce backend authorization and emit required audit records.
- Required metrics, error messages, runbook updates and operator-facing failure states are implemented.
- No release-blocking defects remain under the agreed quality/security policy.
- Documentation and fixtures match deployed behavior; demonstrations use the correct model/rule/artifact versions.
- The product/Quality owner accepts business behavior where required; production deployment is tracked separately from code completion.

## 11. Release evidence checklist

| Gate | Required evidence | Accountable approver |
| --- | --- | --- |
| Scope and rules | D01-D04 artifacts, reviewed recipe/action fixtures and identified unsupported cases | Quality / Manufacturing |
| Equipment and integration | D05/D06 contracts; camera checks; selected PLC/MES acceptance; actuation enablement record | Automation / Enterprise IT |
| Model quality | Dataset lineage, independent evaluation, approved package and rollback rehearsal | Quality / ML |
| Security | D10 role matrix, denial tests, network/certificate checks, scans and issue disposition | Security |
| Data and recovery | D07/D08 policies, backups, recovery drill, evidence consistency and retention plan | Operations / Compliance |
| Pilot functionality | PB-043/PB-044 reports tied to AC-001 through AC-008 | QA / Quality |
| Operational readiness | Runbooks, trained reviewers/operators, alert drill, support ownership and fallback demonstration | Manufacturing / Operations |
| Enterprise rollout | Selected integration reports, multi-line capacity, HA/failback and lifecycle evidence | Product / Operations / Quality |

The product owner maintains this backlog as decisions are resolved. Scope changes must update the architecture, affected contracts, story dependencies and verification matrix together.
