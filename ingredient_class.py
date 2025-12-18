class InsufficientStockError(Exception):
    """Raised when inventory quantity is too low for a recipe."""
    pass


class Ingredient:
    """Represents a single item in the kitchen inventory."""

    def __init__(self, name, quantity, unit):
        #add Exception handling
        try:
            self.quantity = float(quantity)
        except (TypeError, ValueError):
            raise ValueError("Quantity must be numeric.") from None

        self.name = name
        self.unit = unit

    def to_csv_row(self):
        """Converts the Ingredient object to a list for CSV writing."""
        return [self.name, self.quantity, self.unit]

    def __str__(self):
        """Nice representation for display."""
        return f"{self.name}: {self.quantity} {self.unit}"



RECIPES = {
    "Pap and Wors": {
        "Maize Meal": 250,
        "Wors": 500
    },
    "Spinach and Feta Salad": {
        "Spinach": 100,
        "Feta": 50,
        "Tomato": 1
    },

    "Chicken Wrap": {
    "Chicken": 150,
    "Tortilla Wrap": 1,
    "Carrot": 30,
    "Green Pepper": 30,
    "Onion": 20,
    "Lettuce": 40,
    "Sauce": 20
}
}
