#!/usr/bin/env python3
"""Scout public GitHub leads and offload lead scoring to LLMGate.

This script is intentionally read-only with respect to public platforms: it
searches public GitHub issues, filters previously-contacted URLs from
`leads/sent/`, and prepares a ranked action queue. It never posts outreach.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import llm_gateway


DEFAULT_QUERIES = [
    '"pre-launch security review"',
    '"pre-launch security audit"',
    '"security hardening" "help wanted"',
    '"repo security audit"',
    '"exposed secret" "help wanted"',
    '"CSP audit"',
    '"dependency audit" "security"',
]

SENSITIVE_CONTEXT_HINTS = [
    "child",
    "children",
    "education",
    "medical",
    "patient",
    "health",
    "therapy",
    "minor",
    "student",
    "school",
    "fleet",
    "location",
    "tracking",
]

MAX_BODY_CHARS = 900


@dataclass(frozen=True)
class Candidate:
    repo: str
    number: int
    title: str
    url: str
    updated_at: str
    labels: list[str]
    body: str
    query: str

    def compact(self) -> dict[str, Any]:
        return {
            "repo": self.repo,
            "number": self.number,
            "title": self.title,
            "url": self.url,
            "updated_at": self.updated_at,
            "labels": self.labels,
            "query": self.query,
            "body_excerpt": trim_text(self.body, MAX_BODY_CHARS),
        }


def trim_text(value: str, max_chars: int) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def run_json(command: list[str]) -> Any:
    try:
        completed = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise SystemExit(f"Missing required command: {command[0]}") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip()
        raise SystemExit(f"Command failed: {' '.join(command)}\n{detail}") from error
    return json.loads(completed.stdout or "[]")


def normalize_github_url(url: str) -> str:
    """Normalize issue/PR/comment URLs to their public thread URL."""
    clean = url.rstrip(".,;")
    if "#" in clean:
        clean = clean.split("#", 1)[0]
    parts = clean.split("/")
    if len(parts) >= 7 and parts[2] == "github.com" and parts[5] in {"issues", "pull"}:
        return "/".join(parts[:7])
    return clean


def repo_from_github_url(url: str) -> str | None:
    clean = normalize_github_url(url)
    parts = clean.split("/")
    if len(parts) >= 5 and parts[2] == "github.com":
        return f"{parts[3]}/{parts[4]}"
    return None


def sent_urls(sent_dir: Path) -> set[str]:
    urls: set[str] = set()
    if not sent_dir.exists():
        return urls
    for path in sent_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in text.replace("(", " ").replace(")", " ").split():
            if token.startswith("https://github.com/"):
                urls.add(normalize_github_url(token))
    return urls


def sent_repos(sent_dir: Path) -> set[str]:
    return {repo for url in sent_urls(sent_dir) if (repo := repo_from_github_url(url))}


def has_sensitive_hint(candidate: Candidate) -> bool:
    haystack = f"{candidate.repo} {candidate.title} {candidate.body}".lower()
    return any(hint in haystack for hint in SENSITIVE_CONTEXT_HINTS)


def search_candidates(
    queries: list[str],
    per_query: int,
    sent: set[str],
    contacted_repos: set[str],
) -> list[Candidate]:
    seen: set[str] = set()
    candidates: list[Candidate] = []
    for query in queries:
        data = run_json(
            [
                "gh",
                "search",
                "issues",
                query,
                "--state",
                "open",
                "--limit",
                str(per_query),
                "--json",
                "repository,title,url,number,updatedAt,labels,body",
            ]
        )
        for item in data:
            url = item.get("url", "")
            normalized_url = normalize_github_url(url)
            if not normalized_url or normalized_url in seen or normalized_url in sent:
                continue
            labels = [label.get("name", "") for label in item.get("labels", []) if label.get("name")]
            repo = item.get("repository", {}).get("nameWithOwner", "")
            if repo in contacted_repos:
                continue
            candidate = Candidate(
                repo=repo,
                number=int(item.get("number") or 0),
                title=item.get("title", ""),
                url=normalized_url,
                updated_at=item.get("updatedAt", ""),
                labels=labels,
                body=item.get("body", ""),
                query=query,
            )
            seen.add(normalized_url)
            candidates.append(candidate)
    return candidates


def build_prompt(candidates: list[Candidate], top_n: int) -> str:
    payload = [candidate.compact() for candidate in candidates]
    return (
        "You are scoring public GitHub leads for FreeCodex's lightweight "
        "Vibe/Agent Repo Safety Audit revenue campaign.\n\n"
        "Policy constraints:\n"
        "- Public repos/issues only.\n"
        "- No outreach to minors, medical patients, vulnerable users, or sensitive personal-data contexts.\n"
        "- No exploit, stealth, persistence, malware, or unauthorized offensive-security work.\n"
        "- Prefer explicit requests for security review, launch readiness, repo hygiene, CI, CSP, dependency audit, secret scan, or bounded PR fixes.\n"
        "- First action should create value: a small PR, mini-audit, or specific useful comment.\n"
        "- Do not recommend sending payment links in first contact.\n"
        "- All outbound still needs Codex review before posting.\n\n"
        f"Return the top {top_n} candidates as concise Markdown. For each include: "
        "rank, URL, fit score 1-10, risk level, why fit, first action, verification needed, and skip reason if not safe.\n\n"
        "Use the exact `url` value from the JSON. Do not rewrite issue URLs.\n\n"
        "Candidates JSON:\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def score_with_llmgate(args: argparse.Namespace, candidates: list[Candidate]) -> str:
    config = llm_gateway.load_config(args.env)
    base_url, api_key = llm_gateway.require_config(config)
    model = args.model or config.get("LLMGATE_SCOUT_MODEL", "gpt-5.5")
    prompt = build_prompt(candidates[: args.max_candidates], args.top)
    data = llm_gateway.request_json(
        base_url=base_url,
        api_key=api_key,
        path="/chat/completions",
        method="POST",
        payload={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": args.max_tokens,
        },
        timeout=args.timeout,
    )
    choices = data.get("choices") or []
    if not choices:
        return json.dumps(data, indent=2, sort_keys=True)
    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, list):
        content = "\n".join(
            part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text"
        )
    return str(content).strip()


def render_no_llm(candidates: list[Candidate]) -> str:
    return json.dumps([candidate.compact() for candidate in candidates], ensure_ascii=False, indent=2)


def write_or_print(text: str, output: Path | None) -> None:
    if output is None:
        print(text)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"Wrote lead scout report: {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scout public GitHub leads and score them with LLMGate")
    parser.add_argument("--query", action="append", dest="queries", help="GitHub issue search query; repeatable")
    parser.add_argument("--per-query", type=int, default=8, help="results per query")
    parser.add_argument("--max-candidates", type=int, default=25, help="max candidates sent to LLMGate")
    parser.add_argument("--top", type=int, default=5, help="number of ranked leads requested")
    parser.add_argument("--include-sensitive-hints", action="store_true", help="do not prefilter sensitive-context hints")
    parser.add_argument("--include-contacted-repos", action="store_true", help="include repos already contacted in logs")
    parser.add_argument("--no-llm", action="store_true", help="only print/search candidate JSON")
    parser.add_argument("--model", help="LLMGate model id")
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--env", type=Path, default=None, help="LLMGate env path; defaults to local/llmgate.env")
    parser.add_argument("--sent-dir", type=Path, default=Path("leads/sent"))
    parser.add_argument("--output", type=Path, help="optional report path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    queries = args.queries or DEFAULT_QUERIES
    contacted_repos = set() if args.include_contacted_repos else sent_repos(args.sent_dir)
    candidates = search_candidates(queries, args.per_query, sent_urls(args.sent_dir), contacted_repos)
    if not args.include_sensitive_hints:
        candidates = [candidate for candidate in candidates if not has_sensitive_hint(candidate)]
    candidates = candidates[: args.max_candidates]
    text = render_no_llm(candidates) if args.no_llm else score_with_llmgate(args, candidates)
    write_or_print(text, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
