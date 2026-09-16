# Traditional and AI Native Engineering Gap Analysis

## AI-Based Automated Board Defect Inspection System

Version 1.0 | 9 September 2026 | Architecture and engineering assessment

Prepared for Business, Manufacturing, Quality, Architecture, Engineering, Data/ML, Security and Operations stakeholders.

Status: Recommendations for review. This is a document-based assessment, not a production implementation audit or an approved delivery commitment.

## 1. Executive assessment

The proposed solution has a credible foundation for AI Native engineering. It already combines an industrial computer-vision inspection service with deterministic quality rules, human review, evidence retention, model governance and enterprise operational controls. Its use of Angular, Spring Boot, PostgreSQL, RabbitMQ and managed Linux VMs does not prevent it from becoming AI Native.

The most significant transition is to make requirements, datasets, evaluation, model changes and production feedback first-class engineering assets, with reproducible evidence connecting business acceptance to each deployed inspection package. A second transition is to use AI throughout engineering work under explicit review, testing and access controls. Neither transition requires autonomous production agents or replacement of the existing application stack.

The BRD remains a discovery document. Defect definitions, representative data, quality thresholds, throughput, latency, fallback behavior, availability, retention and ROI are unresolved. These are business and feasibility blockers shared by traditional and AI Native delivery. AI-assisted development cannot resolve them without manufacturing observations and accountable stakeholder decisions.

Recommended direction:

- Preserve the local inspection path, deterministic QC module, OT/IT boundary, durable evidence, human authority and controlled deployment.
- Operationalize the existing model-governance design through executable data contracts, reproducible experiments, statistically defensible evaluation and approved feedback loops.
- Introduce AI-assisted requirements, implementation, testing and incident analysis as measured engineering practices.
- Consider an evidence-grounded quality investigation assistant only after core inspection acceptance is demonstrated and a separate business case exists.
- Keep physical repair, autonomous manufacturing-parameter changes, predictive maintenance and general-purpose defect detection outside the scope stated in BRD section 11.2.

The near-term investment priority is evidence and feasibility, followed by a reliable vertical slice and controlled pilot. A broad platform rewrite or agent framework purchase is not justified by the supplied requirements.

## 2. Evidence, scope and interpretation

### 2.1 Source register

| Ref | Source | Role in this analysis |
| --- | --- | --- |
| S1 | Business Requirements Document.docx; discovery version 1.0; sections 1–47 | Primary business source. Includes FR-001–FR-012, AI-001–AI-007, AC-001–AC-008, example rules and open questions. |
| S2 | Solution architecture.png; “Proposed Design — BRD discovery v1.0” | Primary architectural baseline, visually reviewed. Defines OT inspection, DMZ, enterprise services, data, model governance and operations. |
| S3 | SOLUTION_ARCHITECTURE_MERMAID.md | Supporting explanation of the proposed topology and controls. Used to clarify S2; does not establish implementation. |

The workspace filename is “Business Requirements Document.docx,” corresponding to the document requested. The architecture is explicitly proposed. Current factory performance, delivered software, deployed models, production datasets, security implementation and operational results have not been audited. No implementation maturity score or quantified benefit is claimed.

BRD sample defect IDs, image counts, dashboard values and confidence examples are illustrative. They are not accepted taxonomy, available datasets or performance evidence. BR-001–BR-005 require confirmation. Numeric acceptance values remain TBD.

### 2.2 Assessment labels

| Label | Meaning |
| --- | --- |
| Documented | Explicitly represented in the proposed architecture or BRD; implementation unverified. |
| Partial | Intent is documented, but executable detail, ownership or acceptance evidence is incomplete. |
| Open | Explicit business/discovery decision remains unresolved. |
| Not evidenced | The reviewed sources do not describe the capability; this does not prove organizational absence. |
| Optional | Proposed enhancement beyond the core inspection requirements; requires separate prioritization. |

Priorities: P0 must close before the affected live production behavior; P1 establishes repeatable delivery and sustainable scaling; P2 is an optional optimization. Preparatory work can proceed while a production gate remains open.

### 2.3 What AI Native means here

This document uses AI Native as an engineering operating model: teams design around measurable AI behavior, manage data and evaluation alongside code, learn from verified operational evidence, and use AI tools responsibly across the delivery lifecycle. It is a working definition, not a certification or prescribed technology stack.

Three comparisons must remain separate:

1. Current manufacturing inspection: manual and/or existing automation, still to be established under BRD sections 7–10.
2. Proposed conventional software delivery with a dedicated ML service: the actual architectural baseline in S2.
3. Target AI Native delivery and operation: the same reliable application foundation with stronger evidence automation, governed learning and AI-assisted engineering.

Mature traditional engineering and MLOps already use many target practices. The comparison describes emphasis and integration, not capabilities exclusive to an “AI Native” label. Generative AI in the product, AI-assisted software development and computer vision at runtime are separate choices.

## 3. Traditional versus AI Native comparison

