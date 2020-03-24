import typing as t
from zope import interface
from datetime import datetime


class IProduct(interface.Interface):
    sku: str


class ILine(interface.Interface):
    order: str = interface.Attribute("""XXXXX""")
    sku: str = interface.Attribute("""XXXXX""")
    quantity: int = interface.Attribute("""XXXXX""")


class IOrder(interface.Interface):
    reference: str
    lines: t.List[ILine] = interface.Attribute("""XXXXX""")


class IBatch(interface.Interface):
    reference: str = interface.Attribute("""XXXXX""")
    sku: str = interface.Attribute("""XXXXX""")
    quantity: int = interface.Attribute("""XXXXX""")
    eta: t.Optional[datetime] = interface.Attribute("""XXXXX""")
    allocations: t.Set[ILine] = interface.Attribute("""XXXXX""")
    purchased_quantity: int = interface.Attribute("""XXXXX""")

    def can_allocate(line: ILine) -> bool:
        pass

    def is_allocated(line: ILine) -> bool:
        pass

    def allocate(line: ILine) -> None:
        pass

    def deallocate(line: ILine) -> None:
        pass


class IBatchRepository(interface.Interface):
    """An interface for batch repository"""

    def is_allocated(line: ILine) -> bool:
        pass

    def allocate(line: ILine) -> None:
        pass

    def deallocate(line: ILine) -> None:
        pass
