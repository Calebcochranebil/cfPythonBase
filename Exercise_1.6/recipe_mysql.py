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