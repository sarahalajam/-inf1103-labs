from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download (is-a Product). It is NOT shippable.

    LSP: DigitalProduct does not override update_stock(). Its stock means the
    number of licence keys available to sell, so adding or removing stock has
    exactly the same meaning as it does for any other Product.
    """

    TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__download_size: float = 0.0
        self.set_download_size(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def set_download_size(self, download_size: float) -> None:
        """Set download size in megabytes. Rejects negative numbers."""
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def display_information(self) -> None:
        super().display_information()   # parent prints the common details
        print(f"{'':<8}Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} is delivered digitally via download link."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data

    @staticmethod
    def from_dict(data: dict, supplier: Supplier) -> "DigitalProduct":
        return DigitalProduct(
            data["id"], data["name"], data["price"], data["stock"], supplier, data["download_size"]
        )
