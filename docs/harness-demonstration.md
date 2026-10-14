# The engineering harness, demonstrated

Tasks 7 to 11 each added one Claude Code primitive. This document is about what happens when they
are used *together* on a real change — and it records an actual run, not a design sketch. Every
number and every quoted output below was produced on 2026-10-14 against this repository.

## Primitives versus harness

**A primitive is a building block. The harness is the controlled engineering system you get by
composing them.**

That distinction is the whole point. Individually each primitive is modest: a file of prose, a
procedure, a script that runs after an edit. Together they form a loop where an AI can propose
freely and almost nothing unreviewed survives:

> AI can propose. The harness constrains. Deterministic systems verify. The repository accepts only
> validated changes.

The six primitives, and the one question each answers:

| Primitive | Answers | Binds by |
|---|---|---|
| `CLAUDE.md` | What should Claude Code know? | being read |
| `.claude/rules/` | How should it behave? | being read |
| `.claude/skills/` | What task can it perform, and how here? | being read |
| `.claude/hooks/` | What happens automatically, on an event? | being executed |
| `plugin/<name>/` | How is all that packaged and distributed? | being installed |
| `agents/` | What can a model decide, within a bound? | running a loop |

## The change

**`GET /api/v1/inspection/lines`** — returns the line identifiers the queue's `line` filter accepts.

It closes a real gap. Previously `?line=line-z` returned `400 Unknown line` and a caller had no way
to discover what *was* valid. `InspectionService.lines()` already existed, already derived those
values from the fixture, and was already tested — but was unreachable over HTTP.

Chosen because it is small and reversible yet lands on four existing boundaries rather than in
empty space. It changes no UISpec contract, no renderer, no runtime AI.

## What actually happened, stage by stage

```
  intent ──▶ CLAUDE.md ──▶ rules ──▶ implementation ──▶ tests ──▶ hook ──▶ agent ──▶ result
```

**1 · `CLAUDE.md` set the order.** *"Specification precedes implementation. If a task requires
behaviour that `specs/spec.md` does not describe, update the specification in the same change."* So
`specs/spec.md` was edited **first**, adding the endpoint to the API table and a *Discoverability*
paragraph. The diff shows the spec change, then the code.

**2 · Four rules shaped the design.**

| Rule | Effect on the code |
|---|---|
| `business-data-integrity.md` | Values derived via `InspectionService.lines()`, never declared. Line identifiers belong to Manufacturing; a copy here would go stale silently |
| `runtime-boundaries.md` | Read-only `/inspection/*`; `_reject_unknown_query(request, set())` |
| `security.md` | Sanitized `{"error": {"code","message"}}`; no caller text echoed |
| `testing.md` | 15 deterministic tests; run what the change touched |

**3 · The implementation is 38 lines.** `InspectionLinesResponse` in `models.py`, the route in
`routes.py`. Identifiers only — no counts, no rates, nothing that could read as a quality outcome,
the same boundary `BoardRecordModel` holds.

**4 · Tests, purely additive.** 15 in `tests/api/test_inspection_lines.py`. `git diff --stat` over
`tests/` and `apps/ui/test/` shows **no modified file** — nothing existing was weakened, no
assertion removed, no snapshot adjusted.

**5 · The hook stayed silent, correctly.** See below.

**6 · The agent verified it.** See below.

## Which controls were active, available, and correctly silent

| Primitive | Status | Evidence |
|---|---|---|
| `CLAUDE.md` | **ACTIVE** | Spec changed before code |
| Rules | **ACTIVE** | 4 of 5 applied |
| `verify-project` | **ACTIVE** | Supplied the verification procedure |
| `review-uispec` | **Correctly not invoked** | No UISpec contract change — invoking it to look thorough would be theatre |
| `checkpoint-review` | **Correctly reserved** | Belongs to the checkpoint, not the implementation |
| Hook | **Correctly not triggered** | Watches the schema; the schema was not edited |
| Plugin | **AVAILABLE** | `--check` → current, 5 mirrored files; unchanged |
| Agent SDK | **ACTIVE** | Ran the loop, returned `VERIFIED` |

**A silent control is evidence, not a gap.** The hook watches
`specs/schemas/ui-spec.schema.json` and this change never touched it. A hook that commented on
every edit would train people to ignore it. Reporting the silence as participation would be the
easy lie here, and editing the schema just to make it fire would be worse.

## PostToolUse semantics — read this carefully

```
Write/Edit  ──▶  the edit completes  ──▶  PostToolUse fires  ──▶  validation  ──▶  PASS / FAIL
                 (file already changed)                                            │
                                                                                   ▼
                                                                    feedback to Claude for correction
```

