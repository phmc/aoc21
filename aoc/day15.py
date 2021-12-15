#!/usr/bin/env python3


import collections
import itertools
import sys
import typing
from typing import Iterable, Iterator, Mapping, Optional, Tuple


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."

# Cost of moving between adjacent points.
Costs = Mapping[Tuple[Point, Point], int]


def _get_neighbours(point: Point, points: set[Point]) -> Iterator[Point]:
    """Yield all neighbours of a point."""
    yield from (
        Point(x, y)
        for x, y in (
            (point.x + dx, point.y + dy)
            # Diagonals aren't connected.
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )
        if (x, y) in points
    )


T = typing.TypeVar("T")


def _smallest_valued_remaining(
    mapping: Mapping[T, Optional[int]], remaining: set[T]
) -> T:
    """Return the key with the smallest integer value."""
    result: Optional[T] = None
    least: int = 0
    for candidate, value in mapping.items():
        if value is not None and candidate in remaining:
            if result is None or value < least:
                result = candidate
                least = value
    assert result is not None
    return result


def _calculate_distance(costs: Costs, start: Point, end: Point) -> int:
    """Return the lowest total cost of all paths from one point to another."""
    unvisited = set(itertools.chain.from_iterable(costs))
    points = set(unvisited)
    # None ==> arbitrarily far away
    distance: dict[Point, Optional[int]] = {point: None for point in unvisited}
    distance[start] = 0

    current = start
    while unvisited and current != end:
        for neighbour in _get_neighbours(current, points):
            if neighbour not in unvisited:
                continue
            current_distance = distance[current]
            assert current_distance is not None
            potential_distance = current_distance + costs[current, neighbour]
            neighbour_distance = distance[neighbour]
            if neighbour_distance is None or neighbour_distance > potential_distance:
                distance[neighbour] = potential_distance
        unvisited.remove(current)
        current = _smallest_valued_remaining(distance, unvisited)

    result = distance[end]
    assert result is not None
    return result


def _get_edge_costs(entry_costs: dict[Point, int]) -> Costs:
    """Get adjacent-point movement costs from entry costs."""
    points = set(entry_costs)
    return {
        (neighbour, point): cost
        for point, cost in entry_costs.items()
        for neighbour in _get_neighbours(point, points)
    }


def _parse_input(lines: Iterable[str]) -> dict[Point, int]:
    """Parse input lines into entry costs."""
    lines = (line.strip() for line in lines)
    return {
        Point(x, y): int(cost)
        for y, row in enumerate(lines)
        for x, cost in enumerate(row)
    }


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        entry_costs = _parse_input(f)
        edge_costs = _get_edge_costs(entry_costs)
        max_x = max(point.x for point in entry_costs)
        max_y = max(point.y for point in entry_costs)
        print(_calculate_distance(edge_costs, Point(0, 0), Point(max_x, max_y)))


if __name__ == "__main__":
    main(sys.argv[1:])
