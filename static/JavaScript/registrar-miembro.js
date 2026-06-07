document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("form-miembro");

    const tipoMiembro = document.getElementById("tipo-miembro");

    const secciones = {
        pregrado: document.getElementById("datos-pregrado"),
        postgrado: document.getElementById("datos-postgrado"),
        funcionario: document.getElementById("datos-funcionario"),
        academico: document.getElementById("datos-academico")
    };

    function ocultarTodas() {
        Object.values(secciones).forEach(seccion => {
            seccion.classList.add("oculto");
        });
    }

    function mostrarSeccionSeleccionada() {
        const valor = tipoMiembro.value;

        ocultarTodas();

        if (valor && secciones[valor]) {
            secciones[valor].classList.remove("oculto");
        }
    }
    tipoMiembro.addEventListener("change", mostrarSeccionSeleccionada);

    mostrarSeccionSeleccionada();

    const nombres = document.getElementById("nombres");
    const apellidos = document.getElementById("apellidos");
    const correo = document.getElementById("correo");
    const telefono = document.getElementById("telefono");
    const comuna = document.getElementById("comuna");

    const errorNombres = document.getElementById("error-nombres");
    const errorApellidos = document.getElementById("error-apellidos");
    const errorTipo = document.getElementById("error-tipo-miembro");
    const errorCorreo = document.getElementById("error-correo");
    const errorTelefono = document.getElementById("error-telefono");
    const errorComuna = document.getElementById("error-comuna");

    function mostrarError(e){
        e.classList.add("visible");
    }

    function ocultarError(e){
        e.classList.remove("visible");
    }

    function validarTexto(input, error, min = 3, max = 50){
        const valor = input.value.trim();

        if(valor.length < min || valor.length > max){
            mostrarError(error);
            return false;
        }

        ocultarError(error);
        return true;
    }

    function validarTipo(){
        if(tipoMiembro.value === ""){
            mostrarError(errorTipo);
            return false;
        }

        ocultarError(errorTipo);
        return true;
    }

    function validarCorreo(){
        const valor = correo.value.trim();
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if(!regex.test(valor)){
            mostrarError(errorCorreo);
            return false;
        }

        ocultarError(errorCorreo);
        return true;
    }

    function validarTelefono(){
        const valor = telefono.value.trim();
        const regex = /^9+[0-9+\s]{8,15}$/;

        if(!regex.test(valor)){
            mostrarError(errorTelefono);
            return false;
        }

        ocultarError(errorTelefono);
        return true;
    }

    function validarCamposExtra() {
    let valido = true;

    if (tipoMiembro.value === "pregrado") {
        const carrera = document.getElementById("carrera");
        const ingreso = document.getElementById("ingreso-pregrado");
        const semestre = document.getElementById("semestre");

        const errorCarrera = document.getElementById("error-carrera");
        const errorIngresoPregrado = document.getElementById("error-ingreso-pregrado");
        const errorSemestre = document.getElementById("error-semestre");

        if (validarTexto(carrera, errorCarrera) === false) {
            valido = false;
        }

        if (ingreso.value === "" || Number(ingreso.value) < 2000 || Number(ingreso.value) > 2100) {
            mostrarError(errorIngresoPregrado);
            valido = false;
        } else {
            ocultarError(errorIngresoPregrado);
        }

        if (semestre.value === "" || Number(semestre.value) < 1 || Number(semestre.value) > 16) {
            mostrarError(errorSemestre);
            valido = false;
        } else {
            ocultarError(errorSemestre);
        }
    }

    if (tipoMiembro.value === "postgrado") {
        const programa = document.getElementById("programa");
        const grado = document.getElementById("grado");
        const ingreso = document.getElementById("ingreso-postgrado");

        const errorPrograma = document.getElementById("error-programa");
        const errorGrado = document.getElementById("error-grado");
        const errorIngresoPostgrado = document.getElementById("error-ingreso-postgrado");

        if (validarTexto(programa, errorPrograma) === false) {
            valido = false;
        }

        if (grado.value === "") {
            mostrarError(errorGrado);
            valido = false;
        } else {
            ocultarError(errorGrado);
        }

        if (ingreso.value === "" || Number(ingreso.value) < 2000 || Number(ingreso.value) > 2100) {
            mostrarError(errorIngresoPostgrado);
            valido = false;
        } else {
            ocultarError(errorIngresoPostgrado);
        }
    }

    if (tipoMiembro.value === "funcionario") {
        const unidad = document.getElementById("unidad-funcionario");
        const cargo = document.getElementById("cargo-funcionario");

        const errorUnidadFuncionario = document.getElementById("error-unidad-funcionario");
        const errorCargoFuncionario = document.getElementById("error-cargo-funcionario");

        if (validarTexto(unidad, errorUnidadFuncionario) === false) {
            valido = false;
        }

        if (validarTexto(cargo, errorCargoFuncionario) === false) {
            valido = false;
        }
    }

    if (tipoMiembro.value === "academico") {
        const unidad = document.getElementById("unidad-academico");
        const cargo = document.getElementById("cargo-academico");

        const errorUnidadAcademico = document.getElementById("error-unidad-academico");
        const errorCargoAcademico = document.getElementById("error-cargo-academico");

        if (validarTexto(unidad, errorUnidadAcademico) === false) {
            valido = false;
        }

        if (validarTexto(cargo, errorCargoAcademico) === false) {
            valido = false;
        }
    }

    return valido;
}


    form.addEventListener("submit", (e)=>{

        const nombresValidos = validarTexto(nombres, errorNombres);
        const apellidosValidos = validarTexto(apellidos, errorApellidos);
        const tipoValido = validarTipo();
        const correoValido = validarCorreo();
        const telefonoValido = validarTelefono();
        const comunaValida = validarTexto(comuna, errorComuna);
        const camposExtraValidos = validarCamposExtra();

        const valido =
            nombresValidos &&
            apellidosValidos &&
            tipoValido &&
            correoValido &&
            telefonoValido &&
            comunaValida &&
            camposExtraValidos;

        if (!valido) {
            e.preventDefault();
        }
    });

});