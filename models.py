from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2
from sqlalchemy import Enum, DateTime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'  
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(150), unique=True, nullable=False)
    password = db.mapped_column(db.String(255), nullable=False)
    def __str__(self):
        return f"{self.id}: {self.username}"
    
    products = db.relationship('Product', backref='owner', lazy=True)
    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True)

class ActiveShopping(db.Model):
    __tablename__ = 'active_shopping'
    id = db.mapped_column(db.Integer, primary_key=True)
    product_id =  db.mapped_column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    situation =   db.mapped_column(Enum('missing', 'bougth', name='situaton_enum'), nullable=False)
    date = db.mapped_column(db.DateTime, default=datetime.utcnow)
    def __str__(self):
        return f"{self.id}: {self.situation} on ({self.created_at:%Y-%m-%d}"
    

    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(100), nullable=False)
    category = db.mapped_column(db.String, nullable=True)
    user_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    def __str__(self):
        return f"{self.id}: {self.name} on ({self.category} user id : {self.user_id}"
    active_shoppings = db.relationship('ActiveShopping', backref='product', lazy=True)
    shopping_lists = db.relationship('ShoppingList', backref='product', lazy=True)    


class ShoppingList(db.Model):
    __tablename__ = 'shopping_lists'
    id = db.mapped_column(db.Integer, primary_key=True)
    quantity = db.mapped_column(db.Integer, nullable=False)
    product_id = db.mapped_column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    shopping_list_name = db.mapped_column(db.String, nullable=False)
    user_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    notes = db.mapped_column(db.String, nullable=False)


 