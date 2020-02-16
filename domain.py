from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set
from datetime import datetime
import typing as t


@dataclass
class Product:
    sku: str


@dataclass(unsafe_hash=True)
class Line:
    order: str = field(hash=True)
    sku: str = field(hash=True)
    quantity: int = field(compare=False)


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

    def allocate(self, line: Line) -> None:
        if line in self.allocations:
            return
            return True  # ???: not clear behavior, move to can_allocate maybe?
        assert self.can_allocate(line), "Cannot allocate"
        self.allocations.add(line)
        self.quantity -= line.quantity

    def deallocate(self, line: Line) -> None:
        self.allocations.remove(line)
        self.quantity += line.quantity


@dataclass
class BatchRepository:
    batches: List[Batch] = field(default_factory=list)


def allocate_order(batch_repository: BatchRepository, order: Order) -> None:
    for line in order.lines:
        allocate_line(batch_repository, line)


def allocate_line(batch_repository: BatchRepository, line: Line) -> None:
    batches = [i for i in batch_repository.batches if i.sku == line.sku and i.quantity >= line.quantity]
    assert batches, f"cannot allocate f{line}"
    batches.sort()
    batches[0].allocate(line)
