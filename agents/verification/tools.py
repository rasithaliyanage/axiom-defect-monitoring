"""The one tool the verification agent may call.

Engineering-time only. Nothing here is imported by the application runtime.

The commands are owned by this file and are never built from model output. Each
is a fixed argv list run with `shell=False` and a bounded timeout, so there is
no string a model could produce that becomes a different command. The agent
chooses *whether* to verify; it cannot choose *what* gets run.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / "apps" / "ui"

#: The Python interpreter that owns this repository's virtual environment.
VENV_PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

#: npm is a shim on Windows; resolved statically, never from input.
NPM = "npm.cmd" if sys.platform == "win32" else "npm"

Status = Literal["pass", "fail", "error"]


@dataclass(frozen=True)
class Command:
    """One fixed verification command. No field is ever model-supplied."""

    key: str
    argv: tuple[str, ...]
    cwd: Path
    timeout: int
    describes: str


def _python() -> str:
    return str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def _pytest_basetemp() -> str:
    """A short, writable scratch root for pytest's `tmp_path`.

    `.claude/skills/verify-project/SKILL.md` records why this is needed: under a
    sandboxed shell the default location can refuse creation (PermissionError),
    and a long prefix can push a nested fixture past Windows' 260-character
    MAX_PATH. Both surface as errors that look like test failures but are not.
    The documented workaround is to point --basetemp somewhere short and
    writable, so the tool does exactly that rather than reporting a false
    negative. The path is computed here and never comes from a model.
    """
    root = Path(tempfile.gettempdir()) / "bdi-verify"
    root.mkdir(parents=True, exist_ok=True)
    return str(root)


def commands() -> tuple[Command, ...]:
    """The project's existing verification procedure, as argv.

    These mirror what `.claude/skills/verify-project/SKILL.md` documents, so
    the agent and a human run the same checks rather than two philosophies.

    `safety_lint` is here because without it the agent could report VERIFIED on
    a tree containing `eval()` or `dangerouslySetInnerHTML` under `apps/ui/src`:
    `scripts/safety-lint.mjs` runs only via `npm run lint`, and it is the
    mechanical enforcement of CLAUDE.md rule 2. A verification verdict that
    skips it means less than it sounds.

    `npm run typecheck` is covered transitively — `build` is
    `prepare:fixtures && tsc --noEmit && vite build`.
    """
    return (
        Command("python_tests",
                (_python(), "-m", "pytest", "-q", "--basetemp", _pytest_basetemp()),
                ROOT, 900, "Python suite: validator, API, hooks, plugin, agents"),
        Command("react_tests", (NPM, "test", "--silent"), UI, 900,
                "React suite via Vitest"),
        Command("schema_validation",
                (_python(), "-m", "pytest", "-q", "--basetemp", _pytest_basetemp(),
                 "tests/validator/test_task4_fixtures.py",
                 "tests/validator/test_fallback_spec.py"),
                ROOT, 300, "UI specification schema and fixture validation"),
        Command("safety_lint", (NPM, "run", "lint", "--silent"), UI, 300,
                "Render-path safety scan — CLAUDE.md rule 2"),
        Command("react_build", (NPM, "run", "build", "--silent"), UI, 900,
                "React production build"),
    )


@dataclass
class CheckResult:
    status: Status
    detail: str
    exit_code: int | None = None


@dataclass
class VerificationResult:
    """Deterministic, machine-readable. The agent reasons over this, not prose."""

    status: Status
    summary: str
    checks: dict[str, CheckResult] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "summary": self.summary,
            "checks": {k: {"status": v.status, "detail": v.detail,
                           "exit_code": v.exit_code} for k, v in self.checks.items()},
            "counts": dict(self.counts),
        }


CommandRunner = Callable[[Command], CheckResult]


def run_command(command: Command) -> CheckResult:
    """Execute one fixed command. shell=False, bounded, no shell metacharacters.

    `subprocess.run` with a list and `shell=False` passes argv straight to the
    OS: no shell parses it, so quoting and metacharacters have no meaning.
    """
    try:
        completed = subprocess.run(
            list(command.argv),
            cwd=str(command.cwd),
            capture_output=True,
            text=True,
            timeout=command.timeout,
            shell=False,
            check=False,
        )
    except FileNotFoundError:
        return CheckResult("error", f"{command.argv[0]} not found", None)
    except subprocess.TimeoutExpired:
        return CheckResult("error", f"timed out after {command.timeout}s", None)
    except OSError as exc:  # pragma: no cover - platform-specific
        return CheckResult("error", f"{type(exc).__name__}", None)

    tail = (completed.stdout or completed.stderr or "").strip().splitlines()
    detail = tail[-1][:300] if tail else "(no output)"
    return CheckResult("pass" if completed.returncode == 0 else "fail",
                       detail, completed.returncode)


def _counts(checks: dict[str, CheckResult]) -> dict[str, int]:
    return {
        "total": len(checks),
        "passed": sum(1 for c in checks.values() if c.status == "pass"),
        "failed": sum(1 for c in checks.values() if c.status == "fail"),
        "errored": sum(1 for c in checks.values() if c.status == "error"),
    }


def verify_project(runner: CommandRunner | None = None) -> VerificationResult:
    """Run the project's verification suites and report what actually happened.

    `runner` exists so deterministic tests can drive every outcome without
    spending minutes on real suites. It is a test seam, not a way for a caller
    to substitute different commands: the commands come from `commands()`.
    """
    execute = runner or run_command
    checks: dict[str, CheckResult] = {}

    for command in commands():
        checks[command.key] = execute(command)

    counts = _counts(checks)
    if counts["errored"]:
        status: Status = "error"
        summary = f"{counts['errored']} of {counts['total']} checks could not run"
    elif counts["failed"]:
        status = "fail"
        summary = f"{counts['failed']} of {counts['total']} checks failed"
    else:
        status = "pass"
        summary = f"all {counts['total']} checks passed"

    return VerificationResult(status=status, summary=summary, checks=checks, counts=counts)


def verify_project_json(runner: CommandRunner | None = None) -> str:
    return json.dumps(verify_project(runner).to_dict(), indent=2, sort_keys=True)
