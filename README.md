# Activa DCC — Tarea 1

Este repositorio contiene el prototipo del sistema Activa DCC para la gestión de actividades de la comunidad del DCC.

## Navegación

La página inicial es `index.html`.  
Desde allí se puede acceder a:

- Registro de miembros
- Registro de actividades
- Lista de actividades
- Estadísticas

Todas las páginas incluyen un enlace para volver al inicio.

## Registro de miembros

El formulario de registro de miembros incluye campos comunes de identificación y contacto, y campos adicionales que aparecen dinámicamente según el tipo de miembro seleccionado:

- Estudiante de pregrado
- Estudiante de postgrado
- Funcionario
- Académico

Estos campos se muestran u ocultan dinámicamente mediante JavaScript.

Las validaciones se realizaron en registrar-miembro.js, donde se verifica que los campos no esten vacios y que tengan su formawto deseado, sea que los nombres (y otros campos de texto) tengan un minimo de 3 caracteres y maximo de 50 caracteres, que el correo electronico tenga un formato "xxx@xxx.xxx", además se verifica que los numeros telefonicos sean de chile, y por ultimo se revisa que los valores ingresados para los diferentes miembros sean coherentes.

Al registrar correctamente, el sistema redirige a la página inicial.

## Registro de actividades

El formulario de actividades permite ingresar:

- nombre de la actividad
- descripción
- tipo
- miembro que la registra
- días y horarios
- archivo multimedia (obligatorio)
- enlace asociado

Se valida que:
- al menos un día esté seleccionado
- se agregue al menos un archivo
- el enlace tenga formato válido
- los horarios sean consistentes

Al registrar correctamente, el sistema redirige a la página inicial.

## Lista de actividades

La lista de actividades incluye filtros dinámicos implementados con JavaScript:

- filtro por tipo
- filtro por día
- búsqueda por nombre
- ordenamiento

Los filtros funcionan en tiempo real sobre los elementos HTML existentes.

Para evitar problemas con tildes (por ejemplo "Artística"), los textos se normalizan eliminando acentos antes de comparar.

## Estadísticas

La página de estadísticas muestra un gráfico como imagen estática incluida en la carpeta `image`.  
Esto se usa como representación visual de indicadores del sistema para el prototipo.

## Consideraciones

- No se almacenan datos ingresados
- Los listados utilizan datos simulados
- El sistema es solo un prototipo de interfaz