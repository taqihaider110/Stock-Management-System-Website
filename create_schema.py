import sqlite3

def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Create the Companies table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE NOT NULL,
            company_representative TEXT NOT NULL,
            contact TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """
    )

    # Create the Products table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            company_id INTEGER NOT NULL,
            brand TEXT NOT NULL,
            pieces_per_carton INTEGER NOT NULL,
            price_carton REAL NOT NULL,
            selling_price_carton REAL NOT NULL,
            current_cartons INTEGER NOT NULL,
            alarming_stock_level INTEGER NOT NULL
        )
    """
    )

    # Create the Purchase table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS purchase (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            purchased_cartons INTEGER NOT NULL,
            purchase_date DATE NOT NULL,
            purchase_amount REAL NOT NULL
        )
    """
    )

    # Create the Clients table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            client_since DATE NOT NULL,
            address TEXT NOT NULL
        )
    """
    )

    # Create the Sales table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            quantity_sold_cartons REAL NOT NULL,
            sale_total REAL NOT NULL,
            sold_date DATE NOT NULL
        )
    """
    )

    # Create the Users Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            session_id TEXT,
            session_expiration DATE 
        )
    """
    )

    """ To calculate the profit you made from selling 12 cartons of a product at Rs. 4240 each with a 6 percent margin per carton, you can use the following formula:

        Profit = (Selling Price - Cost Price) * Quantity

        Here's how you can calculate it step by step:

        1. Calculate the cost price per carton (without margin):
        Cost Price per Carton = Selling Price per Carton / (1 + Margin Percentage)
        Cost Price per Carton = 4240 / (1 + 6/100) = 4000

        2. Calculate the total cost for 12 cartons:
        Total Cost = Cost Price per Carton * Quantity = 4000 * 12 = Rs. 48,000

        3. Calculate the profit:
        Profit = (Selling Price per Carton - Cost Price per Carton) * Quantity
        Profit = (4240 - 4000) * 12 = Rs. 240 * 12 = Rs. 2,880

        So, the profit you get from selling 12 cartons of the product is Rs. 2,880."""

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