| Dimension | Conventional delivery emphasis | AI Native target for this solution | Practical change |
| --- | --- | --- | --- |
| Requirements | Requirements and stories reviewed as documents | Requirements linked to executable quality rules, evaluation slices and acceptance reports | Version the defect catalogue, supported scope and acceptance contracts. |
| Design | Application services and interfaces define behavior | Code, model, data, preprocessing and recipe jointly define behavior | Treat the compatible inspection package as the release unit. |
| Feasibility | Functional prototype demonstrates workflow | Representative-data experiments establish quality and hardware feasibility early | Validate difficult and rare defects before promising automation. |
| Implementation | Engineers write and review code | Engineers also direct AI tools using bounded tasks and approved context | Measure completed, accepted work and defects rather than generated code volume. |
| Testing | Unit, integration, system and acceptance tests | Those tests plus independent ML evaluation, robustness and feedback-quality checks | One release evidence bundle covers deterministic and statistical behavior. |
| Data | Data is primarily operational storage | Training and evaluation datasets are versioned products | Record provenance, annotation policy, sample selection and permitted use. |
| Release | Build and deploy application artifact | Promote approved software/model/data-evidence/configuration combinations | Block incompatible or insufficiently evaluated packages. |
| Operations | Availability, latency and application errors | Also measure ground-truth quality, coverage, drift signals and review demand | Detect quality degradation even when services remain healthy. |
| Improvement | Prioritized defects and periodic model work | Verified feedback feeds a governed experiment backlog | Automate candidate creation and evidence collection; retain release approval. |
| User experience | Forms, dashboards and review | Evidence-first review; optional grounded investigation assistance | Reduce investigation effort without transferring disposition authority. |
| Security | Users, services, dependencies and networks | Also protect datasets, model artifacts, prompts and AI tool access | Apply additional controls only where the AI capability is introduced. |
| Economics | Delivery cost and operational savings | Also track labeling, evaluation, model maintenance and AI tool overhead | Fund capabilities against measured quality and productivity outcomes. |

## 4. Architecture baseline: retain and extend

### 4.1 Existing strengths

S2 already documents camera acquisition and board correlation, a Java inspection coordinator, Python/ONNX Runtime vision service, versioned QC rules and PASS/FAIL/REVIEW outcomes. An approved model-and-recipe package includes versioning and rollback. Local PostgreSQL and image spooling support persistence before dispatch; the line adapter tracks commands and acknowledgements. Synchronization uses retries, deduplication and capacity limits.

The industrial DMZ uses allowlisted HTTPS and mutual TLS, with factory-initiated communication. Enterprise services support ingestion, authorized review/override, configuration, history and an outbox. Data services include object storage, audit, replication and encrypted backups. Model governance already shows verified labels, versioned datasets, independent evaluation, Quality approval, staged release and rollback. Operations include monitoring, security, resilience and traceability. [S2; S3]

These controls should remain in the target architecture. Their presence materially reduces the design gap, while their implementation and effectiveness still require verification.

### 4.2 Component changes

| Existing component | Recommended extension | Reason |
| --- | --- | --- |
| Cameras and SDK adapter | Version capture settings; record camera/lighting configuration; automated image-quality checks | Acquisition changes can invalidate model performance without a software change. |
| Inspection coordinator | Explicit supported-scope checks, attempt-level package pinning and deadline fencing | Prevent mixed versions and late results from affecting the wrong board. |
| Vision service | Stable input/output schema, preprocessing provenance, failure codes and target-hardware evaluation | Make statistical behavior and service behavior independently testable. |
| QC decision module | Approved executable decision tables and complete-view rules | Model confidence is an input to policy, not the authoritative disposition. |
| Local persistence and synchronization | Traceable image hashes, schema versions, sampling eligibility and evidence completeness | Reconstruct decisions and safely reuse authorized evidence. |
| Review and override | Separate operational disposition from verified training-label status | An override may reflect context or workflow rather than a corrected defect label. |
| Object storage and data platform | Dataset manifests, split membership, lineage and annotation versions | Reproducible model evaluation needs more than retained image files. |
| Model governance | Experiment records, reusable evaluation jobs and machine-verifiable release manifests | Convert the documented lifecycle into repeatable delivery evidence. |
| Git/Jenkins delivery | AI work instructions, artifact promotion gates and integrated evaluation reports | Support AI-assisted engineering without weakening existing controls. |
| Observability | Verified quality metrics by defect/variant, label lag, sampling coverage and model version | Infrastructure health does not establish inspection effectiveness. |
| Angular reporting | Optional permission-aware investigation assistant | Potentially shorten evidence retrieval and explanation work. |

## 5. Prioritized gap register

### 5.1 Business, data and inspection gaps

