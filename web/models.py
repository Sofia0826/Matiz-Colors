from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    LINEA_CHOICES = [
        ('niña', 'Niña'),
        ('mujer', 'Mujer'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    linea = models.CharField(max_length=10, choices=LINEA_CHOICES, default='mujer')  
    visible = models.BooleanField(default=True)  


    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    

class CarritoItem(models.Model):
    TALLA_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    talla = models.CharField(max_length=2, choices=TALLA_CHOICES, default='M')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def subtotal(self):
        return self.producto.precio * self.cantidad 



class Datos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Orden(models.Model): 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    nombre = models.CharField(max_length=200) 
    email = models.EmailField() 
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, default="Sin dirección")  
    ciudad = models.CharField(max_length=100, null=True, blank=True)     
    sesion_id = models.CharField(max_length=100, null=True, blank=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=[('nequi', 'Nequi'), ('bancolombia', 'Bancolombia')]) 
    comprobante = models.ImageField(upload_to='comprobantes/', null=True, blank=True)  
    fecha_creacion = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return f"Orden #{self.id} - {self.nombre}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value set here

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
    
    def calcular_subtotal(self): 
        return self.precio * self.cantidad
