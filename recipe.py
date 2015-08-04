#!/usr/bin/python3
__author__ = 'Kellan Childers'

import os.path as pth
from json import dump, load


class Recipe:
    """Base class for making and containing recipes of ingredients."""
    def __init__(self):
        """Initialize a blank recipe."""
        self._ingredients = {}

    @staticmethod
    def create_from_file(filename):
        """Create a recipe using a previously-created file.

        :param filename: the name of the file to load
        :return: a new recipe read from the file
        """
        new_recipe = Recipe()
        return new_recipe.read_from_file(filename)

    def __iter__(self):
        return iter(self._ingredients)

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
            return self
        except KeyError:
            # If there isn't already an ingredient with this name, add it.
            self._ingredients[name] = (quantity, qualifier)
            return self
        except ValueError as e:
            raise e

    def get_ingredient_quantity(self, name):
        """Get the quantity of an ingredient.

        :param name: the name of the ingredient
        :return: a tuple of the quantity and qualifier of the ingredient
        """
        try:
            return self._ingredients[name]
        except KeyError:
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
        with open(pth.join(pth.dirname(__file__), filename), "r") as read_file:
            self._ingredients = load(read_file)
        return self

    def save_to_file(self, filename):
        """Save a recipe to a json file.

        :param filename: the name of the file to be written to (will lose all old data)
        :return: a reference to the recipe
        """
        with open(pth.join(pth.dirname(__file__), filename), "w") as write_file:
            dump(self._ingredients, write_file)
        return self

    def print_to_console(self):
        """Print all of recipe's ingredients."""
        for ingredient in self._ingredients:
            print(self.show_ingredient(ingredient))

    def save_as_list(self, filename, add_to=False):
        """Save the recipe as a human-readable list of ingredients.

        :param add_to: a boolean value determining if the file should be appended to (true)
         or rewritten (false, default)
        :return: a reference to the recipe
        """
        if add_to:
            with open(pth.join(pth.dirname(__file__), filename), "a") as write_file:
                for ingredient in self._ingredients:
                    write_file.write(self.show_ingredient(ingredient) + '\n')
        else:
            with open(pth.join(pth.dirname(__file__), filename), "w") as write_file:
                for ingredient in self._ingredients:
                    write_file.write(self.show_ingredient(ingredient) + '\n')
        return self

    def clear(self):
        """Remove all ingredients from the recipe.

        :return: a reference to the recipe
        """
        self._ingredients = {}
        return self

    def copy(self):
        """Create a copy of the recipe.

        :return: an identical copy of the recipe
        """
        new_recipe = Recipe()
        for ingredient, full_quantity in self._ingredients.items():
            new_recipe.add_ingredient(ingredient, full_quantity[0], full_quantity[1])
        return new_recipe

    def add_to(self, receiving_recipe):
        """Add every ingredient in recipe to the shopping list.

        :param receiving_recipe: the recipe to receive ingredients
        :return: a reference to the receiving recipe
        """
        for ingredient, full_quantity in self._ingredients.items():
            receiving_recipe.add_ingredient(ingredient, full_quantity[0], full_quantity[1])
        return receiving_recipe

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
    print("Copying recipe and clearing original\n")
    recipe1 = recipe.copy()
    recipe.clear()
    print("Original recipe:")
    recipe.print_to_console()
    print("\nNew recipe:")
    recipe1.print_to_console()
