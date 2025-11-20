// static/js/ventaCompra.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("ventaCompra.js cargado");

  /* ================= SLIDER / PRODUCTO ================= */
  const wrapper = document.querySelector(".sliderWrapper");
  const menuItems = document.querySelectorAll(".menuItem");

  const products = [
    {
      id: 1,
      title: "Air Force",
      price: 119,
      colors: [
        { code: "black",    img: "/static/img/air.png"  },
        { code: "darkblue", img: "/static/img/air2.png" },
      ],
    },
    {
      id: 2,
      title: "Air Jordan",
      price: 149,
      colors: [
        { code: "lightgray", img: "/static/img/jordan.png" },
        { code: "green",     img: "/static/img/jordan2.png" },
      ],
    },
    {
      id: 3,
      title: "Blazer",
      price: 109,
      colors: [
        { code: "lightgray", img: "/static/img/blazer.png" },
        { code: "green",     img: "/static/img/blazer2.png" },
      ],
    },
    {
      id: 4,
      title: "Crater",
      price: 129,
      colors: [
        { code: "black",    img: "/static/img/crater.png" },
        { code: "lightgray", img: "/static/img/crater2.png" },
      ],
    },
    {
      id: 5,
      title: "Hippie",
      price: 99,
      colors: [
        { code: "gray",  img: "/static/img/hippie.png" },
        { code: "black", img: "/static/img/hippie2.png" },
      ],
    },
  ];

  let choosenProduct = products[0];

  const currentProductImg    = document.querySelector(".productImg");
  const currentProductTitle  = document.querySelector(".productTitle");
  const currentProductPrice  = document.querySelector(".productPrice");
  const currentProductColors = document.querySelectorAll(".color");
  const currentProductSizes  = document.querySelectorAll(".size");

  // 🔒 Solo ejecuta la lógica del slider si existen los elementos
  if (wrapper && currentProductImg && currentProductTitle && currentProductPrice) {
    menuItems.forEach((item, index) => {
      item.addEventListener("click", () => {
        wrapper.style.transform = `translateX(${-100 * index}vw)`;
        choosenProduct = products[index];
        currentProductTitle.textContent = choosenProduct.title;
        currentProductPrice.textContent = "$" + choosenProduct.price;
        currentProductImg.src = choosenProduct.colors[0].img;
        currentProductColors.forEach((color, i) => {
          if (choosenProduct.colors[i]) {
            color.style.backgroundColor = choosenProduct.colors[i].code;
          }
        });
      });
    });

    currentProductColors.forEach((color, index) => {
      color.addEventListener("click", () => {
        if (choosenProduct.colors[index]) {
          currentProductImg.src = choosenProduct.colors[index].img;
        }
      });
    });

    currentProductSizes.forEach((size) => {
      size.addEventListener("click", () => {
        currentProductSizes.forEach((s) => {
          s.style.backgroundColor = "white";
          s.style.color = "black";
        });
        size.style.backgroundColor = "black";
        size.style.color = "white";
      });
    });
  }

  /* ================= MODAL DE PERSONALIZACIÓN ================= */

  // Elementos del modal (según plantilla)
  const overlay = document.getElementById("paymentOverlay");
  const modal = document.getElementById("paymentModal");
  const sizeBtns = document.querySelectorAll(".size-btn");
  const colorCircles = document.querySelectorAll(".color-circle");
  const selectedSizeInput = document.getElementById("selectedSize");
  const selectedColorInput = document.getElementById("selectedColor");
  const customTextEl = document.getElementById("customText");
  const notesEl = document.getElementById("notes");
  const payBtn = modal ? modal.querySelector(".payButton") : null;
  const cancelBtns = document.querySelectorAll(".js-cancel-modal, #closePay");

  // Botones que abren modal (desde template)
  const openButtons = document.querySelectorAll(".js-open-custom-modal");

  let currentAction = null; // 'add' o 'buy'
  let currentProduct = { id: null, slug: null };

  // Si la página no tiene modal NI botones que lo abren, no seguimos con esta parte
  if (!modal || !overlay || openButtons.length === 0) {
    console.log("ventaCompra.js: no hay modal de personalización en esta página.");
    return;
  }

  // Seguridad: mostrar / ocultar modal
  function safeDisplayModal(show = true) {
    overlay.style.display = show ? "block" : "none";
    modal.style.display = show ? "flex" : "none";
    modal.setAttribute("aria-hidden", show ? "false" : "true");
  }

  // abrir modal desde botones
  openButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      currentAction = btn.dataset.action || "add";
      currentProduct.id = btn.dataset.productId || null;
      currentProduct.slug = btn.dataset.productSlug || null;

      // reset visuales
      if (selectedSizeInput) selectedSizeInput.value = "";
      if (selectedColorInput) selectedColorInput.value = "";
      sizeBtns.forEach((b) => b.classList.remove("active"));
      colorCircles.forEach((c) => c.classList.remove("selected"));
      if (customTextEl) customTextEl.value = "";
      if (notesEl) notesEl.value = "";

      safeDisplayModal(true);
    });
  });

  // cerrar modal
  overlay.addEventListener("click", () => safeDisplayModal(false));
  cancelBtns.forEach((b) => b.addEventListener("click", () => safeDisplayModal(false)));

  // seleccionar tamaño
  sizeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      sizeBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      if (selectedSizeInput) selectedSizeInput.value = btn.dataset.size || "";
    });
  });

  // seleccionar color
  colorCircles.forEach((circle) => {
    circle.addEventListener("click", () => {
      colorCircles.forEach((c) => c.classList.remove("selected"));
      circle.classList.add("selected");
      if (selectedColorInput) selectedColorInput.value = circle.dataset.color || "";
    });
  });

  // función util para mostrar mensajes
  function showMessage(msg) {
    if (window.toastr) {
      window.toastr.success(msg);
    } else {
      alert(msg);
    }
  }

  // Envío al backend cuando el usuario confirma en el modal
  if (payBtn) {
    payBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      // lectura de campos
      const size = selectedSizeInput ? selectedSizeInput.value : "";
      const color = selectedColorInput ? selectedColorInput.value : "";
      const custom_text = customTextEl ? customTextEl.value.trim() : "";
      const notes = notesEl ? notesEl.value.trim() : "";
      const qty = 1;

      // validaciones
      if (!size) {
        alert("Por favor selecciona una medida.");
        return;
      }
      if (!color) {
        alert("Por favor selecciona un color.");
        return;
      }

      if (!custom_text) {
        if (!confirm("No escribiste texto personalizado. ¿Deseas continuar sin texto?")) {
          return;
        }
      }

      // preparar payload
      const payload = {
        producto_id: currentProduct.id,
        producto_slug: currentProduct.slug,
        qty,
        custom_text,
        size,
        color,
        notes,
        action: currentAction,
      };

      try {
        const url = `/agregar/${encodeURIComponent(currentProduct.slug || "")}`;
        const resp = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify(payload),
          credentials: "same-origin",
        });

        if (!resp.ok) {
          const txt = await resp.text();
          throw new Error(txt || "Error en la petición");
        }

        const data = await resp.json();

        safeDisplayModal(false);

        if (currentAction === "buy") {
          window.location.href = "/carrito";
          return;
        } else {
          showMessage(data.message || "Producto agregado al carrito");
          const cartBadge = document.querySelector(".cart-count-badge");
          if (cartBadge && data.cart_count !== undefined) {
            cartBadge.textContent = data.cart_count;
          }
          const navCartCount = document.querySelector(".js-cart-count, #cart-count");
          if (navCartCount && data.cart_count !== undefined) {
            navCartCount.textContent = data.cart_count;
          }
        }
      } catch (err) {
        console.error("Error al agregar:", err);
        alert("Ocurrió un error al agregar al carrito. Intenta de nuevo.");
      }
    });
  }
}); // DOMContentLoaded
