document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".avatar-card");

  cards.forEach(card => {
    card.addEventListener("click", () => {

      // Si ya está activa, la desactivamos (toggle)
      if (card.classList.contains("active-card")) {
        card.classList.remove("active-card");
        return;
      }

      // Quitamos active de todas
      cards.forEach(c => c.classList.remove("active-card"));

      // Activamos la clickeada
      card.classList.add("active-card");
    });
  });
});
