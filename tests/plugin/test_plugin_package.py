"""Structural checks for the Claude Code plugin package.

The package under `plugin/` is a **mirror**, not a second implementation. The
authoritative skills and hook live in `.claude/`; `scripts/package_plugin.py`
copies them. These tests are what make that claim enforceable rather than
aspirational: if a copy drifts from its source, the suite fails.

They verify structure and provenance. They do not prove that Claude Code
discovers or installs the plugin — see `plugin/README.md` for what was and was
not observed.
"""

from __future__ import annotations

import filecmp
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugin" / "board-defect-inspection-engineering"
MANIFEST = PLUGIN / ".claude-plugin" / "plugin.json"
SKILLS = ("verify-project", "review-uispec", "checkpoint-review")


# --- manifest ----------------------------------------------------------------

def test_manifest_exists_at_the_documented_location():
    """The plugin model looks for .claude-plugin/plugin.json at the plugin root."""
    assert MANIFEST.is_file()


def test_manifest_is_valid_json():
    json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.mark.parametrize("field", ["name", "description", "version"])
def test_manifest_carries_the_required_fields(field):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert field in manifest and manifest[field]


def test_manifest_declares_no_unsupported_field():
    """Fields observed across the installed first-party plugins, and no others."""
    known = {"name", "description", "version", "author", "keywords",
             "license", "homepage", "repository", "userConfig"}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert set(manifest) <= known, f"unknown: {set(manifest) - known}"


def test_manifest_name_is_a_plain_slug():
    name = json.loads(MANIFEST.read_text(encoding="utf-8"))["name"]
    assert name == name.lower()
    assert " " not in name and "/" not in name


def test_description_does_not_claim_to_be_a_runtime_component():
    """BR-3 discipline applied to our own packaging copy."""
    text = json.loads(MANIFEST.read_text(encoding="utf-8"))["description"].lower()
    assert "engineering-time" in text
    for overclaim in ("inference", "model gateway", "classif", "runtime ai"):
        if overclaim in text:
            assert "no model inference" in text or "not part of the application runtime" in text


# --- the mirror is a mirror ---------------------------------------------------

@pytest.mark.parametrize("skill", SKILLS)
def test_packaged_skill_is_byte_identical_to_its_source(skill):
    """The whole point. A divergent copy is the failure this prevents."""
    src = ROOT / ".claude" / "skills" / skill
    dst = PLUGIN / "skills" / skill
    assert dst.is_dir(), f"{skill} is not packaged"
    for source_file in sorted(src.rglob("*.md")):
        packaged = dst / source_file.relative_to(src)
        assert packaged.is_file(), f"missing from package: {packaged.relative_to(ROOT)}"
        assert filecmp.cmp(source_file, packaged, shallow=False), (
            f"{packaged.relative_to(ROOT)} has drifted from "
            f"{source_file.relative_to(ROOT)}"
        )


def test_packaged_hook_is_byte_identical_to_its_source():
    src = ROOT / ".claude" / "hooks" / "check_uispec_schema.py"
    dst = PLUGIN / "hooks" / "check_uispec_schema.py"
    assert filecmp.cmp(src, dst, shallow=False), "packaged hook has drifted"


