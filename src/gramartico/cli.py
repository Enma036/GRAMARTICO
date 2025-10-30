"""Command line interface for the Gramartico assistant."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

from .analyzer import RealTimeWritingAssistant


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyse text and suggest improvements.")
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to analyse. If omitted the assistant reads from stdin.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit suggestions as JSON for integration with editors.",
    )
    return parser


def _iter_text(args: argparse.Namespace) -> Iterable[str]:
    if args.text:
        yield " ".join(args.text)
    else:
        for line in sys.stdin:
            yield line


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    assistant = RealTimeWritingAssistant()
    suggestions = []
    for chunk in _iter_text(args):
        suggestions.extend(assistant.analyse(chunk))

    if args.as_json:
        json.dump([item.as_dict() for item in suggestions], sys.stdout)
        sys.stdout.write("\n")
        return 0

    if not suggestions:
        print("No issues detected. Keep writing!")
        return 0

    for suggestion in suggestions:
        replacements = ", ".join(suggestion.replacements) or "(no suggestion)"
        print(f"{suggestion.start}-{suggestion.end}: {suggestion.message} → {replacements}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
