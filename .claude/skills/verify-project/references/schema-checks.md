# Reference: schema checks

Supporting detail for step 4 of [`../SKILL.md`](../SKILL.md). Split out because the distinctions
below are the ones people collapse, and they need more room than a procedure step should take.

**This file defines nothing.** The UI specification contract lives in
`specs/schemas/ui-spec.schema.json`, `specs/model-contracts.md` and `specs/spec.md`. Nothing here
restates a component, a prop, a rejection code or a limit — read those. This is only how to check
that what exists still holds together, and how to report it.

## Four different things, routinely conflated

Each answers a different question, and each can pass while the next fails. Report them as separate
rows; a single "schema: OK" hides which one you actually ran.

| Check | Question | Passing proves |
|---|---|---|
| **Parsing** | Is the schema file well-formed JSON? | The file loads. Nothing about its correctness |
| **Meta-validation** | Is it a legal Draft 2020-12 schema? | The schema itself is valid. Nothing about any instance |
| **Instance validation** | Does a given specification conform? | Gate 1 only — structure, limits, depth |
| **Full runtime validation** | Does it pass all four gates against its context? | Structure *and* registry, grounding and text policy |

The last two are the pair most often merged. A specification can be structurally perfect and still
reference a metric that does not exist in its grounded context — that is a Gate 3 failure the schema
cannot see, because grounding is a relationship between two documents and the schema only ever sees
one.

## Which schema

`services/domain/validator.py` loads `specs/schemas/ui-spec.schema.json`. That is the authority.

`specs/ui-spec.schema.json` carries `"deprecated": true` and is never merged. The current suite does
**not** meta-validate it. If you report on schema health, say which file you checked — claiming "the
schema validates" while having checked only one of two files that share a name is the kind of
imprecision this project tries not to commit.

## Running them

Instance and full validation are already covered by the suite:

```bash
.venv/Scripts/python.exe -m pytest -q \
  tests/validator/test_task4_fixtures.py \
  tests/validator/test_fallback_spec.py
```

`test_task4_fixtures.py` runs the validator over each `<name>.spec.json` / `<name>.context.json`
pair in `tests/fixtures/ui-spec/` and asserts `VALID`. `test_fallback_spec.py` additionally asserts
the fallback is context-independent — valid against an empty context, its own, and an unrelated
populated one. That last property is what makes the fallback safe to serve when everything else has
failed, so a change there deserves attention.

Parsing and meta-validation are not in the suite. Run them explicitly:

```bash
.venv/Scripts/python.exe -I -c "
import json, jsonschema
s = json.load(open('specs/schemas/ui-spec.schema.json'))
V = jsonschema.validators.validator_for(s)
V.check_schema(s)
print('parses and meta-validates:', V.__name__)
"
```

Expect `Draft202012Validator`. A different validator class means the `$schema` dialect changed,
which is a contract change and needs the four-artefact treatment `CLAUDE.md` requires — not a
passing check.

## Reporting

```
schema   15 passed (fixtures + fallback); loaded schema parses and
         meta-validates as Draft 2020-12; deprecated specs/ui-spec.schema.json
         not meta-validated by the suite
```

Report the count you saw. If it differs from a number in a task prompt or an older document, the
suite is right and the document is stale — and that gap is worth reporting on its own.

## What a passing schema check does not establish

It says nothing about whether the renderer is safe, whether a figure is grounded in real data, or
whether text implies a quality verdict. Gate 4 in particular is a set of deterministic patterns, not
a semantic guarantee — `docs/quality-gates.md` states that limitation plainly, and it is why
`evals/` exists.

And `VALID` refers to a UI specification. It never means a board passed, failed or was approved.
