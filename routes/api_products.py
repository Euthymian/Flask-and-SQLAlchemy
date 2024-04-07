from flask import Blueprint, jsonify, request
from db import db
from models import Product,Order,ProductOrder
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!

api_products_bp = Blueprint("api_products", __name__)

# All products data
@api_products_bp.route("/", methods=["GET"])
def products_json():
    statement = db.select(Product).order_by(Product.id) 
    results = db.session.execute(statement)
    products = [] 
    for product in results.scalars().all(): 
        products.append(product.to_json()) 
    return jsonify(products)

# Create new product
@api_products_bp.route("/", methods=["POST"])
def create_product():
    data = request.json 
    if ("name" not in data) or ("price" not in data): 
        return "Invalid request", 400
    name = data["name"] 
    price = data["price"]
    if (not isinstance(name, str)) or (not isinstance(price, (int, float))):
        return "Invalid request: Datatype", 400
    if price <= 0:
        return "Invalid price", 400
    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return "A new product was added!", 204

api_product_id_bp = Blueprint("api_product_id", __name__)

# Product data with specific product_id
@api_product_id_bp.route("/", methods=["GET"])
def product_json(product_id):
    product = db.get_or_404(Product, product_id)
    return jsonify(product.to_json())

# Delete a product
@api_product_id_bp.route("/", methods=["DELETE"])
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)

    stm = db.select(ProductOrder).where(ProductOrder.product_id == product.id)
    for each in db.session.execute(stm).scalars().all():
        # print(each)
        db.session.delete(each)

    db.session.delete(product) 
    db.session.commit()
    return "Product was deleted!", 204

# Update product's availability
@api_product_id_bp.route("/", methods=["PUT"])
def update_product_availability(product_id):
    data = request.json 
    product = db.get_or_404(Product, product_id)
    if "availability" not in data: 
        return "Invalid request", 400
    new_availability = data["availability"] 
    if not isinstance(new_availability, int):
        return "Invalid request: Datatype", 400
    product.availability = new_availability 
    db.session.commit()
    return "Product's availability was updated!", 204