#!/usr/bin/env python3

import collections
import itertools
import sys
import typing
from typing import Iterable, Iterator, Mapping, Sequence


# Pair of polymer bases
Pair = typing.NewType("Pair", tuple[str, str])

# Mapping from pairs to base inserted between such a pair
Rules = Mapping[Pair, str]


def _generate(pair: Pair, rules: Rules) -> Iterator[Pair]:
    """Generate the to-be-inserted pairs for a current pair."""
    insert = rules[pair]
    yield Pair((pair[0], insert))
    yield Pair((insert, pair[1]))


def _run_pair_insertion(
    pairs: collections.Counter[Pair], rules: Rules
) -> collections.Counter[Pair]:
    """Run a single pair insertion step."""
    result: collections.Counter[Pair] = collections.Counter()
    for pair, count in pairs.items():
        result.update(
            {next_gen_pair: count for next_gen_pair in _generate(pair, rules)}
        )
    return result


def _count_elements(
    pairs: collections.Counter[Pair], first: str, last: str
) -> collections.Counter[str]:
    """Count how many times each element appears in a final polymer."""
    # Each element occurence is part of exactly two pairs, except the first and
    # last.
    #
    # Therefore ensure *every* element is double-counted then half at the end.
    elements: collections.Counter[str] = collections.Counter()
    # Might be the same, so two updates just in case.
    elements.update({first: 1})
    elements.update({last: 1})
    for pair, count in pairs.items():
        for element in pair:
            elements.update({element: count})
    return collections.Counter(
        {element: double_count // 2 for element, double_count in elements.items()}
    )


def _calculate_final_quantity(
    pairs: collections.Counter[Pair], template: Sequence[Pair]
) -> int:
    """Return the final quantity for output."""
    elements = _count_elements(pairs, template[0][0], template[-1][-1])
    (_, most_count), *_, (_, least_count) = elements.most_common()
    return most_count - least_count


def _pairs(src: Iterable[str]) -> Iterator[tuple[str, str]]:
    """Yield consecutive character pairs from an iterable of characters."""
    it, incr_it = itertools.tee(iter(src), 2)
    try:
        next(incr_it)
    except StopIteration:
        return
    yield from zip(it, incr_it)


def _parse_template(lines: Iterator[str]) -> Iterator[Pair]:
    """Yield initial pairs, parsed from input lines."""
    for line in lines:
        line = line.strip()
        if not line:
            break
        for pair in _pairs(line):
            yield Pair(pair)


def _parse_rules(lines: Iterator[str]) -> Rules:
    """Return pair generation rules, parsed from input lines."""
    rules: dict[Pair, str] = {}
    for line in lines:
        line = line.strip()
        pair, op, element = line.split()
        assert op == "->"
        rules[Pair((pair[0], pair[1]))] = element
    return rules


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        template = list(_parse_template(f))
        pairs = collections.Counter(template)
        rules = _parse_rules(f)
        for iterations in (10, 40 - 10):
            for _ in range(iterations):
                pairs = _run_pair_insertion(pairs, rules)
            print(_calculate_final_quantity(pairs, template))


if __name__ == "__main__":
    main(sys.argv[1:])
