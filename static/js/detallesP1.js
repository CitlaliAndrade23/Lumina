// static/js/detallesP1.js

document.addEventListener("DOMContentLoaded", () => {
  // ---------- MODAL Y OVERLAY ----------
  const modal   = document.getElementById("paymentModal");
  const overlay = document.getElementById("paymentOverlay");

  const openButtons   = document.querySelectorAll(".js-open-custom-modal");
  const cancelButtons = document.querySelectorAll(".js-cancel-modal");
  const payButton     = document.querySelector(".payButton");

  const sizeButtons  = document.querySelectorAll(".size-btn");
  const colorButtons = document.querySelectorAll(".color-circle");

  const customTextInput = document.getElementById("customText");
  const notesInput      = document.getElementById("notes");

  // estado actual
  let selectedSize  = null;
  let selectedColor = null;
  let currentAction = "add";  // "add" o "buy"
  let currentSlug   = null;

  // ---------- helpers ----------
  function showModal() {
    if (!modal || !overlay) return;
    modal.style.display = "flex";
    overlay.style.display = "block";
  }

  function hideModal() {
    if (!modal || !overlay) return;
    modal.style.display = "none";
    overlay.style.display = "none";
  }

  // ---------- abrir modal desde los botones ----------
  openButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const slug = btn.dataset.productSlug;
      const action = btn.dataset.action || "add";

      if (!slug) {
        console.error("Falta data-product-slug en el botón.");
        return;
      }

      currentSlug   = slug;
      currentAction = action;
      showModal();
    });
  });

  // ---------- cerrar modal ----------
  if (overlay) {
    overlay.addEventListener("click", hideModal);
  }

  cancelButtons.forEach((btn) => {
    btn.addEventListener("click", hideModal);
  });

  // ---------- seleccionar tamaño ----------
  sizeButtons.forEach((btn, index) => {
    // Marca el primero por default
    if (index === 0) {
      btn.classList.add("active");
      selectedSize = btn.dataset.size;
    }

    btn.addEventListener("click", () => {
      sizeButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      selectedSize = btn.dataset.size;
    });
  });

  // ---------- seleccionar color ----------
  colorButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      colorButtons.forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");
      selectedColor = btn.dataset.color;
    });
  });

  // ---------- Confirmar compra / agregar ----------
  if (payButton) {
    payButton.addEventListener("click", async (e) => {
      e.preventDefault();

      if (!currentSlug) {
        alert("No se reconoce el producto.");
        return;
      }

      // Asegurar que haya un tamaño
      if (!selectedSize) {
        const activeSize = document.querySelector(".size-btn.active") || sizeButtons[0];
        if (activeSize) {
          selectedSize = activeSize.dataset.size;
        }
      }

      if (!selectedSize) {
        alert("Por favor elige una medida.");
        return;
      }

      const customText = (customTextInput?.value || "").trim();
      const notes      = (notesInput?.value || "").trim();

      const payload = {
        qty: 1,
        size: selectedSize,
        color: selectedColor || "",
        custom_text: customText,
        notes: notes,
        action: currentAction
      };

      try {
        const resp = await fetch(`/agregar/${currentSlug}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });

        const data = await resp.json().catch(() => ({}));

        if (!resp.ok || !data.ok) {
          alert(data.error || "No se pudo agregar al carrito.");
          return;
        }

        // Actualizar contador del carrito si existe
        if (typeof data.cart_count !== "undefined") {
          const cartCountEl = document.querySelector(".js-cart-count");
          if (cartCountEl) {
            cartCountEl.textContent = data.cart_count;
          }
        }

        if (currentAction === "buy") {
          // Ir directo al carrito
          window.location.href = "/carrito";
        } else {
          // Solo agregar
          hideModal();
          alert("Producto agregado al carrito.");
        }
      } catch (err) {
        console.error(err);
        alert("Error de conexión con el servidor.");
      }
    });
  }
});
