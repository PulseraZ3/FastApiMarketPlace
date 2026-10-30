const casilla = document.getElementById("mostrar_password");
const campo_password = document.getElementById("password");

casilla.addEventListener("change", function (){
    campo_password.type = casilla.checked ? "text" : "password";
});