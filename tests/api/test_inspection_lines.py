"""GET /api/v1/inspection/lines — the values the `line` filter accepts (FR-9).

The endpoint exists because `?line=line-z` returns 400 without saying what
would have worked. These tests pin the three properties that make the answer
trustworthy: the values are derived from the data rather than declared, they
carry no quality determination, and the endpoint takes no input of its own.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.domain.api.main import create_app
from services.domain.inspection_service import InspectionService

LINES = "/api/v1/inspection/lines"
QUEUE = "/api/v1/inspection/queue"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "inspection" / "queue.json"


@pytest.fixture
def client():
    return TestClient(create_app())


def records() -> list[dict]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["records"]


# --- derived, not declared ---------------------------------------------------

def test_values_come_from_the_data_in_first_seen_order():
    """Line identifiers are Manufacturing's. A copy here would go stale."""
    expected: list[str] = []
    for record in records():
        if record["line"] not in expected:
            expected.append(record["line"])
    assert list(InspectionService().lines()) == expected


def test_endpoint_returns_exactly_what_the_service_derives(client):
    body = client.get(LINES).json()
    assert body["lines"] == list(InspectionService().lines())
    assert body["meta"] == "fixture"


def test_no_line_identifier_is_hard_coded_in_the_route_or_model():
    """The values must not be declared in code anywhere on this path."""
    for module in ("routes.py", "models.py"):
        source = (Path(__file__).resolve().parents[2] / "services" / "domain"
                  / "api" / module).read_text(encoding="utf-8")
        for value in InspectionService().lines():
            assert value not in source, f"{module} hard-codes {value!r}"


# --- the answer is actually usable -------------------------------------------

@pytest.mark.parametrize("line", list(InspectionService().lines()))
def test_every_advertised_line_is_accepted_by_the_filter(client, line):
    """The point of the endpoint: what it lists must work."""
    response = client.get(QUEUE, params={"line": line})
    assert response.status_code == 200
    assert {r["line"] for r in response.json()["records"]} == {line}


def test_a_line_not_listed_is_rejected_by_the_filter(client):
    advertised = set(client.get(LINES).json()["lines"])
    assert "line-z" not in advertised
    assert client.get(QUEUE, params={"line": "line-z"}).status_code == 400


# --- no quality determination -------------------------------------------------

def test_response_carries_identifiers_only(client):
    """Same boundary BoardRecordModel holds: no verdict, no count, no rate."""
    body = client.get(LINES).json()
    assert set(body) == {"lines", "meta"}
    assert all(isinstance(value, str) for value in body["lines"])


def test_response_contains_no_verdict_vocabulary(client):
    serialized = json.dumps(client.get(LINES).json()).lower()
    for word in ("pass", "fail", "approved", "rejected", "conforming",
                 "status", "score", "defect", "count", "rate"):
        assert word not in serialized, f"response contains {word!r}"


# --- input, methods, determinism ----------------------------------------------

@pytest.mark.parametrize("params", [{"line": "line-a"}, {"limit": 1}, {"x": "y"}])
def test_endpoint_accepts_no_query_parameters(client, params):
    response = client.get(LINES, params=params)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


def test_caller_text_is_not_echoed(client):
    body = json.dumps(client.get(LINES, params={"<script>": "x"}).json())
    assert "<script>" not in body


def test_other_methods_are_rejected(client):
    assert client.post(LINES, json={}).status_code == 405
    assert client.delete(LINES).status_code == 405


def test_repeated_requests_are_identical(client):
    assert client.get(LINES).json() == client.get(LINES).json()


def test_request_does_not_mutate_the_fixture_on_disk(client):
    before = FIXTURE.read_text(encoding="utf-8")
    client.get(LINES)
    assert FIXTURE.read_text(encoding="utf-8") == before
