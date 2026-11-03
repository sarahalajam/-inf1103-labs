from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style ABC: a contract for anything that can be shipped.

    It holds no attributes or implementation details - any class that
    'signs the contract' must provide its own calculate_shipping_cost().
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the cost of shipping this item."""
        pass
