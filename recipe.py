__author__ = 'Kellan Childers'


class Recipe:
    def __init__(self):
        self.ingredients = {}

    def add_ingredient(self, name, quantity, qualifier):
        try:
            current = self.ingredients[name]
            if current[1] == qualifier:
                new_quantity = current[0] + quantity
                self.ingredients[name] = (new_quantity, qualifier)
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

    def show_ingredient(self, name):
        return str(self.get_ingredient_quantity(name)[0]) + ' ' + \
            str(self.get_ingredient_quantity(name)[1] + ' ' + str(name))

if __name__ == "__main__":
    print("Demonstrating recipe.py\n")
    recipe = Recipe()
    print("Adding an ingredient to recipe, then showing.")
    recipe.add_ingredient("onions", 3, "whole")
    print("There are {}.\n".format(recipe.show_ingredient("onions")))
    print("Adding more ingredients to the recipe, then showing.\n")
    print("Adding shallots.")
    recipe.add_ingredient("shallots", 5, "chopped")
    print("There are {0} and {1}.\n".format(recipe.show_ingredient("onions"), recipe.show_ingredient("shallots")))
    print("Attempting to add diced onions.")
    try:
        recipe.add_ingredient("onions", 3, "diced")
    except ValueError as e:
        print(e.args[0])
