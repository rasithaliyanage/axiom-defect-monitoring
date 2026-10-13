"""HTTP concerns only. Orchestration lives in services/domain/landing_service.py."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request, status

from ..inspection_service import (
    BoardRecord,
    InspectionDataUnavailable,
    InspectionService,
    UnknownLine,
)
from ..landing_service import (
    FixtureInvalid,
    LandingService,
    LocaleMismatch,
    PageMismatch,
    UnsupportedView,
)
from ..request_context import ContextPayload, Locale, Page, View
from .models import (
    AppliedFilters,
    Bindings,
    BoardRecordModel,
    BoardResponse,
    HealthResponse,
    InspectionQueueMeta,
    InspectionQueueResponse,
    LandingPageRequest,
    LandingPageResponse,
    ResponseMeta,
)

logger = logging.getLogger(__name__)

router = APIRouter()
_service = LandingService()
_inspection = InspectionService()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Process liveness. Not inspection or quality readiness."""
    return HealthResponse(status="ok")


def _bad_request(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"code": "BAD_REQUEST", "message": message},
    )


def _reject_unknown_query(request: Request, allowed: set[str]) -> None:
    """Refuse query parameters outside the declared set.

    FastAPI ignores unknown query parameters by default. Ignoring them would be
    inconsistent with `extra="forbid"` on the request body: a mistyped filter
    would silently return unfiltered data rather than saying so.

    The message names what this endpoint *accepts*, never what the caller sent.
    Naming the supplied parameter would be more pointed, but the parameter name
    is caller-controlled text, and reflecting caller text into an error is the
    one thing every error path here is required not to do. The allowed set is
    server-owned, so it is safe to state and is the more useful half anyway.
    """
    if set(request.query_params) - allowed:
        raise _bad_request(
            f"Unsupported query parameter. This endpoint accepts: "
            f"{', '.join(sorted(allowed))}"
            if allowed
            else "This endpoint accepts no query parameters"
        )


def _as_model(record: BoardRecord) -> BoardRecordModel:
    return BoardRecordModel(
        boardId=record.boardId,
        line=record.line,
        inspectionPoint=record.inspectionPoint,
        recordedAt=record.recordedAt,
    )


def _unavailable(cause: InspectionDataUnavailable) -> HTTPException:
    logger.error("Inspection fixture unusable: %s", cause)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "code": "INSPECTION_DATA_UNAVAILABLE",
            "message": "Inspection records could not be read",
        },
    )


@router.get("/api/v1/inspection/queue", response_model=InspectionQueueResponse)
def inspection_queue(
    request: Request,
    line: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
    limit: Annotated[int | None, Query(ge=1, le=50)] = None,
) -> InspectionQueueResponse:
    """Read-only synthetic inspection queue, including board identifiers.

    Satisfies part of `specs/spec.md` FR-9.

    `line` is validated against the set actually present in the data, so an
    unknown line is rejected rather than returning an empty list. Neither
    parameter is ever used to build a path or choose a fixture — filtering
    happens in memory over records already loaded.

    Records carry identity and capture metadata only. No quality outcome is
    returned, because none is determined anywhere in this phase.
    """
    _reject_unknown_query(request, {"line", "limit"})

    try:
        records, total = _inspection.queue(line=line, limit=limit)
    except UnknownLine:
        # The requested line is not echoed back, so a caller cannot use the
        # error message to reflect arbitrary text.
        raise _bad_request("Unknown line") from None
    except InspectionDataUnavailable as unavailable:
        raise _unavailable(unavailable) from None

    return InspectionQueueResponse(
        records=[_as_model(record) for record in records],
        meta=InspectionQueueMeta(
            source="fixture",
            count=len(records),
            total=total,
            filters=AppliedFilters(line=line, limit=limit),
        ),
    )


@router.get("/api/v1/inspection/board/{board_id}", response_model=BoardResponse)
def inspection_board(request: Request, board_id: str) -> BoardResponse:
    """One board record by identifier.

    The identifier is matched against values already in memory. It never
    reaches the filesystem, so a traversal-shaped identifier matches nothing
    and returns 404 like any other unknown board.
    """
    _reject_unknown_query(request, set())

    try:
        record = _inspection.board(board_id)
    except InspectionDataUnavailable as unavailable:
        raise _unavailable(unavailable) from None

    if record is None:
        # The identifier is not echoed back.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "BOARD_NOT_FOUND", "message": "No such board record"},
        )

    return BoardResponse(record=_as_model(record))


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
