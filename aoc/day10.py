#!/usr/bin/env python3

import enum
import functools
import sys
from typing import Callable, Iterable, Iterator, Sequence, Union

_DELIMS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


class LineState(enum.Enum):
    """Possible states for a line."""

    CORRUPT = 1
    INCOMPLETE = 2


def _score_corruption(char: str) -> int:
    """How well are we doing at being corrupt?"""
    return {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }[char]


def _score_completing_char(char: str) -> int:
    """Score an individual character in an autocomplete."""
    step = lambda score, char: score * 5
    return {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }[char]


def _score_completion(chars: Iterable[str]) -> int:
    """What do you think of my autocomplete efforts?"""
    score_char: Callable[
        [int, str], int
    ] = lambda score, char: score * 5 + _score_completing_char(char)
    return functools.reduce(score_char, chars, 0)


# My kingdom for an ADT...
def _get_line_state(line: str) -> tuple[LineState, Union[str, list[str]]]:
    """
    Look for corruption or incompleteness in a line.

    Returns a (state, relevant data) pair. The second element is one of:

    - The corrupt character
    - The sequence of unclosed opening delimiters causing incompleteness

    """
    # Stack of chunk starting characters.
    scopes: list[str] = []
    for char in line:
        if char in _DELIMS:
            scopes.append(char)
        else:
            assert char in _DELIMS.values()
            if char != _DELIMS[scopes.pop()]:
                return LineState.CORRUPT, char
    else:
        return LineState.INCOMPLETE, scopes


def _get_completion(unclosed_delims: Sequence[str]) -> Iterator[str]:
    """Yield characters required to complete a line."""
    for char in reversed(unclosed_delims):
        yield _DELIMS[char]


def _parse_lines(lines: Iterable[str]) -> Iterator[str]:
    """Parse lines of input into lines of (unparsed) subsystem syntax."""
    for line in lines:
        yield line.strip()


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        lines = _parse_lines(f)
        states = [_get_line_state(line) for line in lines]
        corrupt_chars = (data for (state, data) in states if state is LineState.CORRUPT)
        print(sum(_score_corruption(char) for char in corrupt_chars))  # type: ignore
        autocompletes = (
            _get_completion(data)
            for (state, data) in states
            if state is LineState.INCOMPLETE
        )
        scores = sorted(_score_completion(chars) for chars in autocompletes)
        print(scores[(len(scores) - 1) // 2])


if __name__ == "__main__":
    main(sys.argv[1:])
