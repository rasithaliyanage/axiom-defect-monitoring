# AI Native solution architecture: Model-Driven, Probabilistic, Adaptive, Human in the Loop

AI-Based Automated Board Defect Inspection System | Proposed architecture | 9 September 2026

Target visual structure: [ARCH DIAGRAM WITH EDGE.png](<ARCH DIAGRAM WITH EDGE.png>). This user-designated expected diagram takes precedence for architecture organization and component coverage. Business acceptance still requires the BRD decision process.

Based on [Business Requirements Document.docx](<Business Requirements Document.docx>), [Solution architecture.png](<Solution architecture.png>) and [AI_NATIVE_GAP_ANALYSIS.docx](AI_NATIVE_GAP_ANALYSIS.docx). The gap analysis supplies the proposed extensions; it does not convert BRD discovery questions into approved requirements.

This revision extends AI Native design from detection through hosting using four perspectives: **Model-Driven, Probabilistic, Adaptive, and Human in the Loop**. It contains five complementary Mermaid diagrams. Diagram 1 follows the expected ten-layer edge–enterprise architecture with QG-1 through QG-6; diagrams 2–4 expand decision, learning and engineering; diagram 5 defines adaptive hosting and operations. Standalone `.mmd` files with the same code are provided in `architecture/`. Predictive hosting and bounded operational adaptation are proposed extensions requested in this revision, not requirements already approved in the BRD.

## 1. Architecture interpretation

“Probabilistic” describes estimated visual defect evidence and explicit uncertainty. Model scores become probability estimates only where calibration has been validated for the relevant operating scope. The model need not use stochastic inference at runtime. A fixed model can produce repeatable outputs while its predictions remain uncertain.

The target combines probabilistic perception with deterministic, approved business policy, durable workflows and human authority. Uncertainty methods, calibration, out-of-distribution detection and multi-view aggregation are proposed capabilities subject to feasibility and latency evaluation. They are not guarantees that every unknown defect will be recognized.

The full lifecycle is organized around versioned models, uncertainty-aware decisions, evidence-driven adaptation and accountable human control. This includes visual inspection, data selection, review prioritization, engineering, deployment, capacity planning and incident response. Storage transactions, authorization, interlocks and command delivery remain deterministic foundations of the AI Native system; introducing uncertainty into those guarantees would undermine the solution.

Angular/TypeScript, Java/Spring Boot, Python/ONNX Runtime, PostgreSQL, RabbitMQ and NGINX remain viable implementation choices. Hosting evolves from manually managed machines to a model-aware platform with immutable runtime artifacts, declarative infrastructure, resource isolation, predictive capacity planning, controlled reconciliation and fleet release management. Managed VMs or an approved container platform can implement these capabilities. Platform selection, CPU/GPU capacity and model families remain benchmark and operational decisions; AI Native is an end-to-end operating architecture rather than a vendor label.

### 1.1 Four architecture perspectives

| Perspective | Architectural meaning | Detection through hosting |
| --- | --- | --- |
| Model-Driven | Learned models and executable domain/deployment specifications are first-class, independently versioned artifacts. Distinguish statistical models from deterministic policy specifications. | Vision and image-quality models; uncertainty-aware review ranking; demand and failure-risk models; package registry; resource profiles; deployment and acceptance contracts. |
| Probabilistic | Predictions carry validated score semantics, uncertainty and supported operating scope. Decisions consider error costs and confidence in evidence. | Defect estimates, ambiguity and abstention; evaluation confidence bounds; workload prediction intervals; capacity-exhaustion risk and operational abstention. |
| Adaptive | Feedback changes candidate data, models, routing and resource plans through bounded, observable loops. | Active sampling, governed retraining, approved package selection, predictive central scaling, constrained job scheduling and measured recovery. |
| Human in the Loop | People define goals and permissible actions, adjudicate ambiguity, approve consequential changes and can suspend automation. | Inspectors review boards; Quality verifies labels and models; engineers review generated changes; platform owners approve action envelopes and exceptional hosting changes. |

### 1.2 End-to-end application of the four perspectives

| Layer | Model-Driven | Probabilistic | Adaptive | Human in the Loop |
| --- | --- | --- | --- | --- |
| Acquisition | Versioned capture recipe and validated image-quality model | Blur, occlusion or unfamiliar-image signals | Request recapture only within an approved timing/attempt budget | Automation approves capture settings and camera changes. |
| Detection | Approved model selected for board/revision and required views | Per-defect scores, validated calibration and ambiguity | Select among pre-approved packages before an attempt; improve candidates offline | Quality approves supported scope and release evidence. |
| QC and review | Executable severity/tolerance policy plus optional validated review-ranking model | Abstain where acceptance evidence is insufficient | Reprioritize review within severity/deadline constraints; never relax quality to drain queues | Inspectors decide disputed cases; Manufacturing owns physical routing. |
| Data and learning | Versioned datasets, labels, experiments and sampling policy | Representativeness, label disagreement and statistical uncertainty | Combine targeted sampling with representative PASS audits; generate retraining candidates | Quality adjudicates labels and accepts evaluation. |
| Application and integration | Versioned schemas and workflow specifications; model-linked evidence | Distinguish predicted defects from confirmed outcomes | Bounded worker scaling and review workload recommendations | Owners approve schema, workflow and integration changes. |
| Engineering and evaluation | AI-assisted tasks grounded in approved context and executable contracts | Generated output is a hypothesis until verified | Feedback improves task context, test coverage and candidate implementation | Engineers and QA independently review outputs and evidence. |
| Delivery and hosting | Immutable package, infrastructure specification and demand/risk model | Forecast intervals and risk estimates accompany capacity proposals | Bounded central scaling, scheduling and authorized rollback with cooldowns | Platform owners approve envelopes; Quality approves model-affecting changes. |
| Operations and recovery | Versioned anomaly models, dependency maps and runbooks | Incident hypotheses include uncertainty and supporting telemetry | Low-risk pre-authorized runbooks; otherwise escalate; verify the result | Operators can stop adaptation, approve exceptions and restore known-good operation. |

These are target capabilities with acceptance gates. Learned image-quality, ranking or operational models must earn deployment through evidence; deterministic baseline checks and static capacity reserves remain available when models are absent, stale or unreliable.

### 1.3 Comparison with the expected diagram

