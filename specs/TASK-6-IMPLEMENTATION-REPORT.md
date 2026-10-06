# Task 6 implementation report — Domain Runtime / FastAPI boundary

- **Date:** 2026-09-30
- **Branch:** `wushan` · **HEAD:** `3810dc0` · Git readable, no failures
- **Committed:** no. Tasks 4, 5, the structure alignment and this increment are all uncommitted.

## Corrections to the task premise

Two statements in the Task 6 prompt were not accurate for this repository.

**"Task 5 has local implementation and browser verification evidence."** The Task 5 browser check was
explicitly recorded as **UNVERIFIED** — the Chrome extension was not connected. Task 6 is the first
increment with real browser evidence.

**Referenced paths that do not exist:** `docs/repository-structure.md`, `tests/renderer_fixtures/`,
`apps/ui/fixtures/`, `apps/ui/src/{types,render,components}.ts(x)`,
`specs/TASK-4-IMPLEMENTATION-REPORT.md`. The actual layout is `apps/ui/src/renderer/*`,
`apps/ui/src/components/approved.tsx` and `tests/fixtures/ui-spec/`. The renderer is
`UISpecRenderer`, not `ControlledRenderer`; it was not renamed, per the instruction to use the actual
existing API.

## Readiness decisions, recorded

| # | Decision | Reasoning |
|---|---|---|
| 1 | `POST /api/v1/ui/landing-page`, body `{page:"landing", view:"overview"\|"minimal"}` | Board direction. POST because there is a body to police: `extra="forbid"` **rejects** supplied grounding rather than ignoring it |
| 2 | Success `{spec, bindings, meta}`; errors `{error:{code,message}}` | Not a generic wrapper. `bindings` is required because `Hero.primaryAction` has no label in the contract. `meta` carries identity and provenance only — no approval flag, no auth claim |
| 3 | `bindings.actionLabels` derived from the same validated context | Server-owned. Never invented |
| 4 | Transport adapter inside `approved.ts`; no general `approve(rawJSON)` | Keeps the single minting point. Checks transport shape and registry membership only |
| 5 | Canonical fixtures stay at `tests/fixtures/ui-spec/` | No move, no duplicate. FastAPI reads the pair the preparation gate validates |
| 6 | Vite proxy `/api → 127.0.0.1:8000`; **no CORS** | Same-origin from the browser. UI 5173, API 8000 |

## Files created

| File | Purpose |
|---|---|
| `services/domain/landing_service.py` | Fixture snapshot, validation, binding derivation. No HTTP |
| `services/domain/api/{__init__,main,routes,models}.py` | FastAPI app, sanitized error handlers, routes, transport models |
| `apps/ui/src/api/client.ts` | Restricted client: one path, one method, fixed body |
| `tests/api/test_landing_api.py` | 19 tests |
| `apps/ui/test/api-integration.test.tsx` | 22 tests |
| `specs/TASK-6-IMPLEMENTATION-REPORT.md` | This report |

## Files modified

`apps/ui/src/renderer/approved.ts` (transport adapter appended; minting unchanged and still private) ·
`apps/ui/src/App.tsx` (loading/success/failure, stale-response guard) · `apps/ui/src/style.css`
(state styles) · `apps/ui/vite.config.ts` (proxy) · `apps/ui/test/app.test.tsx` (static-fixture App
tests superseded; catalogue and error-boundary tests retained) · `pytest.ini` (added `tests/api`) ·
`requirements.txt`, `requirements-dev.txt` · `services/domain/README.md`, `apps/ui/README.md`.

**Nothing in `specs/` or the validator changed.** No contract rule, schema bound, component, prop or
rejection code was altered.

## Superseded, not dropped

Task 5's `app.test.tsx` mounted `App` against the static catalogue. The runtime source is now the API,
so those specific assertions were replaced by `api-integration.test.tsx`. The catalogue tests,
verification-evidence tests and error-boundary test remain in `app.test.tsx`.

## Verification — commands actually run

