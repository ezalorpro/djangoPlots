from django import forms
from .models import UserModel


class DataForm(forms.Form):
    x_points = forms.CharField(label='Puntos de X', max_length=200)
    y_points = forms.CharField(label='Puntos de Y', max_length=200)


class UserForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
