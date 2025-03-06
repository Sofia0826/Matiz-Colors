from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User  
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import JsonResponse
from .models import Producto, Categoria, Perfil
from decimal import  InvalidOperation
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import json
import logging
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import CarritoItem, Orden, OrdenItem, Datos
from .forms import OrdenForm
from django.core.mail import EmailMessage
from django.conf import settings
import os
from decimal import Decimal


# Configurar logging
logger = logging.getLogger(__name__)

# Vista principal
def home(request):
    return render(request, 'home.html')

# Vista para galería de productos por sección
def galeria(request, seccion, template_name):
    categorias = Categoria.objects.filter(producto__seccion=seccion).distinct()
    productos = Producto.objects.filter(seccion=seccion, visible=True)
    
    for producto in productos:
        try:
            descuento = getattr(producto, 'descuento', None)
            producto.precio_final = descuento if descuento else producto.precio
        except (InvalidOperation, ValueError):
            producto.precio_final = producto.precio  
    
    if not productos.exists():
        messages.error(request, f"No hay productos disponibles para la sección {seccion.capitalize()}.")
    
    return render(request, template_name, {'categorias': categorias, 'productos': productos})

def mujer(request):
    producto_lista = Producto.objects.filter(linea='mujer', visible=True)

    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id', "").strip()  # Aseguramos que no sea None o vacío
        talla = request.POST.get('talla', 'M')  # Default a M si no está

        if not producto_id.isdigit():
            messages.error(request, "ID del producto inválido.")
            return redirect('niña')

        print(f"📌 ID del producto recibido: {producto_id}")  # Para depuración

        try:
            producto = Producto.objects.get(id=int(producto_id), linea='mujer', visible=True)
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    sesion_id=sesion_id,
                    usuario=None,
                    talla=talla,
                    defaults={'cantidad': 1}
                )
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None,
                    talla=talla,
                    defaults={'cantidad': 1}
                )
            
            if not created:
                carrito_item.cantidad += 1
                carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
    
    return render(request, 'mujer.html', {'productos': producto_lista})

def niña(request):
    producto_lista = Producto.objects.filter(linea='niña', visible=True)

    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id', "").strip()  # Aseguramos que no sea None o vacío
        talla = request.POST.get('talla', 'M')  # Default a M si no está

        if not producto_id.isdigit():
            messages.error(request, "ID del producto inválido.")
            return redirect('niña')

        print(f"📌 ID del producto recibido: {producto_id}")  # Para depuración

        try:
            producto = Producto.objects.get(id=int(producto_id), linea='niña', visible=True)
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    sesion_id=sesion_id,
                    usuario=None,
                    talla=talla,
                    defaults={'cantidad': 1}
                )
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None,
                    talla=talla,
                    defaults={'cantidad': 1}
                )
            
            if not created:
                carrito_item.cantidad += 1
                carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
    
    return render(request, 'niña.html', {'productos': producto_lista})

# Vista sobre nosotros
def conocenos(request):
    return render(request, 'conocenos.html')

