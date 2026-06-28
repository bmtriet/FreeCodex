# Agent Safety Lab by StevenB

Agent Safety Lab by StevenB is a public, MIT-licensed maintainer toolkit for AI-built apps, agent workflows, and MCP servers.

It collects launch-safety checklists, reusable audit templates, local validation scripts, sample reports, and Codex-oriented operating patterns for public GitHub repositories built with tools such as Codex, Cursor, Claude Code, Lovable, Bolt, Replit, MCP servers, and agent skills.

The goal is practical: help maintainers catch obvious launch blockers before they become trust, revenue, or incident-response problems, then turn repeated fixes into public-safe templates and skills that other builders can reuse.

- Landing page: https://bmtriet.github.io/FreeCodex/
- AI app launch checklist: https://bmtriet.github.io/FreeCodex/ai-app-launch-safety-checklist.html
- Sponsored Public Safety Pass: https://bmtriet.github.io/FreeCodex/sponsor-public-safety-pass.html
- Front desk: https://github.com/bmtriet/FreeCodex/issues/1
- Start here: request a free public-repo fit check: https://github.com/bmtriet/FreeCodex/issues/new?template=audit-fit-check.yml
- Optional Ko-fi support after public work helped or after fit/scope is confirmed: https://ko-fi.com/freecodex
- Demo sample report: `reports/samples/vibe-agent-demo-audit.md`
- Actual FreeCodex sample audit: `reports/samples/freecodex-audit.md`

## Why This Project Is Open Source

FreeCodex is maintained in public so the work can be inspected, reused, and improved by other builders. It is intentionally small, but it is already structured as a reusable maintainer workspace:

- public launch/readiness checklist for AI-built apps
- issue template for free public-repo fit checks
- sanitized sample audit reports
- reusable templates for audit reports, delivery checklists, outreach, evals, and skill specs
- local scripts for repository validation, safety scans, mission control snapshots, and lead/repo scouting
- public-safe memory, eval, and skill-candidate records for repeated maintainer workflows

Recent owner-visible GitHub traffic snapshot, captured on 2026-06-28: 570 clones from 111 unique cloners over the previous 14 days. The project is early, but the clone traffic suggests practical reuse beyond stars.

## Maintainer Workload

This repo is maintained by `bmtriet` / StevenB. The recurring maintainer work includes:

- triaging public fit-check issues for AI-built repos, agent workflows, and MCP servers
- reviewing public repositories for launch blockers, obvious secret exposure, security header gaps, dependency risk, unclear setup docs, and release-readiness issues
- keeping the checklist, templates, sample reports, and GitHub Pages site aligned
- turning repeated review patterns into reusable skill candidates under `skills/pipeline/`
- validating generated reports and local automation before publishing public proof-of-work
- keeping all examples public-safe, sanitized, and free of private user data

## Codex And API Credit Roadmap

OpenAI Codex and API credits would directly reduce the maintainer burden for this repository. The highest-value workflows are:

- issue and fit-check triage for public GitHub repos
- first-pass launch-safety review of AI-built apps, MCP servers, and agent workflows
- PR/readiness review before publishing public audit notes
- generation of structured, reusable audit reports from bounded public context
- maintenance of local validators, safety checklists, and skill candidates
- release-note and documentation review for checklist/site updates

All outputs still require maintainer review before public posting. The intended use is maintainer acceleration, not unattended security guarantees.

## Public Fit Checks And Support

If you want StevenB to look at a public repo, start with a free fit-check issue. Fit checks confirm whether the repo is in scope before any paid audit, sponsored public safety pass, or optional support.

Star this repo if the checklist helped. If public proof-of-work helped and you do not need a scoped audit, optional Ko-fi support is welcome.

Donations are optional support for public PRs, triage notes, checklists, and mini-audits. They do not create an audit slot, support obligation, or guaranteed deliverable. Paid audits still require fit and scope confirmation first.

Sponsored Public Safety Passes are pay-what-you-want public mini-passes for a public repo you choose. They are queue-limited, accepted only after fit confirmation, and may result in a public issue, comment, checklist note, or report. They are not private audits or security guarantees.

Want to sponsor a pass for a public repo? Open the fit-check form first and choose "Sponsored Public Safety Pass."

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
- `docs/subagents/` - public-safe worker roles, prompts, and revenue loop delegation.
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
The sub-agent revenue loop is documented in `docs/subagents/revenue-worker-loop.md`.
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
