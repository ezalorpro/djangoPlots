from django.urls import path
from . import views

app_name = 'plots'

urlpatterns = [
    path('', views.home, name='Home'),
    path('resultsplot/', views.resultsplot, name='resultsplot'),
    path('_update_data', views.update_data, name='update_data'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('profile', views.profile, name='profile'),
    path('registrar/', views.signup, name='registrar'),
    path('logout/', views.logoutview, name='logout'),
    path('user_login/', views.user_login, name='user_login'),
]
