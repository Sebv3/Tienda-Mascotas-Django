from django.contrib import admin
from .models import MensajeContacto, Pedido, Producto

# Register your models here.


@admin.register(Producto)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'imagen')
    list_editable = ('precio',)


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo', 'telefono', 'fecha_envio')  # Campos que quieres mostrar
    search_fields = ('nombre', 'apellido', 'correo')  # Permitir búsquedas
    list_filter = ('fecha_envio',)  # Filtros en el lateral


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total', 'estado')  # Columnas en la lista
    list_filter = ('estado', 'fecha')  # Filtros laterales
    search_fields = ('usuario__username', 'estado')  # Barra de búsqueda
    ordering = ('-fecha',)  # Orden predeterminado