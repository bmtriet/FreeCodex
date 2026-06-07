# GitHub Outreach 010

- Date: 2026-06-07
- Channel: GitHub issue comment follow-up
- Public URL: https://github.com/open-webui/open-webui/issues/19313#issuecomment-4642847395
- Thread: https://github.com/open-webui/open-webui/issues/19313
- Project: open-webui/open-webui
- Why fit: A participant directly replied to `@bmtriet` and expanded the per-user MCP secret model from the prior public comment. The follow-up was invited, technical, and limited to guardrails/tests for user-scoped MCP secrets.
- Approval status: autonomous under `docs/autonomous-outreach-policy.md`; follow-up allowed because the recipient engaged directly.
- Follow-up status: do not follow up again unless a maintainer or participant replies, requests clarification, or explicitly invites more input.

## Funnel Status

- Reply received: yes
- Fit-check opened: no
- Qualified lead: strong
- Audit requested: no
- Paid conversion: no
- Notes: Public-safe technical follow-up only. No payment link, private contact info, secrets, or raw private messages.

## Exact Message Sent

Thanks — yes, that matches the model I had in mind.

The key distinction for me is:

- Admin owns the MCP server definition and the allowed injection locations.
- Users only provide values for declared user-scoped secrets.
- Identity interpolation stays separate from auth material.
- Secrets are write-only from the user's perspective after save, encrypted at rest, masked everywhere, and only resolved at request execution time for that user/session.

I also think URL/path injection should be supported only when explicitly declared by the admin, since some MCP-compatible services do require API keys in paths or query parameters, but it should not be a free-form template expansion surface.

A few concrete guardrails/tests that would be useful:

1. **Allowed injection points only**
   - If an admin declares `github_token` may only be injected into `Authorization`, attempts to use it in URL, body, arbitrary headers, logs, or tool arguments should fail validation.

2. **No secret readback**
   - After saving, the UI/API should never return the raw secret value, only metadata like `configured: true`, `updated_at`, or a masked placeholder.

3. **Log and error masking**
   - Secrets should be redacted from request logs, MCP error output, tool traces, debug logs, and frontend-visible exceptions, including partial matches.

4. **Per-user isolation**
   - A request by user A must only resolve user A's secret values. User B, admins, and shared chats should not be able to view or reuse those resolved values.

5. **Identity vars cannot satisfy secret requirements**
   - `USER_EMAIL`, `USER_ID`, etc. should remain usable only for identity/context interpolation, not as replacements for declared auth secrets.

The first-use popup also seems like the right UX: if a user invokes an MCP server that requires missing secrets, prompt them to configure the required fields before execution rather than failing with a generic auth error.

