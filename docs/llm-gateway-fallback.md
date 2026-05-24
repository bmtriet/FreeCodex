# LLM Gateway Fallback

FreeCodex can use a local OpenAI-compatible gateway when Codex quota is low.

The current private gateway config lives in `local/llmgate.env`. That directory is intentionally ignored by Git and must never be committed.

## Local Config

Use this shape for local-only configuration:

```bash
LLMGATE_BASE_URL=https://llmgate.app/v1
LLMGATE_QUICK_MODEL=gpt-5.4-mini
LLMGATE_DEFAULT_MODEL=gpt-5.4
LLMGATE_SCOUT_MODEL=gpt-5.4
LLMGATE_CODE_MODEL=gpt-5.4
LLMGATE_STRONG_MODEL=gpt-5.5
LLMGATE_MODELS=gpt-5.5,gpt-5.4,gpt-5.4-mini
LLMGATE_API_KEY=replace-with-local-secret
```

## Model Policy

- Use `gpt-5.4-mini` only for quick checks, formatting, and low-stakes summaries.
- Use `gpt-5.4` for default research, lead scoring, drafting, and report synthesis.
- Use `gpt-5.5` for high-value strategy, final review, and difficult technical reasoning.
- Do not use Gemini for FreeCodex automation; it has been unreliable in this gateway.

## Usage

List models:

```bash
python3 scripts/llm_gateway.py models
```

Ask the default model:

```bash
python3 scripts/llm_gateway.py chat --prompt "Summarize this repo audit strategy in 5 bullets."
```

Use the quick model for low-stakes checks:

```bash
python3 scripts/llm_gateway.py chat --model gpt-5.4-mini --prompt "Condense this into 3 bullets."
```

Use a stronger model for high-value reasoning:

```bash
python3 scripts/llm_gateway.py chat --model gpt-5.5 --prompt "Draft a concise audit report executive summary."
```

Scout public GitHub leads and let LLMGate score the shortlist:

```bash
python3 scripts/scout_leads.py --per-query 8 --max-candidates 25 --output local/lead-work/next-leads.md
```

Preview raw public candidates without using LLMGate:

```bash
python3 scripts/scout_leads.py --no-llm --per-query 3
```

## Coding Co-worker Workflow

LLMGate can participate in implementation by proposing diffs or review notes from explicitly selected public-safe context files.

Decision order for coding tasks:

1. Use LLMGate first when the work can be expressed as a public-safe proposal, review, or narrow patch request with explicitly selected context files.
2. Use Codex directly when the work needs private/local context, complex interactive debugging, credentials, browser/account access, or immediate hands-on verification.
3. Codex is always responsible for final judgment, applying patches, running checks, committing, and pushing.

For this workflow, "public-safe context" means:

- The file is tracked or intentionally public documentation/code.
- The file does not contain credentials, secrets, private user data, raw chat logs, or customer/project-confidential material.
- The file is not under ignored local/private paths such as `local/`, `private/`, `.env*`, `.git/`, `node_modules/`, or generated build/cache directories.
- The task prompt does not include non-public background, private bug reports, private account details, or raw conversation excerpts.

`docs/llm-gateway-fallback.md` is the implementation guide for LLMGate behavior. `memory/operating-notes.md` records the stable public-safe operating decisions; if they diverge, update both before relying on the workflow.

Generate a patch proposal and check whether it applies:

```bash
python3 scripts/llm_coworker.py \
  --task "Add a unit test for URL normalization" \
  --context scripts/scout_leads.py \
  --context tests/test_repo_audit.py \
  --mode diff \
  --check-apply
```

Generate review notes only:

```bash
python3 scripts/llm_coworker.py \
  --task "Review the mission control generator for public-safety gaps" \
  --context scripts/mission_control.py \
  --context docs/autonomous-outreach-policy.md \
  --mode review
```

The co-worker saves proposals under ignored `local/llm-coworker/`. Codex must review, apply, test, commit, and push. LLMGate must not auto-commit, auto-push, receive secrets, or receive private/raw chat context.

Review mode must stay inside the selected context. It should call out insufficient context rather than infer hidden repository state.

## Policy

- Do not commit gateway credentials.
- Do not paste private user data, raw conversations, or secrets into gateway prompts.
- Prefer local deterministic scripts for scanning and validation.
- Use the gateway for drafting, summarization, and low-risk analysis when quota is tight.
- Use `scripts/scout_leads.py` for lead scoring only; it must not send outreach.
- Use `scripts/llm_coworker.py` for coding proposals only with explicit public-safe context files.
- Keep outbound outreach inside `docs/autonomous-outreach-policy.md`.
