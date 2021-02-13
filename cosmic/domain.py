from __future__ import annotations
from .interfaces import IBatchRepository, IOrder


def allocate_order(batch_repository: IBatchRepository, order: IOrder) -> None:
    try:
        for line in order.lines:
            batch_repository.allocate(line)
    except:
        for line in order.lines:
            batch_repository.deallocate(line)
        raise
