document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-comentario");
    const actividadId = document.getElementById("actividad-id");
    const nombreInput = document.getElementById("nombre-comentario");
    const textoInput = document.getElementById("texto-comentario");
    const mensaje = document.getElementById("mensaje-comentario");
    const listaComentarios = document.getElementById("lista-comentarios");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const nombre = nombreInput.value.trim();
        const texto = textoInput.value.trim();

        mensaje.textContent = "";
        mensaje.className = "";

        if (nombre.length < 3 || nombre.length > 80) {
            mensaje.textContent = "El nombre debe tener entre 3 y 80 caracteres.";
            mensaje.classList.add("error");
            return;
        }

        if (texto.length < 5) {
            mensaje.textContent = "El comentario debe tener al menos 5 caracteres.";
            mensaje.classList.add("error");
            return;
        }

        try {
            const response = await fetch(`/api/actividad/${actividadId.value}/comentarios`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nombre: nombre,
                    texto: texto
                })
            });

            const data = await response.json();
            console.log("Respuesta del servidor:", data);

            if (!response.ok) {
                mensaje.textContent = data.error || "No se pudo agregar el comentario.";
                mensaje.classList.add("error");
                return;
            }

            mensaje.textContent = "Comentario agregado correctamente.";
            mensaje.classList.add("success");

            nombreInput.value = "";
            textoInput.value = "";

            console.log("Cargando comentarios...");
            cargarComentarios();

        } catch (error) {
            mensaje.textContent = "Error al conectar con el servidor.";
            mensaje.classList.add("error");
        }
    });

    async function cargarComentarios() {
        try {
            const response = await fetch(`/api/actividad/${actividadId.value}/comentarios`);
            const comentarios = await response.json();

            listaComentarios.innerHTML = "";

            if (comentarios.length === 0) {
                listaComentarios.innerHTML = "<p>No existen comentarios para esta actividad.</p>";
                return;
            }

            comentarios.forEach((comentario) => {
                const article = document.createElement("article");
                article.classList.add("comentario");

                article.innerHTML = `
                    <div class="comentario-header">
                        <strong>${comentario.nombre}</strong>
                        <span>${comentario.fecha}</span>
                    </div>
                    <p>${comentario.texto}</p>
                `;

                listaComentarios.appendChild(article);
            });

        } catch (error) {
            console.error("Error cargando comentarios:", error);
        }
    }
});