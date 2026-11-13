from product import Product


class Inventory:
    """Groups Product objects (aggregation - SRP: the collection only).

    The Inventory holds references to Products that were created elsewhere.
    It never creates or destroys them: removing a Product only removes the
    reference, so the same Product can be moved to another Inventory.

    The collection is typed as list[Product] (not PhysicalProduct or
    DigitalProduct) so any current or future Product subclass can be stored
    and used through the common Product abstraction.
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Add an existing Product object to the inventory."""
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.find_product(product.get_product_id()) is not None:
            raise ValueError(f"Product ID {product.get_product_id()} already exists.")
        self.__products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the matching Product reference and return it (it is not destroyed)."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID, or None if not found."""
        for product in self.__products:
            if product.get_product_id().lower() == str(product_id).lower():
                return product
        return None

    def search_by_name(self, keyword: str) -> list[Product]:
        """Return a list of Products whose name contains the keyword."""
        keyword = keyword.lower()
        return [p for p in self.__products if keyword in p.get_name().lower()]

    def update_stock(self, product_id: str, quantity: int) -> Product:
        product = self.find_product(product_id)
        if product is None:
            raise ValueError(f"Product ID {product_id} not found.")
        product.update_stock(quantity)   # same call for every Product subclass
        return product

    def clear(self) -> None:
        """Empty the inventory. Only the references go - the Products still exist."""
        self.__products.clear()

    def get_products(self) -> list[Product]:
        """Return a copy of the list so outside code can't change the internal list."""
        return list(self.__products)

    def display_all_products(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return
        print(f"{'ID':<8}{'Name':<20}{'Price':<12}{'Stock':<6}")
        print("-" * 46)
        for product in self.__products:
            product.display_information()   # each object picks its own version
