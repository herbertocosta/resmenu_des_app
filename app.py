from flask import Flask, render_template, request, url_for, redirect, send_from_directory, session, flash
from flask_sqlalchemy import SQLAlchemy
from encrypt import *

app = Flask(__name__)
#mysql
#app.config['SQLALCHEMY_DATABASE_URI']="mysql://testing:12345@127.0.0.1:3306/RESMenu"
#mariadb
app.config['SQLALCHEMY_DATABASE_URI']="mariadb+mariadbconnector://testing:12345@127.0.0.1:3306/RESMenu"
db = SQLAlchemy(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def root():
        products = db.session.execute("SELECT * FROM productos") #sólo de testeo
        return "Welcome page"

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["pwd"]
        passwordEncrypted = encrypt(password)
        query = db.session.execute("SELECT password, gmail FROM usuarios WHERE gmail = :mail",{"mail": mail})
        dbGmail = None
        dbPassword = None
        for result in query:
                dbGmail = result["gmail"]
                dbPassword = result["password"]
        if passwordEncrypted != dbPassword or mail != dbGmail:
                flash("La contraseña o el mail son incorrectos")
                return redirect("/login")

        session["mail"] = mail
        flash("Has iniciado sessión")
        return redirect("/profile")
    else:
        return render_template("login.html")
@app.route("/signup", methods = ["GET","POST"])
def signup():
        if request.method == "POST":
               mail = request.form["mail"]
               nombre = request.form["nombre"]
               apellido = request.form["apellido"]
               password = request.form["pwd"]
               passwordEncrypted = encrypt(password)
               query = db.session.execute("SELECT gmail FROM usuarios WHERE gmail = :mail",{"mail": mail})
               dbGmail = None
               for resutl in query:
                       dbGmail = result["gmail"]
               if mail == dbGmail:
                       flash("Esta cuenta ya existe")
                       return redirect("/signup")
               db.session.execute(
                """INSERT INTO usuarios
               (gmail,nombre,apellido,password,estado)
               VALUES(:mail,:nomb,:apel,:pass,'pendiente' )""",
                {"mail": mail,
                 "nomb": nombre,
                 "apel": apellido,
                 "pass": passwordEncrypted})
               db.session.commit()
               flash("usuario registrado")
               return redirect("/profile")
        return render_template("signup.html")
@app.route("/profile")
def profile():
    if "mail" in session:
        return render_template("profile.html")
    return "no iniciaste sesión"

@app.route("products/select/<int:id>", methods=['GET','POST'])
def search():
    if request.method == "POST":
        productName = request.form["name"]
        db.session.execute("SELECT * FROM products WHERE productName = :n",
                           {"n":productName})
        db.session.commit()
    else:
        return render_template("productos.html")

@app.route("products/select/<int:id>")
def select():
    db.session.execute("SELECT * FROM products")
    db.session.commit()
    return redirect("/")

@app.route("/products/insert/<int:id>", methods=['GET','POST'])
def insert(): 
    if request.method == "POST":
        productName = request.form["name"]
        productPrice = request.form["price"]
        productStock = request.form["quantity_in_stock"]
        db.session.execute("INSERT INTO products (name,price,quantity_in_stock) VALUES(:n,:p ,:s)",
                           {"n":productName,"p":productPrice,"s":productStock})
        db.session.commit()
        return redirect("/")
    else:
        products = db.session.execute("SELECT * FROM products")
        return render_template('index.html',products=products)

@app.route("/delete/<int:id>")
def delete(id):
    db.session.execute("DELETE FROM products WHERE id = :id",{"id":id})
    db.session.commit()
    return redirect("/")
    
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    if request.method == "POST":
        productName = request.form["name"]
        productPrice = request.form["price"]
        productStock = request.form["quantity_in_stock"]
        db.session.execute("UPDATE products SET name= :n ,price= :p ,quantity_in_stock= :s WHERE id= :id",
                           {"n":productName,"p":productPrice,"s":productStock,"id":id})
        db.session.commit()
        return redirect("/")
if __name__ == "__main__":
   app.run(debug=True)

@app.route('/logout')
def logout():
    session.pop('mail', None)
    return redirect("/login")
if __name__ == "__main__":
   app.run(debug=True)
