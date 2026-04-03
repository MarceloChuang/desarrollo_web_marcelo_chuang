document.getElementById("form-actividad").addEventListener("submit", function(event) {
    event.preventDefault();
    const nombre_actividad = document.getElementById("nombre-actividad").value.trim();
    const tipo = document.getElementById("tipo-actividad").value;
    const horas = document.getElementById("horas-actividad").value;

    const errorNombre = document.getElementById("error-nombre");
    const errorTipo = document.getElementById("error-tipo");
    const errorHoras = document.getElementById("error-horas");

    let valid = true;

    if (nombre_actividad === "" || nombre_actividad.length < 3) {
        errorNombre.classList.add("visible");
        valid = false;
    } else {
        errorNombre.classList.remove("visible");
    }
    if (tipo === "") {
        errorTipo.classList.add("visible");
        valid = false;
    } else {
        errorTipo.classList.remove("visible");
    }
    if (horas < 0 || horas > 40 || horas === "") {
        errorHoras.classList.add("visible");
        valid = false;
    } else {
        errorHoras.classList.remove("visible");
    }
    if (valid) {
        const lista = document.getElementById("lista-actividades");
        const total = document.getElementById("total-actividades");

        const nuevaActividad = document.createElement("div");
        nuevaActividad.classList.add("actividad-item");

        const spanTipo = document.createElement("span");
        spanTipo.classList.add("tipo");
        spanTipo.textContent = tipo.toUpperCase() + " ";

        const spanNombre = document.createElement("span");
        spanNombre.classList.add("nombre");
        spanNombre.textContent = nombre_actividad;

        const spanHoras = document.createElement("span");
        spanHoras.textContent = " — " + horas + " hrs/semana";

        nuevaActividad.appendChild(spanTipo);
        nuevaActividad.appendChild(spanNombre);
        nuevaActividad.appendChild(spanHoras);

        lista.appendChild(nuevaActividad);

        total.textContent = lista.children.length;

        // Limpiar el formulario
        document.getElementById("form-actividad").reset();
    }
    else{
        return;
    }
});
