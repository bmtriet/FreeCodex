# GitHub Outreach 018

- Date: 2026-06-15
- Channel: GitHub issue comment
- Public URL: https://github.com/googleapis/mcp-toolbox/issues/3373#issuecomment-4709538013
- Thread: https://github.com/googleapis/mcp-toolbox/issues/3373
- Repository: googleapis/mcp-toolbox
- Lead fit: Large public MCP database server with an active feature request about PII masking before query results enter agent context.
- Why fit: The thread asks how role-based policy should align with existing auth. Public docs and code show JWT/scopes and auth claims as a clean input boundary for a PII masking policy layer.
- Exact message sent:

```text
I did a small public-code/docs pass on the role-alignment question. This is not a certified security audit, and I did not use or need any private data.

One concrete way to keep this from becoming a second RBAC system would be to treat the existing auth claims as the policy input, then keep PII policy roles as local tiers:

- auth layer: validate token, audience, scopes, and expose claims
- policy layer: map selected claims/scopes/groups to masking tiers such as `full`, `partial`, `tokenized`, or `deny-field`
- tool-result layer: apply masking before the result is serialized into MCP tool output / agent context
- audit layer: log policy id, tier, field/type masked, count, and decision reason, but not raw PII values

The public docs already describe MCP auth with JWT validation, audience, and `scopesRequired`, and `internal/auth/auth.go` exposes claims via `GetClaimsFromHeader(...)` / `ValidateMCPAuth(...)`. That seems like a clean boundary: PII policy should consume normalized claims, not own identity.

A small acceptance-test matrix could cover the feature without sensitive sample data:

1. same query result + `scope=admin` -> unmasked allowed fields, audit event emitted
2. same result + `scope=agent` -> email/phone masked before tool output
3. unknown role/scope -> fail closed to the most restrictive tier
4. configured column rule beats regex guess when both match
5. DLP integration disabled/unavailable -> deterministic local rules still run, or request fails closed if policy requires DLP

No worries if this is already where the design is headed; I’m leaving it as a bounded public checklist because the role-mapping question looked like the key decision point.
```

- Follow-up status: No follow-up unless a maintainer replies or explicitly invites a PR.
- Payment link included: No.
