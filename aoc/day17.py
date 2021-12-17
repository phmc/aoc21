#!/usr/bin/env python3

import collections
import dataclasses
import sys
from typing import Iterable, Iterator


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."


Velocity = collections.namedtuple("Velocity", ["x", "y"])
Velocity.__doc__ = "Velocity in 2D space."


@dataclasses.dataclass
class Area:
    """Rectangular region."""

    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def contains(self, p: Point) -> bool:
        """Does a point lie within this area?"""
        return self.min_x <= p.x <= self.max_x and self.min_y <= p.y <= self.max_y


def _step(p: Point, v: Velocity) -> tuple[Point, Velocity]:
    """Return the new position and velocity after a step."""
    return (
        Point(p.x + v.x, p.y + v.y),
        Velocity(0 if not v.x else abs(v.x - 1) * v.x // abs(v.x), v.y - 1),
    )


def _trajectory(initial_p: Point, initial_v: Velocity, target: Area) -> Iterator[Point]:
    """
    Run steps until the current position is within the target area, or past it.

    Yields the position after each step.

    """
    p = initial_p
    v = initial_v
    while True:
        # Within or beyond the target (in some direction).
        if p.x >= target.min_x and p.y <= target.max_y:
            break
        # Definitely beyond the target!
        elif p.x > target.max_x or p.y < target.min_y:
            break
        p, v = _step(p, v)
        yield p


def _fire(initial_p: Point, initial_v: Velocity, target: Area) -> Point:
    """
    Run steps until the current position is within the target area, or past it.

    Returns the final position.

    """
    return collections.deque(_trajectory(initial_p, initial_v, target), maxlen=1)[0]


def _find_possible_velocities(initial_p: Point, target: Area) -> Iterator[Velocity]:
    """Yield all initial velocities that hit the target.."""
    # When the projectile is passing through the line y=0 on its way down, its
    # speed in the y direction must be greater than the speed at which it was
    # launched.  So it's pointless trying any y speed greater than
    # abs(target.min_y).
    #
    # For the x direction, an upper bound is target.max_x (this time assuming
    # the target area is positive), so just try every value starting there!
    #
    # All of this assumes that the x targets are positive and the y targets
    # negative!
    assert target.max_y < 0 and target.min_y < 0
    assert target.max_x > 0 and target.min_x > 0

    yield from (
        Velocity(x, y)
        for y in range(target.min_y, (-target.min_y) + 1)
        for x in range(1, target.max_x + 1)
        if target.contains(_fire(initial_p, Velocity(x, y), target))
    )


def _find_max_height(initial_p: Point, initial_v: Velocity, target: Area) -> int:
    """Find the maximum height attained on a trajectory."""
    return max(point.y for point in _trajectory(initial_p, initial_v, target))


def _parse_input(lines: Iterable[str]) -> Area:
    """Parse the target area from input lines."""
    lines = (line.strip() for line in lines)
    line = next(lines)
    _, coords = line.split(":")
    xs, ys = coords.split(",")
    min_x, _, max_x = xs.split(".")
    min_y, _, max_y = ys.split(".")
    return Area(
        int(min_x.strip().removeprefix("x=")),
        int(max_x),
        int(min_y.strip().removeprefix("y=")),
        int(max_y),
    )


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        target = _parse_input(f)
        velocities = list(_find_possible_velocities(Point(0, 0), target))
        print(
            max(
                _find_max_height(Point(0, 0), velocity, target)
                for velocity in velocities
            )
        )
        print(len(velocities))


if __name__ == "__main__":
    main(sys.argv[1:])
