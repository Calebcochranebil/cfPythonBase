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
