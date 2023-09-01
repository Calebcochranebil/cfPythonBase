import pickle


# Function to display the details of a recipe
def display_recipe(recipe):
    print("Recipe:", recipe["name"])
    print("Cooking time (min):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty:", recipe["difficulty"])
    print()


# Function to search for recipes containing a particular ingredient
def search_ingredient(data):
    # Print the list of available ingredients for reference
    print("Available ingredients:")
    for index, ingredient in enumerate(data["all_ingredients"]):
        print(index, ingredient)
    print()

    try:
        # Ask the user for the ingredient they want to search for by selecting a number
        ingredient_index = int(
            input("Enter the number of the ingredient you want to search for: "))
        # Retrieve the selected ingredient from the list
        ingredient_searched = data["all_ingredients"][ingredient_index]
    except (ValueError, IndexError):
        # Handle incorrect input (non-integer or out-of-range selection)
        print("Incorrect input")
        return
    else:
        # Search for recipes containing the selected ingredient
        recipes_found = []
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                recipes_found.append(recipe)

        # Display the recipes found that contain the selected ingredient
        for recipe in recipes_found:
            display_recipe(recipe)

# This is a hypothetical function used within search_ingredient to display recipes.
# You would need to define the display_recipe function separately based on your requirements.
# Example:
# def display_recipe(recipe):
#     print(f"Recipe: {recipe['name']}")
#     print(f"Cooking Time: {recipe['cooking_time']} minutes")
#     print(f"Ingredients: {', '.join(recipe['ingredients'])}")
#     print(f"Difficulty: {recipe['difficulty']}")
#     print()


# ask user for the name of the file containing the recipes
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
