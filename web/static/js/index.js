document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM completamente cargado.");

    initModal();
    initCart();
    initScrollEffect(); // Agregamos la función para el efecto de scroll

    // 🔍 Modal para ver detalles de productos
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
    }
    

    function abrirModal(item) {
        const id = item.getAttribute("data-id");
        const modal = document.getElementById("detalle-modal");
        const overlay = document.getElementById("modal-overlay");
        const modalProductoId = document.getElementById("modal-producto-id");
    
        console.log("🔎 Verificando modal y overlay...");
        console.log("📌 Modal:", modal);
        console.log("📌 Overlay:", overlay);
    
        if (!modal || !overlay) {
            console.error("❌ No se encontraron los elementos del modal.");
            return;
        }
    
        console.log("✅ Modal y overlay encontrados. Procediendo a mostrar el modal...");
        
        // Extraer datos del producto desde los atributos data-*
        const titulo = item.getAttribute("data-title");
        const precio = parseFloat(item.getAttribute("data-price")) || 0;
        const imagenSrc = item.getAttribute("data-img");
        
        console.log("🛒 Producto seleccionado:", { id, titulo, precio, imagenSrc });
        
        // Insertar título, imagen y precio
        document.getElementById("modal-titulo").textContent = titulo;
        document.getElementById("modal-imagen").src = imagenSrc;
        document.getElementById("modal-precio").textContent = `$${precio.toFixed(2)}`;
        
        // Verificar que modal-producto-id existe antes de asignarle un valor
        if (modalProductoId) {
            modalProductoId.value = id;
        }
        
        // Mostrar la modal
        modal.style.display = "block";
        overlay.style.display = "block";
    }
    

    // Función para cerrar el modal
    function cerrarModal() {
        document.getElementById("detalle-modal").style.display = "none";
        document.getElementById("modal-overlay").style.display = "none";
    }
    
    // 🔥 Notificación emergente
    function showToast(message) {
        const toast = document.querySelector(".toast");
        if (!toast) return;
        toast.textContent = message;
        toast.classList.add("show");
        setTimeout(() => toast.classList.remove("show"), 3000);
    }

    // ⏳ Función debounce para optimizar eventos
    function initScrollEffect() {
        const header = document.querySelector("header");

        if (!header) {
            console.error("❌ No se encontró el header.");
            return;
        }

        window.addEventListener("scroll", function () {
            console.log("📜 Scroll detectado en posición:", window.scrollY);

            if (window.scrollY > 50) {
                header.classList.add("header-scrolled");
                console.log("✅ Clase 'header-scrolled' agregada.");
            } else {
                header.classList.remove("header-scrolled");
                console.log("🔝 Clase 'header-scrolled' eliminada.");
            }
        });
    }
});
