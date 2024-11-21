from django import forms
from .models import Categoria, MensajeContacto, Producto
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'imagen', 'stock', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),  # Updated to Select widget
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {k: '' for k in fields}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo Electrónico")


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
        }

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'itNombre', 
                'aria-describedby': 'nombreHelp'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'itApellido', 
                'aria-describedby': 'apellidoHelp'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control', 
                'id': 'itCorreo', 
                'aria-describedby': 'emailHelp'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'itTelefono', 
                'aria-describedby': 'asuntoHelp'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'itMensaje', 
                'rows': 5
            }),
        }