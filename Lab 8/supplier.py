class Supplier:
    """Who supplies a product (association with Product - no ownership).

    A Supplier is created on its own and then handed to each Product it
    supplies. It is not part of a Product, and a Product is not part of it,
    so either can exist without the other.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = str(supplier_id)
        self.__name: str = str(name)
        self.__contact_email: str = str(contact_email)

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier {self.__supplier_id}: {self.__name} <{self.__contact_email}>")

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @staticmethod
    def from_dict(data: dict[str, str]) -> "Supplier":
        return Supplier(data["id"], data["name"], data["contact_email"])
