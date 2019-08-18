from tests import faker


def test_line():
    line = faker.line()
    assert line.order == 'order-1'
    assert line.sku == 'TEST-LAMP'
    assert line.quantity == 10