| # | Command | Result |
|---|---|---|
| 1 | `pytest -q` (root) | **189 passed** (170 prior + 19 new) |
| 2 | `pytest --collect-only -q` | **189 collected**, matching 189 passed — confirms `tests/api` is discovered, not silently skipped |
| 3 | `npm test` (apps/ui) | **84 passed** (5 files) |
| 4 | `npm run typecheck` | clean, strict |
| 5 | `npm run lint` | `safety lint: clean (10 files, 9 rules)` |
| 6 | `npm run build` | built in 1.22s |
| 7 | `pip check` | No broken requirements found |

### Schema checks, reported separately

Unchanged by Task 6, re-confirmed: JSON parsing PASS (both schemas) · Draft 2020-12 **meta**-validation
PASS (both) · **instance** validation of both fixtures PASS against `specs/schemas/` ·
**full runtime** validation VALID, 0 rejections. The alternative schema still reports
`deprecated: true` and is still not loaded.

### Live API

```
GET  /health                     → 200  {"status":"ok"}
POST /api/v1/ui/landing-page     → 200  keys [bindings, meta, spec]
                                        meta {contextId: task4-catalogue, source: fixture, validation: VALID}
                                        12 blocks, 5 action labels
POST … + {"context":{...}}       → 400  {"error":{"code":"BAD_REQUEST",...}}
GET  /api/v1/ui/landing-page     → 405
POST via proxy on :5173          → 200  (identical body)
```

### Real browser — **VERIFIED**

Chrome, `http://localhost:5173/`.

- **Network log shows `POST http://localhost:5173/api/v1/ui/landing-page → 200`** — the page data
  demonstrably comes from FastAPI, not the static catalogue
- All nine components rendered; Hero showed **"Open inspection queue"**, which exists only in the
  context bindings — proving the binding path end to end
- Synthetic notice visible, reading "served by the Domain Runtime", with view and contextId
- Alert severity rendered as the word **WARNING**, not colour alone
- Keyboard `Tab` produced a visible focus ring on the Hero action
- Console clean: only Vite HMR and the React DevTools notice. No errors or warnings
- No external or model traffic. The only non-localhost requests were an unrelated Acrobat browser
  extension
- **Backend stopped → controlled error**: "The landing page could not be loaded / Nothing was
  substituted in its place", and **no page content rendered**. No silent static fallback

Screenshots: `screenshot-1790751898198-0.jpg` (rendered page), `-1.jpg` (Alert/InfoPanel/Progress),
`-2.jpg` (backend unavailable), `-4.png` (focus ring), under
`C:\Users\WDARSH~1\AppData\Local\Temp\claude-chrome-screenshots-5C3eGT\`.

One observation worth recording: the network log shows a `503` immediately before the `200`. That is
React StrictMode's double-mounted effect being aborted by the cleanup, surfacing through the Vite
proxy. The stale-response guard discards it, and the rendered result is the `200`.

**Not verified:** narrow-viewport layout. `resize_window` reported success but the captured viewport
stayed at its original width, so the ≤30rem media query was not visually confirmed. The CSS exists;
the check did not run. Attempted twice (2026-09-30 and 2026-10-03) with the same outcome — this is an
environment limitation, not a code defect. Closing it needs a headless browser with real viewport
control (Playwright or similar), which has not been added because nothing else requires it.

## Post-checkpoint amendments (2026-10-03)

A checkpoint verification pass against
`Documents/BOARD_DEFECT_INSPECTION_TASK_6_CHECKPOINT_BEGINNER_FRIENDLY_ENTERPRISE_GRADE.docx`
produced two findings. Both are now applied.

**1. `/health` was not reachable through the Vite proxy — fixed.** The proxy forwarded only `/api`,
while the service exposes health at `/health`, outside the versioned API. `localhost:5173/health`
therefore returned the SPA shell: HTTP 200 and HTML, so a liveness check appeared to succeed without
ever reaching the backend. `vite.config.ts` now forwards `/health` as well. Verified:
`curl http://localhost:5173/health` → `{"status":"ok"}`, with landing and SPA routing unaffected.

**2. Narrow viewport — recorded, not fixed.** No code change; see above. Now documented as a known
gap in `apps/ui/README.md` so it is visible to anyone reading the UI package rather than only here.

**3. Error envelope did not cover routing errors — fixed.** Found by reading the captured API
evidence rather than by a failing test, which is why it had survived.

