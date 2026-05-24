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

Mission Control must never include secrets, private user data, raw chat logs, or private project material.
