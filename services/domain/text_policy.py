"""Deterministic text checks, not an exhaustive semantic policy engine.

The exact patterns are deliberately visible and covered by tests. They cannot
prove capability honesty or absence of every implied quality determination.
"""

import re
from collections.abc import Iterator

from .validation_models import RejectionCode


DECISION = re.compile(
    r"\b(?:pass(?:ed|es)?|fail(?:ed|s)?|approv(?:e|ed|al)|reject(?:ed|ion)?|"
    r"certif(?:ied|ication)|(?:non[- ]?)?conforming|accept(?:ed|ance)?|"
    r"fit\s+to\s+ship|safe\s+to\s+ship|cleared\s+for\s+release|"
    r"do\s+not\s+ship|quality\s+is\s+unacceptable)\b", re.IGNORECASE,
)
MARKUP = re.compile(
    r"<\s*/?\s*[a-z!][^>]*>|&(?:[a-z]+|#\d+|#x[0-9a-f]+);|"
    r"```|`[^`]*`|\*\*|__|(?m:^\s{0,3}(?:#{1,6}\s|[-*+]\s|>\s))|"
    r"\[[^\]]*\]\([^)]*\)|(?<!\w)\*[^*\n]+\*(?!\w)|(?<!\w)_[^_\n]+_(?!\w)",
    re.IGNORECASE,
)
LOCATION = re.compile(
    r"\b[a-z][a-z0-9+.-]*://|\b(?:www\.|mailto:|javascript:|data:)|"
    r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b|"
    r"\b(?:[a-z0-9-]+\.)+(?:com|org|net|io|internal|local|edu|gov)\b|"
    r"\b[a-z]:[\\/]|\\\\[^\s]+|(?:^|\s)(?:/|\.\.?/)[\w.-]+|"
    r"\b[\w.-]+[/\\][\w.-]+",
    re.IGNORECASE,
)
CODE = re.compile(
    r"<\s*/?\s*script\b|\b(?:eval|exec|alert|system|fetch)\s*\(|"
    r"\b(?:function\s*\(|const\s+\w+\s*=|let\s+\w+\s*=)|"
    r"=>|\$\{|\{\{|\{%|\$\(|```|"
    r"\b(?:SELECT\s+.+?\s+FROM|DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO)\b|"
    r"(?:^|[\n;])\s*(?:sudo\s+|rm\s+-|curl\s+|powershell\s+|cmd\s+/c)|"
    r"\b(?:import\s+os|os\.system|subprocess\.)|"
    r"[.#][a-z][\w-]*\s*\{[^}]*:[^}]*\}",
    re.IGNORECASE,
)
SELF_REFERENCE = re.compile(
    r"\b(?:as\s+an?\s+(?:ai|language\s+model)|system\s+prompt|"
    r"generated\s+by\s+(?:ai|an?\s+(?:ai|model)))\b", re.IGNORECASE,
)


def policy_violations(text: str, *, rendered: bool) -> Iterator[tuple[RejectionCode, str, str]]:
    # Code-like content is forbidden in every string, including identifiers.
    if CODE.search(text):
        yield "E_CODE_LIKE_CONTENT", "code", "Code-like content is prohibited"
    if not rendered:
        return
    if MARKUP.search(text):
        yield "E_TEXT_POLICY", "markup", "Markup or formatting syntax is prohibited"
    if LOCATION.search(text):
        yield "E_TEXT_POLICY", "location", "URLs, email addresses and paths are prohibited"
    if any(0x1F000 <= ord(c) <= 0x1FAFF or 0x2600 <= ord(c) <= 0x27BF
           or ord(c) in (0xFE0F, 0x20E3) for c in text):
        yield "E_TEXT_POLICY", "emoji", "Emoji are prohibited"
    if SELF_REFERENCE.search(text):
        yield "E_TEXT_POLICY", "self_reference", "Generation self-reference is prohibited"
    if DECISION.search(text):
        yield "E_DECISION_LANGUAGE", "decision_language", "Quality-decision language is prohibited"