| Expected visual element | Previous document | Change in this revision |
| --- | --- | --- |
| Ten numbered layers | Service-centric overview and separate hosting view | Enterprise diagram now follows layers 1–10 in the expected image. Hosting remains supporting detail under layer 9; engineering supports layer 8. |
| Edge capture inputs | Cameras and board identity | Add machine-state sensors and product/camera/time/line metadata; formalize QG-1. |
| On-site edge processing | Inference, QC and local persistence | Explicit preprocessing, optimized inference, local anomaly/OOD, QG-2, optional local decision and trusted evidence. |
| Shared context/reference | Supported recipe and pinned release | Explicit local spec/BOM/rule cache, central authoritative context store, context sync, last-known-good policy and QG-3. |
| AI model layer | Dedicated vision service | Explicit approved orchestration, dynamic selection and optional validated ensembles across edge/enterprise; specialized defect models and unknown/anomaly detection. |
| Probabilistic reasoning/risk | Confidence and aggregation | Separate evidence aggregation, calibration, aleatoric/epistemic uncertainty and severity/product/business risk assessment. |
| Decision quality and outcomes | PASS / FAIL / REVIEW | Introduce QG-4 and expected PASS / HOLD / REJECT vocabulary, mapped to BRD dispositions below. |
| Human review and label quality | Review plus verified labels | Explicit annotation tools, second-level review, QG-5, escalation and validated feedback. |
| MLOps and model evaluation | Independent evaluation and approved rollout | Explicit QG-6, golden dataset, regression/slice checks, champion/challenger and controlled fleet rollout. |
| Observability and governance | Broad operational/security controls | Match layers 9–10: monitoring, drift, incident management, dashboards, access, data protection, audit, model governance and compliance evidence. |
| Targets and outcomes | All numerical values TBD | Record the expected image's recall values as supplied design targets pending business confirmation and independent evaluation. |

### 1.4 Edge and enterprise execution semantics

The numbered layers are logical responsibilities, not a requirement for every board to make a network round trip. Layers 1–2 execute at the edge; layer 3 spans edge and enterprise. Layer 4 includes edge-deployed models and central orchestration/re-analysis. When local decisions are enabled, approved implementations of layers 5–6 execute locally against pinned, QG-3-validated context. Layer 7 and training in layer 8 normally execute centrally. Layers 9–10 cover both environments.

QG-1, QG-2 and QG-3 must pass before a valid local automatic disposition, and QG-4 is mandatory whether the decision runs locally or centrally. A central review or second opinion is a new linked decision; it cannot overwrite the original or actuate on a board that has already moved. If local decisions are disabled, the board follows an approved hold/manual workflow until a valid central disposition arrives. Offline continuation is permitted only with healthy equipment, durable capacity and a compatible unexpired approved model/context/policy package. A last-known-good cache is usable only under an explicit approved validity policy.

The image's arrow from edge processing to context is a presentation ordering. Context required for inference must be validated before inference; it is not supplied retrospectively. Similarly, the label quality gate governs training eligibility, not whether an authorized inspector may record a time-critical operational disposition.

### 1.5 Outcome vocabulary and six quality gates

| Expected image term | BRD / existing API mapping | Meaning |
| --- | --- | --- |
| PASS | PASS | Approved acceptance conditions met. |
| HOLD | REVIEW | Await review or exception resolution; physical hold/manual/stop action is separately approved. |
| REJECT | FAIL | Defect rejection under approved quality rules. |
| Gate rejection / quarantine | INVALID or UNAVAILABLE processing status, normally routed to HOLD | Invalid data does not prove that the board itself is defective. |

Existing API values may remain PASS/FAIL/REVIEW with this explicit UI/domain mapping; a storage/API rename requires schema migration. The diagrams use PASS/HOLD/REJECT as the expected presentation vocabulary.

| Gate | Inputs and checks | Failure behavior | Accountable owner |
| --- | --- | --- | --- |
| QG-1 Ingestion quality | Complete capture, focus/lighting/orientation, board/metadata, source health, timestamp and sequence | Quarantine or bounded re-capture; preserve attempt evidence | Automation / Data |
| QG-2 Edge processing quality | Preprocessing, approved model, inference health, deadline, no runtime error, output schema | Bounded re-process or HOLD/fallback | Edge engineering / Operations |
| QG-3 Context quality | Correct product/revision, spec version, complete component reference, line/machine context and cache validity | HOLD / exception; no silent incompatible fallback | Quality / Manufacturing |
| QG-4 Decision quality | Valid model evidence, applied product policy, required evidence and risk/authority checks | HOLD / human review; known policy-defined defects still REJECT | Quality |
| QG-5 Label quality | Reviewer agreement, critical-case review, completeness and annotation guidelines | Escalate; exclude from training until verified | Quality / Label adjudicator |
| QG-6 Evaluation quality | Independent per-defect recall/FN, calibration/localization, regression and relevant slice checks, golden dataset and hardware performance | Iterate and re-evaluate; no deployment | Quality / ML |

The expected image mentions fairness checks. For this industrial use case, evaluate uneven performance across relevant product revisions, lines, cameras and conditions; determine any additional fairness obligations from the actual data and deployment context. Unknown/anomaly detection is a capability to validate, not a guarantee of discovering all unseen defects.

Legend: solid arrows show runtime requests, evidence or workflow transitions; dashed arrows show configuration, deployment, monitoring or supporting evidence. Purple nodes represent probabilistic processing or model lifecycle; orange nodes represent approved policy and human gates; red nodes represent exception handling; green nodes represent durable data. Arrows across the DMZ show logical payload direction, not permission for unsolicited inbound OT connections.

## 2. Enterprise architecture

