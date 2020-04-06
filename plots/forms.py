from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import Post, UserModel


class DataForm(forms.Form):
    
    x_points = forms.CharField(
        label='Puntos de X', 
        max_length=200, 
        widget=forms.TextInput(
            attrs={
                'placeholder': '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]'
                }
            )
        )
    
    y_points = forms.CharField(
        label='Puntos de Y', 
        max_length=200, 
        widget=forms.TextInput(
            attrs={
                'placeholder': '[0, 1, 1.5, 1.8, 2, 2.1, 2.15, 2.17, 2.18, 2.185]'
                }
            )
        )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2'
            )

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'validate',
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'validate',
                    }
                ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'validate',
                    }
                ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'validate',
                    }
                )
            }

        labels = {
            'email': 'Correo electronico',
            'first_name': 'Nombre (opcional)',
            'last_name': 'Apellido (opcional)',
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'validate'
                }
            )

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'validate'
                }
            )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'autofocus': True,
                'placeholder': 'usuario'
                }
            )
        
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password', 
                'placeholder': 'Contraseña'
                }
            )


class EditProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['location'].required = False
        self.fields['gender'].required = False
        self.fields['information'].required = False

    class Meta:
        model = UserModel
        fields = (
            'avatar', 'first_name', 'last_name',
            'email', 'location', 'gender', 
            'information'
            )

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Primer nombre'
                    }
                ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Primer apellido'
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'validate', 'placeholder': 'correo@mail.com'
                    }
                ),
            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Pais, ciudad y/o estado'
                    }
                ),
            'information': forms.Textarea(
                attrs={
                    'class': 'materialize-textarea',
                    'placeholder': 'Cualquier informacion adicional'
                    }
                ),
            'gender': forms.Select(
                attrs={
                    'class': 'light-blue-text text-accent-4'
                    }
                ),
            }

        labels = {
            "avatar": "Avatar",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electronico",
            "location": "Localizacion",
            "gender": "Genero",
            "information": "Informacion",
        }


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True

    class Meta:
        model = Post
        fields = {'title', 'post_text'}

        widgets = {
            'post_text': forms.Textarea(attrs={
                'class': 'materialize-textarea', 'placeholder': 'Contenido del post...'
            }),
            'title': forms.TextInput(attrs={'placeholder': 'Titulo del post'})
        }

        labels = {
            'title': 'Titulo',
            'post_text': 'Contenido del post',
        }
