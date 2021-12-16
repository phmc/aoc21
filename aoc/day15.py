#!/usr/bin/env python3


import collections
import dataclasses
import heapq
import itertools
import sys
import typing
from typing import Callable, Generic, Iterable, Iterator, Mapping, Tuple


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."

# Cost of moving to a point.
Costs = Mapping[Point, int]

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


def _get_possible_neighbours(point: Point) -> Iterator[Point]:
    """Yield all neighbours of a point (might not be part of the grid)."""
    yield from (
        Point(x, y)
        for x, y in (
            (point.x + dx, point.y + dy)
            # Diagonals aren't connected.
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )
    )


def _calculate_distance(costs: Costs, start: Point, end: Point) -> int:
    """Return the lowest total cost of all paths from one point to another."""
    points = set(costs)
    distance: dict[Point, int] = {start: 0}
    queue = PriorityQueue(points, priority=INFINITY)
    queue.update(start, 0)

    while True:
        current = queue.pop()
        if current == end:
            break
        for neighbour in _get_possible_neighbours(current):
            try:
                potential_distance = distance[current] + costs[neighbour]
            except KeyError:
                continue
            if neighbour not in distance or distance[neighbour] > potential_distance:
                distance[neighbour] = potential_distance
                queue.update(neighbour, potential_distance)

    return distance[end]


def _parse_input(lines: Iterable[str]) -> Costs:
    """Parse input lines into entry costs."""
    lines = (line.strip() for line in lines)
    return {
        Point(x, y): int(cost)
        for y, row in enumerate(lines)
        for x, cost in enumerate(row)
    }


def _multiply_input(initial_costs: Costs, n: int) -> dict[Point, int]:
    """Multiply entry costs n times, according to the rules of part 2."""
    result: dict[Point, int] = {}

    def new_cost(idx: int, x: int, y: int) -> int:
        nominal_cost = template[Point(x, y)] + idx
        if nominal_cost > 9:
            return nominal_cost % 10 + 1
        else:
            return nominal_cost

    # Repeat horizontally first.
    template = initial_costs
    upper_x = max(point.x for point in template) + 1
    upper_y = max(point.y for point in template) + 1
    for idx, x, y in itertools.product(range(n), range(upper_x), range(upper_y)):
        result[Point(x + idx * upper_x, y)] = new_cost(idx, x, y)

    # Now repeat that extended chunk vertically.
    template = result
    upper_x = max(point.x for point in template) + 1
    for idx, x, y in itertools.product(range(n), range(upper_x), range(upper_y)):
        result[Point(x, y + idx * upper_y)] = new_cost(idx, x, y)

    return result


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        initial_costs = _parse_input(f)
        for costs in (
            initial_costs,
            _multiply_input(initial_costs, n=5),
        ):
            max_x = max(point.x for point in costs)
            max_y = max(point.y for point in costs)
            print(_calculate_distance(costs, Point(0, 0), Point(max_x, max_y)))


if __name__ == "__main__":
    main(sys.argv[1:])
