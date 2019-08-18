import domain


def test_order():
    lines = [domain.Line(order='1', sku=1, quantity=10)]
    order = domain.Order(reference=1, lines=lines)
    assert order.reference == 1
    assert order.lines
