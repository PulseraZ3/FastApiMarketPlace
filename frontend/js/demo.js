const MODO_DEMO = true;

if(MODO_DEMO)
{
    const formulario = document.querySelector("#tarjeta form");
    const aviso = document.getElementById("aviso_demo");

    formulario.addEventListener("submit", function (evento) {
        evento.preventDefault();

        const destino = formulario.dataset.demo;

        if(destino)
        {
            window.location.href = destino;
        }

        else
        {
            aviso.textContent = "Modo demo: aqui se enviara un correo para recuperar tu contraseña";
        }
    });
}