__author__ = 'Kellan Childers'


class Recipe:
    def __init__(self):
        self.ingredients = {}

    def add_ingredient(self, name, quantity, qualifier):
        try:
            current = self.ingredients[name]
            if current[1] == qualifier:
                current[0] += quantity
            else:
                raise ValueError("Attempting to add two different quantities failed.")
        except KeyError:
            # If there isn't already an ingredient with this name, add it.
            self.ingredients[name] = (quantity, qualifier)

    def get_ingredient_quantity(self, name):
        if self.ingredients[name]:
            return self.ingredients[name]
        else:
            raise ValueError("No ingredient by that name.")
