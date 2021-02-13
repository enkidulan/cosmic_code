import pytest
from cosmic import models
from cosmic.tests import faker


def test_allocate_fist_to_warehause(batch_repository):
    line = faker.line(quantity=1)
    faker.allocation(batch_repository, lines={line})
    assert line in batch_repository.batches[1].allocations


def test_allocate_fist_to_erliest_eta(batch_repository):
    line = faker.line(quantity=5)
    faker.allocation(batch_repository, lines={line})
    assert line in batch_repository.batches[0].allocations


def test_allocate_last_to_latest_eta(batch_repository):
    line = faker.line(quantity=10)
    faker.allocation(batch_repository, lines={line})
    assert line in batch_repository.batches[2].allocations


def test_allocate(batch_repository):
    lines = {
        models.Line(order="order-1", sku="TEST-LAMP", quantity=5),
        models.Line(order="order-1", sku="TEST-LAMP", quantity=3),
        models.Line(order="order-1", sku="TEST-LAMP", quantity=2),
    }
    faker.allocation(batch_repository, lines=lines)
    assert lines == {j for i in batch_repository.batches for j in i.allocations}


def test_allocation_atomicity_fail(batch_repository):
    from cosmic.exceptions import OutOfStockException

    lines = {
        faker.line(quantity=10),
        faker.line(quantity=4),
        faker.line(quantity=6),
    }
    with pytest.raises(OutOfStockException):
        faker.allocation(batch_repository, lines=lines)
    assert batch_repository.batches[0].quantity == 5
    assert not batch_repository.batches[0].allocations
    assert batch_repository.batches[1].quantity == 4
    assert not batch_repository.batches[1].allocations
    assert batch_repository.batches[2].quantity == 10
    assert not batch_repository.batches[2].allocations


def test_allocate_already_allocated(batch_repository):
    line = faker.line(quantity=3)
    batches, _, _ = faker.allocation(batch_repository, lines={line})
    assert line in batches[1].allocations
    faker.allocation(batch_repository, batches=[], lines={line})
    assert line not in batches[0].allocations
    assert line in batches[1].allocations
    assert line not in batches[2].allocations
    assert batches[1].quantity == 1
