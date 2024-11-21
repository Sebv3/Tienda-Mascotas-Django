from pyexpat.errors import messages
from django import template
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CategoriaForm, ContactoForm, ProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import MensajeContacto, Pedido, Producto, Categoria
from babel.numbers import format_currency
from CarritoApp.Carrito import Carrito
from CarritoApp.models import Producto
from CarritoApp import views
from transbank.webpay.webpay_plus.transaction import Transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import get_object_or_404




def iniciar_pago(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['acumulado'] for item in carrito.values())

    transaction = Transaction()
    response = transaction.create(
        buy_order='orden1234',  # Cambia a un valor único
        session_id='sesion1234',
        amount=total,
        return_url=request.build_absolute_uri('/pago-exitoso/')
    )

    # Redirige al usuario a Webpay para completar el pago
    return redirect(response['url'] + '?token_ws=' + response['token'])


def pago_exitoso(request):
    token = request.GET.get('token_ws')
    transaction = Transaction()
    response = transaction.commit(token)

    if response['status'] == 'AUTHORIZED':
        # Pago exitoso, limpia el carrito
        request.session['carrito'] = {}
        return HttpResponse('Pago exitoso. ¡Gracias por tu compra!')
    else:
        return HttpResponse('Error en el pago. Intenta nuevamente.')


def tienda(request):
    categoria_id = request.GET.get('categoria')

    if categoria_id == "" or categoria_id is None:
        productos = Producto.objects.all()  # Mostrar todos los productos
    else:
        productos = Producto.objects.filter(categoria__id=categoria_id)  # Filtrar por categoría

    categorias = Categoria.objects.all()

    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'tienda.html', context)




def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto)
    messages.success(request, "Producto agregado al carrito.")
    return redirect('Tienda')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect("resumenCarrito")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto)
    return redirect("resumenCarrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("resumenCarrito")

def index(request):
    return render(request, 'index.html')


def registrar_usuario(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('Index')  # Redirigir al índice o cualquier otra página adecuada
    
    if request.method == 'GET':
        return render(request, 'usuario/registrar_usuario.html')
    
    else:
        # Verificar si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Verificar si el correo ya está en uso
                if User.objects.filter(email=request.POST['email']).exists():
                    messages.error(request, "El correo ya está registrado.")
                    return redirect('registrar_usuario')
                
                # Crear usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email']
                )
                user.save()

                # Agregar mensaje de éxito
                messages.success(request, "Usuario registrado exitosamente, por favor inicia sesión.")
                
                # Redirigir al login
                return redirect('login')
                
            except IntegrityError:
                messages.error(request, "El usuario ya existe.")
                return redirect('registrar_usuario')
        else:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registrar_usuario')
            
def cerrar_sesion(request):
    logout(request)
    return redirect('Index')

def iniciar_sesion(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('Index')  # Redirigir al índice o cualquier otra página adecuada
    
    if request.method == 'GET':
        return render(request, 'usuario/login.html', {
            'form': AuthenticationForm
        })
    else:
        email = request.POST['username']  # El campo 'username' se usa para capturar el correo
        password = request.POST['password']
        
        try:
            # Buscar el usuario por correo
            user = get_user_model().objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('Index')
            else:
                # Contraseña incorrecta
                messages.error(request, "Contraseña incorrecta.")
                return redirect('login')  # Redirige para mostrar el mensaje de error
        except get_user_model().DoesNotExist:
            # Correo no registrado
            messages.error(request, "Correo no registrado.")
            return redirect('login')



    


def recuperar(request):
    return render(request, 'recuperar.html')

def contacto(request):
    return render(request, 'contacto.html')

def resumenCarrito(request):
    carrito = Carrito(request)
    return render(request, 'resumenCarrito.html', {'carrito': carrito.carrito})

def nosotros(request):
    return render(request, 'nosotros.html')


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

@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new category to the database
            return redirect('Tienda')  # Redirect after successful save
    else:
        form = CategoriaForm()
    
    return render(request, 'agregar_categoria.html', {'form': form})

@login_required
def perfil_usuario(request):
    return render(request, 'perfil_usuario.html', {'usuario': request.user})


#guardar contacto del usuario con admin
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el formulario en la base de datos
            messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')
            return redirect('contacto')  # Redirigir al mismo formulario
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})

#restringir acceso a lista de mensajes de usuarios
@user_passes_test(lambda u: u.is_superuser)
def lista_mensajes(request):
    mensajes = MensajeContacto.objects.all()  # Recuperar todos los mensajes
    return render(request, 'lista_mensajes.html', {'mensajes': mensajes})

#recuperar cuenta
def recuperar_cuenta(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f"/reset-password/{uid}/{token}/"
            )
            
            # Enviar correo electrónico
            send_mail(
                'Restablece tu contraseña',
                f'Usa el siguiente enlace para restablecer tu contraseña: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, "Hemos enviado un enlace para restablecer tu contraseña a tu correo.")
            return redirect('recuperar_cuenta')
        except User.DoesNotExist:
            messages.error(request, "No se encontró una cuenta con ese correo electrónico.")
    
    return render(request, 'recuperar_cuenta.html')

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Tu contraseña se ha restablecido correctamente.")
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, "El enlace no es válido o ha expirado.")
        return redirect('recuperar_cuenta')
    
def es_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(es_admin)
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')  # Lista todos los pedidos ordenados por fecha
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})