# Business problem and requirements

## Executive summary

Electronics board inspection currently depends on manual visual checks and disconnected reporting,
which makes defect trends slow to surface and inspection status hard to see at a glance. This document
states the business requirements for an internal Automated Board Defect Inspection System. It defines
what the business needs, not how the system is built.

## Context

Boards move through assembly and are inspected for surface and placement defects before they progress.
Today the operational picture is fragmented. Inspection outcomes are recorded in one place, images in
another, and summary reporting is assembled by hand for review meetings. A supervisor asking a simple
question — what is the current inspection backlog, and which defect category is trending this shift —
has no single place to look.

The organisation also intends to adopt AI as a first-class part of its internal tooling rather than as
a bolt-on. That intent creates a second, equally important need: a way to let a model shape what users
see without letting it shape what the software does.

## Problem statement

Inspection stakeholders lack a single, current, trustworthy view of board inspection activity and
defect reporting. Building that view by hand for every audience and every shift does not scale, and
building a conventional fixed interface produces a page that is immediately out of date with what the
operation actually needs to show.

## Users

Inspection operators need to understand current queue state and what to look at next.

Line supervisors need shift-level defect trends and early warning when a defect category is rising.

Quality engineers need defect reports they can export and analyse, with reliable category definitions.

Manufacturing IT needs an internal system that is auditable, that does not widen the attack surface,
and that keeps AI behaviour inside verifiable limits.

## Business requirements

Listed in descending order of priority.

BR-1. Present a single internal landing view that communicates the system's purpose, current
inspection summary statistics, and recent defect alerts, adapted to the operational situation rather
than fixed at build time.

BR-2. Keep AI behaviour provably bounded. The model may compose and word the interface; it may not
execute anything, reach data directly, or extend the system's stated capabilities. This is a condition
of approval for internal deployment, not a preference.

BR-3. Ensure no AI output can constitute a quality decision. Statements that a board passes, fails, is
approved, or is fit to ship must never originate from the model. Such determinations remain with
qualified personnel and with systems outside this scope.

BR-4. Report only real defect categories and real capabilities. A category or capability the
organisation does not have must never appear on screen, because a fabricated category silently
corrupts downstream quality analysis and erodes trust in the whole system.

BR-5. Provide a domain interface for board inspection, image ingest metadata, and defect reporting
that later phases can build on without rework.

BR-6. Degrade safely. If AI generation fails, is slow, or is rejected, users still see a usable page.
An unavailable model must not produce an unavailable application.

BR-7. Keep the initial delivery small and verifiable, so that the control mechanism is proven before
the surface area grows.

## Constraints

Internal use only. Access is controlled at the network level for this phase, so the system must not
build its own authentication subsystem.

Existing manufacturing systems are not to be touched in this phase. No PLC or MES integration, no
camera or edge processing, no changes to how images are captured.

The organisation must be able to audit what the model was given and what it returned. Model
interactions are recorded.

## Success measures

A stakeholder can open the landing view and, without training, state the system's purpose, the current
inspection summary, and any active defect alert.

Every rendered element traces to an approved component and every referenced figure traces to
domain-supplied context. No exceptions in review.

No rendered text asserts a pass, fail, or approval outcome.

When AI generation is disabled or failing, the landing view still loads and remains informative.

## Out of scope for this phase

Physical camera integration. Edge image processing. Real-time PLC or MES signal handling. Automated
defect classification models. Human review override workflows. Production infrastructure.
Authentication and authorisation subsystems. Multi-language content. Mobile-specific interfaces.

## Risk boundaries

The primary risk in a model-driven interface is not a poorly worded heading. It is an AI output path
that becomes an execution path, a data access path, or a decision path. The architecture in
`docs/architecture.md` and the contract in `specs/model-contracts.md` exist to close those three paths,
and the requirements above are the reason they are closed rather than merely discouraged.
