def load_inventory():
        try:
                file = open ("inventory.txt", "r")
                data = file.readline()
                inventory = int(data)
                file.close()
                return inventory        
        except FileNotFoundError:
                return 0        

def save_inventory(inventory, history):
        file = open("inventory.txt", "w")
        file.write(str(inventory) + "\n")
        file.write(str(history))
        file.close()

def get_valid_input():
        stock = input("Enter stock quantity (or type 'quit' to exit): ")

        if stock == "quit":
                return "quit"

        if not stock.isdigit():
                print("Error: Invalid input. Please enter a valid number.")
                return None

        return int(stock)

def process_delivery(current_total, new_value):
        new_total = current_total + new_value
        return new_total

def calculate_tax(amount):
        tax = amount * 0.1  # Assuming a tax rate of 10%
        return tax

def generate_report(total_units, failed_attempts):
        print("\n---Inventory Report---")
        print("Total Units Processed:", total_units)
        print("Number of Failed/Rejected Entries:", failed_attempts)


inventory = load_inventory()
failed_entries = 0
deliveries = 0
history = []

while True:
        stock = get_valid_input()
        if stock == 'quit':
                save_inventory(inventory, history)
                break

        if stock is None:
                failed_entries += 1
                continue

        inventory = process_delivery(inventory, stock)
        tax = calculate_tax(stock)
        deliveries += 1
        history.append(stock)

        print("Stock added sucessfully.")
        print("Tax for this delivery:", tax)
        print("Current inventory:", inventory)

        if inventory > 500:
                print("ALERT: Overstock! Inventory exceeds 500 units.")
                break

generate_report(inventory, failed_entries)