| ID / priority | Evidence and status | Gap and business consequence | Closure evidence / accountable owner |
| --- | --- | --- | --- |
| G01 / P0 | S1 §§5, 7–10, 39, Q03–Q06; Open | No validated baseline or accepted quality/throughput targets. Success and ROI cannot be assessed. | Observed current-state report, metric definitions and signed targets. Product, with Quality/Manufacturing/Finance. |
| G02 / P0 | S1 §§12–14, Q01–Q02, Q07–Q08; Open | Board scope and taxonomy are examples. Training, rules and acceptance could use different definitions. | Approved scope matrix, defect examples, tolerances and unsupported-case policy. Quality. |
| G03 / P0 | S1 §§18–20, Q09–Q11; S2 cameras/datasets; Partial | No representative inventory or imaging feasibility evidence. Critical defects may not be visible or sufficiently represented. | Camera trial and sample inventory by defect, variant, line and condition. Automation, supported by Data/Quality. |
| G04 / P0 | S1 §19; S2 verified labels; Partial | Label ownership is requested, but adjudication and disagreement handling are unspecified. | Annotation handbook, reviewer qualification and adjudication audit. Quality. |
| G05 / P0 | AI-007; S2 independent evaluation; Partial | Independent testing is required, but split construction, leakage checks and statistical acceptance are unspecified. | Frozen grouped test manifest, slice results and approved uncertainty method. ML lead; Quality accepts results. |
| G06 / P0 | AI-005, FR-004, §32; S2 QC rules; Partial/Open | Review thresholds and board decision semantics are unresolved. A detector score could be mistaken for board acceptability. | Approved decision tables covering complete, uncertain, unsupported and failed inspections. Quality. |
| G07 / P0 | S1 §§21–23, 25; S2 local control; Partial/Open | Deadline, capacity and physical fallback policies are unconfirmed. | Hardware timing report, selected interface contract, command/fault tests and approved fallback. Manufacturing/Automation. |
| G08 / P1 | S1 BO-08, §§24, 30; S2 curation; Partial | Feedback exists conceptually; unbiased sampling and training eligibility are unspecified. | Sampling plan covering PASS/FAIL/REVIEW, verified-label state machine and candidate dataset audit. Data lead. |
| G09 / P1 | S1 §§28, 30; S2 registry; Partial | Package/version intent exists; reproducible experiment and full dependency lineage are incomplete. | Replayable experiment record and immutable release manifest. ML/platform lead. |
| G10 / P0 | S1 AC-008; S2 staged release/rollback; Partial | Approval control is shown; compatibility enforcement and rollback criteria need executable proof. | Rejected unapproved package, staged promotion and compatible rollback drill. Release owner, with Quality approval. |
| G11 / P0 | S1 §§24, 41 Q12/Q18; S2 review; Partial/Open | Review staffing, deadlines and escalation capacity are unresolved. | Measured review load, staffed process and overdue-case/fallback rehearsal. Quality operations. |
| G12 / P1 | S1 §31, Q25; S2 observability; Partial | Monitoring intent exists; measured quality needs ground truth, sampling and label-lag handling. | Quality dashboard with denominators, verification coverage, freshness and escalation runbook. ML operations. |

### 5.2 Engineering and governance gaps

| ID / priority | Evidence and status | Gap and business consequence | Closure evidence / accountable owner |
| --- | --- | --- | --- |
| G13 / P1 | S2 Git/Jenkins; AI development workflow not evidenced | No documented method for supplying approved context to engineering AI or reviewing its work. | Versioned task/context template, access policy and accepted pilot changes. Engineering lead. |
| G14 / P1 | S1 AC-001–AC-008; S2 CI and model evaluation; Partial | Requirement-to-code/test/model-evidence links are not shown as an executable release gate. | Acceptance matrix resolving each requirement to versioned test/evaluation evidence. QA lead. |
| G15 / P0 | S1 §§26, 28–29; S2 security/audit; Partial/Open | Retention and authorization questions remain; AI datasets add reuse and artifact-protection needs. | Approved lifecycle/access matrix, artifact integrity tests and retrieval/deletion controls. Security/Data governance. |
| G16 / P0 | S1 §§22–23, 31; S2 resilience; Partial/Open | Redundancy and backups are proposed, but recovery objectives and demonstrated recovery are absent. | Accepted RTO/RPO/offline duration and drills restoring linked evidence. Operations. |
| G17 / P1 | S1 §6; S2 Quality approval; Partial | Stakeholder groups exist; ownership across data, models, software and production incidents needs definition. | Named role assignments, escalation path and release decision record. Product/Engineering leadership. |
| G18 / P1 | S1 §§37–39, Q22–Q23; Open | No established cost baseline or AI engineering productivity evidence. | Cost-per-board model and controlled productivity comparison including rework. Finance/Product. |
| G19 / P2 | Conversational assistance absent from core FRs; Optional | Investigation assistance may save time, but relevance, access and answer quality are unproven. | Scoped benchmark and pilot with verified answers, permissions and measurable benefit. Product. |
| G20 / P2 | Autonomous process modification excluded by S1 §11.2 | Unbounded runtime agents would exceed approved scope and introduce new authority paths. | Explicitly exclude from this release; any future proposal needs a separately assessed scope change. Manufacturing/Product. |

P0 items mostly close existing BRD obligations rather than adding AI Native scope. P1 items make delivery repeatable and measurable. A gap is closed by accepted evidence, not by the presence of a tool or a diagram box.

