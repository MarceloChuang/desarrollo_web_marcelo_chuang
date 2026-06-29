document.addEventListener("DOMContentLoaded", () => {
    const inputBusqueda = document.getElementById("busqueda");
    const contenedorResultados = document.getElementById("resultados");
    const mensajeBusqueda = document.getElementById("mensaje-busqueda");

    inputBusqueda.addEventListener("input", async () => {
        const texto = inputBusqueda.value.trim();

        if (texto.length < 3) {
            contenedorResultados.innerHTML = `
                <p class="sin-resultados">
                    Escriba al menos 3 caracteres para iniciar la búsqueda.
                </p>
            `;
            mensajeBusqueda.textContent = "";
            return;
        }

        await buscarActividades(texto);
    });

    async function buscarActividades(texto) {
        try {
            mensajeBusqueda.textContent = "Buscando...";

            const response = await fetch(`/api/actividades/buscar?q=${encodeURIComponent(texto)}`);
            const actividades = await response.json();

            mensajeBusqueda.textContent = "";

            if (actividades.length === 0) {
                contenedorResultados.innerHTML = `
                    <p class="sin-resultados">
                        No se encontraron actividades para "${texto}".
                    </p>
                `;
                return;
            }

            contenedorResultados.innerHTML = "";

            actividades.forEach((actividad) => {
                const article = document.createElement("article");
                article.classList.add("resultado-item");

                article.innerHTML = `
                    <div class="resultado-header">
                        <h2>${resaltarTexto(actividad.nombre, texto)}</h2>
                        <span class="tipo-actividad">${actividad.tipo}</span>
                    </div>

                    <p><strong>Miembro:</strong> ${actividad.miembro}</p>
                    <p><strong>Día:</strong> ${actividad.dias}</p>
                    <p><strong>Comuna:</strong> ${resaltarTexto(actividad.comuna, texto)}</p>
                    <p><strong>Descripción:</strong> ${resaltarTexto(actividad.descripcion, texto)}</p>

                    <div class="nota-contenedor">
                        <span class="nota-valor">
                            Nota: <span id="nota-${actividad.id}">${actividad.nota}</span>
                            (<span id="contador-notas-${actividad.id}">${actividad.cantidad_notas}</span> evaluaciones)
                        </span>

                        <label for="select-nota-${actividad.id}">Evaluar:</label>

                        <select id="select-nota-${actividad.id}" class="select-nota">
                            <option value="">-- Nota --</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                        </select>

                        <button class="btn-evaluar" data-id="${actividad.id}">
                            Evaluar
                        </button>
                    </div>
                `;

                contenedorResultados.appendChild(article);
            });

        } catch (error) {
            mensajeBusqueda.textContent = "Error al buscar actividades.";
            console.error(error);
        }
    }

    function resaltarTexto(textoOriginal, busqueda) {
        if (!textoOriginal) {
            return "";
        }

        const regex = new RegExp(`(${escapeRegex(busqueda)})`, "gi");

        return textoOriginal.replace(regex, `<span class="resaltado">$1</span>`);
    }

    function escapeRegex(texto) {
        return texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }
    contenedorResultados.addEventListener("click", async (event) => {
        const boton = event.target.closest(".btn-evaluar");

        if (!boton) {
            return;
        }

        const actividadId = boton.dataset.id;
        const select = document.getElementById(`select-nota-${actividadId}`);
        const notaSpan = document.getElementById(`nota-${actividadId}`);
        const contadorSpan = document.getElementById(`contador-notas-${actividadId}`);

        const nota = Number(select.value);

        if (nota === "") {
            alert("Debe seleccionar una nota.");
            return;
        }
        if (!Number.isInteger(nota) || nota < 1 || nota > 7) {
            alert("Debe seleccionar una nota válida entre 1 y 7.");
            return;
        }

        boton.disabled = true;

        try {
            const response = await fetch(`/api/actividades/${actividadId}/nota`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nota: nota })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "No se pudo registrar la nota.");
                return;
            }

            notaSpan.textContent = data.nota;
            contadorSpan.textContent = data.cantidad_notas;
            select.value = "";

        } catch (error) {
            console.error(error);
            alert("Error al conectar con el servidor.");
        } finally {
            boton.disabled = false;
        }
    });
});