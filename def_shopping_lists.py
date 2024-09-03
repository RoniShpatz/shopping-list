from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from collections import namedtuple


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
    