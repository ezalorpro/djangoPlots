from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import UserProfile, Post


class DataForm(forms.Form):
    x_points = forms.CharField(label='Puntos de X', max_length=200)
    y_points = forms.CharField(label='Puntos de Y', max_length=200)


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(label='Nombre (opcional)', required=False)
    last_name = forms.CharField(label='Apellido (opcional)', required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'validate'}),
            'email': forms.EmailInput(attrs={'class': 'validate'}),
            'password1': forms.PasswordInput(attrs={'class': 'validate'}),
            'password2': forms.PasswordInput(attrs={'class': 'validate'}),
        }

        labels = {
            "email": "Correo electronico",
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class EditProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['location'].required = False
        self.fields['gender'].required = False
        self.fields['information'].required = False

    class Meta:
        model = UserProfile
        fields = ('avatar', 'location', 'gender', 'information')

        widgets = {
            'information': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'gender': forms.Select(attrs={'class': 'light-blue-text text-accent-4'}),
        }

        labels = {
            "avatar": "Avatar",
            "location": "Localizacion",
            "gender": "Genero",
            "information": "Informacion",
        }


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'validate'}),
        }

        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electronico",
        }


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True

    class Meta:
        model = Post
        fields = {'title', 'post_text'}

        widgets = {
            'post_text': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }

        labels = {
            'title': 'Titulo',
            'post_text': 'Contenido del post',
        }
