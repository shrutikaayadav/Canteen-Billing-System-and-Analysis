import sqlite3
from datetime import datetime
from database import DATABASE_NAME


# ==========================================
# ADD FOOD
# ==========================================

def add_food(
    food_name,
    selling_price,
    cost_price
):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO food_items
        (food_name, selling_price, cost_price)
        VALUES (?, ?, ?)
    """, (
        food_name,
        selling_price,
        cost_price
    ))

    connection.commit()
    connection.close()

    print("Food item added successfully!")


# ==========================================
# VIEW FOOD
# ==========================================

def view_food():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            food_name,
            selling_price,
            cost_price
        FROM food_items
    """)

    foods = cursor.fetchall()

    connection.close()

    print("\n========== FOOD ITEMS ==========")

    if len(foods) == 0:

        print("No food items found.")

    else:

        for food in foods:

            print(
                "ID:", food[0],
                "| Food:", food[1],
                "| Selling Price: ₹", food[2],
                "| Cost Price: ₹", food[3]
            )


# ==========================================
# ADD SALE
# ==========================================

def add_sale(
    food_id,
    sale_date,
    quantity
):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sales
        (food_id, sale_date, quantity)
        VALUES (?, ?, ?)
    """, (
        food_id,
        sale_date,
        quantity
    ))

    connection.commit()
    connection.close()

    print("Sale added successfully!")


# ==========================================
# VIEW SALES
# ==========================================

def view_sales():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sales.id,
            food_items.food_name,
            sales.sale_date,
            sales.quantity
        FROM sales
        JOIN food_items
        ON sales.food_id = food_items.id
    """)

    sales = cursor.fetchall()

    connection.close()

    print("\n========== SALES ==========")

    if len(sales) == 0:

        print("No sales found.")

    else:

        for sale in sales:

            print(
                "Sale ID:", sale[0],
                "| Food:", sale[1],
                "| Date:", sale[2],
                "| Quantity:", sale[3]
            )


# ==========================================
# DELETE FOOD
# ==========================================

def delete_food(food_id):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM food_items
        WHERE id = ?
    """, (food_id,))

    connection.commit()
    connection.close()

    print("Food item deleted successfully!")


# ==========================================
# USER INPUT MENU
# ==========================================

if __name__ == "__main__":

    while True:

        print("\n")
        print("================================")
        print("      SMART CANTEEN SYSTEM")
        print("================================")

        print("1. Add Food")
        print("2. View Food")
        print("3. Add Sale")
        print("4. View Sales")
        print("5. Delete Food")
        print("6. Exit")

        choice = input(
            "Enter your choice: "
        )


        # ----------------------------------
        # ADD FOOD
        # ----------------------------------

        if choice == "1":

            food_name = input(
                "Enter food name: "
            )

            selling_price = float(
                input(
                    "Enter selling price: ₹"
                )
            )

            cost_price = float(
                input(
                    "Enter cost price: ₹"
                )
            )

            add_food(
                food_name,
                selling_price,
                cost_price
            )


        # ----------------------------------
        # VIEW FOOD
        # ----------------------------------

        elif choice == "2":

            view_food()


        # ----------------------------------
        # ADD SALE
        # ----------------------------------

        elif choice == "3":

            view_food()

            food_id = int(
                input(
                    "Enter food ID: "
                )
            )

            quantity = int(
                input(
                    "Enter quantity sold: "
                )
            )

            sale_date = datetime.now().strftime(
                "%Y-%m-%d"
            )

            add_sale(
                food_id,
                sale_date,
                quantity
            )


        # ----------------------------------
        # VIEW SALES
        # ----------------------------------

        elif choice == "4":

            view_sales()


        # ----------------------------------
        # DELETE FOOD
        # ----------------------------------

        elif choice == "5":

            view_food()

            food_id = int(
                input(
                    "Enter food ID to delete: "
                )
            )

            delete_food(food_id)


        # ----------------------------------
        # EXIT
        # ----------------------------------

        elif choice == "6":

            print(
                "Thank you for using "
                "Smart Canteen!"
            )

            break


        else:

            print("Invalid choice!")