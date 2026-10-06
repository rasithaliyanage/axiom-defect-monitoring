/**
 * Application root.
 *
 * Task 6: the runtime page now comes from the Domain Runtime over HTTP. The
 * static prepared catalogue is retained for tests, but is NOT used as a silent
 * fallback — if the API is unavailable the application says so and renders
 * nothing else. Hiding a failed dependency behind hard-coded content would make
 * a broken boundary look healthy.
 *
 * No raw JSON reaches the renderer: the response passes through the transport
 * adapter, which either issues an ApprovedUISpec handle or rejects the whole
 * response.
 */

import { useEffect, useState, type JSX } from "react";

import { fetchLandingPage, type ViewName } from "./api/client";
import { ErrorBoundary } from "./ErrorBoundary";
import type { ApprovedUISpec } from "./renderer/approved";
import { UISpecRenderer } from "./renderer/renderUISpec";
import type { ActionId, ActionLabels, Omission } from "./renderer/types";

type Screen =
  | { readonly kind: "loading" }
  | {
      readonly kind: "ready";
      readonly spec: ApprovedUISpec;
      readonly actionLabels: ActionLabels;
      readonly contextId: string;
    }
  | { readonly kind: "failed"; readonly reason: string };

export interface AppProps {
  readonly view?: ViewName;
  /** Developer-owned. Tests record identifiers; the demonstration is inert. */
  readonly onAction?: (action: ActionId) => void;
  readonly onOmission?: (omission: Omission) => void;
}

export function App({ view = "overview", onAction, onOmission }: AppProps): JSX.Element {
  const [screen, setScreen] = useState<Screen>({ kind: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    let current = true; // Guards against a stale response winning a race.

    void (async () => {
      try {
        const result = await fetchLandingPage({ view, signal: controller.signal });
        if (!current) return;
        setScreen(
          result.ok
            ? {
                kind: "ready",
                spec: result.spec,
                actionLabels: result.actionLabels,
                contextId: result.contextId,
              }
            : { kind: "failed", reason: result.reason },
        );
      } catch (cause) {
        if (!current) return;
        if (cause instanceof DOMException && cause.name === "AbortError") return;
        setScreen({ kind: "failed", reason: "Unexpected client error" });
      }
    })();

    return () => {
      current = false;
      controller.abort();
    };
  }, [view]);

  const handleAction = (action: ActionId): void => {
    // Inert by design. No navigation, no network call, no state change.
    onAction?.(action);
  };

  return (
    <div className="app">
      {/* Developer-authored, deliberately outside any fixture text. */}
      <aside className="notice" role="note">
        <p className="notice-title">Synthetic demonstration — not live inspection data</p>
        <p className="notice-body">
          This page is served by the Domain Runtime, which validated a
          developer-authored specification against its server-owned context before responding.
          Controls are inert. Nothing shown is a board quality result, and no control changes the
          state of any board.
        </p>
        {screen.kind === "ready" ? (
          <p className="notice-evidence">
            Source <code>Domain Runtime</code> · view <code>{view}</code> · context{" "}
            <code>{screen.contextId}</code>
          </p>
        ) : null}
      </aside>

      {screen.kind === "loading" ? (
        <p className="state state-loading" role="status">
          Loading the inspection landing page…
        </p>
      ) : null}

      {screen.kind === "failed" ? (
        <div className="state state-failed" role="alert">
          <h2 className="state-title">The landing page could not be loaded</h2>
          <p className="state-body">
            The Domain Runtime did not return a usable presentation. Nothing was substituted in its
            place.
          </p>
          <p className="state-detail">{screen.reason}</p>
        </div>
      ) : null}

      {screen.kind === "ready" ? (
        <ErrorBoundary>
          <UISpecRenderer
            spec={screen.spec}
            options={{
              actionLabels: screen.actionLabels,
              onAction: handleAction,
              ...(onOmission ? { onOmission } : {}),
            }}
          />
        </ErrorBoundary>
      ) : null}
    </div>
  );
}
