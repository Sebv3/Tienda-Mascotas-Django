from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required



# Create your views here.
from CarritoApp.Carrito import Carrito
from CarritoApp.models import Producto
from CarritoApp import views


def tienda(request):
    productos = Producto.objects.all()
    return render(request, "tienda.html", {'productos':productos})



def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect('Tienda')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("juguetesPerros")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("juguetesPerros")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("juguetesPerros")

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

@login_required
def agregar_producto_admin(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Index')
    else:
        form = ProductoForm()
    return render(request, 'agregarProducto.html', {'form': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('Tienda')  # Redirige a la lista de productos o a otro lugar
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()  # Elimina el producto de la base de datos
    return redirect('Tienda')  # Redirige a la página de la tienda

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})
