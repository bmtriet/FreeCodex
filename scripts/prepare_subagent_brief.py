#!/usr/bin/env python3
"""Prepare public-safe sub-agent briefs for revenue/evolution workers."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ROLE_GUIDANCE = {
    "revenue-scout": (
        "Find high-fit public leads or public-channel opportunities. "
        "Do not post anything. Return ranked candidates and a filled run report."
    ),
    "conversion-reviewer": (
        "Review owned surfaces for conversion clarity. Return exact file references, "
        "proposed copy, and a filled run report."
    ),
    "proof-worker": (
        "Inspect one public repo or issue. Recommend one bounded PR, comment, "
        "mini-audit note, or no-action result with public-safe evidence."
    ),
    "outreach-draft": (
        "Draft one public-safe first-contact or reply message from approved evidence. "
        "Do not include payment links in first contact."
    ),
    "audit-worker": (
        "Prepare public-safe audit reasoning for an accepted fit-check or sponsored pass. "
        "Redact evidence and avoid private data."
    ),
    "evolution-distiller": (
        "Turn repeated public-safe work into a skill candidate, checklist, eval note, "
        "or operating-memory update."
    ),
}

CONTEXT_PATHS = [
    "docs/autonomous-outreach-policy.md",
    "docs/subagents/revenue-worker-loop.md",
    "ops/queue.md",
    "ops/scoreboard.md",
    "ops/outcomes.md",
    "templates/subagent-run-report.md",
]


@dataclass(frozen=True)
class ContextFile:
    path: str
    content: str


def read_context_file(relative_path: str, max_chars: int) -> ContextFile:
    path = ROOT / relative_path
    if not path.exists():
        return ContextFile(relative_path, f"[missing: {relative_path}]")
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        text = text[: max_chars - 80].rstrip() + "\n\n[truncated for brief size]\n"
    return ContextFile(relative_path, text)


def render_brief(role: str, objective: str, target: str, max_chars_per_file: int) -> str:
    guidance = ROLE_GUIDANCE[role]
    context_files = [read_context_file(path, max_chars_per_file) for path in CONTEXT_PATHS]
    target_line = target or "None supplied. Choose from current public-safe queue only."

    sections = [
        "# Sub-Agent Brief",
        "",
        "## Role",
        "",
        f"- Name: {role}",
        f"- Guidance: {guidance}",
        "- Mode: read-only unless Main Codex explicitly assigns a disjoint edit scope.",
        "- Safety: public-safe context only; do not use secrets, credentials, private data, raw private chats, or private repo material.",
        "",
        "## Objective",
        "",
        objective,
        "",
        "## Target",
        "",
        target_line,
        "",
        "## Required Output",
        "",
        "- Fill `templates/subagent-run-report.md`.",
        "- Include public evidence only.",
        "- Recommend exactly one next action: `skip`, `watch`, `comment`, `PR`, `owned-surface update`, `audit reasoning`, or `skill/checklist`.",
        "- Do not post publicly, send messages, or include payment links in first-contact drafts.",
        "- Stop if the useful action would require private access, credentials, exploit work, or a generic low-value reply.",
        "",
        "## Context Files",
    ]

    for item in context_files:
        sections.extend(
            [
                "",
                f"### {item.path}",
                "",
                "```md",
                item.content.rstrip(),
                "```",
            ]
        )

    return "\n".join(sections).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a public-safe sub-agent brief.")
    parser.add_argument("--role", choices=sorted(ROLE_GUIDANCE), required=True)
    parser.add_argument(
        "--objective",
        default="Move Agent Safety Lab closer to verified revenue while improving public-safe operating capability.",
    )
    parser.add_argument("--target", default="")
    parser.add_argument("--max-chars-per-file", type=int, default=5000)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    brief = render_brief(args.role, args.objective, args.target, args.max_chars_per_file)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(brief, encoding="utf-8")
    else:
        print(brief, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
