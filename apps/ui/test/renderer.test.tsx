/** Block structure, ordering, actions, grounding fidelity, determinism. */

import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { UISpecRenderer } from "../src/renderer/renderUISpec";
import { ACTION_IDS, type ActionId, type Omission, type UISpec } from "../src/renderer/types";
import { approveForTest } from "./support/approve";

import demo from "../../../tests/fixtures/ui-spec/task4-demo.spec.json";
import fullCatalogue from "../../../tests/fixtures/ui-spec/full-catalogue.spec.json";

const labels: Readonly<Record<ActionId, string>> = {
  "view-inspection-queue": "Open inspection queue",
  "view-defect-reports": "Open defect reports",
  "view-ingest-activity": "Open ingest activity",
  "open-documentation": "Open documentation",
  "contact-support": "Contact support",
};

function renderSpec(
  spec: UISpec,
  onAction?: (a: ActionId) => void,
  onOmission?: (o: Omission) => void,
) {
  return render(
    <UISpecRenderer
      spec={approveForTest(spec)}
      options={{
        actionLabels: labels,
        ...(onAction ? { onAction } : {}),
        ...(onOmission ? { onOmission } : {}),
      }}
    />,
  );
}

const catalogue = fullCatalogue as unknown as UISpec;
const demoSpec = demo as unknown as UISpec;

describe("block structure", () => {
  it("renders Hero, Text and CTA as sibling blocks, not children", () => {
    const { container } = renderSpec(demoSpec);
    const blocks = container.querySelectorAll(".uispec-page > .uispec-block");
    expect(blocks).toHaveLength(3);

    const hero = blocks[0]?.querySelector(".hero");
    expect(hero).not.toBeNull();
    // The CTA must not be nested inside the Hero.
    expect(hero?.querySelector(".cta")).toBeNull();
    expect(blocks[1]?.querySelector(".text")).not.toBeNull();
    expect(blocks[2]?.querySelector(".cta")).not.toBeNull();
  });

  it("preserves block order as supplied", () => {
    const { container } = renderSpec(catalogue);
    const rendered = [...container.querySelectorAll(".uispec-block")].map(
      (node) => node.firstElementChild?.className.split(" ")[0] ?? "",
    );
    expect(rendered[0]).toBe("hero");
    expect(rendered[1]).toBe("heading");
    expect(rendered[2]).toBe("text");
    expect(rendered[3]).toBe("feature-grid");
  });
});

describe("FeatureGrid", () => {
  function grid(count: number, columns: 2 | 3): UISpec {
    return {
      specVersion: "1.0",
      page: "landing",
      contextId: "grid",
      blocks: [
        {
          component: "FeatureGrid",
          props: {
            columns,
            items: Array.from({ length: count }, (_, i) => ({
              title: `Card ${i + 1}`,
              body: `Body ${i + 1}`,
            })),
          },
        },
      ],
    } as UISpec;
  }

  it.each([2, 6])("renders %i card-props items in supplied order", (count) => {
    const { container } = renderSpec(grid(count, 2));
    const titles = [...container.querySelectorAll(".feature-card-title")].map(
      (n) => n.textContent,
    );
    expect(titles).toHaveLength(count);
    expect(titles).toEqual(Array.from({ length: count }, (_, i) => `Card ${i + 1}`));
  });

  it("treats items as props objects, not nested blocks", () => {
    const { container } = renderSpec(grid(2, 3));
    expect(container.querySelector(".feature-grid-3")).not.toBeNull();
    // Cards inside a grid are not wrapped as top-level uispec blocks.
    expect(container.querySelectorAll(".uispec-block")).toHaveLength(1);
    expect(container.querySelectorAll(".feature-card")).toHaveLength(2);
  });
});

