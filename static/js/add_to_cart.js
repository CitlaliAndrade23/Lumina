// static/js/add_to_cart.js
document.addEventListener("DOMContentLoaded", () => {
  // Todos los formularios de "Agregar al carrito" y "Comprar ahora"
  const forms = document.querySelectorAll(".js-add-to-cart-form");

  forms.forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const urlRaw = form.action;
      const url = String(urlRaw || "");

      console.log("👉 Form action:", url);

      // Debe apuntar a /agregar/...
      if (url.indexOf("/agregar/") === -1) {
        console.warn("Formulario ignorado, action no es /agregar/:", url);
        alert("Hay un problema con esta página: el formulario no apunta a /agregar/. Revisa el template.");
        return;
      }

      const formData = new FormData(form);

      /* 🟣 Detectar el botón que se presionó */
      const submitter = e.submitter;
      if (submitter && submitter.name === "accion") {
        // Puede ser "add" o "buy"
        formData.set("accion", submitter.value);
      } else {
        // Si por alguna razón no trae botón, default = agregar
        formData.set("accion", "add");
      }

      try {
        const resp = await fetch(url, {
          method: "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const contentType = resp.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
          const text = await resp.text();
          console.error("Respuesta NO JSON desde", url, "status:", resp.status, "body:", text);
          alert("Ocurrió un problema al agregar al carrito. Revisa la consola.");
          return;
        }

        const data = await resp.json();

        // Si el backend manda redirect (Comprar ahora)
        if (data.redirect) {
          window.location.href = data.redirect;
          return;
        }

        // Si se agregó correctamente
        if (data.ok) {
          const badge = document.getElementById("cart-count");
          if (badge && typeof data.cart_count !== "undefined") {
            badge.textContent = data.cart_count;
          }

          const accion = formData.get("accion");
          if (accion === "add") {
            const modalEl = document.getElementById("cartAddedModal");
            if (modalEl && window.bootstrap) {
              const modal = new bootstrap.Modal(modalEl);
              modal.show();
            } else {
              alert("Producto añadido al carrito.");
            }
          }
        } else {
          alert(data.error || "No se pudo agregar al carrito.");
        }
      } catch (err) {
        console.error(err);
        alert("Error de conexión al agregar al carrito.");
      }
    });
  });
});