```mermaid
flowchart TB
    subgraph EDGE["EDGE - factory / on-premises: low latency and operational continuity"]
        subgraph L1["1. DATA CAPTURE AND INGESTION LAYER - Edge"]
            Source["Manufacturing line<br/>Cameras, board ID / scanner / PLC<br/>Sensors and capture metadata"]
            QG1{"QG-1 Ingestion Quality<br/>Complete image; focus, lighting, orientation<br/>Board metadata, source health, time and sequence valid?"}
            CaptureFailure["Quarantine or bounded re-capture<br/>Preserve failure reason and attempt lineage"]
            Source --> QG1
            QG1 -->|"Fail"| CaptureFailure
        end
        subgraph L2["2. EDGE AI PROCESSING LAYER - On-site"]
            Preprocess["Edge preprocessing<br/>Denoise, normalize, align / crop and ROI extraction"]
            EdgeInfer["Optimized edge AI inference<br/>Approved runtime: ONNX Runtime / TensorRT candidate<br/>Defects, local anomaly / OOD and scores"]
            QG2{"QG-2 Edge Quality<br/>Preprocessing, model version, inference health<br/>Deadline and output schema valid?"}
            EdgeFailure["Hold / bounded re-process<br/>Unavailable inspection invokes approved fallback"]
            Trusted[("Trusted evidence - durable local spool and DB<br/>Raw / processed images, results and metadata<br/>Pinned release, context and outbox")]
            EdgeDecision["Optional local decision execution<br/>Approved local layers 5 and 6 including QG-4<br/>Require QG-1 / QG-2 / QG-3; PASS / HOLD / REJECT"]
            EdgeAction["Persist disposition before line action<br/>Command ID, expiry, board-state fence<br/>Optional PLC acknowledgement and reconciliation"]
            QG1 -->|"Pass"| Preprocess
            Preprocess --> EdgeInfer --> QG2
            QG2 -->|"Fail"| EdgeFailure
            QG2 -->|"Pass"| Trusted
            EdgeDecision -->|"Commit decision and pending action"| Trusted
            Trusted -->|"Committed authorized actions only"| EdgeAction
        end
        subgraph L3["3. CONTEXT AND REFERENCE LAYER - Edge + Enterprise"]
            Cache[("Local critical-context cache<br/>Board specs, BOM / component library<br/>Inspection rules and versioned last-known-good context")]
            ContextSync["Context synchronization<br/>Version, checksum, expiry and compatibility checks<br/>Explicit permitted fallback policy"]
            QG3{"QG-3 Context Quality<br/>Product / revision and spec version valid?<br/>Component reference and line / machine context complete?"}
            ContextFailure["Hold / exception<br/>No silent use of incompatible or expired context"]
            Cache --> QG3
            ContextSync --> Cache
            QG3 -->|"Fail"| ContextFailure
            QG3 -->|"Pass: pinned context"| EdgeInfer
        end
    end

    subgraph BOUNDARY["EDGE - ENTERPRISE SECURE SYNCHRONIZATION"]
        Sync["Factory-initiated gateway / DMZ<br/>Authenticated encrypted uploads and polling<br/>Evidence, context, models, policies, configuration and logs<br/>Retry, deduplication, checksums and bounded buffering"]
    end

    subgraph ENTERPRISE["ENTERPRISE - central platform: governance, learning, optimization and fleet management"]
        CentralContext[("Central context store - Layer 3<br/>Authoritative product specs, component library / variants<br/>Manufacturing line, machine and process context<br/>Traceable revisions and approval")]
        subgraph L4["4. AI MODEL LAYER - Enterprise + Edge deployment"]
            Orchestrate["Model orchestration<br/>Approved routing / selection by product and scope<br/>Optional validated ensemble; edge / central placement"]
            Pipeline["Vision AI pipeline<br/>Image understanding, defect detection, classification<br/>Component / area localization and prediction scores"]
            Specialists["Specialized models<br/>Missing / wrong / misaligned component<br/>Solder bridge, damaged component, scratch<br/>Unknown / anomaly detection"]
            ModelResult["Versioned model evidence<br/>Class, location, raw score and supported scope<br/>Central re-analysis is separate from initial edge result"]
            Orchestrate --> Pipeline --> ModelResult
            Specialists -.-> Pipeline
        end
        subgraph L5["5. PROBABILISTIC REASONING AND RISK LAYER"]
            Aggregate["Evidence aggregation<br/>Model outputs, image quality, product context<br/>Historical evidence with provenance; correlated views"]
            Calibrate["Probability calibration<br/>Validated temperature scaling / Platt / isotonic candidate<br/>No assumption that raw scores are probabilities"]
            Uncertainty["Uncertainty quantification<br/>Aleatoric and epistemic estimates where validated<br/>Ambiguity, unfamiliar inputs and abstention"]
            Risk["Risk assessment<br/>Defect severity, product criticality and business impact<br/>Versioned validated risk / loss policy"]
            ModelResult --> Aggregate --> Calibrate --> Uncertainty --> Risk
        end
        subgraph L6["6. DECISION LAYER - AI evidence + business rules"]
            Decision["Decision engine<br/>Product-specific policies, rules and approved thresholds"]
            QG4{"QG-4 Decision Quality<br/>Model evidence valid; risk within policy bounds?<br/>Required context present; policy applied; action authorized?"}
            DecisionOutput["PASS: continue under approved policy<br/>HOLD: review / approved hold procedure<br/>REJECT: confirmed defect under approved rules"]
            DecisionRecord[("Decision record<br/>Initial and subsequent outcomes, reasoning and versions<br/>Evidence, context, audit and action applicability")]
            DecisionHold["Gate failure: HOLD / human review<br/>Invalid evidence is not proof of a defective board"]
            Risk --> Decision --> QG4
            QG4 -->|"Pass"| DecisionOutput --> DecisionRecord
            QG4 -->|"Fail"| DecisionHold --> DecisionRecord
        end
        subgraph L7["7. HUMAN-IN-THE-LOOP LAYER"]
            Review["Review queue<br/>Uncertain, high-risk and unknown cases<br/>Severity / deadline-aware assignment"]
            Annotation["Annotation tools and reviewer workflow<br/>Original evidence, boxes / component IDs<br/>Second-level checks, reasons and override authority"]
            QG5{"QG-5 Label Quality<br/>Reviewer agreement and critical-case review?<br/>Complete labels; annotation guidelines satisfied?"}
            Feedback[("Validated feedback<br/>Verified labels, comments and adjudication<br/>Final disposition stored separately from training eligibility")]
            Escalate["Escalate label disagreement / incomplete review"]
            DecisionHold --> Review
            DecisionOutput -->|"HOLD or authorized dispute"| Review
            Review --> Annotation --> QG5
            QG5 -->|"Pass"| Feedback
            QG5 -->|"Fail"| Escalate
            Annotation -->|"Authorized operational decision, independent of label approval"| DecisionRecord
        end
        subgraph L8["8. MODEL LIFECYCLE AND MLOPS LAYER"]
            Data["Training data management<br/>Representative PASS audits + targeted sampling<br/>Curation, versioning, grouped splits and leakage control"]
            Train["Model training and experimentation<br/>Reproducible runs, validation and calibration"]
            QG6{"QG-6 Evaluation Quality<br/>Independent per-defect recall / FN tests<br/>Calibration, localization, regression and slice checks<br/>Golden dataset and target-hardware performance?"}
            Approval["Quality release approval<br/>Scope, evidence, compatible runtime / context<br/>Risk acceptance and rollback plan"]
            Registry[("Model registry<br/>Approved models, metadata and calibration<br/>Context compatibility and immutable package manifest")]
            Deploy["Controlled deployment<br/>Champion / challenger, observation-only shadow<br/>Staging, fleet activation and rollback"]
            Data --> Train --> QG6
            QG6 -->|"Fail: iterate; preserve test independence"| Train
            QG6 -->|"Pass"| Approval --> Registry --> Deploy
            Feedback --> Data
        end
        subgraph L9["9. OBSERVABILITY, MONITORING AND OPERATIONS LAYER"]
            Monitor["Real-time monitoring<br/>Throughput, latency, health and verified quality<br/>Label lag, sampling coverage and SLO / SLA evidence"]
            Drift["Drift and anomaly detection<br/>Image, data, performance and concept-drift signals"]
            Alerts["Alerts and notifications<br/>Threshold breaches, uncertainty and anomalies"]
            Incident["Incident management and operations dashboard<br/>Diagnose, mitigate, verify, escalate and rollback<br/>Adaptive hosting control loop: diagram 5"]
            Monitor --> Drift --> Alerts --> Incident
        end
        subgraph L10["10. GOVERNANCE, SECURITY AND COMPLIANCE LAYER - cross-cutting"]
            Access["Access control and data protection<br/>RBAC, least privilege, encryption, retention<br/>Anonymization where applicable and OT isolation"]
            Audit[("Audit and lineage<br/>Restricted immutable history and end-to-end traceability")]
            Govern["Model governance and compliance evidence<br/>Approval workflows, risk management<br/>Internal / external audit; applicable obligations to confirm"]
        end
    end

    Trusted -->|"Persisted evidence"| Sync
    Sync -->|"Authorized context response"| ContextSync
    Sync -->|"Poll context"| CentralContext
    Sync -->|"Uploaded evidence for central analysis"| Orchestrate
    CentralContext -->|"Versioned context"| Aggregate
    QG3 -->|"Required local context gate"| EdgeDecision
    QG2 -->|"Valid local model evidence"| EdgeDecision
    Orchestrate -.->|"Approved model assignments through release channel"| Deploy
    Deploy -->|"Approved edge packages via polling"| Sync
    Registry -.-> Specialists
    DecisionRecord -->|"Authorized disposition response via polling"| Sync
    Sync -->|"Local authority / expiry / board-state validation"| EdgeDecision
    Trusted -.->|"Local telemetry uploaded through gateway"| Sync
    Sync --> Monitor
    DecisionRecord --> Monitor
    Feedback -->|"Verified ground truth"| Monitor
    Incident -->|"Investigated improvement request"| Data
    Incident -->|"Authorized rollback request"| Deploy
    DecisionRecord --> Audit
    Deploy --> Audit
    Access -.-> Sync
    Access -.-> Review
    Govern -.-> Approval
    Govern -.-> CentralContext
    Govern -.-> Decision

    classDef ai fill:#eee6ff,stroke:#7954a1,color:#211a33;
    classDef gate fill:#fff0cc,stroke:#ad7600,color:#302400;
    classDef data fill:#e7f4e8,stroke:#39784a,color:#14321b;
    classDef risk fill:#ffe5e5,stroke:#b83e3e,color:#4a1515;
    class EdgeInfer,Orchestrate,Pipeline,Specialists,Aggregate,Calibrate,Uncertainty,Risk,Train ai;
    class QG1,QG2,QG3,QG4,QG5,QG6,Approval,Decision,EdgeDecision gate;
    class Trusted,Cache,CentralContext,DecisionRecord,Feedback,Registry,Audit data;
    class CaptureFailure,EdgeFailure,ContextFailure,DecisionHold,Escalate risk;
```

