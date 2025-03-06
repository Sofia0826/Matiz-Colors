from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from web import views  
from web.views import contacto
from web.views import perfil
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('mujer/', views.mujer, name='mujer'),
    path('niña/', views.niña, name='niña'),
    path('conocenos/', views.conocenos, name='conocenos'),
    path('compras/', views.compras, name='compras'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('web/', include('web.urls')),  
    path("contacto/", contacto, name="contacto"),
    path("restablecer/", views.restablecer, name="restablecer"),
    path("cambiar_contrasena/<str:uidb64>/<str:token>/", views.cambiar_contrasena, name="cambiar_contrasena"), 
    path("password_changed/", views.password_changed, name="password_changed"),
    path("perfil/", perfil, name="perfil"),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/actualizar/<int:item_id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("carrito/eliminar/<int:item_id>/", views.eliminar_item, name="eliminar_item"),
    path('pasarela/', views.pasarela, name='pasarela'),
    path('confirmacion/<int:orden_id>/', views.confirmacion, name='confirmacion'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)