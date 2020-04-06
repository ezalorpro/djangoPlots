from django.urls import path

from . import views

app_name = 'plots'

urlpatterns = [
    path('', views.home, name='Home'),
    path('resultsplot/', views.resultsplot, name='resultsplot'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('profile', views.profile, name='profile'),
    path('registrar/', views.signup, name='registrar'),
    path('logout/', views.logoutview, name='logout'),
    path('user_login/', views.user_login, name='user_login'),
    path('post/<int:post_id>/', views.post_view, name='post'),
    path('posts/', views.list_of_post, name='list_post'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('new_post/', views.new_post, name='new_post'),
]
