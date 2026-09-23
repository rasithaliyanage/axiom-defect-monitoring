"""Executable coverage of the updated v1 contract and documented local choices."""

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator
import pytest

from services.domain.validation_models import GroundedContext, InvalidContextError
from services.domain.validator import SCHEMA_PATH, UISpecValidator


BLOCKS = [
    {"component": "Hero", "props": {"title": "Board inspection", "eyebrow": "Activity", "subtitle": "Recorded information", "primaryAction": "view-inspection-queue"}},
    {"component": "Heading", "props": {"level": 2, "text": "Inspection activity"}},
    {"component": "Text", "props": {"text": "Recorded information", "tone": "muted"}},
    {"component": "FeatureCard", "props": {"title": "History", "body": "Recorded activity", "capabilityId": "history", "icon": "inspection"}},
    {"component": "FeatureGrid", "props": {"columns": 2, "items": [
        {"title": "History", "body": "Recorded activity", "capabilityId": "history"},
        {"title": "Reports", "body": "Inspection summaries"},
    ]}},
    {"component": "CTA", "props": {"label": "Open reports", "action": "view-defect-reports", "variant": "primary"}},
    {"component": "Alert", "props": {"severity": "warning", "title": "Recent observations", "body": "Review the recorded activity", "alertId": "alert-one", "defectCategoryId": "solder-bridge"}},
    {"component": "InfoPanel", "props": {"title": "This shift", "rows": [
        {"metricId": "boards-inspected-shift", "label": "Boards inspected", "value": "1,284"},
        {"metricId": "defect-rate-shift", "label": "Defect rate", "value": "2.4", "unit": "%"},
    ]}},
    {"component": "ProgressIndicator", "props": {"metricId": "defect-rate-shift", "label": "Defect rate", "value": 2.4, "caption": "Current shift"}},
]


def codes(result):
    return {r.code for r in result.rejections}


def check_invalid(validator, spec, context, *expected):
    result = validator.validate(spec, context)
    assert result.status == "INVALID"
    assert set(expected) <= codes(result)
    return result


@pytest.mark.parametrize("block", BLOCKS, ids=lambda b: b["component"])
def test_every_approved_component(validator, spec, context, block):
    spec["blocks"] = [deepcopy(block)]
    assert validator.validate(spec, context).status == "VALID"


def test_all_components_and_hero_cta_text(validator, spec, context):
    spec["blocks"] = deepcopy(BLOCKS)
    assert validator.validate(spec, context).status == "VALID"
    spec["blocks"] = [deepcopy(BLOCKS[i]) for i in (0, 5, 2)]
    assert validator.validate(json.dumps(spec), context).status == "VALID"


@pytest.mark.parametrize("count,valid", [(0, False), (1, True), (12, True), (13, False)])
def test_block_boundaries(validator, spec, context, count, valid):
    spec["blocks"] *= count
    assert (validator.validate(spec, context).status == "VALID") == valid
    if not valid:
        check_invalid(validator, spec, context, "E_SCHEMA", "E_SIZE_LIMIT")


@pytest.mark.parametrize("name", ["run_query", "DispositionControl", "CustomChart", "hero", "", [], None])
def test_unknown_component(validator, spec, context, name):
    spec["blocks"][0]["component"] = name
    check_invalid(validator, spec, context, "E_SCHEMA", "E_UNKNOWN_COMPONENT")


@pytest.mark.parametrize("key", ["specVersion", "page", "contextId", "blocks"])
def test_required_envelope_fields(validator, spec, context, key):
    del spec[key]
    check_invalid(validator, spec, context, "E_SCHEMA")


@pytest.mark.parametrize("key", ["component", "props"])
def test_required_block_fields(validator, spec, context, key):
    del spec["blocks"][0][key]
    check_invalid(validator, spec, context, "E_SCHEMA")


@pytest.mark.parametrize("change", [
    {"specVersion": "2.0"}, {"page": "inspection"}, {"contextId": 1},
    {"blocks": {}}, {"blocks": [None]}, {"blocks": [{"component": "Text", "props": []}]},
    {"unexpected": True},
])
def test_invalid_envelope_shapes(validator, spec, context, change):
    spec.update(change)
    check_invalid(validator, spec, context, "E_SCHEMA")


@pytest.mark.parametrize("props", [
    {}, {"text": 5}, {"text": "Activity", "tone": "loud"},
    {"text": "Activity", "onClick": "handler"}, {"text": "Activity", "url": "https://internal"},
])
def test_closed_props_and_required_props(validator, spec, context, props):
    spec["blocks"][0]["props"] = props
    check_invalid(validator, spec, context, "E_SCHEMA", "E_PROP_INVALID")