Operational interpretation: local inspection can continue during a central outage only while approved equipment, configuration, evidence capacity and the agreed local review/fallback procedure remain available. If the edge itself or its durable storage fails, the independent Manufacturing-approved procedure must work without relying on the failed application. No browser, assistant or training service connects directly to the PLC.

## 3. Probabilistic inference and controlled decision flow

This view defines the ordering of checks. It deliberately avoids a fixed confidence threshold. A confirmed critical-defect rule takes precedence over uncertainty elsewhere in an otherwise valid inspection, subject to Quality approval. Invalid/incomplete inspections follow the approved exception procedure and cannot silently become PASS.

```mermaid
flowchart TD
    Start["Board trigger<br/>Create attempt ID and correlate available board identity"]
    Pin["Pin approved compatible release<br/>Model, transforms, calibration, aggregation and QC recipe"]
    Ready{"QG-1 Ingestion Quality<br/>Source healthy, complete capture and metadata valid?"}
    ContextGate{"QG-3 Context Quality<br/>Pinned spec, BOM, rules and line context valid?"}
    Infer["Run versioned preprocessing and vision inference<br/>Return per-defect locations and raw scores"]
    Valid{"QG-2 Edge Quality<br/>Approved model, preprocessing and inference healthy?<br/>Valid output within deadline?"}
    Confidence["Apply validated score interpretation<br/>Calibrated estimates where supported<br/>Record model and calibration versions"]
    Uncertain["Assess validated ambiguity and novelty signals<br/>Image quality, model uncertainty and view disagreement"]
    Board["Aggregate evidence across required views<br/>Product context, correlated views and multiple defects"]
    RiskAssessment["Probabilistic risk assessment<br/>Validated uncertainty plus severity, product criticality<br/>and approved business-loss policy"]
    DecisionGate{"QG-4 Decision Quality<br/>Valid evidence, complete context and policy applied?"}
    Critical{"Approved critical-defect or<br/>mandatory rejection rule satisfied?"}
    Reject{"Other approved severity or<br/>tolerance rejection rule satisfied?"}
    Abstain{"Uncertain, unfamiliar, conflicting<br/>or insufficient acceptance evidence?"}
    Accept{"Complete inspection satisfies<br/>all approved acceptance conditions?"}
    Fail["REJECT - BRD FAIL<br/>Record rejected criteria and evidence"]
    Review["HOLD - BRD REVIEW<br/>Record abstention reasons and priority"]
    Pass["PASS<br/>Record acceptance evidence and coverage"]
    Invalid["UNAVAILABLE / INVALID processing status<br/>No automatic acceptance<br/>Approved manual / hold / stop procedure"]
    Persist["Persist original evidence, predictions and status<br/>Initial disposition, pinned release and audit<br/>Commit pending action in local outbox"]
    Durable{"Durable recording succeeded?"}
    Emergency["Independent operational fallback<br/>Storage or edge failure procedure<br/>Reconcile evidence when service is restored"]
    Action["Map disposition to approved physical action<br/>HOLD / REVIEW requires an approved physical procedure<br/>Validate board state, command ID and expiry"]
    Integrated{"Physical control integration selected?"}
    Dispatch["Dispatch command once logically<br/>Retries require idempotency and state reconciliation"]
    Ack{"Acknowledgement and observed state agree?"}
    Unknown["UNKNOWN delivery outcome<br/>Reconcile with controller and operator<br/>Never blindly repeat physical action"]
    Stored["Retain local evidence<br/>Upload through DMZ and verify central checksums"]
    Human["Authorized human review<br/>Original images, overlays, uncertainty and reason<br/>Staffed deadline and escalation"]
    Override["Append human decision with actor and reason<br/>Preserve original AI result and prior version"]
    Fence{"Disposition authorized, current<br/>and applicable to board location?"}
    Stale["Reject stale or conflicting action<br/>Retain audit and escalate"]
    Label["QG-5 Label Quality - verification and adjudication<br/>Agreement, completeness and critical-case checks<br/>Failed labels escalate; override alone is not ground truth"]

    Start --> Pin --> Ready
    Ready -->|"Yes"| ContextGate
    ContextGate -->|"Yes"| Infer
    ContextGate -->|"No"| Invalid
    Ready -->|"No"| Invalid
    Infer --> Valid
    Valid -->|"No"| Invalid
    Valid -->|"Yes"| Confidence
    Confidence --> Uncertain --> Board --> RiskAssessment --> DecisionGate
    DecisionGate -->|"Pass"| Critical
    DecisionGate -->|"Fail"| Review
    Critical -->|"Yes"| Fail
    Critical -->|"No"| Reject
    Reject -->|"Yes"| Fail
    Reject -->|"No"| Abstain
    Abstain -->|"Yes"| Review
    Abstain -->|"No"| Accept
    Accept -->|"Yes"| Pass
    Accept -->|"No"| Review
    Fail --> Persist
    Review --> Persist
    Pass --> Persist
    Invalid --> Persist
    Persist --> Durable
    Durable -->|"No"| Emergency
    Durable -->|"Yes"| Action
    Durable -->|"Yes: asynchronous sync"| Stored
    Action --> Integrated
    Integrated -->|"Yes"| Dispatch
    Integrated -->|"No: approved operator procedure"| Stored
    Dispatch --> Ack
    Ack -->|"Yes: persist acknowledgement"| Stored
    Ack -->|"No or timeout"| Unknown
    Unknown -->|"Approved escalation"| Emergency
    Stored -->|"Review required or authorized dispute"| Human
    Human -->|"Decision within workflow"| Override
    Human -->|"Overdue or service unavailable"| Emergency
    Override -->|"Return via factory polling"| Fence
    Fence -->|"Yes: append before dispatch"| Persist
    Fence -->|"No"| Stale
    Override -->|"Candidate annotation only"| Label

    classDef ai fill:#eee6ff,stroke:#7954a1,color:#211a33;
    classDef pass fill:#e7f4e8,stroke:#39784a,color:#14321b;
    classDef review fill:#fff0cc,stroke:#ad7600,color:#302400;
    classDef fail fill:#ffe5e5,stroke:#b83e3e,color:#4a1515;
    class Infer,Confidence,Uncertain,Board ai;
    class Pass,Stored pass;
    class Review,Human,Critical,Reject,Abstain,Accept,Fence review;
    class Fail,Invalid,Emergency,Unknown,Stale fail;
```

