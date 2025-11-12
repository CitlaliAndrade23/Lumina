// === IMAGEN PRINCIPAL Y COLORES ===

// Imagen del producto
const productImg = document.querySelector(".productImg");

// Botones de color (los <div class="color" data-img="...">)
const colorButtons = document.querySelectorAll(".color");

// Cuando haces clic en un color, cambia la imagen según su data-img
colorButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const newSrc = btn.dataset.img;   // lee el atributo data-img
    if (newSrc) {
      productImg.src = newSrc;
    }
  });
});

// === TAMAÑOS ===
const currentProductSizes = document.querySelectorAll(".size");

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

// === MODAL DE PAGO ===
const productButton = document.querySelector(".productButton");
const payment = document.querySelector(".payment");
const close = document.querySelector(".close");

if (productButton && payment && close) {
  productButton.addEventListener("click", () => {
    payment.style.display = "flex";
  });

  close.addEventListener("click", () => {
    payment.style.display = "none";
  });
}

// === TABS (Reseñas / Materiales) ===
const tabs = document.querySelectorAll(".tab-button");
const contents = document.querySelectorAll(".tab-content");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    contents.forEach((c) => c.classList.remove("active"));

    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});
