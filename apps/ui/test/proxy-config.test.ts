/**
 * Guards the dev-server proxy configuration.
 *
 * Why this is worth a test: when `/health` was missing from the proxy, the dev
 * server answered it with the SPA shell — HTTP 200 and HTML. A liveness check
 * against `localhost:5173/health` therefore *appeared* to succeed while never
 * reaching the Domain Runtime. A silent false-pass is exactly the kind of
 * regression a config file will not announce.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const TEST_DIR = dirname(fileURLToPath(import.meta.url));
const RAW = readFileSync(resolve(TEST_DIR, "../vite.config.ts"), "utf8");

/** Comments explain why CORS is absent, so scan the code rather than the prose. */
const CONFIG = RAW.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^[ \t]*\/\/.*$/gm, "");

const TARGET = "http://127.0.0.1:8000";

describe("dev server proxy", () => {
  it.each(["/api", "/health"])("forwards %s to the Domain Runtime", (prefix) => {
    const entry = new RegExp(`"${prefix}":\\s*\\{[^}]*target:\\s*"${TARGET}"`, "s");
    expect(CONFIG).toMatch(entry);
  });

  it("adds no CORS configuration, because the proxy makes requests same-origin", () => {
    expect(CONFIG).not.toMatch(/cors/i);
    expect(CONFIG).not.toContain("Access-Control-Allow-Origin");
  });

  it("uses no wildcard proxy target", () => {
    expect(CONFIG).not.toContain('"*"');
    expect(CONFIG).not.toMatch(/target:\s*"https?:\/\/\*/);
  });
});
