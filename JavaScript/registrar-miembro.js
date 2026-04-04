document.addEventListener("DOMContentLoaded", () => {
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
});