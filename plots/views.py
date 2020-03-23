from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from bokeh.embed import components
from bokeh import plotting as plt

from .forms import DataForm, RegistrationForm

import json

# Create your views here.


def home(request):
    return render(request, 'plots/home.html')


@login_required
def resultsplot(request):
    form = DataForm()

    x_data = [0]
    y_data = [0]

    # the updated/new plot
    p = plt.figure(sizing_mode='scale_width')

    p.line(x_data, y_data)

    script_bok, div_bok = components(p)

    return render(request, 'plots/resultsplot.html', context={
        'form': form,
        'div_bok': div_bok,
        'script_bok': script_bok
    })


def update_data(request):
    # extract nrow, ncol via ajax post - contained in request.form
    data = request.POST
    x_data = json.loads(data['x_points'])
    y_data = json.loads(data['y_points'])

    # the updated/new plot
    p = plt.figure(sizing_mode='scale_width')

    p.line(x_data, y_data)

    script_bok, div_bok = components(p)

    # return rendered html to the browser

    return render(request, 'plots/update_data.html', {
        'div_bok': div_bok,
        'script_bok': script_bok
    })


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('plots:Home')
    else:
        form = RegistrationForm()

    return render(request, 'plots/registrar.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            if request.POST.get('next', None):
                return redirect(request.POST['next'])
            else:
                return redirect('plots:Home')
    else:
        form = AuthenticationForm()
    return render(request, 'plots/user_login.html', {'form': form})


def logoutview(request):
    logout(request)
    return redirect('plots:Home')
