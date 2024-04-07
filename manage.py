import csv
import random
from sqlalchemy.sql import functions as func
from db import db
from models import Product, Customer, Order, ProductOrder
from app import app

def getData(path, dbType):
    with open(path, "r") as file:
        data = csv.DictReader(file)
        for each in data:
            if dbType == "ctm":
                obj = Customer(name=each["name"], phone=each["phone"])
            elif dbType == "pdt":
                obj = Product(name=each["name"], price=each["price"])
            db.session.add(obj)
        db.session.commit()

def initData():
    with app.app_context(): 
        db.drop_all()
        db.create_all()
        getData("./data/customers.csv", "ctm")
        getData("./data/products.csv", "pdt")

def createRecord():
    with app.app_context():
        # Random a customer
        cusStm = db.select(Customer).order_by(func.random()).limit(1)
        cus = db.session.execute(cusStm).scalar()

        # Create an order
        order = Order(customer_id = cus.id)
        db.session.add(order)
        
        # Create an association
        qtt = random.randint(5,10)
        pdtStm = db.select(Product).order_by(func.random()).limit(1)
        pdt = db.session.execute(pdtStm).scalar()
        po = ProductOrder(order_id = order.id, product_id = pdt.id, quantity = qtt)
        db.session.add(po)

        # Create an association
        qtt = random.randint(5,10)
        pdtStm = db.select(Product).order_by(func.random()).limit(1)
        pdt = db.session.execute(pdtStm).scalar()
        po = ProductOrder(order = order, product = pdt, quantity = qtt)
        db.session.add(po)

        db.session.commit()

if __name__ == "__main__": 
    initData()
    createRecord()
    
    
    
    # ----------- Test database -----------
    with app.app_context(): 
        order2 = Order(customer_id = 1)
        order3 = Order(customer_id = 1)
        order4 = Order(customer_id = 5)
        order5 = Order(customer = db.session.execute(db.select(Customer).order_by(func.random()).limit(1)).scalar())
        po3 = ProductOrder(order_id = 2, product_id = 2, quantity = 3)
        po4 = ProductOrder(order_id = 2, product_id = 12, quantity = 12)
        po5 = ProductOrder(order_id = 2, product_id = 14, quantity = 45)
        po6 = ProductOrder(order_id = 2, product_id = 7, quantity = 8)
        po7 = ProductOrder(order_id = 3, product_id = 5, quantity = 7)
        po8 = ProductOrder(order_id = 3, product_id = 3, quantity = 9)
        po9 = ProductOrder(order_id = 4, product_id = 2, quantity = 1)
        po10 = ProductOrder(order_id = 5, product_id = 6, quantity = 4)
        po11 = ProductOrder(order_id = 5, product_id = 11, quantity = 2)
        po12 = ProductOrder(order_id = 5, product_id = 7, quantity = 2)
        db.session.add(order2)
        db.session.add(order3)
        db.session.add(order4)
        db.session.add(order5)
        db.session.add(po3)
        db.session.add(po4)
        db.session.add(po5)
        db.session.add(po6)
        db.session.add(po7)
        db.session.add(po8)
        db.session.add(po9)
        db.session.add(po10)
        db.session.add(po11)
        db.session.add(po12)
        db.session.commit()

        # product = db.get_or_404(Product, 2)

        # stm = db.select(ProductOrder).where(ProductOrder.product_id == product.id)
        # for each in db.session.execute(stm).scalars().all():
        #     print(each)
        #     db.session.delete(each)

        # db.session.delete(product) 
        # db.session.commit()
    #     customer = db.get_or_404(Customer, 1)
    #     print(customer.orders)
    #     print(order3.items[0].product.price)
    #     print(po1.order.customer)

    #     customer.balance = 0
    #     order2.processed = func.now()
    #     print(order2.process("ignore")[0])


    app.run(debug=True, port=8888)