# Vista para compras (responde con JSON)
def compras(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos no válidos'}, status=400)
        return JsonResponse({'message': 'Compra realizada'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista de Registro
def register(request):
    if request.method == "POST":
        userName = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
        elif User.objects.filter(username=userName).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            user = User.objects.create_user(username=userName, email=email, password=password)
            auth_login(request, user)
            messages.success(request, "Registro exitoso! Ahora puedes continuar con tu compra.")

            # Redirigir a la página desde donde vino
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)

    return render(request, 'register.html')

# Vista de Login
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password: 
            messages.error(request, 'Por favor, ingrese ambos campos.')
            return render(request, 'home.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'login.html')

# Cerrar sesión
def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Sesión cerrada exitosamente")
        return redirect('login')
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista de Contacto
def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        mensaje = request.POST.get("mensaje")

        mensaje_completo = f"Nombre: {nombre}\nCorreo: {email}\nTeléfono: {telefono}\n\nMensaje:\n{mensaje}"

        send_mail(
            subject="Nuevo mensaje de contacto",
            message=mensaje_completo,
            from_email="mpimentelplaza@gmail.com", 
            recipient_list=["mariasofiapimentelplaza@gmail.com"],  
            fail_silently=False,
        )

        messages.success(request, "Tu mensaje ha sido enviado con éxito.")
        return redirect("contacto")

    return render(request, "contacto.html")

# Vista para Restablecer Contraseña
def restablecer(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(reverse('cambiar_contrasena', args=[uid, token]))  

            send_mail(
                "Restablecimiento de contraseña",
                f"Haz clic en el siguiente enlace para cambiar tu contraseña: {enlace}",
                "jalmpa77@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Se ha enviado un enlace de restablecimiento a su correo.")
            return redirect("home")
        else:
            messages.error(request, "No se encontró un usuario con ese correo electrónico.")
            return redirect("restablecer")

    return render(request, "restablecer.html")

def cambiar_contrasena(request, uidb64, token):  
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contraseña = request.POST.get("password")
            confirmar_contraseña = request.POST.get("confirm_password")

            if nueva_contraseña == confirmar_contraseña:
                user.set_password(nueva_contraseña)
                user.save()
                messages.success(request, "Tu contraseña ha sido cambiada con éxito.")
                return redirect("password_changed")
            else:
                messages.error(request, "Las contraseñas no coinciden.")

        return render(request, "cambiar_contrasena.html") 
    else:
        messages.error(request, "El enlace para restablecer la contraseña no es válido o ha expirado.")
        return redirect("login")

def password_changed(request):
    return render(request, "password_changed.html")

# Vista de perfil de usuario
@login_required                                                                                         
def perfil(request):
    user_profile, created = Perfil.objects.get_or_create(user=request.user)
    return render(request, "perfil.html", {"user_profile": user_profile, "user": request.user})


def enviar_correo_confirmacion(orden):
    asunto = f"Confirmación de tu pedido #{orden.id}"
    mensaje = f"""
📢 **Nuevo Pedido Recibido** 📢

🛍 **Detalles del Pedido**:
- Número de Pedido: {orden.id}
- Cliente: {orden.nombre}
- Correo: {orden.email}
- Teléfono: {orden.telefono}
- Dirección: {orden.direccion}
- Ciudad: {orden.ciudad if orden.ciudad else 'No especificada'}
- Total: ${orden.total:.2f}
- Método de Pago: {orden.metodo_pago}
- Fecha: {orden.fecha_creacion.strftime('%d/%m/%Y %H:%M')}

📦 **Productos Comprados**:
"""
    
    try:
        send_mail(
            asunto,
            mensaje,
            'mariasofiapimentelplaza@gmail.com',
            [orden.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error al enviar el correo de confirmación: {e}")




def ver_carrito(request):
    carrito_items = []
    total = Decimal("0.00")

    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)

    for item in carrito_items:
        total += item.producto.precio * item.cantidad 

    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })



# Actualizar cantidad en el carrito
def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            
            messages.success(request, "Carrito actualizado")
        else:
            messages.error(request, "No tienes permiso para modificar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

# Eliminar producto del carrito
def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            item.delete()
            messages.success(request, "Item eliminado del carrito")
        else:
            messages.error(request, "No tienes permiso para eliminar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

# Envío de correo de confirmación al cliente
def enviar_correo_empresa(orden):
    asunto = f"Nuevo Pedido #{orden.id} - Notificación para la empresa"
    mensaje = f"""
📢 **Nuevo Pedido Recibido** 📢

🛍 **Detalles del Pedido**:
- Número de Pedido: {orden.id}
- Cliente: {orden.nombre}
- Correo: {orden.email}
- Teléfono: {orden.telefono}
- Dirección: {orden.direccion}
- Ciudad: {orden.ciudad if orden.ciudad else 'No especificada'}
- Total: ${orden.total:.2f}
- Método de Pago: {orden.metodo_pago}
- Fecha: {orden.fecha_creacion.strftime('%d/%m/%Y %H:%M')}
- Comprobante: {'Adjunto' if orden.comprobante else 'No proporcionado'}

📦 **Productos Comprados**:
"""

    items = OrdenItem.objects.filter(orden=orden)
    for item in items:
        precio_unitario = item.precio
        mensaje += f"\n- {item.cantidad} x {item.producto.nombre} (${precio_unitario:.2f} c/u)"

    mensaje += "\n\nPor favor, revisa el sistema para gestionar el pedido."

    email = EmailMessage(
        asunto,
        mensaje,
        'mariasofiapimentelplaza@gmail.com',  # Correo de la tienda
        ['mariasofiapimentelplaza@gmail.com'],  # Destinatarios
    )

    # Adjuntar el comprobante si existe
    if orden.comprobante:
        comprobante_path = os.path.join(settings.MEDIA_ROOT, str(orden.comprobante))
        if os.path.exists(comprobante_path):
            email.attach_file(comprobante_path)

    try:
        email.send()
    except Exception as e:
        logger.error(f"Error al enviar el correo a la empresa: {e}")

# Pasarela de pago
def pasarela(request):
    carrito_items = []
    total = 0

    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    elif request.session.session_key:
        carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)

    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('carrito')

    total = sum(item.subtotal() for item in carrito_items)

    if request.method == 'POST':
        form = OrdenForm(request.POST, request.FILES)
        metodo_pago = request.POST.get('metodo_pago')

        if form.is_valid() and metodo_pago:
            orden = form.save(commit=False)
            if request.user.is_authenticated:
                orden.usuario = request.user
            else:
                orden.sesion_id = request.session.session_key

            orden.total = total
            orden.metodo_pago = metodo_pago
            
            # Guardar el comprobante si fue proporcionado
            if 'comprobante' in request.FILES:
                orden.comprobante = request.FILES['comprobante']
                
            orden.save()
            
            orden_items = [] 
            total = 0 

            for item in carrito_items:
                producto = item.producto  
                cantidad = item.cantidad
                precio = producto.precio  

                orden_item = OrdenItem.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad=cantidad,
                    precio=precio
                )

                subtotal = orden_item.calcular_subtotal()  

                total += subtotal 

                orden_items.append(orden_item)

            CarritoItem.objects.filter(id__in=carrito_items.values_list('id', flat=True)).delete()
            
  
            enviar_correo_confirmacion(orden)
            enviar_correo_empresa(orden)

            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmacion', orden_id=orden.id)
        else:
            if not metodo_pago:
                messages.error(request, "Por favor selecciona un método de pago válido.")
            else:
                messages.error(request, "Por favor completa todos los campos requeridos.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            try:
                datos = Datos.objects.get(usuario=request.user)
                initial_data = {
                    'nombre': f"{datos.nombre} {datos.apellido}",
                    'email': request.user.email
                }
            except Datos.DoesNotExist:
                initial_data = {
                    'nombre': request.user.username,
                    'email': request.user.email
                }

        form = OrdenForm(initial=initial_data)

    return render(request, 'pasarela.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })



# Confirmación de orden
def confirmacion(request, orden_id):
    try:
        if request.user.is_authenticated:
            orden = Orden.objects.prefetch_related('items').get(id=orden_id, usuario=request.user)
        elif request.session.session_key:
            orden = Orden.objects.prefetch_related('items').get(id=orden_id, sesion_id=request.session.session_key)
        else:
            messages.error(request, "No tienes permisos para ver esta orden.")
            return redirect('productos')

        # Now you can access the related 'OrdenItem' objects through 'items'
        items = orden.items.all()  # This uses the 'related_name' 'items'
        return render(request, 'confirmacion.html', {'orden': orden})
    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada.")
        return redirect('home')