Decision semantics:

- Score calibration is assessed on held-out validation data and verified during independent acceptance. A defect detector score is not a board-level probability of acceptability.
- Multi-label defects need not form a mutually exclusive distribution. Do not force all defect probabilities to sum to one or multiply view-level probabilities under an unvalidated independence assumption.
- Risk assessment is explicit in the target architecture. A learned board-level probability requires its own ground truth, calibration and acceptance; a severity-weighted policy score must be identified as a score rather than a probability. Product-specific risk limits remain subject to Quality approval.
- Review routing considers uncertainty, supported scope and evidence completeness. Low scores or no detections alone do not establish PASS.
- Measure automatic-decision coverage and review load alongside false positives, false negatives and critical recall. Statistical confidence intervals on evaluation metrics are different from runtime prediction confidence.
- Processing status, quality disposition and physical command status are separate fields. This prevents unavailable inference or unknown command delivery from masquerading as a valid quality result.
- A processed human command is deduplicated and does not re-open the same review or reissue an action through the diagram's persistence loop.

## 4. Governed data, learning and release architecture

Training/validation and acceptance partitions are separated before experimentation. Candidate shadow execution is authorized for observation only. Quality acceptance and production activation remain explicit gates.

```mermaid
flowchart TB
    Evidence[("Authorized production evidence<br/>PASS / FAIL / REVIEW and unavailable cases<br/>Camera settings, release IDs and downstream outcomes")]
    Sampling["Representative sampling policy<br/>Random PASS audits plus targeted difficult cases<br/>Record selection probability and sampling scope"]
    Annotate["Quality-owned annotation<br/>Defect taxonomy, regions, severity and label policy"]
    Adjudicate{"QG-5 Label Quality<br/>Agreement, critical review, complete labels<br/>Guidelines and permitted reuse satisfied?"}
    Quarantine["Quarantine disputed, corrupt or restricted samples<br/>Resolve disagreement or exclude with reason"]
    Version[("Immutable dataset manifest<br/>Image hashes, label versions and lineage<br/>Board, batch, time and line grouping keys")]
    Split["Group-aware split and leakage validation<br/>Related views and repeated boards remain together"]
    Train[("Training partition")]
    Validate[("Validation partition<br/>Model selection, thresholds and calibration")]
    Holdout[("Frozen independent acceptance partition<br/>Representative real images and slice counts")]
    Experiment["Reproducible model experiments<br/>Code, data, environment and hardware recorded<br/>Architecture choice based on feasibility"]
    Tune["Tune model, calibration and aggregation<br/>Approved cost and quality tradeoffs<br/>No tuning against the final acceptance partition"]
    Candidate[("Candidate inspection package<br/>Compatible model, runtime, transforms, calibration<br/>Taxonomy, capture constraints and QC recipe")]
    Test["Independent evaluation evidence<br/>Per-defect and board errors with uncertainty bounds<br/>Calibration, robustness, review rate and coverage<br/>Target-hardware end-to-end load and fault results"]
    Gate{"QG-6 Evaluation Quality<br/>Independent recall / FN, calibration / localization<br/>Golden dataset, regression, slices and hardware accepted?"}
    Rework["Investigate failure and revise candidate or scope<br/>Refresh acceptance set when tuning contaminated it"]
    ShadowPermit["Authorize observation-only shadow trial<br/>Resource budget and isolated command path"]
    Shadow["Shadow on intended line<br/>Active approved package remains authoritative<br/>Collect independent ground truth"]
    ShadowGate{"Shadow evidence and operational<br/>readiness accepted by Quality?"}
    Approve["Quality approval and authorized release decision<br/>Record scope, evidence, approvers and rollback triggers"]
    Registry[("Immutable approved registry<br/>Authenticated manifest and artifact hashes<br/>Previous approved compatible release retained")]
    Stage["Controlled staged activation<br/>Factory polls through DMZ<br/>Verify compatibility and activate between attempts"]
    Monitor["Monitor service, verified quality and outcomes<br/>Per-line and variant slices, sample counts and label lag<br/>Drift signals and review capacity"]
    Triage{"Investigated unacceptable behavior<br/>under approved incident criteria?"}
    Continue["Continue approved operation<br/>Expand only after rollout gate acceptance"]
    Rollback["Authorized rollback or approved fallback<br/>Compatible prior release; reconcile in-flight attempts"]
    Improvement["Governed improvement backlog<br/>Equipment, data, rules, model or workflow hypothesis"]
    Policy["Quality-owned acceptance contracts<br/>Limits and statistical method: TBD<br/>FR / AI / AC traceability"]
    Software["Reviewed software and integration evidence<br/>Security, schema, durability and recovery checks"]

    Evidence --> Sampling --> Annotate --> Adjudicate
    Adjudicate -->|"No"| Quarantine
    Quarantine -->|"Resolved and authorized"| Annotate
    Adjudicate -->|"Yes"| Version
    Version --> Split
    Split --> Train
    Split --> Validate
    Split --> Holdout
    Train --> Experiment
    Experiment --> Tune
    Validate --> Tune
    Tune --> Candidate
    Candidate --> Test
    Holdout --> Test
    Software --> Test
    Policy -.-> Tune
    Policy -.-> Test
    Test --> Gate
    Gate -->|"No"| Rework
    Rework --> Experiment
    Rework -->|"Additional representative evidence needed"| Sampling
    Gate -->|"Yes"| ShadowPermit
    ShadowPermit --> Shadow --> ShadowGate
    ShadowGate -->|"No"| Rework
    ShadowGate -->|"Yes"| Approve
    Approve --> Registry --> Stage --> Monitor --> Triage
    Triage -->|"No"| Continue
    Continue --> Monitor
    Triage -->|"Yes"| Rollback
    Triage -->|"Confirmed improvement need"| Improvement
    Improvement --> Sampling
    Improvement -->|"Model hypothesis"| Experiment
    Monitor -->|"Sampled evidence, not automatic labels"| Evidence

    classDef data fill:#e7f4e8,stroke:#39784a,color:#14321b;
    classDef ai fill:#eee6ff,stroke:#7954a1,color:#211a33;
    classDef gate fill:#fff0cc,stroke:#ad7600,color:#302400;
    classDef risk fill:#ffe5e5,stroke:#b83e3e,color:#4a1515;
    class Evidence,Version,Train,Validate,Holdout,Candidate,Registry data;
    class Experiment,Tune,Test,Shadow ai;
    class Adjudicate,Gate,ShadowPermit,ShadowGate,Approve,Policy,Triage gate;
    class Quarantine,Rework,Rollback risk;
```

