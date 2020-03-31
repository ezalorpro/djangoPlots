from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from bokeh.embed import components
from bokeh import plotting as plt

from .forms import DataForm, RegistrationForm, EditProfileForm, UserProfileForm, PostForm, UserLoginForm
from .models import UserProfile, Post

import json
# Create your views here.


def maindomain(request):
    return redirect('plots:Home')


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

    return render(request, 'plots/registrar.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
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
        form = UserLoginForm()
    return render(request, 'plots/user_login.html', {'form': form})


@login_required
def logoutview(request):
    logout(request)
    return redirect('plots:Home')


@login_required
def profile(request):
    perfil = UserProfile.objects.get(user=request.user)
    post_object = Post.objects.filter(user=request.user)
    post_list = [item for item in post_object]
    return render(request, 'plots/profile.html', {
        'perfil': perfil,
        'post_list': post_list
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        perfil = UserProfile.objects.get(user=request.user)
        usuario = User.objects.get(username=request.user.username)
        userForm = UserProfileForm(request.POST, instance=usuario)
        perfilForm = EditProfileForm(
            request.POST, request.FILES, instance=perfil)

        if userForm.is_valid() and perfilForm.is_valid():
            userForm.save()
            perfilForm.save()

            perfil = UserProfile.objects.get(user=request.user)

            return redirect('plots:profile')
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


@login_required
def list_of_post(request):
    post_object = Post.objects.filter(user=request.user)
    post_list = [item for item in post_object]
    return render(request, 'plots/list_post.html', context={'post_list': post_list})


@login_required
def post_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'plots/post_template.html', context=context)


@login_required
def edit_post(request, post_id):
    if request.method == 'POST':

        post = Post.objects.get(pk=post_id)
        post_form = PostForm(request.POST, instance=post)

        if post_form.is_valid():
            post_form.save()
            post = Post.objects.get(pk=post_id)

            return redirect('plots:post', post_id=post_id)
        else:
            return render(request, 'plots/edit_post.html', {
                'post_form': post_form,
                'post': post,
            })
    else:
        post = Post.objects.get(pk=post_id)
        post_form = PostForm(instance=post)
        return render(request, 'plots/edit_post.html', {
            'post_form': post_form,
            'post': post,
        })


@login_required
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
        return redirect('plots:profile')
    else:
        return redirect('plots:Home')


@login_required
def new_post(request):
    if request.method == 'POST':
        post = Post(user=request.user)
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            return redirect('plots:post', post_id=post.id)
        else:
            return render(request, 'plots/new_post.html', {
                'post_form': post_form,
            })
    else:
        post_form = PostForm()
        return render(request, 'plots/new_post.html', {
            'post_form': post_form,
        })
