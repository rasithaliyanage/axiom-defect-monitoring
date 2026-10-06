# Capture simulator

Recorded and synthetic inspection fixtures, so a slice can be built and exercised without a camera,
a production line, or live inference.

## Why this exists before it holds anything

An agent — or an engineer — with no way to exercise degraded input writes confident happy-path code.
This directory exists so that awkward inputs have somewhere to live from the start: poor image
quality, an unseen board revision, a missing board identifier, a rare defect, lighting outside the
normal range.

## Status

Empty. No slice reads it yet. The current landing-page slice renders from UI specification fixtures
in `tests/fixtures/ui-spec/`, which are a different thing: those are **model output** fixtures,
validated by `tests/validator/test_task4_fixtures.py`.

This directory is for **inspection input** fixtures — recorded captures and their metadata. It
becomes live with the inspector review panel (TASK-009), which composes a review surface over a
recorded inspection rather than a live one.

## Rules when it is populated

Fixtures are static files committed to the repository. A fixture never contains live production
output captured without review, and never contains a real customer board serial.

Anything here is **synthetic or recorded test data**, and must be labelled as such wherever it
surfaces. It is never evidence of live operation, and no screen built on it may imply otherwise.

Image binaries do not belong in this repository. When real captures are needed, this directory holds
manifests and pointers; the images live in versioned external storage with a retention policy
applied.
