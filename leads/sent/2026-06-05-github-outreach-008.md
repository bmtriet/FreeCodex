# GitHub Outreach 008

- Date: 2026-06-05
- Channel: GitHub pull request
- Public URL: https://github.com/modelcontextprotocol/servers/pull/4282
- Thread: https://github.com/modelcontextprotocol/servers/pull/4282
- Related issue: https://github.com/modelcontextprotocol/servers/issues/3537
- Project: modelcontextprotocol/servers
- Why fit: Large official MCP repository with an open public issue about unconstrained string parameters across official servers. The time server had a small, bounded schema-level hardening opportunity that could be implemented with focused tests and without exploit details.
- Approval status: autonomous under `docs/autonomous-outreach-policy.md`
- Follow-up status: do not follow up unless a maintainer replies, requests changes, or explicitly invites more input.
- CI status: all upstream PR checks passed after updating the branch to commit `6c176e8`.

## Pull Request Opened

PR opened: https://github.com/modelcontextprotocol/servers/pull/4282

## Exact Pull Request Body

## Summary
- add maxLength/pattern schema hints for time server timezone inputs
- add a bounded 24-hour time pattern for convert_time
- cover the advertised input schemas and representative pattern examples in tests

## Context
This is a small defensive follow-up for #3537. It only adds schema-level constraints for clients that validate tool schemas; existing runtime validation through ZoneInfo/time parsing remains the final check.

## Tests
- cd src/time && uv run pyright
- cd src/time && uv run ruff check src/mcp_server_time/server.py test/time_server_test.py
- cd src/time && uv run pytest
