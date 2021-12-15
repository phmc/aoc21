#!/usr/bin/env python3

import collections
import dataclasses
import enum
import sys
from typing import Iterable, Iterator

Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."


class Direction(enum.Enum):
    """Enumeration of possible fold directions."""

    LEFT = 1
    UP = 2


@dataclasses.dataclass
class Fold:
    """Fold instructions."""

    direction: Direction
    position: int


def _transform(points: Iterable[Point], fold: Fold) -> Iterator[Point]:
    """Yield the new position for points after applying a fold."""
    for point in points:
        if fold.direction is Direction.LEFT:
            if point.x <= fold.position:
                yield Point(point.x, point.y)
            else:
                yield Point(2 * fold.position - point.x, point.y)
        elif fold.direction is Direction.UP:
            if point.y <= fold.position:
                yield Point(point.x, point.y)
            else:
                yield Point(point.x, 2 * fold.position - point.y)
        else:
            raise NotImplementedError


def _parse_dots(lines: Iterator[str]) -> Iterator[Point]:
    """
    Yield all points where a dot appears, parsed from the input.

    Stops after consuming the first blank line.

    """
    for line in lines:
        line = line.strip()
        if not line:
            break
        x, y = line.split(",")
        yield Point(int(x), int(y))


def _parse_folds(lines: Iterator[str]) -> Iterator[Fold]:
    """
    Yield folds parsed from the input.

    Consumes the whole iterator.

    """
    for line in lines:
        line = line.strip()
        assert line.startswith("fold along ")
        instruction = line.split()[-1]
        variable, position = instruction.split("=")
        if variable == "x":
            direction = Direction.LEFT
        else:
            assert variable == "y"
            direction = Direction.UP
        yield Fold(direction, position=int(position))


def _print_grid(dots: Iterable[Point]) -> None:
    """Plot the dots."""
    dots = set(dots)
    max_x = max(dot.x for dot in dots)
    max_y = max(dot.y for dot in dots)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in dots:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        dots = set(_parse_dots(f))
        folds = _parse_folds(f)
        fold = next(folds)
        dots = set(_transform(dots, fold))
        print(len(dots))
        for fold in folds:
            dots = set(_transform(dots, fold))
        _print_grid(dots)


if __name__ == "__main__":
    main(sys.argv[1:])
