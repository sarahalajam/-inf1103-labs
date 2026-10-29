from product import Product
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


def add_product_menu(inventory):
    product_id = input("Enter product ID: ").strip()
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = input("Enter product name: ").strip()
    price = get_float("Enter price: ")
    stock = get_int("Enter stock quantity: ")
    inventory.add_product(Product(product_id, name, price, stock))
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
    print(f"{'ID':<8}{'Name':<20}{'Price':<12}{'Stock':<6}")
    print("-" * 46)
    for p in results:
        p.display_information()


def main():
    inventory = load_inventory()

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

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
            if input("Save before exiting? (y/n): ").strip().lower() == "y":
                save_inventory(inventory)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
