"""Typed caller context and immutable validation diagnostics."""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class Capability(ContractModel):
    id: str
    label: str
    description: str


class DefectCategory(ContractModel):
    id: str
    label: str


class Metric(ContractModel):
    id: str
    label: str
    value: str
    unit: str | None = None
    asOf: str


class DefectAlert(ContractModel):
    id: str
    defectCategoryId: str
    severity: Literal["info", "warning", "critical"]
    headline: str
    detectedAt: str


class ApprovedAction(ContractModel):
    id: str
    label: str


class GroundedContext(ContractModel):
    contextVersion: Literal["1.0"]
    contextId: str
    page: Literal["landing"]
    locale: str
    generatedAt: str
    capabilities: list[Capability]
    defectCategories: list[DefectCategory]
    metrics: list[Metric]
    alerts: list[DefectAlert]
    actions: list[ApprovedAction]

    @model_validator(mode="after")
    def unambiguous_identifiers(self) -> Self:
        for entries in (self.capabilities, self.defectCategories, self.metrics,
                        self.alerts, self.actions):
            if len({entry.id for entry in entries}) != len(entries):
                raise ValueError("Context identifiers must be unique within each collection")
        categories = {entry.id for entry in self.defectCategories}
        if any(alert.defectCategoryId not in categories for alert in self.alerts):
            raise ValueError("Context alert category must exist in context categories")
        if any("unit" in metric.model_fields_set and metric.unit is None
               for metric in self.metrics):
            raise ValueError("Metric unit must be a string when supplied")
        return self


RejectionCode = Literal[
    "E_SCHEMA", "E_SIZE_LIMIT", "E_DEPTH_LIMIT", "E_UNKNOWN_COMPONENT",
    "E_PROP_INVALID", "E_UNGROUNDED_METRIC", "E_UNKNOWN_DEFECT_CATEGORY",
    "E_UNKNOWN_ACTION", "E_UNGROUNDED_CAPABILITY", "E_CONTEXT_MISMATCH",
    "E_TEXT_POLICY", "E_CODE_LIKE_CONTENT", "E_DECISION_LANGUAGE",
]


class Rejection(ContractModel):
    gate: Literal[1, 2, 3, 4]
    code: RejectionCode
    path: str
    rule: str
    message: str


class ValidationResult(ContractModel):
    status: Literal["VALID", "INVALID"]
    rejections: tuple[Rejection, ...] = ()


class InvalidContextError(ValueError):
    """Caller supplied malformed or inconsistent grounding data."""
