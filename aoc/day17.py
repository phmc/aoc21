#!/usr/bin/env python3

import collections
import dataclasses
import sys
from typing import Iterable, Iterator, Optional


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


def _next_x_speed(speed: int) -> int:
    """Return the speed in the X direction for the next step."""
    if speed == 0:
        return 0
    else:
        return abs(speed - 1) * speed // abs(speed)


def _step(p: Point, v: Velocity) -> tuple[Point, Velocity]:
    """Return the new position and velocity after a step."""
    return (
        Point(p.x + v.x, p.y + v.y),
        Velocity(_next_x_speed(v.x), v.y - 1),
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


def _find_suitable_x_speed(
    initial_p: Point, initial_y_speed: int, target: Area
) -> Optional[int]:
    """Find an initial speed in the x direction that hits the target."""
    # An upper bound is abs(target.max_x), so just try every value starting there!
    for x in range(target.max_x, 0, -1):
        if target.contains(_fire(initial_p, Velocity(x, initial_y_speed), target)):
            return x
    else:
        return None


def _find_max_y_speed(initial_p: Point, target: Area) -> Velocity:
    """Find the maximum possible initial speed in the y direction."""
    # When the projectile is passing through the line y=0 on its way down, its
    # speed in the y direction must be greater than the speed at which it was
    # launched.
    #
    # So (assuming that the target y range lies below the x axis) it's
    # pointless trying any y speed greater than abs(target.min_y). This
    # provides a definite upper bound; find the max value below this that
    # works.
    for y in range(abs(target.min_y), 0, -1):
        if (x := _find_suitable_x_speed(initial_p, y, target)) is not None:
            return Velocity(x, y)
    else:
        raise ValueError(
            "Couldn't find any speed to hit {target} starting from {initial_p}"
        )


def _find_max_height(initial_p: Point, target: Area) -> int:
    """Find the maximum height that can be attained before finishing in the target."""
    return max(
        point.y
        for point in _trajectory(
            initial_p, _find_max_y_speed(initial_p, target), target
        )
    )


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
        print(_find_max_height(Point(0, 0), target))


if __name__ == "__main__":
    main(sys.argv[1:])
