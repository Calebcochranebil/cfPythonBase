# Initializing Lists
recipes_list = []
ingredients_list = []


# Function to take recipe inputs from the user
def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time: "))
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
    return recipe


# Get the number of recipes to be added from the user
n = int(input("How many recipes would you like to add? "))

# Collect recipes and update the ingredients list
for i in range(n):
    recipe = take_recipe()

    # Update ingredients_list with new ingredients
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    # Add recipe to recipes_list
    recipes_list.append(recipe)

# Calculate the difficulty level for each recipe based on cooking time and ingredient count
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    else:
        recipe["difficulty"] = "Hard"

# Display the details of each recipe
for recipe in recipes_list:
    print("Recipe:", recipe["name"])
    print("Cooking time (min):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty:", recipe["difficulty"])
    print()

# Display the list of ingredients available a to z
print("Ingredients Available Across All Recipes")
print("----------------------------------------")

ingredients_list.sort()

for ingredient in ingredients_list:
    print(ingredient)


//test