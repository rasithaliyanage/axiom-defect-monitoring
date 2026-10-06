"""TASK-005: the deterministic fallback specification.

CLAUDE.md rule 3 requires a fallback. Its defining property is that it must be
renderable when nothing else is: if it referenced a metric, alert, defect
category, capability or action, it could only be shown alongside a context that
happened to contain them — which is exactly the situation a fallback exists to
survive.

These tests assert that property rather than assume it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.domain.validator import UISpecValidator

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ui-spec"

EMPTY_CONTEXT = {
    "contextVersion": "1.0",
    "contextId": "fallback",
    "page": "landing",
    "locale": "en-US",
    "generatedAt": "2026-09-22T06:00:00Z",
    "capabilities": [],
    "defectCategories": [],
    "metrics": [],
    "alerts": [],
    "actions": [],
}

REFERENCE_PROPS = (
    "metricId", "alertId", "defectCategoryId", "capabilityId",
    "action", "primaryAction",
)


def load(name: str, kind: str) -> dict:
    return json.loads((FIXTURES / f"{name}.{kind}.json").read_text(encoding="utf-8"))


@pytest.fixture
def fallback() -> dict:
    return load("fallback", "spec")


def test_fallback_is_valid_against_its_own_context(validator, fallback):
    result = validator.validate(fallback, load("fallback", "context"))
    assert result.status == "VALID", [r.model_dump() for r in result.rejections]


def test_fallback_is_valid_against_a_completely_empty_context(validator, fallback):
    """The defining property: no grounding required."""
    result = validator.validate(fallback, dict(EMPTY_CONTEXT))
    assert result.status == "VALID", [r.model_dump() for r in result.rejections]


@pytest.mark.parametrize("other", ["full-catalogue", "task4-demo"])
def test_fallback_is_valid_against_an_unrelated_populated_context(validator, fallback, other):
    """Context-independent in both directions: a rich context does not break it."""
    context = load(other, "context")
    spec = dict(fallback)
    spec["contextId"] = context["contextId"]  # Gate 3 requires identity to match
    result = validator.validate(spec, context)
    assert result.status == "VALID", [r.model_dump() for r in result.rejections]


def test_fallback_references_nothing_from_a_context(fallback):
    """Asserted structurally, not inferred from the validator passing."""
    found: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in REFERENCE_PROPS:
                    found.append(key)
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(fallback)
    assert found == [], f"fallback references context data: {found}"


def test_fallback_uses_only_approved_components(fallback):
    approved = {
        "Hero", "Heading", "Text", "FeatureCard", "FeatureGrid",
        "CTA", "Alert", "InfoPanel", "ProgressIndicator",
    }
    used = {block["component"] for block in fallback["blocks"]}
    assert used <= approved
    # Components that cannot appear, because each one requires grounding.
    assert used.isdisjoint({"CTA", "InfoPanel", "ProgressIndicator"})


def test_fallback_carries_no_decision_language(validator, fallback):
    """Fixed business copy is permitted here, but it still may not imply a verdict."""
    result = validator.validate(fallback, dict(EMPTY_CONTEXT))
    assert not any(r.code == "E_DECISION_LANGUAGE" for r in result.rejections)


def test_fallback_identity_is_stable(fallback):
    assert fallback["specVersion"] == "1.0"
    assert fallback["page"] == "landing"
    assert fallback["contextId"] == "fallback"
    assert len(fallback["blocks"]) >= 1
