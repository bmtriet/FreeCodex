#!/usr/bin/env python3
"""Validate the public FreeCodex workshop repository."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    ".gitignore",
    "docs/charter.md",
    "docs/operating-model.md",
    "docs/roadmap.md",
    "memory/README.md",
    "evals/README.md",
    "skills/README.md",
    "experiments/README.md",
    "templates/session-note.md",
    "templates/experiment-spec.md",
    "templates/skill-spec.md",
    "templates/eval-report.md",
    "scripts/validate_repo.py",
    ".github/workflows/validate.yml",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"gh[opsu]_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{12,}['\"]"),
]

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}


def git_files() -> list[Path]:
    """Return tracked, staged, and untracked files that are not ignored."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line.strip()]


def is_text_candidate(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}


def check_required_paths() -> list[str]:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    return [f"Missing required path: {path}" for path in missing]


def check_secret_patterns() -> list[str]:
    problems: list[str] = []
    for path in git_files():
        if not path.is_file() or not is_text_candidate(path):
            continue
        relative = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"Possible secret pattern in {relative}")
                break
    return problems


def main() -> int:
    problems = check_required_paths() + check_secret_patterns()
    if problems:
        print("FreeCodex validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("FreeCodex validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