A drift alert is a reason to investigate, not proof that retraining is needed. Adaptation includes uncertainty-based sample acquisition, verified feedback, candidate retraining, calibrated threshold proposals and selection among pre-approved packages. Model selection occurs before an inspection attempt and cannot change the pinned package mid-attempt. Any camera, rule or model change follows the appropriate revalidation path. Production weights and acceptance thresholds are not modified by an unvalidated online feedback loop. Autonomous manufacturing-parameter modification remains outside the BRD scope.

The same lifecycle applies to learned hosting demand/risk models, using operational ground truth, time-separated evaluation, forecast calibration, shadow recommendations and Platform/Operations approval. Vision Quality approval and platform-model approval are distinct authorities. Hosting actions that alter inspection behavior or its validated hardware envelope also require Quality and Automation review.

## 5. AI Native engineering and optional assistance

AI assistance accelerates bounded engineering tasks. Existing review, reproducible builds and release authority remain. The optional runtime assistant has a separate, read-only evidence boundary.

```mermaid
flowchart LR
    subgraph DEV["DEVELOPMENT AND VALIDATION ENVIRONMENT"]
        Sources["Approved BRD decisions and architecture<br/>Schemas, fixtures, acceptance criteria, infrastructure and runbooks"]
        Context["Versioned engineering context pack<br/>Task scope, permitted tools and protected data policy"]
        Engineer["Engineer / BA / QA / ML practitioner<br/>Own task intent and expected behavior"]
        AI["AI engineering assistant<br/>Draft requirements, models, implementation, tests<br/>Infrastructure specifications and evidence summaries"]
        Sandbox["Scoped repository and test environment<br/>No production credentials or unrestricted data export"]
        Review["Human review of changes<br/>Independent expected results and threat analysis"]
        Git["Reviewed version-controlled change<br/>Code, configuration and context references"]
        CI["Reproducible CI and infrastructure evidence<br/>Build, scans, contracts, integration and deployment simulation<br/>Model evaluation and resource benchmarks when affected"]
        Gate{"Applicable acceptance evidence<br/>and release authorization complete?"}
        Release["Controlled artifact promotion<br/>Application release or governed model pipeline"]
        Metrics["Engineering outcome measures<br/>Accepted cycle time, review effort, rework<br/>Escaped defects and tool cost"]
        Sources --> Context
        Engineer --> Context
        Context --> AI
        AI --> Sandbox
        Sandbox --> Review
        Review -->|"Revision needed"| AI
        Review -->|"Accepted"| Git
        Git --> CI --> Gate
        Gate -->|"No: remediate"| Review
        Gate -->|"Yes"| Release
        Review --> Metrics
        CI --> Metrics
    end

    subgraph SUPPORT["OPTIONAL READ-ONLY QUALITY ASSISTANCE - enterprise IT"]
        User["Authenticated operator or quality analyst"]
        Auth["Backend user, role and line authorization"]
        Orchestrator["Bounded investigation assistant<br/>Question interpretation and approved read tools"]
        Tools["Permission-enforcing evidence and reporting APIs<br/>Validated queries calculate counts and trends"]
        Documents["Permission-filtered approved procedures<br/>Document identity, revision and freshness"]
        Model["Language model using authorized retrieved evidence<br/>Retrieved text treated as untrusted input"]
        Check["Answer and citation checks<br/>Evidence IDs, grounding and sensitive-data controls"]
        Answer["Evidence-linked explanation or explicit abstention<br/>User verifies operational relevance"]
        Evaluate["Assistant evaluation and monitoring<br/>Correct retrieval, access denial, grounding<br/>Injection resistance, latency and cost"]
        User --> Auth --> Orchestrator
        Orchestrator --> Tools
        Orchestrator --> Documents
        Tools --> Model
        Documents --> Model
        Model --> Check --> Answer
        Answer --> User
        Check -.-> Evaluate
    end

    Authority["Authority boundary<br/>Assistant output cannot override inspections,<br/>approve packages, change QC rules or command PLCs"]
    Release -->|"Authorized deployment process only"| Authority
    Answer -.->|"Advisory output only"| Authority

    classDef ai fill:#eee6ff,stroke:#7954a1,color:#211a33;
    classDef gate fill:#fff0cc,stroke:#ad7600,color:#302400;
    classDef optional fill:#f4f4f4,stroke:#777777,color:#333333,stroke-dasharray:5 5;
    class AI,Model ai;
    class Engineer,Review,Gate,Auth,Authority gate;
    class Orchestrator,Tools,Documents,Check,Answer,Evaluate optional;
```

The authority node is a constraint annotation, not a deployed service. Engineering releases follow the application or model approval process in diagrams 1 and 3 and the hosting process in diagram 5; the optional assistant cannot invoke that process. Ordinary evidence review remains available if generative assistance fails.

## 6. Inspection package and evidence contracts

| Contract | Minimum content |
| --- | --- |
| Approved package | Release ID; model hash; runtime/hardware compatibility; preprocessing/postprocessing; calibration and aggregation versions where used; taxonomy; QC recipe; capture constraints; supported board/revision/view matrix; schema compatibility; evaluation references; approval; rollback reference. |
| Inspection attempt | QG-1 through QG-4 outcomes and reasons; pinned specification/BOM/context versions; orchestration/routing decision; unique attempt ID; board identity where available; reinspection parent; line/batch/variant; timestamps; required and received views; image hashes; pinned package; raw predictions; calibrated estimates where supported; uncertainty/coverage signals; processing status; initial disposition and reasons. |
| Human review | QG-5 status and adjudication evidence; actor/role; prior record version; original AI outcome; human disposition; reason; timestamp; command applicability; separate verified-label status. |
| Physical command | Stable command ID; attempt; approved action; expiry; expected board state; dispatch status; acknowledgement and reconciliation outcome. |
| Dataset and evaluation | QG-6 outcome and supplied-target approval status; sample selection; image/label versions; provenance; grouped partitions; frozen test manifest; per-slice counts; metric definitions; statistical uncertainty; target-hardware results and acceptance evidence. |
| Hosting model | Model/version hash; telemetry schema; training period; independent time-separated evaluation; forecast horizon; interval coverage; validated workload scope; approval and expiry/revalidation policy. |
| Hosting desired state | Runtime image and package hashes; hardware/driver compatibility; resource reservations; placement; replica limits; data locality; budget; network policy; health gates; approved fallback and rollback. |
| Adaptive action | Action ID; model/version; observed state and freshness; predicted impact/interval; policy version; pre-authorization or named approval; expiry; affected workloads; execution status; post-action evidence and rollback outcome. |

