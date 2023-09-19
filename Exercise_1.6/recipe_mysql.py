import mysql.connector

# Connect to the database
conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="password")

# Create a cursor
cursor = conn.cursor()

# Create a database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Use the database
cursor.execute("USE task_database")

# Create a table called Recipes
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Recipes ("
    "id INT AUTO_INCREMENT PRIMARY KEY,"
    "name VARCHAR(50),"
    "ingredients VARCHAR(255),"
    "cooking_time INT,"
    "difficulty VARCHAR(20)"
    ")"
)

# Main menu function.
def main_menu(conn, cursor):
    while True:
        print("\n-------------------------------------")
        print("Main Menu:")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. View all recipes")
        print("6. Exit")
        print("-------------------------------------\n")

        try:
            selection = int(input("Your choice: "))
            if selection == 1:
                create_recipe(conn, cursor)
            elif selection == 2:
                search_recipe(cursor)
            elif selection == 3:
                update_recipe(conn, cursor)
            elif selection == 4:
                delete_recipe(conn, cursor)
            elif selection == 5:
                view_recipes(cursor)
            elif selection == 6:
                conn.commit()
                conn.close()
                exit()
            else:
                print()
                print("Please select a valid option")
        except ValueError:
            print()
            print("Please select a valid option")

# Create a new recipe.
def create_recipe(conn, cursor):
    ingredients = []
    name = input("\nEnter the name of the recipe: ")
    cooking_time = int(input("\nEnter the cooking time in minutes: "))
    ingredient = input("Enter an ingredient or type 'done' to finish: ")
    while ingredient != "done":
        ingredients.append(ingredient)
        ingredient = input("Enter an ingredient or type 'done' to finish: ")
    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients = ", ".join(ingredients)
    cursor.execute(
        "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)",
        (name, ingredients, cooking_time, difficulty),
    )
    conn.commit()
    print()
    print("Recipe created successfully!")

    # Calculate the difficulty of a recipe based on its cooking time and number of ingredients.
def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"

# Search for a recipe based on an ingredient.
def search_recipe(cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []
    for row in results:
        for ingredient in row:
            ingredients_list = ingredient.split(
                ", "
            )  # Split the ingredients string into a list
            for item in ingredients_list:
                if item not in all_ingredients:
                    all_ingredients.append(item)
    print()
    print("Available ingredients:")
    print()
    for i in range(len(all_ingredients)):
        print(f"{i+1}. {all_ingredients[i]}")
    while True:
        try:
            ingredient_choice = int(
                input("\nEnter the number of the ingredient you want to search for: ")
            )
            if ingredient_choice not in range(1, len(all_ingredients) + 1):
                print()
                print("Please select a valid option")
            else:
                break
        except ValueError:
            print()
            print("Please select a valid option")
    search_ingredient = all_ingredients[ingredient_choice - 1]
    cursor.execute(
        "SELECT name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s",
        (f"%{search_ingredient}%",),
    )
    results = cursor.fetchall()
    if len(results) == 0:
        print()
        print("No recipes found")
    else:
        print()
        print("Search results:")
        for row in results:
            print()
            print(f"Name: {row[0]}")
            print(f"Ingredients: {row[1]}")
            print(f"Cooking time: {row[2]} minutes")
            print(f"Difficulty: {row[3]}")