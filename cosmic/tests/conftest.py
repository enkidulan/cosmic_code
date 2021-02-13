import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from cosmic.storage import sqla
from cosmic.storage import memory


from cosmic.tests import faker


@pytest.fixture(scope="session")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    yield engine


@pytest.fixture(scope="session")
def session(in_memory_db):
    sqla.setup_mappers()
    sqla.metadata.create_all(in_memory_db)
    session = sessionmaker(bind=in_memory_db)()
    session.commit()
    yield session


@pytest.fixture(scope="function")
def batch_repository_in_memory():
    return memory.BatchRepository()


@pytest.fixture(scope="function")
def batch_repository_sqla(session):
    yield sqla.BatchRepository(session)
    session.rollback()


@pytest.fixture(scope="function", params=["sqla", "mem"])
def batch_repository(batch_repository_sqla, batch_repository_in_memory, request):
    testing_backend = request.config.getoption("--testing-backend")
    if testing_backend and request.param == testing_backend:
        pytest.skip("Backend is not selected")
    repos = {
        "sqla": batch_repository_sqla,
        "mem": batch_repository_in_memory,
    }
    repository = repos[request.param]
    batches = [
        faker.batch(quantity=5, eta=datetime(1999, 1, 1)),
        faker.batch(quantity=4, eta=None),
        faker.batch(quantity=10, eta=datetime(2000, 1, 1)),
    ]
    for batch_obj in batches:
        repository.add_batch(batch_obj)
    yield repository


def pytest_addoption(parser):
    parser.addoption(
        "--testing-backend", action="store", default=None, help="backend for testsing"
    )
