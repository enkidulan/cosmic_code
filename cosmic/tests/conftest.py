import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from cosmic.storage.memory import BatchRepository
from cosmic.storage.sqla import BatchRepository, metadata, setup_mappers

from cosmic.tests import faker


@pytest.fixture(scope='session')
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    yield engine


@pytest.fixture(scope='session')
def session(in_memory_db):
    setup_mappers()
    metadata.create_all(in_memory_db)
    session = sessionmaker(bind=in_memory_db)()
    session.commit()
    yield session


@pytest.fixture(scope='function')
def batch_repository(session):
    repository = BatchRepository(session)
    batches = [
        faker.batch(quantity=5, eta=datetime(1999, 1, 1)),
        faker.batch(quantity=4, eta=None),
        faker.batch(quantity=10, eta=datetime(2000, 1, 1)),
    ]
    for batch_obj in batches:
        repository.add_batch(batch_obj)
    yield repository
    session.rollback()
