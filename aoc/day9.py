#!/usr/bin/env python3

import collections
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


def _get_neighbour_heights(m: Map, p: Point) -> set[int]:
    """Return heights of a point's neighbours."""
    return {m[neighbour] for neighbour in _get_neighbours(m, p)}


def _find_low_points(m: Map) -> Iterator[Point]:
    """Yield all low points in a map."""
    return (
        point
        for point, height in m.items()
        if all(height < n_height for n_height in _get_neighbour_heights(m, point))
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
        print(sum(1 + m[point] for point in _find_low_points(m)))


if __name__ == "__main__":
    main(sys.argv[1:])
