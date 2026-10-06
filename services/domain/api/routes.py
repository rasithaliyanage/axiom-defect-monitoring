"""HTTP concerns only. Orchestration lives in services/domain/landing_service.py."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from ..landing_service import (
    FixtureInvalid,
    LandingService,
    LocaleMismatch,
    PageMismatch,
    UnsupportedView,
)
from ..request_context import ContextPayload, Locale, Page, View
from .models import (
    Bindings,
    HealthResponse,
    LandingPageRequest,
    LandingPageResponse,
    ResponseMeta,
)

logger = logging.getLogger(__name__)

router = APIRouter()
_service = LandingService()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Process liveness. Not inspection or quality readiness."""
    return HealthResponse(status="ok")


@router.post("/api/v1/ui/landing-page", response_model=LandingPageResponse)
def landing_page(request: LandingPageRequest) -> LandingPageResponse:
    """Return the developer-authored synthetic landing presentation.

    The specification is validated against its complete server-owned grounded
    context before this returns. There is no model call anywhere in this path.
    """
    # The domain value is constructed only after transport validation has
    # passed, so a malformed request can never reach the service.
    payload = ContextPayload(
        page=Page(request.page),
        view=View(request.view),
        locale=Locale(request.locale),
    )

    try:
        presentation = _service.presentation(payload)
    except UnsupportedView:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "UNSUPPORTED_VIEW", "message": "Unknown view requested"},
        ) from None
    except (PageMismatch, LocaleMismatch) as mismatch:
        logger.error("Request/context mismatch: %s", mismatch)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "VALIDATION_FAILED",
                "message": "The requested presentation could not be validated",
            },
        ) from None
    except FixtureInvalid as invalid:
        # A server defect, not a client error. Rejection codes stay in the log;
        # the client gets a sanitized message and never the invalid spec.
        logger.error(
            "Fixture validation failed for view %s: %s",
            invalid.view,
            [f"{r.gate}/{r.code}@{r.path}" for r in invalid.rejections],
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "VALIDATION_FAILED",
                "message": "The requested presentation could not be validated",
            },
        ) from None

    return LandingPageResponse(
        spec=presentation.spec,
        bindings=Bindings(actionLabels=presentation.action_labels),
        meta=ResponseMeta(
            contextId=presentation.context_id,
            source="fixture",
            validation="VALID",
        ),
    )
