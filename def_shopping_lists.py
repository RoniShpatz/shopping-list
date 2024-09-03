from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from collections import namedtuple
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, asc
from models import User, db, ActiveShopping, Product, ShoppingList,Connections
from flask_sqlalchemy import SQLAlchemy


#sort the user's shoppings lists
def orginize_data_shopping_ilsts(tauple):
    shopping_list_fix = {}
    for id, quantity, shopping_list_name, note, product, category in tauple:
        if shopping_list_name not in shopping_list_fix:
            shopping_list_fix[shopping_list_name] = []
        shopping_list_fix[shopping_list_name].append( {
            'id': id,
            'quantity': quantity,
            'name': product,
            'notes': note,
            'category': category    
        })
     

    return shopping_list_fix

# convert list from the sqlalchemy to dict to use with jinja2

def convert_products_list_to_tauple(product_list):
    Product = namedtuple('Product', ['id', 'name', 'category'])
    product_list_of_namedtuples = [Product(*product) for product in product_list]
    return product_list_of_namedtuples

def convert_products_list_to_edit(product_list, user_id):
    Product = namedtuple('Product', ['id', 'name', 'category', 'user_id'])
    product_list_of_namedtuples = [Product(*product) for product in product_list]
    product_list_of_namedtuples_filterd =  [product for product in product_list_of_namedtuples if product.category != "no products yet"]
    product_with_user_id = [product for product in product_list_of_namedtuples_filterd if product.user_id == user_id]
    products_without_user_id = [product for product in product_list_of_namedtuples_filterd if not product.user_id]
    return product_with_user_id, products_without_user_id

# get the user_id of a product to get the products that are of a user

def get_product_id_by_user_id(products, user_id):
    for product_id, user in products:
        if user == user_id:
            return product_id
        elif user == None:
            return product_id

#get the connection of a user- who the user connect to and who is connected to user.

def connection_user_list(connection1, conection2):
    all_connections = []
    if connection1:
        for list_connection in connection1:
            for num in list_connection:
                all_connections.append(num)
    if conection2:
        for list_connection in conection2:
            for num in list_connection:
                if num not in all_connections:
                    all_connections.append(num)
    return all_connections

def get_usernames_connected(list_of_users_id):
    list_of_usernames = []
    for num in list_of_users_id:
        username = db.session.query(User.username).filter(User.id == num).first()
        if username:
            for name in username:
                if name not in list_of_usernames:
                    list_of_usernames.append(name)
    return list_of_usernames

    