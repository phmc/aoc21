#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import enum
import functools
import operator
import sys
from typing import Callable, Iterable, Iterator, Optional


_VERSION_LEN = 3
_TYPE_ID_LEN = 3
_NIBBLE_HEAD_LEN = 1
_NIBBLE_LEN = 4
_OP_HEAD_LEN = 1
_OP_BIT_COUNT_LEN = 15
_OP_SUB_COUNT_LEN = 11


VAR_OP = Callable[[Iterable[int]], int]


class PacketType(enum.Enum):
    """Enumeration of packet types."""

    SUM = 0b000
    PRODUCT = 0b001
    MINIMUM = 0b010
    MAXIMUM = 0b011
    LITERAL = 0b100
    GT = 0b101
    LT = 0b110
    EQ = 0b111

    def is_operator(self) -> bool:
        """Is this type an operator type?"""
        return self is not self.LITERAL

    def to_operator(self) -> VAR_OP:
        """Return the operator function corresponding to this packet type."""
        if not self.is_operator():
            raise ValueError("Can't get an operator for a non-operator type")
        if self is self.SUM:
            return sum
        elif self is self.PRODUCT:
            return lambda values: functools.reduce(operator.mul, values, 1)
        elif self is self.MINIMUM:
            return min
        elif self is self.MAXIMUM:
            return max
        elif self is self.GT:
            return lambda values: operator.gt(*values)
        elif self is self.LT:
            return lambda values: operator.lt(*values)
        elif self is self.EQ:
            return lambda values: operator.eq(*values)
        else:
            raise NotImplementedError


class OperatorLengthType(enum.Enum):
    """Enumeration of operator packet length types."""

    BIT_COUNT = 0
    SUB_COUNT = 1


@dataclasses.dataclass
class Packet:
    """Parsed packet."""

    version: int
    type: PacketType
    value: Optional[int]
    sub_packets: tuple[Packet, ...]
    length: int

    def descendants(self) -> Iterator[Packet]:
        """Yield all descendant sub-packets (and this packet itself)."""
        yield self
        for sub in self.sub_packets:
            yield from sub.descendants()


class _Parser:
    """Tracks parsing state for a single packet."""

    src: Iterator[str]
    bits_read: int = 0

    def __init__(self, src: Iterator[str]) -> None:
        self.src = src

    def __repr__(self) -> str:
        return f"{type(self).__name__}(bits_read={self.bits_read})"

    def parse(self) -> Packet:
        """Execute the parsing."""
        version = self._parse_version()
        packet_type = self._parse_type()
        value = None
        sub_packets: tuple[Packet, ...] = ()

        if packet_type is PacketType.LITERAL:
            value = self._parse_literal_body()

        elif packet_type.is_operator():
            sub_packets = tuple(self._parse_sub_packets())

        else:
            raise NotImplementedError

        return Packet(version, packet_type, value, sub_packets, length=self.bits_read)

    # ---------------------------------------------------------------------------
    # Implementation details
    #

    def _read(self, n: int) -> str:
        """Read n characters and return as a string."""
        chars = []
        for _ in range(n):
            try:
                chars.append(next(self.src))
            except StopIteration:
                raise RuntimeError("Unexpected end of string")
        self.bits_read += n
        return "".join(chars)

    def _read_int(self, n: int) -> int:
        """Read n characters and return as an int."""
        return int(self._read(n), 2)

    def _parse_version(self) -> int:
        """Parse a packet version."""
        return self._read_int(_VERSION_LEN)

    def _parse_type(self) -> PacketType:
        """Parse a packet type."""
        return PacketType(self._read_int(_TYPE_ID_LEN))

    def _parse_literal_body(self) -> int:
        """Parse the contents of a literal packet."""
        nibbles: list[str] = []
        while True:
            more = self._read_int(_NIBBLE_HEAD_LEN)
            nibbles.append(self._read(_NIBBLE_LEN))
            if not more:
                break
        return int("".join(nibbles), 2)

    def _parse_sub_packet(self) -> Packet:
        """Helper to parse a single sub-packet."""
        return type(self)(self.src).parse()

    def _parse_sub_packets(self) -> Iterator[Packet]:
        """Parse sub-packets in an operator packet."""
        length_type = OperatorLengthType(self._read_int(_OP_HEAD_LEN))
        if length_type is OperatorLengthType.BIT_COUNT:
            bit_count = self._read_int(_OP_BIT_COUNT_LEN)
            bits_read = 0
            while bits_read < bit_count:
                packet = self._parse_sub_packet()
                bits_read += sum(p.length for p in packet.descendants())
                yield packet
            if bits_read != bit_count:
                raise RuntimeError(
                    f"Expected to read {bit_count} bits, but only parsed {bits_read}"
                )

        elif length_type is OperatorLengthType.SUB_COUNT:
            sub_count = self._read_int(_OP_SUB_COUNT_LEN)
            for _ in range(sub_count):
                yield self._parse_sub_packet()


@dataclasses.dataclass
class Expression:
    """Tree of operations on integers."""

    operator: VAR_OP
    operands: list[Expression | int]

    @classmethod
    def _get_operand_from_packet(cls, packet: Packet) -> Expression | int:
        """Return the appropriate operand for a packet."""
        if packet.type.is_operator():
            return cls.from_packet(packet)
        else:
            assert packet.value is not None
            return packet.value

    @classmethod
    def from_packet(cls, packet: Packet) -> Expression:
        """Create an expression correponding to a[n operator] packet."""
        return cls(
            packet.type.to_operator(),
            [cls._get_operand_from_packet(sub) for sub in packet.sub_packets],
        )

    def _eval_operands(self) -> Iterator[int]:
        """Yield int operands, evaluating sub-expressions where necessary."""
        for operand in self.operands:
            if isinstance(operand, int):
                yield operand
            else:
                yield operand.eval()

    def eval(self) -> int:
        """Evaluate this expression."""
        return self.operator(self._eval_operands())


def _hextobin(hexstr: Iterable[str]) -> Iterator[str]:
    """Given a hex string, yield corresponding binary string characters."""
    for char in hexstr:
        yield from f"{int(char, 16):04b}"


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        binstr = _hextobin(f.read().strip())
        packet = _Parser(binstr).parse()
        print(sum(p.version for p in packet.descendants()))
        expr = Expression.from_packet(packet)
        print(expr.eval())


if __name__ == "__main__":
    main(sys.argv[1:])