describe("actions", () => {
  it.each(ACTION_IDS)("CTA %s renders its label and dispatches only that id", (action) => {
    const onAction = vi.fn();
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "cta",
      blocks: [{ component: "CTA", props: { label: `Go ${action}`, action } }],
    } as UISpec;

    renderSpec(spec, onAction);
    const button = screen.getByRole("button", { name: `Go ${action}` });
    button.click();

    expect(onAction).toHaveBeenCalledTimes(1);
    expect(onAction).toHaveBeenCalledWith(action);
    // No navigation, no network, no href.
    expect(button.getAttribute("href")).toBeNull();
    expect(button.getAttribute("type")).toBe("button");
  });

  it("labels Hero.primaryAction from the supplied action labels", () => {
    const onAction = vi.fn();
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "hero",
      blocks: [
        {
          component: "Hero",
          props: { title: "Board inspection activity", primaryAction: "view-inspection-queue" },
        },
      ],
    } as UISpec;

    renderSpec(spec, onAction);
    const button = screen.getByRole("button", { name: "Open inspection queue" });
    button.click();
    expect(onAction).toHaveBeenCalledWith("view-inspection-queue");
  });

  it("omits the Hero control and records it when no label was supplied", () => {
    const onOmission = vi.fn();
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "hero",
      blocks: [
        {
          component: "Hero",
          props: { title: "Board inspection activity", primaryAction: "contact-support" },
        },
      ],
    } as UISpec;

    render(
      <UISpecRenderer spec={approveForTest(spec)} options={{ actionLabels: {}, onOmission }} />,
    );

    expect(screen.queryByRole("button")).toBeNull();
    expect(onOmission.mock.calls[0]?.[0]).toMatchObject({ reason: "missing-action-label" });
  });
});

describe("grounding fidelity", () => {
  it("InfoPanel preserves values and units verbatim", () => {
    const { container } = renderSpec(catalogue);
    const values = [...container.querySelectorAll(".info-panel-value")].map(
      (n) => n.textContent,
    );
    // "1,284" keeps its separator; "2.4" keeps its precision and gains its unit.
    expect(values).toEqual(["1,284", "2.4%"]);
  });

  it("ProgressIndicator shows the supplied percentage without rounding", () => {
    const { container } = renderSpec(catalogue);
    expect(container.querySelector(".progress-value")?.textContent).toBe("62");
    const bar = container.querySelector('[role="progressbar"]');
    expect(bar?.getAttribute("aria-valuenow")).toBe("62");
    expect(bar?.getAttribute("aria-valuemin")).toBe("0");
    expect(bar?.getAttribute("aria-valuemax")).toBe("100");
  });

  it("does not round or reformat a fractional percentage", () => {
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "p",
      blocks: [
        {
          component: "ProgressIndicator",
          props: { metricId: "m", label: "Shift progress", value: 62.5 },
        },
      ],
    } as UISpec;
    const { container } = renderSpec(spec);
    expect(container.querySelector(".progress-value")?.textContent).toBe("62.5");
  });
});

describe("accessibility", () => {
  it("renders heading levels as real heading elements", () => {
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "h",
      blocks: [
        { component: "Heading", props: { level: 2, text: "Level two" } },
        { component: "Heading", props: { level: 3, text: "Level three" } },
      ],
    } as UISpec;
    renderSpec(spec);
    expect(screen.getByRole("heading", { level: 2 }).textContent).toBe("Level two");
    expect(screen.getByRole("heading", { level: 3 }).textContent).toBe("Level three");
  });

  it.each([
    ["info", "Information", "status"],
    ["warning", "Warning", "alert"],
    ["critical", "Critical", "alert"],
  ])("conveys %s severity as text, not colour alone", (severity, text, role) => {
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "a",
      blocks: [
        { component: "Alert", props: { severity, title: "Recorded", body: "Observed." } },
      ],
    } as unknown as UISpec;
    const { container } = renderSpec(spec);
    expect(container.querySelector(".alert-severity")?.textContent).toBe(text);
    expect(container.querySelector(`[role="${role}"]`)).not.toBeNull();
  });
});

describe("determinism and non-mutation", () => {
  it("produces identical markup for the same approved input", () => {
    const first = renderSpec(catalogue).container.innerHTML;
    const second = renderSpec(catalogue).container.innerHTML;
    expect(first).toBe(second);
  });

  it("leaves the input unchanged after rendering and after an action", () => {
    const before = structuredClone(catalogue);
    const onAction = vi.fn();
    renderSpec(catalogue, onAction);
    for (const button of screen.getAllByRole("button")) button.click();
    expect(onAction.mock.calls.length).toBeGreaterThan(0);
    expect(catalogue).toEqual(before);
  });

  it("does not mutate a frozen spec", () => {
    const frozen = Object.freeze(structuredClone(demoSpec)) as UISpec;
    expect(() => renderSpec(frozen)).not.toThrow();
  });
});

describe("validated fixture traverses the whole path", () => {
  it("renders the representative demo fixture end to end", () => {
    const { container } = renderSpec(demoSpec);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe(
      "Board inspection activity",
    );
    expect(container.textContent).toContain("Explore recorded inspection activity.");
    expect(screen.getByRole("button", { name: "Open defect reports" })).toBeDefined();
  });
});
