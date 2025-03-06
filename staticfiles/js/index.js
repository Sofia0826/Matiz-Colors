document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ DOM completamente cargado.");

    let listasRopa = document.querySelectorAll(".grid");

    if (listasRopa.length === 0) {
        console.warn("⚠️ No se encontraron productos en la página.");
        return;
    }

    console.log("✅ Listas de productos detectadas:", listasRopa);

    listasRopa.forEach(lista => {
        lista.addEventListener("click", function (e) {
            if (e.target.classList.contains("ver-detalles")) {
                const item = e.target.closest(".items");
                if (item) {
                    abrirModal(item);
                }
            }
        });
    });

    function abrirModal(item) {
        document.getElementById('modal-titulo').textContent = item.getAttribute("data-title") || 'Sin título';
        document.getElementById('modal-precio').textContent = item.getAttribute("data-price") ? `$${item.getAttribute("data-price")}` : 'Precio no disponible';
        document.getElementById('modal-imagen').src = item.getAttribute("data-image") || '';
        document.getElementById('modal-agregar-carrito').dataset.id = item.getAttribute("data-id");

        document.getElementById('detalle-modal').style.display = "block";
        document.getElementById('modal-overlay').style.display = "block";
    }

    document.getElementById("modal-close").addEventListener("click", cerrarModal);
    document.getElementById("modal-overlay").addEventListener("click", cerrarModal);

    function cerrarModal() {
        document.getElementById('detalle-modal').style.display = "none";
        document.getElementById('modal-overlay').style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector('header');

    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;

        if (scrollTop > 50) {
            // Al bajar, el menú se vuelve semi-transparente
            header.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        } else {
            // Al subir, el menú vuelve a ser blanco sólido
            header.style.backgroundColor = 'rgba(255, 255, 255, 0.0)';
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const userIcon = document.querySelector(".user-icon");
    const userMenu = document.querySelector(".user-menu");

    userIcon.addEventListener("click", function (event) {
        event.preventDefault();
        userMenu.classList.toggle("show-menu");
    });

    // Cerrar el menú si el usuario hace clic fuera
    document.addEventListener("click", function (event) {
        if (!userIcon.contains(event.target) && !userMenu.contains(event.target)) {
            userMenu.classList.remove("show-menu");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let cartCount = document.getElementById("cart-count");
    let cartTotal = document.getElementById("cart-total");
    let cartItemsContainer = document.querySelector(".cart-items");
    let checkoutButton = document.getElementById("checkout");
    let clearCartButton = document.getElementById("clear-cart");

    let cart = [];

    function updateCart() {
        cartItemsContainer.innerHTML = "";
        let total = 0;

        cart.forEach((item, index) => {
            let cartItem = document.createElement("div");
            cartItem.innerHTML = `
                <p>${item.name} - $${item.price}</p>
                <button onclick="removeFromCart(${index})">Eliminar</button>
            `;
            cartItemsContainer.appendChild(cartItem);
            total += item.price;
        });

        cartCount.textContent = cart.length;
        cartTotal.textContent = `$${total.toFixed(2)}`;
    }

    window.addToCart = function (name, price) {
        cart.push({ name, price });
        updateCart();
    };

    window.removeFromCart = function (index) {
        cart.splice(index, 1);
        updateCart();
    };

    clearCartButton.addEventListener("click", function () {
        cart = [];
        updateCart();
    });

    checkoutButton.addEventListener("click", function () {
        alert("Redirigiendo a la pasarela de pago...");
    });
});