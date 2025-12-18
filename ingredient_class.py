# ingredient_class.py

class InsufficientStockError(Exception):
    """Raised when inventory quantity is too low for a recipe."""
    pass


class Ingredient:
    """Represents a single item in the kitchen inventory."""

    def __init__(self, name, quantity, unit):
        """
        Initialize an Ingredient.

        quantity is validated to be numeric (int/float or numeric string).
        The stored quantity will be an int if it has no fractional part, otherwise a float.
        """
        self.name = name
        # Validate quantity is numeric
        try:
            q = float(quantity)
        except (TypeError, ValueError):
            raise TypeError("quantity must be numeric (int, float, or numeric string)")

        # Convert to int when it's a whole number for nicer output
        if q.is_integer():
            q = int(q)

        self.quantity = q
        self.unit = unit

    def to_csv_row(self):
        """
        Converts the Ingredient object to a list for CSV writing.
        Returns: [name, quantity, unit]
        """
        return [self.name, self.quantity, self.unit]

    def __str__(self):
        """Nicely formatted display of the ingredient."""
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient(name={self.name!r}, quantity={self.quantity!r}, unit={self.unit!r})"


# Simple predefined recipes (recipe name -> {ingredient name: quantity_required})
# Note: quantities in RECIPES are amounts only (units assumed by the application).
RECIPES = {
    "Pap and Wors": {"Maize Meal": 250, "Wors": 500},
    "Spinach and Feta Salad": {"Spinach": 100, "Feta": 50, "Tomato": 1},
    # Extra recipe required by the assignment:
    "Tomato Soup": {"Tomato": 400, "Onion": 50, "Garlic": 5, "Vegetable Stock": 500},
}


# Quick self-test when running this file directly
if __name__ == "__main__":
    # Create a few example Ingredient objects
    i1 = Ingredient("Maize Meal", 250, "g")
    i2 = Ingredient("Wors", "500", "g")  # numeric string is accepted
    i3 = Ingredient("Tomato", 1.0, "pc")  # float with integer value becomes int

    print(i1)                     # -> Maize Meal: 250 g
    print(i2.to_csv_row())        # -> ['Wors', 500, 'g']
    print(repr(i3))               # -> Ingredient(name='Tomato', quantity=1, unit='pc')

    # Demonstrate invalid quantity raises error
    try:
        Ingredient("Sugar", "two hundred", "g")
    except Exception as e:
        print("Expected error:", e)
