document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".messages div, .mensajes p");
    messages.forEach((msg) => {
        setTimeout(() => {
            msg.style.display = "none";
        }, 3000); // Oculta los mensajes después de 3 segundos
    });
});
