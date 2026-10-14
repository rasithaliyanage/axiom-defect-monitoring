# board-defect-inspection-engineering

A Claude Code plugin that packages this repository's **engineering-time** controls so they can be
installed somewhere other than this checkout.

It contains no application code. It performs no model inference, holds no credential, and is not
part of the Board Defect Inspection System's runtime.

## Why it exists

Tasks 7–9 built four engineering-time primitives: `CLAUDE.md`, rules, skills and one hook. Three of
those — the skills and the hook — are capabilities rather than prose, and a capability that is
useful in this repository is often useful in a sibling one. A plugin is the documented way to
distribute them. Nothing here is new behaviour; Task 10 is packaging, not design.

## What it packages

**Skills** — `skills/<name>/SKILL.md`

| Skill | Does |
|---|---|
| `verify-project` | Runs the existing verification suites and reports what actually happened |
| `review-uispec` | Reviews a specification-contract change against the authoritative sources |
| `checkpoint-review` | Reviews a proposed checkpoint and stops at the report |

**Hook** — `hooks/hooks.json` + `hooks/check_uispec_schema.py`

A `PostToolUse` hook on `Edit|Write|MultiEdit|NotebookEdit`. When
`specs/schemas/ui-spec.schema.json` is edited it parses the schema, meta-validates it as Draft
2020-12, and runs the project validator over the canonical fixtures. Any other path exits silently.

`PostToolUse` fires *after* a successful tool call, so the file has already changed. A failure is
reported back for correction — it does not undo the completed edit, and no exit code would.
`PreToolUse` is the event for preventing an action before it executes; this plugin contains no such
hook.

## Source of truth

**`.claude/` in this repository is authoritative. This package is a generated mirror.**

`plugin/` is a container directory; this plugin's root is the named directory inside it, which
is where `.claude-plugin/plugin.json` lives.

```
.claude/skills/<name>/SKILL.md   ──┐
.claude/hooks/check_uispec_schema.py ├── scripts/package_plugin.py ──▶ plugin/
                                   ─┘
```

The Claude Code plugin model requires a plugin's capabilities to live inside the plugin root. There
is no documented mechanism for a plugin to reference files elsewhere in a repository, and none was
invented here — so the package is a copy.

What keeps the copy honest is mechanical, not procedural:

- `scripts/package_plugin.py` regenerates the package.
- `scripts/package_plugin.py --check` reports drift and changes nothing.
- `tests/plugin/test_plugin_package.py` asserts **byte-identity** between every packaged file and
  its source, and fails if a packaged file has no source at all.

So a divergent copy is a failing test, not a thing someone has to notice in review. This mirrors
what the repository already does for `apps/ui/src/generated/fixtures.ts`: generated, committed, and
verified rather than hand-maintained.

**To change a skill or the hook, edit `.claude/` and re-run the packaging script.** Editing
anything under this package's `skills/` or `hooks/*.py` directly will be reverted by the next build
and caught by the suite in the meantime. `hooks/hooks.json` is the one authored file in the
package — it is the plugin-form hook configuration, which has no equivalent in `.claude/settings.json`.

## How this relates to the other layers

| | Answers | Binds by |
|---|---|---|
| `CLAUDE.md` | What should Claude Code know? | being read |
| Rules | How should Claude Code behave? | being read |
| Skills | What task can it perform, and how? | being read |
| Hooks | What happens automatically, on an event? | being executed |
| **Plugins** | **How are those capabilities packaged and distributed?** | **being installed** |

A plugin is a container. It changes distribution, not behaviour — the packaged skills and hook do
exactly what they did before.

**Rules are deliberately not packaged.** `.claude/rules/` is behavioural guidance specific to this
repository's architecture, and the plugin model has no rules concept. Distributing them as though
they were portable capabilities would misrepresent what they are.

## What it does not contain

No agents, no commands, no MCP configuration, no Agent SDK integration — a plugin *may* carry those,
but Task 10 packages only what already exists. No model gateway, no AI client, no runtime model
call, no authentication, no application code, no new dependency.

It does not replace the model contract, the JSON Schema, deterministic validation, runtime security
or controlled rendering. Those are runtime controls enforced by `services/domain/validator.py`, the
schema and the component registry, on every request. Delete this plugin and the application's
guarantees are unchanged.

## Installation and use — what is and is not known

The package is laid out per the documented plugin model: `.claude-plugin/plugin.json` at the plugin
root, `skills/<name>/SKILL.md`, and `hooks/hooks.json` whose command resolves through
`${CLAUDE_PLUGIN_ROOT}`. The manifest and structure are verified by `tests/plugin/`.

**Plugin structure and manifest were statically verified, but actual Claude Code plugin
discovery/installation was not independently verified.** The package has not been installed, and
`plugin.json` parsing is not evidence that it would be.

**How the hook finds the repository.** It walks up from its own location until it sees
`specs/schemas/ui-spec.schema.json`, rather than assuming a fixed depth. That matters because this
package nests the hook one level deeper than `.claude/hooks/` does, and a hard-coded depth would
resolve to the wrong directory — the hook would then match nothing and silently do nothing, which
is the worst way for a check to fail. Both locations are exercised.

**The remaining limit, stated plainly.** The search still needs the schema to be somewhere above
the hook. Installed into a plugin cache outside this repository, nothing matches and the hook exits
silently every time — correct behaviour for an unrelated checkout, but it means the hook does real
work only for a checkout that actually contains the UI specification schema. It is a
project-shaped hook; packaging makes it portable to a sibling checkout, not to any project.