Persist images durably before committing references. Track partial uploads and confirm checksums before considering central evidence complete. Use transactional outboxes and idempotent consumers for at-least-once delivery. Message deduplication alone cannot guarantee exactly-once physical actuation.

## 7. Source and gap traceability

| Architecture element | BRD coverage | Gap analysis coverage |
| --- | --- | --- |
| Capture, identity, supported scope and image validation | FR-001/002; sections 12, 18–21 | G02–G03, G07 |
| Probabilistic vision, localization and multi-defect evidence | FR-003/005/006/007/008; AI-001–AI-005 | G03–G06 |
| QC, abstention, review, override and fallback | FR-004/009/010; sections 23–24, 32; AC-007 | G06–G07, G11 |
| Durable evidence, integration, history and audit | FR-011/012; sections 25–29; AC-006 | G09, G14–G16 |
| Dataset lineage and independent evaluation | AI-001–AI-007; sections 17–19; AC-001–AC-003 | G04–G05, G08–G09 |
| Approved packages, shadow, staged release and rollback | AI-006/007; section 30; AC-008 | G09–G10 |
| Latency, offline operation, recovery and observability | Sections 21–23, 31; AC-004/005 | G07, G12, G16 |
| Verified feedback and quality monitoring | BO-08; sections 24, 30–31 | G08, G12, G17–G18 |
| AI-assisted engineering and executable acceptance | Proposed gap-analysis extension; supports AC-001–AC-008 | G13–G14, G17–G18 |
| Optional grounded investigation assistant | Separate enhancement beyond core FRs | G19; G20 authority exclusions retained |
| Business acceptance contracts | Sections 5, 13–17, 21–23, 39–41 | G01–G02, G06–G07, G18 |
| Model-aware hosting and predictive operations | User-requested extension supporting sections 21–23, 29–31; AC-004/005/008 | Extends G09–G10, G12–G18; operational-model acceptance is new design scope |

## 8. Decisions before production design approval

Quality must approve taxonomy, supported scope, metric definitions, per-defect limits, uncertainty/review policy, statistical acceptance and labeling authority. Manufacturing and Automation must approve throughput, the capture-to-action deadline, review/failure routing, equipment behavior and selected PLC/MES interfaces. Operations and Security must establish availability, offline duration, RTO/RPO, retention, network access and release permissions. Finance and Product must validate costs and benefits.

The six recall values supplied in the expected image are recorded in section 10; they remain unconfirmed acceptance targets. Other numerical thresholds remain TBD. Calibration, uncertainty and unfamiliar-input methods must demonstrate value against their compute and review costs. The hosting platform must implement model-aware deployment, declared resource profiles, operational prediction, bounded adaptation and human oversight. Its substrate may be managed VMs or a container platform selected through benchmarking and operational review. A runtime LLM, vector database or cloud-dependent inspection path is not required to meet the four perspectives.

Production acceptance must exercise representative defects and variants, peak load, missing views, model/camera failure, central disconnection, full local storage, duplicate events, lost PLC acknowledgements, concurrent reviews, stale commands, restored evidence and compatible rollback. A diagram describes intended controls; passing evidence establishes readiness.

## 9. AI Native hosting and adaptive operations — diagram 5

Hosting is an active part of the model lifecycle. Each inference package declares a tested runtime and resource envelope. Operational models forecast demand and capacity risk; a planner proposes changes against quality, availability and cost objectives. A deterministic policy gate and scoped reconciler execute only authorized actions. Platform owners retain approval, suspension and recovery authority.

```mermaid
flowchart TB
    subgraph MODEL["MODEL-DRIVEN — approved artifacts and executable specifications"]
        Registry[("Approved artifact registry<br/>Vision and operational models; runtime images<br/>Evaluation, signatures and compatibility manifests")]
        Spec[("Versioned infrastructure and serving specifications<br/>Hardware profiles, reservations, quotas and placement<br/>Network policy, budgets and recovery procedures")]
        Owner["Platform / Operations owner<br/>Quality and Automation for inspection-impacting changes"]
        Envelope["Approved action envelope<br/>Permitted actions, scope, limits, cooldown and expiry"]
        Owner --> Envelope
        Registry --> Spec
    end

    subgraph PROB["PROBABILISTIC — operational evidence and forecasts"]
        Observe["Observed telemetry<br/>Load, queues, latency, storage, health and deployment state"]
        Forecast["Validated demand and operational-risk models<br/>Prediction intervals, scope and freshness<br/>Model and telemetry versions recorded"]
        Reliable{"Evidence fresh, model supported<br/>and uncertainty within approved bounds?"}
        Baseline["Abstain from predictive action<br/>Use approved static reserve / baseline controller<br/>Escalate insufficient capacity"]
        Observe --> Forecast --> Reliable
        Reliable -->|"No"| Baseline
    end

    subgraph ADAPT["ADAPTIVE — propose, constrain, execute and verify"]
        Plan["Capacity / recovery proposal<br/>Expected effect, uncertainty, cost and affected workloads"]
        Gate{"Policy checks pass and action<br/>inside pre-authorized envelope?"}
        Human["Human plan review<br/>Inspect evidence; approve, revise or reject<br/>Quality review if model behavior is affected"]
        Execute["Scoped desired-state reconciler<br/>Action ID, expiry, least privilege and audit<br/>Recheck current state before execution"]
        Reject["Reject or defer action<br/>Retain current approved state<br/>Invoke approved operational fallback if needed"]
        Check{"Post-action health, capacity and<br/>inspection constraints satisfied?"}
        Recover["Authorized rollback / recovery procedure<br/>Compatible state, fenced execution and escalation"]
        Record[("Adaptive action ledger<br/>Proposal, approval, execution and outcome<br/>Model, policy and infrastructure versions")]
        Reliable -->|"Yes"| Plan --> Gate
        Envelope -.-> Gate
        Spec -.-> Gate
        Gate -->|"Yes"| Execute
        Gate -->|"No: outside scope or requires approval"| Human
        Human -->|"Approved and policy-valid"| Execute
        Human -->|"Rejected or expired"| Reject
        Execute --> Record
        Check -->|"Yes"| Record
        Check -->|"No"| Recover
        Recover --> Record
        Baseline -->|"Capacity exception"| Human
    end

    subgraph HOST["HOSTING DATA PLANE — isolated workload classes"]
        Central["Enterprise application and inference support<br/>Bounded replica scaling and worker concurrency<br/>Approved locality and availability domains"]
        Training["Training / evaluation / optional assistant pools<br/>Quota-controlled CPU / GPU scheduling<br/>Never consume reserved inspection capacity"]
        EdgeRelease["Edge fleet release channel through DMZ<br/>Factory polls verified manifests<br/>Maintenance window and attempt-boundary activation"]
        Edge["Reserved edge inspection runtime<br/>Pinned package and tested hardware profile<br/>Local spool, offline operation and known-good package"]
        Execute -->|"Authorized IT resource changes"| Central
        Execute -->|"Bounded job scheduling"| Training
        Execute -->|"Separately approved edge release"| EdgeRelease
        EdgeRelease --> Edge
        Central -->|"Observed result"| Check
        Training -->|"Observed result"| Check
        Edge -->|"Status through DMZ"| Check
        Central -.-> Observe
        Training -.-> Observe
        Edge -.->|"Buffered telemetry through DMZ"| Observe
    end

    Owner -->|"Suspend new adaptive actions"| Execute
    Record -->|"Outcome review and policy tuning proposals"| Owner
    Record -->|"Verified examples for offline model improvement"| Retrain
    Retrain["Operational model lifecycle<br/>Time-separated evaluation, forecast interval coverage<br/>Shadow recommendations and platform approval"]
    Retrain --> Registry
    Registry -.-> Forecast

    classDef ai fill:#eee6ff,stroke:#7954a1,color:#211a33;
    classDef gate fill:#fff0cc,stroke:#ad7600,color:#302400;
    classDef data fill:#e7f4e8,stroke:#39784a,color:#14321b;
    classDef service fill:#e8f1ff,stroke:#3267a8,color:#172b45;
    classDef risk fill:#ffe5e5,stroke:#b83e3e,color:#4a1515;
    class Forecast,Plan,Retrain ai;
    class Owner,Envelope,Reliable,Gate,Human,Check gate;
    class Registry,Spec,Record data;
    class Execute,Central,Training,EdgeRelease,Edge service;
    class Baseline,Reject,Recover risk;
```

