#!/usr/bin/env python3

import collections
import itertools
import sys
import typing
from typing import Iterable, Iterator, Sequence


Cave = typing.NewType("Cave", str)
# Mapping from caves to neighbours.
Map = dict[Cave, set[Cave]]

_START = Cave("start")
_END = Cave("end")


def _is_big(cave: Cave) -> bool:
    """Return `True` if this cave is big."""
    return cave.isupper()


def _get_visits(path: Sequence[Cave]) -> tuple[set[Cave], bool]:
    """
    Return which caves have been visited.

    The second element of the returned tuple is `True` if some small cave has
    already been visited twice on this path, `False` otherwise.

    """
    visited: set[Cave] = set()
    two_small_visits = False
    for cave in path:
        if cave in visited and not _is_big(cave):
            two_small_visits = True
        visited.add(cave)
    return visited, two_small_visits


def _explore(
    path: Sequence[Cave], m: Map, only_one_small_visit: bool
) -> Iterator[tuple[Cave, ...]]:
    """Yield all possible next steps for a path."""
    visited, two_small_visits = _get_visits(path)
    for neighbour in m[path[-1]]:
        if (
            _is_big(neighbour)
            or neighbour not in visited
            or (
                not only_one_small_visit
                and not two_small_visits
                and neighbour != _START
            )
        ):
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
        for only_one_small_visit in (True, False):
            complete_paths: set[tuple[Cave, ...]] = set()
            incomplete_paths: set[tuple[Cave, ...]] = set([(_START,)])
            while incomplete_paths:
                path = incomplete_paths.pop()
                for extension in _explore(path, m, only_one_small_visit):
                    if extension[-1] == _END:
                        complete_paths.add(extension)
                    else:
                        incomplete_paths.add(extension)
            print(len(complete_paths))


if __name__ == "__main__":
    main(sys.argv[1:])
