/** Task 6: React consumption of the Domain Runtime, and the transport boundary. */

import { render, screen, waitFor } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";

/** Resolved once at module scope; `import.meta.url` is unreliable inside callbacks here. */
const TEST_DIR = dirname(fileURLToPath(import.meta.url));

import { App } from "../src/App";
import { INITIAL_CONTEXT, LANDING_PAGE_PATH, fetchLandingPage } from "../src/api/client";
import { acceptLandingResponse } from "../src/renderer/approved";

import catalogueSpec from "../../../tests/fixtures/ui-spec/full-catalogue.spec.json";
import catalogueContext from "../../../tests/fixtures/ui-spec/full-catalogue.context.json";

/** A response shaped exactly as the Domain Runtime returns one. */
function domainResponse(overrides: Record<string, unknown> = {}) {
  const actionLabels = Object.fromEntries(
    (catalogueContext as { actions: { id: string; label: string }[] }).actions.map((a) => [
      a.id,
      a.label,
    ]),
  );
  return {
    spec: catalogueSpec,
    bindings: { actionLabels },
    meta: { contextId: (catalogueSpec as { contextId: string }).contextId, source: "fixture", validation: "VALID" },
    ...overrides,
  };
}

function mockFetch(impl: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>) {
  return vi.spyOn(globalThis, "fetch").mockImplementation(impl as typeof fetch);
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("API client", () => {
  it("POSTs a presentation-only request to the agreed path", async () => {
    const spy = mockFetch(async () => jsonResponse(domainResponse()));
    await fetchLandingPage({ view: "overview" });

    expect(spy).toHaveBeenCalledTimes(1);
    const [url, init] = spy.mock.calls[0] ?? [];
    expect(url).toBe(LANDING_PAGE_PATH);
    expect(init?.method).toBe("POST");
    expect(JSON.parse(String(init?.body))).toEqual({
      page: "landing",
      view: "overview",
      locale: "en-US",
    });
  });

  it("sends the developer-owned INITIAL_CONTEXT, with no input path into it", async () => {
    const spy = mockFetch(async () => jsonResponse(domainResponse()));
    await fetchLandingPage();

    const body = JSON.parse(String(spy.mock.calls[0]?.[1]?.body));
    expect(body).toEqual({ ...INITIAL_CONTEXT });
    // No query string, no path segment: the URL is a module constant.
    expect(String(spy.mock.calls[0]?.[0])).toBe(LANDING_PAGE_PATH);
    expect(String(spy.mock.calls[0]?.[0])).not.toContain("?");
  });

  it("snapshots the request before awaiting, so later mutation cannot change it", async () => {
    const spy = mockFetch(async () => jsonResponse(domainResponse()));
    const options = { view: "minimal" as const };
    const pending = fetchLandingPage(options);
    // Mutating the caller's object after the call must not affect the request.
    (options as { view: string }).view = "overview";
    await pending;

    expect(JSON.parse(String(spy.mock.calls[0]?.[1]?.body)).view).toBe("minimal");
  });

  it("reports HTTP failure rather than throwing", async () => {
    mockFetch(async () => jsonResponse({ error: { code: "BAD_REQUEST", message: "no" } }, 400));
    const result = await fetchLandingPage();
    expect(result.ok).toBe(false);
  });

  it("reports a network failure", async () => {
    mockFetch(async () => {
      throw new TypeError("Failed to fetch");
    });
    const result = await fetchLandingPage();
    expect(result).toMatchObject({ ok: false });
  });

  it("reports invalid JSON", async () => {
    mockFetch(async () => new Response("not json", { status: 200 }));
    const result = await fetchLandingPage();
    expect(result).toMatchObject({ ok: false, reason: "Response was not valid JSON" });
  });
});

describe("transport adapter rejects unusable responses whole", () => {
  const cases: [string, unknown][] = [
    ["not an object", 42],
    ["no spec", { bindings: { actionLabels: {} }, meta: {} }],
    ["wrong specVersion", domainResponse({ spec: { ...catalogueSpec, specVersion: "0.9" } })],
    ["wrong page", domainResponse({ spec: { ...catalogueSpec, page: "inspection" } })],
    ["no blocks", domainResponse({ spec: { ...catalogueSpec, blocks: [] } })],
    [
      "metadata contextId mismatch",
      domainResponse({ meta: { contextId: "other", source: "fixture", validation: "VALID" } }),
    ],
    ["missing bindings", domainResponse({ bindings: undefined })],
  ];

  it.each(cases)("rejects when %s", (_label, payload) => {
    expect(acceptLandingResponse(payload).ok).toBe(false);
  });

  it("rejects the WHOLE response when any block names an unapproved component", () => {
    const payload = domainResponse({
      spec: {
        ...catalogueSpec,
        blocks: [
          ...(catalogueSpec as { blocks: unknown[] }).blocks,
          { component: "DispositionControl", props: { label: "Mark" } },
        ],
      },
    });
    const result = acceptLandingResponse(payload);
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.reason).toContain("Unapproved component");
  });

  it("accepts a well-formed response and issues a handle", () => {
    const result = acceptLandingResponse(domainResponse());
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.contextId).toBe("task4-catalogue");
      expect(Object.keys(result.actionLabels)).toHaveLength(5);
    }
  });

  it("does not trust meta.validation as proof", () => {
    // A forged VALID on an otherwise unusable body still fails.
    const forged = { spec: { specVersion: "1.0" }, bindings: {}, meta: { validation: "VALID" } };
    expect(acceptLandingResponse(forged).ok).toBe(false);
  });
});

