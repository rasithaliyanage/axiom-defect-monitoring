"""Read-only inspection data, served from a synthetic fixture.

Implements the data half of `specs/spec.md` FR-9. Kept separate from
`landing_service.py` because this serves *domain records*, not a UI
specification: nothing here is validated by `UISpecValidator`, which exists to
police model output and has no bearing on a hand-authored data fixture.

Boundaries this module holds
----------------------------
- **No quality determination.** A record carries identity and capture metadata
  and nothing else. There is no status, disposition, verdict or score field,
  because deciding whether a board passes is Quality's to own and is out of
  scope for this phase (`CLAUDE.md`).
- **No defect taxonomy invented here.** Where a category is ever referenced it
  must come from the approved enum in `specs/schemas/ui-spec.schema.json`.
- **No data source.** There is no database and no live capture. The records are
  developer-authored synthetic demonstration data.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Final

REPO_ROOT: Final = Path(__file__).resolve().parents[2]
FIXTURE_DIR: Final = REPO_ROOT / "tests" / "fixtures" / "inspection"


class InspectionDataUnavailable(RuntimeError):
    """The fixture is missing or malformed. A server defect."""


class UnknownLine(ValueError):
    """A filter named a line that does not exist in the data.

    Rejected rather than returning an empty list, so a typo is visible instead
    of silently matching nothing.
    """


@dataclass(frozen=True)
class BoardRecord:
    """One synthetic board in the inspection queue."""

    boardId: str
    line: str
    inspectionPoint: str
    recordedAt: str


class InspectionService:
    """Serves synthetic read-only inspection records."""

    def __init__(self, fixture_dir: Path = FIXTURE_DIR) -> None:
        self._fixture_dir = fixture_dir

    def lines(self) -> tuple[str, ...]:
        """Distinct lines present in the data, in first-seen order.

        The allowed filter values are derived from the fixture rather than
        declared in code. Real line identifiers are owned by Manufacturing, so
        hard-coding an enum here would assert a value set engineering does not
        own, and it could drift from the data it filters.
        """
        seen: list[str] = []
        for record in self._all():
            if record.line not in seen:
                seen.append(record.line)
        return tuple(seen)

    def queue(
        self,
        line: str | None = None,
        limit: int | None = None,
    ) -> tuple[tuple[BoardRecord, ...], int]:
        """Filtered queue plus the total before filtering.

        Filtering happens in memory over records already loaded. No parameter
        is ever used to build a path, open a file, or select a fixture.
        """
        records = self._all()
        total = len(records)

        if line is not None:
            allowed = self.lines()
            if line not in allowed:
                raise UnknownLine(line)
            records = tuple(record for record in records if record.line == line)

        if limit is not None:
            records = records[:limit]

        return records, total

    def board(self, board_id: str) -> BoardRecord | None:
        """One board by identifier, or None.

        The identifier is compared against values already in memory. It never
        reaches the filesystem, so a traversal-shaped identifier is simply a
        string that matches nothing.
        """
        for record in self._all():
            if record.boardId == board_id:
                return record
        return None

    def _all(self) -> tuple[BoardRecord, ...]:
        """Every record, in fixture order."""
        path = self._fixture_dir / "queue.json"
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as cause:
            raise InspectionDataUnavailable(str(path)) from cause

        records = payload.get("records")
        if not isinstance(records, list):
            raise InspectionDataUnavailable("queue fixture has no records list")

        # Copied so a caller mutating the result cannot affect the next request.
        out: list[BoardRecord] = []
        for entry in copy.deepcopy(records):
            if not isinstance(entry, dict):
                raise InspectionDataUnavailable("queue record is not an object")
            try:
                out.append(
                    BoardRecord(
                        boardId=str(entry["boardId"]),
                        line=str(entry["line"]),
                        inspectionPoint=str(entry["inspectionPoint"]),
                        recordedAt=str(entry["recordedAt"]),
                    )
                )
            except KeyError as missing:
                raise InspectionDataUnavailable(f"queue record missing {missing}") from None
        return tuple(out)
