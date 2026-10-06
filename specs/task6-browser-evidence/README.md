# Task 6 browser and API evidence

Captured during the Task 6 checkpoint verification pass on **2026-10-03**. These files exist so the
evidence map in the master walkthrough resolves to something real rather than to a narrative claim.

| File | Contents |
|---|---|
| `api-smoke.json` | Six live API checks plus revalidation of the live response through the Python validator |
| `observations.json` | Eight verified browser observations, two unverified checks, one known non-issue |
| `unavailable.json` | Backend-stopped behaviour and the no-fallback assertions |
| `wide-rendered.jpg` | The page rendered from the Domain Runtime |
| `backend-unavailable.jpg` | The controlled error state with the backend stopped |

## How this was produced

```
# repository root
.venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8000

# apps/ui
npm run dev            # http://localhost:5173
```

Both services were stopped afterwards and their listeners confirmed released.

## What this evidence does and does not establish

**Does:** the browser obtains the page from FastAPI over HTTP (`POST /api/v1/ui/landing-page -> 200`
in the network log); React genuinely renders all nine approved components; the Hero label is resolved
from server-owned context bindings; the live response revalidates as `VALID` with exact fixture and
ordered-binding equality; stopping the backend produces a visible error with no static fallback.

**Does not:** establish correctness of defect detection, quality decisions, or anything about real
boards. Everything shown is a developer-authored synthetic fixture. `VALID` refers to a UI
specification, never to a board passing inspection.

Nor does it establish narrow-viewport behaviour, cross-browser support, or assistive-technology
compatibility — all three are recorded as unverified in `observations.json`.

## Deliberately excluded

A third screenshot was captured while attempting the narrow-viewport check. It was **byte-identical**
to `wide-rendered.jpg`, which proves the viewport resize never took effect. Including it would have
implied a check that did not happen, so it was discarded rather than relabelled.
