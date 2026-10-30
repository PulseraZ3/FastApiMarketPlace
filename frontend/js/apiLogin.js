const API_URL = "http://127.0.0.1:8000"

const formulario = document.getElementById("formulario_login")
const mensajeError = document.getElementById("mensaje_error")
formulario.addEventListener("submit", async(event)=>{
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    try{
        const respuesta = await fetch(`${API_URL}/auth/login`,{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email:email,
                password:password
            })
        });
    const datos = await respuesta.json()

    if (!respuesta.ok){
        throw new Error(datos.detail || "Error al iniciar sesion")
    }
    sessionStorage.setItem("access_token", datos.access_token);
    sessionStorage.setItem("refresh_token", datos.refresh_token);
    window.location.href = "escritorio.html";
    }catch(error){
        mensajeError.textContent = error.message;
    }
});

//sessionStorage.getItem("access_token");