#!/usr/bin/env python3
"""Use LLMGate as a public-safe coding co-worker.

The script sends only explicitly selected context files to LLMGate, asks for a
review or unified diff, and saves the proposal under ignored `local/`. It never
commits, pushes, or applies changes by default.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import llm_gateway


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "local" / "llm-coworker"
DEFAULT_MAX_CONTEXT_BYTES = 80_000
DEFAULT_MAX_FILE_BYTES = 30_000

DENIED_PARTS = {
    ".git",
    ".local",
    ".venv",
    "artifacts",
    "coverage",
    "dist",
    "exports",
    "local",
    "logs",
    "node_modules",
    "private",
    "screenshots",
    "tmp",
    "venv",
}

DENIED_NAMES = {
    ".env",
    ".netrc",
    "credentials",
    "credentials.json",
    "id_ed25519",
    "id_rsa",
}

DENIED_SUFFIXES = {
    ".key",
    ".p12",
    ".pem",
    ".pfx",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"gh[opsu]_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{12,}['\"]"),
]

REVIEW_SECTIONS = ["# Summary", "# Findings", "# Suggested Changes", "# Risks"]


@dataclass(frozen=True)
class ContextFile:
    path: Path
    relative: str
    text: str

    @property
    def size(self) -> int:
        return len(self.text.encode("utf-8"))


class PolicyError(RuntimeError):
    pass


def repo_relative(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(ROOT)
    except ValueError as error:
        raise PolicyError(f"Context file is outside repo: {path}") from error


def is_denied_path(relative: Path) -> bool:
    parts = set(relative.parts)
    name = relative.name
    if parts & DENIED_PARTS:
        return True
    if name in DENIED_NAMES or name.startswith(".env."):
        return True
    if any(name.startswith(prefix) for prefix in ("credentials.", "secrets.")):
        return True
    return relative.suffix in DENIED_SUFFIXES


def detect_secret(text: str) -> str | None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            return pattern.pattern
    return None


def read_context_file(path: Path) -> ContextFile:
    relative = repo_relative(path)
    if is_denied_path(relative):
        raise PolicyError(f"Refusing denied context path: {relative}")
    absolute = ROOT / relative
    if not absolute.is_file():
        raise PolicyError(f"Context path is not a file: {relative}")
    if absolute.stat().st_size > DEFAULT_MAX_FILE_BYTES:
        raise PolicyError(f"Context file exceeds {DEFAULT_MAX_FILE_BYTES} bytes: {relative}")
    raw = absolute.read_bytes()
    if b"\x00" in raw:
        raise PolicyError(f"Refusing binary context file: {relative}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PolicyError(f"Context file is not UTF-8 text: {relative}") from error
    secret_pattern = detect_secret(text)
    if secret_pattern:
        raise PolicyError(f"Possible secret pattern in context file: {relative}")
    return ContextFile(path=absolute, relative=relative.as_posix(), text=text)


def load_task(args: argparse.Namespace) -> str:
    if bool(args.task) == bool(args.task_file):
        raise SystemExit("Provide exactly one of --task or --task-file")
    if args.task:
        task = args.task.strip()
    else:
        task_path = Path(args.task_file)
        relative = repo_relative(task_path)
        if is_denied_path(relative):
            raise SystemExit(f"Refusing denied task file: {relative}")
        task = (ROOT / relative).read_text(encoding="utf-8").strip()
    if not task:
        raise SystemExit("Task must not be empty")
    if detect_secret(task):
        raise SystemExit("Task appears to contain a secret pattern; refusing to send")
    return task


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:64] or "llm-coding-task"


def proposal_dir(output_dir: Path, task: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return output_dir / f"{timestamp}-{slugify(task)}"


def build_prompt(mode: str, task: str, contexts: list[ContextFile]) -> str:
    context_blocks = []
    for context in contexts:
        context_blocks.append(
            "\n".join(
                [
                    f"--- FILE: {context.relative} ---",
                    context.text,
                    f"--- END FILE: {context.relative} ---",
                ]
            )
        )

    output_contract = (
        "Output only a valid unified diff. Keep edits minimal. Use relative repo paths. "
        "Do not modify local/, .git/, .env files, credentials, private data, or generated secrets."
        if mode == "diff"
        else "Output Markdown with exactly these sections: # Summary, # Findings, # Suggested Changes, # Risks."
    )

    return "\n\n".join(
        [
            "You are a coding co-worker operating on the public FreeCodex repository.",
            "Use only the task and selected context files below.",
            "Never request or expose secrets, private user data, raw chat logs, credentials, or account access.",
            "If context is insufficient, say so in the required output format instead of inventing hidden files.",
            f"Mode: {mode}",
            f"Output contract: {output_contract}",
            f"Task:\n{task}",
            "Selected context files:\n" + "\n".join(f"- {context.relative}" for context in contexts),
            "Context:\n" + "\n\n".join(context_blocks),
        ]
    )


def request_llm(args: argparse.Namespace, prompt: str) -> str:
    config = llm_gateway.load_config(args.env)
    base_url, api_key = llm_gateway.require_config(config)
    model = args.model or config.get("LLMGATE_CODE_MODEL") or config.get("LLMGATE_DEFAULT_MODEL", "gpt-5.5")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    data = llm_gateway.request_json(
        base_url=base_url,
        api_key=api_key,
        path="/chat/completions",
        method="POST",
        payload=payload,
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


def extract_diff(response: str) -> str:
    fenced = re.search(r"```(?:diff|patch)?\n(.*?)```", response, re.DOTALL)
    diff = fenced.group(1).strip() if fenced else response.strip()
    if not (diff.startswith("diff --git ") or diff.startswith("--- ")):
        raise PolicyError("LLMGate response is not a unified diff")
    if "\n+++ " not in diff:
        raise PolicyError("LLMGate diff is missing +++ file marker")
    denied_targets = [".git/", "local/", ".env", "private/", "memory/private/"]
    for line in diff.splitlines():
        if line.startswith(("--- ", "+++ ", "diff --git ")):
            for target in denied_targets:
                if target in line:
                    raise PolicyError(f"Diff touches denied target: {line}")
    return diff + "\n"


def validate_review(response: str) -> str:
    missing = [section for section in REVIEW_SECTIONS if section not in response]
    if missing:
        raise PolicyError(f"Review response missing sections: {', '.join(missing)}")
    return response.rstrip() + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_apply_check(diff_path: Path, cwd: Path) -> tuple[bool, str]:
    completed = subprocess.run(
        ["git", "apply", "--check", str(diff_path)],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    output = completed.stdout + completed.stderr
    return completed.returncode == 0, output.strip()


def build_contexts(paths: list[str], max_context_bytes: int) -> list[ContextFile]:
    contexts = [read_context_file(Path(path)) for path in paths]
    total = sum(context.size for context in contexts)
    if total > max_context_bytes:
        raise PolicyError(f"Selected context exceeds {max_context_bytes} bytes")
    return contexts


def summarize(result: dict[str, Any], json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(f"Task: {result['task']}")
    print(f"Mode: {result['mode']}")
    print(f"Context files: {len(result['context_files'])}")
    print(f"Proposal dir: {result['proposal_dir']}")
    if result.get("response_file"):
        print(f"Response: {result['response_file']}")
    if result.get("apply_check") is not None:
        print(f"Apply check: {'PASS' if result['apply_check'] else 'FAIL'}")
    print(f"Next step: {result['next_step']}")


def command_main(args: argparse.Namespace) -> int:
    try:
        task = load_task(args)
        contexts = build_contexts(args.context, args.max_context_bytes)
        prompt = build_prompt(args.mode, task, contexts)
        out_dir = proposal_dir(args.output_dir.resolve(), task)
        out_dir.mkdir(parents=True, exist_ok=False)
        manifest = [context.relative for context in contexts]

        (out_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        (out_dir / "context-manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
        write_json(
            out_dir / "request.json",
            {
                "mode": args.mode,
                "model": args.model or "configured-default",
                "task": task,
                "context_files": manifest,
                "max_context_bytes": args.max_context_bytes,
                "no_send": args.no_send,
            },
        )

        result: dict[str, Any] = {
            "task": task,
            "mode": args.mode,
            "proposal_dir": str(out_dir.relative_to(ROOT)) if out_dir.is_relative_to(ROOT) else str(out_dir),
            "context_files": manifest,
            "response_file": None,
            "apply_check": None,
            "next_step": "codex_review_test_apply",
        }

        if args.no_send:
            result["next_step"] = "review_prompt_then_send"
            write_json(out_dir / "meta.json", result)
            summarize(result, args.json)
            return 0

        response = request_llm(args, prompt)
        if args.mode == "diff":
            response_text = extract_diff(response)
            response_path = out_dir / "response.diff"
        else:
            response_text = validate_review(response)
            response_path = out_dir / "review.md"
        response_path.write_text(response_text, encoding="utf-8")
        result["response_file"] = response_path.name

        if args.check_apply and args.mode == "diff":
            passed, output = run_apply_check(response_path, ROOT)
            (out_dir / "apply-check.txt").write_text(output + "\n", encoding="utf-8")
            result["apply_check"] = passed
            if not passed:
                result["next_step"] = "codex_review_patch_failed_apply_check"
        write_json(out_dir / "meta.json", result)
        summarize(result, args.json)
        return 0
    except PolicyError as error:
        print(f"Blocked by LLM co-worker policy: {error}", file=sys.stderr)
        return 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Use LLMGate as a public-safe coding co-worker")
    parser.add_argument("--task", help="short task text")
    parser.add_argument("--task-file", help="path to a public-safe task file")
    parser.add_argument("--context", action="append", required=True, help="context file to send; repeatable")
    parser.add_argument("--mode", choices=["diff", "review"], default="diff")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--check-apply", action="store_true", help="run git apply --check on generated diff")
    parser.add_argument("--model", help="LLMGate model id; defaults to LLMGATE_CODE_MODEL or gpt-5.5")
    parser.add_argument("--max-context-bytes", type=int, default=DEFAULT_MAX_CONTEXT_BYTES)
    parser.add_argument("--max-tokens", type=int, default=2400)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--env", type=Path, default=None)
    parser.add_argument("--no-send", action="store_true", help="build artifacts without calling LLMGate")
    parser.add_argument("--json", action="store_true", help="print machine-readable summary")
    parser.set_defaults(func=command_main)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
