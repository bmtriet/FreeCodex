#!/usr/bin/env python3
"""Scout large public GitHub repos and score lead candidates with LLMGate.

This script is read-only with respect to public platforms. It searches open
issues in a curated set of large repos, enriches candidates with repo scale
metadata, filters previously contacted repos/threads, and asks LLMGate to rank
the shortlist. It never posts outreach.
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
import scout_leads


DEFAULT_REPOS = [
    "n8n-io/n8n",
    "langgenius/dify",
    "open-webui/open-webui",
    "FlowiseAI/Flowise",
    "browser-use/browser-use",
    "continuedev/continue",
    "langchain-ai/langchain",
    "langchain-ai/langchainjs",
    "run-llama/llama_index",
    "vercel/ai",
    "supabase/supabase",
    "appwrite/appwrite",
    "payloadcms/payload",
    "calcom/cal.com",
    "twentyhq/twenty",
    "medusajs/medusa",
    "mindsdb/mindsdb",
    "lobehub/lobe-chat",
    "Mintplex-Labs/anything-llm",
    "Significant-Gravitas/AutoGPT",
    "microsoft/autogen",
    "microsoft/semantic-kernel",
    "huggingface/transformers",
    "modelcontextprotocol/servers",
    "cline/cline",
]

DEFAULT_TERMS = [
    "security",
    "security hardening",
    "Content-Security-Policy",
    "CSP",
    "security headers",
    "dependency audit",
    "secret scanning",
    "workflow permissions",
    "CORS",
    "webhook signature",
    "MCP security",
]

REPO_FIELDS = (
    "nameWithOwner,description,stargazerCount,forkCount,watchers,url,"
    "isArchived,pushedAt,isSecurityPolicyEnabled,hasIssuesEnabled"
)

ISSUE_FIELDS = "number,title,url,updatedAt,labels,body"

KEYWORD_WEIGHTS = {
    "security": 3,
    "csp": 2,
    "content-security-policy": 3,
    "cors": 2,
    "secret": 3,
    "dependency": 2,
    "audit": 2,
    "permission": 2,
    "webhook": 2,
    "vulnerability": 3,
    "mcp": 3,
    "agent": 2,
}


class CommandError(RuntimeError):
    pass


@dataclass(frozen=True)
class BigCandidate:
    repo: str
    repo_url: str
    stars: int
    forks: int
    pushed_at: str
    security_policy_enabled: bool
    description: str
    issue_title: str
    issue_url: str
    updated_at: str
    labels: list[str]
    query: str
    body: str

    def compact(self) -> dict[str, Any]:
        return {
            "repo": self.repo,
            "repo_url": self.repo_url,
            "stars": self.stars,
            "forks": self.forks,
            "pushed_at": self.pushed_at,
            "security_policy_enabled": self.security_policy_enabled,
            "description": self.description,
            "issue_title": self.issue_title,
            "issue_url": self.issue_url,
            "updated_at": self.updated_at,
            "labels": self.labels,
            "query": self.query,
            "body_excerpt": "",
        }


def run_json(command: list[str], timeout: int) -> Any:
    try:
        completed = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except FileNotFoundError as error:
        raise SystemExit(f"Missing required command: {command[0]}") from error
    except subprocess.TimeoutExpired as error:
        raise CommandError(f"Timed out after {timeout}s: {' '.join(command)}") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip()
        raise CommandError(f"Command failed: {' '.join(command)}\n{detail}") from error
    try:
        return json.loads(completed.stdout or "[]")
    except json.JSONDecodeError as error:
        raise CommandError(f"Command returned invalid JSON: {' '.join(command)}") from error


def labels_from_issue(item: dict[str, Any]) -> list[str]:
    return [label.get("name", "") for label in item.get("labels", []) if label.get("name")]


def watchers_count(meta: dict[str, Any]) -> int:
    watchers = meta.get("watchers")
    if isinstance(watchers, dict):
        return int(watchers.get("totalCount") or 0)
    return int(watchers or 0)


def keyword_score(candidate: BigCandidate) -> int:
    haystack = " ".join(
        [candidate.issue_title, candidate.description, " ".join(candidate.labels), candidate.body]
    ).lower()
    return sum(weight for keyword, weight in KEYWORD_WEIGHTS.items() if keyword in haystack)


def sort_candidates(candidates: list[BigCandidate]) -> list[BigCandidate]:
    return sorted(
        candidates,
        key=lambda candidate: (
            keyword_score(candidate),
            candidate.stars,
            candidate.forks,
            candidate.updated_at,
        ),
        reverse=True,
    )


def as_sensitive_candidate(candidate: BigCandidate) -> scout_leads.Candidate:
    return scout_leads.Candidate(
        repo=candidate.repo,
        number=0,
        title=candidate.issue_title,
        url=candidate.issue_url,
        updated_at=candidate.updated_at,
        labels=candidate.labels,
        body=candidate.body,
        query=candidate.query,
    )


def search_big_candidates(args: argparse.Namespace) -> tuple[list[BigCandidate], list[str]]:
    sent = scout_leads.sent_urls(args.sent_dir)
    contacted_repos = (
        set()
        if args.include_contacted_repos
        else {repo.lower() for repo in scout_leads.sent_repos(args.sent_dir)}
    )
    seen: set[str] = set()
    warnings: list[str] = []
    candidates: list[BigCandidate] = []

    for repo in args.repo:
        if repo.lower() in contacted_repos:
            continue
        try:
            meta = run_json(
                ["gh", "repo", "view", repo, "--json", REPO_FIELDS],
                timeout=args.command_timeout,
            )
        except CommandError as error:
            warnings.append(str(error))
            continue
        if meta.get("isArchived") or not meta.get("hasIssuesEnabled"):
            continue
        stars = int(meta.get("stargazerCount") or 0)
        forks = int(meta.get("forkCount") or 0)
        if stars < args.min_stars and forks < args.min_forks and watchers_count(meta) < args.min_watchers:
            continue

        for term in args.term:
            query = f"{repo}:{term}"
            try:
                issues = run_json(
                    [
                        "gh",
                        "issue",
                        "list",
                        "--repo",
                        repo,
                        "--state",
                        "open",
                        "--search",
                        term,
                        "--limit",
                        str(args.per_term),
                        "--json",
                        ISSUE_FIELDS,
                    ],
                    timeout=args.command_timeout,
                )
            except CommandError as error:
                warnings.append(str(error))
                continue
            for item in issues:
                url = scout_leads.normalize_github_url(item.get("url", ""))
                if not url or url in seen or url in sent:
                    continue
                candidate = BigCandidate(
                    repo=repo,
                    repo_url=meta.get("url", f"https://github.com/{repo}"),
                    stars=stars,
                    forks=forks,
                    pushed_at=meta.get("pushedAt", ""),
                    security_policy_enabled=bool(meta.get("isSecurityPolicyEnabled")),
                    description=meta.get("description") or "",
                    issue_title=item.get("title", ""),
                    issue_url=url,
                    updated_at=item.get("updatedAt", ""),
                    labels=labels_from_issue(item),
                    query=query,
                    body=item.get("body", ""),
                )
                if not args.include_sensitive_hints and scout_leads.has_sensitive_hint(as_sensitive_candidate(candidate)):
                    continue
                seen.add(url)
                candidates.append(candidate)

    return sort_candidates(candidates)[: args.max_candidates], warnings


def build_prompt(candidates: list[BigCandidate], top_n: int) -> str:
    return (
        "You are scoring large public GitHub repo leads for FreeCodex's lightweight "
        "Vibe/Agent Repo Safety Audit revenue campaign.\n\n"
        "Policy constraints:\n"
        "- Public repos/issues only.\n"
        "- No outreach to minors, medical patients, vulnerable users, or sensitive personal-data contexts.\n"
        "- No exploit, stealth, persistence, malware, or unauthorized offensive-security work.\n"
        "- Prefer value-first proof-of-work: a small PR, mini-audit, or specific useful comment.\n"
        "- Do not recommend sending payment links in first contact.\n"
        "- Large active repos are preferred, but skip unsafe or vague issues.\n\n"
        f"Return the top {top_n} candidates as concise Markdown. For each include: "
        "rank, URL, fit score 1-10, risk level, why fit, first action, verification needed, and skip reason if not safe. "
        "End with one recommended next action for Codex.\n\n"
        "Candidates JSON:\n"
        f"{json.dumps([candidate.compact() for candidate in candidates], ensure_ascii=False, indent=2)}"
    )


def score_with_llmgate(args: argparse.Namespace, candidates: list[BigCandidate]) -> str:
    if not candidates:
        return "No large-repo candidates found."
    config = llm_gateway.load_config(args.env)
    base_url, api_key = llm_gateway.require_config(config)
    model = args.model or config.get("LLMGATE_SCOUT_MODEL", "gpt-5.5")
    data = llm_gateway.request_json(
        base_url=base_url,
        api_key=api_key,
        path="/chat/completions",
        method="POST",
        payload={
            "model": model,
            "messages": [{"role": "user", "content": build_prompt(candidates, args.top)}],
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


def render_json(candidates: list[BigCandidate], warnings: list[str]) -> str:
    return json.dumps(
        {
            "warnings": warnings,
            "candidates": [candidate.compact() for candidate in candidates],
        },
        ensure_ascii=False,
        indent=2,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scout large public GitHub repos and score leads with LLMGate")
    parser.add_argument("--repo", action="append", default=None, help="repo to search; repeatable")
    parser.add_argument("--term", action="append", default=None, help="issue search term; repeatable")
    parser.add_argument("--per-term", type=int, default=5, help="issue results per term per repo")
    parser.add_argument("--min-stars", type=int, default=10_000)
    parser.add_argument("--min-forks", type=int, default=1_000)
    parser.add_argument("--min-watchers", type=int, default=100)
    parser.add_argument("--max-candidates", type=int, default=30)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--include-sensitive-hints", action="store_true")
    parser.add_argument("--include-contacted-repos", action="store_true")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--model", help="LLMGate model id")
    parser.add_argument("--max-tokens", type=int, default=1800)
    parser.add_argument("--timeout", type=int, default=90, help="LLMGate request timeout")
    parser.add_argument("--command-timeout", type=int, default=12, help="per-gh-command timeout")
    parser.add_argument("--env", type=Path, default=None, help="LLMGate env path; defaults to local/llmgate.env")
    parser.add_argument("--sent-dir", type=Path, default=Path("leads/sent"))
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.repo = args.repo or DEFAULT_REPOS
    args.term = args.term or DEFAULT_TERMS
    candidates, warnings = search_big_candidates(args)
    text = render_json(candidates, warnings) if args.no_llm else score_with_llmgate(args, candidates)
    scout_leads.write_or_print(text, args.output)
    if warnings and args.no_llm and args.output is None:
        print(f"Warnings: {len(warnings)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
