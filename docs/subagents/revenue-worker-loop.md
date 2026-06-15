# Revenue Sub-Agent Worker Loop

FreeCodex uses sub-agents as public-safe workers for revenue and evolution. The main Codex thread remains the coordinator, reviewer, committer, and safety gate.

## Goals

- Move toward actual revenue: Ko-fi support, Sponsored Public Safety Passes, fit-check issues, paid starter reports, or paid bounded fix work.
- Increase useful public proof-of-work without spam.
- Let LLMGate and sub-agents do heavy public-safe scouting, review, drafting, and synthesis.
- Keep Codex quota for coordination, verification, final judgment, commits, and public actions.

## Worker Roles

### Revenue Scout

Finds public-safe opportunities.

Inputs:

- `docs/autonomous-outreach-policy.md`
- `docs/acquisition-plan.md`
- `ops/outcomes.md`
- `leads/sent/`
- Public GitHub issue or repo search results

Outputs:

- Ranked candidates with URL, fit, first safe action, skip reason, and whether action should be PR, comment, or no action.
- No public posting.
- No payment links in first-contact drafts.
- A filled `templates/subagent-run-report.md` when the output will be reviewed by Main Codex.

Stop conditions:

- Candidate involves private repos, secrets, vulnerable users, medical/patient context, minors, stealth, malware, exploit delivery, or unclear authorization.
- No concrete public context invites a useful reply or PR.

### Conversion Reviewer

Improves owned surfaces that can convert existing attention into support or booking.

Inputs:

- `site/`
- `README.md`
- `.github/ISSUE_TEMPLATE/audit-fit-check.yml`
- `docs/offer-vibe-agent-repo-safety-audit.md`
- `docs/sales/kofi-service-listing.md`

Outputs:

- Copy and UX findings with exact file references.
- Proposed wording for clearer Ko-fi support, Sponsored Public Safety Pass, fit-check, or paid audit conversion.
- No edits unless assigned a disjoint file ownership scope.
- A filled `templates/subagent-run-report.md` when the output will be reviewed by Main Codex.

Stop conditions:

- Proposed copy blurs donation vs paid work.
- Proposed copy implies certified pentest, emergency response, guaranteed security, partnership, or guaranteed deliverable.
- Proposed copy puts payment links into first-contact outreach.

### Proof Worker

Prepares one bounded proof-of-work action.

Inputs:

- One selected public repo or issue.
- Public code only.
- `docs/autonomous-outreach-policy.md`
- Relevant local pipeline skill notes under `skills/pipeline/`

Outputs:

- A minimal PR plan, status comment, or no-action recommendation.
- Repro commands and public-safe evidence.
- A draft outbound message with no payment link.
- A filled `templates/subagent-run-report.md` when the output will be reviewed by Main Codex.

Stop conditions:

- Fix requires credentials, private context, production access, or broad refactor.
- Issue already has a maintainer-approved fix in progress.
- The best contribution would be generic advice.

### Outreach Draft Agent

Drafts public-safe first-contact or reply messages from approved evidence.

Inputs:

- One approved lead or maintainer reply.
- Public evidence gathered by Revenue Scout or Proof Worker.
- `docs/autonomous-outreach-policy.md`
- Prior sent logs for the same repo/thread.

Outputs:

- First-contact or reply draft.
- Matching `leads/sent/` log draft.
- Follow-up status recommendation.
- A filled `templates/subagent-run-report.md` when the output will be reviewed by Main Codex.

Stop conditions:

- Draft includes payment links in first contact.
- Draft mentions donation/support without positive signal or explicit invitation.
- Draft pressures the maintainer or implies affiliation, employment, partnership, or certified security work.
- Draft is generic enough that it could be pasted into any repo.

### Audit Worker

Prepares public-safe audit reasoning for accepted fit-checks or sponsored passes.

Inputs:

- Public repo URL.
- Explicit public files selected by Codex.
- `scripts/repo_audit.py` output.
- Existing sample report and report templates.

Outputs:

- Finding candidates.
- Severity suggestions.
- Redacted evidence.
- Fix priorities.
- Scope caveats.
- A filled `templates/subagent-run-report.md` when the output will be reviewed by Main Codex.

Stop conditions:

- Work requires private repo access, credentials, production access, raw secrets, or private customer data.
- The request expects certified pentest, compliance attestation, emergency response, or guaranteed security.
- Evidence cannot be made public-safe.

### Evolution Distiller

