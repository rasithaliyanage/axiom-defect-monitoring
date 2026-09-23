"""UISpec 1.0 validation with no model, network, rendering or input repair.

Construct once to load a local schema snapshot. validate() performs no I/O.
See README.md for result semantics and the limits of deterministic text checks.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Literal

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaError
from pydantic import ValidationError as ContextError

from .text_policy import policy_violations
from .validation_models import (
    GroundedContext, InvalidContextError, Rejection, RejectionCode, ValidationResult,
)

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "specs" / "schemas" / "ui-spec.schema.json"
TOTAL_TEXT_LIMIT = 4000  # specs/spec.md: UI specification model, VR-9
NUMBER_TEXT = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z")
DISPLAY_FIELDS = {
    "Hero": {"eyebrow", "title", "subtitle"},
    "Heading": {"text"}, "Text": {"text"},
    "FeatureCard": {"title", "body"}, "FeatureGrid": set(),
    "CTA": {"label"}, "Alert": {"title", "body"},
    "InfoPanel": {"title"}, "ProgressIndicator": {"label", "caption"},
}


def _pointer(parts: tuple[str | int, ...]) -> str:
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def _walk(value: object, path: tuple[str | int, ...] = ()) -> Iterator[tuple[tuple[str | int, ...], object]]:
    yield path, value
    if isinstance(value, dict):
        for key in sorted(value):
            yield from _walk(value[key], path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk(item, path + (index,))


def _snapshot(value: object, active: set[int] | None = None) -> object:
    """Copy only JSON data, rejecting cycles and non-JSON Python objects."""
    if active is None:
        active = set()
    if value is None or type(value) in (bool, int):
        return value
    if type(value) is str:
        value.encode("utf-8")  # Reject lone surrogates consistently for both input forms.
        return value
    if type(value) in (float, Decimal):
        if not (value.is_finite() if isinstance(value, Decimal) else math.isfinite(value)):
            raise ValueError("Non-finite number")
        return value
    if type(value) not in (dict, list) or id(value) in active:
        raise ValueError("Not an acyclic JSON value")
    active.add(id(value))
    try:
        if isinstance(value, dict):
            if any(type(key) is not str for key in value):
                raise ValueError("JSON object keys must be strings")
            return {_snapshot(key): _snapshot(item, active) for key, item in value.items()}
        return [_snapshot(item, active) for item in value]
    finally:
        active.remove(id(value))


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(value: str) -> object:
    raise ValueError("Non-JSON number")


class UISpecValidator:
    def __init__(self, schema_path: Path = SCHEMA_PATH) -> None:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError("Expected Draft 2020-12 schema")
        # The shipped schema uses only local references; disallow future accidental
        # network retrieval rather than relying on a resolver's network defaults.
        for _, value in _walk(schema):
            if isinstance(value, dict) and "$ref" in value and not value["$ref"].startswith("#/"):
                raise ValueError("UISpec schema references must be local")
        Draft202012Validator.check_schema(schema)
        self._schema = schema
        self._validator = Draft202012Validator(schema)
        self._branches = {
            schema["$defs"][ref["$ref"].split("/")[-1]]["properties"]["component"]["const"]: index
            for index, ref in enumerate(schema["$defs"]["Block"]["oneOf"])
        }
        self._actions = frozenset(schema["$defs"]["CtaProps"]["properties"]["action"]["enum"])
        self._categories = frozenset(schema["$defs"]["AlertProps"]["properties"]["defectCategoryId"]["enum"])

    def _leaves(self, error: SchemaError) -> Iterator[SchemaError]:
        # oneOf reports all nine branches. Only the selected discriminator branch
        # is relevant; do not report missing props from unrelated components.
        if error.validator == "oneOf" and isinstance(error.instance, dict):
            name = error.instance.get("component")
            index = self._branches.get(name) if isinstance(name, str) else None
            if index is not None:
                for child in error.context:
                    if child.schema_path[0] == index:
                        yield from self._leaves(child)
                return
        yield error

    def validate(self, raw_spec: object, context: GroundedContext | dict[str, object]) -> ValidationResult:
        """Check model output; malformed domain context raises InvalidContextError.

        VALID means all implemented deterministic checks passed. It does not
        certify semantic correctness of unrestricted natural-language claims.
        """
        try:
            context_data = context.model_dump(exclude_unset=True) if isinstance(context, GroundedContext) else context
            grounded = GroundedContext.model_validate(_snapshot(context_data))
        except (ContextError, ValueError, TypeError, RecursionError):
            raise InvalidContextError("Grounded context is malformed or inconsistent") from None

        errors: list[Rejection] = []

        def add(gate: Literal[1, 2, 3, 4], code: RejectionCode, path: tuple[str | int, ...],
                rule: str, message: str) -> None:
            errors.append(Rejection(gate=gate, code=code, path=_pointer(path), rule=rule, message=message))

        def finish() -> ValidationResult:
            unique = {(e.gate, e.path, e.code, e.rule, e.message): e for e in errors}
            ordered = tuple(unique[key] for key in sorted(unique))
            return ValidationResult(status="INVALID" if ordered else "VALID", rejections=ordered)

        try:
            parsed = (json.loads(raw_spec, parse_float=Decimal, parse_constant=_invalid_constant,
                                 object_pairs_hook=_pairs) if isinstance(raw_spec, str) else raw_spec)
            spec = _snapshot(parsed)
        except (ValueError, TypeError, RecursionError):
            add(1, "E_SCHEMA", (), "json", "Input must be finite, acyclic JSON with unique object keys")
            return finish()

        for parent in self._validator.iter_errors(spec):
            for error in self._leaves(parent):
                path = tuple(error.absolute_path)
                rule = str(error.validator)
                paths = [path]
                if rule == "required" and isinstance(error.instance, dict):
                    paths = [path + (key,) for key in error.validator_value if key not in error.instance]
                elif rule == "additionalProperties" and isinstance(error.instance, dict):
                    declared = error.schema.get("properties", {})
                    patterns = error.schema.get("patternProperties", {})
                    paths = [path + (key,) for key in sorted(error.instance)
                             if key not in declared and not any(re.search(p, key) for p in patterns)]
                # Stable messages avoid library formatting changes and disclosure
                # of raw input. JSON Pointer + keyword identifies the violation.
                for diagnostic_path in paths:
                    add(1, "E_SCHEMA", diagnostic_path, rule, f"Schema constraint violated: {rule}")
                    if len(diagnostic_path) >= 3 and diagnostic_path[0] == "blocks" and diagnostic_path[2] == "props":
                        add(2, "E_PROP_INVALID", diagnostic_path, rule, f"Invalid component properties: {rule}")
                if rule in ("minItems", "maxItems"):
                    add(1, "E_SIZE_LIMIT", path, rule, "Array size is outside the contract bounds")
                if rule in ("minLength", "maxLength"):
                    add(4, "E_TEXT_POLICY", path, rule, "String length is outside the schema bounds")

        if not isinstance(spec, dict):
            return finish()
        if isinstance(spec.get("contextId"), str) and spec["contextId"] != grounded.contextId:
            add(3, "E_CONTEXT_MISMATCH", ("contextId",), "context_id", "Context identifier differs from the request")

        metrics = {m.id: m for m in grounded.metrics}
        categories = {c.id for c in grounded.defectCategories}
        actions = {a.id for a in grounded.actions}
        capabilities = {c.id for c in grounded.capabilities}
        alerts = {a.id for a in grounded.alerts}
        rendered: dict[tuple[str | int, ...], str] = {}

        def display(props: dict[str, object], path: tuple[str | int, ...], fields: set[str]) -> None:
            for field in fields:
                if isinstance(props.get(field), str):
                    rendered[path + (field,)] = props[field]

        def reference(props: dict[str, object], path: tuple[str | int, ...], key: str,
                      allowed: set[str] | frozenset[str], code: RejectionCode, gate: Literal[2, 3] = 3) -> None:
            if isinstance(props.get(key), str) and props[key] not in allowed:
                add(gate, code, path + (key,), "reference", "Identifier is not available in the approved request context")

        def card(props: dict[str, object], path: tuple[str | int, ...]) -> None:
            display(props, path, DISPLAY_FIELDS["FeatureCard"])
            reference(props, path, "capabilityId", capabilities, "E_UNGROUNDED_CAPABILITY")

        blocks = spec.get("blocks")
        if isinstance(blocks, list):
            for index, block in enumerate(blocks):
                path = ("blocks", index)
                if not isinstance(block, dict):
                    continue
                name = block.get("component")
                if not isinstance(name, str) or name not in self._branches:
                    if "component" in block:
                        add(2, "E_UNKNOWN_COMPONENT", path + ("component",), "component", "Component is not approved")
                    continue
                props = block.get("props")
                if not isinstance(props, dict):
                    continue
                path += ("props",)
                display(props, path, DISPLAY_FIELDS[name])
                if name == "Hero":
                    reference(props, path, "primaryAction", actions & self._actions, "E_UNKNOWN_ACTION")
                elif name == "CTA":
                    reference(props, path, "action", actions & self._actions, "E_UNKNOWN_ACTION")
                elif name == "FeatureCard":
                    card(props, path)
                elif name == "FeatureGrid" and isinstance(props.get("items"), list):
                    for item_index, item in enumerate(props["items"]):
                        if isinstance(item, dict):
                            card(item, path + ("items", item_index))
                elif name == "Alert":
                    reference(props, path, "defectCategoryId", categories & self._categories, "E_UNKNOWN_DEFECT_CATEGORY")
                    # No dedicated alert code is in v1. An unavailable alertId is
                    # an invalid prop value, using the existing E_PROP_INVALID.
                    reference(props, path, "alertId", alerts, "E_PROP_INVALID", gate=2)
                elif name == "InfoPanel" and isinstance(props.get("rows"), list):
                    for row_index, row in enumerate(props["rows"]):
                        if not isinstance(row, dict):
                            continue
                        row_path = path + ("rows", row_index)
                        display(row, row_path, {"label", "value", "unit"})
                        reference(row, row_path, "metricId", set(metrics), "E_UNGROUNDED_METRIC")
                        metric_id = row.get("metricId")
                        metric = metrics.get(metric_id) if isinstance(metric_id, str) else None
                        if metric:
                            if isinstance(row.get("value"), str) and row["value"] != metric.value:
                                add(3, "E_UNGROUNDED_METRIC", row_path + ("value",), "verbatim", "Metric value must match context exactly")
                            if "unit" in row and row["unit"] != metric.unit:
                                add(3, "E_UNGROUNDED_METRIC", row_path + ("unit",), "verbatim", "Metric unit must match context exactly")
                elif name == "ProgressIndicator":
                    reference(props, path, "metricId", set(metrics), "E_UNGROUNDED_METRIC")
                    metric_id = props.get("metricId")
                    metric = metrics.get(metric_id) if isinstance(metric_id, str) else None
                    if metric:
                        if metric.unit != "%":
                            add(3, "E_UNGROUNDED_METRIC", path + ("metricId",), "percentage_unit", "Progress metric must use the percent unit")
                        try:
                            if not NUMBER_TEXT.fullmatch(metric.value):
                                raise InvalidOperation
                            expected = Decimal(metric.value)
                            value = props.get("value")
                            if type(value) in (int, float, Decimal) and Decimal(str(value)) != expected:
                                add(3, "E_UNGROUNDED_METRIC", path + ("value",), "numeric_match", "Progress value must match the context number exactly")
                        except InvalidOperation:
                            add(3, "E_UNGROUNDED_METRIC", path + ("metricId",), "numeric_format", "Progress metric must contain a JSON-format number")

        total_text = sum(len(value) for value in rendered.values())
        if total_text > TOTAL_TEXT_LIMIT:
            add(1, "E_SIZE_LIMIT", ("blocks",), "total_text", "Rendered string fields exceed 4000 Unicode code points")
        for path, value in _walk(spec):
            if isinstance(value, dict):
                if "component" in value and not (len(path) == 2 and path[0] == "blocks"):
                    add(1, "E_DEPTH_LIMIT", path, "nesting", "Component envelopes are permitted only in top-level blocks")
                    name = value["component"]
                    if isinstance(name, str) and name not in self._branches:
                        add(2, "E_UNKNOWN_COMPONENT", path + ("component",), "component", "Component is not approved")
                if "children" in value:
                    add(1, "E_DEPTH_LIMIT", path + ("children",), "nesting", "Generic component children are not permitted")
            if isinstance(value, str):
                for code, rule, message in policy_violations(value, rendered=path in rendered):
                    add(4, code, path, rule, message)
        return finish()
