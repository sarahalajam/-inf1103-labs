"""Walks through Lab 8 sections 2-7 so each relationship can be seen in the output.

Run with: python demo.py
"""
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print(f"\n{'=' * 64}\n{title}\n{'=' * 64}")


# ---------------------------------------------------------------------------
# Section 2 - Association: Supplier and Product
# ---------------------------------------------------------------------------
def demo_association() -> None:
    heading("2. ASSOCIATION - Supplier and Product")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.1)
    antivirus = DigitalProduct("D010", "Antivirus", 49.90, 300, supplier, 350)

    print("Supplier info through each Product:")
    laptop.display_supplier_information()
    antivirus.display_supplier_information()

    print("\nSeparate objects?")
    print(f"  laptop is supplier?                   {laptop is supplier}")
    print(f"  laptop.get_supplier() is supplier?    {laptop.get_supplier() is supplier}")
    print(f"  both products share ONE Supplier?     "
          f"{laptop.get_supplier() is antivirus.get_supplier()}")

    print("\nPredict first: after 'del supplier', can each Product still show its supplier?")
    del supplier
    try:
        supplier  # noqa: F821 - deliberately checking the name is gone
    except NameError as error:
        print(f"  The variable is gone -> NameError: {error}")
    print("  ...but the Products still hold their own reference to the Supplier object:")
    laptop.display_supplier_information()
    antivirus.display_supplier_information()

    print("\nA Supplier can also exist with no Products at all:")
    new_supplier = Supplier("S099", "Brand New Supplier", "hello@new.example.com")
    new_supplier.display_information()


# ---------------------------------------------------------------------------
# Section 3 - Aggregation: Inventory and Product
# ---------------------------------------------------------------------------
def demo_aggregation() -> None:
    heading("3. AGGREGATION - Inventory and Product")
    supplier = Supplier("S002", "MusicWorld Supplies", "orders@musicworld.example.com")

    print("Step 1: Product created BEFORE any Inventory exists")
    guitar = PhysicalProduct("P003", "Guitar", 350.00, 5, supplier, 3.5)
    print(f"  Created {guitar.get_name()} (id(guitar) = {id(guitar)})")

    inventory_a = Inventory()
    inventory_b = Inventory()

    print("\nStep 2: Add the Product to Inventory A")
    inventory_a.add_product(guitar)
    print(f"  In A? {inventory_a.find_product('P003') is guitar}")

    print("\nPredict first: will the Guitar still work after removing it from Inventory A?")
    print("Step 3: Remove from Inventory A")
    removed = inventory_a.remove_product("P003")
    print(f"  In A? {inventory_a.find_product('P003') is not None}")
    print(f"  Removed object is the same Guitar? {removed is guitar}")
    print("  Guitar still works:")
    guitar.update_stock(-1)
    print(f"    update_stock(-1) -> stock is now {guitar.get_stock()}")
    print(f"    {guitar.get_fulfilment_info()}")

    print("\nStep 4: Add the SAME Product object to Inventory B")
    inventory_b.add_product(guitar)
    print(f"  In B? {inventory_b.find_product('P003') is guitar}  "
          f"(same id: {id(inventory_b.find_product('P003')) == id(guitar)})")

    print("\nStep 5: Empty Inventory B - the Product is not destroyed")
    inventory_b.clear()
    inventory_b.display_all_products()
    print(f"  Guitar still exists: {guitar.get_name()}, stock {guitar.get_stock()}")


