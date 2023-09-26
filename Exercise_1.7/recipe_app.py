from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker, declarative_base


# Helper functions
def is_alpha_space_or_hyphen(s):
    return all(c.isalpha() or c.isspace() or c == "-" for c in s)


# Create engine
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Create base
Base = declarative_base()


# Create table
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # define __repr__ method
    def __repr__(self):
        return f"Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})"

    # define __str__ method
    def __str__(self):
        return f"Recipe: {self.name}\nIngredients: {self.ingredients}\nCooking time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}\n"

    # Calculate difficulty based on cooking time and number of ingredients
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(", "))
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    # Return ingredients as a list
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        else:
            return self.ingredients.split(", ")


# create_all() method to create tables
Base.metadata.create_all(engine)

# Create recipe
def create_recipe():
    try:
        # Ask user for recipe name
        name = input("\nEnter the name of the recipe: ")
        # Check that name is alphanumeric and less than 50 characters
        while not is_alpha_space_or_hyphen(name) or len(name) > 50:
            print()
            print(
                "Please enter a recipe name that contains only letters, spaces and hyphens and is less than 50 characters long"
            )
            name = input("\nEnter the name of the recipe: ")

        # Ask user for cooking time
        cooking_time = input("\nEnter the cooking time in minutes: ")
        # Check that cooking time is numeric
        while not cooking_time.isnumeric():
            print()
            print("Please enter a cooking time that is numeric")
            cooking_time = input("\nEnter the cooking time in minutes: ")

        # Convert cooking_time to integer
        cooking_time = int(cooking_time)

        # Ask user how many ingredients they want to add
        number_of_ingredients = int(
            input("\nHow many ingredients do you want to add? ")
        )

        # Create an empty list to store the ingredients
        ingredients = []

        # Ask user to enter each ingredient
        for i in range(number_of_ingredients):
            ingredient = input(f"\nEnter ingredient {i+1} or type 'done' to finish: ")
            # Check that ingredient is alphabetical
            while not is_alpha_space_or_hyphen(ingredient) and ingredient != "done":
                print()
                print(
                    "Please enter an ingredient using only letters, spaces and hyphens"
                )
                ingredient = input(
                    f"\nEnter ingredient {i+1} or type 'done' to finish: "
                )
            # Add ingredient to list
            if ingredient != "done":
                ingredients.append(ingredient)

        # Join ingredients list into a string separated by commas
        ingredients = ", ".join(ingredients)

        # Create recipe_entry object
        recipe_entry = Recipe(
            name=name,
            ingredients=ingredients,
            cooking_time=cooking_time,
        )

        # Calculate the difficulty of the recipe
        recipe_entry.calculate_difficulty()

        # Add recipe to session
        session.add(recipe_entry)

        # Commit changes
        session.commit()

        print()
        print("Recipe created successfully!")
        print()
    except Exception as e:
        print()
        print("There was an error creating the recipe")
        print(e)
        print()

# View all recipes
def view_all_recipes():
    # Retrieve all recipes from database
    recipes = session.query(Recipe).all()
    # If there are no recipes, inform user and exit function
    if len(recipes) == 0:
        print()
        print("There are no recipes in the database")
        print()
        return None
    else:
        print()
        print("Here are all the recipes in the database:")
    # Loop through recipes and print each recipe
    for recipe in recipes:
        print()
        print(recipe)


# Search by ingredient
def search_by_ingredient():
    # Retrieve all ingredients from database and store in a list
    if session.query(Recipe).count() == 0:
        print()
        print("There are no recipes in the database")
        print()
        return None
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for result in results:
        ingredients = result[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    # Display all ingredients to user
    print()
    print("Here are all the ingredients in the database:")
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}. {ingredient}")
    print()
    # Ask user to enter the numbers of the ingredients they want to search for
    search_ingredients = input(
        "Enter the numbers of the ingredients you want to search for separated by spaces: "
    ).split()
    # Validate user input
    for i in search_ingredients:
        if not i.isnumeric() or int(i) > len(all_ingredients):
            print()
            print("Please enter a valid number")
            print()
            return None
    # Retrieve recipes that contain the ingredients
    search_ingredients = [all_ingredients[int(i) - 1] for i in search_ingredients]
    conditions_all = []
    conditions_any = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions_all.append(Recipe.ingredients.like(like_term))
        conditions_any.append(Recipe.ingredients.like(like_term))
    recipes_all = session.query(Recipe).filter(*conditions_all).all()
    recipes_any = session.query(Recipe).filter(or_(*conditions_any)).all()

    print()
    print("Here are the recipes that contain all those ingredients:")
    if len(recipes_all) == 0:
        print()
        print("None")
    for recipe in recipes_all:
        print()
        print(recipe)
    print()

    print("Here are the recipes that contain at least one of those ingredients:")
    if len(recipes_any) == 0:
        print()
        print("None")
    for recipe in recipes_any:
        print()
        print(recipe)
    print()


