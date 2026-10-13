# Skills

Reusable engineering-time capabilities for Claude Code. Each one is a task this repository needs
performed the same way every time, written down once.

**Status:** three skills.

## The three

| Skill | Use it when |
|---|---|
| [`verify-project`](verify-project/SKILL.md) | You need to know whether the project still passes — before a checkpoint, after a change, or whenever someone asks for test evidence |
| [`review-uispec`](review-uispec/SKILL.md) | A change touches the specification contract: schema, component vocabulary, props, actions, validator, registry or renderer |
| [`checkpoint-review`](checkpoint-review/SKILL.md) | Work is finished and someone is about to commit it |

They compose: `checkpoint-review` calls `verify-project` for the suite results rather than repeating
its procedure, and reaches for `review-uispec` when the diff touches the contract.

## Skills and Rules are different things

A **Rule** answers *how should Claude Code behave?* A **Skill** answers *what task can Claude Code
perform, and how is it performed here?*

| Rule says | Skill does |
|---|---|
| Do not weaken tests | Run the existing suites and report their actual results |
| Do not bypass the UISpec validation boundary | Review a UISpec change against contract, schema, validator, renderer and tests |
| Checkpoint changes must be verified | Perform a structured checkpoint review |

The rule governs; the skill performs. So a skill names the commands, the order and the output shape
— and defers the behavioural question to the rule that owns it. Where a skill would restate a rule,
it links instead.

## Where Skills sit

```
CLAUDE.md          what Claude Code should know about this project
Rules              how it should behave          .claude/rules/
Skills             what it can do, and how       here
Specifications     what the system must do       specs/, docs/
Runtime code       what is actually enforced     validator, schema, registry
Tests              what we verify automatically  tests/, apps/ui/test/
```

Skills operate at **engineering time**. They act on the repository, before anything ships. They are
not part of the running application, they are not available to a runtime model, and they enforce
nothing: like Rules, a skill binds by being read.

That last point is worth stating plainly, because a skill looks more like machinery than a rule
does. The `allowed-tools` list in a skill's frontmatter is coarse — a skill that must run the test
suites needs `Bash`, and that grants far more than running tests. When a skill says it will not
commit, that is an instruction being honoured, not a capability being withheld.

## What Skills are not responsible for

Not runtime enforcement — that is the schema, the validator and the registry. Not the specification
— a skill points at `specs/` and never copies it. Not project knowledge — that is `CLAUDE.md`. Not
behaviour — that is `.claude/rules/`.

And not Hooks, Plugins or the Agent SDK. A hook is executed by the harness rather than read, which
makes it the right home for a constraint that must actually bite; `.claude/hooks/README.md` lists
the candidates. None exists yet.

## Adding one

Add a skill when a task recurs often enough that doing it inconsistently has a cost, and when the
right way to do it here is not obvious from the repository alone. Follow the existing shape:
`<name>/SKILL.md`, frontmatter carrying `name`, a `description` that says *when to use it*, and
`allowed-tools`.

Keep the set small. Three skills that are read beat ten that are skimmed.
