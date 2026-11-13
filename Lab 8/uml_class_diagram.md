# UML Class Diagram – Lab 8 Inventory System

![UML class diagram](uml_class_diagram.png)

The PNG above is the submitted diagram. The Mermaid version below renders on GitHub and shows the same design.

## Relationships

| From → To | Relationship | Multiplicity | Why |
|---|---|---|---|
| PhysicalProduct → Product | Inheritance (solid line, hollow triangle) | – | PhysicalProduct *is-a* Product |
| DigitalProduct → Product | Inheritance (solid line, hollow triangle) | – | DigitalProduct *is-a* Product |
| PhysicalProduct → CanBeShipped | Realisation (dashed line, hollow triangle) | – | Only physical products can be shipped |
| Supplier — Product | **Association** (solid line) | Supplier 1 —— 0..* Product | Product keeps a reference to its Supplier, but neither is part of the other. Both can exist on their own. |
| Inventory ◇— Product | **Aggregation** (hollow diamond at Inventory) | Inventory 0..1 ◇—— 0..* Product | Inventory groups Products, but Products are created outside it and can be removed or moved to another Inventory without being destroyed. |
| Order ◆— OrderLine | **Composition** (filled diamond at Order) | Order 1 ◆—— 0..* OrderLine | Order creates its OrderLines in `add_order_line()`. A line belongs to exactly one Order, is never transferred, and goes away with the Order. |
| OrderLine — Product | **Association** (solid line) | OrderLine 0..* —— 1 Product | A line refers to a Product but does not own it. The same Product can be in many lines and orders. |

**Guiding question: what happens to the part when the whole goes away?**
- Delete a Supplier variable → the Products still hold their reference (association: no whole, no part).
- Empty an Inventory → the Products still exist and can go into another Inventory (aggregation).
- Delete an Order → its OrderLines go with it, but the Products they referred to are untouched (composition for the lines, association for the products).

## Types (Python ↔ UML)

| Python type hint | UML type used |
|---|---|
| `str` | String |
| `list[Product]` | Product [0..*] |
| `list[OrderLine]` / `tuple[OrderLine, ...]` | OrderLine [0..*] |
| `Product \| None` | Product [0..1] |
| `supplier: Supplier` | supplier : Supplier |
| `dict` | Dictionary |
| `-> None` | None (no value returned) |

## Mermaid source

```mermaid
classDiagram
    direction TB

    class Supplier {
        -supplier_id : String
        -name : String
        -contact_email : String
        +Supplier(supplier_id: String, name: String, contact_email: String)
        +get_supplier_id() String
        +get_name() String
        +get_contact_email() String
        +display_information() None
        +to_dict() Dictionary
        +from_dict(data: Dictionary)$ Supplier
    }

    class Product {
        <<abstract>>
        -product_id : String
        -name : String
        -price : float
        -stock : int
        -supplier : Supplier
        +Product(product_id: String, name: String, price: float, stock_quantity: int, supplier: Supplier)
        +get_product_id() String
        +get_name() String
        +get_price() float
        +get_stock() int
        +get_supplier() Supplier
        +set_stock(stock: int) None
        +update_stock(quantity: int) None
        +display_information() None
        +display_supplier_information() None
        +get_fulfilment_info()* String
        +to_dict() Dictionary
    }

    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }

    class PhysicalProduct {
        +TYPE : String = "physical"
        +BASE_SHIPPING_FEE : float = 5.00
        +RATE_PER_KG : float = 2.00
        -weight : float
        +PhysicalProduct(..., supplier: Supplier, weight: float)
        +get_weight() float
        +set_weight(weight: float) None
        +display_information() None
        +get_fulfilment_info() String
        +calculate_shipping_cost() float
        +to_dict() Dictionary
        +from_dict(data: Dictionary, supplier: Supplier)$ PhysicalProduct
    }

    class DigitalProduct {
        +TYPE : String = "digital"
        -download_size : float
        +DigitalProduct(..., supplier: Supplier, download_size: float)
        +get_download_size() float
        +set_download_size(download_size: float) None
        +display_information() None
        +get_fulfilment_info() String
        +to_dict() Dictionary
        +from_dict(data: Dictionary, supplier: Supplier)$ DigitalProduct
    }

    class Inventory {
        -products : Product [0..*]
        +Inventory()
        +add_product(product: Product) None
        +remove_product(product_id: String) Product [0..1]
        +find_product(product_id: String) Product [0..1]
        +search_by_name(keyword: String) Product [0..*]
        +update_stock(product_id: String, quantity: int) Product
        +clear() None
        +get_products() Product [0..*]
        +display_all_products() None
    }

    class Order {
        -order_id : String
        -order_lines : OrderLine [0..*]
        +Order(order_id: String)
        +get_order_id() String
        +add_order_line(product: Product, quantity: int) None
        +remove_order_line(product_id: String) bool
        +get_order_lines() OrderLine [0..*]
        +calculate_total() float
        +display_order() None
    }

    class OrderLine {
        -product : Product
        -quantity : int
        +OrderLine(product: Product, quantity: int)
        +get_product() Product
        +get_quantity() int
        +calculate_subtotal() float
        +display_information() None
    }

    Product <|-- PhysicalProduct : inheritance
    Product <|-- DigitalProduct : inheritance
    CanBeShipped <|.. PhysicalProduct : realisation
    Supplier "1" -- "0..*" Product : association - supplied by
    Inventory "0..1" o-- "0..*" Product : aggregation - contains
    Order "1" *-- "0..*" OrderLine : composition - made up of
    OrderLine "0..*" -- "1" Product : association - refers to
```
