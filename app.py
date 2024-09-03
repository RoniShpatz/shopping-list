from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from flask_bcrypt import Bcrypt 
# making an env var 
from dotenv import load_dotenv  # take environment variables from .env.
from def_shopping_lists import orginize_data_shopping_ilsts, convert_products_list_to_tauple, convert_products_list_to_edit,get_product_id_by_user_id, connection_user_list, get_usernames_connected
from flask_sqlalchemy import SQLAlchemy
from models import User, db, ActiveShopping, Product, ShoppingList, Connections
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
                    return render_template("login.html", NoAuthorize=True)
            else:
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
        session['user_id'] = user_id
        # print(user_id)
        try:
            shopping_lists_data = db.session.query(ShoppingList.id, ShoppingList.quantity, ShoppingList.shopping_list_name, ShoppingList.notes, Product.name, Product.category).join(Product, ShoppingList.product_id == Product.id).filter(ShoppingList.user_id == user_id).all()
            shopping_list = orginize_data_shopping_ilsts(shopping_lists_data)
            products_list = db.session.query(Product.id, Product.name, Product.category).order_by(asc(Product.name)).all() 
            products_list_tupels = convert_products_list_to_tauple(products_list)
            product_list_to_data_list = db.session.query(Product.id, Product.name, Product.category, Product.user_id).order_by(asc(Product.name)).all() 
            products_list_user, products_list_all = convert_products_list_to_edit(product_list = product_list_to_data_list, user_id=user_id)
            print(products_list_user, products_list_all)
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        if 'shopping_list_name' in session:
            shopping_list_name = session['shopping_list_name']
        else: shopping_list_name  = None
        return render_template('home.html', name=name, shopping_list=shopping_list, products_list = products_list_tupels, products_list_all = products_list_all, products_list_user = products_list_user, shopping_list_name = shopping_list_name)
    else:
        return redirect(url_for('login'))

@app.route("/home_add", methods = ['POST','GET'])
def home_add():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == 'POST':
        #    get all the info to send to database

            quantity = request.form.get('quantity') 
            product = request.form.get('product')
            notes = request.form.get('notes')
            shopping_list_name = request.form.get('shopping_list_name')
            if shopping_list_name:
                session['shopping_list_name'] = shopping_list_name
            products_id = db.session.query(Product.id, Product.user_id).filter_by(name=product).all()
            product_id =   get_product_id_by_user_id(products=products_id, user_id=user_id) 
            if product_id and quantity and int(quantity) >= 1:
                shopping_list_item = db.session.query(ShoppingList).filter_by(product_id=product_id,shopping_list_name=shopping_list_name).scalar()
                if shopping_list_item:
                    shopping_list_item.quantity += int(quantity)
                    shopping_list_item.notes = notes
                    flash("Item quantity updated successfully!", "success")
                else:
                    shopping_list_item = ShoppingList(quantity = quantity, product_id= product_id,  shopping_list_name=shopping_list_name, user_id=user_id, notes=notes)
                    db.session.add(shopping_list_item)
                    
                try:
                    db.session.commit()
                    flash("Item added successfully!", "success")
                except  psycopg2.IntegrityError as e:
                        print(f"Error inserting user: {e}")
                        flash("An error occurred while saving the user.")
            else:
                flash("Add valid quantity", "warning")
            return redirect('home')
    else:
        redirect(url_for('login'))

@app.route("/home_edit_list", methods = ['POST','GET'])
def home_edit_list():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == 'POST':
            action = request.form.get('action')
            id_item = request.form.get('item_id')     
            quantity = request.form.get('quantity')
            product = request.form.get('product')
            notes = request.form.get('notes')
            shopping_list_name = request.form.get('shopping_list_name')
            if 'shopping_list_name' in session:
                    session['shopping_list_name'] = shopping_list_name
            item = db.session.query(ShoppingList).filter_by(id =int(id_item )).first()
            if item:
                if action == 'update':
                    if quantity and int(quantity) >= 1:
                        item.quantity = int(quantity)
                        item.notes = notes
                        item.shopping_list_name = shopping_list_name
                        item.user_id = user_id 
                        db.session.commit()
                        flash("Item updated successfully!", "success")
                    else:
                        flash("Invalid quantity", "warning")
                elif action == 'delete':
                    db.session.delete(item)
                    db.session.commit()
                    flash("Item deleted successfully!", "success")
            else:
                flash("Item not found", "error")
        return redirect('home')
    else:
        redirect(url_for('login'))   


