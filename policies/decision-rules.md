# Decision rules

- **Owner:** Quality, with Manufacturing for anything affecting the line
- **Status:** Awaiting business confirmation. Candidate rules recorded, no thresholds attached.
- **Source question:** BRD §32 "Business Rules", §23 "AI Failure / System Failure", §24 "Human-in-the-Loop"

## What this file must eventually contain

What the system must do once a result exists — the mapping from an inspection outcome to an action
on a board, and who is permitted to change it.

## Candidate rules from the BRD, awaiting confirmation

BRD §32 lists these and states: *"these should be confirmed with the Quality/Manufacturing teams."*
They are reproduced as **candidates**, not as approved policy.

| ID | Candidate rule | Confirmed? |
|---|---|---|
| BR-001 | A board containing a critical defect shall not be automatically classified as acceptable | Awaiting |
| BR-002 | Low-confidence predictions shall be routed for human review where required | Awaiting |
| BR-003 | Human overrides shall be recorded | Awaiting |
| BR-004 | Only approved AI models shall be used for production inspection | Awaiting |
| BR-005 | Inspection results shall be associated with the relevant board identifier where available | Awaiting |

BR-002 cannot be implemented until `thresholds.md` defines the review band.

## Undecided, and consequential

| Question | Owner | BRD reference |
|---|---|---|
| What happens when the inspection system is unavailable — continue manually, hold boards, or stop production? | Manufacturing | §23, Q13 |
| Who may override an AI result, and under what authority? | Quality | Q18 |
| Which results require review, by whom, and within what time? | Quality | §24 |
| Does the line require an immediate acceptable/defective signal? | Automation | Q14 |
| Should human corrections become training data? | Quality / Data | §24 |

The first of these is a production-stoppage decision. It is not an engineering default.

## Boundary note

No rule in this file is enforced by any code today. The current phase renders a landing page and
takes no action on any board. When enforcement arrives it belongs in the Domain Runtime, never in the
model and never in the renderer — see the non-negotiable rules in `CLAUDE.md`.
