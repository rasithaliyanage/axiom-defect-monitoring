# Quality gates

There are **two** independently numbered gate sequences in this project. They are unrelated, and
conflating them is the most likely reading error in this document.

| | Sequence | Range | Applies to | Enforced where | Status |
|---|---|---|---|---|---|
| **A** | Validation pipeline gates | Gate 1–4 | A **UI specification** produced by the model | `services/domain/validator.py` | **Implemented** |
| **B** | Inspection quality gates | QG-1–QG-6 | A **board** moving through inspection | Nothing yet | **Not implemented** |

A "Gate 3 failure" is an ungrounded identifier in a UI specification. A "QG-3 failure" is missing
board context on a production line. They share nothing but a word.

---

## A. Validation pipeline gates — implemented

Applied in order to every model output before it can reach the renderer. Defined in
`docs/architecture.md`, enforced by the validator, and reported through the rejection codes in
`specs/model-contracts.md`.

| Gate | Checks | Representative rejection codes |
|---|---|---|
| **Gate 1** — structural | Parses as JSON and conforms to `specs/schemas/ui-spec.schema.json` | `E_SCHEMA`, `E_SIZE_LIMIT`, `E_DEPTH_LIMIT` |
| **Gate 2** — registry | Every component name is approved and every prop is approved for it | `E_UNKNOWN_COMPONENT`, `E_PROP_INVALID` |
| **Gate 3** — grounding | Every referenced metric, alert, defect category, capability and action exists in the grounded context, and copied values match exactly | `E_UNGROUNDED_METRIC`, `E_UNKNOWN_ACTION`, `E_UNKNOWN_DEFECT_CATEGORY`, `E_UNGROUNDED_CAPABILITY`, `E_CONTEXT_MISMATCH` |
| **Gate 4** — policy | Text carries no decision language, code-like content, markup or locations | `E_TEXT_POLICY`, `E_CODE_LIKE_CONTENT`, `E_DECISION_LANGUAGE` |

**Failure action:** the specification is rejected in full. All violations are reported, not just the
first. Per `CLAUDE.md`, failure permits one bounded repair attempt and then the deterministic
fallback specification — neither the repair path nor the fallback is built yet.

**Limitation, stated plainly:** Gate 4 is a set of deterministic patterns, not a semantic
guarantee. It cannot prove capability honesty or the absence of an implied verdict. Both false
positives and false negatives are possible. That is why `evals/` exists.

---

## B. Inspection quality gates — not implemented

From the Enterprise AI-Native PCB Defect Inspection Architecture, which is marked **"Proposed design
— validation required"**. Recorded here ahead of implementation so the sequence is visible; none of
it is built, and none of it is approved.

| Gate | Question |
|---|---|
| **QG-1** Input valid | Is the captured input complete and usable? |
| **QG-2** Inference reliable | Is the inference healthy and within its limits? |
| **QG-3** Context complete | Is the product and line context available? |
| **QG-4** Decision justified | Is the decision based on valid evidence and approved policy? |
| **QG-5** Labels verified | Are review labels high quality and complete? |
| **QG-6** Model ready | Is the model evaluated and approved for release? |

Failure handling in the proposed design: quarantine invalid evidence; bounded re-capture or
re-processing; HOLD for review; escalate for expert review; or an approved manual, hold or stop
fallback.

**Every parameter is undecided** — retry bounds, HOLD dwell time before escalation, and who may
authorise a production stop. See `policies/decision-rules.md` and `policies/thresholds.md`. A HOLD
resolved by timeout would convert a capacity problem into a quality escape, so the dwell-time
question is not a detail.

QG-1 through QG-4 depend on capabilities listed as out of scope in `CLAUDE.md` — camera integration,
edge processing, classification models. They arrive with those increments, not before.
