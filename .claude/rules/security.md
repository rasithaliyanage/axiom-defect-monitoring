# Rule: security

**Scope:** engineering-time guidance for Claude Code. Enforces nothing at runtime — see
[`README.md`](README.md).

**Authority:** `docs/security.md` holds the security posture, including what is deliberately
deferred and when each deferral expires. The text policy that Gate 4 applies, and the rejection
codes it emits, are in `specs/model-contracts.md`; the validation requirements are `specs/spec.md`
VR-7 and VR-8. This file restates none of them and extends none of them.

## Never introduce a dynamic execution path

These are prohibited in `apps/ui/src`, and `apps/ui/scripts/safety-lint.mjs` already fails the build
on most of them:

`eval(` · `new Function` · `innerHTML` · `insertAdjacentHTML` · `document.write` ·
`dangerouslySetInnerHTML` · `import(` (dynamic)

The lint strips comments before scanning, so prose explaining why a mechanism is banned does not trip
it. Do not weaken that scan, add an exemption, or move code out of `src/` to escape it.

Beyond the token list, the same principle covers anything that turns data into behaviour: resolving a
component by string outside the registry, spreading untrusted properties onto a DOM element,
constructing a module path from input, or passing an unvalidated value into `href`, `src`, `action`
or an event handler.

## Keep model output on the data side

Everything returning across the Domain → AI boundary is `unknown` until the validator narrows it.
Text from a specification is rendered as text and therefore escaped; Gate 4 additionally rejects
markup, code-like content and URLs. Probes for script tags, event-handler attributes, template
expressions and `javascript:` URLs live in `apps/ui/test/safety.test.tsx`.

Keep it that way. Do not add a path where generated content is parsed as markup, evaluated, or used
to select code.

## Keep errors sanitized

Every failure leaves as `{"error": {"code", "message"}}`. Two properties hold today and are each
covered by tests:

- **Validator rejection codes are logged, never serialized.** They are internal diagnostics.
- **Caller-supplied text is never echoed into a message.** An unknown line, board identifier or
  parameter name produces a fixed message; the unknown-parameter error names the *allowed* set,
  which is server-owned, rather than what was sent.

The second one was false once, in code written in this repository, and a probe caught it. Assume a
new error message is an echo path until you have checked.

## No secrets in the repository

No API key, token, credential, connection string or model credential belongs in source,
configuration, tests, fixtures, documentation or a commit message. There are none today — the
repository makes no authenticated outbound call. When the model gateway arrives it will hold the only
credential, server-side, and the browser will still hold none.

`.claude/settings.local.json` is meant to be machine-local. It is currently **tracked** and is not
listed in `.gitignore`, so anything written there is shared — treat it as a committed file until that
is resolved, and put nothing in it you would not commit.

## Never bypass a control silently

No debug flag that disables validation in a shipped build. No environment variable that skips a gate.
No test-only escape importable from production code — the safety lint already fails production code
that imports the test tree or the test-only minting helper, which is what that check is for.

If a control genuinely blocks necessary work, say so and propose the change. The unacceptable outcome
is a bypass that exists and is not visible in review.

## Do not invent security machinery

`CLAUDE.md` rule 7 and `docs/security.md` are explicit: no authentication subsystem in this phase —
no login page, token issuance, session management or user table. Likewise no secrets manager, no
network segmentation, no audit retention. These are deferred by decision, with the conditions for
revisiting them recorded.

Adding a partial version of a deferred control is worse than the deferral, because it looks like
coverage. If a task appears to require one, stop and say so.
