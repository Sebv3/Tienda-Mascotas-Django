from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=50)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', default='media/default.png')
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'