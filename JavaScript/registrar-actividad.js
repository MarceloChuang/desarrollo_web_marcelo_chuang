document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-actividad");

    const nombreActividad = document.getElementById("nombre-actividad");
    const descripcion = document.getElementById("descripcion");
    const tipoActividad = document.getElementById("tipo-actividad");
    const miembro = document.getElementById("miembro");
    const dias = document.querySelectorAll('input[name="dias"]');
    const horaInicio = document.getElementById("hora-inicio");
    const horaTermino = document.getElementById("hora-termino");
    const archivos = document.getElementById("archivos");
    const enlace = document.getElementById("enlace");

    const errorNombreActividad = document.getElementById("error-nombre-actividad");
    const errorDescripcion = document.getElementById("error-descripcion");
    const errorTipoActividad = document.getElementById("error-tipo-actividad");
    const errorMiembro = document.getElementById("error-miembro");
    const errorDias = document.getElementById("error-dias");
    const errorHoraInicio = document.getElementById("error-hora-inicio");
    const errorHoraTermino = document.getElementById("error-hora-termino");
    const errorArchivos = document.getElementById("error-archivos");
    const errorEnlace = document.getElementById("error-enlace");

    function mostrarError(elemento) {
        elemento.classList.add("visible");
    }

    function ocultarError(elemento) {
        elemento.classList.remove("visible");
    }

    function validarTexto(input, errorElemento, minLength = 1) {
        const valor = input.value.trim();

        if (valor === "" || valor.length < minLength) {
            mostrarError(errorElemento);
            return false;
        }

        ocultarError(errorElemento);
        return true;
    }

    function validarSelect(select, errorElemento) {
        if (select.value === "") {
            mostrarError(errorElemento);
            return false;
        }

        ocultarError(errorElemento);
        return true;
    }

    function validarDias() {
        const algunoSeleccionado = Array.from(dias).some(dia => dia.checked);

        if (!algunoSeleccionado) {
            mostrarError(errorDias);
            return false;
        }

        ocultarError(errorDias);
        return true;
    }

    function validarHoras() {
        let valido = true;

        if (horaInicio.value === "") {
            mostrarError(errorHoraInicio);
            valido = false;
        } else {
            ocultarError(errorHoraInicio);
        }

        if (horaTermino.value === "") {
            mostrarError(errorHoraTermino);
            valido = false;
        } else {
            ocultarError(errorHoraTermino);
        }

        if (horaInicio.value !== "" && horaTermino.value !== "") {
            if (horaInicio.value >= horaTermino.value) {
                errorHoraTermino.textContent = "La hora de término debe ser mayor que la hora de inicio.";
                mostrarError(errorHoraTermino);
                valido = false;
            } else {
                errorHoraTermino.textContent = "Ingrese la hora de término.";
                ocultarError(errorHoraTermino);
            }
        }

        return valido;
    }

    function validarArchivos() {
        if (archivos.files.length < 1) {
            mostrarError(errorArchivos);
            return false;
        }

        ocultarError(errorArchivos);
        return true;
    }

    function validarEnlace() {
        const valor = enlace.value.trim();

        if (valor === "") {
            mostrarError(errorEnlace);
            return false;
        }

        try {
            new URL(valor);
            ocultarError(errorEnlace);
            return true;
        } catch {
            mostrarError(errorEnlace);
            return false;
        }
    }

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const nombreValido = validarTexto(nombreActividad, errorNombreActividad, 3);
        const descripcionValida = validarTexto(descripcion, errorDescripcion, 10);
        const tipoValido = validarSelect(tipoActividad, errorTipoActividad);
        const miembroValido = validarTexto(miembro, errorMiembro, 8);
        const diasValidos = validarDias();
        const horasValidas = validarHoras();
        const archivosValidos = validarArchivos();
        const enlaceValido = validarEnlace();

        const formularioValido =
            nombreValido &&
            descripcionValida &&
            tipoValido &&
            miembroValido &&
            diasValidos &&
            horasValidas &&
            archivosValidos &&
            enlaceValido;

        if (formularioValido) {
            alert("Actividad registrada correctamente.");
            window.location.href = "index.html";
        }
    });
});