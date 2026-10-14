import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from database import DATABASE_NAME


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def get_food_items():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, food_name, selling_price, cost_price
        FROM food_items
        ORDER BY id
    """)

    foods = cursor.fetchall()

    connection.close()

    return foods


def get_sales_data():

    connection = get_connection()

    query = """
        SELECT
            sales.id,
            food_items.food_name,
            sales.sale_date,
            sales.quantity,
            food_items.selling_price,
            food_items.cost_price
        FROM sales
        JOIN food_items
        ON sales.food_id = food_items.id
        ORDER BY sales.sale_date DESC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return df


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Canteen Billing System and Analysis"
)

root.geometry("1100x700")

root.minsize(900, 600)


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#F4F6F8"
SIDEBAR_COLOR = "#1F2937"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#111827"
BUTTON_COLOR = "#2563EB"


root.configure(
    bg=BG_COLOR
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="CANTEEN BILLING SYSTEM AND ANALYSIS",
    font=("Arial", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title_label.pack(
    pady=20
)


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR_COLOR,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ============================================================
# CONTENT AREA
# ============================================================

content = tk.Frame(
    root,
    bg=BG_COLOR
)

content.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# CLEAR CONTENT
# ============================================================

def clear_content():

    for widget in content.winfo_children():

        widget.destroy()


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    clear_content()

    heading = tk.Label(
        content,
        text="Dashboard",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )

    heading.pack(
        pady=20
    )


    foods = get_food_items()

    df = get_sales_data()


    # Food count
    food_count = len(foods)


    # Today's sales
    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    if not df.empty:

        today_df = df[
            df["sale_date"] == today
        ]

        today_quantity = int(
            today_df["quantity"].sum()
        )

        total_sales = (
            today_df["quantity"]
            * today_df["selling_price"]
        ).sum()

    else:

        today_quantity = 0
        total_sales = 0


    # Total profit
    if not df.empty:

        total_profit = (
            df["quantity"]
            * (
                df["selling_price"]
                - df["cost_price"]
            )
        ).sum()

    else:

        total_profit = 0


    # Cards frame
    cards_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    cards_frame.pack(
        pady=20
    )


    create_card(
        cards_frame,
        "🍔 Food Items",
        str(food_count),
        0
    )

    create_card(
        cards_frame,
        "📦 Today's Quantity",
        str(today_quantity),
        1
    )

    create_card(
        cards_frame,
        "💰 Today's Sales",
        "₹" + str(
            round(total_sales, 2)
        ),
        2
    )

    create_card(
        cards_frame,
        "📈 Total Profit",
        "₹" + str(
            round(total_profit, 2)
        ),
        3
    )


    # Today's sales table
    table_frame = tk.Frame(
        content,
        bg=CARD_COLOR
    )

    table_frame.pack(
        padx=30,
        pady=20,
        fill="both",
        expand=True
    )


    tk.Label(
        table_frame,
        text="Recent Sales",
        font=("Arial", 16, "bold"),
        bg=CARD_COLOR
    ).pack(
        pady=10
    )


    columns = (
        "Food",
        "Date",
        "Quantity",
        "Sales",
        "Profit"
    )


    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=120
        )


    if not df.empty:

        for _, row in df.head(10).iterrows():

            sales_amount = (
                row["quantity"]
                * row["selling_price"]
            )

            profit = (
                row["quantity"]
                * (
                    row["selling_price"]
                    - row["cost_price"]
                )
            )

            tree.insert(
                "",
                "end",
                values=(
                    row["food_name"],
                    row["sale_date"],
                    row["quantity"],
                    f"₹{sales_amount:.2f}",
                    f"₹{profit:.2f}"
                )
            )


    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


# ============================================================
# CARD
# ============================================================

def create_card(
    parent,
    title,
    value,
    column
):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        width=180,
        height=110,
        relief="solid",
        borderwidth=1
    )

    card.grid(
        row=0,
        column=column,
        padx=10
    )

    card.pack_propagate(False)


    tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=10
    )


    tk.Label(
        card,
        text=value,
        font=("Arial", 18, "bold"),
        bg=CARD_COLOR,
        fg=BUTTON_COLOR
    ).pack()


