from dataclasses import dataclass, field
from typing import List, Set
from datetime import datetime


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
    eta: datetime = field(compare=False, default=None)
    allocations: Set[Line] = field(compare=False, default_factory=set, init=False)
    purchased_quantity: int = field(compare=False, init=False)

    def __post_init__(self):
        assert isinstance(self.reference, str)
        assert self.reference
        assert isinstance(self.sku, str)
        assert self.sku
        assert isinstance(self.eta, datetime) or self.eta is None
        assert isinstance(self.quantity, int)
        assert self.quantity > 0
        self.purchased_quantity = self.quantity  # maybe make sense to make vise versa?

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def can_allocate(self, line: Line):
        if line in self.allocations:
            return True  # ???: not clear behavior
        if self.sku != line.sku:
            return False
        if not (self.quantity - line.quantity >= 0):
            return False
        return True

    def allocate(self, line: Line):
        assert self.can_allocate(line), "Cannot allocate"
        self.allocations.add(line)
        self.quantity -= line.quantity

    def deallocate(self, line: Line):
        self.allocations.remove(line)
        self.quantity += line.quantity


@dataclass
class BatchRepository:
    batches: List[Batch] = field(default_factory=list)


def allocate_order(batch_repository, order):
    for line in order.lines:
        line_can_be_allocated(batch_repository, line)
    for line in order.lines:
        allocate_line(batch_repository, line)


def line_can_be_allocated(batch_repository, line):
    batches = [i for i in batch_repository.batches if i.sku == line.sku and i.quantity >= line.quantity]
    assert batches, f"cannot allocate f{line}"


def allocate_line(batch_repository, line):
    batches = [i for i in batch_repository.batches if i.sku == line.sku and i.quantity >= line.quantity]
    batches.sort()
    batches[0].allocate(line)
