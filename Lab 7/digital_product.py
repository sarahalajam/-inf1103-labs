from product import Product


class DigitalProduct(Product):
    """A product delivered by download (is-a Product). It is NOT shippable."""

    TYPE = "digital"

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = 0.0
        self.set_download_size(download_size)

    def get_download_size(self):
        return self.__download_size

    def set_download_size(self, download_size):
        """Set download size in megabytes. Rejects negative numbers."""
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def display_information(self):
        super().display_information()   # parent prints the common details
        print(f"{'':<8}Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return f"{self.get_name()} is delivered digitally via download link."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data

    @staticmethod
    def from_dict(data):
        return DigitalProduct(
            data["id"], data["name"], data["price"], data["stock"], data["download_size"]
        )
