# Security Policy

This repository is public. Treat every committed file as visible to the internet.

## Never Commit

- API keys, tokens, passwords, cookies, or credentials.
- Private keys, certificates, or signing material.
- Raw user conversations, private notes, or personal memory.
- Customer, client, or confidential project data.
- Local `.env` files or machine-specific secret configuration.

## Before Publishing

Run:

```bash
python3 scripts/validate_repo.py
```

The validator is a guardrail, not a guarantee. Review changes manually before committing.

## Reporting

If a secret or private file is committed, rotate the secret immediately and remove it from Git history before continuing public work.

