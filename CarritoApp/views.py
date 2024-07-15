from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
from CarritoApp.Carrito import Carrito
from CarritoApp.models import Producto
from CarritoApp import views


def tienda(request):
    productos = Producto.objects.all()
    return render(request, "tienda.html", {'productos':productos})


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("Tienda")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Tienda")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Tienda")

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password1']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            return HttpResponse('Usuario creado con exito')
        return HttpResponse('Las contraseñas no coinciden')
    

def contacto(request):
    return render(request, 'contacto.html')

def juguetesPerros(request):
    return render(request, 'juguetesPerros.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def login(request):
    return render(request, 'login.html')