@app.route("/home_edit_new_list", methods = ['POST','GET'])
def home_edit_new_list():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == 'POST':
            list_name = request.form.get("new_list")
            if list_name:
                quantity = 1
                notes = None
                product_id = 124
                if list_name:
                    new_item = ShoppingList(quantity = quantity, product_id= product_id,  shopping_list_name=list_name, user_id=user_id, notes=notes)
                    db.session.add(new_item )
                try:
                    db.session.commit()
                    flash("List added successfully!", "success")
                except  psycopg2.IntegrityError as e:
                        print(f"Error inserting user: {e}")
                        flash("An error occurred while saving the user.")
            else: flash("Add shopping list name.")
            return redirect('home')
        else:
            flash("An error occurred while saving the user.", "error")


    else:
        redirect(url_for('login'))   


@app.route("/home_delete_list", methods = ['POST','GET'])
def home_delete_list():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == 'POST':
            list_name_old = request.form.get("list_name_old")
            list_name = request.form.get("list_name_edit")
            action = request.form.get('action')
            if action == "update":
                if list_name:
                    db.session.query(ShoppingList).filter(ShoppingList.shopping_list_name == list_name_old, User.id == user_id).update({"shopping_list_name": list_name})          
                    if 'shopping_list_name' not in session:
                            session['shopping_list_name'] = list_name
                    else:
                        session['shopping_list_name'] = list_name
            elif action == "delete":
                db.session.query(ShoppingList).filter(ShoppingList.shopping_list_name == list_name, User.id == user_id).delete()
            try: 
                db.session.commit() 
                flash("Edit Succecful")
            except:
                flash(f"An error occurred while saving the user", "error")

        return redirect('home')
    else:
        redirect(url_for('login'))   

@app.route("/edit_product_list", methods = ['POST','GET'])
def edit_product_list():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        product_list = db.session.query(Product.id, Product.name, Product.category, Product.user_id ).filter((Product.user_id == user_id) | (Product.user_id == None)).all()
        prodct_list_user_id, product_list_all = convert_products_list_to_edit(product_list, user_id)

        return render_template('edit-lists.html', product_list_all = product_list_all , user_name = name, user_id = user_id, product_list_user = prodct_list_user_id)
    else:
        redirect(url_for('login'))   


@app.route("/edit_product_list_edit", methods = ['POST','GET'])
def edit_product_list_edit():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == "POST":
            product_id = request.form.get("product_id")
            product_name = request.form.get("product_name")
            product_category = request.form.get("product_category")
            product_action = request.form.get("action")          
            item = db.session.query(Product).filter(Product.id == product_id, Product.category == product_category).first()
            print(item)
            if product_action == 'delete':
                db.session.delete(item)
            elif product_action == 'update':
                if product_name and product_category:
                    item.category = product_category
                    item.name = product_name
                    item.user_id = user_id
            try:
                db.session.commit()
                flash("Product updated successfully!", "success")
            except  psycopg2.IntegrityError as e:
                    print(f"Error inserting user: {e}")
                    flash("An error occurred while saving the user.")
        else: flash("Add shopping list name and category.")
        return redirect(url_for('edit_product_list'))
    else:
        redirect(url_for('login'))  


@app.route("/edit_product_list_add", methods = ['POST','GET'])
def edit_product_list_add():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        if request.method == "POST":
            product_name = request.form.get("product_name")
            product_category = request.form.get("category")
            if product_name and product_category:
                isUniqe = db.session.query(Product).filter(Product.name == product_name, Product.user_id == user_id).first()
                print(isUniqe)
                if isUniqe:
                     flash("Product name already exists", "error")
                     return redirect(url_for('edit_product_list'))
                else: 
                    new_item = Product(name=product_name,  category=product_category, user_id=user_id)
                    try:
                        db.session.add(new_item)
                        db.session.commit()
                        flash("Product Added successfully!", "success")
                    except  psycopg2.IntegrityError as e:
                            print(f"Error inserting user: {e}")
                            flash("An error occurred while saving the user.")
            else:  flash("Add shopping list name and category.")       
        return redirect(url_for('edit_product_list'))
    else:
        redirect(url_for('login'))   


@app.route("/profile", methods = ['POST','GET'])
def profile():
    if 'username' in session:
        name = session['username']
        user_id = session['user_id']
        current_username = db.session.query(Connections)


        return render_template("profile.html", name=name)
    else:
        redirect(url_for('login'))    



@app.route("/loguot", methods = ['POST','GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('user_id', None)
        if 'shopping_list' in session:
            session.pop('shopping_list', None)
        return redirect(url_for('login'))
    else:
        redirect(url_for('login'))    

if __name__ == "__main__":
    app.run(debug = True, port = 8080)