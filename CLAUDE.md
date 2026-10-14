# Claude Code engineering instructions

This file governs how Claude Code works in this repository. It is not business documentation and not
a specification. Business requirements live in `docs/business-problem.md`, the system specification in
`specs/spec.md`, and the model contract in `specs/model-contracts.md`.

## Project identity

AI-Based Automated Board Defect Inspection System. Internal application. AI-native and model-driven:
the runtime user interface is produced by an AI model that emits a structured specification, which the
application validates and renders through a fixed component registry.

Current phase: Phase 0, engineering foundation. Two increments of application code exist — the
validation pipeline in `services/domain/` and the controlled renderer in `apps/ui/`. Nothing else
does: no model gateway, no API, no database, no fallback specification, no authentication.

Do not scaffold a build system, install dependencies, or create source files unless the task
explicitly asks for that increment.

## Non-negotiable rules

These rules are architectural, not stylistic. Do not relax them for convenience, and do not implement
a change that violates one — raise the conflict instead.

1. The model never produces executable content. No React, no HTML, no JavaScript, no CSS, no SQL, no
   shell. Model output is a UI specification conforming to `specs/schemas/ui-spec.schema.json` and
   nothing else.
2. The component registry is the only render path. A component that is not registered cannot appear on
   screen. Never introduce a dynamic render escape: no `eval`, no `new Function`, no
   `dangerouslySetInnerHTML`, no dynamic import driven by model output, no string-to-component lookup
   outside the registry.
3. Every model output passes validation before it reaches the renderer. Validation failure results in
   one bounded repair attempt and then the deterministic fallback specification. Never render
   unvalidated output, and never bypass validation with a debug flag that ships.
4. The model reads no data directly. It receives only the grounded context assembled by the Domain
   Runtime. It has no database connection, no image repository access, and no tool that executes
   commands.
5. The model makes no quality decisions. It must not state or imply that a board passes, fails, is
   approved, is rejected, is safe to ship, or is conforming. Pass and fail determinations belong to
   qualified humans and to systems outside this scope.
6. The model invents nothing. Defect categories, metrics, alerts, capabilities, and actions must come
   from identifiers present in the grounded context. An identifier not in the context is a validation
   failure, not a creative liberty.
7. No authentication subsystem. Internal application, network-level access control, this phase only.
   Do not add login pages, token issuance, session management, or user tables.

The seven above are the architectural constraints. How to act on them day to day is in
`.claude/rules/` — runtime boundaries, business data integrity, testing and security, one file each.
Those files are behavioural guidance and cite this one; where they disagree with it, this file wins.
Read `.claude/rules/README.md` first: it explains what a rule can and cannot bind.

## Engineering-time layers

Seven distinct things, easiest to keep straight by what each one answers:

| | Answers | Binds by |
|---|---|---|
| **This file** | What should Claude Code know about the project? | being read |
| **Rules** (`.claude/rules/`) | How should Claude Code behave? | being read |
| **Skills** (`.claude/skills/`) | What task can it perform, and how is it performed here? | being read |
| **Hooks** (`.claude/hooks/`) | What should happen automatically, on an event? | **being executed** |
| **Plugins** (`plugin/<name>/`) | How are those capabilities packaged and distributed? | being installed |
| **Specifications** (`specs/`, `docs/`) | What is the system required to do? | review |
| **Runtime code + tests** | What does the application actually enforce? | executing, and failing |

A rule governs behaviour, a skill performs a task and defers the behavioural question to the rule
that owns it, and a hook runs on its own whether or not anyone remembered. Hooks are the first of
these that is executed rather than read — but a hook is still engineering-time. A plugin is a
reusable, installable package of Claude Code capabilities: it changes distribution, not behaviour.
Only the last row is what the running application enforces for a user.

Three skills exist:

- `verify-project` — run the existing verification suites and report what actually happened.
- `review-uispec` — review a specification-contract change against the authoritative sources.
- `checkpoint-review` — review a proposed checkpoint and stop at the report.

`.claude/skills/README.md` says when to reach for each. Their instructions stay in their own files;
do not copy them here.

One hook exists: a `PostToolUse` check that re-validates `specs/schemas/ui-spec.schema.json`
whenever it is edited, reusing the existing validator rather than adding a second one. Because
`PostToolUse` runs after a successful tool call, it reports a failure back for correction; it does
not undo the edit. `.claude/hooks/README.md` covers what it does, what it refuses to do, and why
it is safe to run automatically.

One plugin exists, at `plugin/board-defect-inspection-engineering/`, packaging those three skills
and that hook for installation elsewhere. `plugin/` is a container directory; the plugin root is
the named directory inside it, which is where `.claude-plugin/plugin.json` lives.

**`.claude/` stays authoritative; the package is a generated mirror** produced by
`scripts/package_plugin.py`, with `tests/plugin/` asserting byte-identity so a divergent copy is a
failing test rather than something a reviewer must spot. Edit `.claude/`, never the package.
Its `README.md` has the packaging rationale and the portability limits.

## Repository layout