`main.py` registered its handler against **FastAPI's** `HTTPException`. Starlette's routing raises
its own `HTTPException`, which FastAPI's *subclasses* — so registering against the child missed the
parent. 404 and 405 bypassed the handler and returned Starlette's default `{"detail": "Not Found"}`,
while `services/domain/README.md` and the `main.py` docstring both promised that *every* error used
`{"error": {code, message}}`.

The handler is now registered against `starlette.exceptions.HTTPException`, which catches both, and
routing statuses map to stable codes (`NOT_FOUND`, `METHOD_NOT_ALLOWED`) rather than echoing
Starlette's wording. Verified live: all four error paths now return the envelope.

Five tests were added that would have caught it — four parameterised routing cases asserting the
exact body and that `detail` is absent, plus one asserting every error response across four
different failure modes shares one shape.

**4. Proxy configuration had no regression guard — added.** The `/health` gap in finding 1 failed
*silently*: the dev server answered with the SPA shell, so a liveness check saw HTTP 200 and looked
healthy. `apps/ui/test/proxy-config.test.ts` now asserts both prefixes are forwarded, that no CORS
configuration exists, and that no wildcard target is used. The guard was checked against a config
with `/health` removed to confirm it actually fails rather than passing vacuously.

### Counts after these fixes

Python **194** passed (163 validator + 7 fixture + 24 API). UI **88** passed across 6 files.
`pip check` clean; typecheck, safety lint and build all clean.

### Checkpoint document mismatch — open, not actioned

That checkpoint document describes a different build from ours: port 8001, request
`{"page":"landing","locale":"en-US"}`, response `{spec, source, rejections, contextId, actions}`,
grounding rejected with 422, canonical fixtures under `apps/ui/fixtures/`, 197 Python and 63 React
tests, plus `check-browser.mjs`, `requirements-lock.txt` and `specs/task6-browser-evidence/`.

None of those match this repository. Our contract is `{"page":"landing","view":"overview"}` on port
8000 returning `{spec, bindings, meta}`, rejecting grounding with 400, with 189 Python and 84 React
tests. Following that document's reproduction commands verbatim returns **HTTP 400**, because
`locale` is not an accepted field and `extra="forbid"` rejects it.

The document was left unchanged — it is another session's artifact. Reconciling it is a separate
documentation decision.

## Excluded scope — confirmed

No AI or model integration, no model gateway, no generation. No authentication, database,
persistence, document processing, onboarding, uploads or risk scoring. No approval or override
workflow. No production infrastructure. No camera, edge, PLC or MES integration. No defect
classifier, defect-ratio calculation or quality decision. No renderer bypass, no duplicated Python
validator in TypeScript, no arbitrary execution path. No contract, schema or grounding change hidden
in the HTTP integration.

A static test asserts the Domain Runtime imports no model SDK, HTTP client, ORM or cloud SDK. An
autouse fixture blocks outbound TCP during API tests. (`socket.socket` itself is left alone: the
event loop needs a local socket pair, and the in-process TestClient is the intended path.)

## Dependencies added

`fastapi 0.142.1`, `uvicorn 0.54.0`, `httpx 0.28.1` (test client), pulling `starlette 1.7.0`,
`anyio 4.15.1`, `h11 0.16.0`, `httpcore 1.0.9`, `click 8.5.0`, `certifi`, `idna`, `annotated-doc`,
`opentelemetry-api`. No AI SDK, ORM, auth, broker or agent framework. No React dependency added.

## Limitations

Narrow-viewport check unverified, as above.

`CLAUDE.md` rule 3 still requires one bounded repair attempt then a deterministic fallback
specification. Neither exists. The client error state is **not** that fallback — it reports failure
rather than substituting content, which is the correct behaviour in its absence but does not satisfy
the rule.

`UnsupportedView` is unreachable over HTTP because the transport `Literal` rejects an unknown view
first. It is retained as defence in depth and tested directly.

Starlette warns that `httpx` with its TestClient is deprecated in favour of `httpx2`. Harmless today;
worth revisiting when pins are next reviewed.

`Documents/.tmp-doc-tools/` shows ~185 modified files from another session's vendored `python-docx`.
Not touched.

## Recommended next task

**TASK-005, the deterministic fallback specification.** It is now the only outstanding item that a
non-negotiable rule requires, it adds no dependency, and with the API in place it is the natural
precondition for the model gateway that follows.
