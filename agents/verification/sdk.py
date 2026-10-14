"""The real `claude-agent-sdk` integration, kept in one file.

Verified against claude-agent-sdk 0.2.165 on Python 3.14: `tool`,
`create_sdk_mcp_server`, `ClaudeSDKClient`, `ClaudeAgentOptions`, and the
`PermissionResultAllow` / `PermissionResultDeny` types all exist with the
signatures used below.

Everything here imports the SDK **lazily**, inside functions. Nothing else in
the repository imports this module at import time, so the deterministic tests
in `tests/agents/` run with no SDK, no API key and no network.

One thing the SDK documentation is explicit about, and it drives this design:

    allowed_tools — "Tools to auto-approve without prompting... This does not
    restrict Claude to only these tools."

`allowed_tools` is an auto-approve list, **not** a boundary. Passing
`["mcp__verification__verify_project"]` alone would leave Claude Code's
built-in Bash, Write and Edit tools reachable. So the bound is built from three
independent things:

1. `tools=[]`           — no Claude Code built-ins are loaded at all.
2. `mcp_servers`        — the only server exposes exactly one tool.
3. `can_use_tool`       — a callback that denies anything else by name.

Any one of those failing still leaves two. The loop in `loop.py` applies its
own allow-list on top, which is the check the deterministic tests exercise.
"""

from __future__ import annotations

from typing import Any

from .tools import verify_project

#: The SDK names an in-process MCP tool `mcp__<server>__<tool>`.
SERVER_NAME = "verification"
TOOL_NAME = "verify_project"
QUALIFIED_TOOL = f"mcp__{SERVER_NAME}__{TOOL_NAME}"

SYSTEM_PROMPT = (
    "You verify this repository and nothing else. Call the verify_project tool, "
    "read its structured result, and then stop. Do not propose code changes, do "
    "not edit files, and do not report success unless the result says status "
    "'pass'. You have exactly one tool."
)


def build_server() -> Any:
    """Build the single-tool in-process MCP server. Imports the SDK lazily."""
    from claude_agent_sdk import create_sdk_mcp_server, tool

    @tool(TOOL_NAME, "Run this project's verification suites and return the result", {})
    async def _verify(_args: dict[str, Any]) -> dict[str, Any]:
        # The tool owns the commands; no argument influences what runs.
        return {
            "content": [
                {"type": "text", "text": verify_project().to_dict().__repr__()}
            ]
        }

    return create_sdk_mcp_server(name=SERVER_NAME, version="0.1.0", tools=[_verify])


def build_permission_callback():
    """Deny by name anything that is not the one approved tool.

    Defence in depth: with `tools=[]` nothing else should be reachable, but a
    callback that fails closed costs nothing and does not rely on that holding.
    """
    from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

    async def can_use_tool(tool_name: str, input_data: dict, _context: Any):
        if tool_name == QUALIFIED_TOOL:
            return PermissionResultAllow(updated_input=input_data)
        return PermissionResultDeny(
            message="Only verify_project may be called by this agent.",
            interrupt=True,
        )

    return can_use_tool


def build_options(max_turns: int = 3) -> Any:
    """Assemble the bounded options object."""
    from claude_agent_sdk import ClaudeAgentOptions

    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        tools=[],                       # no Claude Code built-ins — the real bound
        mcp_servers={SERVER_NAME: build_server()},
        allowed_tools=[QUALIFIED_TOOL],  # auto-approve, not a restriction
        can_use_tool=build_permission_callback(),
        max_turns=max_turns,
        permission_mode="default",
    )


async def run_with_live_model(request: str, max_turns: int = 3) -> list[str]:
    """Drive the real SDK against a live model.

    Requires credentials and network. Nothing in the test suite calls this, and
    nothing in the application runtime imports it.
    """
    from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, TextBlock

    transcript: list[str] = []
    async with ClaudeSDKClient(options=build_options(max_turns)) as client:
        await client.query(request)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        transcript.append(block.text)
    return transcript


def sdk_available() -> bool:
    """Is the SDK importable here? Used for reporting, never for control flow."""
    try:
        import claude_agent_sdk  # noqa: F401
    except ImportError:
        return False
    return True
