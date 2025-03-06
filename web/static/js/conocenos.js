// Variables
const carrito = document.getElementById("carrito"), 
listaropa = document.getElementById("lista-ropa"),
contenedorcarrito = document.querySelector('.buy-card .lista'),
vaciarcarritobtn = document.querySelector('#vaciar_carrito');

let articuloCarrito = [];

registrareventslisteners();

function registrareventslisteners() {
    // Cuando le de click a "Agregar al carrito"
    listaropa.addEventListener('click', agregarropa);

    // Eliminar producto del carrito
    carrito.addEventListener('click', eliminarproducto);

    //vaciar el carrito
    vaciarcarritobtn.addEventListener('click', e => {
        articuloCarrito = [];
        limpiarHTML()
    })

}

function agregarropa(e) {
    if (e.target.classList.contains("agregar-carrito")) {
        const cursoseleccionado = e.target.parentElement.parentElement;
        leerInfo(cursoseleccionado);
    }
}

// Elimina un producto del carrito
function eliminarproducto(d) {
    if (d.target.classList.contains("borrar")) {  // Cambio de "borrar-ropa" a "borrar"
        const ropaId = d.target.getAttribute('data-id');
        
        // Eliminar del arreglo articuloCarrito por el data-id
        articuloCarrito = articuloCarrito.filter(ropa => ropa.id !== ropaId);

        carritoHTML();
    }
}

// Extraer la info del artículo seleccionado
function leerInfo(ropa) {
    // Crear un objeto con la información del producto
    const inforopa = {
        image: ropa.querySelector('img').src,
        titulo: ropa.querySelector('h3').textContent,
        precio: ropa.querySelector('.descuento').textContent, 
        id: ropa.querySelector('button').getAttribute('data-id'),
        cantidad: 1
    };

    // Revisa si un elemento ya existe en el carrito
    const existe = articuloCarrito.some(ropa => ropa.id == inforopa.id);

    if (existe) {
        // Actualizar la cantidad
        articuloCarrito = articuloCarrito.map(ropa => { 
            if (ropa.id == inforopa.id) {
                ropa.cantidad++;
                return ropa;
            } else {
                return ropa;
            }
        });
    } else {
        // Agregar elementos al carrito de compras
        articuloCarrito = [...articuloCarrito, inforopa];
    }

    carritoHTML();
}

// Muestra el carrito en el HTML
function carritoHTML() {
    limpiarHTML();

    // Recorrer el carrito y generar el HTML
    articuloCarrito.forEach(ropa => {
        const fila = document.createElement('div');
        fila.innerHTML = `
            <img src="${ropa.image}">
            <p>${ropa.titulo}</p>
            <p>${ropa.precio}</p>
            <p>${ropa.cantidad}</p>
            <p><span class="borrar" data-id="${ropa.id}">X</span></p> 
        `;

        contenedorcarrito.appendChild(fila);
    });
}

// Elimina los productos de la lista
function limpiarHTML() {
    while (contenedorcarrito.firstChild) {
        contenedorcarrito.removeChild(contenedorcarrito.firstChild);
    }
}