# Edit recipe
def edit_recipe():
    if session.query(Recipe).count() == 0:
        print()
        print("There are no recipes in the database")
        print()
        return None
    results = session.query(Recipe.id, Recipe.name).all()
    print()
    print("Here are the recipes in the database:")
    print()
    for result in results:
        print(f"{result[0]}. {result[1]}")
    print()
    recipe_id = input("Enter the number of the recipe you want to edit: ")
    while not recipe_id.isnumeric() or int(recipe_id) > len(results):
        print()
        print("Please enter a valid number")
        recipe_id = input("Enter the number of the recipe you want to edit: ")
    # Retrieve the recipe to edit and display the recipe, but only the name, ingredients and cooking_time.
    recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()
    print()
    print("Here is the recipe you want to edit:")
    print()
    print(recipe_to_edit)
    print()
    print("Which recipe attribute do you want to edit?")
    print()
    print("1. Name")
    print("2. Ingredients")
    print("3. Cooking time")
    print()
    attribute = input("Enter the number of the recipe attribute you want to edit: ")
    while not attribute.isnumeric() or int(attribute) > 3:
        print()
        print("Please enter a valid number")
        attribute = input("Enter the number of the recipe attribute you want to edit: ")
    if attribute == "1":
        print()
        new_name = input("Enter the new name: ")
        while not new_name.isalnum() or len(new_name) > 50:
            print()
            print(
                "Please enter a recipe name that is alphanumeric and less than 50 characters"
            )
            new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute == "2":
        print()
        num_ingredients = input("How many ingredients do you want to add? ")
        new_ingredients = []
        for i in range(int(num_ingredients)):
            print()
            ingredient = input(f"Enter ingredient {i+1} or type 'done' to finish: ")
            while not is_alpha_space_or_hyphen(ingredient) and ingredient != "done":
                print()
                print(
                    "Please enter an ingredient using only letters, spaces or hyphens"
                )
                ingredient = input(f"Enter ingredient {i+1} or type 'done' to finish: ")
                if ingredient != "done":
                    new_ingredients.append(ingredient)
        new_ingredients = ", ".join(new_ingredients)
        recipe_to_edit.ingredients = new_ingredients
    elif attribute == "3":
        print()
        new_cooking_time = input("Enter the new cooking time in minutes: ")
        while not new_cooking_time.isnumeric():
            print()
            print("Please enter a cooking time that is numeric")
            new_cooking_time = input("Enter the new cooking time in minutes: ")
        recipe_to_edit.cooking_time = int(new_cooking_time)
    recipe_to_edit.calculate_difficulty()
    session.commit()
    print()
    print("Recipe edited successfully!")
    print()


# Delete recipe
def delete_recipe():
    if session.query(Recipe).count() == 0:
        print()
        print("There are no recipes in the database")
        print()
        return None
    results = session.query(Recipe.id, Recipe.name).all()
    print()
    print("Here are the recipes in the database:")
    print()
    for result in results:
        print(f"{result[0]}. {result[1]}")
    print()
    recipe_id = input("Enter the number of the recipe you want to delete: ")
    while not recipe_id.isnumeric() or int(recipe_id) > len(results):
        print()
        print("Please enter a valid number")
        recipe_id = input("Enter the number of the recipe you want to delete: ")
    recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()
    # confirm deletion
    print()
    print("Are you sure you want to delete this recipe?")
    print(recipe_to_delete)
    print()
    confirm = input("Enter 'y' for yes or 'n' for no: ")
    while confirm != "y" and confirm != "n":
        print()
        print("Please enter 'y' for yes or 'n' for no")
        confirm = input("Enter 'y' for yes or 'n' for no: ")
    if confirm == "n":
        print()
        print("Recipe not deleted")
        print()
        return None
    session.delete(recipe_to_delete)
    session.commit()
    print()
    print("Recipe deleted successfully!")
    print()


def main_menu():
    while True:  # Start a loop that continues until the user chooses to exit
        print()
        print("MAIN MENU")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("6. Exit")
        print()
        choice = input("Enter the number of the action you want to perform: ")
        while not choice.isnumeric() or int(choice) > 6:
            print()
            print("Please enter a valid number")
            choice = input("Enter the number of the action you want to perform: ")
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredient()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "6":
            print()
            print("Goodbye!")
            session.close()
            engine.dispose()
            break


# Call the main_menu function
if __name__ == "__main__":
    main_menu()