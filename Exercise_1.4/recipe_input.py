import pickle


def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = []
    while True:
        ingredient = input(
            "Enter an ingredient (or enter 'done' if you have finished): "
        )
        if ingredient == "done":
            break
        else:
            ingredients.append(ingredient)
    recipe = {"name": name, "cooking_time": cooking_time,
              "ingredients": ingredients}
    difficulty = calc_difficulty(recipe)
    recipe["difficulty"] = difficulty
    return recipe


def calc_difficulty(recipe):
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    return difficulty


filename = input("Enter the filename where you've stored your recipes: ")

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
        print("Recipes loaded successfully!")
except FileNotFoundError:
    print("File doesn't exist - creating a new dictionary.")
    data = {"recipes_list": [], "all_ingredients": []}
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")

recipes_list = data["recipes_list"]
all_ingredients = data["all_ingredients"]

n = int(input("How many recipes would you like to add? "))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

filename = input("Enter the filename where you'd like to store your recipes: ")

try:
    with open(filename, "wb") as file:
        pickle.dump(data, file)
        print("Recipes saved successfully!")
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except PermissionError:
    print(f"Error: You don't have permission to write to '{filename}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
