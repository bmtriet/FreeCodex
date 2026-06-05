# Public-Safe Funnel Metrics

Measure the acquisition loop without storing private contact data, raw private conversations, secrets, or sensitive findings.

## Per-Outbound Fields

Add these fields to each sent outreach log when possible:

- Public URL.
- Channel.
- Fit category: strong, maybe, or no fit.
- Policy checklist passed: yes or no.
- Reply received: yes or no.
- Fit-check opened: yes or no.
- Audit requested: yes or no.
- Paid conversion: yes or no.
- Notes: public-safe summary only.

## Definitions

- **Public message:** A GitHub issue/PR/comment or public community reply sent under the autonomous outreach policy.
- **Reply received:** A public response from the maintainer, builder, or thread participant after the message.
- **Fit-check opened:** A GitHub fit-check issue or equivalent public request for review.
- **Qualified lead:** A public repo that matches at least two lead filters in `docs/campaign-playbook.md`.
- **Audit requested:** The builder explicitly asks for a review or accepts an offered validation slot.
- **Paid conversion:** The buyer agrees to the USD 49 report or a scoped paid fix path after scope confirmation.

## Weekly Summary

Track aggregate results:

- Public messages sent.
- Channels used.
- Replies received.
- Fit-check issues opened.
- Free audits accepted.
- Paid reports accepted.
- Reports delivered within 24-48 hours.
- Small fix scopes requested.
- Best channel.
- Most common objection.
- Copy confusion noticed.
- Next change to test.

## Safety Review

Each weekly review must confirm:

- No payment links in first-contact outreach.
- No repeated follow-ups without a reply.
- No private credentials requested or received.
- No private contact information stored.
- No raw private messages or sensitive findings stored.

Review this metrics file monthly or when the offer, channel mix, or booking path changes.

## Objection Categories

Use simple categories instead of private notes:

- price
- timing
- not ready
- private repo
- wants pentest or compliance
- outside scope
- no response
