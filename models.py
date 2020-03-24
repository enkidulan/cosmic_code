from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import typing as t
from zope import interface
from exceptions import OutOfStockException

import interfaces


@interface.implementer(interfaces.IProduct)
@dataclass
class Product:
    sku: str


@interface.implementer(interfaces.ILine)
@dataclass(unsafe_hash=True)
class Line:
    order: str = field(hash=True)
    sku: str = field(hash=True)
    quantity: int = field(hash=True)


@interface.implementer(interfaces.IOrder)
@dataclass
class Order:
    reference: str
    lines: t.List[interfaces.ILine] = field(default_factory=list)


@interface.implementer(interfaces.IBatch)
@dataclass(unsafe_hash=True)
class Batch:
    reference: str = field(hash=True)
    sku: str = field(compare=False)
    quantity: int = field(compare=False)
    eta: t.Optional[datetime] = field(compare=False, default=None)
    allocations: t.Set[interfaces.ILine] = field(compare=False, default_factory=set, init=False)
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

    def __gt__(self, other: interfaces.IBatch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def can_allocate(self, line: interfaces.ILine) -> bool:
        if self.sku != line.sku:
            return False
        if not (self.quantity - line.quantity >= 0):
            return False
        return True

    def is_allocated(self, line: interfaces.ILine) -> bool:
        return line in self.allocations

    def allocate(self, line: interfaces.ILine) -> None:
        if self.is_allocated(line):
            return
        if not self.can_allocate(line):
            raise OutOfStockException(f"Cannot allocate f{line}")
        self.allocations.add(line)
        self.quantity -= line.quantity

    def deallocate(self, line: interfaces.ILine) -> None:
        self.allocations.remove(line)
        self.quantity += line.quantity
