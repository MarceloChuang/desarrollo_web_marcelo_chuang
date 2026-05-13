# Activa DCC — Tarea 2

Este repositorio contiene el sistema Activa DCC para la gestión de actividades de la comunidad del DCC.

El proyecto fue desarrollado utilizando Flask, SQLAlchemy y MySQL, incorporando persistencia de datos, validaciones en frontend y backend, almacenamiento de archivos multimedia y navegación dinámica entre páginas.

# Funcionalidades

El sistema permite:

- registrar miembros de la comunidad
- registrar actividades asociadas a miembros
- subir archivos multimedia asociados a actividades
- visualizar los últimos miembros registrados
- listar miembros desde la base de datos
- visualizar el detalle de cada miembro junto a sus actividades
- visualizar archivos multimedia asociados a actividades
- paginar resultados
- validar formularios tanto en frontend como backend

# Tecnologías utilizadas

- Python 3
- Flask
- SQLAlchemy
- PyMySQL
- filetype
- HTML5
- CSS3
- JavaScript

# Requisitos

Para ejecutar el proyecto se requiere:

- Python 3.12 o superior
- MySQL Server
- pip
- entorno virtual de Python (venv)


# Pasos a seguir

- Clonar el repositorio
- Crea entorno virutal:
python -m venv venv
.\venv\Scripts\activate

- instalar dependencias
pip install -r requirements.txt

- crear la base de datos en mysql:
CREATE DATABASE tarea2;
- Las tablas se crean automáticamente mediante SQLAlchemy al ejecutar `app.py`.
- ejercutar el proyecto:
python app.py

# Archivos multimedia

Los archivos subidos se almacenan en:

static/uploads

# Validaciones

El sistema utiliza validaciones tanto en frontend (JavaScript) como en backend (Flask).

Las validaciones backend se implementaron para evitar bypass de validaciones cliente y proteger la integridad de la base de datos.