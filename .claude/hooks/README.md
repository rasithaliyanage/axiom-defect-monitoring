# Hooks

Shell commands the harness runs automatically on Claude Code events. Unlike `CLAUDE.md`, a rule or
a skill, a hook is **executed rather than read** — so this is the first engineering-time primitive
in this repository that runs on its own, rather than waiting for someone to remember it.

Automatic is not the same as preventive, and the difference turns on which event a hook is bound
to. The one hook here is a `PostToolUse` hook: it performs **automatic post-action validation**.

**Status:** one hook.

## The hook: UI specification schema check

| | |
|---|---|
| **Event** | `PostToolUse` — after a file-editing tool succeeds |
| **Matcher** | `Edit\|Write\|MultiEdit\|NotebookEdit` |
| **Watches** | `specs/schemas/ui-spec.schema.json`, and nothing else |
| **Runs** | `.claude/hooks/check_uispec_schema.py` |
| **Configured in** | `.claude/settings.json` |

### What it does

```
Claude Code calls Write/Edit
        ↓
the file edit completes          ← already done; nothing below undoes it
        ↓
PostToolUse fires, hook receives the tool payload on stdin
        ↓
is the edited path the UISpec schema?  ── no ──▶ exit 0, silently
        ↓ yes
1. parse the schema as JSON
2. meta-validate it as Draft 2020-12
3. run the existing UISpecValidator over every canonical fixture pair
        ↓
report PASS or FAIL back to Claude Code for corrective action
```

**On success** it reports one line: the dialect and the number of fixtures that still validate.

**On failure** it says what broke and where — a JSON syntax error with line and column, an illegal
schema construct, or the fixtures that stopped validating. It surfaces that to Claude Code through
the hook's JSON output and exits `0`.

Be precise about what a failure means here. `PostToolUse` fires *after* the tool call has already
succeeded, so the file on disk has already changed by the time this hook runs. Reporting a failure
provides immediate post-edit validation feedback; it does not undo the completed edit, and it does
not mean the Write or Edit was prevented. A broken schema is usually broken *mid-repair*, so the
useful thing is to tell Claude promptly and let the next edit fix it.

**On an unrelated edit** it exits immediately and prints nothing. A hook that comments on every
file write trains people to ignore it.

### PostToolUse versus PreToolUse

`PostToolUse` runs after a successful tool call. This hook therefore validates the resulting schema
and reports failures to Claude; it does not undo the completed edit. A `PreToolUse` hook would be
the appropriate mechanism if the project later required preventing a tool action before it
executes.

That is deliberate for this check, not a limitation worked around. Validating a schema requires the
edited schema to exist, which only a post-action event can offer. Prevention is a different job and
would need a different event — and none is implemented here.

### What it does not do

It does not modify, repair, reformat or stage the schema. It does not commit, push or merge. It
does not touch runtime code, call a model, open a network connection, or read a credential. It
adds no second validator — step 3 imports the existing `services/domain/validator.py`, because a
second implementation of the contract would be a second thing to keep in sync.

### Why it is safe to run automatically

A hook runs with your permissions and no confirmation, so the design matters more than usual:

- **No shell.** It is configured in exec form — `command` plus `args` — so the script is spawned
  directly and nothing is parsed by a shell. Command injection has no surface here.
- **The input path is compared, never used.** The file path on stdin is matched against one
  location resolved from the hook script's own position on disk. It is never opened, interpolated
  into a command, or echoed. A path like `` `id` `` or `../../../../etc/passwd` simply fails to
  match and the hook exits — there is a test for each.
- **It reads one file.** The only file the hook opens is the schema it already knows about.
- **It is deterministic.** Same schema, same fixtures, same answer, every time. No clock, no
  randomness, no network.

## How this differs from the other primitives

| | Answers | Binds by |
|---|---|---|
| `CLAUDE.md` | What should Claude Code know? | being read |
| [`../rules/`](../rules/) | How should Claude Code behave? | being read |
| [`../skills/`](../skills/) | What task can it perform, and how? | being read |
| **Hooks** | What should happen automatically, on an event? | **being executed** |

A rule says *do not break the schema contract*. A skill says *here is how to review a change to
it*. This hook does neither — it waits for the schema to change and then checks it, whether or not
anyone remembered to.

**It is still not runtime enforcement.** `services/domain/validator.py`, the JSON Schema and the
component registry are what the running application enforces, on every request, for every user.
This hook runs on a developer's machine while the software is being written. If it were deleted
tomorrow, the application's guarantees would be unchanged — which is the clearest way to see that
engineering-time and runtime controls are different things.

## Verifying it yourself

Pipe the payload shape Claude Code sends, with a real absolute path:

```bash
.venv/Scripts/python.exe -c "import json,pathlib; \
  print(json.dumps({'tool_name':'Edit','tool_input':{'file_path': \
  str(pathlib.Path('specs/schemas/ui-spec.schema.json').resolve())}}))" \
| .venv/Scripts/python.exe .claude/hooks/check_uispec_schema.py
```

Deterministic tests live in `tests/hooks/test_uispec_schema_hook.py` and cover trigger, non-trigger,
pass, fail, non-modification, and the security boundaries above.

**What is not verified:** whether Claude Code actually invokes this hook on a real edit. The tests
exercise the script, and the configuration was validated against the settings schema, but automatic
invocation has not been observed end to end in this environment. Treat it as configured and
individually tested, not as demonstrated. The hook config is also read when a session starts, so a
session running when it was added will not have it loaded.

## Candidates, not yet implemented

Each corresponds to a rule the repository currently relies on documentation or a test to uphold:

| Hook | Would enforce |
|---|---|
| Pre-commit prohibition scan | `CLAUDE.md` rule 2 — reject `eval`, `new Function`, `dangerouslySetInnerHTML` or model-driven dynamic import reaching the render path |
| Pre-commit policy check | No invented value lands in `policies/` |
| Post-edit contract check | A change to the schema, vocabulary or props also touches model contract, tests and evals, per "Contract changes are wide changes" |
| Pre-commit test gate | Both suites pass before a commit is accepted |

The prohibition scan currently exists as `apps/ui/scripts/safety-lint.mjs` and a test, which catch
it in CI rather than at the moment of writing. A hook would catch it earlier; the test should
remain either way.

## Caution

A hook runs with the user's permissions and without a prompt. Keep them narrow, fast and read-only
where possible, prefer exec form over a shell string, and never make one destructive.