describe("application states", () => {
  it("shows a loading state before the response arrives", async () => {
    let release: (r: Response) => void = () => undefined;
    mockFetch(() => new Promise<Response>((resolve) => (release = resolve)));

    render(<App />);
    expect(screen.getByRole("status").textContent).toContain("Loading");

    release(jsonResponse(domainResponse()));
    await waitFor(() => expect(screen.queryByRole("status")).toBeNull());
  });

  it("renders the page from the API response", async () => {
    mockFetch(async () => jsonResponse(domainResponse()));
    const { container } = render(<App />);

    await waitFor(() =>
      expect(screen.getByRole("heading", { level: 1 }).textContent).toBe(
        "Board inspection activity",
      ),
    );
    expect(container.querySelectorAll(".uispec-block")).toHaveLength(
      (catalogueSpec as { blocks: unknown[] }).blocks.length,
    );
    expect(container.querySelector(".notice-evidence")?.textContent).toContain("Domain Runtime");
  });

  it("shows a controlled error and no page when the backend is unavailable", async () => {
    mockFetch(async () => {
      throw new TypeError("Failed to fetch");
    });
    const { container } = render(<App />);

    await waitFor(() => expect(screen.getByRole("alert")).toBeDefined());
    expect(screen.getByRole("alert").textContent).toContain("could not be loaded");
    // No silent fallback to the static fixture.
    expect(container.querySelector(".uispec-page")).toBeNull();
    expect(container.querySelectorAll(".uispec-block")).toHaveLength(0);
  });

  it("shows the error state on an unusable response shape", async () => {
    mockFetch(async () => jsonResponse({ unexpected: true }));
    const { container } = render(<App />);
    await waitFor(() => expect(screen.getByRole("alert")).toBeDefined());
    expect(container.querySelector(".uispec-page")).toBeNull();
  });

  it("keeps actions inert after loading from the API", async () => {
    mockFetch(async () => jsonResponse(domainResponse()));
    const onAction = vi.fn();
    render(<App onAction={onAction} />);

    await waitFor(() => expect(screen.getAllByRole("button").length).toBeGreaterThan(0));
    const before = globalThis.location.href;
    for (const button of screen.getAllByRole("button")) button.click();

    expect(onAction).toHaveBeenCalled();
    expect(globalThis.location.href).toBe(before);
  });

  it("ignores a stale response after unmount", async () => {
    let release: (r: Response) => void = () => undefined;
    mockFetch(() => new Promise<Response>((resolve) => (release = resolve)));

    const { unmount, container } = render(<App />);
    unmount();
    release(jsonResponse(domainResponse()));

    await new Promise((resolve) => setTimeout(resolve, 10));
    expect(container.querySelector(".uispec-page")).toBeNull();
  });
});

describe("the application does not bypass the controlled renderer", () => {
  it("never resolves components itself", () => {
    const source = readFileSync(resolve(TEST_DIR, "../src/App.tsx"), "utf8");
    expect(source).not.toContain("componentRegistry");
    expect(source).not.toContain("createElement");
    expect(source).toContain("UISpecRenderer");
  });

  it("keeps the API client free of component resolution", () => {
    const source = readFileSync(resolve(TEST_DIR, "../src/api/client.ts"), "utf8");
    expect(source).not.toContain("componentRegistry");
    expect(source).not.toContain("createElement");
  });
});
