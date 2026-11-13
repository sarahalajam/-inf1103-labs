from order_line import OrderLine
from product import Product


class Order:
    """A customer order made up of OrderLines (composition - the 'whole').

    The Order creates its own OrderLine objects inside add_order_line(); no
    OrderLine is ever passed in from outside. Each line belongs to exactly
    one Order, so when a line is removed or the Order goes away, its lines go
    with it. The Products the lines refer to are NOT affected.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = str(order_id)
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this product and keep it in this Order."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Delete the line for this product. Returns True if a line was removed.

        The line is discarded rather than returned, so it cannot be handed to
        another Order.
        """
        for line in self.__order_lines:
            if line.get_product().get_product_id().lower() == str(product_id).lower():
                self.__order_lines.remove(line)
                return True
        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        """Read-only view of the lines - outside code cannot add or remove them."""
        return tuple(self.__order_lines)

    def calculate_total(self) -> float:
        """Total = the sum of each OrderLine's own subtotal."""
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no order lines)")
            return
        for line in self.__order_lines:
            line.display_information()
        print(f"{'TOTAL':<52}${self.calculate_total():.2f}")
