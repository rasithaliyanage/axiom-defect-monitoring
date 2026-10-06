"""Task 6A: the presentation request seam.

Covers the ContextPayload domain value, its explicit propagation into the
service, and the guarantee that a rejected request never reaches the service.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.domain.api import routes
from services.domain.api.main import create_app
from services.domain.landing_service import LandingService, PageMismatch
from services.domain.request_context import ContextPayload, Locale, Page, View

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ui-spec"
LANDING = "/api/v1/ui/landing-page"


@pytest.fixture
def client():
    return TestClient(create_app())


# --- the domain value -------------------------------------------------------

def test_payload_carries_both_fields():
    payload = ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US)
    assert payload.page is Page.LANDING
    assert payload.view is View.OVERVIEW


def test_payload_is_immutable():
    payload = ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US)
    with pytest.raises(dataclasses.FrozenInstanceError):
        payload.view = View.MINIMAL  # type: ignore[misc]


def test_payload_has_no_defaults():
    """Both fields are required; nothing is silently supplied."""
    with pytest.raises(TypeError):
        ContextPayload()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        ContextPayload(page=Page.LANDING)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    ("page", "view"),
    [("landing", View.OVERVIEW), (Page.LANDING, "overview"), (None, None)],
)
def test_payload_rejects_wrong_types(page, view):
    """Constructed outside HTTP, it still refuses loose values."""
    with pytest.raises(TypeError):
        ContextPayload(page=page, view=view)


def test_payload_carries_no_grounding():
    """ContextPayload is a presentation request, never a GroundedContext."""
    fields = {f.name for f in dataclasses.fields(ContextPayload)}
    assert fields == {"page", "view", "locale"}
    for grounding in ("metrics", "alerts", "actions", "capabilities", "contextId"):
        assert grounding not in fields


# --- propagation ------------------------------------------------------------

def test_route_passes_the_payload_to_the_service(client, monkeypatch):
    seen: list[object] = []
    real = routes._service.presentation

    def spy(request):
        seen.append(request)
        return real(request)

    monkeypatch.setattr(routes._service, "presentation", spy)
    assert client.post(LANDING, json={"page": "landing", "view": "minimal", "locale": "en-US", "locale": "en-US"}).status_code == 200

    assert len(seen) == 1
    payload = seen[0]
    assert isinstance(payload, ContextPayload)
    assert payload.page is Page.LANDING
    assert payload.view is View.MINIMAL


@pytest.mark.parametrize(
    "body",
    [
        {"page": "landing", "view": "nope", "locale": "en-US"},
        {"page": "inspection", "view": "overview", "locale": "en-US"},
        {"page": "landing", "view": "overview", "locale": "en-US", "context": {}},
        {"page": "landing", "view": "overview", "locale": "en-US", "contextId": "forged"},
        {"page": "landing", "view": "overview", "locale": "en-US", "lineId": "L1"},
        {"page": "landing", "view": "overview", "locale": "fr-FR"},
    ],
)
def test_rejected_requests_never_reach_the_service(client, monkeypatch, body):
    """Transport rejection happens first; the service is not called at all."""
    called: list[object] = []
    monkeypatch.setattr(
        routes._service, "presentation", lambda request: called.append(request)
    )

    response = client.post(LANDING, json=body)

    assert response.status_code == 400
    assert called == [], f"service was invoked for rejected body {body}"


@pytest.mark.parametrize(
    "body",
    [
        {"page": "landing", "view": "overview"},   # locale omitted
        {"page": "landing", "locale": "en-US"},    # view omitted
        {"view": "overview", "locale": "en-US"},   # page omitted
        {},                                        # all omitted
    ],
)
def test_omitted_fields_are_now_rejected(client, monkeypatch, body):
    """Every field is required; nothing is silently supplied.

    This replaces an earlier guard that pinned the opposite behaviour. While
    `page` and `view` still carried defaults, omitting one produced a 200 with a
    server-chosen value. That default was removed when `locale` was added, so
    the request now states explicitly what it is asking for. The old guard
    failing is what surfaced this change rather than letting it pass silently.
    """
    called: list[object] = []
    monkeypatch.setattr(
        routes._service, "presentation", lambda request: called.append(request)
    )

    response = client.post(LANDING, json=body)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"
    assert called == [], f"service was invoked for incomplete body {body}"


# --- request / server-context association -----------------------------------

def test_page_is_associated_with_the_server_context(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    context = json.loads((FIXTURES / "full-catalogue.context.json").read_text(encoding="utf-8"))
    assert body["spec"]["page"] == context["page"] == "landing"


def test_page_mismatch_is_an_internal_failure(tmp_path):
    """A context disagreeing with the request fails; neither is rewritten."""
    spec = json.loads((FIXTURES / "full-catalogue.spec.json").read_text(encoding="utf-8"))
    context = json.loads((FIXTURES / "full-catalogue.context.json").read_text(encoding="utf-8"))
    context["page"] = "something-else"
    (tmp_path / "full-catalogue.spec.json").write_text(json.dumps(spec), encoding="utf-8")
    (tmp_path / "full-catalogue.context.json").write_text(json.dumps(context), encoding="utf-8")

    service = LandingService(fixture_dir=tmp_path)
    with pytest.raises(PageMismatch):
        service.presentation(ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US))

    # The fixture on disk was not rewritten to satisfy the request.
    reread = json.loads((tmp_path / "full-catalogue.context.json").read_text(encoding="utf-8"))
    assert reread["page"] == "something-else"


def test_validator_receives_the_complete_server_context(monkeypatch):
    """The full GroundedContext is validated — never the ContextPayload."""
    captured: list[object] = []
    service = LandingService()
    real = service._validator.validate

    def spy(spec, context):
        captured.append(context)
        return real(spec, context)

    monkeypatch.setattr(service._validator, "validate", spy)
    service.presentation(ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US))

    assert len(captured) == 1
    context = captured[0]
    assert isinstance(context, dict)
    assert not isinstance(context, ContextPayload)
    for required in (
        "contextVersion", "contextId", "page", "locale", "generatedAt",
        "capabilities", "defectCategories", "metrics", "alerts", "actions",
    ):
        assert required in context, f"context missing {required}"


# --- unchanged behaviour ----------------------------------------------------

def test_wire_contract_is_unchanged_by_the_seam(client):
    body = client.post(LANDING, json={"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}).json()
    assert set(body) == {"spec", "bindings", "meta"}
    assert set(body["meta"]) == {"contextId", "source", "validation"}
    assert "generated_for" not in json.dumps(body)


def test_repeated_requests_are_identical(client):
    body = {"page": "landing", "view": "overview", "locale": "en-US", "locale": "en-US"}
    assert client.post(LANDING, json=body).json() == client.post(LANDING, json=body).json()


def test_payload_reuse_does_not_mutate_it():
    payload = ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US)
    service = LandingService()
    service.presentation(payload)
    service.presentation(payload)
    assert payload == ContextPayload(page=Page.LANDING, view=View.OVERVIEW, locale=Locale.EN_US)
