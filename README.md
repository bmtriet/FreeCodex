# FreeCodex

FreeCodex is a public workshop for making Codex a better long-running collaborator: more grounded, more testable, more reusable, and more honest about what it knows.

This repository is intentionally small at the start. It is a place to collect public-safe operating notes, evaluation patterns, reusable skill designs, and experiments that help an agent improve through visible work rather than vague promise.

## Mission

Build a practical evolution loop for Codex:

- Remember useful project context in structured, public-safe forms.
- Verify work with lightweight checks, screenshots, tests, and review notes.
- Turn repeated workflows into reusable skills and templates.
- Prototype small tools that make thinking, building, and learning easier.

## Repository Map

- `docs/` - principles, operating model, and roadmap.
- `memory/` - public-safe structured memory patterns.
- `evals/` - self-evaluation checklists and reports.
- `skills/` - reusable skill designs and implementation notes.
- `experiments/` - prototype ideas and experiment records.
- `reports/` - public-safe sample reports and sanitized audit artifacts.
- `leads/` - public-safe lead research and outreach drafts.
- `ops/` - Mission Control queue, scoreboard, and generated operating reports.
- `templates/` - copy-ready templates for repeatable work.
- `scripts/` - local validation and maintenance tools.

Revenue work starts in `docs/revenue-strategy.md` and `experiments/opportunities/`.
The first offer is documented in `docs/offer-vibe-agent-repo-safety-audit.md`.
Quota fallback is documented in `docs/llm-gateway-fallback.md`.
Mission Control starts at `ops/README.md`.

## Current Status

Status: bootstrap.

The first goal is to make the workspace safe to publish, easy to inspect, and hard to accidentally contaminate with private data.

## Public-Safety Rule

This repo is public by design. Do not commit secrets, credentials, private user data, raw chat logs, personal memory, local machine paths beyond documentation examples, or private project material.

Use public-safe summaries and sanitized examples only.

## Quick Check

Run:

```bash
python3 scripts/validate_repo.py
```

The validator checks required files/directories and scans candidate repository files for obvious secret patterns.

Refresh Mission Control:

```bash
python3 scripts/mission_control.py generate
```
