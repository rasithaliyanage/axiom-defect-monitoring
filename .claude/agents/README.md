# Agents

Specialised subagent instructions for engineering-time work.

**Status:** empty. No specialised agents are defined.

## The distinction that matters here

These are **engineering-time** agents — they help build the system. They are not the runtime AI
component that generates UI specifications.

| | Engineering-time agent | Runtime model |
|---|---|---|
| Defined in | this directory | `specs/model-contracts.md` |
| Acts on | the repository | a grounded context |
| Produces | code, tests, review findings | a UI specification |
| Constrained by | `CLAUDE.md` and these instructions | schema, registry, grounding and text policy |

Confusing the two is a meaningful error: a coding agent's latitude in the repository implies nothing
about how much latitude a runtime model should have over a production line.

## Candidates, none yet implemented

A contract reviewer that checks a change touched all four artefacts required by "Contract changes
are wide changes"; a policy auditor that flags invented values in `policies/`; an eval author for
`evals/cases/`.

Add one only when the task recurs often enough to justify it.
