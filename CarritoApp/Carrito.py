from babel.numbers import format_currency
from CarritoApp.models import Producto, CarritoUsuario, ItemCarrito

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.carrito = self.session.get("carrito", {})
        
        # Si el usuario está autenticado, carga el carrito desde la base de datos
        if request.user.is_authenticated:
            self.cargar_carrito_persistente()

    def cargar_carrito_persistente(self):
        carrito_usuario, _ = CarritoUsuario.objects.get_or_create(usuario=self.request.user)
        for item in carrito_usuario.items.all():
            self.carrito[str(item.producto.id)] = {
                "producto_id": item.producto.id,
                "nombre": item.producto.nombre,
                "precio": item.producto.precio,
                "acumulado": item.producto.precio * item.cantidad,
                "cantidad": item.cantidad,
                "imagen": item.producto.imagen.url,
            }
        self.guardar_carrito()

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito:
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "acumulado": producto.precio,
                "cantidad": 1,
                "imagen": producto.imagen.url,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.precio

        self.guardar_carrito()
        if self.request.user.is_authenticated:
            self.guardar_carrito_persistente(producto)

    def guardar_carrito_persistente(self, producto):
        carrito_usuario, _ = CarritoUsuario.objects.get_or_create(usuario=self.request.user)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito_usuario, producto=producto)
        if not created:
            item.cantidad += 1
        item.save()

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
            if self.request.user.is_authenticated:
                self.eliminar_producto_persistente(producto)

    def eliminar_producto_persistente(self, producto):
        carrito_usuario = CarritoUsuario.objects.get(usuario=self.request.user)
        ItemCarrito.objects.filter(carrito=carrito_usuario, producto=producto).delete()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            if self.carrito[id]["cantidad"] > 1:
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["acumulado"] -= producto.precio
                if self.request.user.is_authenticated:
                    self.restar_producto_persistente(producto)
            else:
                self.eliminar(producto)

    def restar_producto_persistente(self, producto):
        carrito_usuario = CarritoUsuario.objects.get(usuario=self.request.user)
        item = ItemCarrito.objects.get(carrito=carrito_usuario, producto=producto)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete() 

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
        if self.request.user.is_authenticated:
            carrito_usuario = CarritoUsuario.objects.get(usuario=self.request.user)
            carrito_usuario.items.all().delete()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def formatear_precio(self, precio):
        return format_currency(precio, 'CLP', locale='es_CL')