@pytest.mark.parametrize("name,field,limit", [
    ("Hero", "eyebrow", 40), ("Hero", "title", 80), ("Hero", "subtitle", 200),
    ("Heading", "text", 80), ("Text", "text", 500),
    ("FeatureCard", "title", 60), ("FeatureCard", "body", 240), ("CTA", "label", 40),
    ("Alert", "title", 80), ("Alert", "body", 300), ("InfoPanel", "title", 60),
    ("ProgressIndicator", "label", 40), ("ProgressIndicator", "caption", 120),
])
def test_string_boundaries(validator, spec, context, name, field, limit):
    block = deepcopy(next(b for b in BLOCKS if b["component"] == name))
    spec["blocks"] = [block]
    block["props"][field] = "a" * limit
    assert validator.validate(spec, context).status == "VALID"
    block["props"][field] += "a"
    check_invalid(validator, spec, context, "E_SCHEMA", "E_TEXT_POLICY")
    block["props"][field] = ""
    check_invalid(validator, spec, context, "E_SCHEMA", "E_TEXT_POLICY")


@pytest.mark.parametrize("kind,count,valid", [
    ("FeatureGrid", 1, False), ("FeatureGrid", 2, True), ("FeatureGrid", 6, True), ("FeatureGrid", 7, False),
    ("InfoPanel", 0, False), ("InfoPanel", 1, True), ("InfoPanel", 8, True), ("InfoPanel", 9, False),
])
def test_grid_and_row_boundaries(validator, spec, context, kind, count, valid):
    block = deepcopy(next(b for b in BLOCKS if b["component"] == kind))
    key = "items" if kind == "FeatureGrid" else "rows"
    block["props"][key] = [deepcopy(block["props"][key][0]) for _ in range(count)]
    spec["blocks"] = [block]
    assert (validator.validate(spec, context).status == "VALID") == valid


@pytest.mark.parametrize("name,key,value", [
    ("Heading", "level", 1), ("Heading", "level", True), ("FeatureGrid", "columns", 4),
    ("FeatureCard", "icon", "camera"), ("Alert", "severity", "fatal"), ("CTA", "variant", "danger"),
    ("ProgressIndicator", "value", True), ("ProgressIndicator", "value", -1), ("ProgressIndicator", "value", 101),
])
def test_invalid_enum_and_numeric_types(validator, spec, context, name, key, value):
    block = deepcopy(next(b for b in BLOCKS if b["component"] == name))
    block["props"][key] = value
    spec["blocks"] = [block]
    check_invalid(validator, spec, context, "E_SCHEMA", "E_PROP_INVALID")


@pytest.mark.parametrize("name", ["Hero", "InfoPanel", "FeatureCard"])
def test_no_generic_children(validator, spec, context, name):
    block = deepcopy(next(b for b in BLOCKS if b["component"] == name))
    block["props"]["children"] = [{"component": "run_query", "props": {}}]
    spec["blocks"] = [block]
    check_invalid(validator, spec, context, "E_SCHEMA", "E_DEPTH_LIMIT", "E_UNKNOWN_COMPONENT")


def test_grid_accepts_card_props_not_block_envelopes(validator, spec, context):
    grid = deepcopy(BLOCKS[4])
    grid["props"]["items"][0] = deepcopy(BLOCKS[3])
    spec["blocks"] = [grid]
    check_invalid(validator, spec, context, "E_SCHEMA", "E_DEPTH_LIMIT")


def test_nested_card_props_are_closed_and_grounded(validator, spec, context):
    grid = deepcopy(BLOCKS[4])
    grid["props"]["items"][1]["capabilityId"] = "invented"
    grid["props"]["items"][1]["unknown"] = True
    spec["blocks"] = [grid]
    result = check_invalid(validator, spec, context, "E_PROP_INVALID", "E_UNGROUNDED_CAPABILITY")
    assert any(r.path == "/blocks/0/props/items/1/capabilityId" for r in result.rejections)


@pytest.mark.parametrize("action", ["view-inspection-queue", "view-defect-reports", "view-ingest-activity", "open-documentation", "contact-support"])
@pytest.mark.parametrize("name,field", [("CTA", "action"), ("Hero", "primaryAction")])
def test_all_actions_need_both_approval_and_context(validator, spec, context, action, name, field):
    block = deepcopy(next(b for b in BLOCKS if b["component"] == name))
    block["props"][field] = action
    spec["blocks"] = [block]
    assert validator.validate(spec, context).status == "VALID"
    context["actions"] = [a for a in context["actions"] if a["id"] != action]
    check_invalid(validator, spec, context, "E_UNKNOWN_ACTION")


