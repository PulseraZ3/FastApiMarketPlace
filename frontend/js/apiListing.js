const API_URL = "http://127.0.0.1:8000";
const contenedor_publicaciones = document.getElementById("contenedor_publicaciones");
const IMAGEN_RESPALDO = "../imagenes/asd.png";

function mostrar_mensaje(texto) {
    const mensaje = document.createElement("p");
    mensaje.classList.add("mensaje_estado");
    mensaje.textContent = texto;
    contenedor_publicaciones.replaceChildren(mensaje);
}

function crear_tarjeta(publicacion) {
    const tarjeta = document.createElement("article");
    tarjeta.classList.add("tarjeta_publicacion");
    tarjeta.title = publicacion.description || "";

    // imagen
    const imagen = document.createElement("div");
    imagen.classList.add("imagen_publicacion");

    const foto = document.createElement("img");
    foto.alt = publicacion.title;
    // {once: true} evita el bucle infinito si el respaldo tampoco carga
    foto.addEventListener("error", () => {
        foto.src = IMAGEN_RESPALDO;
    }, { once: true });
    foto.src = publicacion.image_url || IMAGEN_RESPALDO;
    imagen.appendChild(foto);

    // título
    const titulo = document.createElement("h3");
    titulo.textContent = publicacion.title;

    // precio + botón
    const precio = document.createElement("p");
    precio.classList.add("precio_publicacion");
    precio.textContent = `S/ ${Number(publicacion.price).toFixed(2)}`;

    const boton = document.createElement("button");
    boton.classList.add("boton_ver_publicacion");
    boton.type = "button";
    boton.textContent = "Ver";
    boton.addEventListener("click", () => {
        console.log("Ver publicación", publicacion.id);
    });

    const pie = document.createElement("div");
    pie.classList.add("pie_publicacion");
    pie.append(precio, boton);

    tarjeta.append(imagen, titulo, pie);
    return tarjeta;
}

let cargando = false;

async function cargar_publicaciones() {
    if (cargando) return; // evita cargas simultáneas que hacen parpadear
    cargando = true;

    mostrar_mensaje("Cargando publicaciones...");

    try {
        const respuesta = await fetch(`${API_URL}/listings/`);
        if (!respuesta.ok) {
            throw new Error("No se pudieron obtener las publicaciones");
        }

        const publicaciones = await respuesta.json();

        if (publicaciones.length === 0) {
            mostrar_mensaje("Todavía no hay publicaciones.");
            return;
        }

        contenedor_publicaciones.replaceChildren(
            ...publicaciones.map(crear_tarjeta)
        );

    } catch (error) {
        console.error(error);
        mostrar_mensaje("Ocurrió un error al cargar las publicaciones.");
    } finally {
        cargando = false;
    }
}

cargar_publicaciones();