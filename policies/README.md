# Policies — business-owned, not engineering-owned

Everything in this directory is owned by the **Quality** and **Manufacturing** teams. Engineering
maintains the file structure; it does not decide the contents.

## Why this is a separate directory

Defect definitions, severities and thresholds are business decisions with quality and safety
consequences. Keeping them in their own versioned location means changing a threshold is a
reviewable business action with a named approver, rather than a code edit buried in a commit.

## The rule that matters

**No file here may contain an invented value.**

The Business Requirements Document is a discovery document. Its defect taxonomy is marked "examples
only — the manufacturing/quality team must define the actual taxonomy", and every KPI target is TBD.
Where a value is not yet decided, the file records the open question and the owning team. It does
not record a plausible default.

A reasonable-looking invented threshold is worse than an obviously empty one, because nobody
downstream can tell it was invented.

**Review test:** does any file in this directory contain a number that is not a BRD identifier or a
date? If so, it was invented and is the first thing to remove.

## Contents

| File | Owner | Answers |
|---|---|---|
| `defect-taxonomy.md` | Quality | What counts as a defect, and what is it called? |
| `thresholds.md` | Quality | At what confidence or recall does a decision change? |
| `decision-rules.md` | Quality | What must happen when a defect is found? |
| `ui-layout-policy.md` | Quality / Manufacturing | What may the generative UI compose, and for whom? |

## Status

All four are **placeholders awaiting business input**. No runtime code reads this directory yet. When
one does, the policy version must be pinned into the decision record so a past decision can be
replayed against the policy that was in force at the time.