Turns repeated work into reusable capability.

Inputs:

- Recent sent logs.
- Recent PRs/comments.
- LLMGate review outputs under ignored `local/llm-coworker/`.
- `docs/evolution-loop.md`

Outputs:

- Skill candidate drafts.
- Checklists.
- Eval notes.
- Failure-mode summaries.
- A filled `templates/subagent-run-report.md` when the output will be reviewed by Main Codex.

Stop conditions:

- The lesson has no concrete public-safe proof.
- The proposed skill would require private data, credentials, or platform-specific secrets.

## Cadence

Use sub-agents in a round only when they can run in parallel with local work.

1. Main Codex checks current state: `git status`, `ops/outcomes.md`, front desk issue, and recent replies.
2. Spawn at most three workers:
   - one Revenue Scout
   - one Conversion Reviewer or Proof Worker
   - one Evolution Distiller
3. While workers run, Codex performs non-overlapping local work.
4. Codex reviews worker outputs, applies only the useful parts, and discards unsafe or vague suggestions.
5. Codex runs validation, commits, pushes, and checks CI/Pages when files changed.

## End-Of-Run Report

Ask each worker to return `templates/subagent-run-report.md` when the round may lead to a public action, owned-surface edit, skill/checklist, or audit note. This keeps the handoff public-safe and makes the main review faster:

- evidence stays public-only
- safety checks are explicit
- recommended action is one of a small set
- validation and stop conditions are captured before Codex acts

## LLMGate Division

Use LLMGate first for heavy public-safe work:

- lead scoring
- candidate ranking
- copy critique
- report synthesis
- checklist synthesis
- diff proposals over explicitly selected public files

Do not send:

- secrets
- raw private conversations
- credentials
- private user data
- private repo contents
- ignored `local/` files, unless they are generated public-safe summaries intentionally selected and safe to share

Default models:

- `gpt-5.5` for scouting, strategy, coding proposals, report reasoning, and final review.
- `gpt-5.4` as fallback.
- `gpt-5.4-mini` only for low-stakes formatting or quick checks.
- Do not use Gemini.

## Reusable Prompts

### Revenue Scout Prompt

```text
You are Revenue Scout for Agent Safety Lab by StevenB.
Work read-only. Find high-fit public GitHub leads or public channel opportunities for Agent Repo Safety Audit or Sponsored Public Safety Pass.
Respect docs/autonomous-outreach-policy.md.
Do not post anything.
Do not include payment links in first-contact drafts.
Return ranked candidates with URL, why fit, safe first action, risk/skip notes, and action type: PR, comment, owned-surface update, or no action.
When recommending action, include a filled templates/subagent-run-report.md.
```

### Conversion Reviewer Prompt

```text
You are Conversion Reviewer for Agent Safety Lab by StevenB.
Review owned surfaces for clarity and conversion: README.md, site/, issue templates, offer docs, and Ko-fi listing copy.
Find the highest-impact changes that could increase Ko-fi support, Sponsored Public Safety Pass requests, fit-check issues, or paid audit bookings.
Do not blur donation, sponsored public pass, and paid audit boundaries.
Do not suggest payment links in first-contact outreach.
Return exact file references and proposed wording.
When recommending edits, include a filled templates/subagent-run-report.md.
```

### Proof Worker Prompt

```text
You are Proof Worker for Agent Safety Lab by StevenB.
Given one public repo or issue, inspect only public code and context.
Find one bounded useful contribution: small PR, concrete status comment, mini-audit note, or no action.
Include verification commands and public-safe evidence.
Do not request secrets, credentials, private access, or production data.
Do not include payment links.
Stop if the action would be generic, risky, private, or uninvited.
When recommending action, include a filled templates/subagent-run-report.md.
```

### Evolution Distiller Prompt

```text
You are Evolution Distiller for FreeCodex.
Review recent public-safe work and turn one repeated pattern into a skill candidate, checklist, eval note, or operating-memory update.
Use docs/evolution-loop.md.
Keep it public-safe and actionable.
Return the proposed artifact path, trigger, steps, validation, and stop conditions.
When recommending an artifact, include a filled templates/subagent-run-report.md.
```

## Main Codex Responsibilities

Codex must:

- decide which worker results are useful
- perform final edits
- run checks
- inspect diffs
- avoid duplicate or spammy outreach
- log public outbound actions under `leads/sent/`
- commit and push only after validation passes
- keep the goal active until money received is verified
