#!/usr/bin/env python3
"""Write one sentence to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The pitch is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 240 characters, not only white space.
"""

import os
import sys
from pathlib import Path

PITCH = "Your idea is already good enough, so describe it in plain words on make.fun today and an AI agent will turn it into your first real app for free, with you in charge and no coding needed at all."

MIN_CHARS = 1
MAX_CHARS = 240
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 240 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"pitch is {chars} characters, outside 1-240")
    if not text.strip():
        raise ValueError("pitch is only white space")
    return chars


def main() -> int:
    try:
        chars = validate(PITCH)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PITCH, encoding="utf-8")
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
