#!/usr/bin/env python3


import collections
import dataclasses
import heapq
import itertools
import sys
import typing
from typing import Generic, Iterable, Iterator, Mapping, Tuple


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."

# Cost of moving between adjacent points.
Costs = Mapping[Tuple[Point, Point], int]

# Bigger than any real distance...
INFINITY = 2 ** 64 - 1

T = typing.TypeVar("T")


@dataclasses.dataclass(order=True)
class _QElem(Generic[T]):
    """Element in a priority queue."""

    priority: int
    valid: bool
    item: T


class PriorityQueue(Generic[T]):
    """Boggo implementation of a priority queue using heapq as best we can."""

    _heap: list[_QElem[T]]
    _elements: dict[T, _QElem[T]]

    def __init__(self, items: Iterable[T], priority: int) -> None:
        self._heap = []
        self._elements = {}
        for item in items:
            self.add(item, priority)

    def add(self, item: T, priority: int) -> None:
        """Add an item with the given priority."""
        elem = _QElem(priority, True, item)
        heapq.heappush(self._heap, elem)
        self._elements[item] = elem

    def update(self, item: T, priority: int) -> None:
        """Update an item's priority."""
        if (elem := self._elements.get(item, None)) is not None:
            elem.valid = False
        self.add(item, priority)

    def pop(self) -> T:
        """Pop the lowest-priority item."""
        while self._heap:
            elem = heapq.heappop(self._heap)
            if elem.valid:
                del self._elements[elem.item]
                return elem.item
        else:
            raise ValueError("Popping from empty queue")


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


def _calculate_distance(costs: Costs, start: Point, end: Point) -> int:
    """Return the lowest total cost of all paths from one point to another."""
    points = set(itertools.chain.from_iterable(costs))
    distance: dict[Point, int] = {start: 0}
    queue = PriorityQueue(points, priority=INFINITY)
    queue.update(start, 0)

    while True:
        current = queue.pop()
        if current == end:
            break
        for neighbour in _get_neighbours(current, points):
            potential_distance = distance[current] + costs[current, neighbour]
            if neighbour not in distance or distance[neighbour] > potential_distance:
                distance[neighbour] = potential_distance
                queue.update(neighbour, potential_distance)

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
