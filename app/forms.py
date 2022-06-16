"""Este es el módulo de forms.
Contiene los formularios que se van a realizar en la web.
"""

from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class crearusuarioform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 
 
class anadirPreguntaForm(ModelForm):
    class Meta:
        model=Cuestionario
        fields="__all__"

class registrarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields =  ['username', 'email']

    # Comprobamos que el correo electrónico único
    # Email existe && cuenta activa -> email_ya_registrado_anteriormente
    # El correo electrónico existe && la cuenta no está activa -> eliminar la cuenta anterior y registrar una nueva
    def clean_email(self):
        email_introducido = self.cleaned_data.get("email")
        email_ya_registrado_anteriormente = User.objects.filter(email = email_introducido).exists()
        user_is_active = User.objects.filter(email = email_introducido, is_active = 1)
        if email_ya_registrado_anteriormente and user_is_active:
            raise forms.ValidationError("Email ya registrado.")
        elif email_ya_registrado_anteriormente:
            User.objects.filter(email = email_introducido).delete()

        return email_introducido