@pytest.mark.parametrize("name,field", [("CTA", "action"), ("Hero", "primaryAction")])
def test_context_cannot_authorize_unknown_action(validator, spec, context, name, field):
    block = deepcopy(next(b for b in BLOCKS if b["component"] == name))
    block["props"][field] = "approve-board"
    context["actions"].append({"id": "approve-board", "label": "Action"})
    spec["blocks"] = [block]
    check_invalid(validator, spec, context, "E_UNKNOWN_ACTION")


@pytest.mark.parametrize("key,value,code", [
    ("alertId", "absent", "E_PROP_INVALID"),
    ("defectCategoryId", "missing-component", "E_UNKNOWN_DEFECT_CATEGORY"),
    ("defectCategoryId", "invented", "E_UNKNOWN_DEFECT_CATEGORY"),
])
def test_alert_grounding(validator, spec, context, key, value, code):
    block = deepcopy(BLOCKS[6]); block["props"][key] = value
    spec["blocks"] = [block]
    check_invalid(validator, spec, context, code)


@pytest.mark.parametrize("field,value", [("metricId", "absent"), ("value", "1284"), ("value", "1,300"), ("unit", "boards")])
def test_info_panel_verbatim_metric(validator, spec, context, field, value):
    panel = deepcopy(BLOCKS[7]); panel["props"]["rows"][0][field] = value
    spec["blocks"] = [panel]
    check_invalid(validator, spec, context, "E_UNGROUNDED_METRIC")


def test_optional_unit_may_be_omitted(validator, spec, context):
    panel = deepcopy(BLOCKS[7]); del panel["props"]["rows"][1]["unit"]
    spec["blocks"] = [panel]
    assert validator.validate(spec, context).status == "VALID"


@pytest.mark.parametrize("text,value", [("0", 0), ("100", 100), ("2.40", 2.4), ("2.4e0", 2.4)])
def test_percentage_numeric_equivalence(validator, spec, context, text, value):
    context["metrics"][1]["value"] = text
    progress = deepcopy(BLOCKS[8]); progress["props"]["value"] = value
    spec["blocks"] = [progress]
    assert validator.validate(spec, context).status == "VALID"


@pytest.mark.parametrize("value", ["2,4", " 2.4", "2.4%", "NaN", "Infinity", "+2.4", "02.4", "2_4", ""])
def test_percentage_invalid_context_number(validator, spec, context, value):
    context["metrics"][1]["value"] = value
    spec["blocks"] = [deepcopy(BLOCKS[8])]
    check_invalid(validator, spec, context, "E_UNGROUNDED_METRIC")


def test_progress_wrong_value_or_unit(validator, spec, context):
    context["metrics"][1]["unit"] = "count"
    progress = deepcopy(BLOCKS[8]); progress["props"]["value"] = 3
    spec["blocks"] = [progress]
    result = check_invalid(validator, spec, context, "E_UNGROUNDED_METRIC")
    assert {r.rule for r in result.rejections if r.code == "E_UNGROUNDED_METRIC"} == {"numeric_match", "percentage_unit"}


def test_raw_json_decimal_not_rounded(validator, spec, context):
    context["metrics"][1]["value"] = "2.40000000000000000001"
    spec["blocks"] = [deepcopy(BLOCKS[8])]
    text = json.dumps(spec).replace('"value": 2.4', '"value": 2.40000000000000000001')
    assert validator.validate(text, context).status == "VALID"
    check_invalid(validator, spec, context, "E_UNGROUNDED_METRIC")


def test_context_equality(validator, spec, context):
    spec["contextId"] = "other"
    result = check_invalid(validator, spec, context, "E_CONTEXT_MISMATCH")
    assert next(r for r in result.rejections if r.code == "E_CONTEXT_MISMATCH").path == "/contextId"


def test_total_text_exact_boundary_and_nested_counting(validator, spec, context):
    spec["blocks"] = [{"component": "Text", "props": {"text": "a" * 500}} for _ in range(8)]
    assert validator.validate(spec, context).status == "VALID"
    spec["blocks"].append({"component": "Heading", "props": {"level": 2, "text": "a"}})
    result = check_invalid(validator, spec, context, "E_SIZE_LIMIT")
    assert "E_SCHEMA" not in codes(result)
    spec["blocks"] = [deepcopy(BLOCKS[4]) for _ in range(3)]
    for b in spec["blocks"]:
        b["props"]["items"] = [{"title": "a" * 60, "body": "a" * 240} for _ in range(6)]
    check_invalid(validator, spec, context, "E_SIZE_LIMIT")


