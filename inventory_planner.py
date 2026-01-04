import csv
from ingredient_class import Ingredient

def save_inventory(inventory):
    """Saves the current inventory to a CSV file."""
    with open('inventory.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "quantity", "unit"])
        for ingredient in inventory:
            writer.writerow(ingredient.to_csv_row())

def load_inventory():
    """Loads inventory from a CSV file and returns a list of Ingredient objects."""
    inventory_map = {}
    try:
        with open('inventory.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            if headers != ["name", "quantity", "unit"]:
                raise ValueError("Invalid CSV header. Expected ['name', 'quantity', 'unit'].")

            for row in reader:
                if len(row) != 3:
                    print(f"Skipping malformed row: {row}")
                    continue
                name, quantity_str, unit = row
                try:
                    quantity = float(quantity_str)
                    if name in inventory_map:
                        # If ingredient already exists, add to its quantity
                        inventory_map[name].quantity += quantity
                    else:
                        inventory_map[name] = Ingredient(name, quantity, unit)
                except ValueError:
                    print(f"Skipping row due to invalid quantity for {name}: '{quantity_str}' is not numeric.")
    except FileNotFoundError:
        print("inventory.csv not found. Returning empty inventory.")
        return []
    except ValueError as e:
        print(f"Error loading inventory: {e}")
        return []

    return list(inventory_map.values())

def view_inventory(inventory):
    """Displays the current inventory."""
    if not inventory:
        print("Your inventory is currently empty.")
        return

    print("\n--- Current Inventory ---")
    for ingredient in inventory:
        print(ingredient) 
    print("-------------------------")

def add_ingredient(inventory):
    """Adds a new ingredient or updates an existing one in the inventory."""
    print("\n--- Add/Update Ingredient ---")
    while True:
        name = input("Enter ingredient name (e.g., 'Flour', 'Sugar'): ").strip()
        if name:
            break
        else:
            print("Ingredient name cannot be empty. Please try again.")

    while True:
        unit = input(f"Enter unit for {name} (e.g., 'grams', 'ml', 'pieces'): ").strip()
        if unit:
            break
        else:
            print("Unit cannot be empty. Please try again.")

    while True:
        quantity_str = input(f"Enter quantity for {name} in {unit}: ").strip()
        try:
            quantity = float(quantity_str)
            if quantity <= 0:
                print("Quantity must be a positive number. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid quantity. Please enter a numeric value.")
            
    found_existing = False
    for item in inventory:
        if item.name.lower() == name.lower():
            item.quantity += quantity
          
            if item.unit.lower() != unit.lower():
                print(f"Warning: Unit for '{name}' changed from '{item.unit}' to '{unit}'.")
                item.unit = unit
            print(f"Updated quantity for {item.name}: new total is {item.quantity} {item.unit}.")
            found_existing = True
            break

    if not found_existing:
        new_ingredient = Ingredient(name, quantity, unit)
        inventory.append(new_ingredient)
        print(f"Added new ingredient: {new_ingredient}.")
    print("-----------------------------")
