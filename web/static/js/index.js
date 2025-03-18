document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM completamente cargado.");

    initModal();
    initScrollEffect();
    initSearch();

    function initModal() {
        const botonesDetalles = document.querySelectorAll(".ver-detalles");

        if (!botonesDetalles.length) {
            console.warn("⚠️ No hay botones de 'Ver detalles'.");
            return;
        }

        botonesDetalles.forEach((boton) => {
            boton.addEventListener("click", () => {
                console.log("🛍️ Botón de detalles clickeado.");

                const item = boton.closest(".items");

                if (!item) {
                    console.error("❌ No se encontró el contenedor del producto.");
                    return;
                }

                abrirModal(item);
            });
        });

        document.getElementById("modal-close")?.addEventListener("click", cerrarModal);
        document.getElementById("modal-overlay")?.addEventListener("click", cerrarModal);
        
        // Actualizar talla cuando cambia el selector
        const tallasSelect = document.getElementById('tallas');
        const modalTallaInput = document.getElementById('modal-talla-seleccionada');
        
        if (tallasSelect && modalTallaInput) {
            tallasSelect.addEventListener('change', function() {
                modalTallaInput.value = this.value;
                console.log("📏 Talla seleccionada:", this.value);
            });
        }
        
        // Actualizar color cuando cambia el selector (si existe)
        const coloresSelect = document.getElementById('colores');
        const modalColorInput = document.getElementById('modal-color-seleccionado');
        
        if (coloresSelect && modalColorInput) {
            coloresSelect.addEventListener('change', function() {
                modalColorInput.value = this.value;
                console.log("🎨 Color seleccionado:", this.value);
            });
        }
    }

    function abrirModal(item) {
        const modal = document.getElementById("detalle-modal");
        const overlay = document.getElementById("modal-overlay");
        const productoId = item.dataset.id;

        if (!modal || !overlay) {
            console.error("❌ No se encontraron los elementos del modal.");
            return;
        }

        // Actualizar contenido del modal
        document.getElementById("modal-titulo").textContent = item.dataset.title || "Sin título";
        document.getElementById("modal-imagen").src = item.dataset.img || "";
        document.getElementById("modal-precio").textContent = `$${(parseFloat(item.dataset.price) || 0).toFixed(2)}`;
        
        // IMPORTANTE: Establecer el ID del producto en el campo oculto del formulario
        const productoIdInput = document.getElementById("modal-producto-id");
        if (productoIdInput) {
            productoIdInput.value = productoId;
            console.log("🆔 ID del producto establecido:", productoId);
        } else {
            console.error("❌ No se encontró el campo oculto para el ID del producto");
        }

        modal.style.display = "block";
        overlay.style.display = "block";
    }

    function cerrarModal() {
        document.getElementById("detalle-modal").style.display = "none";
        document.getElementById("modal-overlay").style.display = "none";
    }

    function initScrollEffect() {
        const header = document.querySelector("header");
        if (!header) {
            console.warn("⚠️ No se encontró el header.");
            return;
        }
        window.addEventListener("scroll", function () {
            header.classList.toggle("header-scrolled", window.scrollY > 50);
        });
    }

    function initSearch() {
        const searchInput = document.getElementById("search-input");
        const searchButton = document.getElementById("search-button");
        const productos = document.querySelectorAll(".producto-item");
        const categorias = document.querySelectorAll(".subcategoria-titulo");
        const noResults = document.getElementById("no-results");

        if (!searchInput || !searchButton) {
            console.warn("⚠️ No se encontraron elementos clave de búsqueda.");
            return;
        }

        if (!productos.length) {
            console.warn("⚠️ No se encontraron productos para la búsqueda.");
        }

        function realizarBusqueda() {
            const terminoBusqueda = searchInput.value.toLowerCase().trim();
            let resultadosEncontrados = false;

            productos.forEach(producto => {
                const titulo = producto.dataset.title?.toLowerCase() || "";
                const descripcion = producto.dataset.descripcion?.toLowerCase() || "";
                const categoria = producto.dataset.categoria?.toLowerCase() || "";

                if (
                    titulo.includes(terminoBusqueda) ||
                    descripcion.includes(terminoBusqueda) ||
                    categoria.includes(terminoBusqueda)
                ) {
                    producto.style.display = "block";
                    resultadosEncontrados = true;
                } else {
                    producto.style.display = "none";
                }
            });

            if (categorias.length) {
                categorias.forEach(categoria => {
                    const productosVisibles = Array.from(categoria.nextElementSibling.children).some(
                        producto => producto.style.display === "block"
                    );
                    categoria.style.display = productosVisibles ? "block" : "none";
                });
            }

            if (noResults) {
                noResults.style.display = resultadosEncontrados ? "none" : "block";
            }
        }

        searchButton.addEventListener("click", realizarBusqueda);
        searchInput.addEventListener("input", realizarBusqueda);
    }

    // Añadir validación para el formulario de modal
    const modalForm = document.getElementById('modal-form');
    if (modalForm) {
        modalForm.addEventListener('submit', function(e) {
            const productoId = document.getElementById('modal-producto-id')?.value;
            if (!productoId) {
                e.preventDefault();
                console.error("❌ Intento de enviar formulario sin ID de producto");
                alert("Error: No se pudo identificar el producto");
                return false;
            }
            console.log("📦 Enviando producto al carrito:", productoId);
        });
    }
});