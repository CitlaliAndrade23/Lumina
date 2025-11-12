document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".opinion-card");
  const modal = document.getElementById("modal-opinion");
  const modalImg = document.getElementById("modal-img");
  const modalNombre = document.getElementById("modal-nombre");
  const modalTipo = document.getElementById("modal-tipo");
  const modalTexto = document.getElementById("modal-texto");
  const cerrar = document.querySelector(".cerrar-modal");

  // Abrir modal al hacer clic en una tarjeta
  cards.forEach(card => {
    card.addEventListener("click", () => {
      const img = card.querySelector("img").src;
      const nombre = card.querySelector(".opinion-nombre").textContent;
      const tipo = card.querySelector(".opinion-tipo").textContent;
      const texto = card.querySelector(".opinion-texto").textContent;

      modalImg.src = img;
      modalNombre.textContent = nombre;
      modalTipo.textContent = tipo;
      modalTexto.textContent = texto;

      modal.style.display = "flex";
      setTimeout(() => modal.classList.add("activo"), 10);
    });
  });

  // Cerrar con la X
  cerrar.addEventListener("click", () => {
    modal.classList.remove("activo");
    setTimeout(() => (modal.style.display = "none"), 300);
  });

  // Cerrar haciendo clic fuera del contenido
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("activo");
      setTimeout(() => (modal.style.display = "none"), 300);
    }
  });
});
