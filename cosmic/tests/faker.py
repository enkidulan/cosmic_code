from datetime import datetime
from cosmic import models


def batch(
    reference="reference-1", sku="TEST-LAMP", quantity=20, eta=datetime(1999, 1, 1)
):
    return models.Batch(reference=reference, sku=sku, quantity=quantity, eta=eta)


def line(order="order-1", sku="TEST-LAMP", quantity=10):
    return models.Line(order=order, sku=sku, quantity=quantity)


def order(reference="reference-1", lines=None):
    if lines is None:
        lines = {
            line(quantity=5),
            line(quantity=3),
            line(quantity=2),
        }
    return models.Order(reference=reference, lines=lines)
