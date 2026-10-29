import json
import os

from product import Product
from inventory import Inventory


def load_inventory(filename="inventory.json"):
    """Load products from a JSON file into a new Inventory object."""
    inventory = Inventory()
    if not os.path.exists(filename):
        print(f"No {filename} found. Starting with an empty inventory.")
        return inventory

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        for item in data:
            inventory.add_product(Product.from_dict(item))
        print(f"Loaded {len(data)} product(s) from {filename}.")
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Error reading {filename}: {error}. Starting with an empty inventory.")
        inventory = Inventory()
    return inventory


def save_inventory(inventory, filename="inventory.json"):
    """Save all products in the Inventory to a JSON file."""
    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved to {filename}.")
