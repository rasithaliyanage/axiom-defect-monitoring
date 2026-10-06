# UI Runtime — Controlled UISpec Renderer

Task 4. Renders an **already-validated** UISpec through a closed component registry.

## Entry point

```
render(approvedUISpec, options)
```

Implemented as the `UISpecRenderer` React component in `src/renderer/renderUISpec.tsx`.

There is deliberately **no** `render(rawAIOutput)`. Raw model output has no entry point into this
package. The renderer performs no schema validation and no grounding checks — those authorities are
`specs/schemas/ui-spec.schema.json` and `services/domain/validator.py`, and duplicating them here
would create a second, divergent source of truth.

```
RAW AI OUTPUT
   ↓
UISpec Validator + grounded context     (services/domain/validator.py)
   ↓
VALIDATED UISpec
   ↓
Controlled Renderer                     (this package)
   ↓
Approved React components
   ↓
Browser UI
```

`VALID` refers to a UISpec. It never refers to a board passing, failing, or being approved.

## How approved input reaches the renderer

```
tests/fixtures/ui-spec/*.{spec,context}.json      developer-authored, synthetic
        ↓   scripts/prepare_fixtures.py  →  services/domain/validator.py
        ↓   any INVALID ⇒ generated output deleted, exit 1
src/generated/fixtures.ts                          + sha256 of every input
        ↓   src/renderer/approved.ts                the only minting point
ApprovedUISpec handle  →  UISpecRenderer  →  registry  →  browser
```

Preparation runs automatically before `dev`, `test` and `build`. It is offline: there is **no live
browser-to-Python transport**, and the application consumes only what the gate produced.

`approvedFixture(name)` returns an `ApprovedUISpec` — a type branded with a `unique symbol` that is
not exported, so no value of that type can be constructed outside `approved.ts`. The renderer accepts
nothing else.

**What that proves, and what it does not.** The brand guarantees **provenance**: the data came
through the gate. It is not validation. A cast, brand or `approved: true` flag is worthless as
evidence on its own — the evidence is the passing Python gate, recorded as content hashes in
`VERIFICATION` and shown in the page notice.

`VALID` refers to a UI specification. It never means a board passed, failed or was approved.

Tests need to feed the renderer hostile input the gate would rightly reject, so
`test/support/approve.ts` mints handles directly. It lives outside `src/` on purpose, and
`npm run lint` fails if anything under `src/` imports it.

## Component registry

`src/renderer/registry.ts` — a developer-authored `const` map, typed as:

```ts
type ComponentRegistry = { readonly [K in ComponentName]: BlockRenderer<K> };
```

Exhaustive by construction: omitting an approved component, or adding a name outside
`ComponentName`, is a compile error. Lookup goes through `Object.prototype.hasOwnProperty.call`, so
inherited keys (`toString`, `constructor`, `__proto__`) cannot resolve as components.

The nine approved components: `Hero`, `Heading`, `Text`, `FeatureCard`, `FeatureGrid`, `CTA`,
`Alert`, `InfoPanel`, `ProgressIndicator`. `DispositionControl` is **not** in v1 and cannot render.

## Unapproved components

Per `docs/architecture.md`, an unregistered block is **omitted and the omission recorded** via
`options.onOmission`; it is never resolved by any other means, repaired, or relabelled.

For a genuinely validated spec this path is unreachable — the schema's `oneOf` over nine
discriminated blocks rejects an unknown component at Gate 1, and the validator at Gate 2 with
`E_UNKNOWN_COMPONENT`. The renderer guard is defence in depth for input that bypassed validation.

Whole-spec rejection (VR-2) belongs to the validator, not the renderer.

## Hero.primaryAction

`Hero.primaryAction` is an approved action **identifier**. The contract carries no label prop for it,
and the only human-readable text lives in `GroundedContext.actions[].label`.

So `options.actionLabels` supplies those labels. They are domain-owned data, never model output. When
no label is supplied, no control is rendered and a `missing-action-label` omission is recorded —
rather than inventing a prop, URL, route, or destination.

`CTA` is unaffected: it carries its own `label` prop.

## DOM safety

