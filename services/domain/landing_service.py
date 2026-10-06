"""Landing page orchestration: fixture snapshot, validation, action bindings.

Deliberately free of HTTP concerns so the transport can change without touching
the validation boundary. No domain-data access, no model call, no persistence.

The canonical fixture pair lives in tests/fixtures/ui-spec/ and is the same pair
the offline preparation gate validates. This module does not own a second copy.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .request_context import ContextPayload, View
from .validation_models import Rejection
from .validator import UISpecValidator

REPO_ROOT: Final = Path(__file__).resolve().parents[2]
FIXTURE_DIR: Final = REPO_ROOT / "tests" / "fixtures" / "ui-spec"

# Named views map to the canonical fixture pair. A request selects a view; it
# can never select an arbitrary path.
VIEWS: Final[dict[View, str]] = {
    View.OVERVIEW: "full-catalogue",
    View.MINIMAL: "task4-demo",
}


class UnsupportedView(ValueError):
    """The requested view is not in the fixed catalogue."""


class PageMismatch(RuntimeError):
    """Request page disagrees with the server-owned context. A server defect."""


class LocaleMismatch(RuntimeError):
    """Request locale disagrees with the server-owned context. A server defect."""


class FixtureInvalid(RuntimeError):
    """A fixture failed validation. A server defect, never a client error."""

    def __init__(self, view: str, rejections: tuple[Rejection, ...]) -> None:
        super().__init__(f"Fixture for view {view!r} did not validate")
        self.view = view
        self.rejections = rejections


@dataclass(frozen=True)
class LandingPresentation:
    """A validated snapshot plus the bindings derived from the same context."""

    spec: dict[str, object]
    action_labels: dict[str, str]
    context_id: str


class LandingService:
    """Serves the developer-authored synthetic landing presentation."""

    def __init__(self, validator: UISpecValidator | None = None,
                 fixture_dir: Path = FIXTURE_DIR) -> None:
        self._validator = validator if validator is not None else UISpecValidator()
        self._fixture_dir = fixture_dir

    def _read(self, fixture: str, kind: str) -> dict[str, object]:
        path = self._fixture_dir / f"{fixture}.{kind}.json"
        parsed = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            raise FixtureInvalid(fixture, ())
        return parsed

    def presentation(self, request: ContextPayload) -> LandingPresentation:
        """Validate the snapshot, then return exactly what was validated.

        Takes the immutable presentation request explicitly rather than a bare
        string, so what the caller asked for is visible at this boundary instead
        of being reconstructed from a loose parameter.
        """
        view = request.view
        fixture = VIEWS.get(view)
        if fixture is None:
            raise UnsupportedView(str(view))

        # Deep copies, so a caller mutating the response cannot affect the next
        # request. Isolation is not validation; the validator call below is.
        spec = copy.deepcopy(self._read(fixture, "spec"))
        context = copy.deepcopy(self._read(fixture, "context"))

        # Associate the request with the server-owned context. A mismatch is an
        # internal failure, never something to paper over: the fixture and the
        # context are authoritative and are never rewritten to match a request.
        if context.get("page") != str(request.page):
            raise PageMismatch(
                f"Request page {str(request.page)!r} does not match context page "
                f"{context.get('page')!r}"
            )
        if spec.get("page") != str(request.page):
            raise PageMismatch(
                f"Request page {str(request.page)!r} does not match spec page "
                f"{spec.get('page')!r}"
            )
        if context.get("locale") != str(request.locale):
            raise LocaleMismatch(
                f"Request locale {str(request.locale)!r} does not match context locale "
                f"{context.get('locale')!r}"
            )

        # The COMPLETE server-owned context goes to the validator — never the
        # presentation request, which carries no grounding.
        result = self._validator.validate(spec, context)
        if result.status != "VALID":
            raise FixtureInvalid(str(view), result.rejections)

        actions = context.get("actions", [])
        labels: dict[str, str] = {}
        if isinstance(actions, list):
            for action in actions:
                if isinstance(action, dict):
                    labels[str(action["id"])] = str(action["label"])

        context_id = spec.get("contextId")
        if not isinstance(context_id, str):
            raise FixtureInvalid(str(view), result.rejections)

        # The exact object that was validated is the object returned.
        return LandingPresentation(spec=spec, action_labels=labels, context_id=context_id)
