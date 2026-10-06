/**
 * Test-only minting of the approved handle.
 *
 * This file lives under `test/`, outside `src/`, deliberately. Renderer tests
 * need to feed crafted and hostile specifications to the renderer — an
 * unapproved component, an inherited object key, a payload with markup — and
 * those inputs cannot come from the preparation gate, because the gate would
 * correctly reject them.
 *
 * This is an isolated test mechanism, never a production bypass:
 *
 *   - It is not under `src/`, so it is not part of the application build.
 *   - `npm run lint` fails if any file under `src/` imports from `test/`.
 *
 * Application code obtains handles only from `approvedFixture()` in
 * `src/renderer/approved.ts`, which serves data the Python gate validated.
 */

import type { ApprovedUISpec } from "../../src/renderer/approved";
import type { UISpec } from "../../src/renderer/types";

/** Present a crafted specification to the renderer without the preparation gate. */
export function approveForTest(spec: UISpec): ApprovedUISpec {
  return spec as ApprovedUISpec;
}

/** Present deliberately malformed input, for renderer-boundary probes. */
export function approveUnsafeForTest(spec: unknown): ApprovedUISpec {
  return spec as ApprovedUISpec;
}
