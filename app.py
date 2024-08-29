from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from flask_bcrypt import Bcrypt 
# making an env var 
from dotenv import load_dotenv  # take environment variables from .env.
from def_shopping_lists import orginize_data_shopping_ilsts, convert_products_list_to_tauple
from flask_sqlalchemy import SQLAlchemy
from models import User, db, ActiveShopping, Product, ShoppingList
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, asc

app = Flask(__name__) 

bcrypt = Bcrypt(app)
# protect my info  
load_dotenv()

secret_key = os.getenv('SECRET_KEY')

app.secret_key = secret_key
app.config.from_object('config')

db.init_app(app)



def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def  verify_password(hashed_password, user_password):
    return bcrypt.check_password_hash(hashed_password, user_password) 
            
@app.route("/", methods=["GET", "POST"])
def index():
        return redirect(url_for('login'))
   
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            # Query the user by username using SQLAlchemy
            stmt = select(User).where(User.username == username)
            user = db.session.execute(stmt).scalars().first()
            print(user)
            if user: 
                stored_hash = user.password
                if verify_password(stored_hash, password):
                    session['username'] = username
                    flash('Login successful')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password')
                    return render_template("login.html", NoAuthorize=True)
            else:
                flash('Username not found')
                return render_template("login.html", NoUsername=True)
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            flash('An error occurred while accessing the database')
            return render_template("login.html")

    return render_template("login.html")

   


@app.route("/sign-in", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password-2")
        # color = request.form.get("color")
        # print(name)
        if password == password2:
            if User.query.filter_by(username=name).first():
                return render_template('sign-in.html', password2_error=False, name= True)
            else:
                try:
                    hashed_password = hash_password(password)
                    user = User(username = name, password = hashed_password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('home'))
                except SQLAlchemyError as e:
                    print(f"Error: {e}")
                    flash('sign-in.html', password2_error=True, name= False)
                    return render_template('sign-in.html')
        else: return render_template('sign-in.html', password2_error=False, name= True)
    return render_template('sign-in.html')

  
@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" in session:
        name = session['username']
        user_id = db.session.query(User.id).filter_by(username=name).scalar()
        # print(user_id)
        try:
            shopping_lists_data = db.session.query( ShoppingList.quantity, ShoppingList.shopping_list_name, ShoppingList.notes, Product.name, Product.category).join(Product, ShoppingList.product_id == Product.id).filter(ShoppingList.user_id == user_id).all()
            shopping_list = orginize_data_shopping_ilsts(shopping_lists_data)
            products_list = db.session.query(Product.id, Product.name, Product.category).order_by(asc(Product.name)).all() 
            products_list_tupels = convert_products_list_to_tauple(products_list)
            
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        return render_template('home.html', name=name, shopping_list=shopping_list, products_list = products_list_tupels)
    else:
        return redirect(url_for('login'))

@app.route("/home_edit", methods = ['POST','GET'])
def home_edit():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == 'POST':
        #    get all the info to send to database
            quantity = request.form.get('quantity') 
            product = request.form.get('product')
            notes = request.form.get('notes')
            shopping_list_name = request.form.get('shopping_list_name')
            product_id = db.session.query(Product.id).filter_by(name=product).scalar()
            print(product_id)
            if product_id:
                try:
                    shopping_list_item = ShoppingList(quantity = quantity, product_id= product_id,  shopping_list_name=shopping_list_name, user_id=user_id, notes=notes)
                    db.session.add(shopping_list_item)
                    db.session.commit()
                except  psycopg2.IntegrityError as e:
                        print(f"Error inserting user: {e}")
                        flash("An error occurred while saving the user.")
                        
            return redirect('home')
    else:
        redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True, port = 8080)