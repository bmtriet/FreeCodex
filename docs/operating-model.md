# Operating Model

FreeCodex uses a simple loop:

1. Capture a public-safe intent.
2. Build or document the smallest useful artifact.
3. Validate it with an appropriate check.
4. Record what changed, what worked, and what should improve.
5. Promote repeated patterns into templates, scripts, or skills.

## Memory

Memory in this repo is not a dump of private context. It is a collection of sanitized patterns and public-safe facts that help future work:

- Design preferences that are safe to share.
- Technical decisions without private source material.
- Lessons learned from mistakes.
- Reusable project structures.

Private memory should live outside this public repository.

## Evaluation

Every meaningful artifact should have a clear check. Depending on the work, that can mean:

- A script or unit test.
- A rendered screenshot.
- A manual review checklist.
- A before/after comparison.
- A short failure-mode analysis.

The standard is not perfection. The standard is being able to tell whether the work actually improved.

## Skills

When a workflow repeats, document it as a skill candidate:

- Trigger: when to use it.
- Inputs: what the user or environment must provide.
- Steps: how to execute it safely.
- Checks: how to know it worked.
- Failure modes: how to stop cleanly.

Skills should start as notes, then graduate into scripts or installable skill folders when they prove useful.

## Experiments

Experiments are small, bounded attempts to learn. Each one should define:

- The question being tested.
- The artifact to build.
- The success criteria.
- The result and next step.

The workshop should value honest negative results. A failed experiment that teaches something is still useful.

