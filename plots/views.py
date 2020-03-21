from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from plotly.offline import plot

from .forms import DataForm, UserForm

import plotly.graph_objs as go
import numpy as np
import json

# Create your views here.

def home(request):
    if request.method == 'POST':
        data = request.POST
        x_data = json.loads(data['x_points'])
        y_data = json.loads(data['y_points'])

        trace = go.Scatter(x=x_data, y=y_data,
                        mode='lines', name='sin',
                        opacity=1, marker_color='blue')
        dataPlot = [trace]
        layout = go.Layout(
            margin=dict(l=10, r=20, t=40, b=20),
            xaxis=dict(autorange=True),
            yaxis=dict(autorange=True)
        )

        fig = go.Figure(data=dataPlot, layout=layout)

        plot_div = plot(fig, output_type='div',
                        include_plotlyjs=True, show_link=False)
        
        form = DataForm(data)

        return render(request, 'plots/home.html', context={
            'form': form,
            'plot_div': plot_div
        })
    else:
        form = DataForm()
        return render(request, 'plots/home.html', context={'form': form})


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


def logoutview(request):
    logout(request)
    return redirect('plots:Home')
 

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('plots:Home')
        else:
            messages.error(request, 'Usuario y/o contraseña incorrecto/s')
            return redirect('plots:user_login')
    
    form = AuthenticationForm()
    return render(request, 'plots/user_login.html', {'form': form})
    
    
def resultsplot(request):
    data = request.POST
    x_data = json.loads(data['x_points'])
    y_data = json.loads(data['y_points'])

    trace = go.Scatter(x=x_data, y=y_data,
                       mode='lines', name='sin',
                       opacity=0.8, marker_color='blue')
    data = [trace]
    layout = go.Layout(
        margin=dict(l=10, r=20, t=40, b=20),
        xaxis=dict(autorange=True),
        yaxis=dict(autorange=True)
    )

    fig = go.Figure(data=data, layout=layout)

    plot_div = plot(fig, output_type='div',
                    include_plotlyjs=True, show_link=False)
    return render(request, 'plots/resultsplot.html', context={'plot_div': plot_div})
