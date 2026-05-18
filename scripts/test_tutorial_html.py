#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InteractiveHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.buttons = 0
        self.inline_scripts: list[str] = []
        self.external_scripts: list[str] = []
        self._in_script = False
        self._script_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if "id" in attrs_dict and attrs_dict["id"]:
            self.ids.add(attrs_dict["id"])
        if tag == "button":
            self.buttons += 1
        if tag == "script":
            src = attrs_dict.get("src")
            if src:
                self.external_scripts.append(src)
            self._in_script = True
            self._script_chunks = []

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._script_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_script:
            self.inline_scripts.append("".join(self._script_chunks))
            self._in_script = False
            self._script_chunks = []


def assert_interactive_html(path: Path, required_ids: set[str], required_terms: set[str]) -> None:
    html = path.read_text(encoding="utf-8")
    parser = InteractiveHtmlParser()
    parser.feed(html)
    script_text = "\n".join(parser.inline_scripts)

    missing_ids = sorted(required_ids - parser.ids)
    if missing_ids:
        raise AssertionError(f"{path.name} missing interactive ids: {', '.join(missing_ids)}")

    missing_terms = sorted(term for term in required_terms if term not in html and term not in script_text)
    if missing_terms:
        raise AssertionError(f"{path.name} missing required terms: {', '.join(missing_terms)}")

    if parser.external_scripts:
        raise AssertionError(f"{path.name} must not load external scripts: {parser.external_scripts}")

    if parser.buttons < 2:
        raise AssertionError(f"{path.name} should expose multiple interactive controls")

    if "addEventListener" not in script_text:
        raise AssertionError(f"{path.name} has no scripted interactions")

    if "@keyframes" not in html:
        raise AssertionError(f"{path.name} has no animation keyframes")


def main() -> None:
    assert_interactive_html(
        ROOT / "OPEN_TUTORIAL.html",
        {
            "progressText",
            "progressBar",
            "stepList",
            "nextButton",
            "previousButton",
            "tourButton",
            "copyNarrationButton",
            "operatorToggle",
        },
        {"const scenes = [", "phoneRows", "narration", "operator"},
    )
    assert_interactive_html(
        ROOT / "BUILD_FROM_START.html",
        {
            "progressText",
            "progressBar",
            "stepList",
            "nextButton",
            "prevButton",
            "tourButton",
            "copyButton",
            "queueList",
        },
        {"const steps = [", "codex", "proof", "command"},
    )


if __name__ == "__main__":
    main()
