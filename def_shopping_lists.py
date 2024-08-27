from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql



# def login_db(username, password):
def get_product_id(product_name, db):
    new_name = product_name
    try:
        cur = db.cursor()
        cur.execute('SELECT id FROM products WHERE name ILIKE %s', (new_name, ))
        db.commit()
        result = cur.fetchone()
        if result is not None:
            product_id =result[0]
        else: product_id = None
    except  psycopg2.IntegrityError as e:
        print(f"Error inserting user: {e}")
        flash("An error occurred while saving the user.")       
    return product_id   

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

