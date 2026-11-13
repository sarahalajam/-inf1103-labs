from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base for all products (SRP: one product only).

    Product cannot be created directly - every product must be either a
    PhysicalProduct or a DigitalProduct, which implement get_fulfilment_info().

    Association: each Product keeps a reference to the Supplier that supplies
    it. The Supplier is created elsewhere and passed in - Product does not
    create or own it.

    Expectations every subclass must keep (Liskov Substitution Principle):
      * update_stock(quantity) adds/removes stock and never lets it go below 0.
      * display_information() prints the product and returns None.
      * get_fulfilment_info() always returns a str describing delivery.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier) -> None:
        self.__product_id: str = str(product_id)
        self.__name: str = str(name)
        self.__price: float = float(price)
        self.__stock: int = 0
        self.set_stock(stock_quantity)
        self.__supplier: Supplier = supplier

    # ---------- Getters (read-only access from outside) ----------
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # ---------- Controlled changes to state ----------
    def set_stock(self, stock: int) -> None:
        """Set stock to an exact value. Rejects negative numbers."""
        stock = int(stock)
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = stock

    def update_stock(self, quantity: int) -> None:
        """Add (positive) or remove (negative) stock. Stock can never go below 0."""
        quantity = int(quantity)
        if self.__stock + quantity < 0:
            raise ValueError(
                f"Not enough stock. Current stock is {self.__stock}, "
                f"cannot remove {abs(quantity)}."
            )
        self.__stock += quantity

    def display_information(self) -> None:
        """Display the common product details. Subclasses extend this via super()."""
        print(f"{self.__product_id:<8}{self.__name:<20}${self.__price:<11.2f}{self.__stock:<6}")
        print(f"{'':<8}Supplier: {self.__supplier.get_name()}")

    def display_supplier_information(self) -> None:
        """Ask the associated Supplier to describe itself."""
        self.__supplier.display_information()

    # ---------- Abstract behaviour (every subclass MUST implement) ----------
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how this product is delivered to the customer."""
        pass

    # ---------- Conversion helpers (used by file handling) ----------
    def to_dict(self) -> dict:
        """Return the common fields. Subclasses add their type and extra fields.

        Only the supplier's ID is saved - the Supplier is its own record, so it
        is saved separately rather than copied into every product.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }
