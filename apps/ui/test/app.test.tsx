/**
 * Task 5 assets that remain valid after Task 6.
 *
 * The application's runtime source is now the Domain Runtime, so the
 * static-fixture mounting tests that lived here have been superseded by
 * `api-integration.test.tsx`. The prepared catalogue itself is retained — it
 * still backs tests and still proves the offline gate ran — and the error
 * boundary is unchanged.
 */

import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ErrorBoundary } from "../src/ErrorBoundary";
import {
  approvedActionLabels,
  approvedFixture,
  verificationFor,
  VERIFICATION,
} from "../src/renderer/approved";
import { UISpecRenderer } from "../src/renderer/renderUISpec";
import { ACTION_IDS } from "../src/renderer/types";

describe("prepared fixture catalogue", () => {
  it("carries offline verification evidence for every fixture", () => {
    expect(VERIFICATION.length).toBeGreaterThan(0);
    for (const record of VERIFICATION) {
      expect(record.status).toBe("VALID");
      expect(record.specSha256).toMatch(/^[0-9a-f]{64}$/);
      expect(record.contextSha256).toMatch(/^[0-9a-f]{64}$/);
    }
  });

  it("issues an approved handle whose contextId matches its verification record", () => {
    const spec = approvedFixture("full-catalogue");
    expect(spec.contextId).toBe(verificationFor("full-catalogue").contextId);
    expect(spec.specVersion).toBe("1.0");
    expect(spec.page).toBe("landing");
  });

  it("sources action labels from the validated context, not the model", () => {
    const labels = approvedActionLabels("full-catalogue");
    for (const action of ACTION_IDS) {
      expect(typeof labels[action]).toBe("string");
    }
  });

  it("renders through the controlled renderer with a catalogue handle", () => {
    const { container } = render(
      <UISpecRenderer
        spec={approvedFixture("task4-demo")}
        options={{ actionLabels: approvedActionLabels("task4-demo") }}
      />,
    );
    expect(container.querySelectorAll(".uispec-block")).toHaveLength(3);
    expect(screen.getByRole("button", { name: "Open defect reports" })).toBeDefined();
  });
});

describe("determinism and non-mutation of the catalogue", () => {
  it("leaves the approved fixture unchanged after rendering and clicking", () => {
    const before = structuredClone(approvedFixture("full-catalogue"));
    render(
      <UISpecRenderer
        spec={approvedFixture("full-catalogue")}
        options={{
          actionLabels: approvedActionLabels("full-catalogue"),
          onAction: () => undefined,
        }}
      />,
    );
    for (const button of screen.getAllByRole("button")) button.click();
    expect(approvedFixture("full-catalogue")).toEqual(before);
  });
});

describe("error boundary", () => {
  // Isolated: a component that throws on purpose, never a production bypass.
  function Explode(): never {
    throw new Error("Deliberate test failure");
  }

  it("shows a fixed message and does not repair or substitute anything", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => undefined);
    render(
      <ErrorBoundary>
        <Explode />
      </ErrorBoundary>,
    );
    const alert = screen.getByRole("alert");
    expect(alert.textContent).toContain("could not be rendered");
    expect(alert.textContent).toContain("Nothing was repaired, substituted or retried");
    expect(document.querySelector(".uispec-page")).toBeNull();
    spy.mockRestore();
  });
});

describe("deterministic fallback specification (TASK-005)", () => {
  it("renders through the existing registry with no new component", () => {
    const { container } = render(
      <UISpecRenderer
        spec={approvedFixture("fallback")}
        options={{ actionLabels: {} }}
      />,
    );
    expect(container.querySelectorAll(".uispec-block").length).toBeGreaterThan(0);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe(
      "Board inspection activity",
    );
  });

  it("renders with no action labels at all, because it binds no action", () => {
    render(
      <UISpecRenderer spec={approvedFixture("fallback")} options={{ actionLabels: {} }} />,
    );
    // No control, so nothing can be clicked and nothing needs a label.
    expect(screen.queryByRole("button")).toBeNull();
  });

  it("records no omission, so every block resolved", () => {
    const onOmission = vi.fn();
    render(
      <UISpecRenderer
        spec={approvedFixture("fallback")}
        options={{ actionLabels: {}, onOmission }}
      />,
    );
    expect(onOmission).not.toHaveBeenCalled();
  });
});
