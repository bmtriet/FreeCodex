#!/usr/bin/env python3
"""Generate FreeCodex Mission Control public-safe operating files."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SENT_DIR = ROOT / "leads" / "sent"
LOCAL_SCOUT = ROOT / "local" / "lead-work" / "next-leads.md"
OPS_DIR = ROOT / "ops"

COMMENT_RE = re.compile(r"https://github\.com/[^/\s)]+/[^/\s)]+/issues/\d+#issuecomment-\d+")
PR_RE = re.compile(r"https://github\.com/[^/\s)]+/[^/\s)]+/pull/\d+")
COMMENT_DETAIL_RE = re.compile(
    r"https://github\.com/(?P<owner>[^/\s)]+)/(?P<repo>[^/\s)]+)/issues/(?P<number>\d+)#issuecomment-(?P<comment_id>\d+)"
)
PR_DETAIL_RE = re.compile(r"https://github\.com/(?P<owner>[^/\s)]+)/(?P<repo>[^/\s)]+)/pull/(?P<number>\d+)")
PAYMENT_RE = re.compile(r"paypal\.com/paypalme", re.IGNORECASE)


@dataclass(frozen=True)
class SentLogSummary:
    files: int
    threads: list[str]
    prs: list[str]
    issue_comments: list[str]
    payment_mentions: int


@dataclass(frozen=True)
class OutcomeLeadRef:
    source_file: str
    kind: str
    raw_url: str
    normalized_url: str
    owner: str
    repo: str
    number: int
    comment_id: int | None


@dataclass(frozen=True)
class OutcomeLiveState:
    state: str | None = None
    issue_comment_count: int | None = None
    review_comment_count: int | None = None
    merged: bool | None = None
    closed_at: str | None = None
    merged_at: str | None = None
    last_updated_at: str | None = None
    fetch_error: str | None = None


@dataclass(frozen=True)
class OutcomeRecord:
    lead: OutcomeLeadRef
    live: OutcomeLiveState | None


def normalize_thread(url: str) -> str:
    return url.split("#", 1)[0].rstrip(".,;")


def unique_sorted(values: list[str]) -> list[str]:
    return sorted(set(values), key=lambda value: value.lower())


def collect_sent_logs(sent_dir: Path = SENT_DIR) -> SentLogSummary:
    threads: list[str] = []
    prs: list[str] = []
    comments: list[str] = []
    payment_mentions = 0
    files = 0
    if not sent_dir.exists():
        return SentLogSummary(0, [], [], [], 0)

    for path in sorted(sent_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        files += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        payment_mentions += len(PAYMENT_RE.findall(text))
        comments.extend(COMMENT_RE.findall(text))
        for match in COMMENT_RE.findall(text) + PR_RE.findall(text):
            normalized = normalize_thread(match)
            threads.append(normalized)
            if "/pull/" in normalized:
                prs.append(normalized)

    return SentLogSummary(
        files=files,
        threads=unique_sorted(threads),
        prs=unique_sorted(prs),
        issue_comments=unique_sorted([normalize_thread(url) for url in comments]),
        payment_mentions=payment_mentions,
    )


def parse_issue_comment_url(url: str, source_file: str) -> OutcomeLeadRef | None:
    match = COMMENT_DETAIL_RE.match(url.rstrip(".,;"))
    if not match:
        return None
    owner = match.group("owner")
    repo = match.group("repo")
    number = int(match.group("number"))
    return OutcomeLeadRef(
        source_file=source_file,
        kind="issue_comment",
        raw_url=url.rstrip(".,;"),
        normalized_url=f"https://github.com/{owner}/{repo}/issues/{number}",
        owner=owner,
        repo=repo,
        number=number,
        comment_id=int(match.group("comment_id")),
    )


def parse_pr_url(url: str, source_file: str) -> OutcomeLeadRef | None:
    match = PR_DETAIL_RE.match(url.rstrip(".,;"))
    if not match:
        return None
    owner = match.group("owner")
    repo = match.group("repo")
    number = int(match.group("number"))
    return OutcomeLeadRef(
        source_file=source_file,
        kind="pull_request",
        raw_url=url.rstrip(".,;"),
        normalized_url=f"https://github.com/{owner}/{repo}/pull/{number}",
        owner=owner,
        repo=repo,
        number=number,
        comment_id=None,
    )


def extract_outcome_refs(sent_dir: Path = SENT_DIR) -> list[OutcomeLeadRef]:
    refs: list[OutcomeLeadRef] = []
    if not sent_dir.exists():
        return refs
    for path in sorted(sent_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        source_file = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in COMMENT_RE.findall(text):
            ref = parse_issue_comment_url(match, source_file)
            if ref:
                refs.append(ref)
        for match in PR_RE.findall(text):
            ref = parse_pr_url(match, source_file)
            if ref:
                refs.append(ref)
    return unique_outcome_refs(refs)


def unique_outcome_refs(refs: list[OutcomeLeadRef]) -> list[OutcomeLeadRef]:
    seen: set[tuple[str, str]] = set()
    unique: list[OutcomeLeadRef] = []
    for ref in refs:
        key = (ref.kind, ref.raw_url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(ref)
    return unique


def gh_available() -> bool:
    return shutil.which("gh") is not None


def run_gh_json(args: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        ["gh", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(detail or "gh command failed")
    return json.loads(completed.stdout or "{}")


def sanitize_lookup_error(error: object) -> str:
    text = str(error).lower()
    if "not found" in text or "could not resolve" in text:
        return "not_found_or_inaccessible"
    if "auth" in text or "login" in text or "permission" in text:
        return "auth_required_or_forbidden"
    if "rate limit" in text:
        return "rate_limited"
    return "lookup_failed"


def fetch_issue_live_state(ref: OutcomeLeadRef) -> OutcomeLiveState:
    try:
        data = run_gh_json(
            [
                "issue",
                "view",
                str(ref.number),
                "--repo",
                f"{ref.owner}/{ref.repo}",
                "--json",
                "state,comments,updatedAt,closedAt",
            ]
        )
        comments = data.get("comments")
        return OutcomeLiveState(
            state=str(data.get("state") or ""),
            issue_comment_count=len(comments) if isinstance(comments, list) else None,
            review_comment_count=None,
            merged=None,
            closed_at=str(data.get("closedAt") or "") or None,
            merged_at=None,
            last_updated_at=str(data.get("updatedAt") or "") or None,
        )
    except Exception as error:  # noqa: BLE001 - convert any gh/read failure into report data
        return OutcomeLiveState(fetch_error=sanitize_lookup_error(error))


def fetch_pr_live_state(ref: OutcomeLeadRef) -> OutcomeLiveState:
    try:
        data = run_gh_json(
            [
                "pr",
                "view",
                str(ref.number),
                "--repo",
                f"{ref.owner}/{ref.repo}",
                "--json",
                "state,comments,reviews,updatedAt,closedAt,mergedAt",
            ]
        )
        comments = data.get("comments")
        reviews = data.get("reviews")
        merged_at = str(data.get("mergedAt") or "") or None
        state = "MERGED" if merged_at else str(data.get("state") or "")
        return OutcomeLiveState(
            state=state,
            issue_comment_count=len(comments) if isinstance(comments, list) else None,
            review_comment_count=len(reviews) if isinstance(reviews, list) else None,
            merged=bool(merged_at),
            closed_at=str(data.get("closedAt") or "") or None,
            merged_at=merged_at,
            last_updated_at=str(data.get("updatedAt") or "") or None,
        )
    except Exception as error:  # noqa: BLE001 - convert any gh/read failure into report data
        return OutcomeLiveState(fetch_error=sanitize_lookup_error(error))


def fetch_live_state(ref: OutcomeLeadRef, use_gh: bool) -> OutcomeLiveState | None:
    if not use_gh or not gh_available():
        return None
    if ref.kind == "pull_request":
        return fetch_pr_live_state(ref)
    return fetch_issue_live_state(ref)


def build_outcome_records(refs: list[OutcomeLeadRef], use_gh: bool) -> list[OutcomeRecord]:
    return [OutcomeRecord(lead=ref, live=fetch_live_state(ref, use_gh=use_gh)) for ref in refs]


def read_local_scout_excerpt(path: Path = LOCAL_SCOUT, max_lines: int = 18) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    safe_lines = []
    for line in lines:
        if PAYMENT_RE.search(line):
            continue
        safe_lines.append(line)
        if len(safe_lines) >= max_lines:
            break
    return safe_lines


def render_scoreboard(summary: SentLogSummary, generated_at: str) -> str:
    payment_first_contact = 0 if summary.payment_mentions == 0 else summary.payment_mentions
    rows = [
        ("Generated at UTC", generated_at),
        ("Sent log files", str(summary.files)),
        ("GitHub PRs opened", str(len(summary.prs))),
        ("GitHub issue comments sent", str(len(summary.issue_comments))),
        ("Payment links in sent logs", str(payment_first_contact)),
    ]
    url_rows = []
    for url in summary.threads:
        kind = "PR" if "/pull/" in url else "Issue"
        url_rows.append(f"| {kind} | {url} |")
    if not url_rows:
        url_rows.append("| None | No public outbound logged yet. |")

    return "\n".join(
        [
            "# Mission Control Scoreboard",
            "",
            "Generated by `python3 scripts/mission_control.py generate`.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            *[f"| {key} | {value} |" for key, value in rows],
            "",
            "## Public URLs",
            "",
            "| Type | URL |",
            "| --- | --- |",
            *url_rows,
            "",
            "## Current Read",
            "",
            "- The campaign is in proof-of-work mode.",
            "- Next best action is to watch for replies/merge activity, then convert one accepted fix into a reusable skill.",
            "- New outbound should use `scripts/scout_leads.py` and respect `docs/autonomous-outreach-policy.md`.",
            "",
        ]
    )


def render_queue(summary: SentLogSummary, has_local_scout: bool) -> str:
    scout_action = (
        "Inspect `local/lead-work/next-leads.md`, choose at most 3 safe actions, then log any outbound."
        if has_local_scout
        else "Run `python3 scripts/scout_leads.py --output local/lead-work/next-leads.md`, then review candidates."
    )
    return "\n".join(
        [
            "# Mission Control Queue",
            "",
            "Generated by `python3 scripts/mission_control.py generate`.",
            "",
            "## Active Queue",
            "",
            "| Priority | Status | Item | Next Action | Source |",
            "| --- | --- | --- | --- | --- |",
            "| P0 | todo | Review pending public PRs | Check maintainer replies and CI before any follow-up. | `leads/sent/` |",
            f"| P1 | todo | Review local LLMGate lead scout output | {scout_action} | `scripts/scout_leads.py` |",
            "| P1 | todo | Convert successful fixes into reusable skill notes | If a PR is merged or discussed positively, distill the pattern into `skills/pipeline/`. | `skills/pipeline/README.md` |",
            "",
            "## Rules",
            "",
            "- Do not follow up unless the maintainer replies.",
            "- Prefer proof-of-work PRs over sales copy.",
            "- Keep first contact free of payment links.",
            "- Stop when a lead touches minors, medical data, vulnerable users, private repos, stealth, persistence, or unclear authorization.",
            f"- Current logged outbound threads: {len(summary.threads)}.",
            "",
        ]
    )


def render_mission_report(summary: SentLogSummary, scout_excerpt: list[str], generated_at: str) -> str:
    scout_block = "\n".join(scout_excerpt) if scout_excerpt else "No local scout report found."
    return "\n".join(
        [
            "# Mission Control Report",
            "",
            "Generated by `python3 scripts/mission_control.py generate`.",
            "",
            f"Generated at UTC: `{generated_at}`",
            "",
            "## Recent Work",
            "",
            f"- Logged {summary.files} public-safe outreach runs.",
            f"- Opened {len(summary.prs)} public proof-of-work PRs.",
            f"- Sent {len(summary.issue_comments)} public issue comments with normalized thread tracking.",
            "- Added LLMGate lead scouting support for quota-frugal candidate scoring.",
            "",
            "## Optional Local Scout",
            "",
            "Local scout output lives at `local/lead-work/next-leads.md` and is intentionally ignored by Git.",
            "",
            "```text",
            scout_block,
            "```",
            "",
            "## Next Decision",
            "",
            "At the next revenue loop, review local scout output, pick no more than 3 public-safe targets, and prefer a bounded PR or mini-audit over generic outreach.",
            "",
        ]
    )


def render_cell(value: object | None) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("|", "\\|").replace("\n", " ")
    return text


def render_outcomes(records: list[OutcomeRecord], generated_at: str, used_gh: bool) -> str:
    failures = sum(1 for record in records if record.live and record.live.fetch_error)
    rows = [
        ("Generated at UTC", generated_at),
        ("Tracked outbound artifacts", str(len(records))),
        ("Pull requests tracked", str(sum(1 for record in records if record.lead.kind == "pull_request"))),
        ("Issue comments tracked", str(sum(1 for record in records if record.lead.kind == "issue_comment"))),
        ("Live GitHub lookup", "enabled" if used_gh and gh_available() else "disabled"),
        ("Live fetch failures", str(failures)),
    ]
    outcome_rows = []
    for record in records:
        live = record.live
        if live and live.fetch_error:
            note = live.fetch_error
        elif record.lead.kind == "issue_comment":
            note = "parent issue state only"
        else:
            note = ""
        outcome_rows.append(
            "| "
            + " | ".join(
                [
                    render_cell(record.lead.kind),
                    render_cell(record.lead.source_file),
                    render_cell(record.lead.raw_url),
                    render_cell(record.lead.normalized_url),
                    render_cell(live.state if live else None),
                    render_cell(live.merged if live else None),
                    render_cell(live.issue_comment_count if live else None),
                    render_cell(live.review_comment_count if live else None),
                    render_cell(live.last_updated_at if live else None),
                    render_cell(note),
                ]
            )
            + " |"
        )
    if not outcome_rows:
        outcome_rows.append("| - | - | - | - | - | - | - | - | - | No outbound artifacts logged yet. |")

    return "\n".join(
        [
            "# Mission Control Outcomes",
            "",
            "Generated by `python3 scripts/mission_control.py generate`.",
            "",
            "This file is generated from public sent logs only. It never posts outreach and does not read secrets or private data.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            *[f"| {key} | {value} |" for key, value in rows],
            "",
            "## Tracked Outcomes",
            "",
            "| Kind | Source | URL | Thread | State | Merged | Issue Comments | Review Comments | Last Updated | Notes |",
            "| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
            *outcome_rows,
            "",
        ]
    )


def generated_outputs(use_gh: bool = True) -> dict[Path, str]:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary = collect_sent_logs()
    scout_excerpt = read_local_scout_excerpt()
    outcome_records = build_outcome_records(extract_outcome_refs(), use_gh=use_gh)
    return {
        OPS_DIR / "queue.md": render_queue(summary, has_local_scout=bool(scout_excerpt)),
        OPS_DIR / "scoreboard.md": render_scoreboard(summary, generated_at),
        OPS_DIR / "mission-report.md": render_mission_report(summary, scout_excerpt, generated_at),
        OPS_DIR / "outcomes.md": render_outcomes(outcome_records, generated_at, used_gh=use_gh),
    }


def write_outputs(outputs: dict[Path, str], dry_run: bool) -> None:
    for path, text in outputs.items():
        if dry_run:
            print(f"--- {path.relative_to(ROOT)} ---")
            print(text)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


def command_generate(args: argparse.Namespace) -> int:
    write_outputs(generated_outputs(use_gh=not args.no_gh), dry_run=args.dry_run)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate FreeCodex Mission Control files")
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate", help="generate ops queue, scoreboard, and report")
    generate.add_argument("--dry-run", action="store_true", help="print generated files without writing")
    generate.add_argument("--no-gh", action="store_true", help="skip live read-only GitHub lookups")
    generate.set_defaults(func=command_generate)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
