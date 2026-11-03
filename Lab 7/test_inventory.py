"""Section 7 checklist as unit tests. Run with: python -m unittest -v"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handler import load_inventory, save_inventory


def captured_display(product):
    """Return what display_information() prints."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    return buffer.getvalue()


class TestPhysicalProduct(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5)

    def test_stores_weight(self):
        self.assertEqual(self.guitar.get_weight(), 3.5)

    def test_display_shows_parent_and_child_info(self):
        output = captured_display(self.guitar)
        self.assertIn("P100", output)      # from Product
        self.assertIn("Guitar", output)    # from Product
        self.assertIn("3.50 kg", output)   # from PhysicalProduct

    def test_fulfilment_info(self):
        self.assertIn("physical shipping", self.guitar.get_fulfilment_info())

    def test_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P1", "Light", 1.0, 1, 1)
        heavy = PhysicalProduct("P2", "Heavy", 1.0, 1, 10)
        self.assertEqual(light.calculate_shipping_cost(), 7.00)
        self.assertEqual(heavy.calculate_shipping_cost(), 25.00)

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P1", "Bad", 1.0, 1, -2)


class TestDigitalProduct(unittest.TestCase):
    def setUp(self):
        self.os_product = DigitalProduct("D100", "Operating System", 139.99, 100, 5200)

    def test_stores_download_size(self):
        self.assertEqual(self.os_product.get_download_size(), 5200)

    def test_display_shows_parent_and_child_info(self):
        output = captured_display(self.os_product)
        self.assertIn("D100", output)
        self.assertIn("Operating System", output)
        self.assertIn("5200.00 MB", output)

    def test_fulfilment_info(self):
        self.assertIn("digitally", self.os_product.get_fulfilment_info())

    def test_not_required_to_ship(self):
        self.assertNotIsInstance(self.os_product, CanBeShipped)
        self.assertFalse(hasattr(self.os_product, "calculate_shipping_cost"))


class TestAbstractClasses(unittest.TestCase):
    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X001", "Generic", 1.0, 1)

    def test_can_be_shipped_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_subclasses_are_products(self):
        self.assertIsInstance(PhysicalProduct("P1", "A", 1, 1, 1), Product)
        self.assertIsInstance(DigitalProduct("D1", "B", 1, 1, 1), Product)


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5))
        self.inventory.add_product(DigitalProduct("D100", "Operating System", 139.99, 100, 5200))

    def test_search_by_id_and_name(self):
        self.assertEqual(self.inventory.search_product("p100").get_name(), "Guitar")
        self.assertEqual(len(self.inventory.search_by_name("system")), 1)

    def test_update_stock(self):
        self.inventory.update_stock("D100", -10)
        self.assertEqual(self.inventory.search_product("D100").get_stock(), 90)

    def test_cannot_remove_more_than_stock(self):
        with self.assertRaises(ValueError):
            self.inventory.update_stock("P100", -99)

    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product(DigitalProduct("P100", "Dup", 1, 1, 1))


class TestJsonPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(self.temp_dir.name, "inventory.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_preserves_types(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5))
        inventory.add_product(DigitalProduct("D100", "Operating System", 139.99, 100, 5200))
        with redirect_stdout(io.StringIO()):
            save_inventory(inventory, self.filename)
            loaded = load_inventory(self.filename)

        guitar = loaded.search_product("P100")
        os_product = loaded.search_product("D100")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.get_weight(), 3.5)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(os_product.get_download_size(), 5200)

    def test_saved_json_has_type_identifier(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, 3.5))
        with redirect_stdout(io.StringIO()):
            save_inventory(inventory, self.filename)
        with open(self.filename) as file:
            data = json.load(file)
        self.assertEqual(data[0]["type"], "physical")
        self.assertEqual(data[0]["weight"], 3.5)


if __name__ == "__main__":
    unittest.main()
