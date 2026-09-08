# Solution Architecture - Mermaid Diagram

## AI-Native Manufacturing QC with Calibrated Probabilistic Decisions

```mermaid
graph TD
    subgraph DataSources["📊 Data Sources & Ingestion"]
        Camera["🎥 Production Line<br/>Cameras"]
        Sensors["📡 Sensor Data<br/>Temperature, Vibration"]
        Metadata["📋 Production<br/>Metadata"]
        History["📚 Historical<br/>Images & Labels"]
    end

    subgraph ModelLayer["🧠 Model Intelligence Layer"]
        PreProc["Data Preprocessing<br/>Resize, Normalize"]
        
        subgraph YOLOCore["YOLO v8 Supervised Detector"]
            Backbone["Backbone<br/>Feature Extraction"]
            Neck["Neck<br/>Multi-Scale Features"]
            Head["Detection Head<br/>Class + Box Predictions"]
        end
        
        ConfCalib["⚖️ Confidence Calibration<br/>Temperature Scaling<br/>Platt Scaling<br/>Isotonic Regression<br/>---<br/>⚠️ YOLO scores ≠ Business Prob<br/>Must validate before use"]
        
        Validation["📊 Score Validation<br/>Check if confidence<br/>meets business threshold<br/>Mark uncertainty regions"]
    end

    subgraph Decision["🔀 Probabilistic Decision Routing"]
        HighConf["✅ HIGH CONFIDENCE<br/>Defect Probability > 85%<br/>---<br/>Action: AUTO REJECT<br/>Confidence: Trusted"]
        
        LowConf["⚠️ LOW CONFIDENCE<br/>Defect Probability 50-85%<br/>---<br/>⚡ UNCERTAINTY ≠ FAILURE<br/>Action: HUMAN REVIEW<br/>or RE-IMAGE at 90°"]
        
        NoDefect["✓ NO DEFECT DETECTED<br/>Class Confidence < 50%<br/>---<br/>Action: AUTO PASS<br/>Note: Unseen defects<br/>structurally invisible"]
        
        FailThreshold["🛑 FAILURE THRESHOLD<br/>Multiple HIGH CONF defects<br/>within tolerance zone<br/>---<br/>Grade DOWN to QC Hold<br/>Do NOT ship<br/>Quality preserved"]
    end

    subgraph HumanLoop["👤 Human-in-Loop Learning<br/>(⚠️ Error Prone)"]
        HumanReview["Human Reviewer<br/>Validates Uncertain Cases"]
        
        CorrectLabel["✓ Correct Label"]
        WrongLabel["❌ WRONG LABEL<br/>⚠️ Risk: Model learns<br/>incorrect patterns<br/>→ Future false negatives<br/>→ Defects shipped"]
        
        Feedback["Label + Confidence<br/>+ Review Time"]
    end

    subgraph SecurityGov["🔐 Security & Governance Layer"]
        AccessCtrl["Access Control<br/>Role-Based Permissions"]
        AuditLog["Audit Logging<br/>All decisions & labels"]
        DataProt["Data Protection<br/>Encryption, Retention"]
        ModelVers["Model Versioning<br/>Approved versions only"]
        CompReview["Compliance Review<br/>Bias, fairness checks"]
    end

    subgraph ActiveLearn["🔄 Active Learning & Retraining"]
        SelectCases["Select high-impact<br/>uncertain cases"]
        Retrain["Fine-tune YOLO<br/>on new labels"]
        Validate_v2["Validate on holdout<br/>test set"]
        CompareMetrics["Compare: Accuracy<br/>Precision, Recall"]
    end

    subgraph Observability["📈 Observability & Drift Detection"]
        ModelMonitor["🔍 Model Performance<br/>Real-time accuracy metrics<br/>Precision, Recall drift<br/>Confusion matrix tracking"]
        
        DriftDetect["📊 Drift Detection<br/>Input distribution shift<br/>Covariate drift check<br/>Label shift detection<br/>---<br/>Trigger: Retrain when<br/>Accuracy drops > 5%"]
        
        PerfMetrics["⏱️ Performance Metrics<br/>Inference latency<br/>Throughput (boards/min)<br/>GPU utilization<br/>Model cache hits"]
        
        Alerts["🚨 Alerting<br/>Drift detected → Retrain<br/>Latency spike → Scale<br/>Accuracy drop → Review"]
    end

    subgraph Anomaly["❌ No Anomaly Detection<br/>Everything Routes Through<br/>Supervised Classifier"]
        AnomalyNote["⚠️ Limitation:<br/>Unseen defect types<br/>structurally invisible<br/>---<br/>Mitigation:<br/>Continuous re-labeling<br/>of human-reviewed cases"]
    end

    subgraph Output["📤 Applications & Outputs"]
        RealTimeUI["Real-time Inspection UI<br/>Bounding boxes<br/>Confidence heatmaps"]
        Alerts_Out["🔔 Alerts & Notifications<br/>Auto-reject summary<br/>QC hold escalations"]
        Reports["📊 Reports & Analytics<br/>Defect trends<br/>Pareto analysis<br/>OEE impact"]
        Traceability["🔗 Traceability<br/>Full decision history<br/>Label audit trail<br/>Model version used"]
    end

    subgraph QCSystem["🏭 Quality Control System"]
        QCDecision["QC Decision Engine<br/>Single point of truth<br/>for pass/fail/hold/grade"]
    end

    %% Connections
    Camera --> PreProc
    Sensors --> PreProc
    Metadata --> PreProc
    History --> Validation
    
    PreProc --> Backbone
    Backbone --> Neck
    Neck --> Head
    
    Head --> ConfCalib
    ConfCalib --> Validation
    
    Validation --> HighConf
    Validation --> LowConf
    Validation --> NoDefect
    
    HighConf --> FailThreshold
    LowConf --> HumanReview
    NoDefect --> FailThreshold
    
    FailThreshold --> QCDecision
    
    HumanReview --> CorrectLabel
    HumanReview --> WrongLabel
    
    CorrectLabel --> Feedback
    WrongLabel --> Feedback
    
    Feedback --> ActiveLearn
    QCDecision --> Observability
    
    ModelMonitor --> DriftDetect
    DriftDetect --> Alerts
    PerfMetrics --> Alerts
    
    Alerts --> Retrain
    Retrain --> Validate_v2
    Validate_v2 --> CompareMetrics
    CompareMetrics --> ModelVers
    
    HighConf --> RealTimeUI
    LowConf --> RealTimeUI
    QCDecision --> Alerts_Out
    QCDecision --> Reports
    QCDecision --> Traceability
    
    SecurityGov -.->|Protects| ModelLayer
    SecurityGov -.->|Governs| HumanLoop
    SecurityGov -.->|Audits| QCDecision
    SecurityGov -.->|Tracks| Feedback
    
    Anomaly -.->|Constraint| ModelLayer
    
    style ConfCalib fill:#fff3cd
    style LowConf fill:#e7d4f5
    style FailThreshold fill:#f8d7da
    style WrongLabel fill:#f8d7da
    style DriftDetect fill:#d1ecf1
    style Anomaly fill:#f8d7da
    style SecurityGov fill:#e2e3e5
```

