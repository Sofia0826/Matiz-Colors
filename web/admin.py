from django.contrib import admin
from .models import Categoria, Producto, Orden, OrdenItem

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'linea', 'precio', 'visible')
    list_filter = ('categoria', 'linea', 'visible')


    # Añadir al archivo admin.py

class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0
    readonly_fields = ('calcular_subtotal',)
    
    def calcular_subtotal(self, instance):
        precio = getattr(instance, 'precio', 0) or 0
        cantidad = getattr(instance, 'cantidad', 0) or 0
        return precio * cantidad

    
    calcular_subtotal.short_description = 'Subtotal'

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'total', 'metodo_pago', 'usuario', 'sesion_id', 'fecha_creacion')
    list_filter = ('metodo_pago', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'telefono', 'usuario__username')
    date_hierarchy = 'fecha_creacion'
    inlines = [OrdenItemInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')