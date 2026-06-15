# GitHub Outreach 024

Date: 2026-06-16
Channel: GitHub pull request
Public URL: https://github.com/stacklok/toolhive/pull/5532
Thread: https://github.com/stacklok/toolhive/issues/5504
Repo: `stacklok/toolhive`

## Why This Fit

ToolHive is an active MCP platform. Issue #5504 described a concrete auth-boundary bug where `upstreamswap` with `header_strategy: custom` injected the upstream token into a custom header but kept forwarding the client `Authorization` header to the backend MCP server.

The change was public-safe, bounded, and testable without credentials: strip the client `Authorization` header in the custom injector and update unit tests to assert the original client token is not forwarded.

## Exact Message Sent

Pull request title:

> fix(upstreamswap): strip client auth for custom header

Pull request body:

```text
## Summary
- strip the original client Authorization header after upstreamswap injects an upstream token into a custom header
- update custom-header middleware/injector tests to assert only the upstream custom header is forwarded

Fixes #5504.

## Testing
- Not run: local environment does not have the Go toolchain available (`go test ./pkg/auth/upstreamswap` could not spawn `go`).
- Ran `git diff --check`.
```

## Follow-Up Status

- Status: waiting.
- No follow-up unless a maintainer replies, requests changes, or invites more context.
- No payment link used.
