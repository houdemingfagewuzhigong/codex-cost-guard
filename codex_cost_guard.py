#!/usr/bin/env python3
"""Estimate and guard AI coding-agent token burn from local transcripts."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


TEXT_EXTENSIONS = {".txt", ".md", ".json", ".jsonl", ".log"}
IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}

DEFAULT_PRICES = {
    "cheap": 0.25,
    "standard": 2.50,
    "premium": 10.00,
}


@dataclass
class Session:
    path: str
    chars: int
    estimated_tokens: int
    estimated_cost_usd: float
    turns: int
    risks: list[str]


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORE_DIRS]
        for filename in filenames:
            path = Path(current_root) / filename
            if path.suffix.lower() in TEXT_EXTENSIONS:
                yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def estimate_tokens(text: str) -> int:
    ascii_chars = sum(1 for ch in text if ord(ch) < 128)
    non_ascii_chars = len(text) - ascii_chars
    return max(1, round(ascii_chars / 4 + non_ascii_chars / 1.8))


def estimate_turns(text: str) -> int:
    jsonl_turns = 0
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if any(key in data for key in ("role", "message", "content", "type")):
            jsonl_turns += 1
    if jsonl_turns:
        return jsonl_turns
    markers = re.findall(r"(?im)^(user|assistant|system|tool|human|agent)\s*:", text)
    return len(markers)


def risks(tokens: int, turns: int, max_tokens: int, warn_turns: int) -> list[str]:
    result: list[str] = []
    if tokens >= max_tokens:
        result.append("token budget exceeded")
    elif tokens >= max_tokens * 0.8:
        result.append("near token budget")
    if turns >= warn_turns:
        result.append("long agent session")
    if tokens and turns and tokens / max(turns, 1) > 6000:
        result.append("large average turn")
    return result


def scan(root: Path, price_per_million: float, max_tokens: int, warn_turns: int) -> list[Session]:
    root = root.resolve()
    sessions: list[Session] = []
    for path in iter_files(root):
        text = read_text(path)
        if not text.strip():
            continue
        tokens = estimate_tokens(text)
        turns = estimate_turns(text)
        rel = path.name if root.is_file() else path.relative_to(root).as_posix()
        sessions.append(
            Session(
                path=rel,
                chars=len(text),
                estimated_tokens=tokens,
                estimated_cost_usd=round(tokens / 1_000_000 * price_per_million, 6),
                turns=turns,
                risks=risks(tokens, turns, max_tokens, warn_turns),
            )
        )
    return sorted(sessions, key=lambda item: (-item.estimated_tokens, item.path))


def sarif(sessions: list[Session]) -> dict:
    results = []
    for session in sessions:
        for risk in session.risks:
            results.append(
                {
                    "ruleId": "codex-cost-guard." + risk.replace(" ", "-"),
                    "level": "warning",
                    "message": {
                        "text": f"{session.path}: {risk} ({session.estimated_tokens} estimated tokens)"
                    },
                    "locations": [
                        {"physicalLocation": {"artifactLocation": {"uri": session.path}}}
                    ],
                }
            )
    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{"tool": {"driver": {"name": "codex-cost-guard", "rules": []}}, "results": results}],
    }


def print_table(sessions: list[Session]) -> None:
    if not sessions:
        print("No transcript-like files found.")
        return
    print("path,tokens,cost_usd,turns,risks")
    for session in sessions:
        print(
            f"{session.path},{session.estimated_tokens},{session.estimated_cost_usd:.6f},"
            f"{session.turns},{'|'.join(session.risks) or 'none'}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Estimate token burn and runaway-session risk for Codex, Claude Code, Cursor, and agent transcripts."
    )
    parser.add_argument("path", nargs="?", default=".", help="transcript file or directory")
    parser.add_argument("--price", type=float, default=DEFAULT_PRICES["standard"], help="USD per 1M tokens")
    parser.add_argument("--max-tokens", type=int, default=120_000, help="warn when a transcript exceeds this budget")
    parser.add_argument("--warn-turns", type=int, default=80, help="warn when a transcript has this many turns")
    parser.add_argument("--json", action="store_true", help="print JSON")
    parser.add_argument("--sarif", help="write SARIF to a file")
    args = parser.parse_args(argv)

    root = Path(args.path)
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    sessions = scan(root, args.price, args.max_tokens, args.warn_turns)
    if args.json:
        print(json.dumps([asdict(session) for session in sessions], indent=2))
    else:
        print_table(sessions)

    if args.sarif:
        Path(args.sarif).write_text(json.dumps(sarif(sessions), indent=2) + "\n")

    return 1 if any(session.risks for session in sessions) else 0


if __name__ == "__main__":
    raise SystemExit(main())
