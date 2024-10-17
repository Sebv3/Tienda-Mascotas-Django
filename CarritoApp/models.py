from django.db import models
from django.contrib.auth.models import User  # Importar el modelo User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', default='media/default.png')
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

class CarritoUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con User

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(CarritoUsuario, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"