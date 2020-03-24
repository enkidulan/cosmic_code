import pytest
import domain
from tests import faker


def test_allocate_fist_to_warehause():
    line = faker.line(quantity=1)
    order = faker.order(lines=[line])
    batch_repository = faker.batch_repository()
    domain.allocate_order(batch_repository, order)
    assert line in batch_repository.batches[1].allocations


def test_allocate_fist_to_erliest_eta():
    line = faker.line(quantity=5)
    order = faker.order(lines=[line])
    batch_repository = faker.batch_repository()
    batch_repository.batches = batch_repository.batches[::-1]
    domain.allocate_order(batch_repository, order)
    assert line in batch_repository.batches[2].allocations


def test_allocate_last_to_latest_eta():
    line = faker.line(quantity=10)
    order = faker.order(lines=[line])
    batch_repository = faker.batch_repository()
    domain.allocate_order(batch_repository, order)
    assert line in batch_repository.batches[2].allocations


def test_allocate():
    order = faker.order()
    batch_repository = faker.batch_repository()
    domain.allocate_order(batch_repository, order)
    assert order.lines[0] in batch_repository.batches[0].allocations
    assert order.lines[1] in batch_repository.batches[1].allocations
    assert order.lines[2] in batch_repository.batches[2].allocations


def test_allocation_atomicity_fail():
    from exceptions import OutOfStockException
    order = faker.order(
        lines=[
            faker.line(quantity=10),
            faker.line(quantity=4),
            faker.line(quantity=6),
        ]
    )
    batch_repository = faker.batch_repository()
    with pytest.raises(OutOfStockException):
        domain.allocate_order(batch_repository, order)
    assert batch_repository.batches[0].quantity == 5
    assert not batch_repository.batches[0].allocations
    assert batch_repository.batches[1].quantity == 4
    assert not batch_repository.batches[1].allocations
    assert batch_repository.batches[2].quantity == 10
    assert not batch_repository.batches[2].allocations


def test_allocate_already_allocated():
    line = faker.line(quantity=3)
    order = faker.order(lines=[line])
    batch_repository = faker.batch_repository()
    batch_repository.batches[2].allocate(line)
    assert line in batch_repository.batches[2].allocations
    domain.allocate_order(batch_repository, order)
    assert line not in batch_repository.batches[0].allocations
    assert line not in batch_repository.batches[1].allocations
    assert line in batch_repository.batches[2].allocations
