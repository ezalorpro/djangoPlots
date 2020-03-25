from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms

from .models import UserProfile


class DataForm(forms.Form):
    x_points = forms.CharField(label='Puntos de X', max_length=200)
    y_points = forms.CharField(label='Puntos de Y', max_length=200)

 
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nombre', required=False)
    last_name = forms.CharField(label='Apellido',  required=False)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

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
        
