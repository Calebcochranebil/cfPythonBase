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