## 6. Target operating architecture

Use three boundaries with different timing and authority requirements.

| Boundary | Flow | Timing / authority |
| --- | --- | --- |
| Local inspection | Capture → correlate identity → validate required views/scope → infer → apply QC rules → persist → dispatch selected line command → reconcile acknowledgement | Must satisfy the approved physical decision deadline. Only approved deterministic policy and authorized human disposition control outcomes. |
| Governed improvement | Authorized evidence → sample → label/adjudicate → version dataset → experiment → independent evaluation → Quality approval → staged package deployment → monitoring | Asynchronous. Candidate generation or retraining does not grant production authority. |
| Engineering assistance | Approved requirements/context → AI-assisted task → engineer review → tests/evaluations → acceptance evidence → controlled release | Development boundary. AI tools have scoped repository/test access and no standing production authority. |

The central application and DMZ continue to distribute approved packages and review dispositions. An optional quality assistant sits behind enterprise authentication and accesses approved read APIs. It is not a dependency of capture, inference, QC or PLC execution.

### 6.1 Proposed release manifest

The inspection release should identify: release ID; model artifact hash; model format/runtime compatibility; preprocessing/postprocessing version; taxonomy and recipe versions; capture configuration constraints; supported board/revision/view matrix; application/API schema compatibility; dataset and evaluation report IDs; approval identity/time; activation scope; and compatible rollback reference.

Pin the release to an inspection attempt before inference. Activate new packages at an approved attempt boundary, validate integrity and compatibility, and preserve the previous approved package. Reject incomplete manifests. Camera or recipe changes must trigger the relevant revalidation even if the model file is unchanged.

### 6.2 Proposed evidence contracts

| Record | Minimum recommended contents |
| --- | --- |
| Inspection attempt | Inspection ID; available board ID; reinspection parent; line, batch, board type/revision; capture times; required/received views; image hashes; release ID; predictions; initial disposition; reason codes; processing status. |
| Human decision | Attempt ID; actor/role; prior record version; disposition; reason; timestamp; superseded decision link; authority status. |
| Label record | Image/region ID; taxonomy version; label; annotator; adjudicator where required; verification state; evidence source; allowed dataset use. |
| Dataset manifest | Sample IDs/hashes; collection scope/time; label versions; grouping keys; split membership; exclusions; sampling provenance; access/retention policy. |
| Evaluation run | Model and code hashes; runtime/hardware; dataset manifest; metric definitions; thresholds; per-slice counts/results; uncertainty estimates; failure cases; reviewer. |
| Physical command | Command ID; attempt ID; intended action; validity window; expected board state; dispatch status; acknowledgement; reconciliation outcome. |

Operational review and training labels must remain separate records. A board held for another process reason is not automatically a visual defect example. Historical evidence should preserve both the original AI outcome and subsequent authoritative decisions.

## 7. Data and computer-vision feasibility

### 7.1 Start with observability of the defect

Run acquisition trials using real board variants and representative production conditions. Inspect resolution at the smallest relevant defect, motion blur, exposure, reflections, vibration, required views and occlusions. Quality must confirm that captured images contain enough information to apply its defect definitions. An invisible or internal defect may require a different inspection modality or exclusion from visual scope.

Compare plausible model approaches on the same acceptance contract. Detection, segmentation, classification, reference comparison and anomaly detection are candidates, not prescribed selections. Assess quality, label requirements, maintainability and target-hardware performance together. A more complex model is justified only by measured benefit.

### 7.2 Dataset lifecycle

Collect authorized evidence with provenance; deduplicate at image and related-board levels; label against the approved taxonomy; adjudicate uncertainty; create versioned training/validation/test partitions; evaluate; and preserve the lineage of accepted releases. Keep multiple views and repeated images of the same board together. Where relevant, group by batch or time and include held-out production conditions to test intended deployment generalization.

Use training data for learning and validation data for model/threshold selection. Keep the final test set independent of iterative tuning. After repeated evaluation influences decisions, create a fresh independent acceptance set rather than silently treating the old set as untouched. Record augmentation and synthetic origin; synthetic data may supplement experiments but cannot replace representative real-world acceptance evidence.

### 7.3 Rare defects and feedback bias

Sparse critical defects are a feasibility constraint. Report counts and uncertainty rather than concealing sparse slices in overall accuracy. Consider targeted collection, archived confirmed cases or controlled exemplars approved by Quality. If sufficient evidence is unavailable, narrow the supported scope or retain additional manual inspection.

Sampling only rejected or reviewed boards misses defects in automatic PASS outcomes. Establish independent audits of PASS boards and representative samples across outcomes, shifts, variants and lines. Record selection probabilities where sampling differs by group and use appropriate weighting for population estimates. An override rate is a workflow signal, not an unbiased estimate of model error.

## 8. Evaluation and acceptance strategy

### 8.1 Define the metrics before setting thresholds

