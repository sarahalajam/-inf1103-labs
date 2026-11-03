# UML Class Diagram – OOP Inventory System

```
+-------------------------------------------+
|                 Product                   |
+-------------------------------------------+
| - __product_id : String                   |
| - __name : String                         |
| - __price : float                         |
| - __stock : int                           |
+-------------------------------------------+
| + __init__(product_id, name, price, stock)|
| + get_product_id() : String               |
| + get_name() : String                     |
| + get_price() : float                     |
| + get_stock() : int                       |
| + set_stock(stock : int) : void           |
| + update_stock(quantity : int) : void     |
| + display_information() : void            |
| + to_dict() : dict                        |
| + from_dict(data : dict) : Product        |
+-------------------------------------------+
                     ^
                     | 0..*
                     |
                     <> 1   (aggregation: Inventory has Products)
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
  file_handler.py : load_inventory(filename) : Inventory
                    save_inventory(inventory, filename) : void
  main.py         : main() – menu, user input, calls Inventory methods
```
