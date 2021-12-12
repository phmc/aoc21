#!/usr/bin/env python3

import collections
import itertools
import sys
import typing
from typing import Iterable, Iterator, Sequence


Cave = typing.NewType("Cave", str)
# Mapping from caves to neighbours.
Map = dict[Cave, set[Cave]]


def _is_big(cave: Cave) -> bool:
    """Return `True` if this cave is big."""
    return cave.isupper()


def _explore(path: Sequence[Cave], m: Map) -> Iterator[tuple[Cave, ...]]:
    """Yield all possible next steps for a path."""
    visited = set(path)
    for neighbour in m[path[-1]]:
        if _is_big(neighbour) or neighbour not in visited:
            yield tuple(itertools.chain(path, [neighbour]))


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
        start = Cave("start")
        end = Cave("end")
        complete_paths: set[tuple[Cave, ...]] = set()
        incomplete_paths: set[tuple[Cave, ...]] = set([(start,)])
        while incomplete_paths:
            path = incomplete_paths.pop()
            for extension in _explore(path, m):
                if extension[-1] == end:
                    complete_paths.add(extension)
                else:
                    incomplete_paths.add(extension)
        print(len(complete_paths))


if __name__ == "__main__":
    main(sys.argv[1:])
