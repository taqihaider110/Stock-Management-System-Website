import sqlite3
import uuid
from datetime import datetime, timedelta
import constant as const

DATABASE = "inventory.db"


def connect_db(db):
    return sqlite3.connect(db)


# Company Related Functions


def add_new_company(company):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO COMPANIES (company_name, company_representative, contact, address) VALUES (?,?,?,?)",
            (
                company["company_name"],
                company["company_representative"],
                company["contact"],
                company["address"],
            ),
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Company added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Company already exists"}


def update_company(company):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE COMPANIES SET company_name=?, company_representative=?, contact=?, address=? WHERE company_id=?",
            (
                company["company_name"],
                company["company_representative"],
                company["contact"],
                company["address"],
                company["company_id"],
            ),
        )

        conn.commit()
        conn.close()
        return {"success": True, "message": "Company updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Error updating company"}


def get_all_companies():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM COMPANIES")
    all_companies = cursor.fetchall()
    conn.close()

    if all_companies:
        all_companies = [
            {
                "company_id": company["company_id"],
                "company_name": company["company_name"],
                "company_representative": company["company_representative"],
                "contact": company["contact"],
                "address": company["address"],
            }
            for company in all_companies
        ]

    return all_companies


def get_one_company(company_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM COMPANIES WHERE company_id = ?", (company_id,))
    company = cursor.fetchone()
    conn.close()
    if company:
        return dict(company)


def delete_company(company_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM COMPANIES WHERE company_id = ?", (company_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Company deleted successfully"}
    except Exception as e:
        print(f"Error deleting company: {str(e)}")
        return {"success": False, "message": "Error deleting company"}


# Products Related Functions


def add_new_product(product):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO PRODUCTS (product_name, company_id, brand, pieces_per_carton, price_carton,selling_price_carton,current_cartons,alarming_stock_level) VALUES (?,?,?,?,?,?,?,?)",
            (
                product["product_name"],
                product["company_id"],
                product["brand"],
                product["pieces_per_carton"],
                product["price_carton"],
                product["selling_price_carton"],
                0,
                product["alarming_stock_level"],
            ),
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Product added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Product already exists"}


def update_product(product):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()
        print(product)

        cursor.execute(
            "UPDATE products SET product_name=?, company_id=?, brand=?, pieces_per_carton=?, price_carton=?,selling_price_carton=?,current_cartons=?, alarming_stock_level=? WHERE product_id=?",
            (
                product["product_name"],
                product["company_id"],
                product["brand"],
                product["pieces_per_carton"],
                product["price_carton"],
                product["selling_price_carton"],
                product["current_cartons"],
                product["alarming_stock_level"],
                product["product_id"],
            ),
        )

        conn.commit()
        conn.close()
        return {"success": True, "message": "Product updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Error updating product"}


def get_all_products():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCTS")
    all_products = cursor.fetchall()
    conn.close()

    if all_products:
        all_products = [
            {
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "company_id": product["company_id"],
                "brand": product["brand"],
                "pieces_per_carton": product["pieces_per_carton"],
                "price_carton": product["price_carton"],
                "selling_price_carton": product["selling_price_carton"],
                "current_cartons": product["current_cartons"],
                "alarming_stock_level": product["alarming_stock_level"],
                "company_name": get_one_company(product["company_id"])["company_name"],
            }
            for product in all_products
        ]

    return all_products


def get_one_product(product_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCTS WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        product_dtl = {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "company_id": product["company_id"],
            "brand": product["brand"],
            "pieces_per_carton": product["pieces_per_carton"],
            "price_carton": product["price_carton"],
            "selling_price_carton": product["selling_price_carton"],
            "current_cartons": product["current_cartons"],
            "alarming_stock_level": product["alarming_stock_level"],
        }
        return product_dtl


def delete_product(product_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUCTS WHERE product_id = ?", (product_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Product deleted successfully"}
    except Exception as e:
        print(f"Error deleting product: {str(e)}")
        return {"success": False, "message": "Error deleting product"}


# Users Related Functions


def add_new_user(username, password):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, session_id, session_expiration) VALUES (?,?,?,?)",
            (
                username,
                password,
                None,
                None,
            ),
        )

        return {"success": True, "message": "User added successfully"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": "User already exists!"}
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def get_one_user(username, password):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? and password = ? ", (username, password)
    )
    user = cursor.fetchone()
    if user:
        session_id = str(uuid.uuid4())
        session_expiration = datetime.now() + timedelta(minutes=const.expiry_in_minutes)
        cursor.execute(
            "UPDATE users SET session_id = ? WHERE username = ? and password = ? ",
            (session_id, username, password),
        )
        cursor.execute(
            "UPDATE users SET session_expiration = ? WHERE username = ? and password = ? ",
            (session_expiration, username, password),
        )
        conn.commit()
        cursor.close()
        conn.close()

        user_dtl = {
            "user_id": user["user_id"],
            "username": user["username"],
            "password": user["password"],
            "session_id": session_id,
            "session_expiration": session_expiration,
        }
        return user_dtl


