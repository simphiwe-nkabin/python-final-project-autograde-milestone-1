# inventory_planner.py
import csv
from ingredient_class import Ingredient, InsufficientStockError, RECIPES

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
                if len(row) < 3:
                    continue
                name, qty, unit = row[0].strip(), row[1].strip(), row[2].strip()
                try:
                    qty_val = float(qty)
                except ValueError:
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

    inventory.append(Ingredient(name, qty, unit))
    print("Ingredient added.")


def view_inventory(inventory):
    if not inventory:
        print("Inventory is empty.")
        return
    print("\nCurrent inventory:")
    for i, ing in enumerate(inventory, start=1):
        try:
            print(f"{i}. {ing.name} - {ing.quantity} {ing.unit}")
        except Exception:
            print(f"{i}. (invalid ingredient object)")
    print("")


def check_recipe(inventory):
    print("Available recipes:")
    for name in RECIPES.keys():
        print(f" - {name}")

    recipe_name = input("Enter recipe name to check: ").strip().title()
    recipe_needed = RECIPES.get(recipe_name)

    if recipe_needed is None:
        print("Recipe not found.")
        return

    missing = []

    for req_name, req_info in recipe_needed.items():
        try:
            req_qty, req_unit = req_info
        except Exception:
            continue

        have_qty = 0
        for ing in inventory:
            if ing.name.lower() == req_name.lower() and ing.unit.lower() == req_unit.lower():
                try:
                    have_qty = float(ing.quantity)
                except Exception:
                    have_qty = 0
                break

        if have_qty < req_qty:
            missing.append((req_name, req_qty, req_unit, have_qty))

    if missing:
        msg_lines = ["Missing or insufficient ingredients:"]
        for name, need, unit, have in missing:
            need_more = need - have
            have_str = str(int(have)) if float(have).is_integer() else str(have)
            need_more_str = str(int(need_more)) if float(need_more).is_integer() else str(need_more)
            msg_lines.append(f" - {name}: need {need} {unit}, have {have_str} {unit} (need {need_more_str} more)")
        raise InsufficientStockError("\n".join(msg_lines))

    print(f"You have all the ingredients for {recipe_name}.")


def main():
    inv = load_inventory()
    while True:
        print("\nMenu:\n"
              "1) View inventory\n"
              "2) Add ingredient\n"
              "3) Save inventory\n"
              "4) Save & Exit\n"
              "5) Exit without saving\n"
              "6) Check recipe")
        choice = input("Choose an option (1-6): ").strip()
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
        elif choice == '6':
            try:
                check_recipe(inv)
            except InsufficientStockError as e:
                print(e)
        else:
            print("Invalid choice, try again.")


if __name__ == '__main__':
    main()
