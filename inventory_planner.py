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
                # basic row safety
                if len(row) < 3:
                    continue
                name, qty, unit = row[0].strip(), row[1].strip(), row[2].strip()
                try:
                    qty_val = float(qty)
                except ValueError:
                    # skip bad rows
                    print(f"Skipping row with invalid quantity: {row}")
                    continue
                key = (name.lower(), unit.lower())
                if key in merged:
                    merged[key].quantity += qty_val
                else:
                    merged[key] = Ingredient(name, qty_val, unit)
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


def add_ingredient(inventory):
    """
    Prompt user to add a new ingredient. Validates input and merges duplicates.
    """
    name = input("Ingredient name: ").strip()
    if not name:
        print("Name cannot be empty. Aborting add.")
        return

    qty_input = input("Quantity (number): ").strip()
    try:
        qty = float(qty_input)
    except ValueError:
        print("Quantity must be a number. Aborting add.")
        return

    unit = input("Unit (e.g. g, kg, pcs): ").strip()
    if not unit:
        print("Unit cannot be empty. Aborting add.")
        return

    # check for existing
    for ing in inventory:
        if ing.name.lower() == name.lower() and ing.unit.lower() == unit.lower():
            print(f"Found existing ingredient: {ing.name} ({ing.quantity} {ing.unit})")
            choice = input("Add quantity to existing item? (y/n): ").strip().lower()
            if choice == 'y':
                ing.quantity += qty
                print("Quantity updated.")
            else:
                print("Did not add.")
            return

    # not found -> add new
    inventory.append(Ingredient(name, qty, unit))
    print("Ingredient added.")


def view_inventory(inventory):
    """
    Print the current inventory in a neat list.
    """
    if not inventory:
        print("Inventory is empty.")
        return
    print("\nCurrent inventory:")
    for i, ing in enumerate(inventory, start=1):
        # print nicely
        try:
            print(f"{i}. {ing.name} - {ing.quantity} {ing.unit}")
        except Exception:
            print(f"{i}. (invalid ingredient object)")
    print("")


def main():
    inv = load_inventory()
    while True:
        print("\nMenu:\n1) View inventory\n2) Add ingredient\n3) Save inventory\n4) Save & Exit\n5) Exit without saving")
        choice = input("Choose an option (1-5): ").strip()
        if choice == '1':
            view_inventory(inv)
        elif choice == '2':
            add_ingredient(inv)
        elif choice == '3':
            save_inventory(inv)
            print("Inventory saved.")
        elif choice == '4':
            save_inventory(inv)
            print("Saved. Exiting.")
            break
        elif choice == '5':
            print("Exiting without saving.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == '__main__':
    main()
