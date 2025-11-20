// navbar.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("Navbar listo.");

    // Ejemplo si quieres manejar el menú móvil
    const menuBtn = document.querySelector(".menu-toggle");
    const navMenu = document.querySelector(".nav-links");

    if (menuBtn && navMenu) {
        menuBtn.addEventListener("click", () => {
            navMenu.classList.toggle("active");
        });
    }
});
