import json

from bokeh import plotting as plt
from bokeh.embed import components
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .forms import (DataForm, EditProfileForm, PostForm, RegistrationForm,
                    UserLoginForm)
from .models import Post, UserModel


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
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('plots:Home')
    elif request.is_ajax():
        if request.GET.get('tipo') == 'username':
            data = {
                'flag': UserModel.objects.filter(username=request.GET.get('name', None)).exists()
            }
        elif request.GET.get('tipo') == 'email':
            try:
                validate_email(request.GET.get('email', None))
                if UserModel.objects.filter(email=request.GET.get('email', None)).exists():
                    data = {
                        'flag': False,
                        'info': 'Correo electronico ya registrado, ingrese otro',
                    }
                else:
                    data = {
                        'flag': True,
                        'info': '',
                    }
            except ValidationError as e:
                data = {
                    'flag': False,
                    'info': 'Ingrese una dirección de correo electrónico válida.',
                }                
        return JsonResponse(data)
    else: 
        form = RegistrationForm()

    return render(request, 'plots/registrar.html', {'form': form})


# def username_validation(request):
#     print('holas')
#     return HttpResponse('succes')


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
    usuario = UserModel.objects.get(username=request.user.username)
    post_object = Post.objects.filter(user=request.user)
    post_list = [item for item in post_object]
    return render(request, 'plots/profile.html', {
        'usuario': usuario,
        'post_list': post_list
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        usuario = UserModel.objects.get(username=request.user.username)
        perfilForm = EditProfileForm(
            request.POST, 
            request.FILES, 
            instance=usuario
            )

        if perfilForm.is_valid():
            perfilForm.save()
            return redirect('plots:profile')
        else:
            return render(request, 'plots/edit_profile.html', {
                'perfilForm': perfilForm
            })
    else:
        usuario = UserModel.objects.get(username=request.user.username)
        perfilForm = EditProfileForm(instance=usuario)
        return render(request, 'plots/edit_profile.html', {
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
