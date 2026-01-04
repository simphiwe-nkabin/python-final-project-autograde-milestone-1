# inventory_planner.py
import csv
from ingredient_class import Ingredient

INVENTORY_FILE = 'inventory.csv'
HEADER = ['Name', 'Quantity', 'Unit']

def load_inventory():
    inventory = []
    try:
        with open(INVENTORY_FILE, newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            merged = {}
            for row in reader:
                name, qty, unit = row
                qty = float(qty)
                key = (name.lower(), unit.lower())
                if key in merged:
                    merged[key].quantity += qty
                else:
                    merged[key] = Ingredient(name, qty, unit)
            inventory = list(merged.values())
    except FileNotFoundError:
        print(f"{INVENTORY_FILE} not found. Starting empty inventory.")
    return inventory

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for ing in inventory:
            writer.writerow([ing.name, ing.quantity, ing.unit])

if __name__ == '__main__':
    inv = load_inventory()
    print(f"Loaded {len(inv)} items")
    save_inventory(inv)
