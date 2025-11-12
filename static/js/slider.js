let indice = 0;
mostrarImagen(indice);

function moverSlider(n) {
  mostrarImagen(indice += n);
}

function mostrarImagen(n) {
  const imagenes = document.querySelectorAll(".hero-image");
  if (n >= imagenes.length) indice = 0;
  if (n < 0) indice = imagenes.length - 1;

  imagenes.forEach(img => img.classList.remove("active"));
  imagenes[indice].classList.add("active");
}

// Cambio automático cada 5 segundos
setInterval(() => {
  moverSlider(1);
}, 5000);
