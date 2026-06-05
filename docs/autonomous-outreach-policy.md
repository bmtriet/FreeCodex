# Autonomous Outreach Policy

FreeCodex Agent Safety Lab is allowed to run autonomous outreach for the Agent Repo Safety Audit, but only inside these guardrails.

## Allowed

- Contact public projects or builders when there is a visible, relevant public context.
- Use public GitHub issues, GitHub discussions, or public community replies when the project has invited feedback, audits, launch review, beta testing, or security discussion.
- Send at most 3 outbound messages per automation run.
- Offer the first 3 consenting public repo audits for free while validating the workflow.
- Mention the paid offer only as a later option, without pressure.
- Do not include payment links in first-contact outreach.
- Log every sent message under `leads/sent/`.

## Not Allowed

- No spam, mass scraping, or repeated follow-ups.
- No private repo audit without explicit permission.
- No private DM or email unless the person has publicly invited contact and the message is directly relevant.
- No claims of certified pentesting, compliance, guaranteed security, partnership, employment, or official affiliation.
- No use of secrets, private user data, raw conversations, or confidential project material.
- No sending messages that require paid tools, ad spend, or bypassing platform limits.
- No outreach to minors, medical patients, vulnerable users, or sensitive personal-data contexts.

## Message Requirements

Every autonomous message must:

- Be short and specific to the public project or thread.
- Disclose that this is a lightweight launch/readiness audit, not a certified pentest.
- Say no private credentials or account access are needed.
- Avoid fear-based pressure.
- Include a clear opt-out such as "No worries if not useful."

## Logging

For each sent message, create a public-safe log file in `leads/sent/` with:

- Date and channel.
- Public URL.
- Why the lead fit.
- Exact message sent.
- Follow-up status.

Do not log private contact information or sensitive findings.
