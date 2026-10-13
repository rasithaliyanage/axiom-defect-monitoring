"""Query and path parameters on the read-only inspection endpoints.

Parameters are permitted here and nowhere else. `POST /api/v1/ui/landing-page`
feeds the controlled renderer, so caller-steered input there is exactly what the
approved-input boundary prevents; a test below pins that a query string there
is ignored, never honoured.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.domain.api.main import create_app
from services.domain.inspection_service import InspectionService, UnknownLine

QUEUE = "/api/v1/inspection/queue"
BOARD = "/api/v1/inspection/board"
LANDING = "/api/v1/ui/landing-page"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "inspection" / "queue.json"


@pytest.fixture
def client():
    return TestClient(create_app())


def records() -> list[dict]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["records"]


# --- allowed values are derived, not declared -------------------------------

def test_allowed_lines_come_from_the_data():
    expected = []
    for record in records():
        if record["line"] not in expected:
            expected.append(record["line"])
    assert list(InspectionService().lines()) == expected


def test_line_filter_returns_only_that_line(client):
    body = client.get(QUEUE, params={"line": "line-a"}).json()
    assert body["records"]
    assert {r["line"] for r in body["records"]} == {"line-a"}
    assert body["meta"]["count"] < body["meta"]["total"]
    assert body["meta"]["filters"]["line"] == "line-a"


def test_unknown_line_is_rejected_not_silently_empty(client):
    """A typo must be visible. An empty list would look like 'no boards'."""
    response = client.get(QUEUE, params={"line": "line-z"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


def test_unknown_line_is_not_echoed_back(client):
    """The error must not reflect caller text."""
    body = client.get(QUEUE, params={"line": "<script>alert(1)</script>"}).json()
    assert "<script>" not in json.dumps(body)


def test_service_raises_for_an_unknown_line():
    with pytest.raises(UnknownLine):
        InspectionService().queue(line="line-z")


# --- limit ------------------------------------------------------------------

@pytest.mark.parametrize("limit", [1, 2, 3])
def test_limit_truncates_without_reordering(client, limit):
    body = client.get(QUEUE, params={"limit": limit}).json()
    assert len(body["records"]) == limit
    assert [r["boardId"] for r in body["records"]] == [
        r["boardId"] for r in records()[:limit]
    ]
    # total still reports the unfiltered size.
    assert body["meta"]["total"] == len(records())


@pytest.mark.parametrize("limit", [0, -1, 51, 9999])
def test_limit_outside_bounds_is_rejected(client, limit):
    assert client.get(QUEUE, params={"limit": limit}).status_code == 400


def test_non_numeric_limit_is_rejected(client):
    assert client.get(QUEUE, params={"limit": "many"}).status_code == 400


def test_filters_combine(client):
    body = client.get(QUEUE, params={"line": "line-a", "limit": 1}).json()
    assert len(body["records"]) == 1
    assert body["records"][0]["line"] == "line-a"
    assert body["meta"]["filters"] == {"line": "line-a", "limit": 1}


# --- unknown parameters -----------------------------------------------------

@pytest.mark.parametrize(
    "params",
    [{"lines": "line-a"}, {"Line": "line-a"}, {"offset": 1}, {"sort": "boardId"},
     {"line": "line-a", "unexpected": "x"}],
)
def test_unknown_query_parameters_are_rejected(client, params):
    """Consistent with extra=forbid on the body: a mistyped filter must say so."""
    response = client.get(QUEUE, params=params)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


@pytest.mark.parametrize("name", ["offset", "sort", "</trusted>", "<script>"])
def test_unknown_parameter_message_names_the_allowed_set_not_the_caller(client, name):
    """The diagnostic comes from the server side of the contract.

    Naming the supplied parameter would be more pointed, but that string is
    caller-controlled. The allowed set is server-owned and is the half the
    caller actually needs.
    """
    message = client.get(QUEUE, params={name: "x"}).json()["error"]["message"]
    assert name not in message
    assert "line" in message and "limit" in message


def test_board_endpoint_says_it_accepts_no_query_parameters(client):
    board_id = records()[0]["boardId"]
    message = client.get(f"{BOARD}/{board_id}", params={"line": "line-a"}).json()
    assert message["error"]["message"] == "This endpoint accepts no query parameters"


def test_board_endpoint_accepts_no_query_parameters(client):
    board_id = records()[0]["boardId"]
    assert client.get(f"{BOARD}/{board_id}").status_code == 200
    assert client.get(f"{BOARD}/{board_id}", params={"line": "line-a"}).status_code == 400


# --- single board lookup ----------------------------------------------------

def test_board_lookup_returns_the_matching_record(client):
    expected = records()[0]
    body = client.get(f"{BOARD}/{expected['boardId']}").json()
    assert body["record"] == expected
    assert body["meta"] == "fixture"


def test_unknown_board_is_404(client):
    response = client.get(f"{BOARD}/BRD-does-not-exist")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "BOARD_NOT_FOUND"


@pytest.mark.parametrize(
    "probe",
    [
        "../../../../etc/passwd",
        "..%2F..%2Fsecrets.json",
        "queue.json",
        "../queue",
        "%2e%2e%2f%2e%2e%2fwindows%2fwin.ini",
        "C:\\Windows\\win.ini",
    ],
)
def test_traversal_shaped_identifiers_read_no_file(client, probe):
    """The identifier is matched in memory and never reaches the filesystem.

    Each probe is just a string that matches no board, so it behaves like any
    other unknown identifier.

    One subtlety worth recording: a probe containing an unencoded `..`, such as
    `../queue`, is normalised by the HTTP client *before the request is sent*,
    per RFC 3986. It therefore arrives at the sibling `/queue` route and gets an
    ordinary 200. That is URL resolution landing on an already-public endpoint,
    not traversal — no file is opened either way, which is what this asserts.
    """
    response = client.get(f"{BOARD}/{probe}")
    assert response.status_code in (200, 400, 404), probe

    body = json.dumps(response.json())
    # No filesystem content, ever.
    for leak in ("root:", "passwd", "[fonts]", "specVersion", "contextVersion", "blocks"):
        assert leak not in body, f"{probe} leaked {leak}"

    if response.status_code == 200:
        # Only reachable by normalising onto a known public route, and then the
        # payload must be that route's ordinary response — nothing more.
        assert set(response.json()) in ({"records", "meta"}, {"record", "meta"})


def test_board_identifier_is_not_echoed_back(client):
    body = json.dumps(client.get(f"{BOARD}/<img src=x onerror=1>").json())
    assert "<img" not in body


# --- the UI endpoint remains parameter-free ---------------------------------

def test_landing_page_ignores_query_parameters(client):
    """The approved-input boundary is unchanged by this increment.

    The property that matters is not the status code but that a caller cannot
    steer what the renderer is given: the specification is identical with and
    without a query string.
    """
    body = {"page": "landing", "view": "overview", "locale": "en-US"}
    plain = client.post(LANDING, json=body)
    assert plain.status_code == 200
    # A query string must not steer the presentation request.
    steered = client.post(f"{LANDING}?view=minimal", json=body)
    assert steered.status_code == 200
    assert steered.json()["spec"] == plain.json()["spec"]


# --- determinism and isolation ----------------------------------------------

def test_filtered_requests_are_repeatable(client):
    params = {"line": "line-b"}
    assert client.get(QUEUE, params=params).json() == client.get(QUEUE, params=params).json()


def test_filtering_does_not_mutate_the_fixture_on_disk(client):
    before = FIXTURE.read_text(encoding="utf-8")
    client.get(QUEUE, params={"line": "line-a", "limit": 1})
    client.get(f"{BOARD}/{records()[0]['boardId']}")
    assert FIXTURE.read_text(encoding="utf-8") == before


# --- the rejection message names the right part of the request --------------

@pytest.mark.parametrize("params", [{"limit": 0}, {"limit": 99}, {"limit": "many"}])
def test_limit_rejection_does_not_mention_a_presentation_request(client, params):
    """A bounds failure on `limit` is not a presentation-request failure.

    Both land in the same RequestValidationError handler. Before this was
    pinned, the handler returned the landing-page wording for an inspection
    query, which told the caller nothing true about what went wrong.
    """
    body = client.get(QUEUE, params=params).json()
    message = body["error"]["message"]
    assert body["error"]["code"] == "BAD_REQUEST"
    assert "presentation" not in message.lower()
    assert "query parameter" in message.lower()


def test_landing_body_rejection_keeps_the_presentation_wording(client):
    """The body message is unchanged: this branch must not have moved it."""
    response = client.post(LANDING, json={"page": "landing", "locale": "en-US"})
    assert response.status_code == 400
    assert response.json()["error"]["message"] == (
        "Request is not a supported presentation request"
    )


def test_no_rejection_message_echoes_caller_text(client):
    """Branching on the error location must not have opened an echo path."""
    probes = (
        {"limit": "<script>alert(1)</script>"},
        {"line": "'; DROP TABLE boards--"},
        {"</trusted>": "x"},
    )
    for params in probes:
        serialized = json.dumps(client.get(QUEUE, params=params).json())
        for fragment in ("<script>", "DROP TABLE", "</trusted>"):
            assert fragment not in serialized, params
