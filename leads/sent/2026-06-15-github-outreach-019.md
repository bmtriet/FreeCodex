# GitHub Outreach 019

- Date: 2026-06-15
- Channel: GitHub issue comment
- Public URL: https://github.com/activepieces/activepieces/issues/12389#issuecomment-4709595745
- Thread: https://github.com/activepieces/activepieces/issues/12389
- Repository: activepieces/activepieces
- Lead fit: Large AI automation and MCP project discussing trust verification for external MCP tool delegation.
- Offer stage: Proof-of-work only. No payment link, Ko-fi link, audit pitch, or follow-up request.
- Follow-up status: Do not follow up unless a maintainer replies or explicitly invites help.

## Exact Message Sent

```md
This seems useful if it stays provider-neutral and close to the existing MCP validation path.

A trust-verification interface could probably start as a small policy matrix around the MCP validation and tool metadata path, rather than as a hard dependency on one trust network:

| Check | Why it matters | Possible outcome |
|---|---|---|
| Tool source | Is this a known/internal MCP server, user-added URL, marketplace/community tool, or one-off endpoint? | allow, warn, require approval |
| Auth context | Does the call use project/user credentials, anonymous access, or delegated credentials? | stricter review for privileged contexts |
| Tool capability | Use existing MCP annotations like read-only/destructive/idempotent/open-world when available. | read-only can pass with lower trust; destructive/open-world needs confirmation |
| First-seen status | Has this server/tool been used successfully in this project/workspace before? | first use gets human review |
| Revocation | Can trust be invalidated after a bad result or admin decision? | block future calls and surface reason |
| Audit trail | Record server URL hash, tool name, trust decision, policy version, and user/workflow id. | debuggable without storing sensitive payloads |

Acceptance tests I would want before relying on it:
1. Unknown MCP server with read-only tools: warning/approval path, not silent allow.
2. Unknown MCP server with destructive/open-world tool: blocked or requires explicit approval.
3. Previously allowed server later revoked: future calls blocked with a clear reason.
4. Trust provider unavailable: configurable fail-open/fail-closed behavior.
5. Audit event never stores raw credentials or sensitive tool arguments.

That keeps the feature useful even if MoltBridge or any other provider is swapped out later. This is only a lightweight design/readiness note, not a certified security review, and no credentials or account access are needed. No worries if not useful.
```
