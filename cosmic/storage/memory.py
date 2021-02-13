import typing as t
from zope import interface
from dataclasses import dataclass, field
from cosmic.exceptions import OutOfStockException
from cosmic import interfaces


@interface.implementer(interfaces.IBatchRepository)
@dataclass
class BatchRepository:
    batches: t.List[interfaces.IBatch] = field(default_factory=list, init=False)

    def add_batch(self, batch):
        self.batches.append(batch)

    def is_allocated(self, line: interfaces.ILine) -> bool:
        for batch in self.batches:
            if batch.is_allocated(line):
                return True
        return False

    def allocate(self, line: interfaces.ILine) -> None:
        if self.is_allocated(line):
            return
        batches = [
            i for i in self.batches if i.sku == line.sku and i.quantity >= line.quantity
        ]
        if not batches:
            raise OutOfStockException(f"cannot allocate f{line}")
        batches.sort()
        batches[0].allocate(line)

    def deallocate(self, line: interfaces.ILine) -> None:
        for batch in self.batches:
            if batch.is_allocated(line):
                batch.deallocate(line)

    def allocate_order(self, order: interfaces.IOrder) -> None:
        try:
            for line in order.lines:
                self.allocate(line)
        except Exception:
            for line in order.lines:
                self.deallocate(line)
            raise
