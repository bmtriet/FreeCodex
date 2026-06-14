# GitHub Outreach 017

- Date: 2026-06-14
- Channel: GitHub issue comment
- Public URL: https://github.com/n8n-io/n8n/issues/30596#issuecomment-4701975958
- Thread: https://github.com/n8n-io/n8n/issues/30596
- Repository: n8n-io/n8n
- Lead fit: Very large public automation and AI workflow repo with an open security dependency issue in the LangChain package.
- Why fit: The issue reports `sanitize-html@2.12.1` in `@n8n/n8n-nodes-langchain`; current public `master` still pins that version, and the existing ChatTrigger security tests provide a clear place for a narrow raw-text regression case.
- Exact message sent:

```text
I checked current `master` from the public repo, and this still looks actionable from the dependency/test surface.

Current public state I found:

- `packages/@n8n/nodes-langchain/package.json` still pins `sanitize-html` to `2.12.1`.
- `pnpm-lock.yaml` still has `sanitize-html@2.12.1` entries.
- `packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/templates.ts` imports `sanitize-html` directly in `sanitizeUserInput()`.
- `packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/__test__/templates.test.ts` already has a good `ChatTrigger Templates Security` suite, including script breakout and CSS `</style` parser-differential cases, but I did not see a targeted `<xmp>` / raw-text regression case there yet.

A minimal patch shape would probably be:

1. bump only `sanitize-html` in `@n8n/nodes-langchain` plus the lockfile;
2. add one regression test in the existing `templates.test.ts` security suite for raw-text element handling;
3. run the filtered nodes-langchain tests so this stays scoped to ChatTrigger rendering.

This is a lightweight public-code pass, not a certified security audit, and I did not use or need private credentials or exploit reproduction. No worries if the internal Linear ticket already has the same fix queued.
```

- Follow-up status: No follow-up unless a maintainer replies or explicitly invites a PR.
- Payment link included: No.
