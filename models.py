from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DateTime 
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy import select
from sqlalchemy.sql import functions as func

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    phone = mapped_column(String(20), nullable=False) 
    balance = mapped_column(Numeric, nullable=False, default=100)
    orders = relationship("Order")

    def to_json(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "phone": self.phone, 
            "balance": self.balance 
        }


class Order(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False) 
    created = mapped_column(DateTime, default=func.now())
    processed = mapped_column(DateTime, nullable=True, default=None)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("ProductOrder", back_populates="order")
    
    # Calculate total price of the order
    def getTotal(self):
        res = 0
        for item in self.items:
            res += item.quantity*item.product.price
        return res
    
    def to_json(self):
        res = {}
        res["customer_id"] = self.customer_id
        res["items"] = []
        for item in self.items:
            tmp = {}
            tmp["name"] = item.product.name
            tmp["quantity"] = item.quantity
            res["items"].append(tmp)
        return res

    def process(self, strategy = "adjust"):
        # Check if the order is being processed 
        # processing = db.session.execute(select(self.processed)).scalar()
        # if processing != None:
        #     return "The order is being processed!", False
        processing = self.processed
        if processing is not None:
            return "The order is being processed!", False

        # Check if the customer's balance > 0
        cusBalance = self.customer.balance
        if cusBalance <= 0:
            return "You have no money...", False
        
        # Execute
        if strategy == "reject":
            return "The order is not processed!", False
        else:
            for item in self.items:
                if item.quantity > item.product.availability:
                    if strategy == "ignore":
                        item.quantity = 0
                    else:
                        item.quantity = item.product.availability
                        item.product.availability = 0
                else:
                    item.product.availability -= item.quantity
        
        # Print test
        # for item in self.items:
        #     print(f"{item.product.id}   AVAI: {item.product.availability}   QUAN: {item.quantity}   PRICE: {item.product.price}")

        # Calculate and subtract from customer balance
        total = self.getTotal()
        self.customer.balance -= total
        self.processed = func.now()
        db.session.commit()
        return "Successfully processed!", True


class Product(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    price = mapped_column(Numeric, nullable=False) 
    availability = mapped_column(Integer, nullable=False, default=10)

    def to_json(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "price": self.price, 
            "availability": self.availability 
        }
    

class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False) 
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product")
    order = relationship("Order")
    quantity = mapped_column(Integer, nullable=False, default=0)