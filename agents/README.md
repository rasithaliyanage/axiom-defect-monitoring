# Engineering-time agents

One agent. It verifies this repository and can do nothing else.

**It is not part of the application.** No runtime file imports it, `requirements.txt` does not
contain the Agent SDK, and deleting this directory would change nothing a user of the Board Defect
Inspection System can observe. That separation is asserted by tests, not just stated here.

## Why an agent at all

The other engineering-time primitives are passive: a rule is read, a skill is read, a hook fires on
one event and runs one fixed check. None of them can *decide* anything. Verification is the first
task in this repository with a genuine decision in it — run the checks, look at what came back, and
judge whether the work is done — so it is the smallest honest place to introduce a loop.

"Smallest" is the point. This is deliberately not a coding agent.

## How the loop works

```
         request
            │
            ▼
      ┌─ Reasoner ──────────┐   proposes an Action
      │                     │
      │   Action            ▼
      │        ┌── allow-list ──┐   closed set: {verify_project}
      │        │                │
      │        ▼                ✗ refused ─▶ stop: INVALID_PROPOSAL
      │   static dispatch       │
      │        │                │
      │        ▼                │
      │   verify_project()      │   fixed argv, shell=False, bounded
      │        │                │
      │        ▼                │
      └── Observation ◀─────────┘
            │
            ▼
   stop? ──▶ structured Report (stop reason, verdict, turns)
```

Four things make this safe to run unattended, and each is enforced in code rather than trusted:

**The allow-list is a closed set.** `ALLOWED_TOOLS = frozenset({"verify_project"})`, checked before
anything is dispatched.

**Dispatch is static.** `dispatch()` is a literal `if action.tool == "verify_project"`. No
`getattr`, no registry dict, no import chosen from what the reasoner said. An unknown name cannot
resolve to anything — it fails the allow-list and the loop stops. A test parses the AST to confirm
the tool is named as a literal, and others assert the absence of every dynamic-lookup form.

**The tool owns its commands.** `tools.py` holds four fixed argv tuples run with `shell=False` and
a timeout. No part of any command comes from a model, so there is no string a reasoner could emit
that becomes `rm -rf` or `python something.py`. A test asserts no command contains a shell
metacharacter.

**The loop is bounded.** It stops on success, on a tool error, on a refused proposal, or at
`max_iterations` (default 3). There is no path that does not terminate.

## What it verifies

`verify_project()` runs the checks `.claude/skills/verify-project/SKILL.md` documents — Python
suite, React suite, schema validation, the render-path safety lint, and the React production build
— and returns structured data:

```json
{"status": "pass", "summary": "all 4 checks passed",
 "checks": {"python_tests": {"status": "pass", "exit_code": 0, "detail": "436 passed..."}},
 "counts": {"total": 4, "passed": 4, "failed": 0, "errored": 0}}
```

It deliberately reuses the project's existing verification rather than inventing a second one, and
that reuse is now **enforced**: `tests/agents/test_skill_tool_parity.py` parses the Skill's command
block and fails if the tool stops running something the Skill documents.

The test is fail-closed on addition. A command added to the Skill and not to the tool fails. A
command deliberately not automated must be named in `EXEMPT` with a reason, so silence is not an
option. Two exemptions exist today: `pip check` (an environment question, not a repository one) and
`npm run typecheck` (covered transitively — `build` is
`prepare:fixtures && tsc --noEmit && vite build`). `npm run lint` is explicitly non-exemptible, with
its own test, because that is the omission this file exists to prevent recurring.

It also applies the `--basetemp` workaround that skill records, because without it a sandboxed
shell produces `PermissionError`s that look like failures but are not. That mattered in practice:
the first real run of this agent reported `NOT_VERIFIED` on 11 such errors. The agent was right to
refuse to call that a pass — but the tool was handing it a false negative, so the tool was fixed.

## The verdict is not optimistic

Three outcomes, and they are distinct on purpose:

| Verdict | Means |
|---|---|
| `VERIFIED` | A verification actually ran and returned `pass` |
| `NOT_VERIFIED` | A verification ran and failed, or the tool errored |
| `INCONCLUSIVE` | Nothing was verified — refused proposal, or the iteration limit |

An agent that stops without running anything reports `INCONCLUSIVE`, never `VERIFIED`. A test pins
that, because "I didn't check" and "I checked and it was fine" are the two answers most worth
keeping apart.

## The Claude Agent SDK integration

`sdk.py` holds the real `claude-agent-sdk` integration, verified against **0.2.165** on Python
3.14: `tool`, `create_sdk_mcp_server`, `ClaudeSDKClient`, `ClaudeAgentOptions`,
`PermissionResultAllow` / `PermissionResultDeny`. The tool is exposed as an in-process MCP server,
which is the SDK's documented mechanism for custom tools.

**One thing in the SDK's own documentation drove the design.** Of `allowed_tools` it says:

> Tools to auto-approve without prompting... **This does not restrict Claude to only these tools.**

So `allowed_tools=["mcp__verification__verify_project"]` on its own would *not* bound the agent —
Claude Code's built-in `Bash`, `Write` and `Edit` would still be reachable. The bound is therefore
built from three independent things:

1. `tools=[]` — no built-in tools are loaded at all.
2. `mcp_servers` — the only server exposes exactly one tool.
3. `can_use_tool` — a callback that denies anything else by name and interrupts.

Any one failing still leaves two. The loop's own allow-list sits on top of all three.

**The SDK is imported lazily, inside functions.** Nothing else imports `sdk.py`, so the whole test
suite runs with no SDK, no API key and no network. A test proves this in a clean subprocess rather
than by inspecting the current one.

## Running it

Deterministic, no credentials:

```bash
.venv/Scripts/python.exe -m pytest -q tests/agents
```

Against a live model — requires credentials, costs money, and is not part of any suite:

```python
import asyncio
from agents.verification.sdk import run_with_live_model
asyncio.run(run_with_live_model("Verify the repository is green"))
```

## Limitations, stated plainly

**A live model has not driven this loop.** The `claude-agent-sdk` integration is real and its
surface was verified against the installed package, but every test uses a scripted reasoner, and
no run against a live Claude model was performed. The loop and the tool are exercised for real;
the model is not.

**The SDK's permission layer is asserted structurally, not behaviourally.** Tests confirm `tools=[]`,
`can_use_tool` and `max_turns` are configured. They do not prove the SDK honours them — that would
need a live run. The loop's own allow-list is what the tests actually prove, and it is the layer
that holds regardless.

**`verify_project` is slow by design** — about 25 seconds, because it runs real suites. It is not
suitable for a tight loop, which is part of why `max_iterations` is 3.

**What is now covered that previously was not.** The tool's error branches are exercised for real: a
missing executable, a command that outruns its timeout, a non-zero exit, and output truncation. The
distinction between `error` and `fail` holds at the point it is produced, because the verdict treats
them differently — a tool that could not run has not proved the project wrong.
