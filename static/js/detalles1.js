// static/js/detalles1.js
document.addEventListener("DOMContentLoaded", () => {
  // === IMAGEN PRINCIPAL Y COLORES ===
  const productImg       = document.querySelector(".productImg");
  const colorButtons     = document.querySelectorAll(".colors .color");
  const colorHiddenInput = document.getElementById("colorInput");

  function setVariantFromButton(btn) {
    if (!btn) return;

    const newSrc   = btn.dataset.img;
    const colorHex = btn.dataset.color || "";

    // Cambiar imagen grande
    if (newSrc && productImg) {
      productImg.src = newSrc;
    }

    // Marcar color activo
    colorButtons.forEach((c) => c.classList.remove("active"));
    btn.classList.add("active");

    // Guardar color + imagen en el input hidden
    if (colorHiddenInput) {
      let relativeImg = "";

      if (newSrc && newSrc.startsWith("/static/")) {
        // "/static/img/open.jpg" -> "img/open.jpg"
        relativeImg = newSrc.slice("/static/".length);
      } else if (newSrc) {
        relativeImg = newSrc;
      }

      if (colorHex && relativeImg) {
        // Ejemplo: "#0044ff|||img/open.jpg"
        colorHiddenInput.value = `${colorHex}|||${relativeImg}`;
      } else if (colorHex) {
        colorHiddenInput.value = colorHex;
      } else {
        colorHiddenInput.value = "";
      }
    }
  }

  // Click en cada color
  colorButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      setVariantFromButton(btn);
    });
  });

  // Seleccionar el primer color por defecto
  if (colorButtons.length > 0) {
    setVariantFromButton(colorButtons[0]);
  }

  // === TAMAÑOS ===
  const sizeButtons = document.querySelectorAll(".sizes .size");
  const medidaInput = document.getElementById("medidaInput");

  sizeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      sizeButtons.forEach((s) => s.classList.remove("active"));
      btn.classList.add("active");

      if (medidaInput && btn.dataset.medida) {
        medidaInput.value = btn.dataset.medida;
      }
    });
  });

  // Valor inicial de medida (el que tenga .active)
  const activeSize = document.querySelector(".sizes .size.active");
  if (activeSize && medidaInput && activeSize.dataset.medida) {
    medidaInput.value = activeSize.dataset.medida;
  }

  // === TABS (Reseñas / Materiales) ===
  const tabs     = document.querySelectorAll(".tab-button");
  const contents = document.querySelectorAll(".tab-content");

  function activateTab(name) {
    tabs.forEach((t) =>
      t.classList.toggle("active", t.dataset.tab === name)
    );
    contents.forEach((c) =>
      c.classList.toggle("active", c.id === name)
    );
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => activateTab(tab.dataset.tab));
  });

  if (tabs.length > 0) {
    activateTab(tabs[0].dataset.tab);
  }

  // === MODAL DE PAGO (solo si en algún momento usas btnComprar) ===
  const btnComprar   = document.getElementById("btnComprar");
  const paymentModal = document.getElementById("paymentModal");
  const closePay     = document.getElementById("closePay");

  if (btnComprar && paymentModal && closePay) {
    btnComprar.addEventListener("click", (e) => {
      e.preventDefault();
      paymentModal.style.display = "flex";
    });
    closePay.addEventListener("click", () => {
      paymentModal.style.display = "none";
    });
    paymentModal.addEventListener("click", (e) => {
      if (e.target === paymentModal) paymentModal.style.display = "none";
    });
  }
});