- Props are destructured by name; **nothing from the spec is ever spread onto a DOM element**
- Model strings render as React text children only, so React escapes them
- No `eval`, `new Function`, `dangerouslySetInnerHTML`, `innerHTML`, or dynamic import — asserted by
  a source scan in `test/safety.test.tsx`
- Closed enums select from fixed literal maps; no spec value becomes a tag name, URL, style string,
  or event handler
- Heading levels branch explicitly to `<h2>` / `<h3>`; the level never becomes a computed tag name
- Actions dispatch an identifier to a developer-supplied callback. No navigation, no network

## Fidelity

Block order, text, metric values and units are rendered exactly as supplied. Nothing is calculated,
rounded, classified, or inferred. `ProgressIndicator` renders `String(value)`, so `62.5` stays
`62.5`.

## Commands

```
npm install               # or npm ci against the committed lockfile
npm run dev               # prepare fixtures, then Vite dev server
npm run prepare:fixtures  # offline validation gate on its own
npm run typecheck         # tsc --noEmit, strict
npm run lint              # safety scan of the render path
npm test                  # prepare fixtures, then vitest run
npm run build             # prepare, typecheck, production build
```

There is no `preview` script.

`typecheck` alone does not run the gate, so on a fresh checkout run `prepare:fixtures` first if
`src/generated/fixtures.ts` is missing.

From the repository root:

```
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check
```

## Runtime source: the Domain Runtime (Task 6)

The browser no longer renders the static catalogue. It POSTs to the Domain Runtime and renders what
that service returns, after the service has validated it in Python.

```
React → src/api/client.ts → POST /api/v1/ui/landing-page   (via Vite proxy)
      → FastAPI → fixed spec + complete context → Python validator → VALID
      → { spec, bindings, meta }
      → acceptLandingResponse()  transport shape + fail-closed registry check
      → ApprovedUISpec handle → UISpecRenderer → registry → browser
```

Start both, from two terminals:

```
# repository root
.venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8000

# apps/ui
npm run dev            # http://localhost:5173
```

Vite proxies both `/api` and `/health` → `http://127.0.0.1:8000`, so the browser makes a same-origin
request and **no CORS configuration exists on either side**.

`/health` needs its own proxy entry because it sits outside the versioned API on the service.
Without it the dev server answers `/health` with the SPA shell — HTTP 200 and HTML — so a liveness
check would appear to succeed while never reaching the backend.

```
curl http://localhost:5173/health     → {"status":"ok"}   (proxied to the Domain Runtime)
curl http://localhost:5173/           → the application
```

### Known verification gap: narrow viewport

The responsive rules (`@media (max-width: 30rem)` in `src/style.css`) are **not covered by any
automated or visual check**. jsdom performs no layout, so the Vitest suite cannot see them, and two
attempts to drive a narrow viewport through browser automation left the captured viewport at its
original width.

Closing this properly needs a headless browser with real viewport control (Playwright or similar).
That dependency has not been added, because nothing else currently requires it. Until then, treat
narrow-viewport behaviour as **unverified** rather than working.

The transport adapter lives in `renderer/approved.ts` and checks two things only: the agreed response
shape, and that every block names an approved component. An unapproved component **rejects the whole
response** — it never reaches the renderer. It deliberately does not re-check schema, grounding or
text policy; duplicating the Python authority in TypeScript would create a second, divergent one.
There is no general `approve(rawJSON)` factory.

`meta.validation: "VALID"` is informational. The adapter does not treat it as proof.

### Failure behaviour

Loading, success, HTTP/network failure and unusable-response are all handled. On failure the page
shows a controlled developer-owned error and renders nothing else — **it never silently falls back to
the static fixture**, because hiding a broken dependency makes a broken boundary look healthy. The
prepared catalogue is retained for tests only.

## The browser page

`npm run dev` serves a single page composed from the `full-catalogue` fixture: all nine approved
components and all five actions. A developer-authored notice above it states that the data is
synthetic and the controls inert, and shows the fixture's offline verification status and spec hash.
That notice is deliberately outside any fixture-authored text.

Clicking any control dispatches its action identifier to a developer-owned callback. Nothing
navigates, fetches, or changes any board.

## Not in this package

No model gateway, no API client, no data fetching, no authentication, no repair or fallback
orchestration, no routing. The renderer is a pure function of an approved spec plus developer-supplied
options.