# ---------------------------------------------------------------------------
# Section 4 - Composition: Order and OrderLine
# ---------------------------------------------------------------------------
def demo_composition() -> None:
    heading("4. COMPOSITION - Order and OrderLine")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.1)
    mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1)
    office = DigitalProduct("D003", "Office Suite", 99.00, 500, supplier, 2400)

    print("Order O001 - the Order creates each OrderLine via add_order_line()")
    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(mouse, 2)
    order_1.add_order_line(office, 1)
    order_1.display_order()

    print("\nPredict first: same Product in two Orders - how many OrderLines / Products?")
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 3)
    order_2.display_order()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"\n  OrderLine in O001 is OrderLine in O002?  {line_1 is line_2}  "
          f"(id {id(line_1)} vs {id(line_2)})")
    print(f"  Product in O001 is Product in O002?      "
          f"{line_1.get_product() is line_2.get_product()}  "
          f"(id {id(line_1.get_product())} vs {id(line_2.get_product())})")
    print("  -> 2 OrderLine objects, but only 1 Laptop Product object.")

    print("\nRemove the Mouse line through the Order's own method:")
    order_1.remove_order_line("P002")
    order_1.display_order()

    print("\nget_order_lines() is read-only - lines can't be added or moved from outside:")
    try:
        order_1.get_order_lines().append(line_2)  # type: ignore[attr-defined]
    except AttributeError as error:
        print(f"  AttributeError: {error}")

    print("\nDelete the whole Order - its lines go with it, the Products do not:")
    del order_1
    print(f"  Laptop still exists: {laptop.get_name()}, stock {laptop.get_stock()}")


# ---------------------------------------------------------------------------
# Section 6 - Liskov Substitution Principle
# ---------------------------------------------------------------------------
def show_product_details(product: Product) -> None:
    """Works with ANY Product - it only uses behaviour every Product supports."""
    product.display_information()
    print(product.get_fulfilment_info())


class BrokenDigitalProduct(DigitalProduct):
    """The teammate's proposal from 6.3 - kept here ONLY to show why it breaks LSP."""

    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


def demo_lsp() -> None:
    heading("6. LISKOV SUBSTITUTION PRINCIPLE")
    music_world = Supplier("S002", "MusicWorld Supplies", "orders@musicworld.example.com")
    supplier = Supplier("S003", "SoftHouse Digital", "licensing@softhouse.example.com")
    guitar = PhysicalProduct("P003", "Guitar", 350.00, 5, music_world, 3.5)
    photo_editor = DigitalProduct("D002", "Photo Editor", 59.00, 250, supplier, 850)

    print("6.2 show_product_details(product: Product) with both subclasses:")
    print_header()
    show_product_details(guitar)
    show_product_details(photo_editor)

    print("\n6.3 Expectation from Product: update_stock(n) changes stock by n, never below 0")
    inventory = Inventory()
    inventory.add_product(guitar)
    inventory.add_product(photo_editor)
    for product_id, quantity in (("P003", 2), ("D002", -50)):
        product = inventory.update_stock(product_id, quantity)
        print(f"  Inventory.update_stock('{product_id}', {quantity:+}) -> "
              f"{product.get_name()} stock = {product.get_stock()}")
    for product_id in ("P003", "D002"):
        try:
            inventory.update_stock(product_id, -9999)
        except ValueError as error:
            print(f"  Removing too much from {product_id} -> ValueError: {error}")

    print("\nDiagnose: the teammate's DigitalProduct that raises NotImplementedError")
    broken = BrokenDigitalProduct("D999", "Broken eBook", 9.99, 10, supplier, 5)
    inventory.add_product(broken)
    try:
        inventory.update_stock("D999", 5)
    except NotImplementedError as error:
        print(f"  Inventory.update_stock('D999', 5) -> NotImplementedError: {error}")
        print("  Inventory only knows it has a Product, so this crash is an LSP violation.")


# ---------------------------------------------------------------------------
# Section 7 - Polymorphism
# ---------------------------------------------------------------------------
def demo_polymorphism() -> None:
    heading("7. POLYMORPHISM - one loop, no isinstance()")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.1))
    inventory.add_product(DigitalProduct("D001", "Operating System", 139.99, 100, supplier, 5200))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1))

    print("Predict first: what will each get_fulfilment_info() print?\n")
    print_header()
    for product in inventory.get_products():
        product.display_information()
        print(f"{'':<8}-> {product.get_fulfilment_info()}")


def print_header() -> None:
    print(f"{'ID':<8}{'Name':<20}{'Price':<12}{'Stock':<6}")
    print("-" * 46)


def main() -> None:
    demo_association()
    demo_aggregation()
    demo_composition()
    demo_lsp()
    demo_polymorphism()


if __name__ == "__main__":
    main()