| Metric | Proposed definition / caution |
| --- | --- |
| Per-defect recall | Matched true detections / actual defects for that class. Specify instance matching and localization criteria. |
| Board false-negative rate | Defective boards automatically classified PASS / all ground-truth defective boards evaluated. This follows the BRD's operational concern. |
| Board false-positive rate | Good boards classified FAIL / all ground-truth good boards evaluated. Report good boards routed to REVIEW separately. |
| Released-board escape fraction | Defective boards ultimately released / all boards ultimately released, including human decisions. Distinct from model false-negative rate. |
| Review rate | Attempts routed to REVIEW / all eligible attempts. Show unavailable and unsupported attempts separately. |
| Automatic-decision coverage | Eligible attempts with automatic PASS or FAIL / all eligible attempts. Show quality versus coverage tradeoffs. |
| Latency and deadline misses | Defined trigger to durable disposition and, if required, acknowledged physical action. Report percentiles, maximum observed and deadline-miss rate. |
| Operational quality | Scrap, rework, review effort and confirmed downstream escapes using stable board-level denominators. |

REVIEW must not disappear from reporting to make quality look better. Report model detections, initial board dispositions and final operational dispositions separately. Multiple defects mean defect-level totals do not equal board counts; reinspection attempts must not inflate unique production-board counts.

Raw model confidence is not a validated probability that a board is acceptable. Validate threshold behavior by defect and operating slice, evaluate calibration where relevant, and require complete usable evidence for PASS. Unknown or out-of-distribution checks can support abstention but do not guarantee detection of every novel defect.

### 8.2 Statistical acceptance

Quality and ML should agree the confidence level, sampling design, minimum slice evidence and acceptable uncertainty before final testing. For critical defects, consider a lower confidence bound on recall and an upper bound on false-negative rate, rather than point estimates alone. If the interval is too wide, collect more evidence or limit automation.

For illustration only: with independent representative defective-board trials and zero observed misses, the exact one-sided 95% binomial upper bound on miss probability is 1 − 0.05^(1/n). At n = 300 it is approximately 0.994%. Zero misses therefore does not establish zero risk. Related views or repeated boards do not provide 300 independent trials. This example is not a proposed acceptance target.

### 8.3 Required evaluation layers

| Layer | Evidence required |
| --- | --- |
| Deterministic software | State transitions, permissions, rules, idempotency, stale commands, concurrent reviews and schema compatibility. |
| Statistical model | Per-defect and board metrics; slice counts; confidence intervals; localization matching; threshold and calibration assessment. |
| Robustness | Lighting/camera variation, blur, unfamiliar revision, missing views, corrupted images, multiple defects and supported-scope boundaries. |
| Hardware and integration | Target-hardware capture-to-action timing, peak and sustained load, trigger correlation, selected PLC/MES handshakes. |
| Failure and recovery | Inference timeout, edge crash, lost acknowledgement, central outage, spool exhaustion, duplicate replay, restore and package rollback. |
| Human workflow | Evidence comprehension, authorized override, disagreements, review surge, stale board location and fallback execution. |

### 8.4 BRD acceptance traceability

| BRD criteria | Gap IDs | Acceptance evidence |
| --- | --- | --- |
| AC-001; FR-003/005/006/008; AI-001 | G02–G05, G14 | Independent per-defect and localization report across agreed variants, including multiple defects. |
| AC-002; AI-002/003 | G01–G06 | Critical-defect results with sample sizes/uncertainty and approved QC rule cases. |
| AC-003; AI-004 | G01, G05–G06 | Good-board false-positive assessment plus review/coverage tradeoff. |
| AC-004/005; FR-001 | G03, G07, G16 | End-to-end peak-load timing on intended equipment; fault/fallback evidence. |
| AC-006; FR-002/011/012; AI-006 | G09, G14–G16 | Reconstruct attempt, evidence, release, review and command; restore matching metadata and images. |
| AC-007; FR-007/009/010; AI-005 | G06, G11 | Approved uncertainty policy, role checks, workload and escalation exercise. |
| AC-008; AI-007; §30 | G05, G09–G10 | Independent evaluation, approval, incompatible-package rejection and rollback. |
| BO-08; §§24, 30–31 | G08, G12 | Verified feedback lineage and monitored production quality with visible label lag. |

AI-assisted engineering and optional conversational assistance do not replace any BRD acceptance criterion.

## 9. AI Native software delivery lifecycle

### 9.1 Bounded AI-assisted work

| Stage | Useful AI-assisted work | Human responsibility and verification |
| --- | --- | --- |
| Discovery | Extract questions, map requirements and identify contradictions | BA validates source fidelity; stakeholders resolve business decisions. |
| Architecture | Draft alternatives, decision records and failure scenarios | Architect validates constraints, interfaces and operational consequences. |
| Implementation | Draft adapters, migrations, UI changes and test scaffolds | Engineer reviews behavior, dependencies, access and recovery implications. |
| Testing | Suggest boundary/failure cases and generate fixtures | QA independently checks expected results and tests real durability semantics. |
| Data/ML | Assist annotation proposals, experiment code and failure clustering | Quality verifies labels; ML prevents leakage and validates results. |
| Release | Assemble requirement-to-evidence summaries | Release owners verify reports and approve the actual artifact. |
| Operations | Summarize logs and suggest diagnostic steps | Operator validates evidence and authorizes production changes. |

