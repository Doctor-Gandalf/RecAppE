#!/usr/bin/python3
__author__ = 'Kellan Childers'

from json import dump, load


class Recipe:
    def __init__(self):
        self._ingredients = {}

    def add_ingredient(self, name, quantity, qualifier):
        try:
            current = self._ingredients[name]
            if current[1] == qualifier:
                new_quantity = current[0] + quantity
                self._ingredients[name] = (new_quantity, qualifier)
            else:
                raise ValueError("Attempting to add two different quantities failed.")
        except KeyError:
            # If there isn't already an ingredient with this name, add it.
            self._ingredients[name] = (quantity, qualifier)

    def get_ingredient_quantity(self, name):
        if self._ingredients[name]:
            return self._ingredients[name]
        else:
            raise ValueError("No ingredient by that name.")

    def show_ingredient(self, name):
        return str(self.get_ingredient_quantity(name)[0]) + ' ' + \
            str(self.get_ingredient_quantity(name)[1] + ' ' + str(name))

    def read_from_file(self, filename):
        """Read a file and load the recipe from it.

        :param filename: the name of the file to be read
        :return: a reference to the recipe
        """
        with open(filename, "r") as read_file:
            self._ingredients = load(read_file)
        return self

    def save_to_file(self, filename):
        """Save a recipe to a json file.

        :param filename: the name of the file to be written to (will lose all old data)
        :return: a reference to the recipe
        """
        with open(filename, "w") as write_file:
            dump(self._ingredients, write_file)
        return self

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
