from product import Product


class Inventory:
    """Manages a collection of Product objects (SRP: the collection only)."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError(f"Product ID {product.get_product_id()} already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        """Return the Product with this ID, or None if not found."""
        for product in self.__products:
            if product.get_product_id().lower() == str(product_id).lower():
                return product
        return None

    def search_by_name(self, keyword):
        """Return a list of Products whose name contains the keyword."""
        keyword = keyword.lower()
        return [p for p in self.__products if keyword in p.get_name().lower()]

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)
        if product is None:
            raise ValueError(f"Product ID {product_id} not found.")
        product.update_stock(quantity)
        return product

    def get_products(self):
        """Return a copy of the list so outside code can't change the internal list."""
        return list(self.__products)

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return
        print(f"{'ID':<8}{'Name':<20}{'Price':<12}{'Stock':<6}")
        print("-" * 46)
        for product in self.__products:
            product.display_information()
