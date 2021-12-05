#!/usr/bin/env python3


import collections
import dataclasses
import itertools
import sys
from typing import Iterable, Iterator


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."


def _range(start: int, end: int) -> Iterator[int]:
    """Yield integers in the interval `[start, end]`, in that order."""
    if start <= end:
        yield from range(start, end + 1)
    else:
        yield from range(start, end - 1, -1)


@dataclasses.dataclass
class Line:
    """Line in 2D space."""

    start: Point
    end: Point

    def is_horizontal(self) -> bool:
        """Is this line horizontal?"""
        return self.end.y == self.start.y

    def is_vertical(self) -> bool:
        """Is this line vertical?"""
        return self.end.x == self.start.x

    def points(self) -> Iterator[Point]:
        """Yield all integer-valued points on this line."""
        xs: Iterator[int]
        ys: Iterator[int]

        if self.is_vertical():
            xs = itertools.repeat(self.start.x)
            ys = _range(self.start.y, self.end.y)
        elif self.is_horizontal():
            xs = _range(self.start.x, self.end.x)
            ys = itertools.repeat(self.start.y)
        else:
            raise NotImplementedError

        yield from (Point(x, y) for x, y in zip(xs, ys))


def _parse_coordinates(coords: str) -> Point:
    """Parse an 'x,y' string pair into a Point."""
    x, y = coords.split(",")
    return Point(int(x), int(y))


def _parse_input(lines: Iterable[str]) -> Iterator[Line]:
    """Yield Lines parsed from lines of input."""
    # e.g. '309,347 -> 309,464'
    for line in lines:
        start, _, end = line.strip().split()
        yield Line(_parse_coordinates(start), _parse_coordinates(end))


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        lines = _parse_input(f)
        coverage = collections.Counter(
            itertools.chain.from_iterable(
                line.points()
                for line in lines
                if line.is_horizontal() or line.is_vertical()
            )
        )
        print(sum(int(point_coverage >= 2) for point_coverage in coverage.values()))


if __name__ == "__main__":
    main(sys.argv[1:])
