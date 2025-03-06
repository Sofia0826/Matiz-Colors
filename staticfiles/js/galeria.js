document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("detalle-modal");
    const modalOverlay = document.getElementById("modal-overlay");
    const modalClose = document.getElementById("modal-close");
    const modalImagen = document.getElementById("modal-imagen");
    const modalTitulo = document.getElementById("modal-titulo");
    const modalPrecio = document.getElementById("modal-precio");
    const btnAgregarCarrito = document.getElementById("modal-agregar-carrito");

    // Imagen por defecto en caso de error
    const imagenDefecto = "/static/img/default.jpg";
    
    // Variable para almacenar el ID del producto actual
    let productoActualId;

    // Función para abrir el modal con los datos del producto
    function abrirModal(item) {
        const imgSrc = item.dataset.img || imagenDefecto;
        const titulo = item.dataset.title || "Producto sin nombre";
        const precio = item.dataset.price ? parseFloat(item.dataset.price) : 0;
        const descuento = item.dataset.discount ? parseFloat(item.dataset.discount) : 0;
        
        // Guardar el ID del producto actual
        productoActualId = item.dataset.id;

        // Mostrar precio con descuento si existe
        const precioFinal = descuento > 0 ? `$${descuento}` : `$${precio}`;

        modalImagen.src = imgSrc;
        modalTitulo.textContent = titulo;
        modalPrecio.textContent = "Precio: " + precioFinal;

        modal.style.display = "block";
        modalOverlay.style.display = "block";
    }

    // Función para cerrar el modal
    function cerrarModal() {
        modal.style.display = "none";
        modalOverlay.style.display = "none";
    }

    // Evento para abrir el modal al hacer clic en "Ver Detalles"
    document.querySelectorAll(".ver-detalles").forEach(button => {
        button.addEventListener("click", function () {
            const item = this.closest(".items");
            abrirModal(item);
        });
    });

    // Cerrar modal al hacer clic en el botón de cerrar
    modalClose.addEventListener("click", cerrarModal);

    // Cerrar modal al hacer clic fuera de él
    modalOverlay.addEventListener("click", cerrarModal);

    // Cerrar modal con la tecla "Esc"
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            cerrarModal();
        }
    });

    // Agregar producto al carrito
    btnAgregarCarrito.addEventListener("click", function () {
        if (!productoActualId) {
            alert("Error: No se pudo identificar el producto");
            return;
        }
        
        const talla = document.getElementById("tallas").value;
        const color = document.getElementById("colores").value;
        
        // Crear un formulario para enviar los datos
        const form = document.createElement("form");
        form.method = "POST";
        form.action = `/agregar/${productoActualId}/`;
        
        // Añadir CSRF token
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const csrfInput = document.createElement("input");
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = csrfToken;
        
        // Añadir talla y color
        const tallaInput = document.createElement("input");
        tallaInput.type = "hidden";
        tallaInput.name = "talla";
        tallaInput.value = talla;
        
        const colorInput = document.createElement("input");
        colorInput.type = "hidden";
        colorInput.name = "color";
        colorInput.value = color;
        
        // Añadir inputs al formulario
        form.appendChild(csrfInput);
        form.appendChild(tallaInput);
        form.appendChild(colorInput);
        
        // Añadir al documento y enviar
        document.body.appendChild(form);
        form.submit();
    });
});