## Key Architectural Principles

### 1. **Confidence Calibration is Critical**
- Raw YOLO scores are model confidence, not business probability
- Requires temperature scaling, Platt scaling, or isotonic regression
- Must be validated against labeled test sets before deployment
- Recalibrate when new defect types are introduced

### 2. **Uncertainty ≠ Failure**
- **High Confidence (>85%)**: Auto-reject with trust
- **Low Confidence (50-85%)**: Escalate to human or re-image
- **No Defect (<50%)**: Auto-pass (but note: unseen types invisible)
- Graceful degradation preserves quality

### 3. **No Anomaly Detection Branch**
- Everything is a supervised classification problem
- **Structural Limitation**: Unseen defect types are invisible
- **Mitigation**: Continuously re-label human-reviewed cases to expand training set
- Consider periodic manual "expert sweeps" to catch new defect patterns

### 4. **Quality Grading (Not Binary Fail)**
- Failure Threshold = multiple defects within tolerance
- Grade DOWN to QC Hold (preserve quality)
- Do NOT ship; do NOT fail entire production
- Balances cost vs. quality tradeoff

### 5. **Human Review Has Risk**
- Humans make labeling mistakes
- Wrong labels teach the model incorrect patterns
- **Risk**: Future false negatives (defects shipped)
- **Mitigation**: 
  - Double-blind review for uncertain cases
  - Random spot-check of human labels
  - Track reviewer accuracy over time
  - Flag reviewers with high error rates

### 6. **Security & Governance Across Layers**
- **Access Control**: Role-based permissions (inspectors, QC engineers, data scientists)
- **Audit Logging**: All model decisions, labels, and changes
- **Model Versioning**: Only approved versions deployed
- **Compliance**: Bias detection, fairness validation
- **Data Protection**: Encryption, retention policies

### 7. **Drift Detection is Essential**
- Monitor real-time accuracy metrics
- Detect input distribution shift (covariate drift)
- Detect label shift (defect rates changing)
- **Trigger**: Auto-retrain when accuracy drops >5%

### 8. **Performance Monitoring**
- Inference latency (must stay <100ms per board)
- Throughput (boards/min matching production speed)
- GPU utilization and model cache efficiency
- Alert on bottlenecks

### 9. **Continuous Feedback Loop**
- Collect human labels from review queue
- Use active learning to select high-impact cases
- Retrain on curated dataset
- Validate against holdout set before deployment
- Version control models (approved versions only)

## Deployment Checklist

✅ Confidence calibration validated on production-like data  
✅ Failure threshold set with business stakeholders  
✅ Human reviewer error rates measured & tracked  
✅ Security governance policies documented & enforced  
✅ Drift detection thresholds calibrated  
✅ Audit logging enabled for compliance  
✅ Fallback procedures for model failures  
✅ Feedback loop integrated into QC workflow  
✅ Performance baselines established  
✅ Regular anomaly/new defect type detection (manual sweeps)
