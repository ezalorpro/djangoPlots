from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect 
from django.forms import inlineformset_factory
from django.http import HttpResponse
from bokeh.embed import components
from bokeh import plotting as plt

from .forms import DataForm, RegistrationForm, EditProfileForm, UserProfileForm
from .models import UserProfile

import json
# Create your views here.


def home(request):
    return render(request, 'plots/home.html')


@login_required
def resultsplot(request):
    if request.method == 'POST':
        data = request.POST
        x_data = json.loads(data['x_points'])
        y_data = json.loads(data['y_points'])

        p = plt.figure(sizing_mode='scale_width')
        p.line(x_data, y_data)

        script_bok, div_bok = components(p)
        
        return HttpResponse([script_bok, div_bok])
    else:
        form = DataForm()
        x_data = [0]
        y_data = [0]

        p = plt.figure(sizing_mode='scale_width')
        p.line(x_data, y_data)
        script_bok, div_bok = components(p)

        return render(request, 'plots/resultsplot.html', context={
            'form': form,
            'div_bok': div_bok,
            'script_bok': script_bok
        })


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            perfil = UserProfile(user=usuario)
            perfil.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('plots:Home')
    else:
        form = RegistrationForm()
        print(form)

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


def profile(request):
    perfil = UserProfile.objects.get(user=request.user)
    return render(request, 'plots/profile.html', {
        'perfil': perfil
    })


def edit_profile(request):

    if request.method == 'POST':
        
        perfil = UserProfile.objects.get(user=request.user)
        usuario = User.objects.get(username=request.user.username)
        userForm = UserProfileForm(request.POST, instance=usuario)
        perfilForm = EditProfileForm(
            request.POST, request.FILES, instance=perfil)
        
        if userForm.is_valid():
            userForm.save()
            perfilForm.save()
            
            perfil = UserProfile.objects.get(user=request.user)
            
            return render(request, 'plots/profile.html', {
                'perfil': perfil
            })
        else:
            return render(request, 'plots/edit_profile.html', {
                'userForm': userForm,
                'perfilForm': perfilForm
            })
        
    else:
        perfil = UserProfile.objects.get(user=request.user)
        usuario = User.objects.get(username=request.user.username)
        userForm = UserProfileForm(instance=usuario)
        perfilForm = EditProfileForm(instance=perfil)
        return render(request, 'plots/edit_profile.html', {
            'userForm': userForm,
            'perfilForm': perfilForm
        })
