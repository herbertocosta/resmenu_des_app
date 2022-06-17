#!/usr/bin/env python3

from head import *
def search():
    @app.route("/manage/search", methods=['GET'])
    def search():
            productoNombre = request.args.get("nombre",None)
            productosRaw = db.session.execute("SELECT * FROM productos WHERE nombre = :n",
                            {"n":productoNombre})
            productos = []
            for x in productosRaw:
                    productos.append(x)
            if len(productos) == 0:
                    flash("Tu consulta no ha retornado resultados")
                    return redirect("/manage")
            return render_template("search_results.html", productos=productos)
def select():
    @app.route("/manage")
    def select():
        productos = db.session.execute("SELECT * FROM productos")
        return render_template("manage.html", productos=productos)

def insert():
    @app.route("/manage/insert", methods=['GET','POST'])
    def insert():
        if request.method == "POST":
            productoNombre = request.form["nombre"]
            productoPrecio = request.form["precio"]
            productoDesc = request.form["descripcion"]
            horariod = request.form["horariod"]
            horarioh = request.form["horarioh"]
            db.session.execute("""INSERT INTO productos
            (nombre,precio,descripcion, disponibilidad_desde, disponibilidad_hasta, propietario)
            VALUES(:n,:p ,:d, :dd,:dh,2)""",
            {
            "n":productoNombre,
            "p":productoPrecio,
            "d": productoDesc,
            "dd": horariod,
            "dh": horarioh
            })
            db.session.commit()
            return redirect("/manage")
        else:
            productos = db.session.execute("SELECT * FROM productos")
            return render_template('index.html',productos=productos)
def delete():
    @app.route("/manage/delete/<int:id>")
    def delete(id):
        productoid = id
        db.session.execute("DELETE FROM productos WHERE id = :id",{"id":productoid})
        db.session.commit()
        return redirect("/manage")
def update():
    @app.route("/manage/update/<int:id>", methods=["GET","POST"])
    def update(id):
        if request.method == "POST":
            productoNombre = request.form["nombre"]
            productoPrecio = request.form["precio"]
            productoDesc = request.form["descripcion"]
            horariod = request.form["horariod"]
            horarioh = request.form["horarioh"]
            db.session.execute("""UPDATE productos
            SET nombre= :n ,
            precio= :p,
            descripcion = :d,
            disponibilidad_desde = :dd,
            disponibilidad_hasta = :dh
            WHERE id= :id
            """,
            {
            "n":productoNombre,
            "p":productoPrecio,
            "d": productoDesc,
            "dd": horariod,
            "dh": horarioh,
            "id":id
            })
            db.session.commit()
            return redirect("/manage")
