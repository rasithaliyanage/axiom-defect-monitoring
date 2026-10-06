# Detection and review thresholds

- **Owner:** Quality
- **Status:** Awaiting business definition. No values recorded.
- **Source question:** BRD §16 "AI Requirements", §17 "AI Performance Metrics", §40 "Acceptance Criteria"

## What this file must eventually contain

Per defect category, the numeric boundaries at which system behaviour changes.

| Field | Awaiting |
|---|---|
| Minimum recall | Per defect category, with critical categories held to a higher bar |
| Acceptable false-negative rate | Per category — a defective board reported as acceptable |
| Acceptable false-positive rate | Per category — an acceptable board reported as defective |
| Review band | The confidence range that routes a result to human review |
| Inference latency budget | Maximum time per board, set by line speed |
| Measurement method | The dataset and protocol a threshold is measured against |

## Why nothing is filled in

BRD §17 states:

> "The actual numbers must be established through business/quality discussions."

BRD §5 lists every KPI baseline and target as TBD, and adds that values

> "should be established with manufacturing and quality stakeholders rather than assumed by the
> technology team."

## Note on the recall figures in the architecture diagram

The Enterprise AI-Native PCB Defect Inspection Architecture supplies per-defect minimum recall
figures. That panel is explicitly labelled **"Pending Quality confirmation — not measured results"**,
and the diagram as a whole is marked "Proposed design — validation required".

Those figures are therefore **supplied design targets awaiting confirmation**, not thresholds, not
measurements, and not acceptance criteria. They are deliberately not copied into this file, because
doing so would launder an unconfirmed proposal into an apparent business decision.

## Open questions

| Question | BRD reference |
|---|---|
| What level of false negative is acceptable? | Q19 |
| What level of false positive is acceptable? | Q20 |
| What is the current defect escape rate? | Q03 |
| What is the current false rejection rate? | Q04 |
| What happens when the AI result is uncertain? | Q12 |
| How long is available for inspection per board? | Q06 |
| Who validates the supplied recall targets, and against what dataset? | Architecture diagram |
