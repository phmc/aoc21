#!/usr/bin/env python3

from __future__ import annotations

import collections
import functools
import sys
import typing
from typing import Iterable, Iterator, NamedTuple


Cave = typing.NewType("Cave", str)
# Mapping from caves to neighbours.
Map = dict[Cave, set[Cave]]

_START = Cave("start")
_END = Cave("end")


@functools.cache
def _is_big(cave: Cave) -> bool:
    """Return `True` if this cave is big."""
    return cave.isupper()


class Path(NamedTuple):
    """Path through caves; might be incomplete."""

    path: tuple[Cave, ...]
    may_revisit_small: bool


def _explore(path: Path, m: Map) -> Iterator[Path]:
    """Yield all possible extensions of this path."""
    seen = set(path.path)
    for neighbour in m[path.path[-1]]:
        if (
            (big := _is_big(neighbour))
            or (unseen_small := neighbour not in seen)
            or (path.may_revisit_small and neighbour != _START)
        ):
            yield Path(
                path.path + (neighbour,),
                False if (not big and not unseen_small) else path.may_revisit_small,
            )


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
            complete_paths: set[Path] = set()
            incomplete_paths: set[Path] = set([Path((_START,), may_revisit_small)])
            while incomplete_paths:
                path = incomplete_paths.pop()
                for extension in _explore(path, m):
                    if extension.path[-1] == _END:
                        complete_paths.add(extension)
                    else:
                        incomplete_paths.add(extension)
            print(len(complete_paths))


if __name__ == "__main__":
    main(sys.argv[1:])
