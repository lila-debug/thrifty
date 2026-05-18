from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {".py", ".ts", ".tsx", ".md"}
SKIPPED_PARTS = {
    ".claude",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "agents",
    "__pycache__",
}
SKIPPED_NAMES = {
    "goal.md",
    "uv.lock",
    "lint_copy.py",
}
SKIPPED_DOCS = {
    "01-PRD.md",
    "02-ARCHITECTURE.md",
    "03-DATA-MODEL.md",
    "04-API-CONTRACT.md",
    "05-BACKLOG.md",
}


def terms() -> tuple[str, ...]:
    pieces = [
        ("co", "lor"),
        ("organ", "ize"),
        ("organ", "ization"),
        ("favor", "ite"),
        ("cen", "ter"),
        ("fi", "ber"),
        ("licen", "se"),
        ("real", "ize"),
        ("optim", "ize"),
        ("gon", "na"),
        ("wan", "na"),
        ("awes", "ome"),
        ("total", "ly"),
        ("absolute", "ly"),
        ("no wor", "ries"),
        ("sounds ", "good"),
        ("happy to ", "help"),
    ]
    return tuple("".join(piece) for piece in pieces)


def should_skip(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if any(part in SKIPPED_PARTS for part in relative.parts):
        return True
    if path.name in SKIPPED_NAMES:
        return True
    return path.name in SKIPPED_DOCS and relative.parts[:1] == ("docs",)


def iter_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix in SUFFIXES and not should_skip(path)
    )


def has_allow_marker(line: str) -> bool:
    return "allow-americanism" in line


def main() -> int:
    patterns = [(term, re.compile(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", re.I)) for term in terms()]
    for path in iter_files():
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if has_allow_marker(line):
                continue
            for term, pattern in patterns:
                if pattern.search(line):
                    relative = path.relative_to(ROOT)
                    print(f"{relative}:{number}:{term}")
                    return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