# ============================================================
# ADD FOOD
# ============================================================

def show_add_food():

    clear_content()


    tk.Label(
        content,
        text="Add Food Item",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR
    ).pack(
        pady=30
    )


    form = tk.Frame(
        content,
        bg=CARD_COLOR,
        padx=30,
        pady=30
    )

    form.pack()


    tk.Label(
        form,
        text="Food Name",
        bg=CARD_COLOR
    ).grid(
        row=0,
        column=0,
        pady=10,
        padx=10
    )


    food_entry = tk.Entry(
        form,
        width=30
    )

    food_entry.grid(
        row=0,
        column=1
    )


    tk.Label(
        form,
        text="Selling Price",
        bg=CARD_COLOR
    ).grid(
        row=1,
        column=0,
        pady=10,
        padx=10
    )


    selling_entry = tk.Entry(
        form,
        width=30
    )

    selling_entry.grid(
        row=1,
        column=1
    )


    tk.Label(
        form,
        text="Cost Price",
        bg=CARD_COLOR
    ).grid(
        row=2,
        column=0,
        pady=10,
        padx=10
    )


    cost_entry = tk.Entry(
        form,
        width=30
    )

    cost_entry.grid(
        row=2,
        column=1
    )


    def save_food():

        food_name = food_entry.get().strip()

        selling_price = selling_entry.get().strip()

        cost_price = cost_entry.get().strip()


        if (
            food_name == ""
            or selling_price == ""
            or cost_price == ""
        ):

            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )

            return


        try:

            selling_price = float(
                selling_price
            )

            cost_price = float(
                cost_price
            )


            if selling_price < 0 or cost_price < 0:

                raise ValueError


        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid prices."
            )

            return


        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO food_items
            (
                food_name,
                selling_price,
                cost_price
            )
            VALUES (?, ?, ?)
        """, (
            food_name,
            selling_price,
            cost_price
        ))

        connection.commit()

        connection.close()


        messagebox.showinfo(
            "Success",
            "Food added successfully!"
        )


        food_entry.delete(
            0,
            tk.END
        )

        selling_entry.delete(
            0,
            tk.END
        )

        cost_entry.delete(
            0,
            tk.END
        )


    tk.Button(
        form,
        text="ADD FOOD",
        command=save_food,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        width=20
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=20
    )


# ============================================================
# VIEW FOOD
# ============================================================

def show_food():

    clear_content()


    tk.Label(
        content,
        text="Food Items",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR
    ).pack(
        pady=20
    )


    columns = (
        "ID",
        "Food Name",
        "Selling Price",
        "Cost Price"
    )


    tree = ttk.Treeview(
        content,
        columns=columns,
        show="headings"
    )


    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=150
        )


    foods = get_food_items()


    for food in foods:

        tree.insert(
            "",
            "end",
            values=(
                food[0],
                food[1],
                f"₹{food[2]:.2f}",
                f"₹{food[3]:.2f}"
            )
        )


    tree.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=20
    )


# ============================================================
# ADD SALE
# ============================================================

def show_add_sale():

    clear_content()


    tk.Label(
        content,
        text="Add Today's Sale",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR
    ).pack(
        pady=30
    )


    form = tk.Frame(
        content,
        bg=CARD_COLOR,
        padx=30,
        pady=30
    )

    form.pack()


    tk.Label(
        form,
        text="Select Food",
        bg=CARD_COLOR
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )


    foods = get_food_items()


    food_names = []

    food_ids = {}


    for food in foods:

        food_names.append(
            food[1]
        )

        food_ids[food[1]] = food[0]


    food_combo = ttk.Combobox(
        form,
        values=food_names,
        width=28,
        state="readonly"
    )

    food_combo.grid(
        row=0,
        column=1
    )


    tk.Label(
        form,
        text="Quantity Sold",
        bg=CARD_COLOR
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    quantity_entry = tk.Entry(
        form,
        width=30
    )

    quantity_entry.grid(
        row=1,
        column=1
    )


    tk.Label(
        form,
        text="Date",
        bg=CARD_COLOR
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )


    date_label = tk.Label(
        form,
        text=datetime.now().strftime(
            "%Y-%m-%d"
        ),
        bg=CARD_COLOR
    )

    date_label.grid(
        row=2,
        column=1
    )


    def save_sale():

        selected_food = food_combo.get()

        quantity = quantity_entry.get()


        if selected_food == "":

            messagebox.showerror(
                "Error",
                "Please select food."
            )

            return


        try:

            quantity = int(quantity)

            if quantity <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
            )

            return


        food_id = food_ids[
            selected_food
        ]


        sale_date = datetime.now().strftime(
            "%Y-%m-%d"
        )


        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO sales
            (
                food_id,
                sale_date,
                quantity
            )
            VALUES (?, ?, ?)
        """, (
            food_id,
            sale_date,
            quantity
        ))


        connection.commit()

        connection.close()


        messagebox.showinfo(
            "Success",
            "Sale saved successfully!"
        )


        quantity_entry.delete(
            0,
            tk.END
        )


    tk.Button(
        form,
        text="SAVE SALE",
        command=save_sale,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        width=20
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=20
    )


