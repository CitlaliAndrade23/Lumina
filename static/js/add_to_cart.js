document.addEventListener("DOMContentLoaded", () => {
  // Todos los formularios de "Agregar al carrito"
  const forms = document.querySelectorAll(".js-add-to-cart-form");

  forms.forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const url = form.action;
      const formData = new FormData(form);

      try {
        const resp = await fetch(url, {
          method: "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        if (!resp.ok) {
          // Si el backend manda redirect en JSON
          try {
            const data = await resp.json();
            if (data.redirect) {
              window.location.href = data.redirect;
              return;
            }
          } catch (_) {
            // Si no es JSON, mandamos un alert simple
          }

          alert("Ocurrió un error al agregar al carrito.");
          return;
        }

        const data = await resp.json();

        if (data.redirect) {
          window.location.href = data.redirect;
          return;
        }

        if (data.ok) {
          // Actualizar contador en el navbar
          const badge = document.getElementById("cart-count");
          if (badge && typeof data.cart_count !== "undefined") {
            badge.textContent = data.cart_count;
          }

          // Mostrar modal de agregado
          const modalEl = document.getElementById("cartAddedModal");
          if (modalEl && window.bootstrap) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
          } else {
            alert("Producto añadido al carrito.");
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