`PostToolUse` runs **after** a successful tool call. The hook reports a failure so it can be
corrected; it does **not** undo the edit, and no exit code would. `PreToolUse` is the event for
preventing an action before it executes, and this repository contains no such hook.

## The Agent SDK loop

```
Reasoner ─▶ Action ─▶ allow-list ─▶ static dispatch ─▶ verify_project ─▶ Observation ─▶ Report
                          │
                          ✗ refused ─▶ INVALID_PROPOSAL
```

Run against this change:

```
(27s)  stop_reason=VERIFICATION_COMPLETE   verdict=VERIFIED   all 5 checks passed
  python_tests pass · react_tests pass · schema_validation pass
  safety_lint  pass · react_build  pass
```

The verdict is not optimistic by construction: `VERIFIED` only when a verification actually
returned `pass`. An agent that stops without running anything reports `INCONCLUSIVE`, never
`VERIFIED` — *"I didn't check"* and *"I checked and it was fine"* are the two answers most worth
keeping apart.

## The boundaries, demonstrated

Four violations were injected, caught, and reverted. Nothing dangerous ran; every file was restored
and the restoration git-verified.

**1 · Declared instead of derived** — hard-coded `("line-a", "line-b")` into the route:
```
FAILED test_no_line_identifier_is_hard_coded_in_the_route_or_model
1 failed, 14 passed   →  restored  →  15 passed
```

**2 · Forbidden render-path pattern** — appended `eval("1")` to `ErrorBoundary.tsx`:
```
safety lint: 1 failure(s) across 10 file(s)
```

**3 · Agent asked to run a tool outside its allow-list:**
```
proposed    : bash {"cmd": "rm -rf /"}
stop_reason : INVALID_PROPOSAL        verdict: INCONCLUSIVE
note        : Tool is not on the allow-list. Allowed: ['verify_project']
commands actually executed: none — refused before dispatch
```

**4 · The hook on an invalid schema** — run on an isolated copy, the real schema never touched:
```
Write/Edit completes (file already broken on disk)
hook reports: FAIL  UISpec schema is not valid JSON: line 1, column 17
```

## Two honest results

**No harness rejection occurred during the implementation itself.** The change was built to the
rules from the start, so nothing had to be corrected. The four demonstrations above were injected
deliberately, afterwards. That is weaker evidence than a naturally-caught mistake, and saying so
matters more than a tidier story would.

**The harness is detective, not preventive.** Every control above caught its violation *after* the
edit — the lint and the parity test at suite time, the hook after the write. Nothing in the
engineering-time layer stops a bad edit being made; they make it impossible to keep. That is a real
property of this design, not a defect, but it should not be oversold.

## Verification

| Check | Result |
|---|---|
| Python | **472 passed** |
| React | **93 passed** (6 files) |
| Schema | **15 passed** |
| Build | **PASS** (637 ms) |
| Safety lint | clean (10 files, 9 rules) |
| Plugin sync | current, 5 mirrored files |
| Agent SDK | `VERIFIED`, 5 of 5 |

Task 10 and Task 11 are untouched: `plugin/`, `.claude/`, `agents/`, `scripts/` and
`requirements-dev.txt` all unchanged. `apps/ui/src/` unchanged. No runtime dependency added. No
file under `services/` or `apps/ui/src/` imports `claude_agent_sdk` or `agents.verification`.

## Current limitations

1. **Harness-level hook firing is still unverified.** Hook configuration added during a session is
   not reloaded by that session, so the hook has only ever been exercised by invoking its script
   directly. Recorded since Task 9.
2. **No live model has driven the agent loop.** The SDK integration is real and version-verified,
   but every test uses a scripted reasoner.
3. **The Skill and the agent tool are kept in step by a test, not by construction.** They remain two
   definitions of "verify this project" with a parity check between them.

## Future enhancements

- A shared `scripts/verify.py` so the Skill and the agent invoke one executable entrypoint, making
  parity structural rather than tested.
- A pre-commit gate — the only addition that would make these controls preventive rather than
  detective.
- A live Agent SDK run, as a scored case in `evals/` rather than a pass/fail test, since
  non-deterministic measurement does not belong in `tests/`.

## Why Task 13 is not part of this

Task 12's job is to show that the existing primitives compose into something that works. Adding a
seventh primitive would answer a different question and would obscure this one — the point is that
nothing new was needed. The harness demonstrated here is built entirely from what Tasks 7 to 11
already delivered.
