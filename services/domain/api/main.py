"""FastAPI application construction.

Domain Runtime. This is NOT the AI Runtime: no model gateway, no model call, no
generation. The UI specification it serves is developer-authored and synthetic.

No CORS middleware: the Vite dev server proxies /api to this service, so the
browser sees a single origin. Adding CORS would widen the boundary for no gain.

Run locally from the repository root:
    .venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .routes import router

# Starlette's routing raises its own HTTPException for 404 and 405. FastAPI's
# HTTPException subclasses it, so registering the handler against the PARENT
# catches both; registering against FastAPI's would silently miss routing
# errors and leak Starlette's default {"detail": ...} shape.
STATUS_CODES: dict[int, str] = {
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
}

# One message per place a request can be malformed. Fixed strings: nothing a
# caller supplied is reflected back, only which part of the request was wrong.
REQUEST_MESSAGES: dict[str, str] = {
    "body": "Request is not a supported presentation request",
    "query": "Query parameter is missing, out of range or of the wrong type",
    "path": "Path parameter is not valid",
}


def _error_location(exc: RequestValidationError) -> str:
    """Where the first validation error came from: body, query or path.

    Pydantic reports `loc` as a tuple whose head names the request part. An
    unrecognised head falls back to the body message, so a future parameter
    kind cannot produce an empty or surprising string.
    """
    for error in exc.errors():
        location = error.get("loc") or ()
        if location and location[0] in REQUEST_MESSAGES:
            return str(location[0])
    return "body"


def create_app() -> FastAPI:
    app = FastAPI(
        title="Board Defect Inspection — Domain Runtime",
        version="1.0.0",
        description=(
            "Serves a developer-authored synthetic UI specification, validated "
            "against its server-owned grounded context. No AI or model call."
        ),
    )

    @app.exception_handler(RequestValidationError)
    async def malformed_request(_: Request, exc: RequestValidationError) -> JSONResponse:
        """Normalise FastAPI's 422 into the sanitized error envelope.

        A request supplying grounding fields lands here, because the transport
        models forbid extras. So does a query parameter outside its declared
        bounds or type, which is why the message depends on where the error
        came from: a bounds failure on `limit` has nothing to do with a
        presentation request, and saying so was actively misleading.

        The location is server-owned — it comes from our own parameter and
        model declarations, not from caller text — so branching on it echoes
        nothing. The specific field errors are still not returned.
        """
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "BAD_REQUEST",
                    "message": REQUEST_MESSAGES.get(
                        _error_location(exc), REQUEST_MESSAGES["body"]
                    ),
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def sanitized_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Every error leaves as { "error": { code, message } }.

        Registered against Starlette's HTTPException so routing failures (404,
        405) are covered as well as the ones our routes raise. Keeping one shape
        means a client never has to guess, and nothing internal leaks: the
        validator's rejection codes are logged in the route, never serialized.
        """
        detail = exc.detail
        if isinstance(detail, dict) and "code" in detail and "message" in detail:
            body = {"error": {"code": detail["code"], "message": detail["message"]}}
        else:
            # Routing errors carry a plain string. Map the status to a stable
            # code rather than echoing Starlette's wording back.
            body = {
                "error": {
                    "code": STATUS_CODES.get(exc.status_code, "ERROR"),
                    "message": "Request could not be completed",
                }
            }
        return JSONResponse(status_code=exc.status_code, content=body)

    app.include_router(router)
    return app


app = create_app()
