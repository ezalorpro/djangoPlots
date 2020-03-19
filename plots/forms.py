from django import forms
from material import Layout

class DataForm(forms.Form):
    x_points = forms.CharField(label='Puntos de X', max_length=200, widget=forms.TextInput(
        attrs={'class': "mdl-textfield__input"}))
    
    y_points = forms.CharField(label='Puntos de Y', max_length=200, widget=forms.TextInput(
        attrs={'class': "mdl-textfield__input"}))
    
    # layout = Layout(x_points, y_points)
