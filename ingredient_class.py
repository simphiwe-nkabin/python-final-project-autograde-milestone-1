# ingredient_class.py

class InsufficientStockError(Exception):
    """Raised when inventory quantity is too low for a recipe."""
    pass


class Ingredient:
    """Represents a single item in the kitchen inventory."""

    def __init__(self, name, quantity, unit):
        # Validates if quantity is a number
        if not isinstance(quantity, (int, float)):
            raise ValueError("Quantity must be a numeric value (int or float).")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.quantity = quantity
        self.unit = unit

    def to_csv_row(self):
        """Converts the Ingredient object to a list for CSV writing."""
        return [self.name, self.quantity, self.unit]
    
# TODO: Implement __str__ method to display ingredient nicely
    def __str__(self):
        """Returns a nicely formatted string representation of the ingredient."""
        return f"{self.name}: {self.quantity} {self.unit}"


# Simple predefined recipes
# TODO: Add at least one additional recipe
RECIPES = {
    "Pap and Wors": {"Maize Meal": 250, "Wors": 500},
    "Spinach and Feta Salad": {"Spinach": 100, "Feta": 50, "Tomato": 1},
    "Creamy Chicken Mac and Cheese": {
        "Macaroni": 200,
        "Chicken Breast": 250,
        "Cheddar Cheese": 150,
        "Milk": 200,
        "Butter": 30,
        "Flour": 20
    }
}