def test_total_text_unicode_code_points_not_bytes(validator, spec, context):
    spec["blocks"] = [{"component": "Text", "props": {"text": "é" * 500}} for _ in range(8)]
    assert len(json.dumps(spec, ensure_ascii=False).encode("utf-8")) > 8192
    assert validator.validate(spec, context).status == "VALID"


def test_no_imported_total_node_limit(validator, spec, context):
    spec["blocks"] = [{"component": "FeatureGrid", "props": {"columns": 3, "items": [
        {"title": "a", "body": "b"} for _ in range(6)]}} for _ in range(12)]
    assert validator.validate(spec, context).status == "VALID"  # 84 instances, all locally bounded.


@pytest.mark.parametrize("text,expected", [
    ("<script>alert(1)</script>", {"E_TEXT_POLICY", "E_CODE_LIKE_CONTENT"}),
    ("<b>Activity</b>", {"E_TEXT_POLICY"}), ("&amp;", {"E_TEXT_POLICY"}),
    ("**Activity**", {"E_TEXT_POLICY"}), ("# Activity", {"E_TEXT_POLICY"}),
    ("https://internal/dashboard", {"E_TEXT_POLICY"}), ("www.example.com", {"E_TEXT_POLICY"}),
    ("support@example.com", {"E_TEXT_POLICY"}), ("C:\\records\\file.txt", {"E_TEXT_POLICY"}),
    ("/var/records", {"E_TEXT_POLICY"}), ("Activity 😀", {"E_TEXT_POLICY"}),
    ("${run()}", {"E_CODE_LIKE_CONTENT"}), ("{{ secret }}", {"E_CODE_LIKE_CONTENT"}),
    ("SELECT data FROM boards", {"E_CODE_LIKE_CONTENT"}), ("rm -rf files", {"E_CODE_LIKE_CONTENT"}),
    ("Batch 7781 fails inspection", {"E_DECISION_LANGUAGE"}), ("Do not ship this batch.", {"E_DECISION_LANGUAGE"}),
    ("safe to ship", {"E_DECISION_LANGUAGE"}), ("This batch is approved", {"E_DECISION_LANGUAGE"}),
    ("As an AI, I generated this", {"E_TEXT_POLICY"}),
])
def test_text_policy(validator, spec, context, text, expected):
    spec["blocks"][0]["props"]["text"] = text
    check_invalid(validator, spec, context, *expected)


def test_decision_word_boundaries(validator, spec, context):
    spec["blocks"][0]["props"]["text"] = "Review the recorded activity and compass heading"
    assert validator.validate(spec, context).status == "VALID"


def test_policy_covers_nested_and_metric_text(validator, spec, context):
    spec["blocks"] = [deepcopy(BLOCKS[4]), deepcopy(BLOCKS[7])]
    spec["blocks"][0]["props"]["items"][0]["body"] = "Batch approved"
    context["metrics"][0]["value"] = "<script>alert(1)</script>"
    spec["blocks"][1]["props"]["rows"][0]["value"] = context["metrics"][0]["value"]
    result = check_invalid(validator, spec, context, "E_DECISION_LANGUAGE", "E_CODE_LIKE_CONTENT", "E_TEXT_POLICY")
    assert "E_UNGROUNDED_METRIC" not in codes(result)


@pytest.mark.parametrize("raw", [None, [], 1, True, "not JSON", "{} trailing", '{"page": "a", "page": "b"}',
                                 '{"value": NaN}', float("nan"), {1: "invalid key"}, {"bad": object()}, {"bad": "\ud800"}])
def test_malformed_input_is_structured_failure(validator, context, raw):
    result = check_invalid(validator, raw, context, "E_SCHEMA")
    assert "Traceback" not in result.model_dump_json()


def test_cyclic_input(validator, context):
    raw = {}; raw["self"] = raw
    check_invalid(validator, raw, context, "E_SCHEMA")


def test_superseded_refusal_and_reference_progress_are_invalid(validator, spec, context):
    check_invalid(validator, {"view": "landing", "refusal": "insufficient_context", "components": []}, context, "E_SCHEMA")
    spec["blocks"] = [{"type": "ProgressIndicator", "ref": "metrics.shift_progress"}]
    check_invalid(validator, spec, context, "E_SCHEMA")


