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
