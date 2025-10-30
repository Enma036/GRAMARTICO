"""Lightweight heuristics for improving writing in near real time."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class Suggestion:
    """Represents an actionable suggestion for a span of text."""

    start: int
    end: int
    message: str
    replacements: Sequence[str]

    def as_dict(self) -> dict:
        """Return a JSON serialisable representation."""

        return {
            "start": self.start,
            "end": self.end,
            "message": self.message,
            "replacements": list(self.replacements),
        }


class RealTimeWritingAssistant:
    """Analyse short snippets of text and raise potential issues."""

    def __init__(self) -> None:
        self._detectors = (
            self._detect_repeated_words,
            self._detect_repeated_spaces,
            self._detect_sentence_length,
            self._detect_spelling_typos,
            self._detect_missing_terminal_punctuation,
        )

    def analyse(self, text: str) -> List[Suggestion]:
        """Run all detectors against ``text`` and collect suggestions."""

        suggestions: List[Suggestion] = []
        for detector in self._detectors:
            suggestions.extend(detector(text))
        suggestions.sort(key=lambda item: item.start)
        return suggestions

    # British spelling for top-level API
    analyze = analyse

    _WORD_RE = re.compile(r"\b(\w+)(\s+)(\1)\b", re.IGNORECASE)

    def _detect_repeated_words(self, text: str) -> Iterable[Suggestion]:
        for match in self._WORD_RE.finditer(text):
            word = match.group(1)
            yield Suggestion(
                start=match.start(3),
                end=match.end(3),
                message=f"Repeated word '{word}' detected.",
                replacements=[""],
            )

    def _detect_repeated_spaces(self, text: str) -> Iterable[Suggestion]:
        for match in re.finditer(r" {2,}", text):
            yield Suggestion(
                start=match.start(),
                end=match.end(),
                message="Collapse repeated spaces into a single space.",
                replacements=[" "],
            )

    _SENTENCE_RE = re.compile(r"[^.!?]+")

    def _detect_sentence_length(self, text: str) -> Iterable[Suggestion]:
        for match in self._SENTENCE_RE.finditer(text):
            sentence = match.group()
            words = re.findall(r"\b\w+\b", sentence)
            if len(words) > 30:
                yield Suggestion(
                    start=match.start(),
                    end=match.end(),
                    message="Consider splitting long sentences for clarity.",
                    replacements=[],
                )

    _COMMON_TYPOS = {
        "teh": "the",
        "adn": "and",
        "recieve": "receive",
        "recieved": "received",
        "occurence": "occurrence",
    }

    def _detect_spelling_typos(self, text: str) -> Iterable[Suggestion]:
        for typo, correction in self._COMMON_TYPOS.items():
            for match in re.finditer(rf"\b{re.escape(typo)}\b", text, flags=re.IGNORECASE):
                replacement = correction if match.group().islower() else correction.capitalize()
                yield Suggestion(
                    start=match.start(),
                    end=match.end(),
                    message=f"Did you mean '{replacement}'?",
                    replacements=[replacement],
                )

    def _detect_missing_terminal_punctuation(self, text: str) -> Iterable[Suggestion]:
        stripped = text.rstrip()
        if not stripped:
            return []
        if stripped[-1] in ".!?":
            return []
        last_sentence_start = stripped.rfind("\n") + 1
        return [
            Suggestion(
                start=last_sentence_start,
                end=len(stripped),
                message="Add terminal punctuation to complete the sentence.",
                replacements=[stripped + "."],
            )
        ]
