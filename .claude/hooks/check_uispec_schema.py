#!/usr/bin/env python3
"""PostToolUse hook: re-check the UI specification schema after it is edited.

Engineering-time guardrail. This is NOT the runtime validator and never
substitutes for it: `services/domain/validator.py` remains the authority, and
this hook only *invokes* it earlier, at the moment the schema changes, instead
of waiting for someone to remember to run the suite.

Security notes, because a hook is a program that runs automatically:

  * No shell. The hook is configured in exec form (`command` + `args`), so this
    script is spawned directly and nothing is parsed by a shell.
  * The file path on stdin is never executed, interpolated into a command, or
    opened. It is only *compared* against one known path resolved from this
    file's own location. A hostile path is therefore inert — at worst it fails
    to match and the hook exits silently.
  * Read-only. Nothing is written, repaired, formatted, staged or committed.
  * Offline. No network call, no model call, no credential read.

Exit codes: 0 always. A validation failure is reported through the hook's JSON
output rather than a non-zero exit.

PostToolUse fires after the tool call has already succeeded, so the file on
disk has changed before this hook runs. Nothing here undoes that edit, and no
exit code would: this is automatic post-action validation, surfaced to Claude
for corrective action. Preventing an action before it executes is what a
PreToolUse hook is for, and none exists in this repository.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_RELATIVE = Path("specs") / "schemas" / "ui-spec.schema.json"


def _repository_root() -> Path:
    """Find the repository by walking up until the schema is in view.

    Depth is not assumed. This file is copied into the plugin package, which
    nests it one level deeper than `.claude/hooks/`, and a fixed `parents[n]`
    silently resolves to the wrong directory there — the hook would then match
    nothing and quietly do nothing, which is the worst way for a check to fail.

    Falls back to the grandparent so SCHEMA is always a concrete path; when the
    schema genuinely is not there, nothing matches and the hook exits silently,
    which is the correct behaviour for an unrelated checkout.
    """
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / SCHEMA_RELATIVE).is_file():
            return candidate
    return here.parents[2] if len(here.parents) > 2 else here.parent


ROOT = _repository_root()
SCHEMA = ROOT / SCHEMA_RELATIVE
FIXTURES = ROOT / "tests" / "fixtures" / "ui-spec"


def emit(context: str) -> None:
    """Return a result to Claude Code and exit cleanly."""
    json.dump(
        {
            "suppressOutput": False,
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": context,
            },
        },
        sys.stdout,
    )
    sys.exit(0)


def touched_the_schema(payload: dict) -> bool:
    """Did this tool call affect the authoritative schema file?

    Compares resolved paths. The incoming value is treated as untrusted data:
    it is never opened and never reaches a shell.
    """
    candidates = [
        payload.get("tool_input", {}).get("file_path"),
        payload.get("tool_response", {}).get("filePath"),
    ]
    for raw in candidates:
        if not isinstance(raw, str) or not raw:
            continue
        try:
            if Path(raw).resolve() == SCHEMA.resolve():
                return True
        except (OSError, ValueError):
            # An unresolvable path simply is not our file.
            continue
    return False


def check() -> str:
    """Re-run the existing deterministic checks. Adds no second validator."""
    try:
        raw = SCHEMA.read_text(encoding="utf-8")
    except OSError as exc:
        return f"FAIL  UISpec schema unreadable: {type(exc).__name__}"

    try:
        schema = json.loads(raw)
    except json.JSONDecodeError as exc:
        return (
            f"FAIL  UISpec schema is not valid JSON: line {exc.lineno}, "
            f"column {exc.colno} — {exc.msg}. The schema was NOT modified; "
            "fix the syntax before relying on any validation result."
        )

    try:
        import jsonschema
    except ImportError:
        return (
            "SKIP  UISpec schema parses as JSON. Meta-validation and grounding "
            "were not run: jsonschema is unavailable to this interpreter."
        )

    try:
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
    except Exception as exc:  # noqa: BLE001 - any failure is a reportable result
        return (
            f"FAIL  UISpec schema is not a valid JSON Schema: "
            f"{type(exc).__name__}: {str(exc).splitlines()[0]}"
        )

    dialect = validator_cls.__name__

    # Reuse the authoritative validator rather than reimplementing it.
    sys.path.insert(0, str(ROOT))
    try:
        from services.domain.validator import UISpecValidator
    except Exception as exc:  # noqa: BLE001
        return (
            f"PARTIAL  UISpec schema parses and meta-validates ({dialect}). "
            f"The project validator could not be imported, so fixtures were "
            f"not checked: {type(exc).__name__}."
        )

    try:
        validator = UISpecValidator()
    except Exception as exc:  # noqa: BLE001
        return (
            f"FAIL  UISpec schema parses and meta-validates ({dialect}), but "
            f"the project validator refused to load it: {type(exc).__name__}: "
            f"{str(exc).splitlines()[0]}"
        )

    failures: list[str] = []
    checked = 0
    for spec_path in sorted(FIXTURES.glob("*.spec.json")):
        context_path = spec_path.with_name(
            spec_path.name.replace(".spec.json", ".context.json")
        )
        if not context_path.exists():
            continue
        checked += 1
        try:
            result = validator.validate(
                json.loads(spec_path.read_text(encoding="utf-8")),
                json.loads(context_path.read_text(encoding="utf-8")),
            )
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{spec_path.name}: {type(exc).__name__}")
            continue
        if result.status != "VALID":
            codes = sorted({r.code for r in result.rejections})
            failures.append(f"{spec_path.name}: {result.status} {codes}")

    if failures:
        return (
            f"FAIL  UISpec schema parses and meta-validates ({dialect}), but "
            f"{len(failures)} of {checked} canonical fixtures no longer "
            f"validate against it:\n  " + "\n  ".join(failures) + "\n"
            "The schema has NOT been changed by this hook. Either the schema "
            "edit was wrong, or the fixtures and model contract need the same "
            "change — CLAUDE.md requires contract, schema, tests and evals to "
            "move together."
        )

    return (
        f"PASS  UISpec schema parses, meta-validates as {dialect}, and all "
        f"{checked} canonical fixtures still validate against it."
    )


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        sys.exit(0)  # Not a payload we understand; stay out of the way.

    if not isinstance(payload, dict) or not touched_the_schema(payload):
        sys.exit(0)  # Unrelated edit. Do nothing, say nothing.

    emit(check())


if __name__ == "__main__":
    main()
