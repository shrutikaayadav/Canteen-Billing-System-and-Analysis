from analysis import (
    load_sales_data,
    calculate_finance
)


def generate_finance_report():

    df = load_sales_data()

    if df.empty:

        print(
            "No sales data available."
        )

        return


    df = calculate_finance(df)


    total_sales = (
        df["total_sales"].sum()
    )

    total_cost = (
        df["total_cost"].sum()
    )

    total_profit = (
        df["profit"].sum()
    )


    if total_sales > 0:

        profit_margin = (
            total_profit
            / total_sales
        ) * 100

    else:

        profit_margin = 0


    print("\n")
    print("==============================")
    print("        FINANCE REPORT")
    print("==============================")

    print(
        "Total Sales   : ₹",
        round(total_sales, 2)
    )

    print(
        "Total Cost    : ₹",
        round(total_cost, 2)
    )

    print(
        "Total Profit  : ₹",
        round(total_profit, 2)
    )

    print(
        "Profit Margin :",
        round(profit_margin, 2),
        "%"
    )


if __name__ == "__main__":

    generate_finance_report()