import typing as t
import uuid
from zope import interface
from cosmic.exceptions import OutOfStockException
import sqlalchemy as sa
import sqlalchemy.orm
from cosmic import interfaces
from cosmic import models


__all__ = ["BatchRepository"]

engine = sa.create_engine("sqlite:///:memory:")


def generate_uuid():
    return str(uuid.uuid4())


metadata = sa.MetaData()

product = sa.Table(
    "products",
    metadata,
    sa.Column("uuid", sa.String, primary_key=True, default=generate_uuid),
    sa.Column("sku", sa.String, unique=True),
)


line = sa.Table(
    "lines",
    metadata,
    sa.Column("uuid", sa.String, primary_key=True, default=generate_uuid),
    sa.Column("order", sa.String),  # ref
    sa.Column("order_id", sa.ForeignKey("orders.uuid")),  # ref
    sa.Column("sku", sa.String),
    sa.Column("quantity", sa.String),
)


order = sa.Table(
    "orders",
    metadata,
    sa.Column("uuid", sa.String, primary_key=True, default=generate_uuid),
    sa.Column("reference", sa.String),
    # sa.Column("lines", sa.list),  # ref
)


batch = sa.Table(
    "batches",
    metadata,
    sa.Column("uuid", sa.String, primary_key=True, default=generate_uuid),
    sa.Column("reference", sa.String),
    sa.Column("sku", sa.String),
    sa.Column("quantity", sa.Integer),
    sa.Column("eta", sa.DateTime),
    # sa.Column("allocations", sa.Integer),  # ref
    sa.Column("purchased_quantity", sa.Integer),
)


allocations = sa.Table(
    "allocations",
    metadata,
    sa.Column("uuid", sa.String, primary_key=True, default=generate_uuid),
    sa.Column("line_id", sa.ForeignKey("lines.uuid")),
    sa.Column("batch_id", sa.ForeignKey("batches.uuid")),
)


def setup_mappers():
    product_mapper = sa.orm.mapper(models.Product, product)
    lines_mapper = sa.orm.mapper(models.Line, line)
    order_mapper = sa.orm.mapper(
        models.Order,
        order,
        properties={
            "lines": sa.orm.relationship(
                lines_mapper,
                collection_class=set,
            )
        },
    )
    batch_mapper = sa.orm.mapper(
        models.Batch,
        batch,
        properties={
            "allocations": sa.orm.relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )


@interface.implementer(interfaces.IBatchRepository)
class BatchRepository:
    def __init__(self, session=None):
        self.session = session

    def add_batch(self, batch):
        self.session.add(batch)

    @property
    def batches(self) -> t.List[interfaces.IBatch]:
        return self.session.query(models.Batch).all()

    def is_allocated(self, line: interfaces.ILine) -> bool:
        for batch in self.batches:
            if batch.is_allocated(line):
                return True
        return False

    def allocate(self, line: interfaces.ILine) -> None:
        if self.is_allocated(line):
            return
        batches = [
            i for i in self.batches if i.sku == line.sku and i.quantity >= line.quantity
        ]
        if not batches:
            raise OutOfStockException(f"cannot allocate f{line}")
        batches.sort()
        batches[0].allocate(line)

    def deallocate(self, line: interfaces.ILine) -> None:
        for batch in self.batches:
            if batch.is_allocated(line):
                batch.deallocate(line)
