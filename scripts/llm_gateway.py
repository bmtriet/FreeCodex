#!/usr/bin/env python3
"""Small OpenAI-compatible gateway client for quota-frugal fallback work."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_ENV_FILE = Path("local/llmgate.env")


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def load_config(env_path: Path | None) -> dict[str, str]:
    config = dict(os.environ)
    if env_path is not None:
        config.update(parse_env_file(env_path))
    elif DEFAULT_ENV_FILE.exists():
        config.update(parse_env_file(DEFAULT_ENV_FILE))
    return config


def require_config(config: dict[str, str]) -> tuple[str, str]:
    base_url = config.get("LLMGATE_BASE_URL", "").rstrip("/")
    api_key = config.get("LLMGATE_API_KEY", "")
    if not base_url:
        raise SystemExit("Missing LLMGATE_BASE_URL")
    if not api_key:
        raise SystemExit("Missing LLMGATE_API_KEY")
    return base_url, api_key


def request_json(
    *,
    base_url: str,
    api_key: str,
    path: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    body = None
    headers = {"Authorization": f"Bearer {api_key}"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        f"{base_url}{path}",
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        detail = detail.replace(api_key, "[REDACTED]")
        raise SystemExit(f"Gateway HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Gateway request failed: {error.reason}") from error


def command_models(args: argparse.Namespace) -> int:
    config = load_config(args.env)
    base_url, api_key = require_config(config)
    data = request_json(base_url=base_url, api_key=api_key, path="/models", timeout=args.timeout)
    for item in data.get("data", []):
        model_id = item.get("id")
        if model_id:
            print(model_id)
    return 0


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("Provide --prompt or pipe prompt text on stdin")


def command_chat(args: argparse.Namespace) -> int:
    config = load_config(args.env)
    base_url, api_key = require_config(config)
    model = args.model or config.get("LLMGATE_DEFAULT_MODEL", "gpt-5.4-mini")
    prompt = read_prompt(args)
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    data = request_json(
        base_url=base_url,
        api_key=api_key,
        path="/chat/completions",
        method="POST",
        payload=payload,
        timeout=args.timeout,
    )
    choices = data.get("choices") or []
    if not choices:
        print(json.dumps(data, indent=2, sort_keys=True))
        return 0
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                text_parts.append(part.get("text", ""))
        content = "\n".join(text_parts)
    print(str(content).strip())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Use a local OpenAI-compatible LLM gateway")
    parser.add_argument(
        "--env",
        type=Path,
        default=None,
        help="env file to load; defaults to local/llmgate.env when present",
    )
    parser.add_argument("--timeout", type=int, default=60, help="request timeout in seconds")
    subparsers = parser.add_subparsers(dest="command", required=True)

    models = subparsers.add_parser("models", help="list available models")
    models.set_defaults(func=command_models)

    chat = subparsers.add_parser("chat", help="send one prompt to the gateway")
    chat.add_argument("--model", help="model id; defaults to LLMGATE_DEFAULT_MODEL")
    chat.add_argument("--prompt", help="prompt text; stdin is used when omitted")
    chat.add_argument("--temperature", type=float, default=0.2)
    chat.add_argument("--max-tokens", type=int, default=800)
    chat.set_defaults(func=command_chat)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

