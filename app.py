from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from flask_bcrypt import Bcrypt 

app = Flask(__name__) 
secret_key = "my_secret_key"
bcrypt = Bcrypt(app)




app.secret_key = secret_key

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("login")
   
@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


@app.route("/sign-in", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password-2")
        color = request.form.get("color")
        isUniq = False
        if password == password2 and color and isUniq == False:
            session['username'] = name
            session['profile'] = name[0]
            session["color"] = color
            return redirect(url_for('home'))
        else:
            if password != password2:
                return render_template('sign-in.html', password2_error=True, name= False)
            else: return render_template('sign-in.html', password2_error=False, name= True)
      
    return render_template('sign-in.html')






if __name__ == "__main__":
    app.run(debug = True, port = 8080)