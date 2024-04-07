from flask import Blueprint, jsonify, request
from db import db
from models import Customer,Order,ProductOrder
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!

api_customers_bp = Blueprint("api_customers", __name__)

# All customers data
@api_customers_bp.route("/", methods=["GET"])
def customers_json():
    stmt = db.select(Customer).order_by(Customer.name) 
    results = db.session.execute(stmt).scalars() 
    return jsonify([cust.to_json() for cust in results])

# Create new customer
@api_customers_bp.route("/", methods=["POST"])
def create_customer():
    data = request.json 
    if ("name" not in data) or ("phone" not in data): 
        return "Invalid request", 400
    name = data["name"] 
    phone = data["phone"]
    if (not isinstance(name, str)) or (not isinstance(phone, str)):
        return "Invalid request: Datatype", 400
    new_customer = Customer(name=name, phone=phone)
    db.session.add(new_customer)
    db.session.commit()
    return "A new customer was added!", 204

api_customer_id_bp = Blueprint("api_customer_id", __name__)

# Customer data with specific customer_id
@api_customer_id_bp.route("/", methods=["GET"])
def customer_json(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id) 
    result = db.session.execute(statement)
    customers = []
    for customer in result.scalars().all(): 
        customers.append(customer.to_json())
    return jsonify(customers)

# Delete a customer 
@api_customer_id_bp.route("/", methods=["DELETE"])
def delete_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    for order in customer.orders:
        stm = db.select(ProductOrder).where(ProductOrder.order_id == order.id)
        res = db.session.execute(stm).scalars().all()
        for each in res:
            db.session.delete(each)
        db.session.delete(order)
    db.session.delete(customer)
    db.session.commit()
    return "Customer was deleted!", 204

# Update a customer's balance
@api_customer_id_bp.route("/", methods=["PUT"])
def update_customer_balance(customer_id):
    data = request.json 
    customer = db.get_or_404(Customer, customer_id)
    if "balance" not in data: 
        return "Invalid request", 400
    new_balance = data["balance"] 
    if not isinstance(new_balance, (int,float)):
        return "Invalid request: Datatype", 400
    customer.balance = new_balance 
    db.session.commit()
    return "Customer's balance was updated!", 204