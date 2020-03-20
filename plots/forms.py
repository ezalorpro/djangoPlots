from django import forms

class DataForm(forms.Form):
    x_points = forms.CharField(label='Puntos de X', max_length=200, widget=forms.TextInput(
        attrs={'class': "input-field col s12"}))
    
    y_points = forms.CharField(label='Puntos de Y', max_length=200, widget=forms.TextInput(
        attrs={'class': "input-field col s12"}))

    # layout = Layout(x_points, y_points)
