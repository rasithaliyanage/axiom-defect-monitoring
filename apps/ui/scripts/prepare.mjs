/**
 * Portable launcher for the offline fixture preparation gate.
 *
 * npm scripts run through cmd.exe on Windows and sh elsewhere, so a bare
 * relative interpreter path is not portable. This resolves the project virtual
 * environment first, falls back to a Python on PATH, and forwards the exit
 * code so a failed gate fails the npm script.
 */

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const APP_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const REPO_ROOT = resolve(APP_DIR, "..", "..");
const SCRIPT = join(APP_DIR, "scripts", "prepare_fixtures.py");

const candidates = [
  join(REPO_ROOT, ".venv", "Scripts", "python.exe"), // Windows venv
  join(REPO_ROOT, ".venv", "bin", "python3"), // POSIX venv
  join(REPO_ROOT, ".venv", "bin", "python"),
];

const interpreter = candidates.find((path) => existsSync(path));

function run(command, args) {
  return spawnSync(command, args, { stdio: "inherit", cwd: APP_DIR });
}

let result;
if (interpreter !== undefined) {
  result = run(interpreter, [SCRIPT]);
} else {
  // No project virtual environment. Try a Python on PATH before giving up.
  result = run("python3", [SCRIPT]);
  if (result.error !== undefined) {
    result = run("python", [SCRIPT]);
  }
}

if (result.error !== undefined) {
  console.error(
    "Could not run the fixture preparation gate: no usable Python interpreter found.\n" +
      "Create the project virtual environment at the repository root, or put Python on PATH.",
  );
  process.exit(1);
}

process.exit(result.status ?? 1);
