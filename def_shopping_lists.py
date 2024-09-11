from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from collections import namedtuple
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, asc, func
from models import User, db, ActiveShopping, Product, ShoppingList,Connections, ShoppingListUser
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#sort the user's shoppings lists
def orginize_data_shopping_ilsts(tauple):
    shopping_list_fix = {}
    for user_id, id, quantity, shopping_list_name, note, product, category in tauple:
        if shopping_list_name not in shopping_list_fix:
            shopping_list_fix[shopping_list_name] = []
        shopping_list_fix[shopping_list_name].append( {
            'user_id': user_id,
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

def connection_user_list(connection1, conection2, username):
    combiend_list = connection1 + conection2
    user_dict = {}
    
    for connection_id, shopping_list_name, username in combiend_list:
        if username not in user_dict:
            user_dict[username] = {
                "username": username,
                "shopping_lists": []
            }
        user_dict[username]["shopping_lists"].append({
            "shopping_list_name": shopping_list_name,
            "connection_id": connection_id
        })
        result = list(user_dict.values())
   
    return user_dict  

#get the name of the users that the user connected to in a list without doubels numbers

def get_usernames_connected_and_shopping_lists(list_of_dict):
    all_data = []
    
    for item in list_of_dict:
        user_id = item['user_id']
        shopping_list_ids = item['shopping_list_id']
        
        new_dict = {}
        
        username = db.session.query(User.username).filter(User.id == user_id).scalar()
        new_dict['username'] = username
        
        shopping_list_names = []
        
        for shopping_list_id in shopping_list_ids:
            shopping_list_name = db.session.query(ShoppingList.shopping_list_name).filter(ShoppingList.id == shopping_list_id).scalar()
            shopping_list_names.append(shopping_list_name)
        
        new_dict['shopping_list_name'] = shopping_list_names
        
        all_data.append(new_dict)
    
    return all_data


# convert shopping lists names and remove doubles

def convert_tuples_and_remove_doubles(tuple_list):
    all = []
    for item in tuple_list:
        if item[0] not in all:
            all.append(item[0])
    return all

#get and get the data of the shopping_list shared with user

def get_shared_shopping_list_data(list_shared):
    
    for user_id, shopping_list_name in list_shared:
        info = (
        db.session.query(ShoppingList.user_id, ShoppingList.id, ShoppingList.quantity, 
                         ShoppingList.shopping_list_name, ShoppingList.notes, Product.name, 
                         Product.category)
                .join(Product, ShoppingList.product_id == Product.id)
                .filter(ShoppingList.user_id == user_id, ShoppingList.shopping_list_name == shopping_list_name)
                ).all()
        if info:
            return info
    return 

#get products list to jinja tojason

def orginize_product_list(tauple):
    list_of_products = []
    for quantity, shopping_list_name, notes,  product_name, category, id in tauple:
        list_of_products .append( {
            'quantity': quantity,
            'name': product_name,
            'notes': notes,
            'category': category,
            'product_id': id    
        })
    return list_of_products 

# insert the missing to active shopping list

def save_missing_list(missing_list, user_id):
    for item in missing_list:
        new_item = ActiveShopping(
            product_id = item['product_id'],
            situation = 'missing',
            date = datetime.utcnow(),
            user_id = user_id
        )
        db.session.add(new_item)
        db.session.commit()
    return 


# orginazie to dict missing and bougth lists
def organize_to_dict_shopping_info(info_list):
    dict_info = []
    for name, date in info_list:
        dict_info.append({
            'product_name': name,
            'date': date
        })
    return dict_info


#add missing item to chosen shopping list and removed from missing

def add_item_to_shopping_list_remove(name, date, user_id, shopping_list_name):
    #is product in shopping list?
    products= (
        db.session.query(Product.id, Product.user_id)
        .join(ShoppingListUser, ShoppingListUser.user_id == user_id)
        .filter(Product.name == name, ShoppingListUser.shopping_list_name == shopping_list_name).first()
    )
    #work here !!!! 11.9
    if products:
        
        if product_id is None:
            product_id = products[0][0]
        shopping_list_to_add = (
            db.session.query(ShoppingList.product_id)
            .filter(ShoppingList.shopping_list_name == shopping_list_name, ShoppingList.user_id == user_id).all()
        )
        if shopping_list_to_add:
            if product_id not in shopping_list_to_add:       
                new_product = ShoppingList(
                    quantity = 1,
                    product_id = product_id,
                    shopping_list_name = shopping_list_name,
                    user_id = user_id,
                    notes = None
                )
                db.session.add(new_product)
                db.session.commit()
        missing_item = (db.session.query(ActiveShopping).filter(
                ActiveShopping.user_id == user_id,
                func.date(ActiveShopping.date) == date,  
                ActiveShopping.product_id == product_id
                ).first()
                    )
        # print(missing_item)
        if missing_item:
            db.session.delete(missing_item)
            db.session.commit()

    return 