from cosmic import models


def test_order():
    lines = {models.Line(order="1", sku=1, quantity=10)}
    order = models.Order(reference=1, lines=lines)
    assert order.reference == 1
    assert order.lines
