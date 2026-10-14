"""Deterministic tests for the engineering-time verification agent.

No Anthropic API key, no network, no live model, and no `claude-agent-sdk`
import. The loop takes a `Reasoner` protocol, so a scripted reasoner drives
every path including the ones a real model would reach only occasionally.

A note on what these prove. They pin the *loop's* allow-list and bounds, which
is the control that matters: the loop owns dispatch, so a reasoner — scripted
or live — cannot reach anything the allow-list refuses. They do not prove the
SDK's own permission layer behaves as documented; that is asserted structurally
in the SDK-boundary section and stated as a limit in `agents/README.md`.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

from agents.verification import (
    ALLOWED_TOOLS,
    Action,
    InvalidAction,
    Observation,
    Report,
    StopReason,
    Verdict,
    run_agent,
    validate,
)
from agents.verification.tools import (
    CheckResult,
    Command,
    commands,
    run_command,
    verify_project,
)

ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = ROOT / "agents"


# --- scripted reasoners: the test seam --------------------------------------

class Scripted:
    """Returns predetermined actions. Stands in for the model."""

    def __init__(self, *actions: Action) -> None:
        self.actions = list(actions)
        self.seen: list[list[Observation]] = []

    def next_action(self, request: str, history: list[Observation]) -> Action:
        self.seen.append(history)
        return self.actions.pop(0) if self.actions else Action("stop")


def runner_returning(status: str, detail: str = "scripted"):
    def run(command: Command) -> CheckResult:
        return CheckResult(status, f"{detail}:{command.key}", 0 if status == "pass" else 1)
    return run


VERIFY = Action("verify_project")


# --- the happy path ---------------------------------------------------------

def test_valid_action_runs_verification_and_reports_verified():
    report = run_agent("verify", Scripted(VERIFY), runner=runner_returning("pass"))
    assert report.stop_reason is StopReason.VERIFICATION_COMPLETE
    assert report.verdict is Verdict.VERIFIED
    assert len(report.turns) == 1
    assert report.turns[0].observation.status == "pass"


def test_report_is_structured_and_serialisable():
    report = run_agent("verify", Scripted(VERIFY), runner=runner_returning("pass"))
    body = report.to_dict()
    assert set(body) == {"request", "stop_reason", "verdict", "summary", "turns"}
    assert body["turns"][0]["action"]["tool"] == "verify_project"
    assert body["turns"][0]["observation"]["result"]["counts"]["passed"] == len(commands())


def test_observations_are_fed_back_to_the_reasoner():
    """The loop is a loop: the reasoner sees what happened."""
    reasoner = Scripted(VERIFY, Action("stop"))
    run_agent("verify", reasoner, max_iterations=2, runner=runner_returning("fail"))
    assert reasoner.seen[0] == []
    assert len(reasoner.seen) >= 1


# --- failure, error, and the honesty of the verdict -------------------------

def test_failed_verification_is_not_reported_as_success():
    report = run_agent("verify", Scripted(VERIFY), runner=runner_returning("fail"))
    assert report.verdict is Verdict.NOT_VERIFIED
    assert report.verdict is not Verdict.VERIFIED


def test_tool_error_stops_with_tool_error_and_is_not_verified():
    report = run_agent("verify", Scripted(VERIFY), runner=runner_returning("error"))
    assert report.stop_reason is StopReason.TOOL_ERROR
    assert report.verdict is Verdict.NOT_VERIFIED


def test_stopping_before_any_verification_is_inconclusive_not_verified():
    """An agent that never checked anything has not verified anything."""
    report = run_agent("verify", Scripted(Action("stop")))
    assert report.stop_reason is StopReason.INVALID_PROPOSAL
    assert report.verdict is Verdict.INCONCLUSIVE


# --- the allow-list ---------------------------------------------------------

def test_allow_list_contains_exactly_one_tool():
    assert ALLOWED_TOOLS == frozenset({"verify_project"})


@pytest.mark.parametrize(
    "tool",
    ["bash", "Bash", "Write", "Edit", "run_shell", "verify_project ",
     "VERIFY_PROJECT", "os.system", "__import__", "mcp__other__thing", ""],
)
def test_tools_outside_the_allow_list_are_refused(tool):
    with pytest.raises(InvalidAction):
        validate(Action(tool))


@pytest.mark.parametrize(
    "tool", ["rm -rf /", "python arbitrary_script.py", "; cat /etc/passwd", "$(whoami)"],
)
def test_shell_shaped_proposals_are_refused_as_tool_names(tool):
    """A model cannot smuggle a command through the tool field."""
    with pytest.raises(InvalidAction):
        validate(Action(tool))


def test_invalid_tool_stops_the_loop_before_dispatch():
    calls: list[str] = []

    def runner(command: Command) -> CheckResult:
        calls.append(command.key)
        return CheckResult("pass", "", 0)

    report = run_agent("verify", Scripted(Action("bash", {"cmd": "rm -rf /"})), runner=runner)
    assert report.stop_reason is StopReason.INVALID_PROPOSAL
    assert report.verdict is Verdict.INCONCLUSIVE
    assert calls == [], "a refused tool must never reach dispatch"


def test_rejected_tool_name_is_not_echoed_back():
    """The name is reasoner-supplied text; the error must not reflect it."""
    hostile = "<script>alert(1)</script>"
    with pytest.raises(InvalidAction) as raised:
        validate(Action(hostile))
    assert hostile not in str(raised.value)


def test_arguments_are_rejected_because_the_tool_takes_none():
    with pytest.raises(InvalidAction):
        validate(Action("verify_project", {"path": "/etc"}))
    with pytest.raises(InvalidAction):
        validate(Action("verify_project", "not-a-dict"))  # type: ignore[arg-type]


# --- bounds -----------------------------------------------------------------

def test_loop_stops_at_the_iteration_limit():
    class Forever:
        def next_action(self, request, history):
            return Action("verify_project")

    report = run_agent("verify", Forever(), max_iterations=2, runner=runner_returning("fail"))
    assert len(report.turns) <= 2


def test_iteration_limit_yields_inconclusive_when_nothing_concluded():
    class NeverValid:
        """Proposes a refused tool, so no verification ever runs."""
        def next_action(self, request, history):
            return Action("stop")

    report = run_agent("verify", NeverValid(), max_iterations=1)
    assert report.verdict is Verdict.INCONCLUSIVE


def test_max_iterations_must_be_at_least_one():
    with pytest.raises(ValueError):
        run_agent("verify", Scripted(VERIFY), max_iterations=0)


def test_default_iteration_bound_is_small():
    from agents.verification import DEFAULT_MAX_ITERATIONS
    assert 1 <= DEFAULT_MAX_ITERATIONS <= 10, "the loop must not be open-ended"


# --- the tool's own safety --------------------------------------------------

def test_every_command_is_an_argv_list_with_a_bounded_timeout():
    for command in commands():
        assert isinstance(command.argv, tuple) and len(command.argv) >= 2
        assert all(isinstance(part, str) for part in command.argv)
        assert 0 < command.timeout <= 900
        assert command.cwd.is_dir()


def test_no_command_contains_shell_metacharacters():
    for command in commands():
        for part in command.argv:
            for meta in (";", "&&", "||", "|", ">", "<", "`", "$(", "rm "):
                assert meta not in part, f"{command.key}: {part!r}"


def test_verification_result_is_machine_readable():
    body = verify_project(runner_returning("pass")).to_dict()
    assert body["status"] == "pass"
    assert set(body) == {"status", "summary", "checks", "counts"}
    n = len(commands())
    assert body["counts"] == {"total": n, "passed": n, "failed": 0, "errored": 0}


def test_the_required_checks_are_covered():
    keys = {c.key for c in commands()}
    assert {"python_tests", "react_tests", "schema_validation", "react_build"} <= keys


def test_the_render_path_safety_scan_is_part_of_verification():
    """Without it, VERIFIED would not mean the renderer is still safe.

    `scripts/safety-lint.mjs` enforces CLAUDE.md rule 2 and runs only through
    `npm run lint`. An agent that skips it could certify a tree containing
    eval() or dangerouslySetInnerHTML under apps/ui/src.
    """
    lint = next((c for c in commands() if c.key == "safety_lint"), None)
    assert lint is not None, "the agent must run the safety lint"
    assert lint.argv[1:3] == ("run", "lint")


def test_a_failing_safety_lint_alone_blocks_the_verdict():
    def only_lint_fails(command: Command) -> CheckResult:
        return CheckResult("fail" if command.key == "safety_lint" else "pass", "", 1)

    report = run_agent("verify", Scripted(VERIFY), runner=only_lint_fails)
    assert report.verdict is Verdict.NOT_VERIFIED


def test_a_single_failing_check_fails_the_whole_verification():
    def mixed(command: Command) -> CheckResult:
        return CheckResult("fail" if command.key == "react_build" else "pass", "", 1)

    result = verify_project(mixed)
    assert result.status == "fail"
    assert result.counts["failed"] == 1


# --- run_command: the error branches, exercised for real -------------------

def test_missing_executable_is_an_error_not_a_failure(tmp_path):
    """A tool that cannot run has not proved the project wrong.

    `error` and `fail` are different answers and the verdict treats them
    differently, so the distinction has to hold at the point it is produced.
    """
    missing = Command("probe", ("definitely-not-a-real-binary-xyz",), tmp_path, 10, "probe")
    result = run_command(missing)
    assert result.status == "error"
    assert result.exit_code is None
    assert "not found" in result.detail


def test_a_timeout_is_an_error_and_names_the_bound():
    """Bounded means bounded: a hanging command must not hang the agent."""
    slow = Command(
        "probe",
        (sys.executable, "-c", "import time; time.sleep(30)"),
        ROOT, 1, "deliberately slower than its timeout",
    )
    result = run_command(slow)
    assert result.status == "error"
    assert "timed out" in result.detail
    assert "1s" in result.detail


def test_a_nonzero_exit_is_a_failure_not_an_error():
    failing = Command("probe", (sys.executable, "-c", "raise SystemExit(3)"),
                      ROOT, 60, "exits non-zero")
    result = run_command(failing)
    assert result.status == "fail"
    assert result.exit_code == 3


def test_a_zero_exit_is_a_pass_and_keeps_the_last_output_line():
    ok = Command("probe", (sys.executable, "-c", "print('first'); print('last line')"),
                 ROOT, 60, "exits zero")
    result = run_command(ok)
    assert result.status == "pass"
    assert result.exit_code == 0
    assert result.detail == "last line"


def test_command_output_is_truncated_before_it_reaches_the_report():
    """Tool output crosses into a structured artifact; it must stay bounded."""
    noisy = Command("probe", (sys.executable, "-c", "print('x' * 5000)"), ROOT, 60, "noisy")
    assert len(run_command(noisy).detail) <= 300


def test_an_errored_check_makes_the_whole_verification_an_error():
    def one_errors(command: Command) -> CheckResult:
        return CheckResult("error" if command.key == "react_tests" else "pass", "", None)

    result = verify_project(one_errors)
    assert result.status == "error"
    assert result.counts["errored"] == 1


def test_error_outranks_failure_in_the_overall_status():
    """A run with both must not be reported as a mere failure."""
    def both(command: Command) -> CheckResult:
        if command.key == "react_tests":
            return CheckResult("error", "", None)
        if command.key == "react_build":
            return CheckResult("fail", "", 1)
        return CheckResult("pass", "", 0)

    assert verify_project(both).status == "error"


# --- security: static checks over the agent source --------------------------

SOURCES = {p: p.read_text(encoding="utf-8") for p in AGENT_DIR.rglob("*.py")}


def executable_source(text: str) -> str:
    """The code with every docstring removed.

    Prose that explains why a mechanism is banned must not trip the scan for
    that mechanism — `apps/ui/scripts/safety-lint.mjs` strips comments for the
    same reason. Splitting on the first triple-quote missed docstrings on
    nested functions, which made this check fail on its own documentation.
    """
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(ast.fix_missing_locations(tree))


EXECUTABLE = {p: executable_source(t) for p, t in SOURCES.items()}


def test_no_agent_source_uses_shell_true():
    for path, text in SOURCES.items():
        assert "shell=True" not in text, path


@pytest.mark.parametrize("forbidden", ["eval(", "exec(", "__import__(", "os.system", "popen"])
def test_no_dynamic_execution_in_agent_sources(forbidden):
    for path, body in EXECUTABLE.items():
        assert forbidden not in body, f"{path}: {forbidden}"


def test_the_dynamic_execution_scan_ignores_prose_but_not_code():
    """Non-vacuous: stripping docstrings must not stop the scan working."""
    newline = chr(10)
    prose = newline.join([
        "def f():",
        '    """Explains why eval( is banned."""',
        "    return 1",
    ])
    real = newline.join(["def f():", "    return eval('1')"])
    assert "eval(" not in executable_source(prose), "prose must not trip the scan"
    assert "eval(" in executable_source(real), "real code must still trip it"


def test_dispatch_uses_no_dynamic_tool_lookup():
    """A registry or getattr would make the allow-list advisory."""
    body = EXECUTABLE[AGENT_DIR / "verification" / "loop.py"]
    for dynamic in ("getattr(", "globals()", "locals()", "importlib", "TOOLS[", "registry"):
        assert dynamic not in body, dynamic


def test_dispatch_names_the_tool_literally():
    tree = ast.parse((AGENT_DIR / "verification" / "loop.py").read_text(encoding="utf-8"))
    dispatch = next(n for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef) and n.name == "dispatch")
    literals = [n.value for n in ast.walk(dispatch)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    assert "verify_project" in literals


def test_no_secret_or_env_access_in_agent_sources():
    for path, text in SOURCES.items():
        lowered = text.lower()
        for token in ("api_key", "apikey", "anthropic_api_key", "os.environ", "getenv", ".env"):
            assert token not in lowered, f"{path}: {token}"


def test_agent_makes_no_network_call_of_its_own():
    for path, text in SOURCES.items():
        for net in ("urllib", "requests", "httpx", "socket.", "http.client"):
            assert net not in text, f"{path}: {net}"


def test_no_git_automation_in_the_agent():
    for path, text in SOURCES.items():
        for git in ('"git"', "'git'", "git commit", "git push", "git merge"):
            assert git not in text, f"{path}: {git}"


# --- the SDK boundary -------------------------------------------------------

def test_loop_and_tools_do_not_import_the_sdk_at_all():
    for name in ("loop.py", "tools.py"):
        text = (AGENT_DIR / "verification" / name).read_text(encoding="utf-8")
        assert "claude_agent_sdk" not in text, name


def test_importing_the_agent_does_not_import_the_sdk():
    """Proven in a clean interpreter, not by inspecting this process."""
    probe = (
        "import sys; sys.path.insert(0, r'%s');"
        "import agents.verification;"
        "print('claude_agent_sdk' in sys.modules)" % ROOT
    )
    out = subprocess.run([sys.executable, "-c", probe], capture_output=True,
                         text=True, timeout=120, cwd=ROOT)
    assert out.stdout.strip() == "False", out.stdout + out.stderr


def test_sdk_module_imports_the_sdk_only_inside_functions():
    tree = ast.parse((AGENT_DIR / "verification" / "sdk.py").read_text(encoding="utf-8"))
    for node in tree.body:  # module level only
        assert not isinstance(node, (ast.Import, ast.ImportFrom)) or not any(
            "claude_agent_sdk" in (getattr(node, "module", "") or "")
            or any("claude_agent_sdk" in a.name for a in node.names)
            for _ in [0]
        ), "SDK must be imported lazily"


def test_sdk_boundary_does_not_rely_on_allowed_tools_alone():
    """allowed_tools auto-approves; it does not restrict. The bound is elsewhere."""
    text = (AGENT_DIR / "verification" / "sdk.py").read_text(encoding="utf-8")
    assert "tools=[]" in text, "built-in Claude Code tools must not be loaded"
    assert "can_use_tool" in text, "a deny-by-default callback must be configured"
    assert "max_turns" in text


def test_sdk_permission_callback_denies_anything_but_the_one_tool():
    text = (AGENT_DIR / "verification" / "sdk.py").read_text(encoding="utf-8")
    assert "PermissionResultDeny" in text
    assert "QUALIFIED_TOOL" in text


# --- runtime separation -----------------------------------------------------

def test_no_runtime_code_imports_the_agent_package():
    for area in (ROOT / "services", ROOT / "apps" / "ui" / "src"):
        for source in area.rglob("*"):
            if source.is_file() and source.suffix in {".py", ".ts", ".tsx"}:
                text = source.read_text(encoding="utf-8", errors="ignore")
                assert "agents.verification" not in text, source
                assert "claude_agent_sdk" not in text, source


def test_runtime_requirements_do_not_contain_the_agent_sdk():
    runtime = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
    assert "claude-agent-sdk" not in runtime
    assert "anthropic" not in runtime


def test_the_agent_sdk_is_a_development_dependency():
    dev = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").lower()
    assert "claude-agent-sdk" in dev


def test_agent_package_lives_outside_every_runtime_directory():
    for runtime in ("services", "apps", "specs"):
        assert not (ROOT / runtime / "agents").exists()
    assert AGENT_DIR.parent == ROOT
