/** Registry resolution, closure, and unapproved-name handling. */

import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { componentRegistry, hasRegisteredComponent } from "../src/renderer/registry";
import { UISpecRenderer } from "../src/renderer/renderUISpec";
import { COMPONENT_NAMES, type Block, type Omission, type UISpec } from "../src/renderer/types";
import { approveForTest } from "./support/approve";

import fullCatalogue from "../../../tests/fixtures/ui-spec/full-catalogue.spec.json";

const labels = {
  "view-inspection-queue": "Open inspection queue",
  "view-defect-reports": "Open defect reports",
  "view-ingest-activity": "Open ingest activity",
  "open-documentation": "Open documentation",
  "contact-support": "Contact support",
} as const;

function renderSpec(spec: UISpec, onOmission?: (o: Omission) => void) {
  return render(
    <UISpecRenderer
      spec={approveForTest(spec)}
      options={onOmission ? { actionLabels: labels, onOmission } : { actionLabels: labels }}
    />,
  );
}

describe("component registry", () => {
  it("contains exactly the nine approved components", () => {
    expect(Object.keys(componentRegistry).sort()).toEqual([...COMPONENT_NAMES].sort());
    expect(Object.keys(componentRegistry)).toHaveLength(9);
  });

  it("resolves every approved component through the registry", () => {
    for (const name of COMPONENT_NAMES) {
      expect(hasRegisteredComponent(name)).toBe(true);
      expect(typeof componentRegistry[name]).toBe("function");
    }
  });

  it("renders every approved component from the catalogue fixture", () => {
    const spec = fullCatalogue as unknown as UISpec;
    const { container } = renderSpec(spec);
    expect(container.querySelectorAll(".uispec-block")).toHaveLength(spec.blocks.length);
    expect(screen.getByRole("heading", { level: 1 })).toHaveProperty(
      "textContent",
      "Board inspection activity",
    );
    expect(container.querySelector(".info-panel")).not.toBeNull();
    expect(container.querySelector(".progress")).not.toBeNull();
    expect(container.querySelector(".feature-grid")).not.toBeNull();
    expect(container.querySelector(".alert")).not.toBeNull();
  });
});

describe("unapproved names cannot resolve", () => {
  const hostile = ["run_query", "DispositionControl", "Script", "", "hero"];

  it.each(hostile)("rejects %s as a registry component", (name) => {
    expect(hasRegisteredComponent(name)).toBe(false);
  });

  const inherited = ["toString", "constructor", "__proto__", "hasOwnProperty", "valueOf"];

  it.each(inherited)("does not resolve inherited object key %s", (name) => {
    expect(hasRegisteredComponent(name)).toBe(false);
  });

  it("omits an unapproved block and records the omission", () => {
    const onOmission = vi.fn();
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "probe",
      blocks: [
        { component: "Text", props: { text: "Rendered." } },
        { component: "DispositionControl", props: { label: "Mark board" } },
        { component: "Heading", props: { level: 2, text: "Still rendered" } },
      ] as unknown as Block[],
    } as UISpec;

    const { container } = renderSpec(spec, onOmission);

    expect(container.querySelectorAll(".uispec-block")).toHaveLength(2);
    expect(container.textContent).not.toContain("Mark board");
    expect(onOmission).toHaveBeenCalledTimes(1);
    expect(onOmission.mock.calls[0]?.[0]).toMatchObject({
      reason: "unapproved-component",
      path: "/blocks/1",
    });
  });

  it("omits an inherited-key block rather than resolving it", () => {
    const onOmission = vi.fn();
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "probe",
      blocks: [{ component: "constructor", props: {} }] as unknown as Block[],
    } as UISpec;

    const { container } = renderSpec(spec, onOmission);

    expect(container.querySelectorAll(".uispec-block")).toHaveLength(0);
    expect(onOmission).toHaveBeenCalledTimes(1);
  });
});
