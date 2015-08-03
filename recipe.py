#!/usr/bin/python3
__author__ = 'Kellan Childers'

import os
from json import dump, load


class Recipe:
    """Base class for making and containing recipes of ingredients."""
    def __init__(self):
        """Initialize a blank recipe."""
        self._ingredients = {}

    def add_ingredient(self, name, quantity, qualifier):
        """Add ingredient to the recipe, or update quantity of ingredient.

        :param name: the name of the ingredient
        :param quantity: the quantity of the ingredient
        :param qualifier: the type of quantity of the ingredient (ounces, pounds, etx)
        :return: a reference to the recipe
        """
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
        finally:
            return self

    def get_ingredient_quantity(self, name):
        """Get the quantity of an ingredient.

        :param name: the name of the ingredient
        :return: a tuple of the quantity and qualifier of the ingredient
        """
        if self._ingredients[name]:
            return self._ingredients[name]
        else:
            raise ValueError("No ingredient by that name.")

    def show_ingredient(self, name):
        """Get an ingredient and show it as a string."""
        return str(self.get_ingredient_quantity(name)[0]) + ' ' + \
            str(self.get_ingredient_quantity(name)[1] + ' ' + str(name))

    def read_from_file(self, filename):
        """Read a file and load the recipe from it.

        :param filename: the name of the file to be read
        :return: a reference to the recipe
        """
        with open(os.path.join(os.path.dirname(__file__), "saved_recipes", filename), "r") as read_file:
            self._ingredients = load(read_file)
        return self

    def save_to_file(self, filename):
        """Save a recipe to a json file.

        :param filename: the name of the file to be written to (will lose all old data)
        :return: a reference to the recipe
        """
        with open(os.path.join(os.path.dirname(__file__), "saved_recipes", filename), "w") as write_file:

            dump(self._ingredients, write_file)
        return self

    def print(self):
        """Print all of recipe's ingredients."""
        for ingredient in self._ingredients:
            print(self.show_ingredient(ingredient))

    def clear(self):
        """Remove all ingredients from the recipe.

        :return: a reference to self
        """
        self._ingredients = {}
        return self

    def copy(self):
        new_recipe = Recipe()
        for ingredient in self._ingredients:
            quantity, quality = self.get_ingredient_quantity(ingredient)
            new_recipe.add_ingredient(ingredient, quantity, quality)
        return new_recipe

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
    print("Attempting to add diced onions.\n")
    try:
        recipe.add_ingredient("onions", 3, "diced")
    except ValueError as e:
        print("Unable to add diced onions.\n")
    print("Copying recipe and clearing original\n")
    recipe1 = recipe.copy()
    recipe.clear()
    print("Original recipe:")
    recipe.print()
    print("\nNew recipe:")
    recipe1.print()

