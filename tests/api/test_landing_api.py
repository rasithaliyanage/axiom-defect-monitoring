"""Task 6: the Domain Runtime HTTP boundary.

Deterministic. No model, no network, no database. The FastAPI TestClient calls
the application in-process.
"""

from __future__ import annotations

import copy
import json
import socket
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.domain.api.main import create_app
from services.domain.landing_service import (
    FixtureInvalid,
    LandingService,
    PageMismatch,
    UnsupportedView,
)
from services.domain.request_context import ContextPayload, Locale, Page, View
from services.domain.validator import UISpecValidator

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ui-spec"
LANDING = "/api/v1/ui/landing-page"
OVERVIEW_REQUEST = ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US)


@pytest.fixture(autouse=True)
def no_outbound_network(monkeypatch):
    """No AI, model or external-domain call may occur.

    Only outbound TCP is blocked. `socket.socket` itself is left alone because
    the event loop uses a local socket pair for its own self-pipe, and the
    in-process TestClient is the intended local API path.
    """

    def forbidden(*args, **kwargs):
        raise AssertionError("Domain Runtime tests must not open an outbound connection")

    monkeypatch.setattr(socket, "create_connection", forbidden)


@pytest.fixture
def client():
    return TestClient(create_app())


def read(name: str, kind: str) -> dict:
    return json.loads((FIXTURES / f"{name}.{kind}.json").read_text(encoding="utf-8"))


# 1 and 2 — health

def test_health_returns_200(client):
    assert client.get("/health").status_code == 200


def test_health_body_is_exactly_status_ok(client):
    assert client.get("/health").json() == {"status": "ok"}


# 3 to 6 — the landing endpoint

def test_landing_returns_200_for_a_supported_request(client):
    assert client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).status_code == 200


