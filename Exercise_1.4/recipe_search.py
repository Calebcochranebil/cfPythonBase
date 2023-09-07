import pickle


def display_recipe(recipe):
    print("Recipe:", recipe["name"])
    print("Cooking time (min):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty:", recipe["difficulty"])
    print()


def search_ingredient(data):
    print("Available ingredients:")
    for index, ingredient in enumerate(data["all_ingredients"]):
        print(index, ingredient)
    print()

    try:
        ingredient_index = int(
            input("Enter the number of the ingredient you want to search for: "))
        ingredient_searched = data["all_ingredients"][ingredient_index]
    except (ValueError, IndexError):
        print("Incorrect input")
        return
    else:
        recipes_found = []
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                recipes_found.append(recipe)

        for recipe in recipes_found:
            display_recipe(recipe)


filename = input("Enter the filename where you've stored your recipes: ")

try:
    file = open(filename, "rb")
    data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist")
else:
    search_ingredient(data)
finally:
    print("Goodbye!")
    file.close()
