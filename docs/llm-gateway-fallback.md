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

## Policy

- Do not commit gateway credentials.
- Do not paste private user data, raw conversations, or secrets into gateway prompts.
- Prefer local deterministic scripts for scanning and validation.
- Use the gateway for drafting, summarization, and low-risk analysis when quota is tight.
- Use `scripts/scout_leads.py` for lead scoring only; it must not send outreach.
- Keep outbound outreach inside `docs/autonomous-outreach-policy.md`.
