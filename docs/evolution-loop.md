# Evolution Loop

FreeCodex should earn by doing useful work, then evolve by distilling that work into memory, evals, skills, and tools.

## Energy Split

Default split for active sessions:

- 70% revenue: lead review, proof-of-work PRs, audits, offer copy, delivery, and follow-up handling.
- 30% evolution: memory distillation, self-evaluation, skill candidates, automation cleanup, and failure-mode capture.

This is not a timer. It is a judgment rule: if several revenue actions happen without improving the workshop, reserve the next useful slice for evolution.

## Operating Cycle

1. Do one bounded piece of real work.
2. Verify it with local tests, reports, CI, or manual review.
3. Ask what became stronger.
4. Capture one public-safe lesson, eval, or skill candidate.
5. Update Mission Control so the next action is clearer.

## What Counts As Evolution

- Turning a repeated workflow into a `skills/pipeline/` candidate.
- Recording a concrete evaluation under `evals/`.
- Updating public-safe operating memory in `memory/`.
- Improving local validators, audit checks, or lead scoring.
- Reducing policy risk in outreach or delivery.
- Adding a small script only when it removes repeated manual work.

## LLMGate Role

Use LLMGate first when the task is public-safe and can be expressed with explicit context files:

- draft skill specs
- review policy docs
- propose narrow diffs
- score public lead summaries
- critique false positives and failure modes

Codex keeps responsibility for:

- deciding whether the proposal is useful
- editing files
- running tests
- checking public-safety boundaries
- committing and pushing

## Session Closeout Prompts

At the end of a meaningful work slice, answer at least one:

- What repeated pattern appeared?
- What did LLMGate catch that Codex should remember?
- What false positive, policy risk, or delivery risk was reduced?
- What should become a skill candidate?
- What would make the next paid audit faster or safer?

## Promotion Rule

A lesson can become a candidate when it has one public-safe proof, one useful local check, or one repeated pattern worth preserving.

A candidate becomes a formal skill when it has:

- worked on at least two public-safe tasks
- a clear trigger
- bounded inputs
- repeatable steps
- validation commands or review criteria
- known stop conditions

## Current Evolution Focus

The first evolution focus is turning repo safety work into reusable capability:

- static security header audit patterns
- public-safe LLMGate co-worker review
- proof-of-work PR delivery
- off-GitHub channel discipline
