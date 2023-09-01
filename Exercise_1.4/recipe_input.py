import pickle

# Function to take a recipe from the user


def take_recipe():
    # Prompt the user for the name and cooking time of the recipe
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = []

    # Prompt the user for ingredients until they enter "done"
    while True:
        ingredient = input(
            "Enter an ingredient (or enter 'done' if you have finished): "
        )
        if ingredient == "done":
            break
        else:
            ingredients.append(ingredient)

    # Create a recipe dictionary with name, cooking time, and ingredients
    recipe = {"name": name, "cooking_time": cooking_time,
              "ingredients": ingredients}

    # Calculate the difficulty level for the recipe using the calc_difficulty function
    difficulty = calc_difficulty(recipe)

    # Add the difficulty level to the recipe dictionary
    recipe["difficulty"] = difficulty

    # Return the completed recipe dictionary
    return recipe


# Function to calculate the difficulty level for each recipe based on cooking time and ingredient count


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


# Ask the user for the filename where the recipes are stored
filename = input("Enter the filename where you've stored your recipes: ")

try:
    # Try to open the file in binary read mode
    with open(filename, "rb") as file:
        # Attempt to load data from the file using pickle
        data = pickle.load(file)
        print("Recipes loaded successfully!")

# If the file doesn't exist, handle the FileNotFoundError
except FileNotFoundError:
    print("File doesn't exist - creating a new dictionary.")
    # Create a new data dictionary with empty recipe and ingredient lists
    data = {"recipes_list": [], "all_ingredients": []}

# Handle other unexpected exceptions
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
    # Create a new data dictionary with empty recipe and ingredient lists

else:
    # Close the file if it was successfully opened
    file.close()

# Regardless of whether the file exists or not, extract the recipe list and ingredient list from the data dictionary
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]


# Get the number of recipes to add from the user
n = int(input("How many recipes would you like to add? "))

# Take recipes and append to recipes_list
for i in range(n):
    recipe = take_recipe()

    # Update all_ingredients with new ingredients
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    # Add recipe to recipes_list
    recipes_list.append(recipe)

# Save the recipes_list and all_ingredients to a dictionary
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Save the dictionary to a user-specified file
filename = input("Enter the filename where you'd like to store your recipes: ")
with open(filename, "wb") as file:
    pickle.dump(data, file)
    print("Recipes saved successfully!")
    file.close()
