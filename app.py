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
        nombres = request.form.get("nombres", "").strip()
        apellidos = request.form.get("apellidos", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        telefono = telefono.replace(" ", "")
        tipo_miembro = request.form.get("tipo_miembro", "").strip()
        observaciones = request.form.get("observaciones", "").strip()

        carrera = request.form.get("carrera", "").strip() or None
        ingreso_pregrado = request.form.get("ingreso_pregrado", "").strip() or None
        semestre = request.form.get("semestre", "").strip() or None

        programa = request.form.get("programa", "").strip() or None
        grado = request.form.get("grado", "").strip() or None
        ingreso_postgrado = request.form.get("ingreso_postgrado", "").strip() or None

        unidad_funcionario = request.form.get("unidad_funcionario", "").strip() or None
        cargo_funcionario = request.form.get("cargo_funcionario", "").strip() or None

        unidad_academico = request.form.get("unidad_academico", "").strip() or None
        cargo_academico = request.form.get("cargo_academico", "").strip() or None
        oficina = request.form.get("oficina", "").strip() or None

        errores = []

        if len(nombres) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres.")

        if len(apellidos) < 3:
            errores.append("El apellido debe tener al menos 3 caracteres.")

        if "@" not in correo or "." not in correo:
            errores.append("Debe ingresar un correo válido.")

        if not telefono.isdigit() or len(telefono) < 8:
            errores.append("Debe ingresar un teléfono válido.")

        if tipo_miembro not in ["pregrado", "postgrado", "funcionario", "academico"]:
            errores.append("Debe seleccionar un tipo de miembro válido.")

        if tipo_miembro == "pregrado":
            if not carrera:
                errores.append("Debe ingresar la carrera.")
            if not ingreso_pregrado:
                errores.append("Debe ingresar el año de ingreso.")
            if not semestre:
                errores.append("Debe ingresar el semestre actual.")

        if tipo_miembro == "postgrado":
            if not programa:
                errores.append("Debe ingresar el programa.")
            if grado not in ["magister", "doctorado"]:
                errores.append("Debe seleccionar el grado.")
            if not ingreso_postgrado:
                errores.append("Debe ingresar el año de ingreso.")

        if tipo_miembro == "funcionario":
            if not unidad_funcionario:
                errores.append("Debe ingresar la unidad o área.")
            if not cargo_funcionario:
                errores.append("Debe ingresar el cargo.")

        if tipo_miembro == "academico":
            if not unidad_academico:
                errores.append("Debe ingresar el departamento.")
            if not cargo_academico:
                errores.append("Debe ingresar el cargo.")

        if errores:
            return render_template(
                "registrar-miembro.html",
                errores=errores,
                form=request.form
            )

        crear_miembro(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            tipo_miembro=tipo_miembro,
            observaciones=observaciones or None,
            carrera=carrera,
            ingreso_pregrado=int(ingreso_pregrado) if ingreso_pregrado else None,
            semestre=int(semestre) if semestre else None,
            programa=programa,
            grado=grado,
            ingreso_postgrado=int(ingreso_postgrado) if ingreso_postgrado else None,
            unidad_funcionario=unidad_funcionario,
            cargo_funcionario=cargo_funcionario,
            unidad_academico=unidad_academico,
            cargo_academico=cargo_academico,
            oficina=oficina
        )

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