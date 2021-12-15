#!/usr/bin/env python3

from __future__ import annotations

import collections
import sys
import typing
from typing import Iterable


Cave = typing.NewType("Cave", str)
# Mapping from caves to neighbours.
Map = dict[Cave, set[Cave]]

# Singleton instances of caves, allowing comparison by identity.
_CAVES: dict[str, Cave] = {}


def _make_cave(id: str) -> Cave:
    """Create a cave, or reuse the existing cave with the same ID."""
    if id not in _CAVES:
        _CAVES[id] = Cave(id)
    return _CAVES[id]


_START = _make_cave("start")
_END = _make_cave("end")


def _is_big(cave: Cave) -> bool:
    """Return `True` if this cave is big."""
    return cave.isupper()


def _count_paths(m: Map, may_ever_revisit_small: bool) -> int:
    """Count the number of paths from start to end."""
    complete_paths = 0
    small_caves = set(
        cave
        for cave in m
        if not _is_big(cave) and cave is not _START and cave is not _END
    )
    pending: list[tuple[bool, frozenset[Cave], Cave]] = [
        (may_ever_revisit_small, frozenset(), _START)
    ]
    while pending:
        may_revisit_small, visited, cave = pending.pop()
        for neighbour in m[cave]:
            if neighbour is _END:
                complete_paths += 1
            elif neighbour is _START:
                continue
            elif neighbour not in small_caves:
                pending.append((may_revisit_small, visited, neighbour))
            elif neighbour not in visited:
                pending.append(
                    (
                        may_revisit_small,
                        visited | set([neighbour]),
                        neighbour,
                    )
                )
            elif may_revisit_small:
                pending.append(
                    (
                        False,
                        visited | set([neighbour]),
                        neighbour,
                    )
                )
    return complete_paths


def _parse_input(lines: Iterable[str]) -> Map:
    """Parse a cave map from input lines."""
    m: Map = collections.defaultdict(set)
    for line in lines:
        first, second = (_make_cave(tok) for tok in line.strip().split("-"))
        m[first].add(second)
        m[second].add(first)
    return dict(m)


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        m = _parse_input(f)
        for may_revisit_small in (False, True):
            print(_count_paths(m, may_revisit_small))


if __name__ == "__main__":
    main(sys.argv[1:])
