import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_FOLDER = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)

DATABASE_NAME = os.path.join(
    DATABASE_FOLDER,
    "canteen.db"
)


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    # Food table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            selling_price REAL NOT NULL,
            cost_price REAL NOT NULL
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (food_id) REFERENCES food_items(id)
        )
    """)

    connection.commit()

    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()