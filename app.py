from flask import Flask, render_template, request, jsonify, send_from_directory
import json, uuid
from datetime import datetime, timedelta
from db_functions import *
from constant import *
import traceback

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True


def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def is_valid_session(session_id):
    user = get_user_by_session_id(session_id)

    if user:
        username = user["username"]
        expiration_time = user["session_expiration"]
        if datetime.now() < expiration_time:
            return True, username
    return False, False


@app.route("/", methods=["GET"])
def index():
    return render_template("login.html", message="Please login to start session!")


@app.route("/register", methods=["GET"])
def register():
    return render_template("signup.html", message="Please add account!")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = get_one_user(username, password)
    if user:
        return render_template(
            "dashboard.html",
            session_id=user["session_id"],
            username=username,
            page_name="dashboard",
            product_count=count_product(),
            purchase_count=count_purchase(),
            sales_count=count_sales(),
            alarming_alerts_count=count_alarming_alerts(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    response = add_new_user(username, password)
    if response["success"]:
        return render_template(
            "login.html", message="Account Added Successfully! Please Login."
        )
    else:
        return render_template("signup.html", message=response["message"])


@app.route("/dashboard", methods=["GET"])
def dashboard():
    session_id = request.cookies.get("session_id")
    valid_id, username = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "dashboard.html",
            session_id=session_id,
            username=username,
            page_name=request.endpoint,
            product_count=count_product(),
            purchase_count=count_purchase(),
            sales_count=count_sales(),
            alarming_alerts_count=count_alarming_alerts(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.headers["Session-Id"]
    valid_id, _ = is_valid_session(session_id)
    if valid_id:
        delete_session(session_id)
        return jsonify({"message": "User logged Out Successfully!"})
    return jsonify({"message": "Unauthorized Access Denied!"})


# Companies
@app.route("/add_company", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        try:
            company = request.get_json()
            response = add_new_company(company)
            return jsonify(response)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        session_id = request.cookies.get("session_id")
        valid_id, username = is_valid_session(session_id)
        if valid_id:
            return render_template(
                "add_company.html",
                session_id=session_id,
                username=username,
                page_name="Add New Company",
            )
        else:
            return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/companies", methods=["GET", "POST"])
def companies():
    session_id = request.cookies.get("session_id")
    valid_id, username = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "companies.html",
            session_id=session_id,
            username=username,
            page_name=request.endpoint,
            companies=get_all_companies(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/edit_company", methods=["GET", "POST"])
def edit_company():
    if request.method == "GET":
        try:
            company_id = int(request.args.get("company_id"))
            session_id = request.cookies.get("session_id")

            company_to_edit = get_one_company(company_id)

            verified = is_valid_session(session_id)

            if not verified:
                return render_template(
                    "login.html", message="Unauthorized Access Denied!"
                )

            return render_template(
                "edit_company.html",
                request=request,
                session_id=request.cookies.get("session_id"),
                user=verified,
                company_to_edit=company_to_edit,
                page_name="Edit Company",
            )

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        company = request.get_json()
        response = update_company(company)
        return jsonify(response)


@app.route("/remove_company", methods=["POST"])
def remove_company():
    try:
        session_id = request.cookies.get("session_id")
        company_id = int(request.args.get("company_id"))
        verified = is_valid_session(session_id)

        if not verified:
            return jsonify({"success": False, "message": "Unauthorized Access Denied!"})

        result = delete_company(company_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# Clients
@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        try:
            client = request.get_json()
            response = add_new_client(client)
            return jsonify(response)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        session_id = request.cookies.get("session_id")
        valid_id, username = is_valid_session(session_id)
        if valid_id:
            return render_template(
                "add_client.html",
                session_id=session_id,
                username=username,
                page_name="Add New Client",
            )
        else:
            return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/clients", methods=["GET", "POST"])
def clients():
    session_id = request.cookies.get("session_id")
    valid_id, username = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "client.html",
            session_id=session_id,
            username=username,
            page_name=request.endpoint,
            clients=get_all_clients(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/edit_client", methods=["GET", "POST"])
def edit_client():
    if request.method == "GET":
        try:
            client_id = int(request.args.get("client_id"))
            session_id = request.cookies.get("session_id")

            client_to_edit = get_one_client(client_id)

            verified = is_valid_session(session_id)

            if not verified:
                return render_template(
                    "login.html", message="Unauthorized Access Denied!"
                )

            return render_template(
                "edit_client.html",
                request=request,
                session_id=request.cookies.get("session_id"),
                user=verified,
                client_to_edit=client_to_edit,
                page_name="Edit client",
            )

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        client = request.get_json()
        response = update_client(client)
        return jsonify(response)


@app.route("/remove_client", methods=["POST"])
def remove_client():
    try:
        session_id = request.cookies.get("session_id")
        client_id = int(request.args.get("client_id"))
        verified = is_valid_session(session_id)

        if not verified:
            return jsonify({"success": False, "message": "Unauthorized Access Denied!"})

        result = delete_client(client_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# Products
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        try:
            product = request.get_json()
            response = add_new_product(product)
            return jsonify(response)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        session_id = request.cookies.get("session_id")
        valid_id, username = is_valid_session(session_id)
        if valid_id:
            companies = (
                get_all_companies()
            )  # Assuming you have a function to get all companies
            return render_template(
                "add_product.html",
                session_id=session_id,
                username=username,
                page_name="Add New Product",
                companies=companies,
            )
        else:
            return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/products", methods=["GET", "POST"])
def products():
    session_id = request.cookies.get("session_id")
    valid_id, username = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "products.html",
            session_id=session_id,
            username=username,
            page_name=request.endpoint,
            products=get_all_products(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/edit_product", methods=["GET", "POST"])
def edit_product():
    if request.method == "GET":
        try:
            product_id = int(request.args.get("product_id"))
            session_id = request.cookies.get("session_id")

            product_to_edit = get_one_product(product_id)
            companies = (
                get_all_companies()
            )  # Assuming you have a function to get all companies

            verified = is_valid_session(session_id)

            if not verified:
                return render_template(
                    "login.html", message="Unauthorized Access Denied!"
                )

            return render_template(
                "edit_product.html",
                session_id=request.cookies.get("session_id"),
                user=verified,
                product_to_edit=product_to_edit,
                companies=companies,
                page_name="Edit Product",
            )

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        product = request.get_json()
        response = update_product(product)
        return jsonify(response)


@app.route("/remove_product", methods=["POST"])
def remove_product():
    try:
        session_id = request.cookies.get("session_id")
        product_id = int(request.args.get("product_id"))
        verified = is_valid_session(session_id)

        if not verified:
            return jsonify({"success": False, "message": "Unauthorized Access Denied!"})

        result = delete_product(product_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(
        app.root_path, "./favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


# purchases Related Routes


@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    session_id = request.cookies.get("session_id")
    valid_id, username = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "purchases.html",
            session_id=session_id,
            username=username,
            page_name=request.endpoint,
            purchases=get_all_purchases(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/edit_purchase", methods=["GET", "POST"])
def edit_purchase():
    if request.method == "GET":
        try:
            purchase_id = int(request.args.get("purchase_id"))
        except ValueError:
            return jsonify({"success": False, "message": "Invalid purchase_id"})

        session_id = request.cookies.get("session_id")
        verified = is_valid_session(session_id)
        if not verified:
            return render_template("login.html", message="Unauthorized Access Denied!")

        purchase_to_edit = get_one_purchase(purchase_id)
        if purchase_to_edit is None:
            return render_template("error.html", message="Purchase not found!")

        products = get_all_products()
        return render_template(
            "edit_purchase.html",
            session_id=session_id,
            user=verified,
            purchase_to_edit=purchase_to_edit,
            products=products,
            page_name="Edit Purchase",
        )
    else:
        purchase = request.get_json()
        response = update_purchase(purchase)
        return jsonify(response)


@app.route("/add_purchase", methods=["GET", "POST"])
def add_purchase():
    if request.method == "POST":
        try:
            purchase = request.get_json()
            print(purchase)
            response = add_new_purchase(purchase)
            return jsonify(response)

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        session_id = request.cookies.get("session_id")
        valid_id, username = is_valid_session(session_id)
        if valid_id:
            return render_template(
                "add_purchase.html",
                session_id=session_id,
                username=username,
                page_name="Add New purchase",
                companies=get_all_companies(),
                products=get_all_products(),
            )
        else:
            return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/remove_purchase", methods=["POST"])
def remove_purchase():
    try:
        session_id = request.cookies.get("session_id")
        purchase_id = int(request.args.get("purchase_id"))
        verified = is_valid_session(session_id)

        if not verified:
            return jsonify({"success": False, "message": "Unauthorized Access Denied!"})

        result = delete_purchase(purchase_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# Sales Related Routes


@app.route("/sales", methods=["GET", "POST"])
def sales():
    session_id = request.cookies.get("session_id")
    valid_id, username = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "sales.html",
            session_id=session_id,
            username=username,
            page_name=request.endpoint,
            sales=get_all_sales(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/edit_sale", methods=["GET", "POST"])
def edit_sale():
    if request.method == "GET":
        try:
            sale_id = int(request.args.get("sale_id"))
        except ValueError:
            return jsonify({"success": False, "message": "Invalid sale_id"})

        session_id = request.cookies.get("session_id")
        verified = is_valid_session(session_id)
        if not verified:
            return render_template("login.html", message="Unauthorized Access Denied!")

        sale_to_edit = get_one_sale(sale_id)
        if sale_to_edit is None:
            return render_template("error.html", message="sale not found!")

        products = get_all_products()
        clients = get_all_clients()
        
        return render_template(
            "edit_sale.html",
            session_id=session_id,
            user=verified,
            sale_to_edit=sale_to_edit,
            products=products,
            clients=clients,
            page_name="Edit sale",
        )
    else:
        sale = request.get_json()
        response = update_sale(sale)
        return jsonify(response)


@app.route("/add_sale", methods=["GET", "POST"])
def add_sale():
    if request.method == "POST":
        try:
            if request.is_json:
                sale = request.get_json()
                response = add_new_sale(sale)
                return jsonify(response)
            else:
                return jsonify(
                    {"success": True, "message": "Payload JSON nahi bhejre tum!"}
                )
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

    else:
        session_id = request.cookies.get("session_id")
        valid_id, username = is_valid_session(session_id)
        if valid_id:
            return render_template(
                "add_sale.html",
                session_id=session_id,
                username=username,
                page_name="Add New sale",
                products=get_all_products(),
                clients=get_all_clients(),
            )
        else:
            return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/remove_sale", methods=["POST"])
def remove_sale():
    try:
        session_id = request.cookies.get("session_id")
        sale_id = int(request.args.get("sale_id"))
        verified = is_valid_session(session_id)

        if not verified:
            return jsonify({"success": False, "message": "Unauthorized Access Denied!"})

        result = delete_sales(sale_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
