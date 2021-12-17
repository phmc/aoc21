#!/usr/bin/env python3


import collections
import dataclasses
import enum
import itertools
import sys
from typing import Callable, Iterable, Iterator, Optional


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


class TestResult(enum.Enum):
    """Result of a test during a binary search."""

    INCONCLUSIVE = 0
    TOO_LOW = 1
    OK = 2
    TOO_HIGH = 3


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


def _do_binary_search(test: Callable[[int], TestResult]) -> Optional[int]:
    """Find an integer that satisfies a test or `None` if no solution exists."""
    lower_bound = 1
    upper_bound: int

    # Three steps:
    #
    # 1. Starting at 1, double until an initial upper bound is established.
    # 2. Binary search in the [1, upper bound] interval until an OK value is found.
    # 3. If we're missing the target for some value in the interval,
    #    exhaustively test all remaining values.

    for n in itertools.count():
        candidate = 2 ** n
        result = test(candidate)
        assert result is not TestResult.INCONCLUSIVE
        if test(candidate) is TestResult.TOO_LOW:
            lower_bound = candidate
        else:
            upper_bound = candidate
            break

    while abs(upper_bound - lower_bound) > 0:
        candidate = int((upper_bound + lower_bound) / 2)
        result = test(candidate)
        if result is TestResult.OK:
            return candidate
        elif result is TestResult.TOO_HIGH:
            upper_bound = candidate
        elif result is TestResult.TOO_LOW:
            lower_bound = candidate
        elif result is TestResult.INCONCLUSIVE:
            break

    if upper_bound != lower_bound:
        for candidate in range(lower_bound, upper_bound + 1):
            if test(candidate) is TestResult.OK:
                return candidate

    return None


def _test_x_speed(initial_p: Point, test_v: Velocity, target: Area) -> TestResult:
    """Evaluate the success of a candidate speed in the x direction."""
    final_p = _fire(initial_p, test_v, target)
    if final_p.x < target.min_x:
        return TestResult.TOO_LOW
    elif final_p.x > target.max_x:
        return TestResult.TOO_HIGH
    elif target.contains(final_p):
        return TestResult.OK
    else:
        return TestResult.INCONCLUSIVE


def _find_suitable_x_speed(
    initial_p: Point, initial_y_speed: int, target: Area
) -> Optional[int]:
    """Find an initial speed in the x direction that hits the target."""
    return _do_binary_search(
        lambda candidate: _test_x_speed(
            initial_p, Velocity(candidate, initial_y_speed), target
        )
    )


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
    # When the projectile is passing through the line y=0 on its way down, its
    # speed in the y direction must be greater than the speed at which it was
    # launched.
    #
    # So (assuming that the target y range lies below the x axis) it's
    # pointless trying any y speed greater than abs(target.min_y). This
    # provides a definite upper bound; find the max value below this that
    # works.
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
