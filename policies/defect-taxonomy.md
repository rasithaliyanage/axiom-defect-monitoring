# Defect taxonomy

- **Owner:** Quality
- **Status:** Awaiting business definition. No values recorded.
- **Source question:** BRD §13 "Defect Taxonomy" and §14 "Defect Severity"

## What this file must eventually contain

The authoritative list of defect categories the system inspects for, and the severity classification
of each.

| Field | Awaiting |
|---|---|
| Category identifier | Stable machine identifier per defect category |
| Display label | Human-readable name |
| Severity | Classification and what that classification obliges |
| Localization required | Whether the defect's position on the board must be reported |
| Applicable board types | Whether the category applies to all variants or some |

## Why nothing is filled in

BRD §13 presents a table of six example defects and states explicitly:

> "These are examples only. The manufacturing/quality team must define the actual taxonomy."

BRD §14 lists suggested severity bands and states:

> "The actual classification must be provided by the Quality team."

Copying the BRD's examples into this file would convert an illustration into an apparent
requirement. They are therefore not reproduced here.

## Note on identifiers already present in code

`specs/schemas/ui-spec.schema.json` constrains `Alert.defectCategoryId` to a fixed enum, and
`services/domain/validator.py` enforces it. Those identifiers exist so the schema can be closed
rather than permissive — they are a **structural placeholder, not an approved taxonomy**. When
Quality supplies the real taxonomy, that enum is expected to change, and the change is a contract
change requiring all four artefacts listed under "Contract changes are wide changes" in `CLAUDE.md`.

## Open questions

| Question | BRD reference |
|---|---|
| What exactly counts as a defect? | Q01 |
| What makes a defect critical, major or minor? | Q02 |
| How frequently does each defect occur? | Workshop 3 |
| Who owns ground truth, and how are inspector disagreements resolved? | Q11, §19 |
