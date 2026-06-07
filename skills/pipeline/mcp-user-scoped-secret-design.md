# MCP User-Scoped Secret Design

Status: candidate

## Trigger

Use this pattern when a public agent/MCP project discusses per-user MCP credentials, shared MCP server configs, forwarded user identity, or secret injection into tool requests.

## Public-Safe Inputs

- Public issue, discussion, or PR context.
- Public docs or code showing MCP server configuration.
- Existing identity interpolation variables, if documented.
- Existing secret storage or masking behavior, if documented.

Do not request or inspect real user tokens, API keys, private tenant data, production logs, or private MCP server configuration.

## Recommended Model

- Admins own the MCP server definition.
- Admins declare allowed user-scoped secret fields.
- Admins declare allowed injection points, such as specific headers or explicit URL/path/query slots.
- Users provide only the values for declared user-scoped secrets.
- Identity variables remain separate from authentication secrets.
- Secrets are encrypted at rest, masked in UI/logs, and resolved only at execution time for the requesting user/session.
- Missing required secrets should trigger a first-use setup prompt instead of a generic tool failure.

## Guardrails

- User secrets must be write-only after save; APIs return metadata such as `configured: true`, not raw values.
- Secret values cannot be injected into arbitrary headers, bodies, URLs, tool arguments, logs, or debug traces.
- User A's request can resolve only user A's secret values.
- Shared chats, admins, and other users cannot view or reuse resolved secret values.
- Identity variables such as `USER_EMAIL` or `USER_ID` cannot satisfy declared auth-secret requirements.

## Validation Ideas

- Attempt to use a declared secret outside its allowed injection point and expect validation failure.
- Save a user secret, then verify UI/API readback returns only masked metadata.
- Trigger request, error, and debug paths and verify redaction.
- Test two users with different secret values and verify per-user isolation.
- Invoke an MCP server with missing required secrets and verify first-use setup flow.

## Stop Conditions

- The discussion requires real credentials, private repo access, production logs, or tenant-specific data.
- The requested behavior would make URL/header injection free-form by default.
- The context involves sensitive personal-data domains where a lightweight public comment is not enough.
- The thread turns into exploit reproduction rather than defensive design.

## Evidence

- Public discussion: https://github.com/open-webui/open-webui/issues/19313
- Public follow-up: https://github.com/open-webui/open-webui/issues/19313#issuecomment-4642847395