**This section is the authoritative repository layout.** Where it differs from
`Documents/Proposed Project Structure - Board Defect Inspection (AI-Native)-Vinod.pdf`, this file
wins; that document is a review draft with open decisions. The naming differences are deliberate and
mapped below, not drift. See `docs/adr/0001-repository-layout.md`.

Present today:

```
CLAUDE.md                    this file
README.md                    orientation and document map
docs/                        business requirements, architecture, quality gates, security
docs/adr/                    numbered architecture decision records
specs/                       system specification, model contract
specs/schemas/               the authoritative UI specification schema
policies/                    BUSINESS-OWNED placeholders — Quality and Manufacturing, not engineering
plans/                       implementation plan
tasks/                       task breakdown
apps/ui/                     UI Runtime — React, TypeScript, renderer, component registry
plugin/<name>/               GENERATED MIRROR — Claude Code plugin package; edit .claude/ instead
scripts/                     repository-level tooling, e.g. the plugin packaging script
services/domain/             Domain Runtime — validation pipeline today; board inspection API to come
simulators/capture/          harness — recorded inspection fixtures, so slices need no factory
tests/                       deterministic tests and shared fixtures
evals/                       AI evaluations and case sets
.claude/                     Claude Code configuration, rules, skills, hooks and agent instructions
```

Role mapping to the proposed structure, so the divergence is unambiguous:

| This repository | Proposed structure | Role |
|---|---|---|
| `apps/ui/` | `frontend/` | UI Runtime |
| `services/domain/` | `backend/` | Domain Runtime |
| `services/domain/ai/` | `ai/` | AI Runtime |
| `specs/schemas/` | `contracts/ui/` | UI specification schema |

`apps/*` and `services/*` are a conventional monorepo shape carrying the same responsibilities. Do not
rename them to `frontend/` and `backend/` without a new ADR superseding 0001.

Not yet created, because no authorised increment needs them:

```
services/domain/ai/          AI Runtime — model gateway, prompt assembly
ml/                          model lifecycle — training, packaging, registry
edge/  enterprise/           deployment composition only, never business logic
ops/  infra/  ci/            runbooks, environments, pipeline definitions
contracts/                   shared cross-runtime schemas, if the schema outgrows specs/schemas/
```

The AI Runtime begins life as a bounded module inside the Domain Runtime rather than a separate
deployable. The boundary is enforced by interface and dependency direction, not by process isolation.
Do not promote it to its own service without an architecture decision recorded in
`docs/architecture.md`.

## Working method

Specification precedes implementation. If a task requires behaviour that `specs/spec.md` does not
describe, update the specification in the same change and say so.

Contract changes are wide changes. Any modification to the component vocabulary, component props, the
grounded context shape, or the UI specification schema requires all four of the following in one
change, or the change is incomplete:

1. `specs/model-contracts.md` updated.
2. `specs/schemas/ui-spec.schema.json` updated.
3. Deterministic tests added or amended under `tests/`.
4. Eval cases added or amended under `evals/`.

Requirements are traceable. Business requirements are numbered `BR-n`, functional requirements `FR-n`,
validation requirements `VR-n`, and architecture decisions `AD-n`. Cite the identifier you are
satisfying in commit messages and pull request descriptions.

Scope is the deliverable. Implement the increment asked for, complete it fully, and stop. Do not
speculatively add caching, feature flags, message queues, retry frameworks, metrics backends, or
abstraction layers for requirements that do not yet exist.

## Conventions

TypeScript. Strict mode on. No `any`. Model-derived data is typed as `unknown` until it has passed
validation, and the validator is the only place that narrows it. Component props are explicit
interfaces. Registry entries are typed so that an unregistered component name fails to compile.

Python. Type hints throughout. Pydantic models for every request, response, grounded context, and
validated specification. No untyped dictionaries crossing a runtime boundary.

Validation. One validation pipeline, one place. Rejections carry a stable machine-readable code from
the list in `specs/model-contracts.md`. Never silently drop an invalid block without recording the
rejection.

Logging. Log the grounded context identifier, the raw model output, the validation outcome, and every
rejection code. This log is the evidence base for evals and for incident review. Do not log image
content or anything that could identify a customer board serial beyond what the domain layer already
exposes.

Text on screen. All user-facing wording is either model-generated within the text policy or a fixed
string in the fallback specification. Do not hard-code business copy inside renderer components.

## Terminology

UI specification — the validated JSON document describing a page as approved components and text.

Component registry — the fixed mapping from an approved component name to its React implementation.

Grounded context — the structured, domain-sourced input that bounds what the model may reference.

Controlled Generative UI — generation of layout and copy within a closed vocabulary, as distinct from
generating code.

Deterministic test — a repeatable pass or fail check with no model in the loop. Lives in `tests/`.

AI evaluation — a scored measurement of model behaviour across a case set. Lives in `evals/`.

## Out of scope for this phase

Physical camera integration. Edge image processing. Real-time PLC or MES signal handling. Automated
defect classification models. Human review override workflows. Production infrastructure,
provisioning, and deployment automation. Authentication and authorisation subsystems.

If a task appears to require one of these, stop and say so rather than building a partial version.
