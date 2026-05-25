#!/usr/bin/env python3
"""Generate a lightweight public-repo safety audit report."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import re
import sys
from pathlib import Path


SEVERITY_ORDER = {
    "Critical": 0,
    "High": 1,
    "Medium": 2,
    "Low": 3,
    "Info": 4,
}

TEXT_SUFFIXES = {
    ".css",
    ".env",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".vue",
    ".yaml",
    ".yml",
}

CODE_SUFFIXES = {
    ".js",
    ".jsx",
    ".mjs",
    ".py",
    ".ts",
    ".tsx",
    ".vue",
}

SPECIAL_TEXT_NAMES = {
    ".gitignore",
    "Dockerfile",
    "LICENSE",
    "Makefile",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "local",
    "node_modules",
    "private",
    "target",
    "venv",
}

MAX_TEXT_BYTES = 1_000_000


@dataclasses.dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    severity: str
    title: str
    recommendation: str


@dataclasses.dataclass
class Finding:
    severity: str
    category: str
    title: str
    path: str
    line: int | None
    evidence: str
    recommendation: str


SECRET_RULES = [
    Rule(
        "OpenAI key",
        re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
        "Critical",
        "Possible OpenAI API key committed",
        "Revoke the key, rotate dependent services, and move the value to a secret manager or local environment variable.",
    ),
    Rule(
        "GitHub token",
        re.compile(r"github_pat_[A-Za-z0-9_]{20,}|gh[opsu]_[A-Za-z0-9_]{20,}"),
        "Critical",
        "Possible GitHub token committed",
        "Revoke the token, rotate any exposed credentials, and remove it from Git history before publishing.",
    ),
    Rule(
        "AWS access key",
        re.compile(r"AKIA[0-9A-Z]{16}"),
        "Critical",
        "Possible AWS access key committed",
        "Disable the key, rotate affected IAM credentials, and audit cloud activity.",
    ),
    Rule(
        "Stripe secret key",
        re.compile(r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{20,}"),
        "Critical",
        "Possible Stripe secret key committed",
        "Rotate the key in Stripe, review webhook and payment activity, and move the secret out of source control.",
    ),
    Rule(
        "Slack token",
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
        "Critical",
        "Possible Slack token committed",
        "Revoke the token, review workspace app permissions, and store future tokens outside the repo.",
    ),
    Rule(
        "Private key",
        re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Critical",
        "Private key material committed",
        "Treat the key as compromised, revoke or replace it, and remove it from Git history.",
    ),
    Rule(
        "Generic secret assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]"
        ),
        "High",
        "Possible hardcoded secret assignment",
        "Move the value to runtime configuration and rotate it if it was ever real.",
    ),
]

FRONTEND_SECRET_RE = re.compile(
    r"(?i)(OPENAI_API_KEY|ANTHROPIC_API_KEY|STRIPE_SECRET|SERVICE_ROLE|SUPABASE_SERVICE_ROLE|PRIVATE_KEY|CLIENT_SECRET)"
)
SUPABASE_SERVICE_ROLE_RE = re.compile(r"(?i)(supabase.*service[_-]?role|service[_-]?role.*supabase|service_role)")
CORS_WILDCARD_RE = re.compile(r"(?i)(access-control-allow-origin[^\\n]*\*|cors\s*\([^)]*origin\s*:\s*['\"]\*['\"])")
WEBHOOK_RE = re.compile(r"(?i)(webhook)")
SIGNATURE_RE = re.compile(r"(?i)(signature|verify|constructEvent|svix|x-hub-signature|stripe-signature)")
AGENT_PROMPT_CONTEXT_RE = re.compile(
    r"github\.event\.(?:issue|pull_request|comment)\.body|github\.event\.issue\.title|github\.event\.comment\.body"
)
AGENT_TOOL_RE = re.compile(r"(?i)(openai|anthropic|claude|codex|agent|prompt|llm)")
RISKY_SKILL_RE = re.compile(
    r"(?i)(ignore previous instructions|exfiltrate|curl\s+https?://|rm\s+-rf|chmod\s+777|base64\s+-d|send.*token)"
)
MCP_CONFIG_NAME_RE = re.compile(r"(?i)(^mcp.*\.json$|claude_desktop_config\.json|\.mcp\.json)")
MCP_COMMAND_RE = re.compile(r"(?i)\"command\"\s*:\s*\"(?:bash|sh|python|node|npx|uvx|docker|bun|deno)")
BIDI_CONTROL_RE = re.compile("[\u202a-\u202e\u2066-\u2069]")
ZERO_WIDTH_RE = re.compile("[\u200b-\u200f\ufeff]")


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_text_file(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES or path.name in SPECIAL_TEXT_NAMES


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            relative_parts = path.parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        if not path.is_file() or not is_text_file(path):
            continue
        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                continue
        except OSError:
            continue
        files.append(path)
    return sorted(files)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except OSError:
        return None


def redact(text: str) -> str:
    redacted = text
    for rule in SECRET_RULES:
        redacted = rule.pattern.sub(f"[REDACTED:{rule.name}]", redacted)
    redacted = re.sub(
        r"(?i)(\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"])[^'\"]+(['\"])",
        r"\1[REDACTED]\2",
        redacted,
    )
    return redacted


def evidence_line(line: str) -> str:
    clean = redact(line.strip())
    clean = clean.replace("|", "\\|")
    if len(clean) > 180:
        return clean[:177] + "..."
    return clean


def add_finding(
    findings: list[Finding],
    *,
    severity: str,
    category: str,
    title: str,
    path: str,
    line: int | None = None,
    evidence: str = "",
    recommendation: str,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            category=category,
            title=title,
            path=path,
            line=line,
            evidence=evidence,
            recommendation=recommendation,
        )
    )


def scan_secrets(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        text = read_text(path)
        if text is None:
            continue
        rel = relative(path, root)
        if path.name.startswith(".env") and path.name != ".env.example":
            add_finding(
                findings,
                severity="High",
                category="Secrets",
                title="Environment file appears committed",
                path=rel,
                evidence=path.name,
                recommendation="Keep real environment files outside source control; commit only sanitized examples.",
            )
        for number, line in enumerate(text.splitlines(), start=1):
            for rule in SECRET_RULES:
                if rule.pattern.search(line):
                    add_finding(
                        findings,
                        severity=rule.severity,
                        category="Secrets",
                        title=rule.title,
                        path=rel,
                        line=number,
                        evidence=evidence_line(line),
                        recommendation=rule.recommendation,
                    )
                    break
    return findings


def check_launch_readiness(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    required = {
        "README.md": ("Medium", "README is missing", "Add a clear README before public launch."),
        "LICENSE": ("Low", "License is missing", "Add a license so users know how the code may be used."),
        "SECURITY.md": ("Low", "Security policy is missing", "Add SECURITY.md with vulnerability reporting and secret-handling guidance."),
        ".gitignore": ("Medium", ".gitignore is missing", "Add a .gitignore that excludes local config, dependencies, build output, logs, and secrets."),
    }
    for name, (severity, title, recommendation) in required.items():
        if not (root / name).exists():
            add_finding(
                findings,
                severity=severity,
                category="Launch readiness",
                title=title,
                path=name,
                recommendation=recommendation,
            )

    workflows = list((root / ".github" / "workflows").glob("*.yml")) + list(
        (root / ".github" / "workflows").glob("*.yaml")
    )
    if not workflows:
        add_finding(
            findings,
            severity="Low",
            category="Launch readiness",
            title="No GitHub Actions workflow detected",
            path=".github/workflows/",
            recommendation="Add at least one lightweight validation workflow for public launch confidence.",
        )

    env_examples = list(root.glob(".env.example")) + list(root.glob("*.env.example"))
    if not env_examples:
        add_finding(
            findings,
            severity="Info",
            category="Launch readiness",
            title="No environment example detected",
            path=".env.example",
            recommendation="If the project needs runtime configuration, publish a sanitized .env.example.",
        )

    manifests = [
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
    ]
    if not any((root / manifest).exists() for manifest in manifests):
        add_finding(
            findings,
            severity="Info",
            category="Launch readiness",
            title="No dependency manifest detected",
            path=".",
            recommendation="If the repo has runtime dependencies, add a standard manifest so reviewers can inspect them.",
        )
    return findings


def is_frontend_path(path: Path, root: Path) -> bool:
    rel_parts = set(path.relative_to(root).parts)
    return bool(rel_parts & {"app", "components", "frontend", "pages", "public", "src", "web"}) or path.suffix in {
        ".html",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".vue",
    }


def is_code_path(path: Path) -> bool:
    return path.suffix in CODE_SUFFIXES or path.name in {"Dockerfile", "Makefile"}


def scan_agent_and_vibe_risks(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        text = read_text(path)
        if text is None:
            continue
        rel = relative(path, root)

        if BIDI_CONTROL_RE.search(text) or ZERO_WIDTH_RE.search(text):
            add_finding(
                findings,
                severity="High",
                category="Agent safety",
                title="Hidden Unicode control characters detected",
                path=rel,
                recommendation="Remove hidden Unicode characters; they can obscure instructions or alter code review meaning.",
            )

        if path.name == "SKILL.md" and RISKY_SKILL_RE.search(text):
            add_finding(
                findings,
                severity="High",
                category="Agent safety",
                title="Risky instruction pattern in agent skill",
                path=rel,
                evidence=evidence_line(RISKY_SKILL_RE.search(text).group(0)),
                recommendation="Review the skill manually before installing or allowing it to run tools.",
            )

        if path.name in {"AGENTS.md", "SKILL.md"}:
            add_finding(
                findings,
                severity="Info",
                category="Agent safety",
                title=f"{path.name} detected",
                path=rel,
                recommendation="Review agent instructions as executable trust boundaries, not just documentation.",
            )

        if MCP_CONFIG_NAME_RE.search(path.name) and MCP_COMMAND_RE.search(text):
            add_finding(
                findings,
                severity="Medium",
                category="Agent safety",
                title="MCP config launches a local command",
                path=rel,
                evidence=evidence_line(MCP_COMMAND_RE.search(text).group(0)),
                recommendation="Verify the command source, permissions, environment access, and update path before enabling the MCP server.",
            )

        if rel.startswith(".github/workflows/") and AGENT_PROMPT_CONTEXT_RE.search(text) and AGENT_TOOL_RE.search(text):
            add_finding(
                findings,
                severity="High",
                category="Agent safety",
                title="Workflow may pass untrusted GitHub text into an agent",
                path=rel,
                recommendation="Treat issue, PR, and comment text as untrusted input. Add allowlists, approval gates, and prompt boundaries.",
            )

        for number, line in enumerate(text.splitlines(), start=1):
            if is_frontend_path(path, root) and FRONTEND_SECRET_RE.search(line):
                add_finding(
                    findings,
                    severity="High",
                    category="Vibe-app risk",
                    title="Secret-like variable referenced in frontend code",
                    path=rel,
                    line=number,
                    evidence=evidence_line(line),
                    recommendation="Confirm this value is not bundled into client-side code. Move server-only secrets behind server routes.",
                )
            if is_frontend_path(path, root) and SUPABASE_SERVICE_ROLE_RE.search(line):
                add_finding(
                    findings,
                    severity="Critical",
                    category="Vibe-app risk",
                    title="Possible Supabase service-role exposure in client-side code",
                    path=rel,
                    line=number,
                    evidence=evidence_line(line),
                    recommendation="Never expose Supabase service-role keys to browsers. Rotate the key if it was shipped and enforce RLS with anon keys.",
                )
            if is_code_path(path) and CORS_WILDCARD_RE.search(line):
                add_finding(
                    findings,
                    severity="Medium",
                    category="Vibe-app risk",
                    title="Wildcard CORS policy detected",
                    path=rel,
                    line=number,
                    evidence=evidence_line(line),
                    recommendation="Restrict CORS origins to known domains unless this endpoint is intentionally public.",
                )

        if is_code_path(path) and WEBHOOK_RE.search(text) and not SIGNATURE_RE.search(text):
            add_finding(
                findings,
                severity="Medium",
                category="Vibe-app risk",
                title="Webhook code detected without obvious signature verification",
                path=rel,
                recommendation="Verify webhook signatures before trusting payloads. Manual review is required to confirm this finding.",
            )
    return findings


def audit_path(root: Path) -> list[Finding]:
    root = root.resolve()
    files = iter_text_files(root)
    findings = []
    findings.extend(scan_secrets(root, files))
    findings.extend(check_launch_readiness(root))
    findings.extend(scan_agent_and_vibe_risks(root, files))
    findings.sort(key=lambda item: (SEVERITY_ORDER[item.severity], item.category, item.path, item.line or 0, item.title))
    if not any(finding.category == "Secrets" for finding in findings):
        add_finding(
            findings,
            severity="Info",
            category="Secrets",
            title="No obvious secret patterns detected",
            path=".",
            recommendation="Continue using a dedicated secret scanner before public launch; this lightweight audit is not exhaustive.",
        )
    return sorted(
        findings,
        key=lambda item: (SEVERITY_ORDER[item.severity], item.category, item.path, item.line or 0, item.title),
    )


def severity_counts(findings: list[Finding]) -> dict[str, int]:
    return {severity: sum(1 for finding in findings if finding.severity == severity) for severity in SEVERITY_ORDER}


def finding_location(finding: Finding) -> str:
    if finding.line is None:
        return finding.path
    return f"{finding.path}:{finding.line}"


def render_report(root: Path, findings: list[Finding]) -> str:
    counts = severity_counts(findings)
    today = dt.date.today().isoformat()
    lines = [
        "# Vibe/Agent Repo Safety Audit",
        "",
        f"Date: {today}",
        f"Repository: `{root.name}`",
        "Audit type: lightweight launch/readiness review",
        "",
        "## Disclaimer",
        "",
        "This is a lightweight safety audit for launch readiness. It is not a certified penetration test, compliance attestation, or guarantee that the repository is secure.",
        "",
        "## Summary",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ]
    for severity in SEVERITY_ORDER:
        lines.append(f"| {severity} | {counts[severity]} |")
    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )

    if not findings:
        lines.append("No findings.")
    else:
        for index, finding in enumerate(findings, start=1):
            lines.extend(
                [
                    f"### {index}. {finding.title}",
                    "",
                    f"- Severity: {finding.severity}",
                    f"- Category: {finding.category}",
                    f"- Location: `{finding_location(finding)}`",
                ]
            )
            if finding.evidence:
                lines.append(f"- Evidence: `{finding.evidence}`")
            lines.extend(
                [
                    f"- Recommendation: {finding.recommendation}",
                    "",
                ]
            )

    lines.extend(
        [
            "## Next Steps",
            "",
            "- Fix Critical and High findings before launch.",
            "- Rotate any credential that may have been real.",
            "- Ask for a bounded fix package only after report findings are confirmed.",
            "",
            "Payment link for paid audits or fix packages: https://ko-fi.com/freecodex",
            "",
        ]
    )
    return "\n".join(lines)


def run_audit(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Audit path is not a directory: {root}", file=sys.stderr)
        return 2
    findings = audit_path(root)
    report = render_report(root, findings)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(f"Wrote audit report: {output}")
    else:
        print(report)
    counts = severity_counts(findings)
    print(
        "Findings: "
        + ", ".join(f"{severity}={counts[severity]}" for severity in SEVERITY_ORDER)
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FreeCodex lightweight repo safety audit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="audit a repository path")
    audit_parser.add_argument("--path", default=".", help="repository path to audit")
    audit_parser.add_argument("--output", help="markdown report output path")
    audit_parser.set_defaults(func=run_audit)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
