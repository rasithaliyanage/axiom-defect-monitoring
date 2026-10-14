"""A bounded engineering-time agent whose only capability is verifying this project.

`loop` and `tools` import no SDK. `sdk` holds the real claude-agent-sdk
integration and imports it lazily, so the deterministic tests need no package,
no API key and no network.
"""

from .loop import (
    ALLOWED_TOOLS,
    DEFAULT_MAX_ITERATIONS,
    Action,
    InvalidAction,
    Observation,
    Reasoner,
    Report,
    StopReason,
    Verdict,
    run_agent,
    validate,
)
from .tools import VerificationResult, verify_project

__all__ = [
    "ALLOWED_TOOLS", "DEFAULT_MAX_ITERATIONS", "Action", "InvalidAction",
    "Observation", "Reasoner", "Report", "StopReason", "Verdict",
    "run_agent", "validate", "VerificationResult", "verify_project",
]
