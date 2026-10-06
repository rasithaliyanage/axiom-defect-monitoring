"""Offline fixture preparation gate.

Validates every developer-authored UISpec fixture against its matching synthetic
GroundedContext using the existing Task 3 validator, then emits the generated
TypeScript catalogue the browser application loads.

This is the ONLY way data becomes an approved fixture. There is no live
browser-to-Python validation transport: this runs offline, before dev, test and
build, and the application consumes only what it produced.

On any failure the generated output is deleted and the process exits non-zero,
so a stale catalogue can never survive a failed run.

Run from apps/ui:
    ../../.venv/Scripts/python.exe scripts/prepare_fixtures.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_DIR.parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "ui-spec"
OUTPUT = APP_DIR / "src" / "generated" / "fixtures.ts"

sys.path.insert(0, str(REPO_ROOT))

from services.domain.validator import SCHEMA_PATH, UISpecValidator  # noqa: E402

# Fixed catalogue. Adding a fixture is a deliberate edit here, never a directory
# scan, so an unreviewed file cannot reach the browser by being dropped in.
#
# Role mapping used by the application:
#   full-catalogue -> the browser overview page (all nine components, five actions)
#   task4-demo     -> the focused minimal page used by application tests
#   fallback       -> the deterministic fallback specification (TASK-005). It
#                     references no metric, alert, defect category, capability
#                     or action, so it validates against ANY grounded context.
CATALOGUE: tuple[str, ...] = ("full-catalogue", "task4-demo", "fallback")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str, kind: str) -> dict[str, object]:
    return json.loads((FIXTURE_DIR / f"{name}.{kind}.json").read_text(encoding="utf-8"))


def action_labels(context: dict[str, object]) -> dict[str, str]:
    """Action labels come from the validated context, never from the model."""
    actions = context.get("actions", [])
    assert isinstance(actions, list)
    labels: dict[str, str] = {}
    for action in actions:
        assert isinstance(action, dict)
        labels[str(action["id"])] = str(action["label"])
    return labels


def fail(message: str) -> None:
    OUTPUT.unlink(missing_ok=True)
    print(f"FIXTURE PREPARATION FAILED: {message}", file=sys.stderr)
    print("Generated catalogue removed. The application cannot load stale data.", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    validator = UISpecValidator()
    records: list[dict[str, object]] = []
    specs: dict[str, object] = {}
    labels: dict[str, dict[str, str]] = {}

    for name in CATALOGUE:
        spec_path = FIXTURE_DIR / f"{name}.spec.json"
        context_path = FIXTURE_DIR / f"{name}.context.json"
        if not spec_path.exists() or not context_path.exists():
            fail(f"{name}: missing spec or context file")

        spec = load(name, "spec")
        context = load(name, "context")

        if spec.get("contextId") != context.get("contextId"):
            fail(f"{name}: spec contextId does not match its context")

        result = validator.validate(spec, context)
        if result.status != "VALID":
            for rejection in result.rejections:
                print(f"  {rejection.gate} {rejection.code} {rejection.path}: {rejection.message}",
                      file=sys.stderr)
            fail(f"{name}: validator returned {result.status}")

        specs[name] = spec
        labels[name] = action_labels(context)
        records.append({
            "name": name,
            "contextId": spec["contextId"],
            "status": "VALID",
            "specSha256": sha256(spec_path),
            "contextSha256": sha256(context_path),
        })
        print(f"  VALID  {name}  contextId={spec['contextId']}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(records, specs, labels), encoding="utf-8")
    print(f"Prepared {len(CATALOGUE)} fixture(s) -> {OUTPUT.relative_to(APP_DIR)}")
    print(f"Structural authority: {SCHEMA_PATH.relative_to(REPO_ROOT)}")


def render(records: list[dict[str, object]],
           specs: dict[str, object],
           labels: dict[str, dict[str, str]]) -> str:
    def js(value: object) -> str:
        return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False)

    names = " | ".join(f'"{name}"' for name in CATALOGUE)
    return f'''// GENERATED FILE — DO NOT EDIT.
// Produced by apps/ui/scripts/prepare_fixtures.py.
// Every entry below was validated by services/domain/validator.py against its
// matching synthetic GroundedContext before this file was written. Editing it by
// hand breaks that guarantee, because nothing here is re-checked at runtime.
//
// Content is synthetic demonstration data. It is not a live production result.

import type {{ ActionLabels, UISpec }} from "../renderer/types";

export type FixtureName = {names};

export interface VerificationRecord {{
  readonly name: FixtureName;
  readonly contextId: string;
  readonly status: "VALID";
  readonly specSha256: string;
  readonly contextSha256: string;
}}

/** Evidence of the offline validation run that produced this file. */
export const VERIFICATION: readonly VerificationRecord[] = {js(records)} as const;

/** Action labels lifted from each validated context. Never model-authored. */
export const ACTION_LABELS: Readonly<Record<FixtureName, ActionLabels>> = {js(labels)};

/** Validated specifications, keyed by fixture name. */
export const FIXTURES: Readonly<Record<FixtureName, UISpec>> = {js(specs)} as unknown as Readonly<
  Record<FixtureName, UISpec>
>;
'''


if __name__ == "__main__":
    main()
