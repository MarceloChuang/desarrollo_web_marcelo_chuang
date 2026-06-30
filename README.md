# Activa DCC — Tarea 4

Este repositorio contiene el sistema Activa DCC para la gestión de actividades de la comunidad del DCC.

El proyecto fue desarrollado utilizando Flask, Spring Boot, SQLAlchemy y MySQL, incorporando persistencia de datos, validaciones en frontend y backend, almacenamiento de archivos multimedia y navegación dinámica entre páginas.

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
- comentar en actividades y ver comentarios
- estadisticas de los usuarios 
- buscar actividades con buscador
- agregarle notas a actividades

# Tecnologías utilizadas

- Python 3
- Flask
- SQLAlchemy
- PyMySQL
- filetype
- HTML5
- CSS3
- JavaScript
- Java
- Spring Boot

# Requisitos

Para ejecutar el proyecto se requiere:

- Python 3.12 o superior
- MySQL Server
- pip
- entorno virtual de Python (venv)
- Java 26


# Pasos a seguir

- Clonar el repositorio
- Crea entorno virutal:
python -m venv venv
.\venv\Scripts\activate

- instalar dependencias
pip install -r requirements.txt

- crear la base de datos en mysql:
CREATE DATABASE tarea2;
- Las tablas se crean automáticamente mediante SQLAlchemy al ejecutar `app.py`. (incluyendo la tabla cometario, pero en el caso de que no esta la consulta sql en la carpeta database, lo mismo para nota)
- Ejercutar el proyecto:
python app.py //(Tarea 1-3)
- Entrar a la carpeta spring en otra terminal para correr el servidor de spring boot utilizando java 26.
.\mvnw.cmd spring-boot:run // (Tarea 4)
- por último correr region-comuna.sql para llenar la tablas de comuna y region.
(si necesitan datos de prueba pueden correr test_actividades.sql y test_miembros.sql)


# Archivos multimedia

Los archivos subidos se almacenan en:

static/uploads

# Validaciones

El sistema utiliza validaciones tanto en frontend (JavaScript) como en backend (Flask y Java).

Las validaciones backend se implementaron para evitar bypass de validaciones cliente y proteger la integridad de la base de datos.