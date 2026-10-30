
const API_URL = "http://127.0.0.1:8000";

const formulario = document.getElementById("formulario_registro");

const mensajeError = document.getElementById("mensaje_error");
const mensajeExito = document.getElementById("mensaje_exito");

formulario.addEventListener("submit", async (event) => {

    event.preventDefault();

    mensajeError.textContent = "";
    mensajeExito.textContent = "";

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {

        const respuesta = await fetch(`${API_URL}/auth/register`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })

        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.detail || "No se pudo registrar el usuario");
        }

        mensajeExito.textContent = datos.mensaje;
        
        window.location.href="login.html";

    } catch (error) {

        mensajeError.textContent = error.message;

    }

});
