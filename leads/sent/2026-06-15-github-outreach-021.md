# GitHub Outreach 021

- Date: 2026-06-15
- Channel: GitHub issue comment
- Public URL: https://github.com/NotYuSheng/TracePcap/issues/364#issuecomment-4709744833
- Thread: https://github.com/NotYuSheng/TracePcap/issues/364
- Repository: NotYuSheng/TracePcap
- Lead fit: Fresh explicit security-audit request for a public self-hosted LLM packet-analysis tool with concrete app and infrastructure scope.
- Offer stage: Proof-of-work only. No payment link, Ko-fi link, audit pitch, or follow-up request.
- Follow-up status: Do not follow up unless the maintainer replies or explicitly invites help.

## Exact Message Sent

```md
Thanks for opening #364 for `docs/security-audit.md`. I did a lightweight public-source readiness pass on `main` only. This is not a certified penetration test or formal security audit, and it does not require credentials or account access, but it may help prioritize the requested app/infra review.

### Prioritized findings

1. **Public signature management endpoints**
   `SignaturesController` exposes unauthenticated `GET`/`PUT` of raw YAML signature content and writes to `tracepcap.signatures.path`. Even with SnakeYAML `SafeConstructor`, this should likely require authentication/authorization and audit logging.

2. **Download header filename handling**
   `FileController.download` sets `Content-Disposition` using the stored original filename directly: `attachment; filename=" + fileName`. Consider RFC 6266-safe encoding/sanitization to avoid malformed headers or unsafe client behavior.

3. **Deployment defaults expose sensitive services**
   `docker-compose.yml` uses default Postgres/MinIO credentials, exposes Postgres `5432` and MinIO `9000/9001`, and configures the MinIO bucket as anonymous public. These are risky defaults for non-local deployments and should be clearly marked dev-only or hardened.

4. **CORS credentials with broad headers**
   `WebConfig` / `application.yml` allows origins from env, `allowed-headers: "*"`, and `allow-credentials: true`. Ensure production docs require explicit trusted origins and avoid overly broad CORS when credentials are enabled.

5. **Sorting parameter validation**
   `FileController.getAllFiles` accepts a `sort` parameter and passes the requested property into `Sort.by`. Consider allowlisting sortable fields to avoid unexpected property references or backend errors.

### Positive notes

- Upload storage uses UUID-based object names and validates extension/size.
- Merge uses `ProcessBuilder` argument lists, temp files, filename sanitization, and a timeout.
- Inspected `JdbcTemplate` queries in `NodeRoleService` use placeholders for `fileId` / `entityKey`.

### Suggested next step

Add `docs/security-audit.md` with a lightweight readiness checklist covering auth boundaries, file handling, CORS, deployment defaults, LLM data disclosure, and a note that production deployments must override all sample credentials and restrict exposed services. No worries if not useful.
```
