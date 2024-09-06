from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


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

from django.db import IntegrityError

def registrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'usuario/registrar_usuario.html', {
            'form': UserCreationForm
        })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('Index')
            except IntegrityError:
                return render(
                    request,
                    "usuario/registrar_usuario.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe"},

                )
            else:
                return render(
                    request,
                    "usuario/registrar_usuario.html",
                    {"form": UserCreationForm, "error": "Las constraseñas no coinciden"},

                )
            
def cerrar_sesion(request):
    logout(request)
    return redirect('Index')

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'usuario/login.html',{
            'form':AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(
                    request,
                    "usuario/login.html",
                    {"form": AuthenticationForm, "error": "Datos incorrectos"},

                )
        else:
            login(request,user)
            return redirect('Index')



    


    

def contacto(request):
    return render(request, 'contacto.html')

def juguetesPerros(request):
    return render(request, 'juguetesPerros.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def b(request):
    return render(request, 'b.html')

