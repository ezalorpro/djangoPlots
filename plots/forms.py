from django import forms
from .models import UserModel
from django.utils.translation import gettext, gettext_lazy as _


class DataForm(forms.Form):
    x_points = forms.CharField(label='Puntos de X', max_length=200)
    y_points = forms.CharField(label='Puntos de Y', max_length=200)


class UserForm(forms.Form):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }
