/**
 * Error boundary for the demonstration shell.
 *
 * This is NOT a model-repair or fallback-UISpec loop. It catches a React
 * rendering error and shows a fixed, developer-authored message. It never
 * retries generation, never substitutes another specification, and never
 * repairs or relabels a block.
 *
 * The deterministic fallback specification required by CLAUDE.md rule 3 is a
 * separate, unbuilt increment (TASK-005). This boundary does not stand in for it.
 */

import { Component, type ErrorInfo, type JSX, type ReactNode } from "react";

interface Props {
  readonly children: ReactNode;
}

interface State {
  readonly failed: boolean;
  readonly message: string;
}

export class ErrorBoundary extends Component<Props, State> {
  override state: State = { failed: false, message: "" };

  static getDerivedStateFromError(error: unknown): State {
    return {
      failed: true,
      message: error instanceof Error ? error.message : "Unknown rendering error",
    };
  }

  override componentDidCatch(error: Error, info: ErrorInfo): void {
    // Recorded for the developer console only. No user-facing model content.
    console.error("Rendering failed", error, info.componentStack);
  }

  override render(): ReactNode {
    if (!this.state.failed) {
      return this.props.children;
    }
    return (
      <div className="boundary" role="alert">
        <h2 className="boundary-title">The page could not be rendered</h2>
        <p className="boundary-body">
          Rendering stopped. Nothing was repaired, substituted or retried.
        </p>
        <p className="boundary-detail">{this.state.message}</p>
      </div>
    ) as JSX.Element;
  }
}
