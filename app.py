from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import psycopg2
from psycopg2 import sql
from flask_bcrypt import Bcrypt 
# making an env var 
from dotenv import load_dotenv  # take environment variables from .env.
from def_shopping_lists import get_product_id, orginize_data_shopping_ilsts
app = Flask(__name__) 

bcrypt = Bcrypt(app)
# protect my info  
load_dotenv()
username = os.getenv('USER_NAME')
db_password = os.getenv('USER_PASSWORD')
secret_key = os.getenv('SECRET_KEY')

app.secret_key = secret_key

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def get_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5433,
            database="shoppingList",
            user=username,
            password=db_password
        )
        return connection
    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
        return None

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
        
        connection = get_db_connection()
        if connection:
            cur = connection.cursor()
            try:
                cur.execute('SELECT password FROM users WHERE username = %s', (username,))
                result = cur.fetchone()
                # print(result)
                if result: 
                    stored_hash = result[0]
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
            except psycopg2.DatabaseError as e:
                print(f"Error: {e}")
                return render_template("login.html")
            finally:
                cur.close()
                connection.close()
        else:
            flash('Database connection error')
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
            connection = get_db_connection()
            if connection:
                    cur = connection.cursor()
                    cur.execute('SELECT * FROM users WHERE username = %s', (name,))
                    connection.commit()
                    user = cur.fetchone()
                    if user:
                        cur.close()
                        connection.close()
                        return render_template('sign-in.html', password2_error=False, name= True)
                    try:
                        hashed_password = hash_password(password)
                        cur.execute(
                            'INSERT INTO users (username, password) VALUES (%s, %s)',
                            (name, hashed_password)
                        )
                        connection.commit()
                        cur.close()
                        connection.close()
                        session['username'] = name
                        session['profile'] = name[0]
                        # session["color"] = color
                        return redirect(url_for('home'))
                    except psycopg2.IntegrityError as e:
                        print(f"Error inserting user: {e}")
                        flash("An error occurred while saving the user.")
                        cur.close()
                        connection.close()
                        return render_template('sign-in.html', password2_error=False, name=True)
            else:
                flash("Failed to connect to the database.")
                return render_template('sign-in.html', password2_error=False, name=True)
        else:
            if password != password2:
                return render_template('sign-in.html', password2_error=True, name= False)
            else: return render_template('sign-in.html', password2_error=False, name= True)
      
    return render_template('sign-in.html')


@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" in session:
        name = session['username']
        connection = get_db_connection()
        if connection:
            cur = connection.cursor()
            try:
                cur.execute('SELECT * FROM users WHERE username = %s', (name,))
                connection.commit()
                user_id = cur.fetchone()[0]
                if user_id:
                    session['user_id'] = user_id
                # getting the user shopping lists data
                cur.execute('SELECT  sl.quantity, sl.shopping_list_name, sl.notes, p.name, p.category FROM shopping_lists sl INNER JOIN products p ON sl.product_id = p.id WHERE sl.user_id = %s', (user_id, ))
                connection.commit()
                shopping_lists_info = cur.fetchall()
                # orginaize the output to get the full info of the user
                shopping_list = orginize_data_shopping_ilsts(shopping_lists_info)
                # print(shopping_list)
                cur.execute('SELECT id, name FROM products ORDER BY name ASC')
                connection.commit()
                products_list = cur.fetchall()
                # print(products_list)
                cur.close()
                connection.close()
            except psycopg2.IntegrityError as e:
                    print(f"Error inserting user: {e}")
                    flash("An error occurred while saving the user.")
                    cur.close()
                    connection.close()

            
        return render_template('home.html', name=name, shopping_list=shopping_list, products_list = products_list)
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
            connection = get_db_connection()
            if connection:
                product_id = get_product_id(product, connection)
                if product_id:
                    try:
                        cur = connection.cursor()
                        cur.execute('INSERT INTO shopping_lists (quantity, product_id, shopping_list_name, user_id ,notes) VALUES  (%s, %s, %s, %s, %s)', 
                                                (quantity, product_id, shopping_list_name, user_id, notes))
                        connection.commit()
                        cur.close()
                        connection.close()    
                    except  psycopg2.IntegrityError as e:
                            print(f"Error inserting user: {e}")
                            flash("An error occurred while saving the user.")
                            cur.close()
                    connection.close()          
            return redirect('home')

    else:
        redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True, port = 8080)