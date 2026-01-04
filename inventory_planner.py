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
