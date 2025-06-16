function scrollToResaltado() {
    const target = document.querySelector('.resaltado');
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
    }
}
window.addEventListener('resize', () => {
    clearTimeout(window.__resizeTimeout);
    window.__resizeTimeout = setTimeout(scrollToResaltado, 200);
});

 // Ejecutar al cargar
  window.addEventListener('load', scrollToResaltado);
  document.addEventListener('DOMContentLoaded', scrollToResaltado);

  // Intentar también un retraso (por si tarda en cargar)
  setTimeout(scrollToResaltado, 100);

  // Intentar más veces si es necesario
  let intentos = 0;
  const intervalo = setInterval(() => {
    scrollToResaltado();
    intentos++;
    if (intentos > 5) clearInterval(intervalo);
  }, 300);

