from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from file_handler import load_inventory, save_inventory


def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_int(prompt, allow_negative=False):
    while True:
        try:
            value = int(input(prompt))
            if value < 0 and not allow_negative:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def print_header():
    print(f"{'ID':<8}{'Name':<20}{'Price':<12}{'Stock':<6}")
    print("-" * 46)


def add_product_menu(inventory):
    print("Product type:")
    print("1. Physical product")
    print("2. Digital product")
    product_type = input("Enter product type (1-2): ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ").strip()
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = input("Enter product name: ").strip()
    price = get_float("Enter price: ")
    stock = get_int("Enter stock quantity: ")

    if product_type == "1":
        weight = get_float("Enter weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_float("Enter download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print(f"Product '{name}' added.")


def update_stock_menu(inventory):
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)
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


def search_product_menu(inventory):
    keyword = input("Enter product ID or name: ").strip()
    product = inventory.search_product(keyword)
    results = [product] if product else inventory.search_by_name(keyword)
    if not results:
        print("No matching products found.")
        return
    print_header()
    for p in results:
        p.display_information()


def fulfilment_menu(inventory):
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print(product.get_fulfilment_info())
    # Only products that signed the CanBeShipped contract have a shipping cost.
    if isinstance(product, CanBeShipped):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")
    else:
        print("No shipping required.")


def main():
    inventory = load_inventory()

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. View fulfilment / shipping info")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            fulfilment_menu(inventory)
        elif choice == "7":
            if input("Save before exiting? (y/n): ").strip().lower() == "y":
                save_inventory(inventory)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
