from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import filetype
from database.db import get_ultimos_miembros, crear_miembro, SessionLocal, Miembro, Actividad, Foto, init_db

app = Flask(__name__)

app.config["SECRET_KEY"] = "S3cr3tK3y"
app.config["UPLOAD_FOLDER"] = "static/uploads"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registrar-miembro", methods=["GET", "POST"])
def registrar_miembro():
    if request.method == "POST":
        # Aquí después van las validaciones del servidor
        # y la inserción en la base de datos.
        flash("Miembro registrado correctamente.")
        return redirect(url_for("index"))

    return render_template("registrar-miembro.html")


@app.route("/registrar-actividad", methods=["GET", "POST"])
def registrar_actividad():
    if request.method == "POST":
        flash("Actividad registrada correctamente.")
        return redirect(url_for("index"))

    return render_template("registrar-actividad.html")


@app.route("/lista-miembros")
def lista_miembros():
    return render_template("lista-miembros.html")

@app.route("/miembro/<int:id>")
def ver_miembro(id):
    return render_template("ver-miembro.html", id=id)


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)