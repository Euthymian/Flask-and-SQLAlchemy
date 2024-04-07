from flask import *
from sqlalchemy import select
from pathlib import Path
from db import db
from models import Product, Customer, Order, ProductOrder
from routes.api_customers import *
from routes.api_products import *
from routes.api_orders import *

app = Flask(__name__)
# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()
# This helps connect to the database 
db.init_app(app)

# ---------------------------- RENDER_TEMPLATE ----------------------------


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/customers")
def customer_list():
    statement = select(Customer).order_by(Customer.id)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("customers.html", customers = data)

@app.route("/customers/<int:customer_id>")
def customer_order_infor(customer_id):
    cus = db.get_or_404(Customer, customer_id)
    return render_template("customer_info.html", customer = cus)

@app.route("/products")
def product_list():
    statement = select(Product).order_by(Product.id)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("products.html", products = data)

@app.route("/orders")
def order_list():
    statement = select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("orders.html", orders = data)

@app.route("/orders/<int:order_id>")
def order_infor(order_id):
    order = db.get_or_404(Order, order_id)
    return render_template("order_info.html", order = order, total = order.getTotal())

@app.route("/orders/<int:order_id>/delete", methods = ["POST"])
def delete_order(order_id):
    order = db.get_or_404(Order, order_id)

    stm = db.select(ProductOrder).where(ProductOrder.order_id == order.id)
    res = db.session.execute(stm).scalars().all()
    for each in res:
        db.session.delete(each)
    
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("order_list"))



# ---------------------------- REGISTER BLUEPRINT ----------------------------


app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_customer_id_bp, url_prefix="/api/customers/<int:customer_id>")

app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(api_product_id_bp, url_prefix="/api/products/<int:product_id>")

app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
app.register_blueprint(api_order_id_bp, url_prefix="/api/orders/<int:order_id>")



# ---------------------------- CUSTOMER API ----------------------------


# Endpoints API of customers data
# @app.route("/api/customers")
# def customers_json():
#     statement = select(Customer).order_by(Customer.id) 
#     results = db.session.execute(statement)
#     customers = [] # output variable
#     for customer in results.scalars().all(): 

#         # json_record = { 
#         #     "id": customer.id, 
#         #     "name": customer.name, 
#         #     "phone": customer.phone, 
#         #     "balance": customer.balance
#         # }      
#         # customers.append(json_record) 

#         customers.append(customer.to_json()) 

#     return jsonify(customers)

# Create new customer instance
# @app.route("/api/customers", methods=["POST"])
# def create_customer():
#     data = request.json 
#     if ("name" not in data) or ("phone" not in data): 
#         return "Invalid request", 400
#     name = data["name"] 
#     phone = data["phone"]
#     if (not isinstance(name, str)) or (not isinstance(phone, str)):
#         return "Invalid request: Datatype", 400
#     new_customer = Customer(name=name, phone=phone)
#     db.session.add(new_customer)
#     db.session.commit()
#     return "A new customer was added!", 204

# # Endpoints API of customer who has specific customer_id
# @app.route("/api/customers/<int:customer_id>")
# def customer_json(customer_id):
#     statement = select(Customer).where(Customer.id == customer_id) 
#     result = db.session.execute(statement)
#     customers = []
#     for customer in result.scalars().all(): 
#         customers.append(customer.to_json())
#     return jsonify(customers)

# Delete a customer instance
# @app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
# def delete_customer(customer_id):
#     result = db.session.execute(select(Customer).where(Customer.id == customer_id)) 
#     for customer in result.scalars().all(): 
#         db.session.delete(customer) 
#     db.session.commit()
#     return "Customer was deleted!"

# Update customer's balance
# @app.route("/api/customers/<int:customer_id>", methods=["PUT"])
# def update_customer_balance(customer_id):
#     data = request.json 
#     customer = db.get_or_404(Customer, customer_id)
#     if "balance" not in data: 
#         return "Invalid request", 400
#     new_balance = data["balance"] 
#     if not isinstance(new_balance, (int,float)):
#         return "Invalid request: Datatype", 400
#     customer.balance = new_balance 
#     db.session.commit()
#     return "Customer's balance was updated!", 204


# ---------------------------- PRODUCT API ----------------------------


# Endpoints API of products data
# @app.route("/api/products")
# def products_json():
#     statement = select(Product).order_by(Product.id) 
#     results = db.session.execute(statement)
#     products = []
#     for product in results.scalars().all(): 
#         products.append(product.to_json()) 
#     return jsonify(products)

# Create new product instance
# @app.route("/api/products", methods=["POST"])
# def create_product():
#     data = request.json 
#     if ("name" not in data) or ("price" not in data): 
#         return "Invalid request", 400
#     name = data["name"] 
#     price = data["price"]
#     if (not isinstance(name, str)) or (not isinstance(price, (int, float))):
#         return "Invalid request: Datatype", 400
#     new_product = Product(name=name, price=price)
#     db.session.add(new_product)
#     db.session.commit()
#     return "A new product was added!", 204

# # Endpoints API of product who has specific product_id
# @app.route("/api/products/<int:product_id>")
# def product_json(product_id):
#     product = db.get_or_404(Product, product_id)
#     return jsonify(product.to_json())

# Delete a product instance
# @app.route("/api/products/<int:product_id>", methods=["DELETE"])
# def delete_product(product_id):
#     product = db.get_or_404(Product, product_id)
#     db.session.delete(product) 
#     db.session.commit()
#     return "Product was deleted!"

# Update product's availability
# @app.route("/api/products/<int:product_id>", methods=["PUT"])
# def update_product_availability(product_id):
#     data = request.json 
#     product = db.get_or_404(Product, product_id)
#     if "availability" not in data: 
#         return "Invalid request", 400
#     new_availability = data["availability"] 
#     if not isinstance(new_availability, int):
#         return "Invalid request: Datatype", 400
#     product.availability = new_availability 
#     db.session.commit()
#     return "Product's availability was updated!", 204


# ---------------------------- ORDER API ----------------------------


# @app.route("/api/orders")
# def orders_json():
#     statement = select(Order).order_by(Order.id) 
#     results = db.session.execute(statement)
#     orders = []
#     for order in results.scalars().all(): 
#         orders.append(order.to_json())
#     return jsonify(orders)

# @app.route("/api/orders", methods = ["POST"])
# def create_order():
#     data = request.json
#     customer = db.get_or_404(Customer, data["customer_id"])
#     items = data["items"]
#     new_order = Order(customer = customer)
#     db.session.add(new_order)

#     for item in items:
#         stm = db.select(Product).where(Product.name == item["name"])
#         product = db.session.execute(stm).scalar()
#         po = ProductOrder(order = new_order, product = product, quantity = item["quantity"])
#         db.session.add(po)

#     db.session.commit()
#     return "", 204

# @app.route("/api/orders/<int:order_id>", methods=["PUT"])
# def process_order(order_id):
#     data = request.json

#     strategy = None
#     if ("process" not in data) or (data["process"] is not True):
#         return "Invalid input, cant process!", 400
    
#     if ("strategy" in data) and (data["strategy"] not in ["reject", "ignore", "adjust"]):
#         return "Invalid input, cant process!", 400

#     if "strategy" not in data:
#         strategy = "adjust"
#     else:
#         strategy = data["strategy"]
    
#     order = db.get_or_404(Order, order_id)
#     order.process(strategy)
#     return redirect(url_for("order_list"))

# @app.route("/api/orders/<int:order_id>", methods=["POST"])
# def process_order_no_json(order_id):
#     order = db.get_or_404(Order, order_id)
#     order.process()
#     return redirect(url_for("order_list"))