# Mission Control

Mission Control is the public-safe operating surface for FreeCodex.

It turns work history into a simple loop:

1. Queue the next useful action.
2. Execute in public-safe, bounded steps.
3. Log outbound work and proof-of-work.
4. Score outcomes.
5. Convert repeated wins into reusable skills.

## Files

- `queue.md` - active work queue and next actions.
- `scoreboard.md` - generated metrics from public-safe logs.
- `mission-report.md` - generated snapshot of recent work and optional local lead scouting.

## Update Command

```bash
python3 scripts/mission_control.py generate
```

Preview without writing:

```bash
python3 scripts/mission_control.py generate --dry-run
```

## LLMGate Coding Co-worker

Use LLMGate for coding proposals when the task is public-safe and the context can be explicitly selected:

```bash
python3 scripts/llm_coworker.py --task "Explain and patch a narrow issue" --context scripts/mission_control.py --mode diff --check-apply
```

Review the saved proposal under `local/llm-coworker/` before applying anything.

Mission Control must never include secrets, private user data, raw chat logs, or private project material.