def test_the_packaging_script_agrees_that_the_package_is_current():
    """Runs the generator's own --check; the single command a reviewer needs."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "package_plugin.py"), "--check"],
        capture_output=True, text=True, timeout=120, cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_package_contains_no_file_without_a_source():
    """An orphan means a capability was added to the package, not to .claude/."""
    authored = {PLUGIN / "hooks" / "hooks.json"}
    for packaged in (PLUGIN / "skills").rglob("*"):
        if not packaged.is_file():
            continue
        source = ROOT / ".claude" / "skills" / packaged.relative_to(PLUGIN / "skills")
        assert source.is_file(), f"no source for {packaged.relative_to(ROOT)}"
    for packaged in (PLUGIN / "hooks").iterdir():
        if packaged.is_file() and packaged not in authored:
            source = ROOT / ".claude" / "hooks" / packaged.name
            assert source.is_file(), f"no source for {packaged.relative_to(ROOT)}"


# --- scope: exactly what Task 8 and Task 9 built, nothing more ---------------

def test_exactly_the_three_existing_skills_are_packaged():
    packaged = sorted(p.name for p in (PLUGIN / "skills").iterdir() if p.is_dir())
    assert packaged == sorted(SKILLS)


def test_exactly_one_hook_is_packaged():
    scripts = [p for p in (PLUGIN / "hooks").iterdir()
               if p.is_file() and p.suffix == ".py"]
    assert len(scripts) == 1


def test_no_agent_mcp_or_command_was_added():
    for unexpected in ("agents", "commands", ".mcp.json", "mcp.json"):
        assert not (PLUGIN / unexpected).exists(), f"{unexpected} is out of scope"


# --- the packaged hook configuration -----------------------------------------

def test_packaged_hooks_json_is_valid_and_postooluse_only():
    config = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    assert list(config["hooks"]) == ["PostToolUse"], "PreToolUse is out of scope"
    groups = config["hooks"]["PostToolUse"]
    assert len(groups) == 1 and len(groups[0]["hooks"]) == 1


def test_packaged_hook_matcher_matches_the_project_configuration():
    packaged = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    project = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert (packaged["hooks"]["PostToolUse"][0]["matcher"]
            == project["hooks"]["PostToolUse"][0]["matcher"])


def test_packaged_hook_resolves_its_script_through_the_plugin_root():
    """A plugin must not assume where it was installed."""
    entry = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8")
                       )["hooks"]["PostToolUse"][0]["hooks"][0]
    assert "args" in entry, "exec form keeps a shell out of the path"
    assert entry["args"][0].startswith("${CLAUDE_PLUGIN_ROOT}/")


def test_packaged_hooks_json_does_not_claim_to_prevent_an_edit():
    text = (PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8").lower()
    assert "does not undo" in text


# --- security: the packaging introduced no new surface ------------------------

@pytest.mark.parametrize(
    "forbidden",
    ["subprocess", "os.system", "shlex", "eval(", "exec(", "__import__",
     "urllib", "requests", "httpx", "socket", "anthropic", "openai",
     "aiclient", "modelgateway", "git ", "getenv", "environ"],
)
def test_packaged_hook_introduces_no_dangerous_construct(forbidden):
    source = (PLUGIN / "hooks" / "check_uispec_schema.py").read_text(encoding="utf-8")
    body = source.split('"""', 2)[-1]  # executable part, docstring removed
    assert forbidden not in body.lower()


def test_no_secret_in_the_package():
    combined = "".join(
        p.read_text(encoding="utf-8", errors="ignore").lower()
        for p in PLUGIN.rglob("*") if p.is_file()
    )
    for token in ("api_key", "apikey", "password", "bearer ", "secret_key"):
        assert token not in combined


# --- the plugin is not runtime ------------------------------------------------

def test_no_runtime_code_imports_the_plugin():
    """Engineering-time packaging must not leak into the application."""
    for area in (ROOT / "services", ROOT / "apps" / "ui" / "src"):
        for source in area.rglob("*"):
            if source.is_file() and source.suffix in {".py", ".ts", ".tsx"}:
                assert "plugin/" not in source.read_text(encoding="utf-8", errors="ignore")


def test_plugin_package_lives_outside_every_runtime_directory():
    """A plugin root is identified by .claude-plugin/; none may sit under runtime code.

    Checks for the package itself, not for any directory called "plugin" --
    tests/plugin/ is this test suite and is expected.
    """
    for runtime in ("services", "apps", "specs"):
        found = list((ROOT / runtime).rglob(".claude-plugin"))
        assert not found, f"plugin package inside runtime tree: {found}"
    assert MANIFEST.parent.parent == PLUGIN
    assert PLUGIN.parent == ROOT / "plugin"


def test_readme_documents_the_source_of_truth():
    readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    assert ".claude/" in readme
    assert "scripts/package_plugin.py" in readme
