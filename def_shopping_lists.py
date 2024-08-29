from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from collections import namedtuple


#sort the user's shoppings lists
def orginize_data_shopping_ilsts(tauple):
    shopping_list_fix = {}
    for quantity, shopping_list_name, note, product, category in tauple:
        if shopping_list_name not in shopping_list_fix:
            shopping_list_fix[shopping_list_name] = []
        shopping_list_fix[shopping_list_name].append( {
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
