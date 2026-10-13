"""Deterministic tests for the engineering-time UISpec schema hook.

Scope, stated up front because it is the easy thing to overclaim: these tests
exercise the hook **script** by piping it the payload shape Claude Code sends.
They do not prove Claude Code invokes it. That is a separate question, answered
(or not) in `.claude/hooks/README.md`.

Nothing here touches the real schema. The failure cases build a throwaway copy
of the repository skeleton in `tmp_path` and corrupt that.

Windows note: that copy nests several directories deep, so a long `--basetemp`
prefix can push the deepest fixture past the 260-character MAX_PATH limit and
the sandbox tests error with FileNotFoundError. It is a path-length failure,
not a hook failure. Run with a short basetemp, e.g. `--basetemp=C:/Temp/cch`.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude" / "hooks" / "check_uispec_schema.py"
SCHEMA = ROOT / "specs" / "schemas" / "ui-spec.schema.json"
SETTINGS = ROOT / ".claude" / "settings.json"


def run(hook: Path, payload: dict) -> subprocess.CompletedProcess[str]:
    """Pipe a payload to the hook exactly as Claude Code would."""
    return subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=120,
    )


def context_of(result: subprocess.CompletedProcess[str]) -> str:
    return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]


def edit_of(path: Path) -> dict:
    return {"tool_name": "Edit", "tool_input": {"file_path": str(path)}}


@pytest.fixture
def sandbox(tmp_path: Path) -> Path:
    """A throwaway repository skeleton whose schema may be corrupted freely."""
    for sub in ("specs/schemas", "tests/fixtures/ui-spec", ".claude/hooks"):
        (tmp_path / sub).mkdir(parents=True, exist_ok=True)
    shutil.copy(HOOK, tmp_path / ".claude/hooks/")
    shutil.copy(SCHEMA, tmp_path / "specs/schemas/")
    for fixture in (ROOT / "tests/fixtures/ui-spec").glob("*.json"):
        shutil.copy(fixture, tmp_path / "tests/fixtures/ui-spec")
    shutil.copytree(ROOT / "services", tmp_path / "services", dirs_exist_ok=True)
    return tmp_path


# --- A. a relevant edit triggers the check -----------------------------------

def test_schema_edit_triggers_the_check():
    result = run(HOOK, edit_of(SCHEMA))
    assert result.returncode == 0
    body = json.loads(result.stdout)
    assert body["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    assert "UISpec schema" in context_of(result)


def test_write_response_path_also_triggers_the_check():
    """Claude Code reports the path under tool_response for some tools."""
    payload = {"tool_name": "Write", "tool_response": {"filePath": str(SCHEMA)}}
    assert "UISpec schema" in context_of(run(HOOK, payload))


# --- B. an unrelated edit does not ------------------------------------------

@pytest.mark.parametrize(
    "path",
    [
        "README.md",
        "CLAUDE.md",
        "services/domain/validator.py",
        "specs/ui-spec.schema.json",       # the deprecated twin, deliberately not watched
        "specs/schemas/ui-spec.schema.json.bak",
    ],
)
def test_unrelated_edit_produces_no_output(path):
    """Exit cleanly and say nothing. A chatty hook trains people to ignore it."""
    result = run(HOOK, edit_of(ROOT / path))
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"tool_name": "Bash", "tool_input": {"command": "ls"}},
        {"tool_name": "Edit", "tool_input": {}},
        {"tool_name": "Edit", "tool_input": {"file_path": None}},
        {"tool_name": "Edit", "tool_input": {"file_path": ""}},
    ],
)
def test_payloads_without_a_relevant_path_are_ignored(payload):
    result = run(HOOK, payload)
    assert result.returncode == 0
    assert result.stdout == ""


def test_malformed_stdin_exits_cleanly():
    """A hook that crashes on junk is worse than no hook."""
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input="not json at all",
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0
    assert result.stdout == ""


# --- C. a valid schema reports success --------------------------------------

def test_valid_schema_reports_pass():
    context = context_of(run(HOOK, edit_of(SCHEMA)))
    assert context.startswith("PASS")
    assert "Draft202012Validator" in context
    assert "fixtures still validate" in context


# --- D. an invalid schema reports failure -----------------------------------

def test_unparseable_schema_reports_failure(sandbox):
    target = sandbox / "specs/schemas/ui-spec.schema.json"
    target.write_text('{"broken": ', encoding="utf-8")
    context = context_of(run(sandbox / ".claude/hooks/check_uispec_schema.py",
                             edit_of(target)))
    assert context.startswith("FAIL")
    assert "not valid JSON" in context
    assert "NOT modified" in context


def test_schema_that_is_not_a_legal_json_schema_reports_failure(sandbox):
    target = sandbox / "specs/schemas/ui-spec.schema.json"
    target.write_text(json.dumps(
        {"$schema": "https://json-schema.org/draft/2020-12/schema",
         "type": "not-a-real-type"}), encoding="utf-8")
    context = context_of(run(sandbox / ".claude/hooks/check_uispec_schema.py",
                             edit_of(target)))
    assert context.startswith("FAIL")
    assert "not a valid JSON Schema" in context


def test_failure_is_reported_without_a_nonzero_exit(sandbox):
    """Reported as information, not as a blocked tool call.

    The edit that broke the schema is usually mid-repair; blocking it would
    make the situation harder to fix, not safer.
    """
    target = sandbox / "specs/schemas/ui-spec.schema.json"
    target.write_text("{", encoding="utf-8")
    result = run(sandbox / ".claude/hooks/check_uispec_schema.py", edit_of(target))
    assert result.returncode == 0
    assert context_of(result).startswith("FAIL")


# --- E/F. the hook modifies nothing -----------------------------------------

def test_hook_does_not_modify_the_schema():
    before = hashlib.sha256(SCHEMA.read_bytes()).hexdigest()
    run(HOOK, edit_of(SCHEMA))
    assert hashlib.sha256(SCHEMA.read_bytes()).hexdigest() == before


def test_hook_does_not_repair_an_invalid_schema(sandbox):
    """Reporting a problem must never become silently fixing one."""
    target = sandbox / "specs/schemas/ui-spec.schema.json"
    broken = '{"deliberately": "broken"'
    target.write_text(broken, encoding="utf-8")
    run(sandbox / ".claude/hooks/check_uispec_schema.py", edit_of(target))
    assert target.read_text(encoding="utf-8") == broken


def test_hook_modifies_no_file_in_the_repository():
    tracked = sorted(
        p for p in (ROOT / "specs").rglob("*") if p.is_file()
    ) + sorted(p for p in (ROOT / "tests/fixtures").rglob("*") if p.is_file())
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    run(HOOK, edit_of(SCHEMA))
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    assert before == after


# --- G/H/I. the hook stays inside its boundaries ----------------------------

SOURCE = HOOK.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "forbidden",
    ["git commit", "git push", "git merge", "git add", "git reset",
     "subprocess", "os.system", "popen", "shutil.rmtree", "unlink"],
)
def test_hook_cannot_commit_push_or_delete(forbidden):
    """G. No git action and no process spawning anywhere in the hook."""
    assert forbidden.lower() not in SOURCE.lower()


@pytest.mark.parametrize(
    "forbidden",
    ["anthropic", "openai", "AiClient", "ModelGateway", "langchain",
     "urllib", "requests", "httpx", "socket"],
)
def test_hook_calls_no_model_and_opens_no_network(forbidden):
    """H. No AI SDK, no outbound call."""
    assert forbidden.lower() not in SOURCE.lower()


@pytest.mark.parametrize("forbidden", ["eval(", "exec(", "__import__", "compile("])
def test_hook_executes_nothing_derived_from_its_input(forbidden):
    """I. No arbitrary execution, model-derived or otherwise."""
    assert forbidden not in SOURCE


def test_hook_only_writes_to_stdout():
    """The single write in the hook is the JSON result."""
    assert SOURCE.count("write_text") == 0
    assert SOURCE.count("open(") == 0


def test_input_path_is_compared_never_opened():
    """A hostile path is inert: it is matched against one known location.

    The hook reads exactly one file, and that file is resolved from the hook's
    own location rather than from anything on stdin.
    """
    assert "SCHEMA.read_text" in SOURCE
    assert "Path(raw).resolve() == SCHEMA.resolve()" in SOURCE


@pytest.mark.parametrize(
    "hostile",
    [
        "; rm -rf /",
        "$(whoami)",
        "`id`",
        "a' || true; '",
        "../../../../etc/passwd",
        "C:\\Windows\\System32\\config\\SAM",
        "\x00truncated",
    ],
)
def test_hostile_paths_are_inert(hostile):
    """None of these is executed, opened, or echoed; none matches the schema."""
    result = run(HOOK, {"tool_name": "Edit", "tool_input": {"file_path": hostile}})
    assert result.returncode == 0
    assert result.stdout == ""
    assert hostile not in result.stderr


# --- the configuration itself ------------------------------------------------

def test_hook_is_registered_as_posttooluse_in_exec_form():
    """Exec form (`args`) spawns directly — no shell parses the path."""
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    groups = settings["hooks"]["PostToolUse"]
    entry = next(h for g in groups for h in g["hooks"] if h["type"] == "command")
    assert "args" in entry, "shell form would reintroduce an injection surface"
    assert entry["command"].endswith("python.exe")
    assert entry["args"][0].endswith("check_uispec_schema.py")


def test_settings_still_carry_the_existing_permission_block():
    """The hook was merged in, not written over the top of existing settings."""
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    assert set(settings["permissions"]) == {"allow", "ask", "deny"}


def test_no_secret_is_embedded_in_the_hook_or_its_configuration():
    combined = (SOURCE + SETTINGS.read_text(encoding="utf-8")).lower()
    for token in ("api_key", "apikey", "secret", "password", "token=", "bearer "):
        assert token not in combined