def get_user_by_session_id(session_id: str):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE session_id = ?", (session_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_dtl = {
            "user_id": user["user_id"],
            "username": user["username"],
            "password": user["password"],
            "session_id": user["session_id"],
            "session_expiration": datetime.strptime(
                user["session_expiration"], "%Y-%m-%d %H:%M:%S.%f"
            ),
        }
        return user_dtl


def delete_session(session_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users set session_id = NULL WHERE session_id= ?", (session_id,)
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Session removed successfully"}
    except Exception as e:
        print(f"Error deleting session: {str(e)}")
        return {"success": False, "message": "Error deleting session"}


# purchases Related Function


def add_new_purchase(purchase):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO purchase (
            
                product_id,
                purchased_cartons,
                purchase_date,
                purchase_amount
            ) 
            VALUES (?, ?, ?, ?)
            """,
            (
                purchase["product_id"],
                purchase["purchased_cartons"],
                purchase["purchase_date"],
                purchase["purchase_amount"],
            ),
        )
        cursor.execute(
            f"""UPDATE PRODUCTS SET current_cartons = current_cartons + {purchase["purchased_cartons"]}  where product_id = {purchase["product_id"]} """
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "purchase added successfully"}
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return {"success": False, "message": "purchase already exists"}
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": f"Database Error: {str(e)}"}


def get_one_purchase(purchase_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM purchase WHERE purchase_id = ?", (purchase_id,))
    purchase = cursor.fetchone()
    conn.close()

    if purchase:
        purchase_dtl = {
            "purchase_id": purchase["purchase_id"],
            "product_id": purchase["product_id"],
            "purchased_cartons": purchase["purchased_cartons"],
            "purchase_date": purchase["purchase_date"],
            "purchase_amount": purchase["purchase_amount"],
        }
        return purchase_dtl


def update_purchase(purchase):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT purchased_cartons FROM purchase WHERE purchase_id = ?",
            (purchase["purchase_id"],),
        )
        purchased_cartons = cursor.fetchone()

        cursor.execute(
            "UPDATE purchase SET product_id=?, purchased_cartons=?, purchase_date=?,purchase_amount=? WHERE purchase_id=?",
            (
                purchase["product_id"],
                purchase["purchased_cartons"],
                purchase["purchase_date"],
                purchase["purchase_amount"],
                purchase["purchase_id"],
            ),
        )

        cursor.execute(
            f"""UPDATE PRODUCTS SET current_cartons = current_cartons - {purchased_cartons[0]} + {purchase["purchased_cartons"]}  where product_id = {purchase["product_id"]} """
        )

        conn.commit()
        conn.close()
        return {"success": True, "message": "Purchase updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Error updating Purchase"}


def get_all_purchases():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """SELECT

                p.purchase_id,
                pr.product_name ,
                pr.pieces_per_carton,
                p.purchased_cartons,
                pr.price_carton ,
                p.purchase_amount,
                p.purchase_date,
                c.company_name
            FROM
                PURCHASE p
            LEFT JOIN products pr
            on
                p.product_id = pr.product_id
            LEFT JOIN companies c
            on
                c.company_id = pr.company_id """
    )
    all_purchases = cursor.fetchall()
    conn.close()

    if all_purchases:
        all_purchases = [dict(purchase) for purchase in all_purchases]

    return all_purchases


def delete_purchase(purchase_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PURCHASE WHERE purchase_id = ?", (purchase_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "purchase deleted successfully"}
    except Exception as e:
        print(f"Error deleting purchase: {str(e)}")
        return {"success": False, "message": "Error deleting purchase"}


# Sales Related Function


def get_all_sales():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """SELECT   s.sale_id,
                    p.product_name,
                    cl.client_name,
                    p.selling_price_carton,
                    s.quantity_sold_cartons,
                    s.sale_total,
                    s.sold_date 
        FROM SALES s
            LEFT JOIN products P ON p.product_id = s.product_id
            LEFT JOIN clients cl ON cl.client_id = s.client_id"""
    )
    all_sales = cursor.fetchall()
    conn.close()

    if all_sales:
        all_sales = [
            {
                "sale_id": sale["sale_id"],
                "product_name": sale["product_name"],
                "client_name": sale["client_name"],
                "quantity_sold_cartons": sale["quantity_sold_cartons"],
                "selling_price_carton": sale["selling_price_carton"],
                "sale_total": sale["sale_total"],
                "sold_date": sale["sold_date"],
            }
            for sale in all_sales
        ]

    return all_sales


# my code
def count_product():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
    count = cursor.fetchone()[0]  # fetchone() returns a tuple, get the first item
    conn.close()
    return count


def count_purchase():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM PURCHASE")
    count = cursor.fetchone()[0]  # fetchone() returns a tuple, get the first item
    conn.close()
    return count


def count_sales():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM SALES")
    count = cursor.fetchone()[0]  # fetchone() returns a tuple, get the first item
    conn.close()
    return count


def count_alarming_alerts():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM PRODUCTS WHERE CURRENT_CARTONS <=  ALARMING_STOCK_LEVEL"
    )
    count = cursor.fetchone()[0]  # fetchone() returns a tuple, get the first item
    conn.close()
    return count


def add_new_sale(sale):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sales (
                product_id,
                client_id,
                quantity_sold_cartons,
                sale_total,
                sold_date
            ) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                sale["product_id"],
                sale["client_id"],
                sale["quantity_sold_cartons"],
                sale["sale_total"],
                sale["sale_date"],
            ),
        )

        cursor.execute(
            """
            UPDATE products 
            SET current_cartons = current_cartons - ?  
            WHERE product_id = ?
            """,
            (sale["quantity_sold_cartons"], sale["product_id"]),
        )

        conn.commit()
        conn.close()
        return {"success": True, "message": "Sale added successfully"}
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return {"success": False, "message": "Sale already exists"}
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": f"Database Error: {str(e)}"}


def get_one_sale(sale_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """SELECT s.sale_id,p.product_id,cl.client_id,p.selling_price_carton,s.quantity_sold_cartons,s.sale_total,s.sold_date FROM SALES s
            LEFT JOIN products P ON p.product_id = s.product_id
            LEFT JOIN clients cl ON cl.client_id = s.client_id where sale_id=?""",
        (sale_id,),
    )
    sale = cursor.fetchone()
    conn.close()

    if sale:
        return dict(sale)
    else:
        return None


def update_sale(sale):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT quantity_sold_cartons FROM SALES WHERE sale_id = ?",
            (sale["sale_id"],),
        )
        old_quantity_sold_cartons = cursor.fetchone()

        cursor.execute(
            """
            UPDATE SALES
            SET
                product_id = ?,
                client_id = ?,
                quantity_sold_cartons = ?,
                sale_total = ?,
                sold_date = ?
            WHERE sale_id = ?
            """,
            (
                sale["product_id"],
                sale["client_id"],
                sale["quantity_sold_cartons"],
                sale["sale_total"],
                sale["sold_date"],
                sale["sale_id"],
            ),
        )

        cursor.execute(
            f"""UPDATE PRODUCTS SET current_cartons = current_cartons + {old_quantity_sold_cartons[0]} - {sale["quantity_sold_cartons"]}  where product_id = {sale["product_id"]} """
        )
        
        conn.commit()
        conn.close()
        return {"success": True, "message": "sale updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Error updating sale"}


def delete_sales(sale_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SALES WHERE sale_id = ?", (sale_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "sales deleted successfully"}
    except Exception as e:
        print(f"Error deleting sales: {str(e)}")
        return {"success": False, "message": "Error deleting sales"}


# Client Related Functions


def add_new_client(client):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO CLIENTS (client_name, contact, client_since, address) VALUES (?,?,?,?)",
            (
                client["client_name"],
                client["contact"],
                client["client_since"],
                client["address"],
            ),
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "client added successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "client already exists"}


def update_client(client):
    try:
        conn = connect_db(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE CLIENTS SET client_name=?, contact=?, client_since=?, address=? WHERE client_id=?",
            (
                client["client_name"],
                client["contact"],
                client["client_since"],
                client["address"],
                client["client_id"],
            ),
        )

        conn.commit()
        conn.close()
        return {"success": True, "message": "client updated successfully"}
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return {"success": False, "message": "Error updating client"}


def get_all_clients():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENTS")
    all_clients = cursor.fetchall()
    conn.close()

    if all_clients:
        all_clients = [
            {
                "client_id": client["client_id"],
                "client_name": client["client_name"],
                "contact": client["contact"],
                "client_since": client["client_since"],
                "address": client["address"],
            }
            for client in all_clients
        ]

    return all_clients


def get_one_client(client_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENTS WHERE client_id = ?", (client_id,))
    client = cursor.fetchone()
    conn.close()

    if client:
        return dict(client)


def delete_client(client_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CLIENTS WHERE client_id = ?", (client_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "client deleted successfully"}
    except Exception as e:
        print(f"Error deleting client: {str(e)}")
        return {"success": False, "message": "Error deleting client"}


if __name__ == "__main__":
    pass
    # Example sale data

    # new_client = {
    #     "client_name": "John Doe",
    #     "contact": "john.doe@example.com",
    #     "client_since": "2024-06-25",
    #     "address": "123 Main St, Anytown, USA",
    # }
    # print(add_new_client(new_client))
    # sale_data = {
    #     "sale_id": 1,
    #     "product_name": "Biryani Masala",
    #     "product_id": 3,
    #     "client_name": "Client X",
    #     "quantity_sold_cartons": 10,
    #     "selling_price_per_carton": 20.0,
    #     "cost_price_per_carton": 15.0,
    #     "margin_per_carton": 5.0,
    #     "total_value": 200.0,
    #     "profit_amount": 50.0,
    #     "date": "2024-06-24",
    # }

    # # Call add_new_sale function with the sample data
    # result = add_new_sale(sale_data)
    # print(result)

    # new_purchase = {
    #     "product_name": "Surf Excel",
    #     "product_id": 3,
    #     "company_id": 1,
    #     "available_cartons": 100,
    #     "rate_current_purchase_cartons": 15.0,
    #     "alarming_stock_level": 10,
    #     "last_amount_added_cartons": 50,
    #     "date_amount_added": "2024-06-15",
    #     "old_available_cartons": 150,
    #     "rate_old_purchase_cartons": 12.0
    # }

    # result = add_new_purchase(new_purchase)
    # print(result)

    # get_purchase = {
    #         "purchase_id": 2,
    #         # "product_id": 3,
    #         # "purchased_cartons": 120,
    #         # "purchased_date": "2024-06-16",
    #         # "purchased_amount": 190,
    # }
    # result = get_one_purchase(1)
    # print(result)

    # updated_purchase = {
    #     "purchase_id": 2,  # Provide the ID of the purchase you want to update
    #     "product_id": 3,
    #     "purchased_cartons": 120,
    #     "purchase_date": "2024-06-16",
    #     "purchase_amount": 190,
    # }

    # result = update_purchase(updated_purchase)
    # print(result)

    # purchase_id = 1
    # result = delete_purchase(purchase_id)
    # print (result)
    # user = {
    #     "username": "imran",
    #     "password": "1234",
    #     "session_id": None,
    #     "session_expiration": None,
    # }
    # add_new_user(user)
    # user = get_one_user("Taqi","1234")
    # print(user)
    # print(get_all_companies())
    # print(get_one_company(6))
