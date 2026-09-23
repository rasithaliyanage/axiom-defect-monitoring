"""Fixed domain fixtures; no model or live data."""

import socket

import pytest

from services.domain.validator import UISpecValidator


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Validator tests must not use the network")
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)


@pytest.fixture
def validator():
    return UISpecValidator()


@pytest.fixture
def context():
    return {
        "contextVersion": "1.0", "contextId": "ctx-fixture", "page": "landing",
        "locale": "en-US", "generatedAt": "2026-09-22T06:00:00Z",
        "capabilities": [{"id": "history", "label": "Inspection history", "description": "Recorded inspection activity"}],
        "defectCategories": [{"id": "solder-bridge", "label": "Solder bridge"}],
        "metrics": [
            {"id": "boards-inspected-shift", "label": "Boards inspected", "value": "1,284", "asOf": "2026-09-22T06:00:00Z"},
            {"id": "defect-rate-shift", "label": "Defect rate", "value": "2.4", "unit": "%", "asOf": "2026-09-22T06:00:00Z"},
        ],
        "alerts": [{"id": "alert-one", "defectCategoryId": "solder-bridge", "severity": "warning",
                    "headline": "Recorded observations", "detectedAt": "2026-09-22T06:00:00Z"}],
        "actions": [{"id": key, "label": "Open view"} for key in (
            "view-inspection-queue", "view-defect-reports", "view-ingest-activity",
            "open-documentation", "contact-support",
        )],
    }


@pytest.fixture
def spec():
    return {"specVersion": "1.0", "page": "landing", "contextId": "ctx-fixture",
            "blocks": [{"component": "Text", "props": {"text": "Inspection activity"}}]}
