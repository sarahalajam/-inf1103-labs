# UML Class Diagram – Lab 7 Inventory System

Notation used:
- `<<abstract>>` / `{abstract}` – abstract class / abstract method
- `<<interface>>` – interface-style abstract base class
- `───▷` solid line, hollow triangle   = inheritance (generalisation), points to parent
- `- - ▷` dashed line, hollow triangle = interface realisation, points to interface
- `◇───` hollow diamond                = aggregation (Inventory has Products)

```
+-------------------------------------------+            +----------------------------------+
|               <<abstract>>                |            |          <<interface>>           |
|                 Product                   |            |          CanBeShipped            |
+-------------------------------------------+            +----------------------------------+
| - __product_id : String                   |            |                                  |
| - __name : String                         |            +----------------------------------+
| - __price : float                         |            | + calculate_shipping_cost()      |
| - __stock : int                           |            |       : float {abstract}         |
+-------------------------------------------+            +----------------------------------+
| + __init__(product_id, name, price, stock)|                            △
| + get_product_id() : String               |                            ┊
| + get_name() : String                     |                            ┊  (realisation:
| + get_price() : float                     |                            ┊   dashed line)
| + get_stock() : int                       |                            ┊
| + set_stock(stock : int) : void           |                            ┊
| + update_stock(quantity : int) : void     |                            ┊
| + display_information() : void            |                            ┊
| + get_fulfilment_info() : String          |                            ┊
|       {abstract}                          |                            ┊
| + to_dict() : dict                        |                            ┊
+-------------------------------------------+                            ┊
     ◇ 1             △ (inheritance: solid line)                         ┊
     |               |                                                   ┊
     |      +--------+-------------------------------+                   ┊
     |      |                                        |                   ┊
     |  +-----------------------------------+   +----+-----------------------------+
     |  |          DigitalProduct           |   |         PhysicalProduct          |
     |  +-----------------------------------+   +----------------------------------+
     |  | + TYPE : String = "digital"       |   | + TYPE : String = "physical"     |
     |  | - __download_size : float         |   | + BASE_SHIPPING_FEE : float      |
     |  +-----------------------------------+   | + RATE_PER_KG : float            |
     |  | + __init__(product_id, name,      |   | - __weight : float               |
     |  |     price, stock, download_size)  |   +----------------------------------+
     |  | + get_download_size() : float     |   | + __init__(product_id, name,     |
     |  | + set_download_size(size : float) |   |     price, stock, weight)        |
     |  |     : void                        |   | + get_weight() : float           |
     |  | + display_information() : void    |   | + set_weight(weight : float)     |
     |  | + get_fulfilment_info() : String  |   |     : void                       |
     |  | + to_dict() : dict                |   | + display_information() : void   |
     |  | + from_dict(data : dict)          |   | + get_fulfilment_info() : String |
     |  |     : DigitalProduct              |   | + calculate_shipping_cost()      |
     |  +-----------------------------------+   |     : float                      |
     |                                          | + to_dict() : dict               |
     |                                          | + from_dict(data : dict)         |
     |                                          |     : PhysicalProduct            |
     |                                          +----------------------------------+
     |                                              (PhysicalProduct - - ▷ CanBeShipped)
     | 0..*
     |   (aggregation: Inventory has 0..* Products)
+-------------------------------------------+
|                Inventory                  |
+-------------------------------------------+
| - __products : List<Product>              |
+-------------------------------------------+
| + __init__()                              |
| + add_product(product : Product) : void   |
| + search_product(product_id : String)     |
|       : Product                           |
| + search_by_name(keyword : String)        |
|       : List<Product>                     |
| + update_stock(product_id : String,       |
|       quantity : int) : Product           |
| + get_products() : List<Product>          |
| + display_all() : void                    |
+-------------------------------------------+

Supporting modules (not classes):
  file_handler.py : PRODUCT_TYPES : dict  ("physical" -> PhysicalProduct, "digital" -> DigitalProduct)
                    product_from_dict(data) : Product
                    load_inventory(filename) : Inventory
                    save_inventory(inventory, filename) : void
  main.py         : main() – menu, user input, creates Physical/Digital products, calls Inventory methods
```

Relationship summary:
| From            | To           | Relationship                         |
|-----------------|--------------|--------------------------------------|
| PhysicalProduct | Product      | Inheritance (solid line, hollow ▷)   |
| DigitalProduct  | Product      | Inheritance (solid line, hollow ▷)   |
| PhysicalProduct | CanBeShipped | Realisation (dashed line, hollow ▷)  |
| Inventory       | Product      | Aggregation 1 ◇── 0..*               |
