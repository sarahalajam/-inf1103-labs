import json
import os

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory

# Maps the "type" identifier saved in JSON to the subclass that rebuilds it.
PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    PhysicalProduct.TYPE: PhysicalProduct,
    DigitalProduct.TYPE: DigitalProduct,
}


def product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    """Create the correct Product subclass and link it to its existing Supplier."""
    product_type = data.get("type")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type '{product_type}' for product {data.get('id')}")
    supplier_id = data.get("supplier_id")
    if supplier_id not in suppliers:
        raise ValueError(f"Unknown supplier '{supplier_id}' for product {data.get('id')}")
    return PRODUCT_TYPES[product_type].from_dict(data, suppliers[supplier_id])


def load_inventory(filename: str = "inventory.json") -> tuple[Inventory, dict[str, Supplier]]:
    """Load suppliers and products from a JSON file.

    Suppliers are loaded first, then each product is given a reference to
    the (shared) Supplier object with the matching ID.
    """
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    if not os.path.exists(filename):
        print(f"No {filename} found. Starting with an empty inventory.")
        return inventory, suppliers

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        for item in data["suppliers"]:
            supplier = Supplier.from_dict(item)
            suppliers[supplier.get_supplier_id()] = supplier
        for item in data["products"]:
            inventory.add_product(product_from_dict(item, suppliers))
        print(f"Loaded {len(suppliers)} supplier(s) and "
              f"{len(data['products'])} product(s) from {filename}.")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Error reading {filename}: {error}. Starting with an empty inventory.")
        inventory, suppliers = Inventory(), {}
    return inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier],
                   filename: str = "inventory.json") -> None:
    """Save all suppliers and products to a JSON file."""
    data = {
        "suppliers": [supplier.to_dict() for supplier in suppliers.values()],
        "products": [product.to_dict() for product in inventory.get_products()],
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved to {filename}.")
