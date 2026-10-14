import sqlite3
import numpy as np

from database import DATABASE_NAME


def predict_demand(food_id):

    # Connect to database
    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    # Get previous sales
    cursor.execute("""
        SELECT quantity
        FROM sales
        WHERE food_id = ?
        ORDER BY sale_date
    """, (food_id,))

    rows = cursor.fetchall()

    connection.close()


    # Check if sales exist
    if len(rows) == 0:

        print(
            "No sales data available "
            "for this food."
        )

        return


    # Convert database values to NumPy array
    sales = np.array([
        row[0]
        for row in rows
    ])


    # Average demand
    average_demand = np.mean(
        sales
    )


    # Recent sales
    recent_sales = sales[-3:]

    recent_demand = np.mean(
        recent_sales
    )


    # Prediction
    predicted_demand = (
        average_demand * 0.6
        + recent_demand * 0.4
    )


    # 10% safety stock
    recommended_quantity = int(
        predicted_demand * 1.10
    )


    print("\n")
    print("==============================")
    print("       DEMAND PREDICTION")
    print("==============================")

    print(
        "Previous sales:",
        sales
    )

    print(
        "Average demand:",
        round(
            average_demand,
            2
        )
    )

    print(
        "Recent demand:",
        round(
            recent_demand,
            2
        )
    )

    print(
        "Predicted demand:",
        round(
            predicted_demand,
            2
        )
    )

    print(
        "Recommended quantity:",
        recommended_quantity
    )


if __name__ == "__main__":

    print("\n===== FOOD ITEMS =====")

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, food_name
        FROM food_items
    """)

    foods = cursor.fetchall()

    connection.close()


    for food in foods:

        print(
            "ID:",
            food[0],
            "|",
            food[1]
        )


    food_id = int(
        input(
            "\nEnter food ID for prediction: "
        )
    )


    predict_demand(food_id)