Create a versioned engineering context pack containing the approved BRD decisions, architecture, API schemas, data contracts, state machine, coding conventions, test commands and prohibited production actions. Each task should identify source requirements, scope, permitted files/tools, acceptance criteria and unresolved assumptions. Refresh context when requirements change.

AI-generated tests and AI-generated implementation can share the same misunderstanding. Independent specification review, trusted fixtures and hardware/integration checks remain necessary. Do not allow an assistant to redefine acceptance thresholds simply to make its change pass.

### 9.2 Delivery evidence and Definition of Done

A change is complete when the relevant source requirements are linked; implementation and generated artifacts are reviewed; applicable deterministic and model tests pass; data/model/configuration lineage is recorded; access and audit behavior are verified; migration/recovery implications are addressed; and operating instructions match the released behavior. Model or recipe changes require the applicable Quality acceptance even when no application code changes.

For AI-assisted changes, record tool/model identity where available and material context/task versions sufficient for audit, without storing unnecessary secrets or confidential prompts. Preserve the accepted code and test evidence: repeating an AI interaction is not a substitute for a reproducible build.

### 9.3 Measuring engineering benefit

Run a bounded trial on comparable tasks such as an ingestion adapter, review UI enhancement or test-fixture generation. Compare accepted task cycle time, reviewer time, rework, escaped defects and tool costs against a documented baseline. Account for task complexity and learning effects. Do not extrapolate prototype speed to full production delivery or promise a productivity multiplier without evidence.

## 10. Human workflow and authority

The operator should see board/attempt identity, original images, overlays, predicted defects, initial disposition, reason codes, model/recipe version and review urgency. Confidence displays must explain their semantics. A failed or incomplete inspection needs an explicit status distinct from a verified acceptable board.

Quality owns defect definitions and authoritative labels. Authorized reviewers own permitted operational overrides. Manufacturing owns the physical response to REVIEW or unavailable inspection. Automation implements and tests the selected control contract. A human disposition arriving after the board has moved must be checked against current state; an audit record alone does not authorize late actuation.

For staffing, estimate review arrivals as production rate × review fraction and reviewer demand as arrivals × average handling time. Plan headroom for bursts, disagreement, absence and outages; average capacity alone does not establish queue deadlines. If review demand exceeds approved capacity, invoke the agreed fallback rather than lowering quality thresholds automatically.

## 11. Model operations and continuous improvement

Maintain three monitoring views: equipment/application health; statistical inspection quality; and business outcomes. Correlate line, camera, board variant, release and inspection IDs. Include image-quality failures, deadline misses, spool growth, synchronization lag, review age, command reconciliation, verified recalls/error rates and downstream escapes.

Drift signals such as brightness changes, embedding shifts or prediction-frequency changes trigger investigation. They do not prove quality loss or identify its cause. Confirm with representative verified labels, capture checks and comparisons against the deployed release. Show the age and coverage of ground truth so a dashboard does not imply real-time verified accuracy when labels arrive later.

Use a governed improvement sequence: alert or reported case → triage → confirmed cause → data/camera/rule/model change proposal → independent evaluation → approval → shadow execution → limited rollout → broader activation. Shadow candidates cannot issue physical commands and must not compromise active-model resource budgets.

Rollback triggers should include operational failure, incompatible behavior and statistically supported unacceptable degradation, with thresholds and responsibility agreed before rollout. Roll back a compatible package; then reconcile in-flight attempts and retained evidence. Online learning or automatic threshold relaxation on the active production model is not recommended for this scope.

## 12. Security, governance and responsible use

Preserve the architecture's OT/IT segmentation, authenticated services, backend authorization, secrets management, audit and recovery. NIST's OT guidance explicitly addresses the distinctive performance, reliability and safety requirements of systems interacting with the physical environment. It supports treating the factory control boundary as a separate design concern. [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final)

Add dataset lineage and label-change controls against accidental or malicious poisoning; verify model artifacts and dependencies; isolate training from production; and restrict who can approve and deploy packages. A checksum detects content changes against a trusted reference; use authenticated manifests or signatures where package authenticity is required. Define retention separately for operational evidence, datasets, models, audit and backups, including deletion propagation and holds.

For engineering AI, restrict code/data export to approved environments, remove secrets from context, limit tool permissions and treat repository text and retrieved content as untrusted inputs. Require normal review and CI gates before generated changes can affect production. Review provider data handling before exposing proprietary board imagery or engineering material.

If generative assistance is introduced, explicitly evaluate fabricated answers, information leakage, prompt injection through retrieved documents and misuse of tools. The NIST Generative AI Profile supplies supplementary risk-management guidance for generative capabilities; those concerns are additional to computer-vision model evaluation. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

