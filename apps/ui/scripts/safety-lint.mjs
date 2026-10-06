/**
 * Safety lint for the render path.
 *
 * Enforces the boundaries in CLAUDE.md rule 2 as a command, not a convention.
 * Implemented with the Node standard library so the check adds no dependency.
 *
 * Comments are stripped before scanning, so prose that names a prohibited
 * mechanism (the code that documents why it is banned) does not fail the check.
 */

import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const APP_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(APP_DIR, "src");

const FORBIDDEN = [
  { token: "dangerouslySetInnerHTML", why: "raw HTML injection" },
  { token: "eval(", why: "dynamic evaluation" },
  { token: "new Function", why: "dynamic function construction" },
  { token: "innerHTML", why: "raw HTML injection" },
  { token: "insertAdjacentHTML", why: "raw HTML injection" },
  { token: "document.write", why: "raw HTML injection" },
];

const FORBIDDEN_PATTERNS = [
  { re: /\bimport\s*\(/, why: "dynamic import (may be driven by model output)" },
  { re: /from\s+["'][^"']*\.\.\/\.\.\/test\//, why: "production code importing the test tree" },
  { re: /from\s+["']\.\.?\/.*\/approve["']/, why: "production code importing the test-only minting helper" },
];

function* walk(dir) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      yield* walk(full);
    } else if (/\.(ts|tsx)$/.test(entry)) {
      yield full;
    }
  }
}

function stripComments(source) {
  return source.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^[ \t]*\/\/.*$/gm, "");
}

let failures = 0;
let scanned = 0;

for (const file of walk(SRC)) {
  scanned += 1;
  const code = stripComments(readFileSync(file, "utf8"));
  const shown = relative(APP_DIR, file);

  for (const { token, why } of FORBIDDEN) {
    if (code.includes(token)) {
      console.error(`FAIL ${shown}: contains "${token}" — ${why}`);
      failures += 1;
    }
  }
  for (const { re, why } of FORBIDDEN_PATTERNS) {
    if (re.test(code)) {
      console.error(`FAIL ${shown}: matches ${re} — ${why}`);
      failures += 1;
    }
  }
}

// The generated catalogue must not be hand-maintained.
const generated = join(SRC, "generated", "fixtures.ts");
const header = readFileSync(generated, "utf8").slice(0, 200);
if (!header.includes("GENERATED FILE")) {
  console.error("FAIL src/generated/fixtures.ts: missing generated-file header");
  failures += 1;
}

if (failures > 0) {
  console.error(`\nsafety lint: ${failures} failure(s) across ${scanned} file(s)`);
  process.exit(1);
}

console.log(`safety lint: clean (${scanned} files, ${FORBIDDEN.length + FORBIDDEN_PATTERNS.length} rules)`);
