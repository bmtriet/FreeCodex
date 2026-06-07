# Agent Safety Lab by StevenB

Agent Safety Lab by StevenB is the public-facing service for lightweight launch/readiness audits of public AI-built apps, agent workflows, and MCP servers.

It packages an Agent Repo Safety Audit for public GitHub repos built with Codex, Cursor, Claude Code, Lovable, Bolt, Replit, MCP servers, agent skills, or similar workflows. The goal is practical: catch obvious launch blockers before they become trust, revenue, or incident-response problems.

Star this repo if you want a reusable public checklist for safer AI-built launches. Open a fit-check issue if you want a public-repo scope check or paid launch-readiness report.

- Landing page: https://bmtriet.github.io/FreeCodex/
- AI app launch checklist: https://bmtriet.github.io/FreeCodex/ai-app-launch-safety-checklist.html
- Request a fit check: https://github.com/bmtriet/FreeCodex/issues/new?template=audit-fit-check.yml
- Demo sample report: `reports/samples/vibe-agent-demo-audit.md`
- Actual FreeCodex sample audit: `reports/samples/freecodex-audit.md`

Agent Safety Lab by StevenB is an independent project. FreeCodex remains the public workshop and proof repo behind the lab. StevenB is the public operator name; GitHub proof-of-work continues through `bmtriet`.

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

Revenue work starts in `docs/revenue-strategy.md` and `docs/opportunities/`.
Acquisition work starts in `docs/acquisition-plan.md`.
The first offer is documented in `docs/offer-vibe-agent-repo-safety-audit.md`.
The public sales pack starts at `docs/sales/vibe-launch-safety-sprint.md`.
The Ko-fi service listing copy is in `docs/sales/kofi-service-listing.md`.
Public-safe funnel metrics are in `docs/funnel-metrics.md`.
Public fit-check booking starts with `.github/ISSUE_TEMPLATE/audit-fit-check.yml`.
The public service landing page publishes at `https://bmtriet.github.io/FreeCodex/`.
The strongest public proof starts with `reports/samples/vibe-agent-demo-audit.md`.
The evolution loop is documented in `docs/evolution-loop.md`.
Quota fallback is documented in `docs/llm-gateway-fallback.md`.
Use `python3 scripts/llm_coworker.py` as the LLMGate coding co-worker command.
Use `python3 scripts/scout_big_repos.py` for targeted large-repo lead scouting.
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
