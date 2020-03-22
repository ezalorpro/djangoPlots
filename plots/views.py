from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from bokeh.embed import components
from bokeh import plotting as plt

from .forms import DataForm

import numpy as np
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
    print(data)
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('plots:Home')
    else:
        form = UserCreationForm()

    return render(request, 'plots/registrar.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return redirect('plots:Home')
            else:
                messages.error(request, 'Usuario y/o contraseña incorrecto/s')
                return render(request, 'plots/user_login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'plots/user_login.html', {'form': form})


def logoutview(request):
    logout(request)
    return redirect('plots:Home')
