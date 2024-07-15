from django.contrib import admin
from .models import Producto

# Register your models here.


@admin.register(Producto)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'imagen')
    list_editable = ('precio',)