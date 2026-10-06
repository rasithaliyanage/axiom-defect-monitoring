"""Transport models for the Domain Runtime HTTP boundary.

These describe the wire format only. They are not a second contract: the UI
specification's authority remains specs/schemas/ui-spec.schema.json, enforced by
services/domain/validator.py. Nothing here re-validates a spec.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransportModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class LandingPageRequest(TransportModel):
    """Presentation-only request.

    `extra="forbid"` is the mechanism that rejects supplied grounding: a request
    carrying `context`, `metrics`, `alerts`, `actions`, `blocks` or `contextId`
    is refused rather than ignored. The browser cannot supply grounding truth.

    Every field is required and has no default: the request states explicitly
    what it is asking for, rather than relying on the server to fill gaps.
    """

    page: Literal["landing"]
    view: Literal["overview", "minimal"]
    locale: Literal["en-US"]


class ResponseMeta(TransportModel):
    """Identity and provenance. Informational — not the client's proof."""

    contextId: str = Field(min_length=1)
    source: Literal["fixture"]
    validation: Literal["VALID"]


class Bindings(TransportModel):
    """Server-owned action labels, from the same validated context.

    Required because Hero.primaryAction is an identifier and the UI
    specification carries no label for it. A bare spec cannot supply this.
    """

    actionLabels: dict[str, str]


class LandingPageResponse(TransportModel):
    spec: dict[str, object]
    bindings: Bindings
    meta: ResponseMeta


class ErrorBody(TransportModel):
    code: str
    message: str


class ErrorResponse(TransportModel):
    """Sanitized. Validator rejection codes are logged, never returned."""

    error: ErrorBody


class HealthResponse(TransportModel):
    """Process liveness only. Says nothing about manufacturing readiness."""

    status: Literal["ok"]
