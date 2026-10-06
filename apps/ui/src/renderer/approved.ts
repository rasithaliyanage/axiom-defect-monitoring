/**
 * The approved-input boundary.
 *
 * `ApprovedUISpec` is a branded type whose brand symbol is not exported, so a
 * value of that type cannot be constructed outside this module. The only values
 * it ever issues come from `src/generated/fixtures.ts`, which
 * `scripts/prepare_fixtures.py` writes only after the Task 3 Python validator
 * has returned VALID for every fixture against its matching context.
 *
 * What this does and does not prove
 * ---------------------------------
 * The brand is a guarantee of PROVENANCE, not of validity. It proves the data
 * came through the offline preparation gate. It does not itself validate
 * anything, and a cast, a brand or an `approved: true` flag would be worthless
 * as evidence on its own — the evidence is the passing Python gate, recorded as
 * content hashes in `VERIFICATION`.
 *
 * What it buys is that "no raw JSON reaches the renderer" stops being a
 * convention a reviewer has to police and becomes a property the compiler
 * enforces.
 *
 * VALID here means the presentation specification is well formed and grounded.
 * It never means a board passed, failed, or was approved.
 */

import {
  ACTION_LABELS,
  FIXTURES,
  VERIFICATION,
  type FixtureName,
  type VerificationRecord,
} from "../generated/fixtures";
import { isApprovedAction, isApprovedComponent, type ActionLabels, type UISpec } from "./types";

/** Not exported. Nothing outside this module can name it, so nothing can forge the brand. */
declare const APPROVED_BRAND: unique symbol;

export interface ApprovedUISpec extends UISpec {
  readonly [APPROVED_BRAND]: true;
}

export type { FixtureName, VerificationRecord };

/**
 * Issue the approved handle for a prepared fixture.
 *
 * The cast is the single minting point in the application, and it is reachable
 * only for data the preparation gate produced.
 */
export function approvedFixture(name: FixtureName): ApprovedUISpec {
  return FIXTURES[name] as ApprovedUISpec;
}

/** Action labels from the validated grounded context. Never model-authored. */
export function approvedActionLabels(name: FixtureName): ActionLabels {
  return ACTION_LABELS[name];
}

/** Offline verification evidence for a fixture: status and content hashes. */
export function verificationFor(name: FixtureName): VerificationRecord {
  const record = VERIFICATION.find((entry) => entry.name === name);
  if (record === undefined) {
    throw new Error(`No verification record for fixture "${name}"`);
  }
  return record;
}

export { VERIFICATION };

/* ------------------------------------------------------------------------- *
 * Restricted runtime transport adapter (Task 6)
 *
 * The Domain Runtime validates schema, grounding and text policy in Python
 * before responding. This adapter deliberately does NOT repeat any of that —
 * duplicating it in TypeScript would create a second, divergent authority.
 *
 * It checks two things only:
 *   1. Transport shape — is this the agreed response envelope?
 *   2. Fail-closed registry membership — does every block name an approved
 *      component? An unapproved name rejects the WHOLE response; nothing is
 *      skipped, repaired or substituted.
 *
 * There is deliberately no general `approve(rawJSON)` factory. Minting stays
 * inside this module, reachable only after the checks below pass.
 * ------------------------------------------------------------------------- */

export type TransportResult =
  | {
      readonly ok: true;
      readonly spec: ApprovedUISpec;
      readonly actionLabels: ActionLabels;
      readonly contextId: string;
    }
  | { readonly ok: false; readonly reason: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function reject(reason: string): TransportResult {
  return { ok: false, reason };
}

/** Accept a Domain Runtime landing response, or reject it entirely. */
export function acceptLandingResponse(payload: unknown): TransportResult {
  if (!isRecord(payload)) return reject("Response was not an object");

  const { spec, bindings, meta } = payload;
  if (!isRecord(spec)) return reject("Response contained no specification");
  if (!isRecord(bindings)) return reject("Response contained no bindings");
  if (!isRecord(meta)) return reject("Response contained no metadata");

  if (spec["specVersion"] !== "1.0") return reject("Unsupported specVersion");
  if (spec["page"] !== "landing") return reject("Unsupported page");

  const contextId = spec["contextId"];
  if (typeof contextId !== "string" || contextId.length === 0) {
    return reject("Specification carried no contextId");
  }
  // Identity association: the metadata must describe the spec it arrived with.
  if (meta["contextId"] !== contextId) {
    return reject("Metadata contextId does not match the specification");
  }
  if (meta["source"] !== "fixture") return reject("Unexpected presentation source");

  const blocks = spec["blocks"];
  if (!Array.isArray(blocks) || blocks.length === 0) {
    return reject("Specification carried no blocks");
  }
  for (const block of blocks) {
    if (!isRecord(block)) return reject("A block was not an object");
    const component = block["component"];
    if (typeof component !== "string" || !isApprovedComponent(component)) {
      // Whole-response rejection. The renderer is never given the chance.
      return reject(`Unapproved component in response: ${String(component)}`);
    }
  }

  const rawLabels = bindings["actionLabels"];
  if (!isRecord(rawLabels)) return reject("Bindings carried no action labels");
  const actionLabels: Record<string, string> = {};
  for (const [id, label] of Object.entries(rawLabels)) {
    if (typeof label !== "string") return reject("An action label was not a string");
    if (isApprovedAction(id)) actionLabels[id] = label;
  }

  // The single minting point for runtime data.
  return { ok: true, spec: spec as unknown as ApprovedUISpec, actionLabels, contextId };
}
