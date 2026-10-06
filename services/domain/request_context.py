"""The presentation request, as a domain value.

`ContextPayload` is the *presentation request* — what the caller asked to see.
It is emphatically **not** the `GroundedContext`, which is server-owned, carries
metrics, alerts, capabilities and actions, and never comes from a caller.

Why a frozen dataclass rather than a Pydantic model
---------------------------------------------------
The transport layer (`api/models.py`) is already Pydantic and has already
rejected unknown fields, wrong types and supplied grounding by the time this is
constructed. Re-validating the same values through a second Pydantic model would
be the duplicate validation layer the design brief warns against.

What this type adds instead is a *domain* boundary: the service receives a named,
immutable value with enum-typed fields rather than a bare string, so a caller
cannot pass an arbitrary view name and nothing downstream can mutate the request
mid-flight. The `__post_init__` checks exist because this value is also
constructed directly in tests and could later be constructed by a non-HTTP
caller, where no Pydantic layer would have run first.

Extensibility
-------------
More request dimensions are expected (line, shift, board type, locale). They are
deliberately **not** present here: their value sets are business-owned and not
yet decided, and inventing them would convert an open question into an apparent
requirement. When they are decided, they become additional fields on this
dataclass and additional members on their own enums — the seam does not need to
be redesigned to accept them.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Page(StrEnum):
    """Pages the presentation API can serve. One, for now."""

    LANDING = "landing"


class View(StrEnum):
    """Named views over the canonical fixture catalogue."""

    OVERVIEW = "overview"
    MINIMAL = "minimal"


class Locale(StrEnum):
    """Supported presentation locales.

    One member today. The value is not invented: `en-US` is the locale already
    carried by every server-owned context. Additional locales are a business
    decision and are added here only once that decision is made.
    """

    EN_US = "en-US"


@dataclass(frozen=True, slots=True)
class ContextPayload:
    """An immutable presentation request. Every field is required."""

    page: Page
    view: View
    locale: Locale

    def __post_init__(self) -> None:
        if not isinstance(self.page, Page):
            raise TypeError(f"page must be a Page, got {type(self.page).__name__}")
        if not isinstance(self.view, View):
            raise TypeError(f"view must be a View, got {type(self.view).__name__}")
        if not isinstance(self.locale, Locale):
            raise TypeError(f"locale must be a Locale, got {type(self.locale).__name__}")
