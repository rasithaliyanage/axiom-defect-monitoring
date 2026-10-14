"""The bounded agentic loop.

    Reasoner -> proposed Action -> allow-list -> static dispatch -> Observation
                                                        |
                                                        v
                                        Reasoner -> continue or stop -> Report

Three properties make this safe to run unattended, and each is enforced here
rather than trusted:

* **The allow-list is a closed set**, checked before dispatch.
* **Dispatch is static.** A literal `if` on one name. No `getattr`, no registry
  lookup, no import driven by what the reasoner said — so an unknown tool name
  cannot resolve to anything, it simply fails the allow-list.
* **The loop is bounded.** It stops on success, on a tool error, on an invalid
  proposal, or at the iteration limit. There is no path that does not stop.

The Reasoner is a protocol, so the loop can be driven by a scripted reasoner in
tests or by the real Claude Agent SDK in `sdk.py`. The loop itself never
imports the SDK.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol

from .tools import CommandRunner, VerificationResult, verify_project

#: The only tool any reasoner may name. A closed set, not a default.
ALLOWED_TOOLS: frozenset[str] = frozenset({"verify_project"})

#: Bounded by default. The loop is not an open-ended autonomous agent.
DEFAULT_MAX_ITERATIONS = 3


class StopReason(StrEnum):
    VERIFICATION_COMPLETE = "VERIFICATION_COMPLETE"
    TOOL_ERROR = "TOOL_ERROR"
    INVALID_PROPOSAL = "INVALID_PROPOSAL"
    MAX_ITERATIONS = "MAX_ITERATIONS"


class Verdict(StrEnum):
    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class Action:
    """What a reasoner proposes. `stop` ends the loop; anything else is a tool."""

    tool: str
    arguments: dict[str, object] = field(default_factory=dict)

    @property
    def is_stop(self) -> bool:
        return self.tool == "stop"


@dataclass(frozen=True)
class Observation:
    """What came back. Returned to the reasoner; never executed."""

    tool: str
    status: str
    result: dict | None = None
    error: str | None = None


class Reasoner(Protocol):
    """The model boundary.

    Implementations decide the next action from the observations so far. They
    never execute anything: the loop owns dispatch, which is what keeps the
    allow-list meaningful.
    """

    def next_action(self, request: str, history: list[Observation]) -> Action: ...


@dataclass
class Turn:
    index: int
    action: Action
    observation: Observation | None
    note: str = ""


@dataclass
class Report:
    """The deliverable. Structured so a human or a CI step can read it."""

    request: str
    turns: list[Turn]
    stop_reason: StopReason
    verdict: Verdict
    summary: str

    def to_dict(self) -> dict:
        return {
            "request": self.request,
            "stop_reason": str(self.stop_reason),
            "verdict": str(self.verdict),
            "summary": self.summary,
            "turns": [
                {
                    "index": t.index,
                    "action": {"tool": t.action.tool, "arguments": dict(t.action.arguments)},
                    "observation": (
                        None if t.observation is None
                        else {"tool": t.observation.tool, "status": t.observation.status,
                              "error": t.observation.error, "result": t.observation.result}
                    ),
                    "note": t.note,
                }
                for t in self.turns
            ],
        }


class InvalidAction(ValueError):
    """A proposal the allow-list refuses. Carries no caller text onward."""


def validate(action: Action) -> None:
    """Reject anything outside the closed set, before dispatch."""
    if not isinstance(action.tool, str) or not action.tool:
        raise InvalidAction("Proposed action names no tool")
    if action.is_stop:
        return
    if action.tool not in ALLOWED_TOOLS:
        # The rejected name is not echoed: it is reasoner-supplied text.
        raise InvalidAction(
            f"Tool is not on the allow-list. Allowed: {sorted(ALLOWED_TOOLS)}"
        )
    if not isinstance(action.arguments, dict):
        raise InvalidAction("Tool arguments must be an object")
    if action.arguments:
        raise InvalidAction("verify_project takes no arguments")


def dispatch(action: Action, runner: CommandRunner | None = None) -> VerificationResult:
    """Static dispatch. One literal name, no dynamic lookup of any kind."""
    if action.tool == "verify_project":
        return verify_project(runner)
    raise InvalidAction("Unknown tool reached dispatch")  # pragma: no cover - guarded above


def _verdict_for(stop_reason: StopReason, last: Observation | None) -> tuple[Verdict, str]:
    if stop_reason is StopReason.VERIFICATION_COMPLETE and last and last.result:
        if last.result.get("status") == "pass":
            return Verdict.VERIFIED, str(last.result.get("summary", "verification passed"))
        return Verdict.NOT_VERIFIED, str(last.result.get("summary", "verification did not pass"))
    if stop_reason is StopReason.TOOL_ERROR:
        return Verdict.NOT_VERIFIED, "the verification tool could not complete"
    if stop_reason is StopReason.INVALID_PROPOSAL:
        return Verdict.INCONCLUSIVE, "the agent proposed an action outside the allow-list"
    if stop_reason is StopReason.MAX_ITERATIONS:
        return Verdict.INCONCLUSIVE, "the iteration limit was reached before a conclusion"
    return Verdict.INCONCLUSIVE, "the agent stopped without a verification result"


def run_agent(
    request: str,
    reasoner: Reasoner,
    *,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    runner: CommandRunner | None = None,
) -> Report:
    """Drive the loop to a bounded conclusion and return a structured report.

    Success is never assumed: the verdict is VERIFIED only when a verification
    actually returned `pass`.
    """
    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1")

    history: list[Observation] = []
    turns: list[Turn] = []
    stop_reason = StopReason.MAX_ITERATIONS

    for index in range(1, max_iterations + 1):
        action = reasoner.next_action(request, list(history))

        try:
            validate(action)
        except InvalidAction as invalid:
            turns.append(Turn(index, action, None, str(invalid)))
            stop_reason = StopReason.INVALID_PROPOSAL
            break

        if action.is_stop:
            turns.append(Turn(index, action, None, "reasoner stopped"))
            stop_reason = (
                StopReason.VERIFICATION_COMPLETE if history else StopReason.INVALID_PROPOSAL
            )
            if not history:
                turns[-1].note = "stopped before any verification was run"
            break

        result = dispatch(action, runner)
        observation = Observation(action.tool, result.status, result.to_dict())
        history.append(observation)
        turns.append(Turn(index, action, observation))

        if result.status == "error":
            stop_reason = StopReason.TOOL_ERROR
            break
        if result.status == "pass":
            stop_reason = StopReason.VERIFICATION_COMPLETE
            break
        # A failure is a real answer; re-running identical checks cannot change it.
        stop_reason = StopReason.VERIFICATION_COMPLETE
        break

    last = history[-1] if history else None
    verdict, summary = _verdict_for(stop_reason, last)
    return Report(request, turns, stop_reason, verdict, summary)
