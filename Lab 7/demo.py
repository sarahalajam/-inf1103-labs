"""Walks through Lab 7 sections 1-4 so each concept can be seen in the output."""
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped


def main():
    guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, 3.5)
    windows = DigitalProduct("D100", "Operating System", 139.99, 100, 5200)

    print("=== 1 & 2. Inheritance + method overriding (display_information) ===")
    guitar.display_information()
    windows.display_information()

    print("\n=== 3.2 Abstract method implemented by each subclass ===")
    print(guitar.get_fulfilment_info())
    print(windows.get_fulfilment_info())

    print("\n=== 3.3 Trying to create a Product directly ===")
    try:
        Product("X001", "Generic", 1.00, 1)
    except TypeError as error:
        print(f"TypeError: {error}")

    print("\n=== 4.2 CanBeShipped: shipping cost by weight ===")
    for weight in (0.5, 3.5, 20):
        item = PhysicalProduct("P2", "Box", 10.00, 1, weight)
        print(f"{weight:>5} kg -> ${item.calculate_shipping_cost():.2f}")
    print(f"Guitar is CanBeShipped? {isinstance(guitar, CanBeShipped)}")
    print(f"Operating System is CanBeShipped? {isinstance(windows, CanBeShipped)}")


if __name__ == "__main__":
    main()
