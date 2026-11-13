"""Lab 8 section 9 checklist as unit tests. Run with: python -m unittest -v"""
import inspect
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
from supplier import Supplier
from inventory import Inventory
from order_line import OrderLine
from order import Order
from file_handler import load_inventory, save_inventory


def captured(func, *args) -> str:
    """Return whatever func(*args) prints."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue()


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSource", "sales@techsource.example.com")


# ---------------------------------------------------------------- Association
class TestSupplierAssociation(unittest.TestCase):
    def setUp(self):
        self.supplier = make_supplier()
        self.laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, self.supplier, 2.1)
        self.antivirus = DigitalProduct("D001", "Antivirus", 49.9, 300, self.supplier, 350)

    def test_supplier_display_information(self):
        output = captured(self.supplier.display_information)
        self.assertIn("S001", output)
        self.assertIn("TechSource", output)
        self.assertIn("sales@techsource.example.com", output)

    def test_product_stores_reference_to_supplier_object(self):
        self.assertIs(self.laptop.get_supplier(), self.supplier)
        self.assertIs(self.antivirus.get_supplier(), self.supplier)

    def test_supplier_info_through_product(self):
        self.assertIn("TechSource", captured(self.laptop.display_supplier_information))
        self.assertIn("TechSource", captured(self.antivirus.display_supplier_information))

    def test_supplier_and_product_are_separate_objects(self):
        self.assertIsNot(self.laptop, self.supplier)
        self.assertNotIsInstance(self.supplier, Product)

    def test_product_still_works_after_supplier_variable_deleted(self):
        supplier = Supplier("S002", "Temp", "t@example.com")
        product = PhysicalProduct("P9", "Box", 1.0, 1, supplier, 1)
        del supplier
        self.assertEqual(product.get_supplier().get_name(), "Temp")

    def test_supplier_exists_without_products(self):
        lonely = Supplier("S003", "Lonely", "l@example.com")
        self.assertEqual(lonely.get_name(), "Lonely")


# ---------------------------------------------------------------- Aggregation
class TestInventoryAggregation(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P003", "Guitar", 350.0, 5, make_supplier(), 3.5)
        self.inventory_a = Inventory()
        self.inventory_b = Inventory()

    def test_add_and_find(self):
        self.inventory_a.add_product(self.guitar)
        self.assertIs(self.inventory_a.find_product("p003"), self.guitar)

    def test_find_missing_returns_none(self):
        self.assertIsNone(self.inventory_a.find_product("NOPE"))

    def test_remove_does_not_destroy_product(self):
        self.inventory_a.add_product(self.guitar)
        removed = self.inventory_a.remove_product("P003")
        self.assertIs(removed, self.guitar)
        self.assertIsNone(self.inventory_a.find_product("P003"))
        self.guitar.update_stock(1)     # still fully usable
        self.assertEqual(self.guitar.get_stock(), 6)

    def test_transfer_same_object_to_another_inventory(self):
        self.inventory_a.add_product(self.guitar)
        self.inventory_a.remove_product("P003")
        self.inventory_b.add_product(self.guitar)
        self.assertIs(self.inventory_b.find_product("P003"), self.guitar)

    def test_clearing_inventory_keeps_products(self):
        self.inventory_a.add_product(self.guitar)
        self.inventory_a.clear()
        self.assertEqual(self.inventory_a.get_products(), [])
        self.assertEqual(self.guitar.get_name(), "Guitar")

    def test_duplicate_id_rejected(self):
        self.inventory_a.add_product(self.guitar)
        with self.assertRaises(ValueError):
            self.inventory_a.add_product(
                DigitalProduct("P003", "Dup", 1, 1, make_supplier(), 1))

    def test_cannot_remove_more_than_stock(self):
        self.inventory_a.add_product(self.guitar)
        with self.assertRaises(ValueError):
            self.inventory_a.update_stock("P003", -99)


# ---------------------------------------------------------------- Composition
class TestOrderComposition(unittest.TestCase):
    def setUp(self):
        supplier = make_supplier()
        self.laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.1)
        self.mouse = PhysicalProduct("P002", "Mouse", 25.5, 40, supplier, 0.1)
        self.office = DigitalProduct("D003", "Office Suite", 99.0, 500, supplier, 2400)

    def test_order_line_subtotal(self):
        line = OrderLine(self.mouse, 4)
        self.assertEqual(line.calculate_subtotal(), 102.0)

    def test_order_creates_its_own_lines(self):
        order = Order("O001")
        order.add_order_line(self.laptop, 1)
        order.add_order_line(self.mouse, 2)
        lines = order.get_order_lines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(isinstance(line, OrderLine) for line in lines))
        self.assertIs(lines[0].get_product(), self.laptop)

    def test_add_order_line_takes_product_and_quantity_not_a_line(self):
        params = list(inspect.signature(Order.add_order_line).parameters)
        self.assertEqual(params, ["self", "product", "quantity"])

    def test_total_uses_order_line_subtotals(self):
        order = Order("O001")
        order.add_order_line(self.laptop, 1)   # 1200.00
        order.add_order_line(self.mouse, 2)    #   51.00
        order.add_order_line(self.office, 1)   #   99.00
        self.assertAlmostEqual(order.calculate_total(), 1350.0)
        self.assertAlmostEqual(
            order.calculate_total(),
            sum(line.calculate_subtotal() for line in order.get_order_lines()))

    def test_same_product_in_two_orders(self):
        order_1, order_2 = Order("O001"), Order("O002")
        order_1.add_order_line(self.laptop, 1)
        order_2.add_order_line(self.laptop, 3)
        line_1, line_2 = order_1.get_order_lines()[0], order_2.get_order_lines()[0]
        self.assertIsNot(line_1, line_2)                          # 2 OrderLines
        self.assertIs(line_1.get_product(), line_2.get_product())  # 1 Product

    def test_remove_order_line(self):
        order = Order("O001")
        order.add_order_line(self.laptop, 1)
        order.add_order_line(self.mouse, 2)
        self.assertTrue(order.remove_order_line("P002"))
        self.assertFalse(order.remove_order_line("P002"))
        self.assertEqual(len(order.get_order_lines()), 1)
        self.assertEqual(self.mouse.get_name(), "Mouse")   # Product unaffected

    def test_lines_cannot_be_changed_from_outside(self):
        order = Order("O001")
        order.add_order_line(self.laptop, 1)
        with self.assertRaises(AttributeError):
            order.get_order_lines().append(OrderLine(self.mouse, 1))

    def test_invalid_quantity_rejected(self):
        with self.assertRaises(ValueError):
            Order("O001").add_order_line(self.laptop, 0)


# ------------------------------------------------------------ LSP + polymorphism
class TestLiskovAndPolymorphism(unittest.TestCase):
    def setUp(self):
        supplier = make_supplier()
        self.products: list[Product] = [
            PhysicalProduct("P003", "Guitar", 350.0, 5, supplier, 3.5),
            DigitalProduct("D002", "Photo Editor", 59.0, 250, supplier, 850),
        ]
        self.inventory = Inventory()
        for product in self.products:
            self.inventory.add_product(product)

    def test_both_subclasses_are_products(self):
        for product in self.products:
            self.assertIsInstance(product, Product)

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X001", "Generic", 1.0, 1, make_supplier())

    def test_update_stock_has_same_meaning_for_every_subclass(self):
        for product in self.products:
            before = product.get_stock()
            self.inventory.update_stock(product.get_product_id(), 3)
            self.assertEqual(product.get_stock(), before + 3)
            self.inventory.update_stock(product.get_product_id(), -3)
            self.assertEqual(product.get_stock(), before)
            with self.assertRaises(ValueError):
                self.inventory.update_stock(product.get_product_id(), -(before + 1))

    def test_fulfilment_info_always_returns_str(self):
        for product in self.products:
            self.assertIsInstance(product.get_fulfilment_info(), str)

    def test_polymorphic_calls_pick_subclass_implementation(self):
        results = [p.get_fulfilment_info() for p in self.inventory.get_products()]
        self.assertEqual(results[0], "Guitar requires physical shipping.")
        self.assertEqual(results[1], "Photo Editor is delivered digitally via download link.")

    def test_display_shows_subclass_details(self):
        output = captured(self.inventory.display_all_products)
        self.assertIn("3.50 kg", output)       # PhysicalProduct version
        self.assertIn("850.00 MB", output)     # DigitalProduct version
        self.assertIn("TechSource", output)    # supplier via Product

    def test_only_physical_products_can_be_shipped(self):
        self.assertIsInstance(self.products[0], CanBeShipped)
        self.assertNotIsInstance(self.products[1], CanBeShipped)


# -------------------------------------------------------------- Type hints
class TestTypeHints(unittest.TestCase):
    def test_key_type_hints_present(self):
        self.assertIs(inspect.signature(Product.__init__).parameters["supplier"].annotation,
                      Supplier)
        self.assertIs(inspect.signature(Inventory.add_product).parameters["product"].annotation,
                      Product)
        self.assertEqual(inspect.signature(Inventory.find_product).return_annotation,
                         Product | None)
        self.assertIs(inspect.signature(OrderLine.calculate_subtotal).return_annotation, float)
        self.assertIs(inspect.signature(Order.calculate_total).return_annotation, float)


# -------------------------------------------------------------- Persistence
class TestJsonPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(self.temp_dir.name, "inventory.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_keeps_types_and_shared_supplier(self):
        supplier = make_supplier()
        suppliers = {supplier.get_supplier_id(): supplier}
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, supplier, 3.5))
        inventory.add_product(DigitalProduct("D100", "OS", 139.99, 100, supplier, 5200))
        with redirect_stdout(io.StringIO()):
            save_inventory(inventory, suppliers, self.filename)
            loaded, loaded_suppliers = load_inventory(self.filename)

        guitar, os_product = loaded.find_product("P100"), loaded.find_product("D100")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(guitar.get_supplier().get_name(), "TechSource")
        # Both products point at the SAME loaded Supplier object.
        self.assertIs(guitar.get_supplier(), os_product.get_supplier())
        self.assertIs(guitar.get_supplier(), loaded_suppliers["S001"])

    def test_saved_json_stores_supplier_id_only(self):
        supplier = make_supplier()
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P100", "Guitar", 350.0, 5, supplier, 3.5))
        with redirect_stdout(io.StringIO()):
            save_inventory(inventory, {"S001": supplier}, self.filename)
        with open(self.filename) as file:
            data = json.load(file)
        self.assertEqual(data["products"][0]["supplier_id"], "S001")
        self.assertEqual(data["suppliers"][0]["name"], "TechSource")

    def test_project_inventory_json_loads(self):
        here = os.path.dirname(os.path.abspath(__file__))
        with redirect_stdout(io.StringIO()):
            inventory, suppliers = load_inventory(os.path.join(here, "inventory.json"))
        self.assertEqual(len(suppliers), 3)
        self.assertEqual(len(inventory.get_products()), 5)


if __name__ == "__main__":
    unittest.main()
