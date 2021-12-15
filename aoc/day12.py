#!/usr/bin/env python3

from __future__ import annotations

import collections
import functools
import sys
import typing
from typing import Iterable


Cave = typing.NewType("Cave", str)
# Mapping from caves to neighbours.
Map = dict[Cave, set[Cave]]

_START = Cave("start")
_END = Cave("end")


@functools.cache
def _is_big(cave: Cave) -> bool:
    """Return `True` if this cave is big."""
    return cave.isupper()


def _count_paths(m: Map, may_ever_revisit_small: bool) -> int:
    """Count the number of paths from start to end."""
    complete_paths = 0
    pending: list[tuple[bool, frozenset[Cave], Cave]] = [
        (may_ever_revisit_small, frozenset(), _START)
    ]
    while pending:
        may_revisit_small, visited, cave = pending.pop()
        for neighbour in m[cave]:
            if neighbour == _END:
                complete_paths += 1
            elif neighbour == _START:
                continue
            elif _is_big(neighbour):
                pending.append((may_revisit_small, visited, neighbour))
            elif neighbour not in visited:
                pending.append(
                    (
                        may_revisit_small,
                        visited | set([neighbour]),
                        neighbour,
                    )
                )
            elif may_revisit_small and neighbour != _START:
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
        first, second = (Cave(tok) for tok in line.strip().split("-"))
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