def test_returned_spec_has_expected_identity(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    spec = body["spec"]
    assert spec["specVersion"] == "1.0"
    assert spec["page"] == "landing"
    assert spec["contextId"] == body["meta"]["contextId"]


def test_returned_spec_passes_the_existing_python_validator(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    result = UISpecValidator().validate(body["spec"], read("full-catalogue", "context"))
    assert result.status == "VALID", [r.model_dump() for r in result.rejections]


def test_response_contains_the_exact_developer_authored_fixture(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    assert body["spec"] == read("full-catalogue", "spec")


def test_bindings_come_from_the_matching_context(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    expected = {a["id"]: a["label"] for a in read("full-catalogue", "context")["actions"]}
    assert body["bindings"]["actionLabels"] == expected


def test_minimal_view_is_served_too(client):
    body = client.post(LANDING, json={"page": "landing", "view": "minimal", "locale": "en-US", "locale": "en-US"}).json()
    assert body["spec"] == read("task4-demo", "spec")


# 7 — an invalid fixture can never be returned as success

def test_invalid_fixture_raises_and_is_never_returned(tmp_path):
    spec = read("task4-demo", "spec")
    spec["blocks"].append({"component": "DispositionControl", "props": {"label": "Mark"}})
    (tmp_path / "task4-demo.spec.json").write_text(json.dumps(spec), encoding="utf-8")
    (tmp_path / "task4-demo.context.json").write_text(
        json.dumps(read("task4-demo", "context")), encoding="utf-8"
    )

    service = LandingService(fixture_dir=tmp_path)
    with pytest.raises(FixtureInvalid) as raised:
        service.presentation(ContextPayload(page=Page.LANDING, view=View.MINIMAL, locale=Locale.EN_US))
    assert any(r.code == "E_UNKNOWN_COMPONENT" for r in raised.value.rejections)


def test_invalid_fixture_surfaces_as_sanitized_500(tmp_path, monkeypatch):
    spec = read("task4-demo", "spec")
    spec["blocks"].append({"component": "DispositionControl", "props": {"label": "Mark"}})
    (tmp_path / "task4-demo.spec.json").write_text(json.dumps(spec), encoding="utf-8")
    (tmp_path / "task4-demo.context.json").write_text(
        json.dumps(read("task4-demo", "context")), encoding="utf-8"
    )

    from services.domain.api import routes

    monkeypatch.setattr(routes, "_service", LandingService(fixture_dir=tmp_path))
    response = TestClient(create_app(), raise_server_exceptions=False).post(
        LANDING, json={"page": "landing", "view": "minimal", "locale": "en-US", "locale": "en-US"}
    )
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_FAILED"
    # No validator codes, paths or exception text leak to the client.
    serialized = json.dumps(body)
    assert "E_UNKNOWN_COMPONENT" not in serialized
    assert "DispositionControl" not in serialized
    assert "Traceback" not in serialized


# 8 — mutation isolation

def test_mutating_the_response_does_not_affect_the_next_request(client):
    first = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    first["spec"]["blocks"].clear()
    second = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    assert second["spec"] == read("full-catalogue", "spec")


def test_service_does_not_mutate_the_fixture_on_disk(client):
    before = read("full-catalogue", "spec")
    presentation = LandingService().presentation(OVERVIEW_REQUEST)
    presentation.spec["blocks"].clear()
    assert read("full-catalogue", "spec") == before


# 9 — determinism

def test_same_request_produces_the_same_response(client):
    body = {"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}
    assert client.post(LANDING, json=body).json() == client.post(LANDING, json=body).json()


# 10 and request policing

def test_supplied_grounding_is_rejected(client):
    for payload in (
        {"page": "landing", "view": "overview", "locale": "en-US", "context": {"metrics": []}},
        {"page": "landing", "view": "overview", "locale": "en-US", "contextId": "forged"},
        {"page": "landing", "view": "overview", "locale": "en-US", "blocks": []},
        {"page": "landing", "view": "overview", "locale": "en-US", "actions": []},
    ):
        response = client.post(LANDING, json=payload)
        assert response.status_code == 400, payload
        assert response.json()["error"]["code"] == "BAD_REQUEST"


def test_unsupported_values_are_rejected(client):
    assert client.post(LANDING, json={"page": "landing", "view": "nope", "locale": "en-US"}).status_code == 400
    assert client.post(LANDING, json={"page": "inspection", "view": "overview", "locale": "en-US"}).status_code == 400


def test_an_unknown_view_cannot_even_be_constructed():
    # The View enum makes an unknown view unrepresentable, so UnsupportedView is
    # now unreachable in practice. It is retained as defence in depth for a
    # future view added to the enum but not to the VIEWS mapping.
    with pytest.raises(ValueError):
        View("does-not-exist")


def test_get_is_not_allowed_on_the_landing_endpoint(client):
    assert client.get(LANDING).status_code == 405


# Every error shape, including routing errors.
#
# Regression guard: the handler was originally registered against FastAPI's
# HTTPException, which does not catch the Starlette parent that routing raises.
# 404 and 405 silently returned {"detail": ...} while the README promised one
# sanitized envelope.

@pytest.mark.parametrize(
    ("method", "path", "status", "code"),
    [
        ("GET", LANDING, 405, "METHOD_NOT_ALLOWED"),
        ("DELETE", LANDING, 405, "METHOD_NOT_ALLOWED"),
        ("GET", "/api/v1/does-not-exist", 404, "NOT_FOUND"),
        ("POST", "/api/v1/does-not-exist", 404, "NOT_FOUND"),
    ],
)
def test_routing_errors_use_the_sanitized_envelope(client, method, path, status, code):
    response = client.request(method, path)
    assert response.status_code == status
    body = response.json()
    assert "detail" not in body, "Starlette's default shape leaked"
    assert body == {"error": {"code": code, "message": "Request could not be completed"}}


def test_every_error_response_uses_the_same_envelope(client):
    """One shape for every failure, so a client never has to guess."""
    responses = [
        client.post(LANDING, json={"page": "landing", "view": "nope", "locale": "en-US"}),
        client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "context": {}}),
        client.get(LANDING),
        client.get("/api/v1/does-not-exist"),
    ]
    for response in responses:
        assert response.status_code >= 400
        body = response.json()
        assert set(body) == {"error"}, body
        assert set(body["error"]) == {"code", "message"}, body
        assert isinstance(body["error"]["code"], str)


def test_domain_runtime_imports_no_model_or_http_client():
    """Static check: the Domain Runtime has no path to an AI or external service."""
    banned = (
        "openai", "anthropic", "langchain", "transformers", "torch",
        "requests", "httpx", "aiohttp", "urllib.request", "boto3",
        "sqlalchemy", "psycopg", "pymongo",
    )
    root = Path(__file__).resolve().parents[2] / "services" / "domain"
    for path in root.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in source, f"{path.name} imports {name}"
            assert f"from {name}" not in source, f"{path.name} imports from {name}"


def test_response_carries_no_approval_or_auth_claim(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    assert set(body) == {"spec", "bindings", "meta"}
    assert set(body["meta"]) == {"contextId", "source", "validation"}
    assert "approved" not in json.dumps(body["meta"])
