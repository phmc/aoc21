#!/usr/bin/env python3

import sys
from typing import Iterable, Iterator, Optional

_DELIMS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def _score_corruption(char: str) -> int:
    """How well are we doing at being corrupt?"""
    return {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }[char]


def _find_corruption(line: str) -> Optional[str]:
    """Return the first corrupt character in a line, if any."""
    # Stack of chunk starting characters.
    scopes: list[str] = []
    for char in line:
        if char in _DELIMS:
            scopes.append(char)
        else:
            assert char in _DELIMS.values()
            if char != _DELIMS[scopes.pop()]:
                return char
    else:
        return None


def _parse_lines(lines: Iterable[str]) -> Iterator[str]:
    """Parse lines of input into lines of (unparsed) subsystem syntax."""
    for line in lines:
        yield line.strip()


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        lines = _parse_lines(f)
        maybe_corrupt_chars = (_find_corruption(line) for line in lines)
        corrupt_chars = (char for char in maybe_corrupt_chars if char is not None)
        print(sum(_score_corruption(char) for char in corrupt_chars))


if __name__ == "__main__":
    main(sys.argv[1:])
