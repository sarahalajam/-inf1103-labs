from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.

    Single class inheritance: PhysicalProduct is-a Product.
    Interface realisation: PhysicalProduct CanBeShipped.
    """

    TYPE: str = "physical"
    BASE_SHIPPING_FEE: float = 5.00   # flat fee per shipment
    RATE_PER_KG: float = 2.00         # extra cost per kilogram

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__weight: float = 0.0
        self.set_weight(weight)

    def get_weight(self) -> float:
        return self.__weight

    def set_weight(self, weight: float) -> None:
        """Set weight in kilograms. Rejects negative numbers."""
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    def display_information(self) -> None:
        super().display_information()   # parent prints the common details
        print(f"{'':<8}Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Shipping = flat base fee + a charge per kilogram."""
        return round(self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight, 2)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    @staticmethod
    def from_dict(data: dict, supplier: Supplier) -> "PhysicalProduct":
        return PhysicalProduct(
            data["id"], data["name"], data["price"], data["stock"], supplier, data["weight"]
        )
