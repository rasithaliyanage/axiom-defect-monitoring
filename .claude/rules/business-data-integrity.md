# Rule: business data integrity

**Scope:** engineering-time guidance for Claude Code. Enforces nothing at runtime — see
[`README.md`](README.md).

**Authority:** `docs/business-problem.md` holds the business requirements (BR-3, BR-4 in
particular). `specs/model-contracts.md` defines the grounded context, what the model may reference
and the rejection codes for referencing anything else; `specs/spec.md` states the validation
requirements, VR-4 to VR-6 and VR-8 in particular. `policies/` is owned by Quality and
Manufacturing, not by engineering. This file restates none of them — it says how to behave when
touching data they govern.

## Why this rule is specific to board inspection

A wrong number in most applications is a bug. Here it is a number a line supervisor may act on —
hold a line, release a batch, escalate a defect trend. The cost of a fabricated figure is not a
failed test, it is a wrong manufacturing decision taken confidently.

So the standard is higher than "plausible". Every figure on screen must be traceable to a record
that produced it.

## Never invent a figure

Do not originate, estimate, interpolate, round, recompute or "fix up" any of these:

- inspection counts, queue depths, throughput
- defect counts, defect rates, defect ratios
- shift, line or period statistics
- pass yields or any rate derived from an outcome
- timestamps presented as capture or inspection times

If a figure is needed and no authoritative source exists, that is a finding to report, not a gap to
fill. Say what is missing and stop. A placeholder that looks like production data is worse than an
empty state, because nothing downstream can tell it apart.

**Synthetic data must be unmistakable.** The fixtures under `tests/fixtures/` are synthetic and
labelled as such. Keep new ones labelled, keep them out of any path that could be read as live, and
never relabel a synthetic figure as real to make a demonstration look better.

## Never invent a vocabulary

Defect categories, inspection capabilities, metric identifiers, actions and line identifiers are
owned outside engineering. An identifier that is not already in the grounded context, the fixtures
or `policies/` does not exist, and adding one here would convert an open business question into an
apparent decision.

The pattern already used for this in the code is worth repeating: `InspectionService.lines()` derives
the allowed `line` values from the data at load rather than declaring an enum, precisely so that this
repository never becomes a second source of truth for a list Manufacturing owns. Prefer deriving over
declaring whenever the value set belongs to the business.

## Never let generated text become a fact

When the AI Runtime exists, the model will choose wording and layout. It will not choose figures: it
names a metric identifier, and the Domain Runtime resolves the value. Gate 3 exists to make a
fabricated or drifted figure mechanically detectable by exact match.

Do not build anything that inverts this — no path where a number is read back out of generated prose,
no field where the model supplies both a label and its value, no logging of a model-stated figure as
if it were an observation. The rule that makes this checkable is in `specs/spec.md` VR-4: a
displayed value that does not match the context value exactly is a rejection, not a rounding.

## Never let the system decide quality

The application reports and highlights. It does not conclude.

Nothing in the UI, the API or a log line may state or imply that a board passes, fails, is approved,
rejected, conforming, safe to ship or certified. This is BR-3, and it is why `BoardRecordModel`
carries identity and capture metadata only — no `status`, `disposition`, `verdict`, `score` or
`defectRatio` field — with tests asserting that no such field and no verdict vocabulary appears in a
response.

Highlighting unusual activity is in scope. Deciding what the activity means is not. A qualified
person remains responsible, and the system's job is to get them there sooner with information they
can trust.

## Before touching the presentation layer

When a change involves a business figure, identify the authoritative source first, and say what it
is. If the answer is "the fixture", say that. If the answer is "nothing yet", the change is blocked
on a business input, and reporting that is the deliverable.
