"""Task 4 renderer fixtures must be VALID under the existing Task 3 validator.

The renderer consumes these exact files. There is no runtime transport and no
trust token between this check and the TypeScript tests; the approved-input
guarantee is that this test asserts these bytes are VALID.
"""

import json
from pathlib import Path

import pytest

from services.domain.validator import UISpecValidator

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ui-spec"
CASES = ("task4-demo", "full-catalogue")

APPROVED_COMPONENTS = frozenset({
    "Hero", "Heading", "Text", "FeatureCard", "FeatureGrid",
    "CTA", "Alert", "InfoPanel", "ProgressIndicator",
})
APPROVED_ACTIONS = frozenset({
    "view-inspection-queue", "view-defect-reports", "view-ingest-activity",
    "open-documentation", "contact-support",
})


def load(case: str, kind: str) -> dict[str, object]:
    return json.loads((FIXTURES / f"{case}.{kind}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES)
def test_fixture_is_valid_against_supplied_context(validator: UISpecValidator, case: str) -> None:
    result = validator.validate(load(case, "spec"), load(case, "context"))
    assert result.status == "VALID", [r.model_dump() for r in result.rejections]
    assert result.rejections == ()


@pytest.mark.parametrize("case", CASES)
def test_fixture_contextid_matches_its_context(case: str) -> None:
    assert load(case, "spec")["contextId"] == load(case, "context")["contextId"]


def test_catalogue_fixture_covers_every_approved_component() -> None:
    blocks = load("full-catalogue", "spec")["blocks"]
    assert {block["component"] for block in blocks} == APPROVED_COMPONENTS


def test_catalogue_fixture_covers_every_approved_action() -> None:
    blocks = load("full-catalogue", "spec")["blocks"]
    used = {
        block["props"]["action"] for block in blocks if block["component"] == "CTA"
    } | {
        block["props"]["primaryAction"]
        for block in blocks
        if block["component"] == "Hero" and "primaryAction" in block["props"]
    }
    assert used == APPROVED_ACTIONS


def test_renderer_fixtures_carry_no_unapproved_component() -> None:
    for case in CASES:
        for block in load(case, "spec")["blocks"]:
            assert block["component"] in APPROVED_COMPONENTS
