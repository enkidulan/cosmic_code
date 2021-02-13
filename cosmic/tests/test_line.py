from cosmic.tests import faker


def test_line():
    line = faker.line()
    assert line.order == 'order-1'
    assert line.sku == 'TEST-LAMP'
    assert line.quantity == 10


def test_equal():
    line1 = faker.line()
    line2 = faker.line()
    assert line1 == line2


def test_hash():
    line1 = faker.line()
    line2 = faker.line()
    assert hash(line1) == hash(line2)
