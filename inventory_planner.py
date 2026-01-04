# inventory_planner.py
import csv
from ingredient_class import Ingredient, InsufficientStockError, RECIPES

INVENTORY_FILE = 'inventory.csv'
HEADER = ['Name', 'Quantity', 'Unit']

def load_inventory():
    """
    Loads ingredients from the CSV file.
      
    Returns:
      list[Ingredient].
    Notes:
      Warn on missing/extra headers; merge duplicates by (name, unit).
    """
    inventory = []
    # TODO: Implement load logic using csv.reader, handle conversion/errors
    try:
        with open(INVENTORY_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Checking if there are header issues
            file_headers = reader.fieldnames
            if file_headers is None:
                print(f" File '{INVENTORY_FILE}' is empty or corrupted.")
                return []

            missing_headers = [h for h in HEADER if h not in file_headers]
            extra_headers = [h for h in file_headers if h not in HEADER]
            if missing_headers:
                print(f"Missing headers: {missing_headers}")
            if extra_headers:
                print(f"Extra headers in CSV: {extra_headers}")

            merged = {}

            for row in reader:
                try:
                    name = row.get('Name', '').strip()
                    quantity = float(row.get('Quantity', 0))
                    unit = row.get('Unit', '').strip()

                    key = (name.lower(), unit.lower())

                    if key in merged:
                        merged[key].quantity += quantity
                    else:
                        merged[key] = Ingredient(name, quantity, unit)

                except ValueError:
                    print(f"Skipping invalid row (non-numeric quantity): {row}")
                except Exception as e:
                    print(f"Error reading row {row}: {e}")

            inventory = list(merged.values())

    except FileNotFoundError:
        print(f"'{INVENTORY_FILE}' not found. Returning empty inventory.")
        return []
    except Exception as e:
        print(f"Error reading '{INVENTORY_FILE}': {e}")
    return inventory

def save_inventory(inventory):
    """
    Saves the current inventory to CSV.
      
    Args:
      inventory: list[Ingredient] to persist (one row per item via to_csv_row()).
    """
    # TODO: Implementing save logic using csv.writer and Ingredient.to_csv_row()
    try:
        with open(INVENTORY_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)

            for item in inventory:
                writer.writerow(item.to_csv_row())

        print(f"Inventory successfully saved to '{INVENTORY_FILE}'.")

    except Exception as e:
        print(f"Error saving inventory: {e}")

def add_ingredient(inventory):
    """
    Prompt the user for a new ingredient and add it to the given inventory.

    Args:
      inventory: list[Ingredient] to mutate.
    Returns:
        None
    """
    name = input("Enter ingredient name: ").strip()
    if not name:
        print("Ingredient name cannot be empty.")
        return

    unit = input("Enter unit (e.g., g, ml, pcs): ").strip()
    if not unit:
        print("Unit cannot be empty.")
        return

    try:
        quantity = float(input("Enter quantity: ").strip())
    except ValueError:
        print("Invalid quantity. Please enter a numeric value.")
        return

    # Checks for duplicate (same name + unit for ingredients)
    for ing in inventory:
        if ing.name.lower() == name.lower() and ing.unit.lower() == unit.lower():
            print(f"    Ingredient '{name}' ({unit}) already exists in inventory.")
            try:
                merge_choice = input("Do you want to update the quantity? (y/n): ").strip().lower()
                if merge_choice == 'y':
                    ing.quantity += quantity
                    print(f"    Updated quantity of '{name}' to {ing.quantity} {unit}.")
                else:
                    print(" No changes made.")
            except Exception:
                print(" Could not update existing ingredient.")
            return

    # Add new ingredient
    try:
        new_ing = Ingredient(name, quantity, unit)
        inventory.append(new_ing)
        print(f"    Added {new_ing}")
    except ValueError as e:
        print(f"    Error: {e}")


def view_inventory(inventory):
    """
    Display the current inventory.
      
    Args:
        inventory: list[Ingredient] to display.
    Returns:
        None
    """
    if not inventory:
        print(" Inventory is empty.")
        return

    print("\n*** Current Inventory ***")
    for idx, item in enumerate(inventory, start=1):
        print(f"{idx}. {item}")
    print("")
def check_recipe(inventory):
    """
    Checks if there are enough ingredients for a chosen recipe.

    Args:
      inventory: list[Ingredient] to check against.
    Returns:
        None
    """

    print("\nAvailable Recipes:")
    for name in RECIPES.keys():
        print(f" - {name}")

    user_input = input("\nEnter recipe name to check: ").strip().lower()

    recipe_name = None
    for name in RECIPES.keys():
        if name.lower() == user_input:
            recipe_name = name
            break

    if recipe_name is None:
        print("❌ Recipe not found.")
        return

    recipe_needed = RECIPES[recipe_name]

    missing_items = []
    for req_name, req_quantity in recipe_needed.items():

        found = next((i for i in inventory if i.name.lower() == req_name.lower()), None)

        if not found:
            missing_items.append((req_name, req_quantity, "Missing"))
        elif found.quantity < req_quantity:
            needed = req_quantity - found.quantity
            missing_items.append((req_name, needed, found.unit))

    if missing_items:
        message_lines = ["❌ Insufficient stock for the recipe! Missing items:"]
        for name, needed, unit in missing_items:
            if unit == "Missing":
                message_lines.append(f" - {name}: {needed} (completely missing)")
            else:
                message_lines.append(f" - {name}: need {needed} more {unit}")
        message = "\n".join(message_lines)
        raise InsufficientStockError(message)

    print(f"✅ All ingredients are available for '{recipe_name}'!")


def main():
    """Main CLI loop: routes menu actions, catches recipe errors, saves on exit."""
    inventory = load_inventory()
    print("\n  Welcome to the Culinary Inventory Planner!")

    menu_options = {
        "1": add_ingredient,
        "2": view_inventory,
        "3": check_recipe,
        "4": "Exit"
    }

    while True:
        print("\nMain Menu:")
        print("1. Add Ingredient")
        print("2. View Inventory")
        print("3. Check Recipe")
        print("4. Exit")

        choice = input("Select an option (1–4): ").strip()

        if choice not in menu_options:
            print("❌ Invalid selection. Please choose between 1 and 4.")
            continue

        if choice == "4":
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm == 'y':
                save_inventory(inventory)
                print("     Inventory saved. Goodbye!")
                break
            else:
                print("     Returning to main menu.")
                continue

        action = menu_options[choice]
        if action == check_recipe:
            try:
                action(inventory)
            except InsufficientStockError as e:
                print(e)
        else:
            try:
                action(inventory)
            except Exception as e:
                print(f"     Unexpected error: {e}")


if __name__ == "__main__":
    main()