# ============================================================
# VIEW SALES
# ============================================================

def show_sales():

    clear_content()


    tk.Label(
        content,
        text="Sales Records",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR
    ).pack(
        pady=20
    )


    columns = (
        "ID",
        "Food",
        "Date",
        "Quantity",
        "Sales",
        "Profit"
    )


    tree = ttk.Treeview(
        content,
        columns=columns,
        show="headings"
    )


    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=120
        )


    df = get_sales_data()


    for _, row in df.iterrows():

        sales_amount = (
            row["quantity"]
            * row["selling_price"]
        )

        profit = (
            row["quantity"]
            * (
                row["selling_price"]
                - row["cost_price"]
            )
        )


        tree.insert(
            "",
            "end",
            values=(
                row["id"],
                row["food_name"],
                row["sale_date"],
                row["quantity"],
                f"₹{sales_amount:.2f}",
                f"₹{profit:.2f}"
            )
        )


    tree.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )


# ============================================================
# DEMAND PREDICTION
# ============================================================

def show_prediction():

    clear_content()


    tk.Label(
        content,
        text="Demand Prediction",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR
    ).pack(
        pady=20
    )


    foods = get_food_items()


    food_names = []

    food_ids = {}


    for food in foods:

        food_names.append(
            food[1]
        )

        food_ids[food[1]] = food[0]


    form = tk.Frame(
        content,
        bg=CARD_COLOR,
        padx=30,
        pady=20
    )

    form.pack()


    tk.Label(
        form,
        text="Select Food",
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    food_combo = ttk.Combobox(
        form,
        values=food_names,
        state="readonly",
        width=30
    )

    food_combo.pack(
        pady=5
    )


    result_label = tk.Label(
        content,
        text="",
        font=("Arial", 14),
        bg=BG_COLOR,
        justify="left"
    )

    result_label.pack(
        pady=30
    )


    def calculate_prediction():

        selected_food = food_combo.get()


        if selected_food == "":

            messagebox.showerror(
                "Error",
                "Please select food."
            )

            return


        food_id = food_ids[
            selected_food
        ]


        connection = get_connection()

        cursor = connection.cursor()


        cursor.execute("""
            SELECT quantity
            FROM sales
            WHERE food_id = ?
            ORDER BY sale_date
        """, (food_id,))


        rows = cursor.fetchall()

        connection.close()


        if len(rows) == 0:

            result_label.config(
                text="No sales data available."
            )

            return


        sales = np.array([
            row[0]
            for row in rows
        ])


        average_demand = np.mean(
            sales
        )


        recent_sales = sales[-3:]


        recent_demand = np.mean(
            recent_sales
        )


        predicted_demand = (
            average_demand * 0.6
            + recent_demand * 0.4
        )


        recommended_quantity = int(
            predicted_demand * 1.10
        )


        result = (
            f"Food: {selected_food}\n\n"
            f"Previous Sales: {sales.tolist()}\n\n"
            f"Average Demand: "
            f"{average_demand:.2f}\n\n"
            f"Recent Demand: "
            f"{recent_demand:.2f}\n\n"
            f"Predicted Demand: "
            f"{predicted_demand:.2f}\n\n"
            f"Recommended Quantity: "
            f"{recommended_quantity}"
        )


        result_label.config(
            text=result
        )


    tk.Button(
        form,
        text="PREDICT DEMAND",
        command=calculate_prediction,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        width=25
    ).pack(
        pady=15
    )


# ============================================================
# FINANCE
# ============================================================

def show_finance():

    clear_content()


    tk.Label(
        content,
        text="Finance Report",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR
    ).pack(
        pady=30
    )


    df = get_sales_data()


    if df.empty:

        total_sales = 0
        total_cost = 0
        total_profit = 0

    else:

        total_sales = (
            df["quantity"]
            * df["selling_price"]
        ).sum()


        total_cost = (
            df["quantity"]
            * df["cost_price"]
        ).sum()


        total_profit = (
            total_sales
            - total_cost
        )


    if total_sales > 0:

        profit_margin = (
            total_profit
            / total_sales
        ) * 100

    else:

        profit_margin = 0


    report = tk.Frame(
        content,
        bg=CARD_COLOR,
        padx=60,
        pady=40
    )

    report.pack()


    tk.Label(
        report,
        text="TOTAL SALES",
        font=("Arial", 12),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text=f"₹{total_sales:.2f}",
        font=("Arial", 22, "bold"),
        bg=CARD_COLOR,
        fg=BUTTON_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text="TOTAL COST",
        font=("Arial", 12),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text=f"₹{total_cost:.2f}",
        font=("Arial", 22, "bold"),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text="TOTAL PROFIT",
        font=("Arial", 12),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text=f"₹{total_profit:.2f}",
        font=("Arial", 22, "bold"),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text="PROFIT MARGIN",
        font=("Arial", 12),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


    tk.Label(
        report,
        text=f"{profit_margin:.2f}%",
        font=("Arial", 22, "bold"),
        bg=CARD_COLOR
    ).pack(
        pady=5
    )


# ============================================================
# DEMAND CHART
# ============================================================

def show_chart():

    df = get_sales_data()


    if df.empty:

        messagebox.showinfo(
            "No Data",
            "No sales data available."
        )

        return


    grouped = (
        df.groupby("food_name")[
            "quantity"
        ].sum()
    )


    plt.figure(
        figsize=(8, 5)
    )


    grouped.plot(
        kind="bar"
    )


    plt.title(
        "Food Demand"
    )

    plt.xlabel(
        "Food"
    )

    plt.ylabel(
        "Quantity Sold"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# SIDEBAR BUTTON
# ============================================================

def sidebar_button(
    text,
    command
):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=SIDEBAR_COLOR,
        fg="white",
        activebackground="#374151",
        activeforeground="white",
        relief="flat",
        font=("Arial", 11),
        anchor="w",
        padx=20
    )

    button.pack(
        fill="x",
        pady=3
    )


# ============================================================
# SIDEBAR MENU
# ============================================================

tk.Label(
    sidebar,
    text="SMART\nCANTEEN",
    font=("Arial", 17, "bold"),
    bg=SIDEBAR_COLOR,
    fg="white"
).pack(
    pady=25
)


sidebar_button(
    "🏠  Dashboard",
    show_dashboard
)

sidebar_button(
    "🍔  Add Food",
    show_add_food
)

sidebar_button(
    "📋  Food Items",
    show_food
)

sidebar_button(
    "📦  Add Sale",
    show_add_sale
)

sidebar_button(
    "📊  Sales Records",
    show_sales
)

sidebar_button(
    "🔮  Demand Prediction",
    show_prediction
)

sidebar_button(
    "💰  Finance",
    show_finance
)

sidebar_button(
    "📈  Demand Chart",
    show_chart
)


# ============================================================
# START DASHBOARD
# ============================================================

show_dashboard()


# ============================================================
# RUN APPLICATION
# ============================================================

root.mainloop()