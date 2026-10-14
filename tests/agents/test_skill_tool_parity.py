"""The agent's verification must not drift from the Skill that defines it.

`.claude/skills/verify-project/SKILL.md` is the human-readable source of truth
for what verifying this project means. `agents/verification/tools.py` is the
programmatic one. Nothing but prose tied them together, and that is exactly how
`npm run lint` — the only path that runs the render-path safety scan, and so the
mechanical enforcement of CLAUDE.md rule 2 — was left out of the agent without
anyone noticing. The agent reported VERIFIED on a tree it had not safety-scanned.

So this file makes the tie mechanical, in the spirit of `.claude/rules/README.md`:

    "A rule that matters enough to be mechanical should become a test or a hook;
     until it does, it is a statement of intent that a reviewer still has to check."

The design that matters is **fail-closed on addition**. A command added to the
Skill and not to the tool fails here. A command deliberately not automated must
be named in EXEMPT with a reason — silence is not an option, which is the
property the old arrangement lacked.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from agents.verification.tools import commands

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".claude" / "skills" / "verify-project" / "SKILL.md"

#: Commands the Skill documents that the agent deliberately does not run.
#: Each needs a reason. Adding an entry is a decision; forgetting one is a failure.
EXEMPT: dict[str, str] = {
    "python -m pip check": (
        "Dependency consistency, not project correctness. It answers a question "
        "about the environment the agent is already running in, so a failure "
        "would not tell the agent anything about the repository."
    ),
    "npm run typecheck": (
        "Covered transitively: build is "
        "'prepare:fixtures && tsc --noEmit && vite build', so running it "
        "separately would execute tsc twice for the same signal."
    ),
}


def documented_commands() -> list[str]:
    """Every command in the Skill's run block, normalised.

    Parses the fenced bash block rather than matching loose prose, so a command
    mentioned in passing elsewhere in the Skill does not become a requirement.
    """
    text = SKILL.read_text(encoding="utf-8")
    blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
    assert blocks, "the Skill no longer has a fenced bash block to parse"

    found: list[str] = []
    for line in "\n".join(blocks).splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("cd "):
            continue
        # Collapse the interpreter path so the comparison is about the command.
        line = re.sub(r"^\S*python(\.exe)?\b", "python", line)
        found.append(re.sub(r"\s+", " ", line))
    return found


def tool_commands() -> list[str]:
    """The same, as the agent actually runs them."""
    normalised: list[str] = []
    for command in commands():
        argv = list(command.argv)
        head = "python" if "python" in Path(argv[0]).name.lower() else Path(argv[0]).stem
        normalised.append(re.sub(r"\s+", " ", " ".join([head, *argv[1:]])))
    return normalised


def covers(documented: str, actual: list[str]) -> bool:
    """Does some tool command run what this documented line asks for?

    Compared on the meaningful prefix — the tool legitimately adds flags the
    Skill does not spell out (`--silent`, the `--basetemp` workaround the Skill
    itself documents elsewhere), and narrows pytest to specific files for the
    schema check. What must match is the command being invoked.
    """
    tokens = documented.split()
    key = " ".join(tokens[: 4 if tokens[:2] == ["python", "-m"] else 3])
    return any(candidate.startswith(key) for candidate in actual)


# --- the parity contract ----------------------------------------------------

def test_the_skill_still_parses():
    documented = documented_commands()
    assert len(documented) >= 5, documented
    assert any("pytest" in c for c in documented)
    assert any("npm run lint" in c for c in documented)


@pytest.mark.parametrize("documented", documented_commands())
def test_every_documented_command_is_run_or_explicitly_exempt(documented):
    if any(documented.startswith(e) for e in EXEMPT):
        return
    assert covers(documented, tool_commands()), (
        f"The Skill documents '{documented}' but the agent does not run it.\n"
        f"Either add it to commands() in agents/verification/tools.py, or add it "
        f"to EXEMPT in this file with a reason. Do not delete this test."
    )


def test_every_exemption_still_corresponds_to_a_documented_command():
    """A stale exemption is drift in the other direction."""
    documented = documented_commands()
    for exempt in EXEMPT:
        assert any(c.startswith(exempt) for c in documented), (
            f"'{exempt}' is exempted but the Skill no longer documents it — "
            f"remove the exemption."
        )


def test_every_exemption_carries_a_reason():
    for exempt, reason in EXEMPT.items():
        assert len(reason) > 40, f"{exempt}: an exemption needs a real reason"


def test_the_safety_scan_is_not_exemptible():
    """The omission that caused this file. It must never become an exemption.

    npm run lint is the only path that invokes safety-lint.mjs, which enforces
    CLAUDE.md rule 2. A VERIFIED verdict that skips it is not a verification.
    """
    assert not any(e.startswith("npm run lint") for e in EXEMPT)
    assert covers("npm run lint", tool_commands())


def test_parity_check_is_non_vacuous():
    """It must actually fail when the tool stops running something."""
    without_lint = [c for c in tool_commands() if "lint" not in c]
    assert not covers("npm run lint", without_lint)
    assert covers("npm run lint", tool_commands())
