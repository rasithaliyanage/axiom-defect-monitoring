---
name: checkpoint-review
description: Review a proposed engineering checkpoint before anyone commits it — diff, scope, protected surfaces, regressions, dependencies, artifacts. Use when asked to review a checkpoint, verify work before committing, or confirm a change set matches its declared task.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# checkpoint-review

Independently review a proposed checkpoint and produce the evidence a human needs in order to decide
whether to commit it.

**This skill stops at the report.** It never commits, pushes, merges, deletes or reverts. Deciding
to publish is a human action; this skill exists to make that decision informed, not to pre-empt it.

## Governed by

`.claude/rules/testing.md` for what counts as evidence. `.claude/rules/security.md` for the
security pass. The Task 7 checkpoint in this repository is the worked example of the output.

## Procedure

**1. Establish the baseline — do not take it on trust.**

```bash
git branch --show-current
git log --oneline -5
git cat-file -t <claimed-baseline>      # confirm it exists
git rev-parse HEAD origin/<branch>
```

A baseline hash quoted in a task prompt is a claim. Verify it resolves in *this* repository. If it
does not, say so, state the real HEAD, and carry on against that — do not silently substitute one
and report as though the premise held.

**2. Inspect the working tree.** `git status --short`, then `git diff --stat` and
`git diff --name-only`. Read the full diff, not just the stat.

**3. Classify every path** as expected for the declared task, or not. Both lists go in the report.
Unexpected files are the single most useful thing this review produces — uncommitted work from an
earlier task, a stray generated file, an editor artifact.

**4. Check protected surfaces.** Confirm whether the change touched the specification, schema,
validator, registry, renderer or API. If it did and the task said it would not, that is a finding.

Resolve paths against this repository rather than a prompt's wording — a task may name
`ui/src/registry.ts` when the real path is `apps/ui/src/renderer/registry.ts`. When a named path does
not exist, say so and state which real file you checked.

Attribute changes honestly: a modified file is not evidence *this* task modified it. Cross-check
mtimes against when the work was done before blaming the wrong change.

**5. Run the regression suites.** Use the `verify-project` skill rather than restating its
procedure; its `verify-project/references/schema-checks.md` covers the schema reporting. Report the actual numbers,
never a baseline quoted from a document.

**6. Security pass.** Dangerous APIs, arbitrary component resolution, model SDK, secrets, bypassed
boundaries. Distinguish a real hit from a match inside a comment or a test probe string.

**7. Dependencies.** `requirements.txt`, `apps/ui/package.json`, `apps/ui/package-lock.json`.
Report any change, however small; "none" is the usual and expected answer.

**8. Generated artifacts.** Confirm `__pycache__`, `.pytest_cache`, `node_modules`, `dist/`, `.env`
and logs are untracked. Locally present and ignored is fine; tracked is a finding.

**9. Application smoke checks — optional, and only when the change could affect them.** Skip this
for a documentation or engineering-time change and say you skipped it; running it proves nothing
about a Markdown edit. Run it when the diff touches the API, the renderer, the client or the proxy.

The established procedure is in `apps/ui/README.md`, and `specs/task6-browser-evidence/README.md`
is the worked example of what the output looked like last time.

```bash
# repository root
.venv/Scripts/python.exe -m uvicorn services.domain.api.main:app --host 127.0.0.1 --port 8000

curl http://127.0.0.1:8000/health                          # {"status":"ok"}
curl http://127.0.0.1:8000/api/v1/inspection/queue          # records + meta
curl "http://127.0.0.1:8000/api/v1/inspection/queue?line=line-z"   # 400, Unknown line
curl http://127.0.0.1:8000/api/v1/inspection/board/BRD-nope # 404, BOARD_NOT_FOUND

curl -H 'Content-Type: application/json'      -d '{"page":"landing","view":"overview","locale":"en-US"}'      http://127.0.0.1:8000/api/v1/ui/landing-page           # 200
```

Check the failure paths, not just the happy one — a rejection that returns the wrong code or echoes
caller text is the kind of regression a 200 never reveals.

For the browser layer, `npm run dev` in `apps/ui` and confirm the page renders from the Domain
Runtime rather than a fixture. Note that Vite may bind IPv6-only, so a `127.0.0.1:5173` probe can
report nothing while the server is running — use `localhost:5173`.

**Stop every service you started** and confirm the listeners are released. Leaving a port held is
a side effect a review should not have.

**10. Scope.** Does the change set match what the task declared? Both directions matter — work that
crept in, and work that was declared but is missing.

**11. Report.** Files added and modified, lines changed, suite results, findings, and anything
unexpected. State what you could not verify.

## Stop conditions

**If anything unexpected is found, stop and report it.** Do not fix unrelated changes, do not
restage, do not tidy the tree. An unexpected file is information for a human; silently resolving it
destroys exactly the signal the review exists to produce.

Likewise stop and ask when the obvious next step would commit or push something whose premise did
not hold — a wrong branch, a missing baseline, or a tree containing more than the declared task.

## Boundaries, and how they are held

Nothing in the tool allowlist prevents a `git commit`. The allowlist is coarse: this skill needs
`Bash` to run the suites, and that grants more than it needs. The prohibition above is therefore an
instruction, not a mechanism — which is exactly the distinction `.claude/rules/README.md` draws, and
it applies to this skill as much as to anything else.

So treat it as load-bearing: produce the report and stop, even when committing looks obviously
correct and even when the task text asks for it. The human has context this review does not.
