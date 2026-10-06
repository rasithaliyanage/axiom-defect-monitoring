/**
 * DOM safety. Model-like strings must never become markup, attributes, event
 * handlers or executable behaviour.
 *
 * The malformed inputs below are renderer-boundary probes. They are test-only
 * and are not a production bypass: nothing in `src/` accepts raw model output.
 */

import { render, screen } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it, vi } from "vitest";

/** Resolved once at module scope so every source scan uses the same base. */
const TEST_DIR = dirname(fileURLToPath(import.meta.url));

function readSource(relative: string): string {
  return readFileSync(resolve(TEST_DIR, relative), "utf8");
}

import { UISpecRenderer } from "../src/renderer/renderUISpec";
import type { Block, UISpec } from "../src/renderer/types";
import { approveForTest } from "./support/approve";

const labels = { "view-defect-reports": "Open defect reports" } as const;

function renderSpec(spec: UISpec) {
  return render(<UISpecRenderer spec={approveForTest(spec)} options={{ actionLabels: labels }} />);
}

function textSpec(text: string): UISpec {
  return {
    specVersion: "1.0",
    page: "landing",
    contextId: "probe",
    blocks: [{ component: "Text", props: { text } }],
  } as UISpec;
}

describe("model-like strings cannot execute or inject", () => {
  const payloads = [
    "<script>window.__pwned = true;</script>",
    "<img src=x onerror=\"window.__pwned = true\">",
    "javascript:window.__pwned=true",
    "${constructor.constructor('return 1')()}",
    "<b>bold</b> and <i>italic</i>",
    "{{ 7 * 7 }}",
  ];

  it.each(payloads)("renders %s as literal text", (payload) => {
    const { container } = renderSpec(textSpec(payload));

    const paragraph = container.querySelector(".text");
    expect(paragraph?.textContent).toBe(payload);
    // Escaped, so no element was created from the payload.
    expect(container.querySelector("script")).toBeNull();
    expect(container.querySelector("img")).toBeNull();
    expect(paragraph?.children).toHaveLength(0);
    expect((globalThis as Record<string, unknown>)["__pwned"]).toBeUndefined();
  });

  it("does not create an executable handler from a string", () => {
    const { container } = renderSpec(textSpec("onclick=alert(1)"));
    const paragraph = container.querySelector(".text");
    expect(paragraph?.getAttribute("onclick")).toBeNull();
    expect(paragraph?.textContent).toBe("onclick=alert(1)");
  });
});

describe("unknown props cannot reach the DOM", () => {
  it("ignores props outside the approved set", () => {
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "probe",
      blocks: [
        {
          component: "Text",
          props: {
            text: "Rendered.",
            onClick: "alert(1)",
            style: "color:red",
            href: "https://example.internal",
            dangerouslySetInnerHTML: { __html: "<b>x</b>" },
            "data-evil": "1",
            className: "injected",
          },
        },
      ] as unknown as Block[],
    } as UISpec;

    const { container } = renderSpec(spec);
    const paragraph = container.querySelector("p.text");

    expect(paragraph?.textContent).toBe("Rendered.");
    expect(paragraph?.getAttribute("style")).toBeNull();
    expect(paragraph?.getAttribute("href")).toBeNull();
    expect(paragraph?.getAttribute("data-evil")).toBeNull();
    expect(paragraph?.getAttribute("onclick")).toBeNull();
    expect(paragraph?.className).toBe("text");
    expect(container.querySelector("b")).toBeNull();
  });

  it("ignores an unapproved prop on a component with a closed enum", () => {
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "probe",
      blocks: [
        {
          component: "Alert",
          props: {
            severity: "warning",
            title: "Recorded",
            body: "Observed.",
            severityClass: "alert-critical-injected",
          },
        },
      ] as unknown as Block[],
    } as UISpec;

    const { container } = renderSpec(spec);
    expect(container.querySelector(".alert")?.className).toBe("alert alert-warning");
  });
});

describe("no dynamic execution mechanism exists in the render path", () => {
  const sources = [
    "../src/renderer/renderUISpec.tsx",
    "../src/renderer/registry.ts",
    "../src/renderer/types.ts",
    "../src/components/approved.tsx",
  ];

  const forbidden = [
    "dangerouslySetInnerHTML",
    "eval(",
    "new Function",
    "innerHTML",
    "insertAdjacentHTML",
    "document.write",
  ];

  it.each(sources)("%s contains no dynamic execution mechanism", (relative) => {
    // Strip comments so prose naming a mechanism does not fail the scan.
    const code = readSource(relative)
      .replace(/\/\*[\s\S]*?\*\//g, "")
      .replace(/^[ \t]*\/\/.*$/gm, "");
    for (const token of forbidden) {
      expect(code).not.toContain(token);
    }
  });

  it.each(sources)("%s contains no dynamic import", (relative) => {
    const code = readSource(relative)
      .replace(/\/\*[\s\S]*?\*\//g, "")
      .replace(/^[ \t]*\/\/.*$/gm, "");
    expect(code).not.toMatch(/\bimport\s*\(/);
  });
});

describe("action handling stays developer-owned", () => {
  it("records the identifier without navigating or fetching", () => {
    const onAction = vi.fn();
    const fetchSpy = vi.spyOn(globalThis, "fetch" as never);
    const spec = {
      specVersion: "1.0",
      page: "landing",
      contextId: "probe",
      blocks: [
        {
          component: "CTA",
          props: { label: "Open defect reports", action: "view-defect-reports" },
        },
      ],
    } as UISpec;

    render(
      <UISpecRenderer spec={approveForTest(spec)} options={{ actionLabels: labels, onAction }} />,
    );
    screen.getByRole("button", { name: "Open defect reports" }).click();

    expect(onAction).toHaveBeenCalledWith("view-defect-reports");
    expect(fetchSpy).not.toHaveBeenCalled();
    expect(globalThis.location.href).not.toContain("view-defect-reports");
  });
});