### 9.1 Hosting topology and runtime guarantees

- **Edge inference:** maintain local hardware reservations, preloaded approved artifacts, warm-up checks and version-pinned attempts. Central autoscaling cannot rescue a board whose physical deadline is local. Edge resource or runtime changes require target-hardware revalidation and a permitted activation boundary.
- **Enterprise serving:** deploy application, ingestion and worker capacity across the approved failure domains. Adaptive scaling operates within quotas and availability constraints, with rate limits and cooldowns to prevent oscillation. Measured service load can drive a baseline controller when the forecast model abstains.
- **Training and evaluation:** isolate compute, storage access and credentials from production. Schedule optional or interruptible jobs against approved budgets. Shadow candidates must fit a reserved shadow budget and cannot issue production commands.
- **Artifacts and infrastructure:** promote immutable runtime images and authenticated model packages together with declarative specifications. Validate driver/runtime compatibility, resource headroom, schema migration and recovery. Containerization is an implementation option; infrastructure specifications and reproducible deployment are required capabilities.
- **Outages:** the operational prediction service and central platform controller are outside the local inspection critical path. If they fail, freeze predictive changes, retain the approved desired state and use the baseline capacity/fallback procedure. The human suspension control stops new adaptive actions and reconciles in-flight actions without terminating a board attempt arbitrarily.

### 9.2 Adaptation and human authority matrix

| Action | Permitted automatic behavior after policy approval | Human decision boundary |
| --- | --- | --- |
| Sampling and review ranking | Select uncertain cases within budget while retaining representative audits and severity/deadline constraints | Quality approves sampling policy, ranking behavior and label acceptance. |
| Model selection | Route a new attempt to an already approved compatible package for its supported board/revision | New model, new scope, threshold or recipe requires Quality approval and evaluation. |
| Central capacity | Scale eligible application/worker replicas within approved quotas, locality and availability limits | New topology, network exposure, expanded spend or stateful storage changes require platform approval. |
| Training scheduling | Schedule authorized jobs within isolated CPU/GPU and spend budgets | New dataset use, larger budgets or resource-class changes require accountable approval. |
| Edge deployment | Distribute an already approved release and activate at its authorized boundary | Runtime/hardware envelope changes and production activation require the designated release approvals. |
| Recovery | Run explicitly pre-authorized low-risk procedures with health checks and bounded retries | Uncertain cause, stateful failover, destructive action or changed inspection behavior escalates. |
| Model improvement | Create and evaluate candidates using authorized verified data | Neither the vision model nor the operational model approves its own promotion. |

Automatic behavior here describes the proposed production system under a previously approved policy. It does not grant unrestricted authority to engineering assistants. Resource adaptation never changes defect severity, skips required views or relaxes acceptance thresholds to meet cost or throughput goals.

### 9.3 Evidence required to call hosting AI Native

| Perspective | Required demonstration |
| --- | --- |
| Model-Driven | Reconstruct a deployment from artifact, model, policy and infrastructure versions; reject an incompatible model/runtime profile. |
| Probabilistic | Evaluate operational forecasts on independent time periods; report interval coverage and demand errors against a baseline; abstain on stale or unsupported telemetry. |
| Adaptive | Replay representative load changes; demonstrate constrained scaling, cooldowns, quota denial, outcome verification and recovery without inspection deadline degradation. |
| Human in the Loop | Demonstrate plan approval/rejection, audit, suspension, exception escalation and Quality approval for inspection-affecting changes. |

Hosting acceptance also measures false operational alarms, action failure rate, recovery time, cost per inspected board and controller-induced instability. Targets remain stakeholder decisions. This extends AI Native accountability through the hosting layer while preserving the physical and quality constraints of the manufacturing solution.


## 10. Supplied performance targets and business outcomes

The expected diagram labels the following minimum recall values as “from requirements.” They are now captured as user-supplied design targets from that image. The reviewed discovery BRD does not provide these numerical approvals, and no measured model performance is supplied. Quality must confirm definitions, applicable variants and statistical acceptance before these become release gates.

| Defect type in expected image | Supplied minimum recall |
| --- | --- |
| Missing component | 99.5% |
| Wrong component | 99.0% |
| Misaligned component | 98.5% |
| Solder bridge | 99.5% |
| Damaged component | 98.0% |
| Scratch | 95.0% |

Define instance versus board-level denominators, localization matching, representative sampling, minimum counts and confidence-bound acceptance. False-positive limits, unknown-defect criteria, latency, throughput and review capacity remain open. Target recall is not runtime prediction confidence and must not be used as an inference threshold.

Track the expected outcomes: higher product quality, lower escape rate, reduced manual inspection effort, faster consistent decisions, traceable auditable evidence and continuous improvement. These are desired outcomes, not demonstrated benefits.

### 10.1 Supporting-view alignment and acceptance

Diagram 2 expands layers 1–6 and operational review with QG-1 through QG-5. Diagram 3 expands layers 7–8 with QG-5 and QG-6. Diagram 4 supports AI-assisted delivery of the ten layers, retaining optional read-only assistance. Diagram 5 expands layer 9 hosting and fleet operations under layer 10 governance. PostgreSQL, object storage, durable queues, DMZ and backup controls remain implementation responsibilities even where the expected overview groups them into broader layers.

In addition to existing fault tests, exercise every quality-gate failure, stale/wrong BOM or spec revision, disconnected context synchronization, permitted versus prohibited last-known-good use, disabled local decisions, bounded re-capture, specialist-model selection, correlated evidence, label disagreement, regression failures and central decisions arriving after board movement. Gate outcomes, context versions and model-routing choices must be reconstructable from the inspection record.
