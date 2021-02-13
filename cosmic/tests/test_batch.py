from datetime import datetime
import pytest

# import domain
from cosmic.tests import faker


def test_batch():
    batch = faker.batch()
    assert batch.reference == "reference-1"
    assert batch.sku == "TEST-LAMP"
    assert batch.quantity == 20
    assert batch.eta == datetime(1999, 1, 1)
    batch = faker.batch(eta=None)
    assert batch.eta is None


def test_batch_comparison():
    batch_0 = faker.batch()
    batch_1 = faker.batch()
    batch_2 = faker.batch(eta=datetime(1999, 1, 2))
    batch_3 = faker.batch(eta=None)
    batch_4 = faker.batch(quantity=30, eta=None)
    assert batch_3 < batch_1
    assert batch_3 < batch_2
    assert batch_2 > batch_1
    assert batch_0 == batch_1
    assert batch_3 == batch_4


def test_batch_identity():
    batch = faker.batch()
    # assert str(batch) == "Batch(reference='reference-1', sku='TEST-LAMP', quantity=20, eta=datetime.datetime(1999, 1, 1, 0, 0), purchased_quantity=20)"
    # assert repr(batch) == "Batch(reference='reference-1', sku='TEST-LAMP', quantity=20, eta=datetime.datetime(1999, 1, 1, 0, 0), purchased_quantity=20)"
    assert hash(batch) == hash(("reference-1",))
    batch_2 = faker.batch(eta=None)
    assert batch == batch_2
    assert batch is not batch_2


def test_batch_validation():
    with pytest.raises(Exception):
        faker.batch(reference=1)
    with pytest.raises(Exception):
        faker.batch(sku=1)
    with pytest.raises(Exception):
        faker.batch(quantity=0)
    with pytest.raises(Exception):
        faker.batch(quantity=-1)
    with pytest.raises(Exception):
        faker.batch(eta=1)


def test_allocate():
    batch = faker.batch()
    line = faker.line()
    batch.allocate(line)
    assert batch.quantity == 10


def test_allocate_same_line_twice():
    batch = faker.batch()
    line = faker.line()
    batch.allocate(line)
    batch.allocate(line)
    assert batch.quantity == 10


def test_allocate_wrong_sku():
    batch = faker.batch()
    line = faker.line(sku="qwerty")
    with pytest.raises(Exception):
        batch.allocate(line)


def test_allocate_exits_quantity():
    batch = faker.batch()
    line = faker.line(quantity=21)
    with pytest.raises(Exception):
        batch.allocate(line)


def test_deallocate():
    batch = faker.batch()
    line = faker.line()
    batch.allocate(line)
    assert line in batch.allocations
    assert batch.quantity == 10
    batch.deallocate(line)
    assert line not in batch.allocations
    assert batch.quantity == 20


def test_deallocate_not_allocated():
    batch = faker.batch()
    line_1 = faker.line()
    batch.allocate(line_1)
    line_2 = faker.line(order="2")
    with pytest.raises(Exception):
        batch.deallocate(line_2)
    assert line_1 in batch.allocations
    assert batch.quantity == 10
