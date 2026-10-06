# Task 6A readiness — presentation request seam

- **Date:** 2026-10-03 (readiness), 2026-10-06 (verification completed)
- **Branch:** `wushan` · **HEAD:** `3810dc0` · Git readable
- **Outcome:** readiness was **BLOCKED**; scope was narrowed by explicit user decision and only the
  narrowed scope was implemented.

## Premise corrections

The Task 6A brief described a build this repository does not have.

| Brief assumes | Actual |
|---|---|
| Request is `{page, locale}` | Request is `{page, view}`. `locale` appears nowhere in the request |
| Rejection is HTTP `422` with `{"error":"invalid_request"}` | HTTP `400` with `{"error":{"code","message"}}` |
| Canonical fixture `apps/ui/fixtures/overview.spec.json` | `tests/fixtures/ui-spec/full-catalogue.{spec,context}.json`, plus a second pair |
| Response carries `source`, `rejections`, `contextId`, `actions` at top level | `{spec, bindings, meta}` |
| Sources at `apps/ui/src/{approved,types,registry,render}.*` | Under `apps/ui/src/renderer/` and `apps/ui/src/api/` |
| Baseline 197 Python / 63 UI | 194 / 88 at the time of readiness |

Ten paths named in the brief's reading list do not exist, including
`docs/repository-structure.md`, `tests/domain_api`, `tests/renderer_fixtures` and `apps/ui/tests`.

## Blocking decisions raised

1. **`locale` would be a new request field**, which the brief itself forbids ("No new fields"). And
   if `ContextPayload` is "exactly page and locale", `view` has no home.
2. **"Both required, no defaults" conflicts with "no wire change."** Removing defaults moves a
   request omitting `page` from `200` to rejected — that *is* a wire-semantics change.
3. **The mandated `422` + flat `{"error":"invalid_request"}` reverses a fix made the same day.**
   The Task 6 checkpoint found that routing errors leaked Starlette's `{"detail": ...}`; that was
   corrected so every error uses one envelope. Adopting the brief's shape reintroduces the
   inconsistency, while the brief simultaneously says to preserve the sanitized 404/405/500
   contracts.
4. **The brief's canonical fixture path contradicts ADR-0001** and would break the preparation gate
   and both suites.
5. **The brief describes a different response envelope while instructing that ours be retained.**
   Self-contradictory.

## Decisions taken

Put to the user explicitly and recorded here.

**Scope: seam only, using our real fields.** Add an immutable domain request constructed after HTTP
validation and passed explicitly to the service. **No wire change, no output change, no contract
change, no fixture move.** Blockers 1–5 deferred.

**Variants: expected.** The user confirmed that multiple lines, shifts, board types and locales are
anticipated. This shapes the seam but adds nothing: `ContextPayload` is a named frozen dataclass with
enum fields, so new dimensions become additional fields and enum members rather than a redesign.
Their value sets are business-owned and undecided, so **none were invented** — adding speculative
fields would convert an open question into an apparent requirement.

## Representation choice

A **frozen dataclass with `StrEnum` fields**, not a Pydantic model.

`api/models.py` is already Pydantic and has rejected unknown fields, wrong types and supplied
grounding before this value is constructed. A second Pydantic model would re-validate the same values
— the duplicate validation layer the brief warns against. The dataclass instead marks a *domain*
boundary: an immutable, enum-typed value rather than a bare string.

`__post_init__` type checks remain, because the value is also constructed directly in tests and could
later be constructed by a non-HTTP caller where no Pydantic layer has run.

This is consistent with `CLAUDE.md`'s "Pydantic models for every request" — the *transport* request
stays Pydantic; this is the domain value it produces.

## Deferred, with its guard

Making both fields required is deferred. `tests/api/test_request_context.py::test_omitted_fields_still_default`
pins current behaviour so the deferral stays visible and will fail loudly if defaults are removed
without a contract update.
