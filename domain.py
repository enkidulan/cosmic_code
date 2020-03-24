from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set
from datetime import datetime
import typing as t


class OutOfStockException(Exception):
    pass


@dataclass
class Product:
    sku: str


@dataclass(unsafe_hash=True)
class Line:
    order: str = field(hash=True)
    sku: str = field(hash=True)
    quantity: int = field(hash=True)


@dataclass
class Order:
    reference: str
    lines: List[Line] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class Batch:
    reference: str = field(hash=True)
    sku: str = field(compare=False)
    quantity: int = field(compare=False)
    eta: t.Optional[datetime] = field(compare=False, default=None)
    allocations: Set[Line] = field(compare=False, default_factory=set, init=False)
    purchased_quantity: int = field(compare=False, init=False)

    def __post_init__(self) -> None:
        assert isinstance(self.reference, str)
        assert self.reference
        assert isinstance(self.sku, str)
        assert self.sku
        assert isinstance(self.eta, datetime) or self.eta is None
        assert isinstance(self.quantity, int)
        assert self.quantity > 0
        self.purchased_quantity = self.quantity  # maybe make sense to make vise versa?

    def __gt__(self, other: Batch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def can_allocate(self, line: Line) -> bool:
        if self.sku != line.sku:
            return False
        if not (self.quantity - line.quantity >= 0):
            return False
        return True

    def is_allocated(self, line: Line) -> bool:
        return line in self.allocations

    def allocate(self, line: Line) -> None:
        if self.is_allocated(line):
            return
        if not self.can_allocate(line):
            raise OutOfStockException(f"Cannot allocate f{line}")
        self.allocations.add(line)
        self.quantity -= line.quantity

    def deallocate(self, line: Line) -> None:
        self.allocations.remove(line)
        self.quantity += line.quantity


@dataclass
class BatchRepository:
    batches: List[Batch] = field(default_factory=list)

    def is_allocated(self, line: Line) -> bool:
        for batch in self.batches:
            if batch.is_allocated(line):
                return True
        return False

    def allocate(self, line: Line) -> None:
        if self.is_allocated(line):
            return
        batches = [i for i in self.batches if i.sku == line.sku and i.quantity >= line.quantity]
        if not batches:
            raise OutOfStockException(f"cannot allocate f{line}")
        batches.sort()
        batches[0].allocate(line)

    def deallocate(self, line: Line) -> None:
        for batch in self.batches:
            if batch.is_allocated(line):
                batch.deallocate(line)


def allocate_order(batch_repository: BatchRepository, order: Order) -> None:
    try:
        for line in order.lines:
            batch_repository.allocate(line)
    except Exception:
        for line in order.lines:
            batch_repository.deallocate(line)
        raise