@pytest.mark.parametrize("invalid", [False, True])
def test_determinism_and_non_mutation(validator, spec, context, invalid):
    spec["blocks"] = deepcopy(BLOCKS)
    if invalid:
        spec["contextId"] = "wrong"
        spec["blocks"][1]["props"].update({"text": "Batch approved", "extra": 1})
        spec["blocks"][8]["props"]["value"] = 8
    original = deepcopy((spec, context))
    results = [validator.validate(spec, context).model_dump_json() for _ in range(10)]
    assert len(set(results)) == 1
    assert (spec, context) == original
    reversed_spec = dict(reversed(list(spec.items())))
    assert validator.validate(reversed_spec, context).model_dump_json() == results[0]


def test_all_gates_and_stable_result(validator, spec, context):
    spec["contextId"] = "wrong"
    spec["blocks"][0]["props"] = {"text": "Batch approved", "extra": 1}
    result = check_invalid(validator, spec, context, "E_SCHEMA", "E_PROP_INVALID", "E_CONTEXT_MISMATCH", "E_DECISION_LANGUAGE")
    assert [r.gate for r in result.rejections] == sorted(r.gate for r in result.rejections)
    assert set(result.model_dump()) == {"status", "rejections"}
    assert all(set(r.model_dump()) == {"gate", "code", "path", "rule", "message"} for r in result.rejections)
    with pytest.raises(Exception):
        result.status = "VALID"


def test_discriminator_diagnostics_exclude_other_components(validator, spec, context):
    spec["blocks"][0]["props"] = {"tone": "default"}
    result = check_invalid(validator, spec, context, "E_SCHEMA", "E_PROP_INVALID")
    assert {r.rule for r in result.rejections} == {"required"}
    assert len(result.rejections) == 2


def test_every_missing_and_extra_prop_has_an_exact_pointer(validator, spec, context):
    spec["blocks"] = [{"component": "FeatureCard", "props": {"x/y~z": True, "another": 1}}]
    result = check_invalid(validator, spec, context, "E_SCHEMA", "E_PROP_INVALID")
    schema_paths = {r.path for r in result.rejections if r.code == "E_SCHEMA"}
    assert schema_paths == {"/blocks/0/props/title", "/blocks/0/props/body",
                            "/blocks/0/props/x~1y~0z", "/blocks/0/props/another"}
    assert len(result.rejections) == 8


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "wrong_type", "null_unit", "alert_category"])
def test_invalid_context_is_caller_error(validator, spec, context, mutation):
    if mutation == "missing": del context["metrics"]
    if mutation == "duplicate": context["metrics"].append(deepcopy(context["metrics"][0]))
    if mutation == "wrong_type": context["metrics"][0]["value"] = 1284
    if mutation == "null_unit": context["metrics"][0]["unit"] = None
    if mutation == "alert_category": context["alerts"][0]["defectCategoryId"] = "absent"
    with pytest.raises(InvalidContextError, match="malformed or inconsistent"):
        validator.validate(spec, context)


def test_typed_context_supported(validator, spec, context):
    typed = GroundedContext.model_validate(context)
    before = typed.model_dump()
    assert validator.validate(spec, typed).status == "VALID"
    assert typed.model_dump() == before


def test_validate_does_not_read_files_after_construction(validator, spec, context, monkeypatch):
    def forbidden(*args, **kwargs): raise AssertionError("Unexpected file access")
    monkeypatch.setattr(Path, "read_text", forbidden)
    assert validator.validate(spec, context).status == "VALID"


def test_schema_meta_validation_coverage_and_contract_example(validator, context):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    definitions = schema["$defs"]
    actual = {definitions[r["$ref"].split("/")[-1]]["properties"]["component"]["const"] for r in definitions["Block"]["oneOf"]}
    assert actual == {b["component"] for b in BLOCKS}
    assert set(definitions["CtaProps"]["properties"]["action"]["enum"]) == {a["id"] for a in context["actions"]}
    contract = (SCHEMA_PATH.parents[1] / "model-contracts.md").read_text(encoding="utf-8")
    example = json.loads(re.search(r"## Example of valid output.*?```json\s*(.*?)```", contract, re.S)[1])
    Draft202012Validator(schema).validate(example)
    context["contextId"] = example["contextId"]
    assert validator.validate(example, context).status == "VALID"


def test_external_schema_reference_is_not_fetched(tmp_path):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema["properties"]["blocks"]["items"]["$ref"] = "https://invalid.example/schema"
    path = tmp_path / "schema.json"; path.write_text(json.dumps(schema), encoding="utf-8")
    with pytest.raises(ValueError, match="must be local"):
        UISpecValidator(path)
