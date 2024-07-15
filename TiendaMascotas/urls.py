from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from CarritoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="Index"),
    path('signup/', views.signup, name='signup'),
    path('tienda/', views.tienda, name="Tienda"),
    path('agregar/<int:producto_id>/', views.agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', views.restar_producto, name="Sub"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),
    path('contacto/', views.contacto, name="contacto"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('juguetesPerros/', views.juguetesPerros, name="juguetesPerros"),
    path('login/', views.login, name="login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
