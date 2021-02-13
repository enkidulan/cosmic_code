from datetime import datetime
from cosmic import models


def batch(
    reference="reference-1", sku="TEST-LAMP", quantity=20, eta=datetime(1999, 1, 1)
):
    return models.Batch(reference=reference, sku=sku, quantity=quantity, eta=eta)


def line(order="order-1", sku="TEST-LAMP", quantity=10):
    return models.Line(order=order, sku=sku, quantity=quantity)


def _lines_factory():
    return [
        line(quantity=5),
        line(quantity=3),
        line(quantity=2),
    ]


def order(reference="reference-1", lines=None):
    if lines is None:
        lines = set(_lines_factory())
    return models.Order(reference=reference, lines=lines)


def allocation(batch_repository, batches=None, order_=None, lines=None):
    if batches is None:
        batches = [
            batch(quantity=5, eta=datetime(1999, 1, 1)),
            batch(quantity=4, eta=None),
            batch(quantity=10, eta=datetime(2000, 1, 1)),
        ]
    for batch_obj in batches:
        batch_repository.add_batch(batch_obj)
    if order_ is None:
        if lines is None:
            lines = _lines_factory()
        order_ = order(lines=set(lines))
    batch_repository.allocate_order(order_)
    return batches, order_, lines
