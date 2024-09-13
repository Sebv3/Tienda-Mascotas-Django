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
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages





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
        return render(request, 'usuario/registrar_usuario.html')
    
    else:
        # Verificar si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Verificar si el correo ya está en uso
                if User.objects.filter(email=request.POST['email']).exists():
                    return render(request, 'usuario/registrar_usuario.html', {
                        "error": "El correo ya está registrado."
                    })
                
                # Crear usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email']  # Guardar el correo
                )
                user.save()
                login(request, user)
                return redirect('Index')
            except IntegrityError:
                return render(request, 'usuario/registrar_usuario.html', {
                    "error": "El usuario ya existe"
                })
        else:
            return render(request, 'usuario/registrar_usuario.html', {
                "error": "Las contraseñas no coinciden"
            })
            
def cerrar_sesion(request):
    logout(request)
    return redirect('Index')

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'usuario/login.html', {
            'form': AuthenticationForm
        })
    else:
        email = request.POST['username']  # El campo 'username' se usa para capturar el correo
        password = request.POST['password']
        
        # Buscar el usuario por correo
        try:
            user = get_user_model().objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Index')
            else:
                return render(request, 'usuario/login.html', {
                    "error": "Datos incorrectos"
                })
        except get_user_model().DoesNotExist:
            return render(request, 'usuario/login.html', {
                "error": "Correo no registrado"
            })



    


    

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
            return redirect('Tienda')
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




@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()  # Obtener todos los usuarios
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

@user_passes_test(lambda u: u.is_superuser)
def cambiar_rol_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if usuario.is_superuser:
        usuario.is_superuser = False
    else:
        usuario.is_superuser = True
    usuario.save()
    return redirect('lista_usuarios')

def eliminar_usuario(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
    except User.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
    return redirect('lista_usuarios')