from product import Product


class OrderLine:
    """One product and quantity inside an Order (the 'part' in a composition).

    OrderLines are only created by Order.add_order_line() - they are never
    created on their own or moved to another Order.

    OrderLine -> Product is an association: the line refers to a Product but
    does not own it. The Product carries on existing (e.g. in an Inventory)
    whatever happens to the line.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_product_id():<8}{self.__product.get_name():<20}"
              f"{self.__quantity:>4} x ${self.__product.get_price():<10.2f}"
              f"= ${self.calculate_subtotal():.2f}")