Organize governance around accountable ownership, documented deployment context, measured acceptance and managed incidents/releases. This is an application of the AI RMF's Govern, Map, Measure and Manage functions; the framework and playbook are voluntary guidance, not evidence of compliance or product certification. [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook)

## 13. Optional quality investigation assistant

An optional assistant could answer “Why was this board rejected?”, retrieve supporting inspection evidence, or summarize defect trends. Its business value would be faster investigation and easier access to approved quality procedures. This feature is not required to satisfy the core inspection BRD.

Use backend-authorized, read-only evidence APIs and approved procedure documents. Compute counts and trends through validated queries; use the language model to explain returned results. Cite inspection IDs and procedure versions, show data freshness, and abstain when evidence is missing or contradictory. Retrieve only data the user can access; permission checks must apply before context reaches the model.

Keep model predictions distinct from confirmed defects and correlations distinct from root causes. Do not let generated explanations alter inspection outcomes, thresholds, deployed models or manufacturing settings. Any later write workflow requires a separately designed authorization and validation contract.

Evaluate correct record retrieval, grounded answer accuracy, citation correctness, cross-line access denial, injection resistance, abstention, response time and cost per completed investigation. Compare against existing dashboard/search workflows before adopting retrieval infrastructure or specialized agent orchestration. Assistant failure must leave ordinary evidence review available.

## 14. Capacity and economic analysis

All inputs below remain to be collected; these formulas are planning aids, not forecasts.

| Planning measure | Calculation and caveat |
| --- | --- |
| Image ingest per second | Boards/second × images/board × average encoded image bytes; add metadata and transfer overhead. |
| Local offline storage | Peak ingest bytes/second × supported offline seconds × approved capacity margin; include DB, pending uploads and recovery headroom. |
| Retained image storage | Boards/day × images/board × image bytes × retention days × retained fraction; add replicas, versions, backups and datasets separately. |
| Review work | Boards/hour × review fraction × mean review minutes / 60 = reviewer-hours per hour before headroom. |
| End-to-end timing | Capture + queueing + preprocessing + inference + QC + durable persistence + applicable control/acknowledgement; benchmark the real execution path. |
| Cost per inspected board | Allocated recurring operations, labeling, model maintenance and platform cost / unique boards inspected; report capital allocation separately. |

Establish a conventional-delivery baseline and an incremental AI Native case. Shared costs include cameras, lighting, edge compute, integration and core software. Incremental costs include dataset operations, evaluation automation, AI engineering tools, training, review overhead and optional assistance. Avoid counting common infrastructure as a new AI Native expense twice.

Estimate annual net benefit as avoided verified escape/rework/scrap costs plus realizable inspection/investigation savings, minus incremental annual operating cost. Payback is incremental investment divided by positive annual net benefit. Use low/base/high scenarios and Finance-approved assumptions. Time released is not automatically cash saved; throughput improvement has value only where a constraint and usable demand exist. Keep overlapping scrap, rework and escape savings from being counted twice.

## 15. Delivery roadmap and gates

The sequence below is dependency-based. Duration and budget should be estimated after data availability, equipment access and staffing are established.

| Phase | Work and outputs | Exit gate | Main gaps |
| --- | --- | --- | --- |
| A: Discovery and baseline | Observe production; confirm scope, taxonomy, targets, interfaces, fallback and data rights | Accountable decisions and baseline report; unresolved assumptions visible | G01–G04, G06–G07, G11, G15–G18 |
| B: Feasibility and foundations | Camera trial; representative labels; simple model comparisons; contracts; engineering context pack; CI skeleton | Evidence supports a bounded inspection scope and hardware approach | G03–G05, G09, G13–G14 |
| C: Integrated vertical slice | One supported board path from capture through durable result, review and sync; selected control simulation | Functional, access and recovery tests pass; independent model evidence available | G06–G07, G10–G11, G14–G16 |
| D: Shadow and controlled pilot | Real-line shadow comparison; verified PASS sampling; reviewer training; deployment/rollback drills | AC-001–AC-008 accepted for pilot scope; live actuation additionally passes hardware acceptance | All applicable P0; G08, G12 |
| E: Governed scaling | Repeatable datasets/evaluation, quality monitoring, additional line validation and recovery exercises | Each new line/variant meets quality, capacity and operating gates | G08–G12, G17–G18 |
| F: Optional assistance | Grounded investigation prototype and measured user trial | Demonstrated value and access/answer-quality acceptance | G19; G20 stays excluded |

Useful preparation can proceed in parallel across the team: simulated contracts, data inventory, camera access planning and the engineering context pack. Live automation cannot bypass unresolved quality or fallback decisions. Security, evidence durability and tested fallback are pilot prerequisites; enterprise redundancy depth depends on the approved availability requirement.

### 15.1 Initial work packages

