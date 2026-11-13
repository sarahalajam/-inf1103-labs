from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from supplier import Supplier
from inventory import Inventory
from order import Order
from file_handler import load_inventory, save_inventory


def get_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_int(prompt: str, allow_negative: bool = False) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0 and not allow_negative:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def print_header() -> None:
    print(f"{'ID':<8}{'Name':<20}{'Price':<12}{'Stock':<6}")
    print("-" * 46)


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    """Pick an existing Supplier, or create a new one, to associate with a product."""
    print("Suppliers:")
    for supplier in suppliers.values():
        supplier.display_information()
    supplier_id = input("Enter supplier ID (or a new ID to create a supplier): ").strip()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        return suppliers[supplier_id]
    name = input("New supplier name: ").strip()
    email = input("New supplier contact email: ").strip()
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    print(f"Supplier '{name}' created.")
    return supplier


def add_product_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("Product type:")
    print("1. Physical product")
    print("2. Digital product")
    product_type = input("Enter product type (1-2): ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ").strip()
    if inventory.find_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = input("Enter product name: ").strip()
    price = get_float("Enter price: ")
    stock = get_int("Enter stock quantity: ")
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    product: Product
    if product_type == "1":
        weight = get_float("Enter weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_float("Enter download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    print(f"Product '{name}' added.")


def remove_product_menu(inventory: Inventory) -> None:
    product_id = input("Enter product ID to remove: ").strip()
    product = inventory.remove_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        print(f"'{product.get_name()}' removed from the inventory.")


def update_stock_menu(inventory: Inventory) -> None:
    product_id = input("Enter product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print(f"Current stock for {product.get_name()}: {product.get_stock()}")
    quantity = get_int("Enter quantity to add (use negative to remove): ", allow_negative=True)
    try:
        inventory.update_stock(product_id, quantity)
        print(f"Stock updated. New stock: {product.get_stock()}")
    except ValueError as error:
        print(error)


def search_product_menu(inventory: Inventory) -> None:
    keyword = input("Enter product ID or name: ").strip()
    product = inventory.find_product(keyword)
    results = [product] if product else inventory.search_by_name(keyword)
    if not results:
        print("No matching products found.")
        return
    print_header()
    for p in results:
        p.display_information()


def fulfilment_menu(inventory: Inventory) -> None:
    product_id = input("Enter product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print(product.get_fulfilment_info())
    product.display_supplier_information()
    # Shipping is an optional extra capability (CanBeShipped interface), not part
    # of the Product contract, so asking whether it is supported is fine here.
    if isinstance(product, CanBeShipped):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")
    else:
        print("No shipping required.")


def create_order_menu(inventory: Inventory, order_count: int) -> None:
    """Build an Order. The Order itself creates each OrderLine."""
    order = Order(f"O{order_count:03d}")
    print(f"Creating order {order.get_order_id()}. Leave product ID blank to finish.")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_int("Quantity: ")
        try:
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(error)
    order.display_order()


def main() -> None:
    inventory, suppliers = load_inventory()
    order_count = 0

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Remove a product")
        print("4. Update stock")
        print("5. Search for a product")
        print("6. View fulfilment / supplier / shipping info")
        print("7. Create an order")
        print("8. Save inventory")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product_menu(inventory, suppliers)
        elif choice == "3":
            remove_product_menu(inventory)
        elif choice == "4":
            update_stock_menu(inventory)
        elif choice == "5":
            search_product_menu(inventory)
        elif choice == "6":
            fulfilment_menu(inventory)
        elif choice == "7":
            order_count += 1
            create_order_menu(inventory, order_count)
        elif choice == "8":
            save_inventory(inventory, suppliers)
        elif choice == "9":
            if input("Save before exiting? (y/n): ").strip().lower() == "y":
                save_inventory(inventory, suppliers)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-9.")


if __name__ == "__main__":
    main()
