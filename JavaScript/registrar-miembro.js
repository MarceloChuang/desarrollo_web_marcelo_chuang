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

    tipoMiembro.addEventListener("change", () => {
        const valor = tipoMiembro.value;

        ocultarTodas();

        if (valor && secciones[valor]) {
            secciones[valor].classList.remove("oculto");
        }
    });

    const nombres = document.getElementById("nombres");
    const apellidos = document.getElementById("apellidos");
    const correo = document.getElementById("correo");
    const telefono = document.getElementById("telefono");

    const errorNombres = document.getElementById("error-nombres");
    const errorApellidos = document.getElementById("error-apellidos");
    const errorTipo = document.getElementById("error-tipo-miembro");
    const errorCorreo = document.getElementById("error-correo");
    const errorTelefono = document.getElementById("error-telefono");

    function mostrarError(e){
        e.classList.add("visible");
    }

    function ocultarError(e){
        e.classList.remove("visible");
    }

    function validarTexto(input, error, min = 3){
        const valor = input.value.trim();

        if(valor.length < min){
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
        const regex = /^[0-9+\s]{8,15}$/;

        if(!regex.test(valor)){
            mostrarError(errorTelefono);
            return false;
        }

        ocultarError(errorTelefono);
        return true;
    }

    function validarCamposExtra(){

        let valido = true;

        if(tipoMiembro.value === "pregrado"){
            const carrera = document.getElementById("carrera");
            const ingreso = document.getElementById("ingreso-pregrado");
            const semestre = document.getElementById("semestre");

            if(carrera.value.trim() === "") valido = false;
            if(ingreso.value === "") valido = false;
            if(semestre.value === "") valido = false;
        }

        if(tipoMiembro.value === "postgrado"){
            const programa = document.getElementById("programa");
            const grado = document.getElementById("grado");
            const ingreso = document.getElementById("ingreso-postgrado");

            if(programa.value.trim() === "") valido = false;
            if(grado.value === "") valido = false;
            if(ingreso.value === "") valido = false;
        }

        if(tipoMiembro.value === "funcionario"){
            const unidad = document.getElementById("unidad-funcionario");
            const cargo = document.getElementById("cargo-funcionario");

            if(unidad.value.trim() === "") valido = false;
            if(cargo.value.trim() === "") valido = false;
        }

        if(tipoMiembro.value === "academico"){
            const unidad = document.getElementById("unidad-academico");
            const categoria = document.getElementById("categoria");

            if(unidad.value.trim() === "") valido = false;
            if(categoria.value === "") valido = false;
        }

        return valido;
    }


    form.addEventListener("submit", (e)=>{
        e.preventDefault();

        const nombresValidos = validarTexto(nombres, errorNombres);
        const apellidosValidos = validarTexto(apellidos, errorApellidos);
        const tipoValido = validarTipo();
        const correoValido = validarCorreo();
        const telefonoValido = validarTelefono();
        const camposExtraValidos = validarCamposExtra();

        const valido =
            nombresValidos &&
            apellidosValidos &&
            tipoValido &&
            correoValido &&
            telefonoValido &&
            camposExtraValidos;

        if(valido){
            alert("Miembro registrado correctamente");
            window.location.href = "index.html";
        }
    });

});