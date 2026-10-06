/**
 * Restricted HTTP client for the Domain Runtime.
 *
 * One endpoint, one method, a fixed request body. There is no general "call any
 * URL" helper: the path is a module constant, so no API or model data can steer
 * a request. Responses are treated as `unknown` until the transport adapter in
 * `renderer/approved.ts` accepts them.
 *
 * Reaches the API through the Vite dev proxy, so this is a same-origin relative
 * request and no CORS configuration is involved.
 */

import {
  acceptLandingResponse,
  type TransportResult,
} from "../renderer/approved";

const LANDING_PAGE_PATH = "/api/v1/ui/landing-page" as const;

export type ViewName = "overview" | "minimal";
export type LocaleName = "en-US";

/**
 * The developer-owned request context.
 *
 * Fixed at build time. There is no form, query string, selector or other input
 * that can influence it — a caller may choose a view, nothing more.
 */
export interface RequestContext {
  readonly page: "landing";
  readonly view: ViewName;
  readonly locale: LocaleName;
}

export const INITIAL_CONTEXT: RequestContext = {
  page: "landing",
  view: "overview",
  locale: "en-US",
};

export interface FetchOptions {
  readonly view?: ViewName;
  /** Lets a caller cancel a stale request. */
  readonly signal?: AbortSignal;
}

/**
 * Request the landing presentation.
 *
 * Returns the adapter's verdict. Transport-level problems are reported the same
 * way as an unusable body, so a caller cannot accidentally treat a failure as a
 * success. An HTTP 200 on its own is never treated as validation.
 */
export async function fetchLandingPage(options: FetchOptions = {}): Promise<TransportResult> {
  const { view = INITIAL_CONTEXT.view, signal } = options;

  // Snapshot the scalar values before any asynchronous work, so a caller
  // mutating its own state mid-flight cannot change what was requested.
  const requested: RequestContext = {
    page: INITIAL_CONTEXT.page,
    view,
    locale: INITIAL_CONTEXT.locale,
  };

  let response: Response;
  try {
    response = await fetch(LANDING_PAGE_PATH, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(requested),
      ...(signal ? { signal } : {}),
    });
  } catch (cause) {
    if (cause instanceof DOMException && cause.name === "AbortError") throw cause;
    return { ok: false, reason: "Could not reach the Domain Runtime" };
  }

  if (!response.ok) {
    return { ok: false, reason: `Domain Runtime returned HTTP ${response.status}` };
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    return { ok: false, reason: "Response was not valid JSON" };
  }

  return acceptLandingResponse(payload);
}

export { LANDING_PAGE_PATH };
