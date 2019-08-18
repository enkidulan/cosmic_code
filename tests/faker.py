from datetime import datetime
import domain


def batch(reference="reference-1", sku="TEST-LAMP", quantity=20, eta=datetime(1999, 1, 1)):
    return domain.Batch(reference=reference, sku=sku, quantity=quantity, eta=eta)


def line(order='order-1', sku="TEST-LAMP", quantity=10):
    return domain.Line(order=order, sku=sku, quantity=quantity)


def order(reference="reference-1", lines=None):
    if lines is None:
        lines = [
            line(quantity=5),
            line(quantity=3),
            line(quantity=2),
        ]
    return domain.Order(reference=reference, lines=lines)


def batch_repository(batches=None):
    if batches is None:
        batches = [
            batch(quantity=5, eta=datetime(1999, 1, 1)),
            batch(quantity=4, eta=None),
            batch(quantity=10, eta=datetime(2000, 1, 1)),
        ]
    return domain.BatchRepository(batches)
