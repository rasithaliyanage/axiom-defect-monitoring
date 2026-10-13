"""GET /api/v1/inspection/queue — read-only synthetic board records (FR-9)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.domain.api.main import create_app
from services.domain.inspection_service import (
    InspectionDataUnavailable,
    InspectionService,
)

QUEUE = "/api/v1/inspection/queue"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "inspection" / "queue.json"

# Fields that would express a quality determination. None may appear.
VERDICT_FIELDS = {
    "status", "disposition", "verdict", "result", "outcome",
    "pass", "passed", "fail", "failed", "approved", "rejected",
    "score", "confidence", "defectRatio", "quality",
}


@pytest.fixture
def client():
    return TestClient(create_app())


def test_queue_returns_200(client):
    assert client.get(QUEUE).status_code == 200


def test_queue_returns_board_identifiers(client):
    body = client.get(QUEUE).json()
    assert body["records"], "expected at least one board record"
    for record in body["records"]:
        assert record["boardId"].startswith("BRD-")


def test_queue_matches_the_fixture_exactly(client):
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))["records"]
    assert client.get(QUEUE).json()["records"] == expected


def test_queue_preserves_fixture_order(client):
    expected = [r["boardId"] for r in json.loads(FIXTURE.read_text(encoding="utf-8"))["records"]]
    assert [r["boardId"] for r in client.get(QUEUE).json()["records"]] == expected


def test_meta_reports_source_and_count(client):
    body = client.get(QUEUE).json()
    assert body["meta"]["source"] == "fixture"
    assert body["meta"]["count"] == len(body["records"])


def test_no_record_carries_a_quality_determination(client):
    """The boundary that matters: identity and capture metadata only.

    A status or disposition here would be a quality outcome, which Quality owns
    and which nothing in this phase determines.
    """
    body = client.get(QUEUE).json()
    for record in body["records"]:
        leaked = VERDICT_FIELDS & {key.lower() for key in record}
        assert not leaked, f"record exposes a quality field: {leaked}"
    assert VERDICT_FIELDS.isdisjoint({k.lower() for k in body["meta"]})


def test_response_text_contains_no_verdict_vocabulary(client):
    serialized = json.dumps(client.get(QUEUE).json()).lower()
    for word in ("pass", "fail", "approved", "rejected", "conforming"):
        assert word not in serialized, f"response contains verdict word {word!r}"


def test_queue_takes_no_payload_and_rejects_other_methods(client):
    assert client.post(QUEUE, json={"line": "line-a"}).status_code == 405
    assert client.delete(QUEUE).status_code == 405


def test_unfiltered_request_returns_everything(client):
    body = client.get(QUEUE).json()
    assert body["meta"]["count"] == body["meta"]["total"]
    assert body["meta"]["filters"] == {"line": None, "limit": None}


def test_repeated_requests_are_identical(client):
    assert client.get(QUEUE).json() == client.get(QUEUE).json()


def test_mutating_the_response_does_not_affect_the_next_request(client):
    first = client.get(QUEUE).json()
    first["records"].clear()
    assert len(client.get(QUEUE).json()["records"]) > 0


def test_service_does_not_mutate_the_fixture_on_disk():
    before = FIXTURE.read_text(encoding="utf-8")
    records = list(InspectionService().queue())
    records.clear()
    assert FIXTURE.read_text(encoding="utf-8") == before


def test_missing_fixture_is_a_sanitized_server_error(tmp_path, monkeypatch):
    from services.domain.api import routes

    monkeypatch.setattr(routes, "_inspection", InspectionService(fixture_dir=tmp_path))
    response = TestClient(create_app(), raise_server_exceptions=False).get(QUEUE)

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INSPECTION_DATA_UNAVAILABLE"
    # No path or exception text leaks to the client.
    assert str(tmp_path) not in json.dumps(body)
    assert "Traceback" not in json.dumps(body)


def test_malformed_fixture_raises_rather_than_returning_partial_data(tmp_path):
    (tmp_path / "queue.json").write_text('{"records": [{"line": "line-a"}]}', encoding="utf-8")
    with pytest.raises(InspectionDataUnavailable):
        InspectionService(fixture_dir=tmp_path).queue()
