import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

# Maps the "type" identifier saved in JSON to the subclass that rebuilds it.
PRODUCT_TYPES = {
    PhysicalProduct.TYPE: PhysicalProduct,
    DigitalProduct.TYPE: DigitalProduct,
}


def product_from_dict(data):
    """Create the correct Product subclass using the saved type identifier."""
    product_type = data.get("type")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type '{product_type}' for product {data.get('id')}")
    return PRODUCT_TYPES[product_type].from_dict(data)


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
            inventory.add_product(product_from_dict(item))
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
