document.addEventListener("DOMContentLoaded", () => {

    const filtroTipo = document.getElementById("filtro-tipo");
    const filtroDia = document.getElementById("filtro-dia");
    const filtroTexto = document.getElementById("filtro-texto");
    const ordenar = document.getElementById("ordenar");

    const form = document.querySelector(".filtros-form");
    const lista = document.querySelector(".lista-actividades");

    const items = Array.from(document.querySelectorAll(".actividad-item"));

    function normalizarTexto(texto) {
    return texto
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
    }

    function filtrar() {
        const tipo = normalizarTexto(filtroTipo.value);
        const dia = normalizarTexto(filtroDia.value);
        const texto = normalizarTexto(filtroTexto.value);

        items.forEach(item => {
            const nombre = normalizarTexto(
                item.querySelector(".actividad-nombre").textContent
            );
            const tipoActividad = normalizarTexto(
                item.querySelector(".actividad-tipo").textContent
            );
            const contenido = normalizarTexto(item.textContent);

            const matchNombre = nombre.includes(texto);
            const matchTipo = tipo === "" || tipoActividad.includes(tipo);
            const matchDia = dia === "" || contenido.includes(dia);

            if (matchNombre && matchTipo && matchDia) {
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
        });
    }

    function ordenarLista() {

        const criterio = ordenar.value;

        const itemsVisibles = items.filter(i => i.style.display !== "none");

        itemsVisibles.sort((a, b) => {

            if (criterio === "nombre") {
                return a.querySelector(".actividad-nombre")
                    .textContent.localeCompare(
                        b.querySelector(".actividad-nombre").textContent
                    );
            }

            if (criterio === "tipo") {
                return a.querySelector(".actividad-tipo")
                    .textContent.localeCompare(
                        b.querySelector(".actividad-tipo").textContent
                    );
            }

            if (criterio === "miembro") {
                return a.textContent.localeCompare(b.textContent);
            }

        });

        itemsVisibles.forEach(item => lista.appendChild(item));
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        filtrar();
        ordenarLista();
    });

    form.addEventListener("reset", () => {
        setTimeout(() => {
            items.forEach(item => item.style.display = "block");
        }, 0);
    });

});