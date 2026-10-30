const API_URL = "http://127.0.0.1:8000";
const contenedor_publicaciones = document.getElementById("contenedor_publicaciones");

async function cargar_publicaciones() {
    contenedor_publicaciones.textContent = "Cargando publicaciones...";

    try {
        const respuesta = await fetch(`${API_URL}/listings/`);

        if (!respuesta.ok) {
            throw new Error("No se pudieron obtener las publicaciones");
        }

        const publicaciones = await respuesta.json();

        contenedor_publicaciones.replaceChildren();

        if (publicaciones.length === 0) {
            contenedor_publicaciones.textContent = "Todavía no hay publicaciones.";
            return;
        }

        publicaciones.forEach(publicacion => {

            const tarjeta = document.createElement("article");
            tarjeta.classList.add("tarjeta_publicacion");

            const encabezado = document.createElement("div");
            encabezado.classList.add("encabezado_publicacion");

            const estado = document.createElement("span");
            estado.classList.add("estado_publicacion");
            estado.textContent = publicacion.status;

            const identificador = document.createElement("span");
            identificador.textContent = `#${publicacion.id}`;

            encabezado.append(estado, identificador);

            const imagen = document.createElement("div");
            imagen.classList.add("imagen_publicacion");
            const foto = document.createElement("img");
            foto.src = publicacion.image_url || "../imagenes/asd.png";
            foto.alt = publicacion.title;
            imagen.appendChild(foto);

            const titulo = document.createElement("h3");
            titulo.textContent = publicacion.title;

            const precio = document.createElement("p");
            precio.classList.add("precio_publicacion");
            precio.textContent = `S/ ${Number(publicacion.price).toFixed(2)}`;

            const descripcion = document.createElement("p");
            descripcion.classList.add("descripcion_publicacion");
            descripcion.textContent = publicacion.description;

            const condicion = document.createElement("span");
            condicion.classList.add("condicion_publicacion");
            condicion.textContent = publicacion.condition;

            const pie = document.createElement("div");
            pie.classList.add("pie_publicacion");
            pie.appendChild(condicion);

            tarjeta.append(
                encabezado,
                imagen,
                titulo,
                precio,
                descripcion,
                pie
            );

            contenedor_publicaciones.appendChild(tarjeta);
        });

    } catch (error) {
        console.error(error);
        contenedor_publicaciones.textContent =
            "Ocurrió un error al cargar las publicaciones.";
    }
}