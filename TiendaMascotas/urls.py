from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from CarritoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="Index"),
    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    path('tienda/', views.tienda, name="Tienda"),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name="Add"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', views.restar_producto, name="Sub"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),
    path('contacto/', views.contacto, name="contacto"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('juguetesPerros/', views.juguetesPerros, name="juguetesPerros"),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('login/', views.iniciar_sesion, name='login'),
    path('tienda', include('CarritoApp.urls')),
    path('b/', views.b, name="b"),
    path('agregar_producto/', views.agregar_producto_admin, name='agregar_producto'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),


]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
