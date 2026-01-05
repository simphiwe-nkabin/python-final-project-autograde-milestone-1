# inventory_planner.py
import sys
import os
# ensure local module imports work in VS Code / Pylance
# (Needed for 'from ingredient_class import...')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import csv
from ingredient_class import Ingredient, InsufficientStockError, RECIPES

INVENTORY_FILE = 'inventory.csv'
HEADER = ['Name', 'Quantity', 'Unit']


def load_inventory():
    """Load inventory from INVENTORY_FILE. Merge duplicates by (name, unit)."""
    inventory = []
    try:
        with open(INVENTORY_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                # File is empty except maybe header
                return inventory

            merged = {}
            for row in reader:
                if len(row) < 3:
                    # skip malformed rows
                    continue
                name, qty, unit = row[0].strip(), row[1].strip(), row[2].strip()
                if not name or not unit:
                    continue
                try:
                    qty_val = float(qty)
                except Exception:
                    # skip rows with bad quantities
                    print(f"Skipping row with invalid quantity: {row}")
                    continue

                key = (name.lower(), unit.lower())
                if key in merged:
                    merged[key].quantity += qty_val
                else:
                    merged[key] = Ingredient(name, qty_val, unit)

            inventory = list(merged.values())
    except FileNotFoundError:
        print(f"{INVENTORY_FILE} not found. Starting with empty inventory.")
    except Exception as e:
        print(f"Error loading inventory: {e}")
    return inventory


def save_inventory(inventory):
    """Write inventory to INVENTORY_FILE (overwrite)."""
    try:
        with open(INVENTORY_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            for ing in inventory:
                # attempt to write sensible values
                name = getattr(ing, 'name', '')
                qty = getattr(ing, 'quantity', '')
                unit = getattr(ing, 'unit', '')
                writer.writerow([name, qty, unit])
    except Exception as e:
        print(f"Error saving inventory: {e}")


def add_ingredient(inventory):
    """Prompt user to add an ingredient. Validate inputs and merge duplicates."""
    name = input("Ingredient name: ").strip()
    if not name:
        print("Name cannot be empty. Aborting add.")
        return

    qty_input = input("Quantity (number): ").strip()
    try:
        qty = float(qty_input)
    except Exception:
        print("Quantity must be a number. Aborting add.")
        return

    unit = input("Unit (e.g. g, kg, pcs): ").strip()
    if not unit:
        print("Unit cannot be empty. Aborting add.")
        return

    # merge with existing if same name & unit (case-insensitive check)
    for ing in inventory:
        if ing.name.lower() == name.lower() and ing.unit.lower() == unit.lower():
            print(f"Found existing ingredient: {ing.name} ({ing.quantity} {ing.unit})")
            choice = input("Add quantity to existing item? (y/n): ").strip().lower()
            if choice == 'y':
                try:
                    ing.quantity += qty
                except Exception:
                    # fallback: replace quantity if addition fails
                    ing.quantity = float(qty)
                print("Quantity updated.")
            else:
                print("Did not add.")
            return

    # not found -> add new
    inventory.append(Ingredient(name, qty, unit))
    print("Ingredient added.")


def view_inventory(inventory):
    """Display the inventory in a simple numbered list."""
    if not inventory:
        print("Inventory is empty.")
        return
    print("\nCurrent inventory:")
    for i, ing in enumerate(inventory, start=1):
        try:
            # Use the Ingredient's __str__ method for nice formatting
            print(f"{i}. {ing}") 
        except Exception:
            print(f"{i}. (invalid ingredient object)")
    print("")


def check_recipe(inventory):
    """
    Let user choose a recipe (from RECIPES) and check if inventory has enough.
    If shortages exist, raise InsufficientStockError with a summary.
    """
    if not RECIPES:
        print("No recipes available to check.")
        return

    print("Available recipes:")
    for name in RECIPES.keys():
        print(f" - {name}")

    recipe_name = input("Enter recipe name to check: ").strip().title()
    recipe_needed = RECIPES.get(recipe_name)

    if recipe_needed is None:
        print("Recipe not found.")
        return

    missing = []

    # recipe_expected format: { 'Tomato': (2, 'pcs'), ... }
    for req_name, req_info in recipe_needed.items():
        try:
            req_qty, req_unit = req_info
        except Exception:
            # skip invalid recipe entries
            continue

        have_qty = 0.0
        # Find the matching ingredient in inventory
        for ing in inventory:
            if ing.name.lower() == req_name.lower() and ing.unit.lower() == req_unit.lower():
                try:
                    have_qty = float(ing.quantity)
                except Exception:
                    have_qty = 0.0
                break # Found the item, stop searching

        if have_qty < req_qty:
            missing.append((req_name, req_qty, req_unit, have_qty))

    if missing:
        # Helper for consistent number formatting
        def format_qty(q):
            q = float(q)
            return str(int(q)) if q.is_integer() else f"{q:.2f}"

        # build a readable summary of shortages
        lines = ["Missing or insufficient ingredients:"]
        for name, need, unit, have in missing:
            need_more = need - have
            
            have_str = format_qty(have)
            need_more_str = format_qty(need_more)
            need_str = format_qty(need)

            lines.append(f" - {name}: need {need_str} {unit}, have {have_str} {unit} (need {need_more_str} more)")
        
        # Raise the custom exception as intended by the original script
        raise InsufficientStockError("\n".join(lines))

    print(f"You have all the ingredients for {recipe_name}.")


def main():
    """Main CLI loop: routes menu actions, catches recipe errors, saves on exit."""
    inventory = load_inventory()
    print("\nWelcome to the Culinary Inventory Planner!")

    while True:
        print("\nMenu:")
        print("1. Add Ingredient")
        print("2. View Inventory")
        print("3. Check Recipe")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip
