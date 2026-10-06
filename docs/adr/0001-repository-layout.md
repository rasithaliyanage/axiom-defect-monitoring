# ADR-0001: Repository layout, and the relationship to the proposed structure

- **Status:** Accepted
- **Date:** 2026-09-30
- **Supersedes:** nothing
- **Related:** `CLAUDE.md` (Repository layout), `Documents/Proposed Project Structure - Board Defect Inspection (AI-Native)-Vinod.pdf`

## Format

Decision records are numbered, append-only, and never edited once Accepted. A decision that changes
is superseded by a new record that names the one it replaces. Each record states: context, the
decision, the alternatives rejected, and the consequences — including what would reopen it.

## Context

Two documents specified a repository layout, and they disagreed:

| Source | UI Runtime | Domain Runtime |
|---|---|---|
| `CLAUDE.md` "Repository layout" | `apps/ui/` | `services/domain/` |
| Proposed Project Structure (review draft) | `frontend/` | `backend/` + `ai/` |

The repository followed `CLAUDE.md`, so the deviation was not accidental drift — it matched the file
that governs how Claude Code works here. But nothing recorded that the two differed, so a reader
comparing the tree against the proposal would reasonably conclude the structure was wrong.

The proposed structure describes itself as a review draft that is "not a validated reference
architecture", carries five open decisions of which the first two "change the shape of the tree", and
advises: *"Do not accept this layout on paper. Build the first vertical slice through it… and watch
for files that want a home the tree does not offer."*

## Decision

`CLAUDE.md` is the authoritative repository layout. `apps/ui/` and `services/domain/` keep their
names and are recorded there as filling the `frontend/` and `backend/` roles respectively.

The harness and governance directories that both documents agree on, and that nothing depended on,
are created now: `policies/`, `docs/adr/`, `docs/quality-gates.md`, `docs/security.md`, `plans/`,
`tasks/`, `simulators/capture/`, and `.claude/{rules,hooks,agents}/`.

Directories that no authorised increment needs — `ml/`, `edge/`, `enterprise/`, `ops/`, `infra/`,
`ci/` — are deliberately not created. Empty directories imply commitments nobody has made.

The UI specification schema stays at `specs/schemas/ui-spec.schema.json`, the file
`services/domain/validator.py` loads. It does not move to `contracts/ui/`.

## Alternatives rejected

**Rename to `frontend/` and `backend/`.** Cheap in mechanical terms — `git mv` plus nine import and
path edits — but it would adopt an unratified draft over the checked-in governing file, against that
draft's own advice to validate the layout by building through it first. Deferred, not refused: a
future ADR may supersede this one.

**Change nothing and record only the analysis.** Leaves `policies/` absent, which is the one gap with
a live consequence — without it, business-owned values have no home and tend to get written into
engineering files as plausible defaults.

## Consequences

The two layouts no longer silently disagree; `CLAUDE.md` states the mapping and points here.

No code moved, so no imports, path computations, or test fixtures changed. Both suites remain valid
without re-verification of moved paths.

`policies/` exists and is owned by Quality and Manufacturing. Engineering does not fill it in.

**What would reopen this:** a second deployment target (edge tier) needing its own composition
directory; extraction of the AI Runtime into a separate deployable; or resolution of open decisions 1
and 2 in the proposed structure (deployment granularity and repository strategy), either of which may
make `frontend/`/`backend/` the better shape. Any of those warrants a superseding ADR, not an edit to
this one.
