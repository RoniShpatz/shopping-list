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
    user_id =  db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __str__(self):
        return f"{self.id}: {self.situation} on ({self.date:%Y-%m-%d}"
    

    
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


class Connections(db.Model):
    __tablename__ = 'connections'
    id = db.mapped_column(db.Integer, primary_key=True)
    user_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_send = db.mapped_column(db.Boolean, nullable = True)
    is_excepted = db.mapped_column(db.Boolean, nullable = True)
    user_id_join = db.mapped_column(db.Integer, nullable=True)
   
    shopping_list_id = db.mapped_column(db.Integer, db.ForeignKey('shopping_list_user.id'), nullable=True)


class ShoppingListUser(db.Model):
    __tablename__ = 'shopping_list_user'
    id = db.mapped_column(db.Integer, primary_key=True)
    shopping_list_name = db.mapped_column(db.String, nullable=False)
    user_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=True)