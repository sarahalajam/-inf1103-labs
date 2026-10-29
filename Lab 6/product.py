class Product:
    """Represents and manages a single product (SRP: one product only)."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = 0
        self.set_stock(stock)

    # ---------- Getters (read-only access from outside) ----------
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---------- Controlled changes to state ----------
    def set_stock(self, stock):
        """Set stock to an exact value. Rejects negative numbers."""
        stock = int(stock)
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = stock

    def update_stock(self, quantity):
        """Add (positive) or remove (negative) stock. Stock can never go below 0."""
        quantity = int(quantity)
        if self.__stock + quantity < 0:
            raise ValueError(
                f"Not enough stock. Current stock is {self.__stock}, "
                f"cannot remove {abs(quantity)}."
            )
        self.__stock += quantity

    def display_information(self):
        print(f"{self.__product_id:<8}{self.__name:<20}${self.__price:<11.2f}{self.__stock:<6}")

    # ---------- Conversion helpers (used by file handling) ----------
    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @staticmethod
    def from_dict(data):
        return Product(data["id"], data["name"], data["price"], data["stock"])
