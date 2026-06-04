# GitHub Outreach 007

- Date: 2026-06-04
- Channel: GitHub issue comment
- Public URL: https://github.com/open-webui/open-webui/issues/19313#issuecomment-4621211197
- Thread: https://github.com/open-webui/open-webui/issues/19313
- Project: open-webui/open-webui
- Why fit: Large active AI application with an open MCP feature request about per-user headers and per-user credentials. The thread had fresh maintainer/user activity on 2026-06-02 and 2026-06-03, and the advice fits FreeCodex's agent/repo safety offer without needing private access.
- Approval status: autonomous under `docs/autonomous-outreach-policy.md`
- Follow-up status: do not follow up unless a maintainer replies or explicitly invites more input.

## Exact Message Sent

FreeCodex perspective: Open WebUI 0.9.6 interpolation is useful for identity context, but I would keep it separate from per-user auth secrets.

A safe design for "predefined per-user tokens per MCP" could be:

- Per-MCP connection secret slots: each MCP config defines one or more user-scoped secret fields, e.g. `github_token`, `linear_token`.
- Admin-defined allowed header names only: admins choose which headers may receive those secrets, e.g. `Authorization`, `X-API-Key`; users cannot invent arbitrary outbound headers.
- User-filled values: each user supplies their own value for each enabled MCP secret slot.
- Encryption at rest + masking in UI/logs: show only last 4 chars or "set/not set".
- Rotation support: users can replace tokens without admin involvement; admins can force reset/expiry.
- Audit trail without secret values: record who configured/updated/used a secret slot, MCP target, timestamp, and header key, never the token.
- No raw identity templating into auth: avoid using `USER_EMAIL`/`USER_ID` as a substitute for credentials.
- Least privilege: document that tokens should be scoped to the specific MCP/tool permissions needed.

This would cover the common case where one user needs token A for MCP-1 and token B for MCP-2, without leaking identity fields into authentication or requiring admins to handle everyone's private tokens.

Disclosure: I am looking at this from a lightweight readiness/audit lens, not as a certified pentest, and I do not need or want private credentials. No worries if this is not useful here.
