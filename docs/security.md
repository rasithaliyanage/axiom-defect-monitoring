# Security posture

Scope: Phase 0, the engineering foundation and the landing-page slice. This describes what is true
today and what each deferral depends on — it is not a target-state security architecture.

## Access control

**No authentication subsystem exists, by decision.** The application is internal, access is
controlled at the network level, and the current slice is read-only: nothing it renders can change
the state of a board.

**This deferral expires** the moment the UI can submit an action that changes board state — a
disposition, an override, or a quality decision. At that point authentication, authorisation and
attribution become prerequisites, not enhancements, because an unattributed quality decision is not
auditable. Recording *who* decided is the point, not gating access.

Per `CLAUDE.md` rule 7, do not add login pages, token issuance, session management or user tables in
this phase.

## The model as an untrusted input source

Model output is treated as untrusted data throughout. The controls are structural, not advisory:

| Control | Where enforced |
|---|---|
| Output is data, never executable content | Schema validation; nothing is evaluated or parsed as markup |
| Only registered components can render | Component registry, own-property lookup only |
| No dynamic execution path | No `eval`, `new Function`, `dangerouslySetInnerHTML` or model-driven dynamic import — asserted by a source scan in `apps/ui/test/safety.test.tsx` |
| No prop reaches the DOM unchecked | Components destructure named props; nothing from a specification is spread onto an element |
| Model holds no data values | The model names references; the Domain Runtime resolves them |
| Model reaches no system | No database connection, no image repository access, no command-executing tool |

The last two matter most. A model that can pass a value through can pass a wrong one, and a model
with a tool can be induced to use it.

## Injection

Text arriving in a UI specification is rendered as text, so it is escaped by default. Gate 4
additionally rejects markup, code-like content, URLs, email addresses and paths in displayed
strings. Probes covering script tags, event-handler attributes, template expressions and
`javascript:` URLs are in `apps/ui/test/safety.test.tsx`.

Prompt injection reaching the model through grounded context is **not addressed in this phase**.
Context is assembled from domain data, and no untrusted document or image caption currently enters
it. That changes the moment board metadata or operator free-text does.

## Logging

`CLAUDE.md` requires logging the grounded context identifier, the raw model output, the validation
outcome and every rejection code — this is the evidence base for evals and incident review.

Do not log image content, or anything identifying a board serial beyond what the domain layer
already exposes. No logging pipeline is implemented yet.

## Data protection

Retention periods, anonymisation scope and residency constraints for captured images and inspection
metadata are **undecided** and owned by Quality and Compliance (BRD §26, Q17). No image data is
handled in this phase.

## Not in scope this phase

Authentication and authorisation subsystems, secrets management, network segmentation between the
factory and enterprise tiers, OT/IT boundary controls, audit retention, and deployment hardening.

If a task appears to require one of these, stop and say so rather than building a partial version.
