#!/usr/bin/env python3

import collections
import functools
import operator
import sys

from typing import Iterable, Iterator


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."


# Mapping from points to floor heights.
Map = dict[Point, int]


def _get_neighbours(m: Map, p: Point) -> set[Point]:
    """Return neighbours of a point."""
    return {
        Point(x, y)
        for x, y in [
            (p.x - 1, p.y),
            (p.x + 1, p.y),
            (p.x, p.y - 1),
            (p.x, p.y + 1),
        ]
        if (x, y) in m
    }


def _find_low_points(m: Map) -> Iterator[Point]:
    """Yield all low points in a map."""
    return (
        point
        for point in m
        if all(m[point] < m[neighbour] for neighbour in _get_neighbours(m, point))
    )


def _find_basin(m: Map, low_point: Point) -> Iterator[Point]:
    """Yield all points in the basin draining to a low point."""
    candidates: set[Point] = set([low_point])
    visited: set[Point] = set()
    while candidates:
        current = candidates.pop()
        visited.add(current)
        yield current
        candidates.update(
            neighbour
            for neighbour in _get_neighbours(m, current)
            if neighbour not in visited
            and neighbour not in candidates
            and m[neighbour] < 9
        )


def _parse_input(lines: Iterable[str]) -> Map:
    """Parse lines of input into a height map."""
    lines = (line.strip() for line in lines)
    return {
        Point(x, y): int(height)
        for y, row in enumerate(lines)
        for x, height in enumerate(row)
    }


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        m = _parse_input(f)
        low_points = set(_find_low_points(m))
        print(sum(1 + m[point] for point in low_points))
        basins = (_find_basin(m, low_point) for low_point in low_points)
        sizes = (len(list(basin)) for basin in basins)
        print(functools.reduce(operator.mul, sorted(sizes)[-3:]))


if __name__ == "__main__":
    main(sys.argv[1:])
