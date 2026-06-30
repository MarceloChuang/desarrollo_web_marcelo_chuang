from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import filetype
from database.db import (crear_actividad, crear_foto, get_ultimos_miembros, crear_miembro, init_db, 
                        get_todos_miembros, get_miembros_paginados, get_miembro_by_id, get_todas_comunas, 
                        estadistica_miembros_por_dia, estadistica_actividades_por_tipo, estadistica_actividades_por_comuna, get_actividad_by_id,
                        get_comentarios_actividad, crear_comentario)

app = Flask(__name__)


app.config["SECRET_KEY"] = "S3cr3tK3y"
app.config["UPLOAD_FOLDER"] = "static/uploads"


@app.route("/")
def index():
    miembros = get_ultimos_miembros()
    return render_template("index.html", miembros=miembros)


@app.route("/registrar-miembro", methods=["GET", "POST"])
def registrar_miembro():
    comunas = get_todas_comunas()
    if request.method == "POST":
        nombres = request.form.get("nombres", "").strip()
        apellidos = request.form.get("apellidos", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        telefono = telefono.replace(" ", "")
        comuna_id = request.form.get("comuna_id", "").strip()
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

        try:
            comuna_id = int(comuna_id)
        except ValueError:
            comuna_id = None

        if comuna_id is None:
            errores.append("Debe seleccionar una comuna válida.")

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
                comunas=comunas,
                errores=errores,
                form=request.form
            )

        crear_miembro(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            comuna_id=comuna_id,
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

    return render_template("registrar-miembro.html", comunas=comunas)


@app.route("/registrar-actividad", methods=["GET", "POST"])
def registrar_actividad():
    miembros = get_todos_miembros()
    if request.method == "POST":
        miembro_id = request.form.get("miembro_id", "").strip()

        nombre = request.form.get("nombre_actividad", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        dias_lista = request.form.getlist("dias")
        tipo = request.form.get("tipo_actividad", "").strip()
        hora_inicio = request.form.get("hora_inicio", "").strip()
        hora_termino = request.form.get("hora_termino", "").strip()
        enlace = request.form.get("enlace", "").strip()
        files = request.files.getlist("archivos")

        file_permitidos = [
            "image/jpeg",
            "image/png",
            "image/gif",
        ]

        errores = []
        if not files or files[0].filename == "":
            errores.append("Debe subir al menos un archivo.")
        for archivo in files:
            if archivo.filename == "":
                continue
            file_elegido = filetype.guess(archivo)
            archivo.seek(0)
            if file_elegido is None:
                errores.append(
                    f"{archivo.filename}: tipo de archivo no reconocido."
                )
                continue
            if file_elegido.mime not in file_permitidos:
                errores.append(
                    f"{archivo.filename}: archivo no permitido."
                )

        try:
            miembro_id = int(miembro_id)
        except ValueError:
            miembro_id = None

        if miembro_id is None:
            errores.append("Debe seleccionar un miembro válido.")

        if len(nombre) < 3:
            errores.append("El nombre de la actividad debe tener al menos 3 caracteres.")

        if len(descripcion) < 10:
            errores.append("La descripción debe tener al menos 10 caracteres.")

        tipos_validos = ["artistica", "deportiva", "tecnologica", "social", "recreativa"]
        if tipo not in tipos_validos:
            errores.append("Debe seleccionar un tipo de actividad válido.")

        dias_validos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        if not dias_lista:
            errores.append("Debe seleccionar al menos un día.")
        elif not all(dia in dias_validos for dia in dias_lista):
            errores.append("Uno de los días seleccionados no es válido.")

        if not hora_inicio:
            errores.append("Debe ingresar la hora de inicio.")

        if not hora_termino:
            errores.append("Debe ingresar la hora de término.")

        if hora_inicio and hora_termino and hora_inicio >= hora_termino:
            errores.append("La hora de inicio debe ser anterior a la hora de término.")

        if not enlace.startswith("http://") and not enlace.startswith("https://"):
            errores.append("Debe ingresar un enlace válido que comience con http:// o https://.")

        if errores:
            return render_template(
                "registrar-actividad.html",
                errores=errores,
                form=request.form,
                miembros=miembros
            )

        dias = ",".join(dias_lista)

        actividad_id = crear_actividad(
            miembro_id=miembro_id,
            nombre=nombre,
            descripcion=descripcion,
            tipo=tipo,
            dias=dias,
            hora_inicio=hora_inicio,
            hora_termino=hora_termino,
            enlace=enlace
        )
        for file in files:

            if file.filename == "":
                continue

            nombre_seguro = secure_filename(file.filename)

            ruta = os.path.join(
                app.config["UPLOAD_FOLDER"],
                nombre_seguro
            ).replace("\\", "/")

            file.save(ruta)

            crear_foto(
                ruta_archivo=ruta,
                nombre_archivo=nombre_seguro,
                actividad_id=actividad_id
            )

        flash("Actividad registrada correctamente.")
        return redirect(url_for("index"))

    return render_template("registrar-actividad.html", miembros=miembros, form=None)


@app.route("/lista-miembros")
def lista_miembros():
    page = request.args.get("page", 1, type=int)
    per_page = 5

    miembros, total = get_miembros_paginados(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page

    return render_template("lista-miembros.html", miembros=miembros, page=page, total_pages=total_pages)

@app.route("/miembro/<int:id>")
def ver_miembro(id):
    miembro = get_miembro_by_id(id)

    if miembro is None:
        flash("El miembro solicitado no existe.")
        return redirect(url_for("lista_miembros"))

    return render_template("ver-miembro.html", miembro=miembro)


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")

@app.route("/api/estadisticas/miembros-por-dia")
def api_miembros_por_dia():
    datos = estadistica_miembros_por_dia()
    return jsonify(datos)

@app.route("/api/estadisticas/actividades-por-tipo")
def api_actividades_por_tipo():
    datos = estadistica_actividades_por_tipo()
    return jsonify(datos)


@app.route("/api/estadisticas/actividades-por-comuna")
def api_actividades_por_comuna():
    datos = estadistica_actividades_por_comuna()
    return jsonify(datos)

@app.route("/actividad/<int:id>")
def ver_actividad(id):
    actividad = get_actividad_by_id(id)

    if actividad is None:
        flash("La actividad solicitada no existe.")
        return redirect(url_for("lista_miembros"))

    return render_template("ver-actividad.html", actividad=actividad)


@app.route("/api/actividad/<int:actividad_id>/comentarios", methods=["GET"])
def api_get_comentarios(actividad_id):
    comentarios = get_comentarios_actividad(actividad_id)

    return jsonify([
        {
            "id": comentario.id,
            "nombre": comentario.nombre,
            "texto": comentario.texto,
            "fecha": comentario.fecha.strftime("%d-%m-%Y %H:%M")
        }
        for comentario in comentarios
    ])


@app.route("/api/actividad/<int:actividad_id>/comentarios", methods=["POST"])
def api_crear_comentario(actividad_id):
    data = request.get_json()

    nombre = data.get("nombre", "").strip()
    texto = data.get("texto", "").strip()

    errores = []

    if len(nombre) < 3 or len(nombre) > 80:
        errores.append("El nombre debe tener entre 3 y 80 caracteres.")

    if len(texto) < 5:
        errores.append("El comentario debe tener al menos 5 caracteres.")

    if errores:
        return jsonify({"error": errores[0]}), 400

    crear_comentario(
        actividad_id=actividad_id,
        nombre=nombre,
        texto=texto
    )

    return jsonify({"mensaje": "Comentario agregado correctamente."}), 201

if __name__ == "__main__":
    init_db()
    app.run(debug=True)