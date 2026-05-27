# Public-Safe Booking Funnel

Status: candidate

Use this workflow when turning a public FreeCodex offer into a request path that strangers can use without sharing secrets, private context, or account access.

## Trigger

Good fits:

- a public landing page needs a concrete booking CTA
- an offer doc describes pricing but lacks intake mechanics
- a service should collect repo URLs, launch context, and scope hints
- public outreach is starting to create inbound interest

Do not use this for private repo onboarding, credential collection, account login, medical/legal/financial intake, or any workflow that needs sensitive personal data.

## Inputs

- Public offer page or sales doc.
- Public repository URL for the service workspace.
- Payment destination, if already approved.
- Outreach policy or safety boundary docs.

Never ask for secrets, passwords, tokens, cookies, private keys, private customer data, or account access.

## Workflow

1. Add a GitHub issue form for public-safe fit checks.
2. Require a public repo URL and launch context.
3. Add checkboxes that force acknowledgement of no secrets, no private data, and no certified-pentest guarantee.
4. Keep payment language after fit, positive reply, scope confirmation, and consent to proceed.
5. Point landing-page CTAs directly at the issue form.
6. Document the booking path in the offer doc and README.
7. Add the issue form and any critical funnel files to the repo validator.
8. Ask LLMGate to review public-safety and policy consistency before publishing.

## Validation

```bash
python3 scripts/validate_repo.py
python3 -m unittest tests.test_repo_audit
ruby -e 'require "yaml"; YAML.load_file(".github/ISSUE_TEMPLATE/audit-fit-check.yml")'
git diff --check
```

Also verify:

- the public CTA URL uses `issues/new?template=...`
- no first-contact copy includes a payment link
- payment metadata points to the current approved destination
- the issue form cannot reasonably be read as inviting private material into a public issue

## Failure Modes

Stop and revise when:

- the form asks for credentials, access, or private context
- private repo language appears inside the public intake path
- payment appears before fit/scope/consent
- the booking CTA points to an obsolete payment destination
- warnings are only in docs and not visible in the actual intake form

## Evidence

This candidate is based on the FreeCodex GitHub Pages booking funnel and LLMGate review that caught private-material ambiguity in the first draft.
