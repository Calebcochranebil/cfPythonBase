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