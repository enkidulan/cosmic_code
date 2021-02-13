"""Cosmic Interfaces."""
import typing as t
from zope import interface
from datetime import datetime


class IProduct(interface.Interface):
    """A model of a physical object that may be sold to a customer.

    For example:
    * red chair
    * tasteless lamp
    """

    sku: str = interface.Attribute("""
        Stock-keeping unit, a human-friendly product identifier.

        For example: 'RED-CHAIR' or 'TASTELESS-LAMP'.""")



class ILine(interface.Interface):
    """Part of a :class:`IOrder` that specifies `quantity` for :class:`IProduct`."""

    order: str = interface.Attribute("ID of a :class:`IOrder`.")
    sku: str = interface.Attribute("SKU of a :class:`IProduct`.")
    quantity: int = interface.Attribute("Number of items.")


class IOrder(interface.Interface):
    """An order model of items that customer wants to purchase.

    An order is identified by an order reference and comprises multiple order lines.
    """

    reference: str = interface.Attribute("ID of an :class:`IOrder`.")
    lines: t.List[ILine] = interface.Attribute("A set of :class:`ILines`.")


class IBatch(interface.Interface):
    """A set avalivable :class:`IProduct`s that can be allocated to :class:`IOrder`s.

    The purchasing department orders small batches of stock. A batch of stock has a unique ID
    called a reference, a SKU, and a quantity. We need to allocate order lines to batches.
    When we’ve allocated an order line to a batch, we will send stock from that specific batch
    to the customer’s delivery address.
    """
    reference: str = interface.Attribute("ID of a :class:`IBatch`.")
    sku: str = interface.Attribute("SKU of a :class:`IProduct`.")
    quantity: int = interface.Attribute("Avalivable quantity of :class:`IProduct`s. in this :class:`IBatch`.")
    eta: t.Optional[datetime] = interface.Attribute("""XXXXX""")
    allocations: t.Set[ILine] = interface.Attribute(":class:`ILines`s that have been allocated to this :class:`IBatch`.")
    purchased_quantity: int = interface.Attribute("Numbers of :class:`IProduct`s purchased from this :class:`IBatch`.")

    def can_allocate(line: ILine) -> bool:
        """Check if class:`ILine` can be allocated to this :class:`IBatch`.

        We can allocate to a batch if requested quantity does not exits batch's available quantity. For example:
            * We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2 SMALL-TABLE.
            * The batch should have 18 SMALL-TABLE remaining.

        We can’t allocate to a batch if the available quantity is less than the quantity of the order line. For example:
            * We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION.
            * We should not be able to allocate the line to the batch.

        We can’t allocate the same line twice. For example:
            * We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE.
            * If we allocate the order line again to the same batch, the batch should still have an available quantity of 8.
        """

    def is_allocated(line: ILine) -> bool:
        """Check if class:`ILine` is allocated to this :class:`IBatch`."""

    def allocate(line: ILine) -> None:
        """Allocate class:`ILine` is allocated to this :class:`IBatch`.

        When we allocate class:`ILine` to a :class:`IBatch`, the available quantity is reduced by attribute:`ILine.quantity`."""

    def deallocate(line: ILine) -> None:
        """Deallocate class:`ILine` is allocated to this :class:`IBatch`.

        When we deallocate class:`ILine` from a :class:`IBatch`, the available quantity is increased by attribute:`ILine.quantity`."""


class IBatchRepository(interface.Interface):
    """An interface for batch repository."""

    def is_allocated(line: ILine) -> bool:
        pass

    def allocate(line: ILine) -> None:
        pass

    def deallocate(line: ILine) -> None:
        pass

    def add(batch: IBatch) -> None:
        pass
