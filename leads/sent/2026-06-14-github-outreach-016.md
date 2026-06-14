# GitHub Outreach 016

- Date: 2026-06-14
- Channel: GitHub issue comment
- Public URL: https://github.com/FlowiseAI/Flowise/issues/6433#issuecomment-4701961784
- Thread: https://github.com/FlowiseAI/Flowise/issues/6433
- Repository: FlowiseAI/Flowise
- Lead fit: Large public visual agent platform with an open MCP trust-verification issue.
- Why fit: The issue asks for a pre-execution trust hook before MCP tool dispatch. A public-code pass found concrete surfaces in `authorizeCustomMcpServer()` and `MCPTool()` where discovery-time and execution-time checks could be tested.
- Exact message sent:

```text
I did a quick public-code pass on the MCP path, and this looks like it could be made testable without needing a large design upfront.

Two concrete surfaces I would consider:

- `packages/server/src/services/custom-mcp-servers/index.ts`: `authorizeCustomMcpServer()` already builds `serverParams`, creates `MCPToolkit`, initializes, stores discovered tools, and has focused tests in `index.test.ts`. This looks like a good place to test registration/discovery trust decisions.
- `packages/components/nodes/tools/MCP/core.ts`: `MCPTool()` is the actual dispatch point that creates a fresh client and calls `client.request({ method: 'tools/call', ... })`. If the goal is pre-execution trust verification, this is the place where a deny/warn/allow decision should happen before `tools/call`, not only during initial authorization.

A small acceptance checklist that would make the hook safer:

1. No verifier configured means no behavior change.
2. A deny decision prevents `tools/call` and still closes the client.
3. The verifier receives redacted/contextual fields only: transport type, server URL/origin or server id, tool name, and arguments summary/shape rather than raw secrets.
4. Cached tool discovery does not bypass per-call verification; the cache can avoid re-listing tools, but each execution should still pass through the hook.
5. Tests cover both discovery-time behavior around `authorizeCustomMcpServer()` and execution-time denial in `MCPTool()`.

No private access or credentials needed for this. Happy to help with a small test-first PR if maintainers want that direction. No worries if not useful.
```

- Follow-up status: No follow-up unless a maintainer replies or explicitly invites a PR.
- Payment link included: No.