| Package | Deliverable | Depends on | Completion criterion |
| --- | --- | --- | --- |
| WP01 | Decision and baseline register | Production observation and stakeholder access | Each production-blocking question has an owner, evidence and decision status. |
| WP02 | Scope/taxonomy and annotation handbook | WP01 Quality input | Inspectors can consistently label representative and ambiguous cases. |
| WP03 | Acquisition feasibility and data inventory | Camera/line access, WP02 | Visibility and coverage limitations are recorded and accepted. |
| WP04 | Versioned schemas and QC state machine | WP01–WP02 | Fixtures cover PASS/FAIL/REVIEW/unavailable and stale commands. |
| WP05 | Dataset and evaluation pipeline | WP02–WP03 | Frozen grouped test set and per-slice report can be reproduced. |
| WP06 | Durable inspection vertical slice | WP04; suitable model fixture, then WP05 candidate | Traceable attempt survives sync retry and selected fault cases. |
| WP07 | Approved release and rollback mechanism | WP05–WP06 | Unapproved/incompatible packages are rejected; rollback is demonstrated. |
| WP08 | AI-assisted engineering trial | Approved context/access policy | Accepted delivery benefit measured with review and defect costs included. |
| WP09 | Review/quality operations | WP01, WP05–WP07 | Staffing, sampled quality, escalation and fallback are rehearsed. |
| WP10 | Pilot acceptance bundle | WP01–WP07, WP09 | Every applicable AC has evidence and accountable acceptance. |

## 16. Ownership and operating model

Assign named individuals to these roles before pilot; several roles may be combined if approval separation is preserved.

| Decision or artifact | Accountable | Responsible contributors |
| --- | --- | --- |
| Scope, priority and business value | Product owner / sponsor | BA, Finance, Manufacturing, Quality |
| Defect taxonomy, ground truth and quality thresholds | Quality lead | Inspectors, Data, ML |
| Physical fallback and actuation enablement | Manufacturing lead | Automation, Quality, Operations |
| Dataset quality and provenance | Data lead | Annotators, Quality, ML |
| Model development and evaluation evidence | ML lead | Data, QA, Automation |
| Production model quality approval | Quality lead | Independent evaluator, ML, Manufacturing |
| Software contracts and AI-assisted development | Engineering lead | Software engineers, QA, Architect |
| Authorized release execution and recovery | Operations/release lead | Platform, ML, Automation |
| Security and data-access controls | Security lead | IT, Data governance, Engineering |
| Cost and benefit validation | Finance/business owner | Product, Manufacturing, Engineering |

Train engineers to verify generated changes, inspectors to handle uncertainty and label disagreements, ML staff to connect metrics to production outcomes, and operators to execute fallback and recovery. Incident triage must distinguish equipment, data, model, rule, integration and human-workflow causes so that retraining is not the default response to every anomaly.

## 17. Decision checklist and readiness conclusion

Before committing to live scope, resolve the BRD open questions in these groups:

| Decision group | BRD questions | Required outcome |
| --- | --- | --- |
| Quality and supported product scope | Q01–Q04, Q07–Q08, Q19–Q20, Q24 | Approved defect/variant scope, baseline, limits and change/revalidation policy. |
| Production and control | Q05–Q06, Q12–Q16, Q18, Q21 | Throughput/deadline, review authority, fallback, interfaces and availability. |
| Data and improvement | Q09–Q11, Q17, Q25 | Data inventory, verified-label ownership, retention and quality monitoring. |
| Investment | Q22–Q23 | Budget envelope, benefit assumptions and evidence-based funding gates. |

Additional engineering decisions concern dataset split rules, release compatibility, AI tool data access, evidence automation, monitoring ownership and support staffing. These are proposed design refinements; they must not be presented as BRD-approved requirements.

The documents support proceeding with discovery, feasibility and a controlled implementation foundation. They do not establish production readiness. The architecture already contains many of the correct controls; the main work is to make those controls executable, connect them to accepted evidence, and extend the engineering lifecycle with measured AI assistance and governed feedback.

The recommended target is a reliable industrial inspection system whose behavior is validated across code, data, model, hardware and human workflow. Adoption should be judged by quality, repeatability, delivery effectiveness and operating cost, not by the number of generative models, agents or new platforms introduced.

## Appendix A. Source navigation

- [Business Requirements Document.docx](<Business Requirements Document.docx>): business objectives §§4–5; functional requirements §15; AI requirements §§16–19; operating constraints §§20–31; risks and economics §§33–39; acceptance §40; open questions §41; discovery/handover §§42–47.
- [Solution architecture.png](<Solution architecture.png>): factory OT and industrial inspection computer; DMZ; enterprise application; data platform; model governance; cross-cutting operations; end-to-end workflow.
- [Supporting architecture narrative](SOLUTION_ARCHITECTURE_MERMAID.md): runtime and review flows, enterprise controls, traceability and open decisions.
- [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook): voluntary governance framing used in section 12.
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final): OT-specific security context used in section 12; this report does not claim compliance.
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf): supplementary generative-AI risk context used in section 12.

External references checked 9 September 2026. Architecture recommendations, gap priorities, formulas and work packages are the assessment author's proposed application to this solution, unless explicitly attributed to S1–S3 or an external reference.
