import sqlite3
import pandas as pd

from database import DATABASE_NAME


def load_sales_data():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    query = """
    SELECT
        food_items.food_name,
        sales.sale_date,
        sales.quantity,
        food_items.selling_price,
        food_items.cost_price
    FROM sales
    JOIN food_items
    ON sales.food_id = food_items.id
    ORDER BY sales.sale_date
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return df


def calculate_finance(df):

    # Sales amount
    df["total_sales"] = (
        df["quantity"]
        * df["selling_price"]
    )

    # Cost amount
    df["total_cost"] = (
        df["quantity"]
        * df["cost_price"]
    )

    # Profit
    df["profit"] = (
        df["total_sales"]
        - df["total_cost"]
    )

    return df


if __name__ == "__main__":

    df = load_sales_data()

    if df.empty:

        print(
            "No sales data available."
        )

    else:

        df = calculate_finance(df)

        print("\n===== SALES ANALYSIS =====")

        print(df.to_string(
            index=False
        ))

        print(
            "\nTotal Sales: ₹",
            round(
                df["total_sales"].sum(),
                2
            )
        )

        print(
            "Total Cost: ₹",
            round(
                df["total_cost"].sum(),
                2
            )
        )

        print(
            "Total Profit: ₹",
            round(
                df["profit"].sum(),
                2
            )
        )
        if df["total_sales"].sum() > 0:
    profit_margin = (
        df["profit"].sum()
        / df["total_sales"].sum()
    ) * 100
else:
    profit_margin = 0

print(
    "Profit Margin:",
    round(profit_margin, 2),
    "%"
)